from rest_framework import serializers
from projects.models import ProjectMember
from api.serializers.common_serializers import UserSerializer


class ProjectMemberSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProjectMember
        fields = ['member', 'role', 'joined_at', 'is_active']

        