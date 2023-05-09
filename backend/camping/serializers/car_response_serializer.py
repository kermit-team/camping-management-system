from rest_framework import serializers

from camping.models import Car


class CarResponseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Car
        fields = '__all__'