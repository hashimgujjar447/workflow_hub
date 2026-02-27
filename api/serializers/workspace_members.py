from rest_framework import serializers
from workspaces.models import WorkspaceMember
from api.serializers.common_serializers import UserSerializer


class WorkSpaceMemberSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)

    class Meta:
        model = WorkspaceMember
        fields = ['user', 'user_detail', 'role', 'joined_at', 'is_active']
        extra_kwargs = {
            'user': {'write_only': True}
        }