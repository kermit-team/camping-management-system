from rest_framework import serializers
from django.contrib.auth.models import Group

from .permission_serializer import PermissionSerializer


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'permissions',
        )