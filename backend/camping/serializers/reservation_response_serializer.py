from rest_framework import serializers

from camping.models import Reservation
from .camping_plot_response_serializer import CampingPlotResponseSerializer
from .car_response_serializer import CarResponseSerializer

from account.serializers import UserResponseSerializer 


class ReservationResponseSerializer(serializers.ModelSerializer):
    user = UserResponseSerializer(read_only=True)
    car = CarResponseSerializer(read_only=True)
    camping_plot = CampingPlotResponseSerializer(read_only=True)
    
    class Meta:
        model = Reservation
        fields = '__all__'