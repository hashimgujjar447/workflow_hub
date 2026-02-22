from rest_framework import serializers
from workspaces.models import WorkspaceMember
from accounts.models import Account
class UserSerializer(serializers.ModelSerializer):
     class Meta:
         model=Account
         fields=['first_name','last_name','email','username','date_joined']

class WorkSpaceMemberSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=WorkspaceMember
        fields=['user','role','joined_at','is_active']

