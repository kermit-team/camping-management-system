from rest_framework import serializers


class AvailableCampingPlotsRequestSerializer(serializers.Serializer):
    date_from = serializers.DateField()
    date_to = serializers.DateField()
