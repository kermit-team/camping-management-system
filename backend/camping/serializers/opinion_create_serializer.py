from rest_framework import serializers

from camping.models import Opinion


class OpinionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opinion
        fields = (
            'rating',
            'description',
            'author',
            'camping_plot',
        )
