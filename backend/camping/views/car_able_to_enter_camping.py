from datetime import date

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from camping.serializers import CarAbleToEnterCampingSerializer
from camping.services import CarService, ReservationService


class CarAbleToEnterCampingView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        response_data = {
            'car_exists': True,
            'car_able_to_enter_camping': True,
        }

        car_able_to_enter_camping_serializer = CarAbleToEnterCampingSerializer(data=request.data)
        car_able_to_enter_camping_serializer.is_valid(raise_exception=True)

        service_response = CarService.get_cars(
            filters={
                'registration_plate': car_able_to_enter_camping_serializer.validated_data['registration_plate'],
            },
        )

        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        if not service_response['content']:
            response_data['car_exists'] = False
            response_data['car_able_to_enter_camping'] = False
            return Response(response_data)

        found_car = service_response['content'].first()
        service_response = ReservationService.get_reservations(
            filters={
                'date_from__lte': date.today(),
                'date_to__gte': date.today(),
                'car': found_car.id,
                'payment__status': 'A',
            },
        )

        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        if not service_response['content']:
            response_data['car_able_to_enter_camping'] = False
            return Response(response_data)

        return Response(response_data)
