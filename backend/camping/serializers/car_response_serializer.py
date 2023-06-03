from rest_framework import serializers

from account.serializers import UserResponseSerializer
from camping.models import Car


class CarResponseSerializer(serializers.ModelSerializer):
    drivers = UserResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = '__all__'
