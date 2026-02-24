from rest_framework.generics import ListCreateAPIView
from tasks.models import Task
from comments.models import TaskComment
from api.serializers.comment_reply_serializer import CommentDetailSerializer
from api.serializers.comment_serializer import CommentSerializer
from rest_framework import permissions


class TaskCommentsAPIView(ListCreateAPIView):
     permission_classes = [permissions.IsAuthenticated]
     def get_queryset(self):
        self.task = Task.objects.get(pk=self.kwargs['pk'])

        return TaskComment.objects.filter(
            task=self.task,
            parent_comment__isnull=True
        ).select_related('author').prefetch_related('replies')

     def get_serializer_class(self):
        if self.request.method == "POST":
            return CommentSerializer   # for creating comment
        return CommentDetailSerializer  # for GET nested response
     
   

     def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
          
        )