from rest_framework import serializers

from camping.models import Payment
from .reservation_response_serializer import ReservationResponseSerializer


class PaymentRequestSerializer(serializers.ModelSerializer):
    reservation = ReservationResponseSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = (
            'method',
            'status',
            'price',
            'reservation',
        )