from rest_framework import serializers
from tasks.models import Task
from api.serializers.common_serializers import UserSerializer
from api.serializers.workspace_projects import WorkSpaceProjectMembersSerializer
from api.serializers.comment_serializer import CommentSerializer
from projects.models import ProjectMember
from rest_framework.pagination import PageNumberPagination

class TaskPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'  # optional (user change kar sakta)
    max_page_size = 50

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
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=ProjectMember.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_to', 'status', 'due_date']
        read_only_fields = ['id']


class DashboardTaskSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source='assigned_to.member.username', read_only=True)
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



class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    workspace_name = serializers.CharField(source='project.workspace.name', read_only=True)

    assigned_to = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
  

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'due_date',
            'created_at',
            'updated_at',

            # relations
            'project_name',
            'workspace_name',
            'assigned_to',
            'created_by',
        ]

    def get_assigned_to(self, obj):
        if obj.assigned_to and obj.assigned_to.member:
            return {
                "id": obj.assigned_to.member.id,
                "name": obj.assigned_to.member.first_name,
                "email": obj.assigned_to.member.email,
            }
        return None

    def get_created_by(self, obj):
        return {
            "id": obj.created_by.id,
            "name": obj.created_by.first_name,
            "email": obj.created_by.email,
        }