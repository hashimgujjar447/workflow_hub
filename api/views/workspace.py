from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from workspaces.models import Workspace
from api.serializers.workspace import WorkspaceSerializer
from django.db.models import Q




class WorkspaceViewSet(ModelViewSet):
    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        user = self.request.user

        return (
            Workspace.objects
            .filter(Q(creator=user) | Q(members__user=user))
            .distinct()
            .prefetch_related("members", "members__user")
        )

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)