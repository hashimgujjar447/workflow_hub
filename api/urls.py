from rest_framework.routers import DefaultRouter
from api.views.workspace import ListCreateWorkspaceView,WorkSpaceDetailView
from api.views.workspace_members import ListCreateWorkspaceMembersApiView
from django.urls import path



urlpatterns =[
    path('workspaces/',ListCreateWorkspaceView.as_view()),
    path('workspaces/<slug:slug>/',WorkSpaceDetailView.as_view()),
    path('workspaces/<slug:slug>/members/',ListCreateWorkspaceMembersApiView.as_view())
]