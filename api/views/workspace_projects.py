from rest_framework import generics
from projects.models import Project,ProjectMember
from api.serializers.workspace_projects import WorkspaceProjectSerializer,WorkspaceProjectDetailSerializer
from django.db.models import Q
from django.utils.text import slugify
from workspaces.models import Workspace
from django.db.models import Count
from tasks.models import Task
from api.serializers.task_serializers import ProjectTaskSerializer
class WorkspaceProjectApiView(generics.ListCreateAPIView):
      queryset=Project.objects.all()
      serializer_class=WorkspaceProjectSerializer
      def get_queryset(self):
            slug=self.kwargs['workspace_slug']
            qs=super().get_queryset()
            return qs.filter(workspace__slug=slug)
      def perform_create(self, serializer):
            workspace=Workspace.objects.get(slug=self.kwargs["workspace_slug"])
            serializer.save(workspace=workspace)
      
     


class WorkspaceProjectDetailsApiView(generics.RetrieveUpdateDestroyAPIView):
     
      serializer_class=WorkspaceProjectDetailSerializer
     
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
      
      

class ProjectTasksApiView(generics.ListAPIView):
      queryset=Task.objects.all()
      
      serializer_class=ProjectTaskSerializer
            