from rest_framework import serializers

from account.serializers import UserResponseSerializer
from camping.models import Opinion
from .camping_plot_response_serializer import CampingPlotResponseSerializer


class OpinionResponseSerializer(serializers.ModelSerializer):
    author = UserResponseSerializer(read_only=True)
    camping_plot = CampingPlotResponseSerializer(read_only=True)

    class Meta:
        model = Opinion
        fields = '__all__'
