from rest_framework import serializers

from camping.models import CampingPlot
from .camping_section_response_serializer import CampingSectionResponseSerializer


class CampingPlotResponseSerializer(serializers.ModelSerializer):
    camping_section = CampingSectionResponseSerializer(read_only=True)
    
    class Meta:
        model = CampingPlot
        fields = '__all__'