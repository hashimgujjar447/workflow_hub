from rest_framework import generics
from tasks.models import Task
from api.serializers.task_serializers import ProjectTaskSerializer, CreateTaskSerializer
from rest_framework import permissions
from api.permissions import IsProjectMember, IsManagerOrLeader


class RetrieveTaskApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsProjectMember]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return CreateTaskSerializer
        return ProjectTaskSerializer

    def get_queryset(self):
        workspace_slug = self.kwargs['workspace_slug']
        project_slug = self.kwargs['project_slug']
        return Task.objects.filter(
            project__workspace__slug=workspace_slug,
            project__slug=project_slug,
        ).select_related(
            "project",
            "created_by",
            "assigned_to",
            "assigned_to__member"
        ).prefetch_related(
            "comments"
        )