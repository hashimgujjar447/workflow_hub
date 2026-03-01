from django.urls import path
from . import views
urlpatterns = [
    path('', views.send_invite, name="send_invite"),
    path('accept/<uuid:token>/', views.accept_invite, name="accept_invite"),
    path('reject/<uuid:token>/', views.reject_invite, name="reject_invite"),
]