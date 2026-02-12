from django.urls import path
from . import views

urlpatterns=[
    path('<int:id>/',views.view_all_comments,name="view_comment_details"),
   

]
