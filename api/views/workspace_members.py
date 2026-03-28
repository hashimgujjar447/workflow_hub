from rest_framework import generics
from workspaces.models import WorkspaceMember, Workspace
from projects.models import ProjectMember   # 👈 ADD THIS
from api.serializers.workspace_members import WorkSpaceMemberSerializer
from rest_framework import permissions
from api.permissions import IsManager
from api.permissions import IsManager
from django.shortcuts import get_object_or_404

class ListCreateWorkspaceMembersApiView(generics.ListCreateAPIView):
    
    serializer_class = WorkSpaceMemberSerializer

    def get_queryset(self):
        slug = self.kwargs['workspace_slug']

        # 🔐 secure access
        if not WorkspaceMember.objects.filter(
            workspace__slug=slug,
            user=self.request.user,
            is_active=True
        ).exists() and not Workspace.objects.filter(
            slug=slug,
            creator=self.request.user
        ).exists():
            return WorkspaceMember.objects.none()

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

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsManager()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        workspace = get_object_or_404(
            Workspace,
            slug=self.kwargs['workspace_slug']
        )
        serializer.save(workspace=workspace)