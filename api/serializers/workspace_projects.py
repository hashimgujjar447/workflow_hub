from rest_framework import serializers
from projects.models import Project, ProjectMember
from api.serializers.common_serializers import UserSerializer


class WorkspaceProjectSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Project
        fields = ('name', 'slug', 'created_at', 'is_active', 'status')


class WorkSpaceProjectMembersSerializer(serializers.ModelSerializer):
    member = UserSerializer(read_only=True)

    class Meta:
        model = ProjectMember
        fields = ('id','member', 'role', 'is_active', 'joined_at')


class WorkspaceProjectDetailSerializer(serializers.ModelSerializer):
    total_members = serializers.IntegerField(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = (
            'name',
            'slug',
            'created_at',
         
            'total_members',
            'is_active',
            'created_by',
            'status',
        )