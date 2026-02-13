from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
   
    path('', views.projects, name="projects"),
    path('<slug:workspace_slug>/<slug:project_slug>/', views.project_detail, name="project_detail"),
    path('<slug:workspace_slug>/<slug:project_slug>/add_new_member',views.add_member,name="add_member"),
    path('<slug:workspace_slug>/<slug:project_slug>/task/',include('tasks.urls')),
    path('<slug:workspace_slug>/<slug:project_slug>/comment/',include('comments.urls')),
    
    
]
