from rest_framework import serializers
from tasks.models import Task
from api.serializers.common_serializers import UserSerializer
from api.serializers.workspace_projects import WorkSpaceProjectMembersSerializer
from api.serializers.comment_serializer import CommentSerializer


class ProjectTaskSerializer(serializers.ModelSerializer):
    assigned_to = WorkSpaceProjectMembersSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'assigned_to',
            'created_by',
            'status',
            'due_date',
            'created_at',
            'updated_at',
            'comments'
        ]

    def get_comments(self, obj):
        top_level_comments = obj.comments.filter(parent_comment__isnull=True).select_related('author')
        return CommentSerializer(top_level_comments, many=True).data


class CreateTaskSerializer(serializers.ModelSerializer):
    """Used for creating and updating tasks. assigned_to accepts ProjectMember pk."""

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_to', 'status', 'due_date']
        read_only_fields = ['id']


class DashboardTaskSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source='assigned_to.user.username', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'status',
            'due_date',
            'assigned_to_name',
            'project_name',
        ]
