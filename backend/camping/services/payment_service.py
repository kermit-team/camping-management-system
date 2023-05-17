from typing import Any, Dict, List, Optional, Union

from django.db.models import QuerySet
from django.db.utils import IntegrityError
from django.core.exceptions import FieldError, FieldDoesNotExist

from camping.models import Payment


class PaymentService:

    @staticmethod
    def get_payments(
        order_by: str = 'id',
        filters: Optional[Dict[str, Any]] = None) -> Optional[Union[QuerySet, List[Payment]]]:
        try:
            if filters:
                payments = Payment.objects.filter(**filters).order_by(order_by)
            else:
                payments = Payment.objects.all().order_by(order_by)
            return payments
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None
            
    @staticmethod
    def get_payment(pk: int) -> Optional[Payment]:
        try:
            payment = Payment.objects.get(pk=pk)
            return payment
        except Payment.DoesNotExist:
            return None
    
    @staticmethod
    def create_payment(payment_data: Dict[str, Any]) -> Optional[Payment]:
        try:
            payment = Payment.objects.create_payment(**payment_data)
                    
            return payment
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None
        except IntegrityError:
            return None

    @staticmethod
    def update_payment(pk: int, payment_data: Dict[str, Any]) -> Optional[Payment]:
        try:
            if payment_data:                    
                Payment.objects.filter(pk=pk).update(**payment_data)
                payment = Payment.objects.get(pk=pk)
                return payment
            
        except Payment.DoesNotExist:
            return None
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None


    @staticmethod
    def delete_payment(pk:int) -> bool:
        try:
            payment = Payment.objects.get(pk=pk)
            payment.delete()
            return True
        except Payment.DoesNotExist:
            return False
        