from django.http import Http404
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.viewsets import ViewSet

from camping.models import Payment
from camping.serializers import PaymentRequestSerializer, PaymentResponseSerializer
from camping.services import PaymentService


class PaymentViewSet(ViewSet):
    queryset = Payment.objects.none()

    @staticmethod
    def list(request):
        filters = {}
        filters_errors = {}
        params = {k: v[0] for k, v in dict(request.query_params).items()}
        order_by = params.pop('order_by', 'id')

        if not Payment.field_exists(order_by):
            filters_errors['order_by'] = _('Invalid field name')

        for k, v in params.items():
            field_name = k if '__' not in k else k.split('__')[0]
            if Payment.field_exists(field_name):
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

        service_response = PaymentService.get_payments(
            filters=filters,
            order_by=order_by,
        )
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        payments_list_serializer = PaymentResponseSerializer(service_response['content'], many=True)
        return Response(payments_list_serializer.data)

    @staticmethod
    def create(request):
        payment_serializer = PaymentRequestSerializer(data=request.data)
        payment_serializer.is_valid(raise_exception=True)

        service_response = PaymentService.create_payment(payment_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        response_payment_serializer = PaymentResponseSerializer(service_response['content'])
        return Response(
            response_payment_serializer.data,
            status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None):
        service_response = PaymentService.get_payment(pk)
        if service_response['status'] == 'Error':
            raise Http404
        payment = service_response['content']
        self.check_object_permissions(request, payment)

        response_payment_serializer = PaymentResponseSerializer(payment)
        return Response(response_payment_serializer.data)

    def update(self, request, pk=None):
        service_response = PaymentService.get_payment(pk)
        if service_response['status'] == 'Error':
            raise Http404
        payment = service_response['content']
        self.check_object_permissions(request, payment)

        payment_serializer = PaymentRequestSerializer(
            payment,
            data=request.data,
        )
        payment_serializer.is_valid(raise_exception=True)

        service_response = PaymentService.update_payment(pk, payment_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        response_payment_serializer = PaymentResponseSerializer(service_response['content'])
        return Response(
            response_payment_serializer.data,
            status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        service_response = PaymentService.get_payment(pk)
        if service_response['status'] == 'Error':
            raise Http404
        payment = service_response['content']
        self.check_object_permissions(request, payment)

        payment_serializer = PaymentRequestSerializer(
            payment,
            data=request.data,
            partial=True,
        )
        payment_serializer.is_valid(raise_exception=True)

        service_response = PaymentService.update_payment(pk, payment_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        response_payment_serializer = PaymentResponseSerializer(service_response['content'])
        return Response(
            response_payment_serializer.data,
            status.HTTP_201_CREATED,
        )

    def destroy(self, request, pk=None):
        service_response = PaymentService.get_payment(pk)
        if service_response['status'] == 'Error':
            raise Http404
        payment = service_response['content']
        self.check_object_permissions(request, payment)

        service_response = PaymentService.delete_payment(pk)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {'message': _('Payment has been deleted')},
            status.HTTP_204_NO_CONTENT,
        )
