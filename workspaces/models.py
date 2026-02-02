from django.db import models
from accounts.models import Account

# Create your models here.

class Workspace(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    creator = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='created_workspaces'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name




class WorkspaceMember(models.Model):

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

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name='members'
    )

    user = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='workspace_memberships'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('workspace', 'user')

    def __str__(self):
        return f"{self.user.email} - {self.workspace.name} ({self.role})"
