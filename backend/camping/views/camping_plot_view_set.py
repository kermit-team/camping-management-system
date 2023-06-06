from django.http import Http404
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.viewsets import ViewSet

from camping.models import CampingPlot
from camping.serializers import CampingPlotRequestSerializer, CampingPlotResponseSerializer
from camping.services import CampingPlotService


class CampingPlotViewSet(ViewSet):
    queryset = CampingPlot.objects.none()

    @staticmethod
    def list(request):
        filters = {}
        filters_errors = {}
        params = {k: v[0] for k, v in dict(request.query_params).items()}
        order_by = params.pop('order_by', 'id')

        if not CampingPlot.field_exists(order_by):
            filters_errors['order_by'] = _('Invalid field name')

        for k, v in params.items():
            field_name = k if '__' not in k else k.split('__')[0]
            if CampingPlot.field_exists(field_name):
                if '__in' in k or k[-1] == 's':
                    filters[k] = [
                        int(string) if string.isdigit() else string.strip()
                        for string in v.split(',')
                    ]
                else:
                    filters[k] = v
            else:
                filters_errors[k] = _('Field does not exist')

        if filters_errors:
            return Response(filters_errors, status.HTTP_400_BAD_REQUEST)

        service_response = CampingPlotService.get_camping_plots(
            filters=filters,
            order_by=order_by,
        )
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        camping_plots_list_serializer = CampingPlotResponseSerializer(service_response['content'], many=True)
        return Response(camping_plots_list_serializer.data)

    @staticmethod
    def create(request):
        camping_plot_serializer = CampingPlotRequestSerializer(data=request.data)
        camping_plot_serializer.is_valid(raise_exception=True)

        service_response = CampingPlotService.create_camping_plot(camping_plot_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        response_camping_plot_serializer = CampingPlotResponseSerializer(service_response['content'])
        return Response(
            response_camping_plot_serializer.data,
            status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None):
        service_response = CampingPlotService.get_camping_plot(pk)
        if service_response['status'] == 'Error':
            raise Http404
        camping_plot = service_response['content']
        self.check_object_permissions(request, camping_plot)
        response_camping_plot_serializer = CampingPlotResponseSerializer(camping_plot)

        return Response(response_camping_plot_serializer.data)

    def update(self, request, pk=None):
        service_response = CampingPlotService.get_camping_plot(pk)
        if service_response['status'] == 'Error':
            raise Http404
        camping_plot = service_response['content']
        self.check_object_permissions(request, camping_plot)

        camping_plot_serializer = CampingPlotRequestSerializer(
            camping_plot,
            data=request.data,
        )
        camping_plot_serializer.is_valid(raise_exception=True)

        service_response = CampingPlotService.update_camping_plot(pk, camping_plot_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        response_camping_plot_serializer = CampingPlotResponseSerializer(service_response['content'])
        return Response(
            response_camping_plot_serializer.data,
            status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        service_response = CampingPlotService.get_camping_plot(pk)
        if service_response['status'] == 'Error':
            raise Http404
        camping_plot = service_response['content']
        self.check_object_permissions(request, camping_plot)

        camping_plot_serializer = CampingPlotRequestSerializer(
            camping_plot,
            data=request.data,
            partial=True,
        )
        camping_plot_serializer.is_valid(raise_exception=True)

        service_response = CampingPlotService.update_camping_plot(pk, camping_plot_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        response_camping_plot_serializer = CampingPlotResponseSerializer(service_response['content'])
        return Response(
            response_camping_plot_serializer.data,
            status.HTTP_201_CREATED,
        )

    def destroy(self, request, pk=None):
        service_response = CampingPlotService.get_camping_plot(pk)
        if service_response['status'] == 'Error':
            raise Http404
        camping_plot = service_response['content']
        self.check_object_permissions(request, camping_plot)

        service_response = CampingPlotService.delete_camping_plot(pk)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {'message': _('Camping plot has been deleted')},
            status.HTTP_204_NO_CONTENT,
        )
