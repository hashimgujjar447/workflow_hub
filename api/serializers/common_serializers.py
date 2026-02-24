from accounts.models import Account
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'username', 'date_joined']