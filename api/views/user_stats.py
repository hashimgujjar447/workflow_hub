from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count

from workspaces.models import Workspace
from projects.models import Project, ProjectMember


class UserStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        workspaces_count = Workspace.objects.filter(
            members__user=user
        ).distinct().count()

        projects_count = Project.objects.filter(
            workspace__members__user=user
        ).distinct().count()

        project_memberships = ProjectMember.objects.filter(
            member=user,
            is_active=True
        ).count()

        return Response({
            "workspaces_count": workspaces_count,
            "projects_count": projects_count,
            "project_memberships": project_memberships,
        })