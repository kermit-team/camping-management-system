from django.contrib.auth.models import Permission
from rest_framework import serializers


class PermissionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            'name',
            'codename',
        )
