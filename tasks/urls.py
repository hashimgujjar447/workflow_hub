from django.urls import path
from . import views
urlpatterns=[
    path('add_task',views.add_task,name="add_project_task"),
    path('get_all_tasks/',views.get_all_tasks,name="get_all_tasks"),


]