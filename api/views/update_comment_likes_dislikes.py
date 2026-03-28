from rest_framework import generics, permissions
from api.serializers.comment_serializer import CommentReactionSerializer
from django.shortcuts import get_object_or_404
from comments.models import TaskComment, CommentReaction

class CommentReactionView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentReactionSerializer

    def perform_create(self, serializer):
        user = self.request.user
        comment_id = self.kwargs.get('comment_id')

        comment = get_object_or_404(TaskComment, id=comment_id)
        reaction_type = serializer.validated_data['reaction']

        obj, created = CommentReaction.objects.get_or_create(
            user=user,
            comment=comment
        )

        # toggle logic
        if not created and obj.reaction == reaction_type:
            obj.delete()
        else:
            obj.reaction = reaction_type
            obj.save()  