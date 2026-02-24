from rest_framework import serializers
from api.serializers.common_serializers import UserSerializer
from comments.models import TaskComment


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = TaskComment
        fields = ['task', 'author', 'content', 'created_at', 'updated_at']