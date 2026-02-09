from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from workspaces.models import Workspace, WorkspaceMember

# Create your views here.

def workspaces(request):
    findAllWorkSpaces = Workspace.objects.filter(
    creator=request.user
).prefetch_related('members','projects')

    workspaces = {}

    for workspace in findAllWorkSpaces:
        workspaces[workspace.id] = {
            'workspace': workspace,
            'members': workspace.members.all(),
            'projects':workspace.projects.count()
        }

  
    for key,value in workspaces.items():
        print(value['workspace'])


    context = {
        'user': request.user,
        'all_workspaces': workspaces
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


def workspace_detail(request, slug):
    workspace = get_object_or_404(Workspace, slug=slug, creator=request.user)
    
    # Get workspace members
    members = workspace.members.select_related('user').all()
    
    # Get workspace projects
    projects = workspace.projects.all()
    
    context = {
        'workspace': workspace,
        'members': members,
        'projects': projects,
        'total_members': members.count(),
        'total_projects': projects.count(),
    }
    
    return render(request, 'workspaces/workspace_detail.html', context)