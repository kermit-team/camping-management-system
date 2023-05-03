from rest_framework import serializers
from django.contrib.auth.models import Group

from .permission_response_serializer import PermissionResponseSerializer


class GroupRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'name',
            'permissions',
        )