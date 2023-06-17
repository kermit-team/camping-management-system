from django.http import Http404
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.viewsets import ViewSet

from account.services import MailService
from camping.models import Reservation
from camping.permissions import UserRelatedToObjectOrStaffPermissions
from camping.serializers import ReservationRequestSerializer, ReservationResponseSerializer
from camping.serializers.reservation_create_serializer import ReservationCreateSerializer
from camping.services import ReservationService


class ReservationViewSet(ViewSet):
    queryset = Reservation.objects.none()
    permission_classes = [UserRelatedToObjectOrStaffPermissions]

    @staticmethod
    def list(request):
        filters = {}
        filters_errors = {}
        params = {k: v[0] for k, v in dict(request.query_params).items()}
        order_by = params.pop('order_by', 'id')

        if not Reservation.field_exists(order_by):
            filters_errors['order_by'] = _('Invalid field name')

        for k, v in params.items():
            field_name = k if '__' not in k else k.split('__')[0]
            if Reservation.field_exists(field_name):
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

        service_response = ReservationService.get_reservations(
            filters=filters,
            order_by=order_by,
        )
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        reservations_list_serializer = ReservationResponseSerializer(service_response['content'], many=True)
        return Response(reservations_list_serializer.data)

    @staticmethod
    def create(request):
        reservation_serializer = ReservationCreateSerializer(data=request.data)
        reservation_serializer.is_valid(raise_exception=True)

        reservation_data = reservation_serializer.validated_data
        reservation_data['user'] = request.user

        service_response = ReservationService.create_reservation(reservation_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        MailService.send_reservation_payment_mail(reservation_data['user'], service_response['content']['checkout_url'])
        response_reservation_serializer = ReservationResponseSerializer(service_response['content']['reservation'])
        return Response(
            {
                'reservation': response_reservation_serializer.data,
                'checkout_url': service_response['content']['checkout_url'],
            },
            status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None):
        service_response = ReservationService.get_reservation(pk)
        if service_response['status'] == 'Error':
            raise Http404
        reservation = service_response['content']
        self.check_object_permissions(request, reservation)

        response_reservation_serializer = ReservationResponseSerializer(reservation)
        return Response(response_reservation_serializer.data)

    def update(self, request, pk=None):
        service_response = ReservationService.get_reservation(pk)
        if service_response['status'] == 'Error':
            raise Http404
        reservation = service_response['content']
        self.check_object_permissions(request, reservation)

        reservation_serializer = ReservationRequestSerializer(
            reservation,
            data=request.data,
        )
        reservation_serializer.is_valid(raise_exception=True)

        service_response = ReservationService.update_reservation(pk, reservation_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        response_reservation_serializer = ReservationResponseSerializer(service_response['content'])
        return Response(
            response_reservation_serializer.data,
            status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        service_response = ReservationService.get_reservation(pk)
        if service_response['status'] == 'Error':
            raise Http404
        reservation = service_response['content']
        self.check_object_permissions(request, reservation)

        reservation_serializer = ReservationRequestSerializer(
            reservation,
            data=request.data,
            partial=True,
        )
        reservation_serializer.is_valid(raise_exception=True)

        service_response = ReservationService.update_reservation(pk, reservation_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        response_reservation_serializer = ReservationResponseSerializer(service_response['content'])
        return Response(
            response_reservation_serializer.data,
            status.HTTP_201_CREATED,
        )

    def destroy(self, request, pk=None):
        service_response = ReservationService.get_reservation(pk)
        if service_response['status'] == 'Error':
            raise Http404
        reservation = service_response['content']
        self.check_object_permissions(request, reservation)

        service_response = ReservationService.delete_reservation(pk)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {'message': _('Reservation has been deleted')},
            status.HTTP_204_NO_CONTENT,
        )
