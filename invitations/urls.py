from django.urls import path
from . import views
urlpatterns = [
    path('', views.send_invite, name="send_invite"),
    path('all_invites/', views.get_invites, name="all_invites"),
   
]