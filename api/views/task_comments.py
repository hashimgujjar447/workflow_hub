from rest_framework.generics import ListCreateAPIView
from tasks.models import Task
from comments.models import TaskComment
from api.serializers.comment_reply_serializer import CommentDetailSerializer
from api.serializers.comment_serializer import CommentSerializer, CommentPagination
from rest_framework import permissions
from api.permissions import IsProjectMember


class TaskCommentsAPIView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsProjectMember]
    pagination_class = CommentPagination

    def get_task(self):
        """Helper to fetch and cache task on the view instance."""
        if not hasattr(self, '_task'):
            self._task = Task.objects.get(
                pk=self.kwargs['pk'],
                project__workspace__slug=self.kwargs['workspace_slug'],
                project__slug=self.kwargs['project_slug']
            )
        return self._task

    def get_queryset(self):
        task = self.get_task()
        return TaskComment.objects.filter(
            task=task,
            parent_comment__isnull=True
        ).select_related('author').prefetch_related(
            'replies',
            'replies__author'
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentSerializer
        return CommentDetailSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            task=self.get_task()
        )