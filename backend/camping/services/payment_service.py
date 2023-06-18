import time
from typing import Any, Dict, Optional

import stripe
from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework.utils import json

from camping.models import Payment


class PaymentService:
    stripe.api_key = settings.STRIPE_API_KEY

    @staticmethod
    def create_stripe_checkout_session(payment_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email=payment_data['email'],
                line_items=[
                    {
                        "price_data": {
                            "currency": "pln",
                            "product_data": {
                                "name": f"Rezerwacja parceli {payment_data['camping_plot']} w terminie {payment_data['date_from']} - {payment_data['date_to']}",
                            },
                            "unit_amount": int(payment_data['camping_plot'].camping_section.plot_price * 100),
                        },
                        "quantity": (payment_data['date_to'] - payment_data['date_from']).days,
                    },
                    {
                        "price_data": {
                            "currency": "pln",
                            "product_data": {"name": "Opłata za osoby dorosłe"},
                            "unit_amount": int(payment_data['camping_plot'].camping_section.price_per_adult * 100),
                        },
                        "quantity": payment_data['number_of_adults'],
                    },
                    {
                        "price_data": {
                            "currency": "pln",
                            "product_data": {"name": "Opłata za dzieci"},
                            "unit_amount": int(payment_data['camping_plot'].camping_section.price_per_child * 100),
                        },
                        "quantity": payment_data['number_of_children'],
                    },
                ],
                mode="payment",
                success_url="http://localhost:4242/payment_data/payment/success",
                cancel_url="http://localhost:4242/payment_data/payment/cancel",
                expires_at=int(time.time() + 3600),  # Configured to expire after 1 hour,
            )
            return checkout_session
        except Exception:
            return None

    @staticmethod
    def update_stripe_checkout_session(payment_data: Dict[str, Any], checkout_id: str) -> Optional[Dict[str, Any]]:

        try:
            checkout_session = PaymentService.create_stripe_checkout_session(payment_data)

            expired_checkout_session = stripe.checkout.Session.expire(checkout_id)
            if not expired_checkout_session.get('id'):
                raise Exception

            return checkout_session
        except Exception:
            return None

    @staticmethod
    def update_payment_status(checkout_id: str, status: str) -> Dict[str, Any]:

        try:
            payment = Payment.objects.filter(stripe_checkout_id=checkout_id)
            if not payment:
                raise Exception(_('Payment with given checkout id doesn\'t exist'))

            new_status = None
            match status:
                case 'unpaid':
                    new_status = Payment.Status.UNPAID

                case 'paid':
                    new_status = Payment.Status.PAID

                case 'returned':
                    new_status = Payment.Status.RETURNED

                case 'expired':
                    new_status = Payment.Status.CANCELED

            payment.update(status=new_status)

            response = {'status': 'Success', 'content': new_status}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response

    @staticmethod
    def get_payments(
        order_by: str = 'id',
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        try:
            if filters:
                payments = Payment.objects.filter(**filters).order_by(order_by)
            else:
                payments = Payment.objects.all().order_by(order_by)
            response = {'status': 'Success', 'content': payments}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response

    @staticmethod
    def get_payment(pk: int) -> Dict[str, Any]:
        try:
            payment = Payment.objects.get(pk=pk)
            response = {'status': 'Success', 'content': payment}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response

    @staticmethod
    def create_payment(payment_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            checkout_session = PaymentService.create_stripe_checkout_session(payment_data)
            if not checkout_session:
                raise Exception(json.dumps({'payment': _('Error occurred while trying to create payment page')}))

            payment = Payment.objects.create(
                price=payment_data['price'],
                stripe_checkout_id=checkout_session['id'],
            )

            response = {'status': 'Success', 'content': {'payment': payment, 'checkout_session': checkout_session}}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response

    @staticmethod
    def update_payment(pk: int, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            checkout_session = None
            if payment_data:
                payment = Payment.objects.get(pk=pk)
                checkout_session = PaymentService.update_stripe_checkout_session(payment_data,
                                                                                 payment.stripe_checkout_id)

                if not checkout_session:
                    raise Exception(json.dumps({'payment': _('Error occurred while trying to create payment page')}))

                Payment.objects.filter(pk=pk).update(
                    price=payment_data['price'],
                    stripe_checkout_id=checkout_session['id'],
                    status=Payment.Status.WAITING_FOR_PAYMENT,
                )

            payment = Payment.objects.get(pk=pk)
            response = {'status': 'Success', 'content': {'payment': payment}}
            if checkout_session:
                response['content']['checkout_session'] = checkout_session
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response

    @staticmethod
    def delete_payment(pk: int) -> Dict[str, Any]:
        try:
            payment = Payment.objects.get(pk=pk)
            payment.delete()
            response = {'status': 'Success'}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response
