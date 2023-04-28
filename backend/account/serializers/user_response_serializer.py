from rest_framework import serializers

from account.models import User
from .group_response_serializer import GroupResponseSerializer


class UserResponseSerializer(serializers.ModelSerializer):
    groups = GroupResponseSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'id',
            'url',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'is_staff',
            'is_superuser',
            'phone_number',
            'avatar',
            'groups',
        )
