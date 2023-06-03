from django.contrib.auth.models import Group
from rest_framework import serializers


class GroupRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'name',
            'permissions',
        )
