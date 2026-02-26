from rest_framework import generics
from workspaces.models import WorkspaceMember,Workspace
from api.serializers.workspace_members import WorkSpaceMemberSerializer
from rest_framework import permissions
from api.permissions import IsManager
class ListCreateWorkspaceMembersApiView(generics.ListCreateAPIView):
    
    serializer_class=WorkSpaceMemberSerializer
    permission_classes=[permissions.IsAuthenticated,IsManager]

    def get_queryset(self):
        slug = self.kwargs['workspace_slug']
        return WorkspaceMember.objects.filter(
            workspace__slug=slug,
            is_active=True
        ).select_related('user')
    def perform_create(self, serializer):
        workspace=Workspace.objects.get(slug=self.kwargs['workspace_slug'])
        serializer.save(workspace=workspace)
    

    
