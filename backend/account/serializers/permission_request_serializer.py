from rest_framework import serializers
from django.contrib.auth.models import Permission


class PermissionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            'name', 
            'codename',
        )