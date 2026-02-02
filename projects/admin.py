from django.contrib import admin
from .models import Project,ProjectMember

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'workspace', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'workspace')
    search_fields = ('name',)


admin.site.register(Project,ProjectAdmin)
admin.site.register(ProjectMember)


