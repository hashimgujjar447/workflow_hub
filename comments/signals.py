from django.db.models.signals import post_save
from .models import TaskComment
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
                "author": instance.author.username,
                "parent_comment": instance.parent_comment.id if instance.parent_comment else None,
            }
        }
    )