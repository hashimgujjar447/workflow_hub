from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from workspaces.models import Workspace, WorkspaceMember
from accounts.models import Account
from django.shortcuts import redirect
from django.contrib import messages
from projects.models import Project,ProjectMember
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.

@login_required
def workspaces(request):
    findAllWorkSpaces = Workspace.objects.filter(
      Q(creator=request.user) | Q(members__user=request.user)
).prefetch_related('members','projects').distinct()

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

@login_required
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


@login_required
def workspace_detail(request, slug):
    workspace = get_object_or_404(Workspace, slug=slug)
    
    # Get workspace members
    members = workspace.members.select_related('user').all()
    
    # Get workspace projects
    projects = workspace.projects.all()
    is_creator=request.user==workspace.creator
    
    context = {
        'workspace': workspace,
        'members': members,
        'projects': projects,
        'total_members': members.count(),
        'total_projects': projects.count(),
        'is_creator':is_creator
        
    }
    
    return render(request, 'workspaces/workspace_detail.html', context)

@login_required
def add_member_in_workspace(request,slug):
    workspace = get_object_or_404(Workspace, slug=slug)

    if request.method=="POST":
        member_id = request.POST.get('member_id')
        role = request.POST.get('role')

        user=Account.objects.get(id=member_id)
        if member_id and role:
            try:
                if not WorkspaceMember.objects.filter(workspace=workspace,user=user).exists():
                    WorkspaceMember.objects.create(
                        workspace=workspace,
                        user=user,
                        role=role
                    )
                    messages.success(request, f'{user.first_name} {user.last_name} has been added to the project.')
                else:
                    messages.warning(request, 'This member is already in the project.')
            except Account.DoesNotExist:
                messages.error(request, 'Selected user does not exist.')
        return redirect('workspace_detail', slug=workspace.slug)

    all_members=Account.objects.all()
 
    which_members_are_in_workspace=workspace.members.all()
    get_ids=[]
    for m in which_members_are_in_workspace:
        get_ids.append(m.user.id)

    get_member=all_members.exclude(
        id__in=get_ids
    )
    print(get_member)

    context = {
        'workspace': workspace,
        'available_members':get_member
    }
    return render(request,'workspaces/add_member.html', context)



@login_required
def create_workspace_project(request, slug):
    workspace = get_object_or_404(Workspace, slug=slug)

    if request.method == "POST":
        project_name = request.POST.get("name")
        project_status = request.POST.get("status")
        is_active = request.POST.get("is_active") == "true"

        if not project_name:
            messages.error(request, "Project ka naam zaroori hai.")
            return redirect('workspace_detail', slug=workspace.slug)

        if not workspace.members.filter(user=request.user).exists():
            messages.error(request, "Aap is workspace ka hissa nahi hain.")
            return redirect('workspace_detail', slug=workspace.slug)

        if workspace.projects.filter(name__iexact=project_name).exists():
            messages.error(
                request,
                "Is workspace mein isi naam ka project pehle se mojood hai."
            )
            return redirect('workspace_detail', slug=workspace.slug)

        with transaction.atomic():
            project = Project.objects.create(
                workspace=workspace,
                name=project_name,
                slug=slugify(f"{workspace.slug}-{project_name}"),
                status=project_status,
                is_active=is_active
            )

            ProjectMember.objects.get_or_create(
                project=project,
                member=request.user,
                defaults={"role": "manager"}
            )

        messages.success(request, "Project successfully add ho gaya 🎉")
        return redirect('workspace_detail', slug=workspace.slug)

    return render(request, 'projects/create_project.html', {
        'workspace': workspace
    })
