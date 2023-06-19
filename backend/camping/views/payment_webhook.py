import stripe
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from camping.services import PaymentService


class PaymentWebhookView(APIView):
    permission_classes = [AllowAny]
    stripe.api_key = settings.STRIPE_API_KEY

    @staticmethod
    def post(request):
        payload = request.data

        if not payload or payload.get('object') != 'event':
            return Response(
                'Webhook error while parsing basic request.',
                status=status.HTTP_400_BAD_REQUEST,
            )

        if payload['type'] == 'checkout.session.completed':
            session = stripe.checkout.Session.retrieve(
                payload['data']['object']['id'],
            )

            service_response = PaymentService.update_payment_status(session.id, session.payment_status)
            if service_response['status'] == 'Error':
                return Response(
                    json.loads(service_response['errors']),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            print(f'Updated payment with checkout id {session.id} to status {service_response["content"]}')

        elif payload['type'] == 'checkout.session.expired':
            session = stripe.checkout.Session.retrieve(
                payload['data']['object']['id'],
            )

            service_response = PaymentService.update_payment_status(session.id, 'expired')
            if service_response['status'] == 'Error':
                return Response(
                    json.loads(service_response['errors']),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            print(f'Updated payment with checkout id {session.id} to status {service_response["content"]}')
        else:
            # Unexpected event type
            print(f'Unhandled event type {payload["type"]}')

        return Response()
