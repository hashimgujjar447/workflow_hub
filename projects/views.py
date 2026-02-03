from django.shortcuts import render
from workspaces.models import Workspace
from projects.models import Project
from django.shortcuts import get_object_or_404

# Create your views here.

def projects(request):
   if request.method=="POST":
      workspaces=Workspace.objects.filter(creator=request.user)
      workspace_slug=request.POST.get("workspace_slug")

      workspace=get_object_or_404(
         Workspace,
         slug=workspace_slug
      )
      print(workspace_slug)
      projects=Project.objects.filter(
         workspace=workspace
         )
      print(projects)
      context={
         'workspaces':workspaces,
         'projects':projects
      }
      return render(request,'projects/index.html',context)

   else:
      workspaces=Workspace.objects.filter(creator=request.user)
      context={
         'workspaces':workspaces
      }

      return render(request,'projects/index.html',context)