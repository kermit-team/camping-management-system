from rest_framework import serializers


class CarAbleToEnterCampingSerializer(serializers.Serializer):
    registration_plate = serializers.CharField(max_length=25)
