from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from tasks.models import Task

@receiver(post_save,sender=Task)
def task_realtime_update(sender,instance,created,**kwargs):
    chanel_layer=get_channel_layer()
    group_name=f'project_{instance.project.slug}'
    async_to_sync(chanel_layer.group_send)(
        group_name,{
            "type":"task_update",
            "data":{
                "event": "task_created" if created else "task_updated",
                "id": instance.id,
                "title": instance.title,
                "status": instance.status,
                "project": instance.project.slug,
            }
        }
    )

