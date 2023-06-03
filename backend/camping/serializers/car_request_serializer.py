from rest_framework import serializers

from camping.models import Car


class CarRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            'registration_plate',
        )
