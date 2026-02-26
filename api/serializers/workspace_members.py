from rest_framework import serializers
from workspaces.models import WorkspaceMember
from api.serializers.common_serializers import UserSerializer


class WorkSpaceMemberSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = WorkspaceMember
        fields = ['user', 'role', 'joined_at', 'is_active']