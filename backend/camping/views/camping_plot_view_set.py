from django.http import Http404
from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from camping.models import CampingPlot
from camping.serializers import CampingPlotRequestSerializer, CampingPlotResponseSerializer
from camping.services import CampingPlotService


class CampingPlotViewSet(ViewSet):

    def list(self, request):
        filters = {}        
        filters_errors = {}
        params = {k: v[0] for k, v in dict(request.query_params).items()}
        order_by = params.pop('order_by', 'id')
        
        if not CampingPlot.field_exists(order_by):
            filters_errors['order_by'] = _('Invalid field name')
        
        for k, v in params.items():
            if CampingPlot.field_exists(k) if '__' not in k else CampingPlot.field_exists(k.split('__')[0]):
                filters[k] = [int(string) if string.isdigit() else string.strip() for string in v.split(',')] if ('__in' in k or k[-1] == 's') else v
            else:
                filters_errors[k] = _('Field does not exist')
        
        if filters_errors:
            return Response (
                {'errors': filters_errors},
                status.HTTP_400_BAD_REQUEST,
            )  
        
        queryset_of_camping_plots = CampingPlotService.get_camping_plots(
            filters=filters, 
            order_by=order_by,
        )
        
        serializer_context = {
            'request': request,
        }

        camping_plots_list_serializer = CampingPlotResponseSerializer(
            queryset_of_camping_plots, 
            many = True,
            context = serializer_context,
        )

        return Response(camping_plots_list_serializer.data)

    def create(self, request):        
        camping_plot_serializer = CampingPlotRequestSerializer(data=request.data)
        camping_plot_serializer.is_valid(raise_exception=True)

        serializer_context = {
            'request': request,
        }

        created_camping_plot = CampingPlotService.create_camping_plot(camping_plot_serializer.validated_data)
        if created_camping_plot:
            
            response_camping_plot_serializer = CampingPlotResponseSerializer(
                created_camping_plot,
                context = serializer_context,
            )

            return Response(
                response_camping_plot_serializer.data,
                status.HTTP_201_CREATED,
            )

    def retrieve(self, request, pk=None):
        camping_plot = CampingPlotService.get_camping_plot(pk)
        if not camping_plot:
            raise Http404
        self.check_object_permissions(self.request, camping_plot)
        serializer_context = {
            'request': request,
        }

        response_camping_plot_serializer = CampingPlotResponseSerializer(
            camping_plot,
            context = serializer_context,
        )

        return Response(response_camping_plot_serializer.data)

    def update(self, request, pk=None):
        camping_plot = CampingPlotService.get_camping_plot(pk)
        if not camping_plot:
            raise Http404
        self.check_object_permissions(self.request, camping_plot)
        serializer_context = {
            'request': request,
        }
        
        camping_plot_serializer = CampingPlotRequestSerializer(
            camping_plot, 
            data = request.data,
        )
        camping_plot_serializer.is_valid(raise_exception=True)

        updated_camping_plot = CampingPlotService.update_camping_plot(pk, camping_plot_serializer.validated_data)
        response_camping_plot_serializer = CampingPlotResponseSerializer(
            updated_camping_plot,
            context = serializer_context,
        )

        return Response(
            response_camping_plot_serializer.data,
            status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        camping_plot = CampingPlotService.get_camping_plot(pk)
        if not camping_plot:
            raise Http404
        self.check_object_permissions(self.request, camping_plot)
        serializer_context = {
            'request': request,
        }        

        camping_plot_serializer = CampingPlotRequestSerializer(
            camping_plot, 
            data = request.data,
            partial = True,
        )
        camping_plot_serializer.is_valid(raise_exception=True)

        updated_camping_plot = CampingPlotService.update_camping_plot(pk, camping_plot_serializer.validated_data)
        response_camping_plot_serializer = CampingPlotResponseSerializer(
            updated_camping_plot,
            context = serializer_context,
        )

        return Response(
            response_camping_plot_serializer.data,
            status.HTTP_201_CREATED,
        )
        
    def destroy(self, request, pk=None):
        camping_plot = CampingPlotService.get_camping_plot(pk)
        if not camping_plot:
            raise Http404
        self.check_object_permissions(self.request, camping_plot)

        if CampingPlotService.delete_camping_plot(pk):
            return Response(
                {'message': _('Camping plot has been deleted')},
                status.HTTP_204_NO_CONTENT,
            )
        