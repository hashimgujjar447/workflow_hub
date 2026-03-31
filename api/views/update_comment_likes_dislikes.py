from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from comments.models import TaskComment, CommentReaction
from api.serializers.comment_serializer import CommentReactionSerializer
from projects.models import ProjectMember

class CommentReactionView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentReactionSerializer


    def get_comment(self):
        return get_object_or_404(
            TaskComment,
            id=self.kwargs.get('comment_id')
        )

    def is_project_member(self, comment):
        return ProjectMember.objects.filter(
            project=comment.task.project,
            member=self.request.user,
            is_active=True
        ).exists()

    def perform_create(self, serializer):
        user = self.request.user
        comment = self.get_comment()

        # 🔐 Only project members allowed
        if not self.is_project_member(comment):
            raise PermissionDenied("You are not allowed to react to this comment")

        reaction_type = serializer.validated_data['reaction']

        obj, created = CommentReaction.objects.get_or_create(
        user=user,
        comment=comment,
        defaults={"reaction": reaction_type}   # 🔥 IMPORTANT
    )

        # 🔁 Toggle logic
        if not created:
            if obj.reaction == reaction_type:
                obj.delete()
            else:
                obj.reaction = reaction_type
                obj.save()
            
