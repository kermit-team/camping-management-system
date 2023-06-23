from typing import Any, Dict, Optional

from account.models import User
from account.serializers import errors_serializer
from camping.models import Car


class CarService:

    @staticmethod
    def add_user_to_car(pk: int, user: User) -> Dict[str, Any]:
        try:
            car = Car.objects.get(pk=pk)
            car.drivers.add(user)
            response = {'status': 'Success', 'content': car}
        except Exception as err:
            response = {'status': 'Error', 'errors': errors_serializer(err)}

        return response

    @staticmethod
    def remove_user_from_car(pk: int, user: User) -> Dict[str, Any]:
        try:
            car = Car.objects.get(pk=pk)
            car.drivers.remove(user)
            response = {'status': 'Success', 'content': car}
        except Exception as err:
            response = {'status': 'Error', 'errors': errors_serializer(err)}

        return response

    @staticmethod
    def get_cars(
        order_by: str = 'id',
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        try:
            if filters:
                cars = Car.objects.filter(**filters).order_by(order_by)
            else:
                cars = Car.objects.all().order_by(order_by)
            response = {'status': 'Success', 'content': cars}
        except Exception as err:
            response = {'status': 'Error', 'errors': errors_serializer(err)}

        return response

    @staticmethod
    def get_car(pk: int) -> Dict[str, Any]:
        try:
            car = Car.objects.get(pk=pk)
            response = {'status': 'Success', 'content': car}
        except Exception as err:
            response = {'status': 'Error', 'errors': errors_serializer(err)}

        return response

    @staticmethod
    def create_car(car_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            car = Car.objects.create(**car_data)
            response = {'status': 'Success', 'content': car}
        except Exception as err:
            response = {'status': 'Error', 'errors': errors_serializer(err)}

        return response

    @staticmethod
    def update_car(pk: int, car_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if car_data:
                Car.objects.filter(pk=pk).update(**car_data)
            car = Car.objects.get(pk=pk)
            response = {'status': 'Success', 'content': car}
        except Exception as err:
            response = {'status': 'Error', 'errors': errors_serializer(err)}

        return response

    @staticmethod
    def delete_car(pk: int) -> Dict[str, Any]:
        try:
            car = Car.objects.get(pk=pk)
            car.delete()
            response = {'status': 'Success'}
        except Exception as err:
            response = {'status': 'Error', 'errors': errors_serializer(err)}

        return response
