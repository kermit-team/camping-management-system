from rest_framework import serializers

from camping.models import Reservation


class ReservationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = (
            'date_from',
            'date_to',
            'number_of_adults',
            'number_of_children',
            'number_of_babies',
            'car',
            'camping_plot',
        )
