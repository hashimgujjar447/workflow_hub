from django.shortcuts import render,redirect
from django.utils.text import slugify
from workspaces.models import Workspace,WorkspaceMember

# Create your views here.

def workspaces(request):
    findAllWorkSpaces=Workspace.objects.filter(creator=request.user)
    workspaces={}
    for workspace in findAllWorkSpaces:
        findAllMemebrsOfWorkspaces=WorkspaceMember.objects.filter(workspace=workspace)
        if findAllWorkSpaces:
            workspaces[workspace]=findAllMemebrsOfWorkspaces
        else:
            workspaces[workspace] =[]   
    
    
    context={
        'user':request.user,
        'all_workspaces':workspaces
    }

    return render(request,'workspaces/workspaces.html',context)

def create_workspace(request):
    if request.method=="POST":
        name=request.POST.get("name")
        is_active=request.POST.get("is_active")

        # Generate unique slug from name
        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        
        # Ensure slug is unique
        while Workspace.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        create=Workspace.objects.create(
            name=name,
            slug=slug,
            is_active=(is_active=="true"),
            creator=request.user
        )
        if create:
            return redirect('workspaces')
    return render(request,'workspaces/create_workspace.html')