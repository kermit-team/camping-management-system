from rest_framework import serializers

from camping.models import Opinion


class OpinionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opinion
        fields = (
            'rating',
            'description',
        )
