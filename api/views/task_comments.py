from rest_framework.generics import ListCreateAPIView
from tasks.models import Task
from comments.models import TaskComment
from api.serializers.comment_reply_serializer import CommentDetailSerializer
from api.serializers.comment_serializer import CommentSerializer,CommentPagination
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView
from rest_framework import permissions
from tasks.models import Task
from comments.models import TaskComment
from api.serializers.comment_reply_serializer import CommentDetailSerializer
from api.serializers.comment_serializer import CommentSerializer, CommentPagination


class TaskCommentsAPIView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CommentPagination

    def get_queryset(self):
        self.task = Task.objects.get(pk=self.kwargs['pk'])

        return TaskComment.objects.filter(
            task=self.task,
            parent_comment__isnull=True
        ).select_related('author').prefetch_related(
            'replies',
            'replies__author'
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CommentSerializer
        return CommentDetailSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            task=self.task   # ✅ VERY IMPORTANT
        )
     