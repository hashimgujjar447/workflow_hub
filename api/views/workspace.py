from rest_framework import generics
from workspaces.models import Workspace,WorkspaceMember
from api.serializers.workspace import WorkspaceSerializer
from django.db.models import Count,Q
from rest_framework import permissions
class ListCreateWorkspaceView(generics.ListCreateAPIView):
   
    serializer_class=WorkspaceSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
      
        return Workspace.objects.filter(creator=self.request.user).annotate(
            total_members=Count('members', distinct=True),
            total_projects=Count('projects', distinct=True)
        ).order_by('-created_at')
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        super().perform_create(serializer)
    
class WorkSpaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkspaceSerializer
    lookup_field = 'slug'
    lookup_url_kwarg='workspace_slug'
    permission_classes = [permissions.IsAuthenticated]   # ✅ sirf login user allowed

    def get_queryset(self):
        return (
            Workspace.objects
            .annotate(
                total_members=Count(
                    'members',
                    filter=Q(members__is_active=True),
                    distinct=True
                ),
                total_projects=Count('projects', distinct=True)
            )
        )