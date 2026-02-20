from rest_framework import serializers
from workspaces.models import Workspace

class WorkspaceSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()

    class Meta:
        model = Workspace
        fields = [
            'id',
            'name',
            'slug',
            'creator',
            'created_at',
            'updated_at',
        ]