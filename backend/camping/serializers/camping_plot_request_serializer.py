from rest_framework import serializers

from camping.models import CampingPlot


class CampingPlotRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampingPlot
        fields = (
            'position',
            'camping_section',
        )
