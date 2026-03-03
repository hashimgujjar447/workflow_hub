from rest_framework import permissions
from workspaces.models import Workspace, WorkspaceMember
from projects.models import ProjectMember, Project


class IsProjectMember(permissions.BasePermission):
    """Allow access only to active members of the project."""

    def has_permission(self, request, view):
        workspace_slug = view.kwargs.get("workspace_slug")
        project_slug = view.kwargs.get("project_slug")
        return ProjectMember.objects.filter(
            project__workspace__slug=workspace_slug,
            project__slug=project_slug,
            member=request.user,
            is_active=True
        ).exists()


class IsManager(permissions.BasePermission):

    def has_permission(self, request, view):
        # Allow safe methods (GET etc.)
        if request.method in permissions.SAFE_METHODS:
            return True

        workspace_slug = view.kwargs.get("workspace_slug")
        if not workspace_slug:
            return False

        # Workspace creator always has manager-level access
        if Workspace.objects.filter(slug=workspace_slug, creator=request.user).exists():
            return True

        try:
            member = WorkspaceMember.objects.get(
                workspace__slug=workspace_slug,
                user=request.user,
                is_active=True
            )
        except WorkspaceMember.DoesNotExist:
            return False

        # Allow only manager for update/delete
        return member.role == 'manager'
    

class IsManagerOrLeader(permissions.BasePermission):

    def has_permission(self, request, view):
        workspace_slug = view.kwargs.get("workspace_slug")
        project_slug = view.kwargs.get("project_slug")

        # -----------------------------
        # ✅ SAFE METHODS (GET, HEAD, OPTIONS)
        # Allow if user is Project Member
        # -----------------------------
        if request.method in permissions.SAFE_METHODS:
            return ProjectMember.objects.filter(
                project__workspace__slug=workspace_slug,
                project__slug=project_slug,
                member=request.user,
                is_active=True
            ).exists()

        # -----------------------------
        # ✅ WRITE METHODS
        # Allow only manager or leader in Workspace (or workspace creator)
        # -----------------------------
        if Workspace.objects.filter(slug=workspace_slug, creator=request.user).exists():
            return True

        try:
            workspace_member = WorkspaceMember.objects.get(
                workspace__slug=workspace_slug,
                user=request.user,
                is_active=True
            )
        except WorkspaceMember.DoesNotExist:
            return False

        return workspace_member.role in ['manager', 'leader']