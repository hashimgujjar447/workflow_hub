from django.db import models
from accounts.models import Account
from workspaces.models import Workspace,WorkspaceMember
from django.utils.text import slugify



class Project(models.Model):

    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_FAILED, 'Failed'),
    )

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name='projects'
    )

    name = models.CharField(max_length=150)

    slug = models.SlugField(
        max_length=150
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    created_by = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_projects'
    )


    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Workspace.objects.filter(slug=slug).exists():
                slug=f"{base_slug}-{counter}"
                counter=counter+1
            self.slug = slug    

        super().save(*args,**kwargs)

    class Meta:
        unique_together = ('workspace', 'slug')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.workspace.name} - {self.name}"
    

class ProjectMember(models.Model):

    ROLE_MANAGER = 'manager'
    ROLE_LEADER = 'leader'
    ROLE_FRONTEND = 'frontend'
    ROLE_BACKEND = 'backend'
    ROLE_SEO = 'seo'

    ROLE_CHOICES = (
        (ROLE_MANAGER, 'Manager'),
        (ROLE_LEADER, 'Leader'),
        (ROLE_FRONTEND, 'Frontend Developer'),
        (ROLE_BACKEND, 'Backend Developer'),
        (ROLE_SEO, 'SEO'),
    )

    member = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='project_memberships'
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='members'
    )

    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)

    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('project', 'member')

    def __str__(self):
        return f"{self.member.email} -> {self.project.name}"
