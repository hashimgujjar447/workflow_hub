from django.shortcuts import render, get_object_or_404, redirect
from workspaces.models import Workspace,WorkspaceMember
from .models import Project, ProjectMember
from tasks.models import Task
from comments.models import TaskComment
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.contrib import messages



@login_required
def projects(request):
    workspaces = Workspace.objects.filter( Q(creator=request.user) | Q(members__user=request.user) ,is_active=True)
    selected_projects = None

    if request.method == "POST":
        workspace_slug = request.POST.get("workspace_slug")

        workspace = get_object_or_404(
            Workspace,
            
             Q(creator=request.user) | Q(members__user=request.user) ,is_active=True,
             slug=workspace_slug,
        )

        selected_projects = workspace.projects.all()

    context = {
        'workspaces': workspaces,
        'projects': selected_projects
    }

    return render(request, 'projects/index.html', context)

@login_required
def project_detail(request, workspace_slug, project_slug):
    
    workspace = get_object_or_404(
        Workspace.objects.distinct(),
        Q(creator=request.user) | Q(members__user=request.user),
        slug=workspace_slug
    )
    # Get project belonging to this workspace
    IsMemberAvailabke=Project.objects.filter(workspace__slug=workspace_slug,slug=project_slug).prefetch_related("members")


    for p in IsMemberAvailabke:
        if not p.members.all():
            print("No mmebers available")
        for m in p.members.all():
            if m.member==request.user:
                print("Yes member")
            else:
                print("Not member")    

   
    project = get_object_or_404(
        Project.objects.prefetch_related(
            Prefetch(
                "tasks__comments",
                 queryset=TaskComment.objects.select_related("parent_comment").prefetch_related("replies")
            ),
        ),
         slug=project_slug,
        workspace=workspace
    )
    
    # Get project members (filter by project, not workspace)
    members = project.members.select_related('member').all()
    
    # Get project tasks
    tasks = project.tasks.select_related('assigned_to__member', 'created_by').all()
    for t in tasks:
        for r in t.comments.all():
            if r.parent_comment:
                print(r.content)
                print(r.replies.all())
        
    # Get all last 2 comments

    
    # Task statistics
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status=Task.STATUS_COMPLETED).count()
    in_progress_tasks = tasks.filter(status=Task.STATUS_IN_PROGRESS).count()
    todo_tasks = tasks.filter(status=Task.STATUS_TODO).count()
    

    context = {
        'workspace': workspace,
        'project': project,
        'members': members,
        'tasks': tasks,
        'total_members': members.count(),
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'todo_tasks': todo_tasks,
        'is_allow_to_delete_and_create':project.members.filter( member=request.user,role__in=['leader','manager'],is_active=True)
    }
   
    
    return render(request, 'projects/project_detail.html', context)


@login_required
def add_member(request, workspace_slug, project_slug):
    from django.contrib.auth import get_user_model
    from django.shortcuts import redirect
    from django.contrib import messages
    
    User = get_user_model()
    
    workspace = get_object_or_404(
        Workspace,
        slug=workspace_slug,
        is_active=True
    )
    
    project = get_object_or_404(
        Project,
        slug=project_slug,
        workspace=workspace,
        is_active=True
    )
    
    if request.method == "POST":
        member_id = request.POST.get('member_id')
        role = request.POST.get('role')

        if project.members.filter( member=request.user,role__in=['leader','manager'],is_active=True):
        
            if member_id and role:
                try:
                    user = User.objects.get(id=member_id)
                    
                    # Check if member already exists in project
                    if not ProjectMember.objects.filter(project=project, member=user).exists():
                        ProjectMember.objects.create(
                            project=project,
                            member=user,
                            role=role
                        )
                        messages.success(request, f'{user.first_name} {user.last_name} has been added to the project.')
                    else:
                        messages.warning(request, 'This member is already in the project.')
                        
                except User.DoesNotExist:
                    messages.error(request, 'Selected user does not exist.')
            else:
              
                messages.error(request, 'Please select a member and role.')
            
        return redirect('project_detail', workspace_slug=workspace_slug, project_slug=project_slug)
      

    
    # GET request - show form

    get_all_available_members = workspace.members.all()
    all_project_members = project.members.all()
    
    # Find members not in project
    check_which_member_not_in_project = []
    for m in get_all_available_members:
        is_member = False
        for n in all_project_members:
            if m.user == n.member:
                is_member = True
                break
        if not is_member:
            check_which_member_not_in_project.append(m)
    
    context = {
        'workspace_slug': workspace_slug,
        'project_slug': project_slug,
        'available_members': check_which_member_not_in_project
    }
    return render(request, 'projects/add_new_member.html', context)


@login_required
def project_settings(request, workspace_slug, project_slug):
    workspace = get_object_or_404(
        Workspace,
        slug=workspace_slug,
        is_active=True
    )
    
    project = get_object_or_404(
        Project.objects.prefetch_related("members"),
        slug=project_slug,
        workspace=workspace
    )

    # Check if user is manager or leader
    is_manager_or_leader = project.members.filter(
        member=request.user,
        role__in=["manager", "leader"],
        is_active=True
    ).exists()

    if request.method == "POST":
        if not is_manager_or_leader:
            raise PermissionDenied("You are not allowed to delete this project.")
        
        project.is_active = False
        project.save()
        messages.success(request, f'Project "{project.name}" has been deleted successfully.')
        return redirect('workspace_detail', slug=workspace.slug)

    return render(
        request,
        'projects/settings.html',
        {
            'workspace': workspace,
            'project': project,
            'is_allow_to_delete': is_manager_or_leader
        }
    )
    
