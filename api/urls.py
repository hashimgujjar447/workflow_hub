from rest_framework.routers import DefaultRouter
from api.views.workspace import ListCreateWorkspaceView,WorkSpaceDetailView
from api.views.workspace_members import ListCreateWorkspaceMembersApiView
from api.views.workspace_projects import WorkspaceProjectApiView,WorkspaceProjectDetailsApiView,ProjectTasksApiView,ProjectMembersApiView
from api.views.task_comments import TaskCommentsAPIView
from django.urls import path
from api.views.project_task_details import RetrieveTaskApiView
from api.views.profile import ProfileView

from api.views.get_all_tasks import DashboardTasksView,AllTasksView
from api.views.invites import SendInviteView,ListInvitesView,HandleInviteView
from api.views.auth import RegisterView,LoginView,LogoutView
from api.views.update_comment_likes_dislikes import CommentReactionView



urlpatterns = [
     path('profile/',ProfileView.as_view()),
     path('tasks/',AllTasksView.as_view()),
     path('workspaces/', ListCreateWorkspaceView.as_view()),
     path('workspaces/<slug:slug>/invite/', SendInviteView.as_view()),
     path('invites/', ListInvitesView.as_view()),
     path('invites/action/', HandleInviteView.as_view()),
     path('dashboard_tasks/',DashboardTasksView.as_view() ),
    
     path('workspaces/<slug:workspace_slug>/', WorkSpaceDetailView.as_view()),

     path('workspaces/<slug:workspace_slug>/members/',
         ListCreateWorkspaceMembersApiView.as_view()),

     path('workspaces/<slug:workspace_slug>/projects/',
         WorkspaceProjectApiView.as_view()),

     path('workspaces/<slug:workspace_slug>/projects/<slug:project_slug>/',
         WorkspaceProjectDetailsApiView.as_view()),
          path('workspaces/<slug:workspace_slug>/projects/<slug:project_slug>/members/',
         ProjectMembersApiView.as_view()),
     path('workspaces/<slug:workspace_slug>/projects/<slug:project_slug>/tasks/',ProjectTasksApiView.as_view()),
     path('workspaces/<slug:workspace_slug>/projects/<slug:project_slug>/tasks/<int:pk>/',RetrieveTaskApiView.as_view()),
     path('workspaces/<slug:workspace_slug>/projects/<slug:project_slug>/tasks/<int:pk>/comments/',TaskCommentsAPIView.as_view()),
     path(
    'workspaces/<slug:workspace_slug>/projects/<slug:project_slug>/tasks/<int:task_id>/comments/<int:comment_id>/reaction/',
    CommentReactionView.as_view()
),
     path('auth/register/', RegisterView.as_view()),
     path('auth/login/', LoginView.as_view()),
     path('auth/logout/', LogoutView.as_view()),
     path('auth/profile/', ProfileView.as_view()),
]