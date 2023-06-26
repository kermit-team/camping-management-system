from django.contrib.auth.models import Group
from rest_framework import serializers

from .permission_response_serializer import PermissionResponseSerializer


class GroupResponseSerializer(serializers.ModelSerializer):
    permissions = PermissionResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'
