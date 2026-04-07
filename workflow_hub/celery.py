import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE",'workflow_hub.settings')
app=Celery('workflow_hub')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()