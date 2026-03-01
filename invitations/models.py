import uuid
from django.db import models
from accounts.models import Account
from workspaces.models import Workspace
from django.utils import timezone
from datetime import timedelta

class WorkspaceInvite(models.Model):

    STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
    ('expired', 'Expired'),
)
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="invites"
    )

    email = models.EmailField()
    
    invited_by = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="sent_invites"
    )

    role = models.CharField(max_length=20)

    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.email} → {self.workspace.name}"
  
    
    def is_expired(self):
        if not self.expires_at:
            return False
        return self.expires_at < timezone.now()
    

    def save(self, *args,**kwargs):
        if not self.expires_at:
            self.expires_at=timezone.now() + timedelta(days=7)
        super().save(*args,**kwargs)    
    class Meta:
            unique_together = ("workspace", "email")    
        