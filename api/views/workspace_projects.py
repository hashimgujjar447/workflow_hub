from rest_framework import generics
from projects.models import Project, ProjectMember
from api.serializers.workspace_projects import WorkspaceProjectSerializer, WorkspaceProjectDetailSerializer
from django.db.models import Q
from django.utils.text import slugify
from workspaces.models import Workspace
from api.serializers.project_member_serializer import ProjectMemberSerializer
from django.db.models import Count
from tasks.models import Task
from api.serializers.task_serializers import ProjectTaskSerializer, CreateTaskSerializer
from rest_framework import permissions
from api.permissions import IsManagerOrLeader, IsProjectMember


class WorkspaceProjectApiView(generics.ListCreateAPIView):
      queryset = Project.objects.all()
      serializer_class = WorkspaceProjectSerializer
      permission_classes = [permissions.IsAuthenticated]

      def get_queryset(self):
            slug = self.kwargs['workspace_slug']
            qs = super().get_queryset()
            return qs.filter(workspace__slug=slug)

      def perform_create(self, serializer):
            workspace = Workspace.objects.get(slug=self.kwargs["workspace_slug"])
            project = serializer.save(
                workspace=workspace,
                created_by=self.request.user
            )
            # Automatically add creator as Project Manager
            ProjectMember.objects.create(
                project=project,
                member=self.request.user,
                role=ProjectMember.ROLE_MANAGER
            )


class WorkspaceProjectDetailsApiView(generics.RetrieveUpdateDestroyAPIView):
      serializer_class = WorkspaceProjectDetailSerializer
      permission_classes = [permissions.IsAuthenticated, IsManagerOrLeader]
      lookup_field = "slug"
      lookup_url_kwarg = "project_slug"

      def get_queryset(self):
           return Project.objects.filter(
                workspace__slug=self.kwargs["workspace_slug"]
           ).filter(
                Q(workspace__creator=self.request.user) |
                Q(workspace__members__user=self.request.user)
           ).distinct().annotate(
                total_members=Count(
                    "members",
                    filter=Q(members__is_active=True),
                    distinct=True
                )
           )


class ProjectTasksApiView(generics.ListCreateAPIView):
      permission_classes = [permissions.IsAuthenticated, IsProjectMember]

      def get_serializer_class(self):
            if self.request.method == 'POST':
                return CreateTaskSerializer
            return ProjectTaskSerializer

      def get_queryset(self):
            workspace_slug = self.kwargs["workspace_slug"]
            project_slug = self.kwargs["project_slug"]
            return Task.objects.filter(
                project__workspace__slug=workspace_slug,
                project__slug=project_slug
            ).select_related(
                "project", "created_by", "assigned_to", "assigned_to__member"
            ).prefetch_related("comments")

      def perform_create(self, serializer):
            workspace_slug = self.kwargs["workspace_slug"]
            project_slug = self.kwargs["project_slug"]
            project = Project.objects.get(
                slug=project_slug,
                workspace__slug=workspace_slug
            )
            serializer.save(project=project, created_by=self.request.user)


class ProjectMembersApiView(generics.ListCreateAPIView):
     queryset = ProjectMember.objects.all()
     serializer_class = ProjectMemberSerializer
     permission_classes = [permissions.IsAuthenticated, IsManagerOrLeader]

     def get_queryset(self):
          project_slug = self.kwargs["project_slug"]
          workspace_slug = self.kwargs["workspace_slug"]
          return ProjectMember.objects.filter(
              project__slug=project_slug,
              project__workspace__slug=workspace_slug,
              is_active=True
          ).select_related('member')

     def perform_create(self, serializer):
            project_slug = self.kwargs["project_slug"]
            workspace_slug = self.kwargs["workspace_slug"]
            project = Project.objects.get(slug=project_slug, workspace__slug=workspace_slug)
            serializer.save(project=project)