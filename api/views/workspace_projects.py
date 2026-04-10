from rest_framework import generics, permissions
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from collections import defaultdict
from rest_framework.response import Response

from projects.models import Project, ProjectMember
from workspaces.models import Workspace
from tasks.models import Task

from api.serializers.workspace_projects import (
    WorkspaceProjectSerializer,
    WorkspaceProjectDetailSerializer,
)
from api.serializers.project_member_serializer import ProjectMemberSerializer
from api.serializers.task_serializers import (
    ProjectTaskSerializer,
    CreateTaskSerializer,
)

from api.permissions import IsManagerOrLeader,IsManager


from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics, permissions
from projects.models import Project, ProjectMember
from workspaces.models import Workspace
from rest_framework.exceptions import PermissionDenied



class WorkspaceProjectApiView(generics.ListCreateAPIView):
    serializer_class = WorkspaceProjectSerializer
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsManager()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        slug = self.kwargs['workspace_slug']
        user = self.request.user

        workspace = get_object_or_404(Workspace, slug=slug)

     
        if workspace.creator == user:
            return Project.objects.filter(workspace=workspace)

       
        workspace_member = workspace.members.filter(user=user).first()

        if workspace_member and workspace_member.role in ["manager", "leader"]:
            return Project.objects.filter(workspace=workspace)
      
        return Project.objects.filter(
            workspace=workspace,
            members__member=user,  # 👈 IMPORTANT
            members__is_active=True
        ).distinct()

    def perform_create(self, serializer):
        workspace = get_object_or_404(
            Workspace, slug=self.kwargs["workspace_slug"]
        )

        project = serializer.save(
            workspace=workspace,
            created_by=self.request.user
        )

        # ✅ safe create (no duplicate crash)
        ProjectMember.objects.get_or_create(
            project=project,
            member=self.request.user,
            defaults={'role': ProjectMember.ROLE_MANAGER}
        )


class WorkspaceProjectDetailsApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkspaceProjectDetailSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "project_slug"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            permission_classes = [permissions.IsAuthenticated, IsManagerOrLeader]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

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

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTaskSerializer
        return ProjectTaskSerializer

    def get_project(self):
        return get_object_or_404(
            Project,
            slug=self.kwargs["project_slug"],
            workspace__slug=self.kwargs["workspace_slug"]
        )

    def is_project_member(self, project):
        return ProjectMember.objects.filter(
            project=project,
            member=self.request.user,
            is_active=True
        ).exists()

    def get_queryset(self):
        project = self.get_project()

        # 🔐 ONLY project members can see tasks
        if not self.is_project_member(project):
            return Task.objects.none()

        return Task.objects.filter(
            project=project
        ).select_related(
            "project", "created_by", "assigned_to", "assigned_to__member"
        ).prefetch_related("comments")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        grouped = defaultdict(list)

        for task in serializer.data:
            status = task.get("status", "todo")
            grouped[status].append(task)

        return Response({
            "todo": grouped.get("todo", []),
            "inprogress": grouped.get("in_progress", []),
            "failed": grouped.get("failed", []),
            "completed": grouped.get("completed", []),
        })

    def perform_create(self, serializer):
        project = self.get_project()

        # 🔐 ONLY project members can create tasks
        if not self.is_project_member(project):
            raise PermissionDenied("You are not a member of this project")

        serializer.save(
            project=project,
            created_by=self.request.user
        )


class ProjectMembersApiView(generics.ListCreateAPIView):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [permissions.IsAuthenticated, IsManagerOrLeader]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

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

        project = get_object_or_404(
            Project,
            slug=project_slug,
            workspace__slug=workspace_slug
        )

        serializer.save(project=project)