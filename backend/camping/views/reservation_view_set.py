from django.http import Http404
from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from camping.models import Reservation
from camping.serializers import ReservationRequestSerializer, ReservationResponseSerializer
from camping.services import ReservationService


class ReservationViewSet(ViewSet):

    def list(self, request):
        filters = {}        
        filters_errors = {}
        params = {k: v[0] for k, v in dict(request.query_params).items()}
        order_by = params.pop('order_by', 'id')
        
        if not Reservation.field_exists(order_by):
            filters_errors['order_by'] = _('Invalid field name')
        
        for k, v in params.items():
            if Reservation.field_exists(k) if '__' not in k else Reservation.field_exists(k.split('__')[0]):
                filters[k] = [int(string) if string.isdigit() else string.strip() for string in v.split(',')] if ('__in' in k or k[-1] == 's') else v
            else:
                filters_errors[k] = _('Field does not exist')
        
        if filters_errors:
            return Response (
                {'errors': filters_errors},
                status.HTTP_400_BAD_REQUEST,
            )  
        
        queryset_of_reservations = ReservationService.get_reservations(
            filters=filters, 
            order_by=order_by,
        )
        
        serializer_context = {
            'request': request,
        }

        reservations_list_serializer = ReservationResponseSerializer(
            queryset_of_reservations, 
            many = True,
            context = serializer_context,
        )

        return Response(reservations_list_serializer.data)

    def create(self, request):        
        reservation_serializer = ReservationRequestSerializer(data=request.data)
        reservation_serializer.is_valid(raise_exception=True)

        serializer_context = {
            'request': request,
        }

        created_reservation = ReservationService.create_reservation(reservation_serializer.validated_data)
        if created_reservation:
            
            response_reservation_serializer = ReservationResponseSerializer(
                created_reservation,
                context = serializer_context,
            )

            return Response(
                response_reservation_serializer.data,
                status.HTTP_201_CREATED,
            )

    def retrieve(self, request, pk=None):
        reservation = ReservationService.get_reservation(pk)
        if not reservation:
            raise Http404
        self.check_object_permissions(self.request, reservation)
        serializer_context = {
            'request': request,
        }

        response_reservation_serializer = ReservationResponseSerializer(
            reservation,
            context = serializer_context,
        )

        return Response(response_reservation_serializer.data)

    def update(self, request, pk=None):
        reservation = ReservationService.get_reservation(pk)
        if not reservation:
            raise Http404
        self.check_object_permissions(self.request, reservation)
        serializer_context = {
            'request': request,
        }
        
        reservation_serializer = ReservationRequestSerializer(
            reservation, 
            data = request.data,
        )
        reservation_serializer.is_valid(raise_exception=True)

        updated_reservation = ReservationService.update_reservation(pk, reservation_serializer.validated_data)
        response_reservation_serializer = ReservationResponseSerializer(
            updated_reservation,
            context = serializer_context,
        )

        return Response(
            response_reservation_serializer.data,
            status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        reservation = ReservationService.get_reservation(pk)
        if not reservation:
            raise Http404
        self.check_object_permissions(self.request, reservation)
        serializer_context = {
            'request': request,
        }        

        reservation_serializer = ReservationRequestSerializer(
            reservation, 
            data = request.data,
            partial = True,
        )
        reservation_serializer.is_valid(raise_exception=True)

        updated_reservation = ReservationService.update_reservation(pk, reservation_serializer.validated_data)
        response_reservation_serializer = ReservationResponseSerializer(
            updated_reservation,
            context = serializer_context,
        )

        return Response(
            response_reservation_serializer.data,
            status.HTTP_201_CREATED,
        )
        
    def destroy(self, request, pk=None):
        reservation = ReservationService.get_reservation(pk)
        if not reservation:
            raise Http404
        self.check_object_permissions(self.request, reservation)

        if ReservationService.delete_reservation(pk):
            return Response(
                {'message': _('Reservation has been deleted')},
                status.HTTP_204_NO_CONTENT,
            )
        