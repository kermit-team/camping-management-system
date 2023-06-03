from rest_framework import serializers

from camping.models import CampingSection


class CampingSectionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampingSection
        fields = '__all__'
