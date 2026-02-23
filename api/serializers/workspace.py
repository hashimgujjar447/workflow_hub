from rest_framework import serializers
from workspaces.models import Workspace,WorkspaceMember
from django.utils.text import slugify

class WorkspaceMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model=WorkspaceMember
        fields=[
            'user',
            'joined_at',
            'is_active'
        ]


class WorkspaceSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    total_members = serializers.IntegerField(read_only=True)
    total_projects = serializers.IntegerField(read_only=True)


    class Meta:
        model = Workspace
        fields = [
            'creator',
            'name',
            'slug',
            'is_active',
            'created_at',
            'updated_at',
            'total_members',
            'total_projects'
        ]

   
    
    


   
