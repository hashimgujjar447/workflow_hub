from rest_framework import generics
from workspaces.models import Workspace, WorkspaceMember
from api.serializers.workspace import WorkspaceSerializer
from django.db.models import Count, Q
from rest_framework import permissions
from api.permissions import IsManager
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
class ListCreateWorkspaceView(generics.ListCreateAPIView):
   
    serializer_class=WorkspaceSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
      
        return Workspace.objects.filter(Q(creator=self.request.user) | Q(members__user=self.request.user)).annotate(
            total_members=Count('members', distinct=True),
            total_projects=Count('projects', distinct=True)
        ).order_by('-created_at')
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    
class WorkSpaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkspaceSerializer
    lookup_field = 'slug'
    lookup_url_kwarg='workspace_slug'
    permission_classes = [permissions.IsAuthenticated,IsManager]   # ✅ sirf login user allowed

    def get_queryset(self):
        return (
            Workspace.objects
            .annotate(
                total_members=Count(
                    'members',
                    filter=Q(members__is_active=True),
                    distinct=True
                ),
                total_projects=Count('projects', distinct=True)
            )
        )
    def perform_update(self, serializer):
        title = serializer.validated_data.get("name", serializer.instance.name)
        base_slug = slugify(title)
        slug = base_slug
        count = 1
        # Exclude the current instance to avoid false collision with its own slug
        while Workspace.objects.filter(slug=slug).exclude(pk=serializer.instance.pk).exists():
            slug = f"{base_slug}-{count}"
            count += 1
        serializer.save(slug=slug)

