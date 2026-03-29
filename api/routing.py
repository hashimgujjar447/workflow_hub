from django.urls import path
from .consumers import TaskConsumer

websocket_urlpatterns=[
  path("ws/tasks/<slug:project_slug>/", TaskConsumer.as_asgi())
]