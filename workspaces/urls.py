from django.urls import path
from . import views

urlpatterns = [
    path('', views.workspaces, name="workspaces"),
    path('create/', views.create_workspace, name="create_workspace"),
    path('<slug:slug>/', views.workspace_detail, name="workspace_detail"),
    path('<slug:slug>/add_member/',views.add_member_in_workspace,name="add_member")
]