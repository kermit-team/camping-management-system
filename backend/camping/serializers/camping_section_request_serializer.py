from rest_framework import serializers

from camping.models import CampingSection


class CampingSectionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampingSection
        fields = (
            'name',
            'plot_price',
            'price_per_adult',
            'price_per_child',
        )
