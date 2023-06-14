from rest_framework import serializers

from camping.models import Payment


class PaymentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
