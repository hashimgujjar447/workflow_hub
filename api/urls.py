from rest_framework.routers import DefaultRouter
from api.views.workspace import ListCreateWorkspaceView,WorkSpaceDetailView
from api.views.workspace_members import ListCreateWorkspaceMembersApiView
from api.views.workspace_projects import WorkspaceProjectApiView,WorkspaceProjectDetailsApiView,ProjectTasksApiView
from api.views.task_comments import TaskCommentsAPIView
from django.urls import path
from api.views.project_task_details import RetrieveTaskApiView



urlpatterns = [
    path('workspaces/', ListCreateWorkspaceView.as_view()),

    path('workspaces/<slug:workspace_slug>/', WorkSpaceDetailView.as_view()),

    path('workspaces/<slug:workspace_slug>/members/',
         ListCreateWorkspaceMembersApiView.as_view()),

    path('workspaces/<slug:workspace_slug>/projects/',
         WorkspaceProjectApiView.as_view()),

    path('workspaces/<slug:workspace_slug>/projects/<slug:project_slug>/',
         WorkspaceProjectDetailsApiView.as_view()),
path('workspaces/<slug:workspace_slug>/projects/<slug:project_slug>/tasks/',ProjectTasksApiView.as_view()),
path('workspaces/<slug:workspace_slug>/projects/<slug:project_slug>/tasks/<int:pk>/',RetrieveTaskApiView.as_view()),
path('workspaces/<slug:workspace_slug>/projects/<slug:project_slug>/tasks/<int:pk>/comments/',TaskCommentsAPIView.as_view())
]