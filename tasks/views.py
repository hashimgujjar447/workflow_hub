from django.shortcuts import render
from .models import Task
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from workspaces.models import Workspace
from projects.models import Project,ProjectMember
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def get_all_tasks(request):
    get_all_my_tasks=Task.objects.filter(created_by=request.user)
    

@login_required
def add_task(request,workspace_slug,project_slug):
    print(project_slug,workspace_slug)
    workspace=get_object_or_404(
        Workspace,
        slug=workspace_slug
    )
    if not workspace:
        print("Workspace not found")
        return
    project=get_object_or_404(
        Project,
        slug=project_slug
    )
    if not project:
        print("project not found")
        return
    
    # Handle POST request for task creation
    if request.method == "POST":
        title=request.POST.get("title")
        description=request.POST.get("description")
        status=request.POST.get("status")
        assigned_to=request.POST.get("assigned_to")
        due_date=request.POST.get("due_date")
        
        # Check if current user is a member of the project
        check_is_user_is_member = project.members.filter(member=request.user).exists()
        
        if check_is_user_is_member:
            task_data = {
                'project': project,
                'title': title,
                'description': description,
                'status': status,
                'created_by': request.user
            }
            
            # Add assigned_to if provided
            if assigned_to:
                get_project_member = project.members.get(id=assigned_to)
                task_data['assigned_to'] = get_project_member
            
            # Add due_date if provided
            if due_date:
                task_data['due_date'] = due_date
            
            Task.objects.create(**task_data)
            print("Task created successfully")
            
    
    # Get all project members for the form
    project_members = project.members.select_related('member').all()
    
    context = {
        'project': project,
        'project_members': project_members,
    }
    
    return render(request, 'tasks/create_task.html', context)


