from typing import Any, Dict, List, Optional, Union

from django.db.models import QuerySet
from django.db.utils import IntegrityError
from django.core.exceptions import FieldError, FieldDoesNotExist

from camping.models import Car


class CarService:

    @staticmethod
    def get_cars(
        order_by: str = 'id',
        filters: Optional[Dict[str, Any]] = None) -> Optional[Union[QuerySet, List[Car]]]:
        try:
            if filters:
                cars = Car.objects.filter(**filters).order_by(order_by)
            else:
                cars = Car.objects.all().order_by(order_by)
            return cars
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None
            
    @staticmethod
    def get_car(pk: int) -> Optional[Car]:
        try:
            car = Car.objects.get(pk=pk)
            return car
        except Car.DoesNotExist:
            return None
    
    @staticmethod
    def create_car(car_data: Dict[str, Any]) -> Optional[Car]:
        try:
            car = Car.objects.create_car(**car_data)
                    
            return car
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None
        except IntegrityError:
            return None

    @staticmethod
    def update_car(pk: int, car_data: Dict[str, Any]) -> Optional[Car]:
        try:
            if car_data:                    
                Car.objects.filter(pk=pk).update(**car_data)
                car = Car.objects.get(pk=pk)
                return car
            
        except Car.DoesNotExist:
            return None
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None


    @staticmethod
    def delete_car(pk:int) -> bool:
        try:
            car = Car.objects.get(pk=pk)
            car.delete()
            return True
        except Car.DoesNotExist:
            return False
        