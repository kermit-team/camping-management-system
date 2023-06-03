from typing import Any, Dict, Optional

from camping.models import Payment


class PaymentService:

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
            response = {'status': 'Error', 'errors': [str(err)]}

        return response

    @staticmethod
    def get_payment(pk: int) -> Dict[str, Any]:
        try:
            payment = Payment.objects.get(pk=pk)
            response = {'status': 'Success', 'content': payment}
        except Exception as err:
            response = {'status': 'Error', 'errors': [str(err)]}

        return response

    @staticmethod
    def create_payment(payment_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            payment = Payment.objects.create(**payment_data)
            response = {'status': 'Success', 'content': payment}
        except Exception as err:
            response = {'status': 'Error', 'errors': [str(err)]}

        return response

    @staticmethod
    def update_payment(pk: int, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if payment_data:
                Payment.objects.filter(pk=pk).update(**payment_data)
            payment = Payment.objects.get(pk=pk)
            response = {'status': 'Success', 'content': payment}
        except Exception as err:
            response = {'status': 'Error', 'errors': [str(err)]}

        return response

    @staticmethod
    def delete_payment(pk: int) -> Dict[str, Any]:
        try:
            payment = Payment.objects.get(pk=pk)
            payment.delete()
            response = {'status': 'Success'}
        except Exception as err:
            response = {'status': 'Error', 'errors': [str(err)]}

        return response
