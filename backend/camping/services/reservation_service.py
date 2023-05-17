from typing import Any, Dict, List, Optional, Union

from django.db.models import QuerySet
from django.db.utils import IntegrityError
from django.core.exceptions import FieldError, FieldDoesNotExist

from camping.models import Reservation


class ReservationService:

    @staticmethod
    def get_reservations(
        order_by: str = 'id',
        filters: Optional[Dict[str, Any]] = None) -> Optional[Union[QuerySet, List[Reservation]]]:
        try:
            if filters:
                reservations = Reservation.objects.filter(**filters).order_by(order_by)
            else:
                reservations = Reservation.objects.all().order_by(order_by)
            return reservations
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None
            
    @staticmethod
    def get_reservation(pk: int) -> Optional[Reservation]:
        try:
            reservation = Reservation.objects.get(pk=pk)
            return reservation
        except Reservation.DoesNotExist:
            return None
    
    @staticmethod
    def create_reservation(reservation_data: Dict[str, Any]) -> Optional[Reservation]:
        try:
            reservation = Reservation.objects.create_reservation(**reservation_data)
                    
            return reservation
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None
        except IntegrityError:
            return None

    @staticmethod
    def update_reservation(pk: int, reservation_data: Dict[str, Any]) -> Optional[Reservation]:
        try:
            if reservation_data:                    
                Reservation.objects.filter(pk=pk).update(**reservation_data)
                reservation = Reservation.objects.get(pk=pk)
                return reservation
            
        except Reservation.DoesNotExist:
            return None
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None


    @staticmethod
    def delete_reservation(pk:int) -> bool:
        try:
            reservation = Reservation.objects.get(pk=pk)
            reservation.delete()
            return True
        except Reservation.DoesNotExist:
            return False
        