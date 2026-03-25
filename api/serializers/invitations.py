from rest_framework import serializers
from invitations.models import WorkspaceInvite
from api.serializers.workspace import WorkspaceSerializer

class WorkspaceInviteSerializer(serializers.ModelSerializer):
    workspace=WorkspaceSerializer()
    class Meta:
        model = WorkspaceInvite
        fields = '__all__'