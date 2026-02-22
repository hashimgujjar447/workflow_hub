from rest_framework import serializers
from workspaces.models import Workspace
from django.utils.text import slugify


class WorkspaceSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Workspace
        fields = [
            'creator',
            'name',
            'slug',
        ]

    def create(self, validated_data):
        name = validated_data.get('name')
        validated_data['slug'] = slugify(name)
        return super().create(validated_data)