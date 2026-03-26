from rest_framework import generics
from workspaces.models import WorkspaceMember, Workspace
from projects.models import ProjectMember   # 👈 ADD THIS
from api.serializers.workspace_members import WorkSpaceMemberSerializer
from rest_framework import permissions
from api.permissions import IsManager


class ListCreateWorkspaceMembersApiView(generics.ListCreateAPIView):
    
    serializer_class = WorkSpaceMemberSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def get_queryset(self):
        slug = self.kwargs['workspace_slug']

        queryset = WorkspaceMember.objects.filter(
            workspace__slug=slug,
            is_active=True
        ).select_related('user')

        project_slug = self.request.query_params.get("exclude_project")

        if project_slug:
            project_members = ProjectMember.objects.filter(
                project__slug=project_slug,
                project__workspace__slug=slug
            ).values_list('member_id', flat=True)

            queryset = queryset.exclude(user_id__in=project_members)

        return queryset

    def perform_create(self, serializer):
        workspace = Workspace.objects.get(slug=self.kwargs['workspace_slug'])
        serializer.save(workspace=workspace)    