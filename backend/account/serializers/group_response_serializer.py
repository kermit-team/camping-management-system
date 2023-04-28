from rest_framework import serializers
from django.contrib.auth.models import Group

from .permission_response_serializer import PermissionResponseSerializer


class GroupResponseSerializer(serializers.ModelSerializer):
    permissions = PermissionResponseSerializer(many=True)

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'permissions',
        )