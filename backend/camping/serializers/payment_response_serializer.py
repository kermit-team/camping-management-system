from rest_framework import serializers

from camping.models import Payment


class PaymentResponseSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Payment
        fields = '__all__'
