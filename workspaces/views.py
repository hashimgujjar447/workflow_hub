from django.shortcuts import render

# Create your views here.

def workspaces(request):
    return render(request,'workspaces/workspaces.html')