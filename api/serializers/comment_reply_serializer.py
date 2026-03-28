from rest_framework import serializers
from api.serializers.common_serializers import UserSerializer
from comments.models import TaskComment


from rest_framework import serializers
from api.serializers.common_serializers import UserSerializer
from comments.models import TaskComment


class CommentDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    user_reaction = serializers.SerializerMethodField()

    class Meta:
        model = TaskComment
        fields = [
            'id',
            'content',
            'author',
            'created_at',
            'replies',
            'parent_comment',
            'likes',
            'dislikes',
            'user_reaction',
        ]

    def get_replies(self, obj):
        replies = obj.replies.all()
        return CommentDetailSerializer(
            replies,
            many=True,
            context=self.context
        ).data

    def get_likes(self, obj):
        return obj.reactions.filter(reaction='like').count()

    def get_dislikes(self, obj):
        return obj.reactions.filter(reaction='dislike').count()

    def get_user_reaction(self, obj):
        user = self.context['request'].user

        if not user.is_authenticated:
            return None

        reaction = obj.reactions.filter(user=user).first()
        return reaction.reaction if reaction else None