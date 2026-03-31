from django.db.models.signals import post_save,post_delete
from .models import TaskComment,CommentReaction
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=TaskComment)
def comment_realTime_update(sender, instance, created, **kwargs):
    channel = get_channel_layer()
    if channel is None:
        return
    
    print(instance.task.project.slug)

    group_name = f'project_{instance.task.project.slug}'

    async_to_sync(channel.group_send)(
        group_name,
        {
            "type": "comment_update",
            "data": {
                "event": "comment_created" if created else "comment_updated",
                "id": instance.id,
                "content": instance.content,
                "project": instance.task.project.slug,
                "task": instance.task.id,
                "author_id": instance.author.id,
                "author":instance.author.username,
                "parent_comment": instance.parent_comment.id if instance.parent_comment else None,
            }
        }
    )

@receiver(post_save, sender=CommentReaction)
def commentReaction_realTime_update(sender, instance, created, **kwargs):
    print("🔥 SAVE SIGNAL")

    channel = get_channel_layer()
    if channel is None:
        return
    
    group_name = f'project_{instance.comment.task.project.slug}'

    
    comment=instance.comment
    likes_count = comment.reactions.filter(reaction='like').count()
    dislikes_count = comment.reactions.filter(reaction='dislike').count()
    
    async_to_sync(channel.group_send)(
        group_name,
        {
            "type": "comment_reaction_update",
            "data": {
                "event": "comment_reaction_created" if created else "comment_reaction_updated",
                "id": instance.id,
                "comment_id": instance.comment.id,
                "reaction": instance.reaction,
                "likes": likes_count,
                "dislikes": dislikes_count,
                  "user_id": instance.user.id,
            }
        }
    )



@receiver(post_delete, sender=CommentReaction)
def commentReaction_deleted(sender, instance, **kwargs):
    print("🔥 DELETE SIGNAL")

    channel = get_channel_layer()
    if channel is None:
        return
    
    group_name = f'project_{instance.comment.task.project.slug}'

    comment=instance.comment
    likes_count = comment.reactions.filter(reaction='like').count()
    dislikes_count = comment.reactions.filter(reaction='dislike').count()


    

    async_to_sync(channel.group_send)(
        group_name,
        {
            "type": "comment_reaction_update",
            "data": {
                "event": "comment_reaction_deleted",
                "comment_id": instance.comment.id,
                "reaction": None,
                "id":instance.id,
                'likes':likes_count,
                "dislikes":dislikes_count
                

            }
        }
    )