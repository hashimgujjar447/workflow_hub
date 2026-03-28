from django.contrib import admin
from .models import TaskComment,CommentReaction

# Register your models here.

admin.site.register(TaskComment)
admin.site.register(CommentReaction)