from rest_framework import serializers
from api.serializers.common_serializers import UserSerializer
from comments.models import TaskComment


class CommentDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = TaskComment
        fields = [
            'id',
            'content',
            'author',
            'created_at',
            'replies'
        ]

    def get_replies(self, obj):
        replies = obj.replies.all()
        return CommentDetailSerializer(replies, many=True).data