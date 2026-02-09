from django.shortcuts import render
from .models import Task

# Create your views here.

def get_all_tasks(request):
    get_all_my_tasks=Task.objects.filter(created_by=request.user)
    