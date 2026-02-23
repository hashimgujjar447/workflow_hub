from rest_framework import generics
from workspaces.models import WorkspaceMember
from api.serializers.workspace_members import WorkSpaceMemberSerializer

class ListCreateWorkspaceMembersApiView(generics.ListCreateAPIView):
    
    serializer_class=WorkSpaceMemberSerializer

    def get_queryset(self):
        slug = self.kwargs['workspace_slug']
        return WorkspaceMember.objects.filter(
            workspace__slug=slug,
            is_active=True
        ).select_related('user')

    
