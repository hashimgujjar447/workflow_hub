from rest_framework import generics
from tasks.models import Task
from api.serializers.task_serializers import ProjectTaskSerializer
from rest_framework import permissions
class RetrieveTaskApiView(generics.RetrieveUpdateDestroyAPIView):
    
       serializer_class=ProjectTaskSerializer
       permission_classes=[permissions.IsAuthenticated]
    
       def get_queryset(self):
              workspace_slug=self.kwargs['workspace_slug']
              project_slug=self.kwargs['project_slug']
              return Task.objects.filter(
                     project__workspace__slug=workspace_slug,
                     project__slug=project_slug,
                     project__workspace__members__user=self.request.user
                     ).select_related(
            "project",
            "created_by"
        ).prefetch_related(
            "comments"
        )