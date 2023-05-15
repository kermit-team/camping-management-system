from rest_framework import serializers

from account.models import User
from .group_response_serializer import GroupResponseSerializer


class UserResponseSerializer(serializers.ModelSerializer):
    groups = GroupResponseSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
