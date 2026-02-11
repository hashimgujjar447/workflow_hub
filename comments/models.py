from django.db import models
from accounts.models import Account
from tasks.models import Task


class TaskComment(models.Model):

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    author = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        related_name='task_comments'
    )

    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.task} comment is {self.content}"
