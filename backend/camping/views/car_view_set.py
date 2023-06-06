from django.http import Http404
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.viewsets import ViewSet

from camping.models import Car
from camping.permissions import UserRelatedToObjectOrStaffPermissions
from camping.serializers import CarRequestSerializer, CarResponseSerializer
from camping.services import CarService


class CarViewSet(ViewSet):
    queryset = Car.objects.none()
    permission_classes = [UserRelatedToObjectOrStaffPermissions]

    @staticmethod
    def list(request):
        filters = {}
        filters_errors = {}
        params = {k: v[0] for k, v in dict(request.query_params).items()}
        order_by = params.pop('order_by', 'id')

        if not Car.field_exists(order_by):
            filters_errors['order_by'] = _('Invalid field name')

        for k, v in params.items():
            field_name = k if '__' not in k else k.split('__')[0]
            if Car.field_exists(field_name):
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

        service_response = CarService.get_cars(
            filters=filters,
            order_by=order_by,
        )
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        cars_list_serializer = CarResponseSerializer(service_response['content'], many=True)
        return Response(cars_list_serializer.data)

    @staticmethod
    def create(request):
        service_response = CarService.get_cars(filters={'registration_plate': request.data.get('registration_plate')})
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )
        cars = service_response['content']

        if cars.exists():
            service_response = CarService.add_user_to_car(cars.first().id, request.user)
            if service_response['status'] == 'Error':
                return Response(
                    json.loads(service_response['errors']),
                    status.HTTP_400_BAD_REQUEST,
                )
            car = service_response['content']
        else:
            car_serializer = CarRequestSerializer(data=request.data)
            car_serializer.is_valid(raise_exception=True)
            service_response = CarService.create_car(car_serializer.validated_data)
            if service_response['status'] == 'Error':
                return Response(
                    json.loads(service_response['errors']),
                    status.HTTP_400_BAD_REQUEST,
                )
            service_response = CarService.add_user_to_car(service_response['content'].id, request.user)
            if service_response['status'] == 'Error':
                return Response(
                    json.loads(service_response['errors']),
                    status.HTTP_400_BAD_REQUEST,
                )
            car = service_response['content']

        response_car_serializer = CarResponseSerializer(car)
        return Response(
            response_car_serializer.data,
            status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None):
        service_response = CarService.get_car(pk)
        if service_response['status'] == 'Error':
            raise Http404
        car = service_response['content']
        self.check_object_permissions(request, car)

        response_car_serializer = CarResponseSerializer(car)
        return Response(response_car_serializer.data)

    def update(self, request, pk=None):
        service_response = CarService.get_car(pk)
        if service_response['status'] == 'Error':
            raise Http404
        car = service_response['content']
        self.check_object_permissions(request, car)

        car_serializer = CarRequestSerializer(
            car,
            data=request.data,
        )
        car_serializer.is_valid(raise_exception=True)

        service_response = CarService.update_car(pk, car_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        response_car_serializer = CarResponseSerializer(service_response['content'])
        return Response(
            response_car_serializer.data,
            status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        service_response = CarService.get_car(pk)
        if service_response['status'] == 'Error':
            raise Http404
        car = service_response['content']
        self.check_object_permissions(request, car)

        car_serializer = CarRequestSerializer(
            car,
            data=request.data,
            partial=True,
        )
        car_serializer.is_valid(raise_exception=True)

        service_response = CarService.update_car(pk, car_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        response_car_serializer = CarResponseSerializer(service_response['content'])
        return Response(
            response_car_serializer.data,
            status.HTTP_201_CREATED,
        )

    def destroy(self, request, pk=None):
        service_response = CarService.get_car(pk)
        if service_response['status'] == 'Error':
            raise Http404
        car = service_response['content']
        self.check_object_permissions(request, car)

        if car.drivers.count() == 1:
            service_response = CarService.delete_car(pk)
            if service_response['status'] == 'Error':
                return Response(
                    json.loads(service_response['errors']),
                    status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                {'message': _('Car has been deleted')},
                status.HTTP_204_NO_CONTENT,
            )

        service_response = CarService.remove_user_from_car(pk, request.user)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {'message': _('User has been removed from car')},
            status.HTTP_204_NO_CONTENT,
        )
