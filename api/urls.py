from rest_framework.routers import DefaultRouter
from api.views.workspace import workspace_list
from django.urls import path



urlpatterns =[
    path('workspaces/',workspace_list)
]