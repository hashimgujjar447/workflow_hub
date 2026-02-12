from numbers import Number
from django.shortcuts import render, redirect
from comments.models import TaskComment,Task
from django.shortcuts import get_object_or_404
from workspaces.models import Workspace,WorkspaceMember
from django.db.models import Prefetch
from projects.models import Project,ProjectMember
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.

def view_all_comments(request,workspace_slug,project_slug,id):

    

    workspace=get_object_or_404(
      Workspace,
      slug=workspace_slug
    )
    project=get_object_or_404(
         Project.objects.prefetch_related("tasks__comments__replies"),
        slug=project_slug
    )
       
    tasks=list(project.tasks.all())
    get_task=[t for t in tasks if t.id==id][0]
    
    context={
        'task':get_task,
        }
    
    if request.method=="POST":
           content=request.POST.get("content")
           task_id=request.POST.get("task_id")
           parent_comment_id=request.POST.get("parent_comment_id")

           print(task_id)
           print(get_task.id==int(task_id))
           if get_task.id!=int(task_id):
                print("Id error")
                return render(
                request,
                'task/tast_comments_details.html',
                context
            )
           
           task=get_object_or_404(
                Task,
                id=task_id
           )
           parent=None

           if parent_comment_id and parent_comment_id.strip():
                print("Have a parent comment")
                parent_comment_id=int(parent_comment_id)
                parent=get_object_or_404(
                     TaskComment,
                     id=parent_comment_id
                )


                
           
           TaskComment.objects.create(
                task=task,
                content=content,
                author=request.user,
                parent_comment=parent
           )
           
           # Redirect to prevent duplicate submission on refresh
           return redirect('view_comment_details', workspace_slug=workspace_slug, project_slug=project_slug, id=id)
          
    return render(
        request,
        'task/tast_comments_details.html',
        context
    )

    

       