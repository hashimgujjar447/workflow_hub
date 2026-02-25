from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from workspaces.models import Workspace
from projects.models import Project, ProjectMember
from django.db.models import Prefetch, Count


@login_required
def get_all_tasks(request):

    projects = Project.objects.filter(
        members__member=request.user
    ).prefetch_related(
        Prefetch(
            "tasks",
            queryset=Task.objects.select_related(
                "assigned_to",
                "created_by"
            ).annotate(
                comment_count=Count('comments')
            )
        )
    ).distinct()

    all_data = []

    for project in projects:
        tasks = project.tasks.all()  # NO extra query (prefetched)

        my_assigned_tasks = [
            t for t in tasks
            if t.assigned_to and t.assigned_to.member == request.user
        ]

        my_created_tasks = [
            t for t in tasks
            if t.created_by == request.user
        ]

        all_data.append({
            "project": project,
            "assigned_tasks": my_assigned_tasks,
            "created_tasks": my_created_tasks,
        })

    context = {
        "all_data": all_data
    }

    return render(request, "task/all_tasks.html", context)

@login_required
def add_task(request, workspace_slug, project_slug):
    workspace = get_object_or_404(Workspace, slug=workspace_slug)
    project = get_object_or_404(Project, slug=project_slug)

    # Ensure user is a member of the project
    is_member = ProjectMember.objects.filter(
        project=project,
        member=request.user
    ).exists()

    if not is_member:
        return render(request, "403.html", status=403)

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        status_value = request.POST.get("status")
        assigned_to_id = request.POST.get("assigned_to")
        due_date = request.POST.get("due_date")

        task_data = {
            "project": project,
            "title": title,
            "description": description,
            "status": status_value,
            "created_by": request.user,
        }

        # Secure assignment (validate inside project)
        if assigned_to_id:
            assigned_member = get_object_or_404(
                ProjectMember,
                id=assigned_to_id,
                project=project
            )
            task_data["assigned_to"] = assigned_member

        if due_date:
            task_data["due_date"] = due_date

        Task.objects.create(**task_data)

        return redirect("get_all_tasks")  # change to your url name

    # Optimized: avoid N+1 queries
    project_members = ProjectMember.objects.filter(
        project=project
    ).select_related("member")

    context = {
        "project": project,
        "workspace": workspace,
        "project_members": project_members,
    }

    return render(request, "tasks/create_task.html", context)
