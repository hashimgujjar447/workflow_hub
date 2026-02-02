from django.contrib import admin
from .models import Workspace,WorkspaceMember


# Register your models here.

class WorkspaceManager(admin.ModelAdmin):
    list_display=('name','creator','created_at')
    prepopulated_fields={'slug':('name',)}


class WorkspaceMemberManager(admin.ModelAdmin):
    list_display=('user','workspace','role',)


admin.site.register(Workspace,WorkspaceManager)
admin.site.register(WorkspaceMember,WorkspaceMemberManager)