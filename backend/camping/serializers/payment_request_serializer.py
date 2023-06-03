from rest_framework import serializers

from camping.models import Payment


class PaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'status',
            'price',
        )
