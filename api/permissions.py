from rest_framework import permissions
from workspaces.models import WorkspaceMember

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != "POST":
            return True

        workspace_slug = view.kwargs.get("workspace_slug")
        try:
            member = WorkspaceMember.objects.get(
                workspace__slug=workspace_slug,
                user=request.user,
                is_active=True
            )
        except WorkspaceMember.DoesNotExist:
            return False
        return member.role in ['manager']
      