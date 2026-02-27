from rest_framework import serializers
from projects.models import ProjectMember
from api.serializers.common_serializers import UserSerializer


class ProjectMemberSerializer(serializers.ModelSerializer):
    member_detail = UserSerializer(source='member', read_only=True)

    class Meta:
        model = ProjectMember
        fields = ['member', 'member_detail', 'role', 'joined_at', 'is_active']
        extra_kwargs = {
            'member': {'write_only': True}
        }