from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from camping.serializers import CampingPlotResponseSerializer, AvailableCampingPlotsRequestSerializer
from camping.services import CampingPlotService


class AvailableCampingPlotsView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        available_camping_plots_serializer = AvailableCampingPlotsRequestSerializer(data=request.data)
        available_camping_plots_serializer.is_valid(raise_exception=True)

        service_response = CampingPlotService.get_available_camping_plots(
            available_camping_plots_serializer.validated_data['date_from'],
            available_camping_plots_serializer.validated_data['date_to'],
        )

        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        camping_plots_list_serializer = CampingPlotResponseSerializer(service_response['content'], many=True)
        return Response(camping_plots_list_serializer.data)
