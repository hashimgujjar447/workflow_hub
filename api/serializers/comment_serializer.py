from rest_framework import serializers
from api.serializers.common_serializers import UserSerializer
from comments.models import TaskComment
from rest_framework.pagination import PageNumberPagination

class CommentPagination(PageNumberPagination):
    page_size = 5

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = TaskComment
        fields = [ 'author', 'content', 'created_at', 'updated_at','parent_comment']