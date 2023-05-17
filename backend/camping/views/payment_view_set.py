from django.http import Http404
from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from camping.models import Payment
from camping.serializers import PaymentRequestSerializer, PaymentResponseSerializer
from camping.services import PaymentService


class PaymentViewSet(ViewSet):

    def list(self, request):
        filters = {}        
        filters_errors = {}
        params = {k: v[0] for k, v in dict(request.query_params).items()}
        order_by = params.pop('order_by', 'id')
        
        if not Payment.field_exists(order_by):
            filters_errors['order_by'] = _('Invalid field name')
        
        for k, v in params.items():
            if Payment.field_exists(k) if '__' not in k else Payment.field_exists(k.split('__')[0]):
                filters[k] = [int(string) if string.isdigit() else string.strip() for string in v.split(',')] if ('__in' in k or k[-1] == 's') else v
            else:
                filters_errors[k] = _('Field does not exist')
        
        if filters_errors:
            return Response (
                {'errors': filters_errors},
                status.HTTP_400_BAD_REQUEST,
            )  
        
        queryset_of_payments = PaymentService.get_payments(
            filters=filters, 
            order_by=order_by,
        )
        
        serializer_context = {
            'request': request,
        }

        payments_list_serializer = PaymentResponseSerializer(
            queryset_of_payments, 
            many = True,
            context = serializer_context,
        )

        return Response(payments_list_serializer.data)

    def create(self, request):        
        payment_serializer = PaymentRequestSerializer(data=request.data)
        payment_serializer.is_valid(raise_exception=True)

        serializer_context = {
            'request': request,
        }

        created_payment = PaymentService.create_payment(payment_serializer.validated_data)
        if created_payment:
            
            response_payment_serializer = PaymentResponseSerializer(
                created_payment,
                context = serializer_context,
            )

            return Response(
                response_payment_serializer.data,
                status.HTTP_201_CREATED,
            )

    def retrieve(self, request, pk=None):
        payment = PaymentService.get_payment(pk)
        if not payment:
            raise Http404
        self.check_object_permissions(self.request, payment)
        serializer_context = {
            'request': request,
        }

        response_payment_serializer = PaymentResponseSerializer(
            payment,
            context = serializer_context,
        )

        return Response(response_payment_serializer.data)

    def update(self, request, pk=None):
        payment = PaymentService.get_payment(pk)
        if not payment:
            raise Http404
        self.check_object_permissions(self.request, payment)
        serializer_context = {
            'request': request,
        }
        
        payment_serializer = PaymentRequestSerializer(
            payment, 
            data = request.data,
        )
        payment_serializer.is_valid(raise_exception=True)

        updated_payment = PaymentService.update_payment(pk, payment_serializer.validated_data)
        response_payment_serializer = PaymentResponseSerializer(
            updated_payment,
            context = serializer_context,
        )

        return Response(
            response_payment_serializer.data,
            status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        payment = PaymentService.get_payment(pk)
        if not payment:
            raise Http404
        self.check_object_permissions(self.request, payment)
        serializer_context = {
            'request': request,
        }        

        payment_serializer = PaymentRequestSerializer(
            payment, 
            data = request.data,
            partial = True,
        )
        payment_serializer.is_valid(raise_exception=True)

        updated_payment = PaymentService.update_payment(pk, payment_serializer.validated_data)
        response_payment_serializer = PaymentResponseSerializer(
            updated_payment,
            context = serializer_context,
        )

        return Response(
            response_payment_serializer.data,
            status.HTTP_201_CREATED,
        )
        
    def destroy(self, request, pk=None):
        payment = PaymentService.get_payment(pk)
        if not payment:
            raise Http404
        self.check_object_permissions(self.request, payment)

        if PaymentService.delete_payment(pk):
            return Response(
                {'message': _('Payment has been deleted')},
                status.HTTP_204_NO_CONTENT,
            )
        