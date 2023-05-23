from rest_framework import serializers

from account.models import User
from .group_response_serializer import GroupResponseSerializer


class UserResponseSerializer(serializers.ModelSerializer):
    groups = GroupResponseSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'avatar',
            'id_card',
            'is_superuser',
            'is_staff',
            'is_active',
            'last_login',
            'date_joined',
            'groups',
            'user_permissions',
        )
