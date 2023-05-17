from django.http import Http404
from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from camping.models import Car
from camping.serializers import CarRequestSerializer, CarResponseSerializer
from camping.services import CarService


class CarViewSet(ViewSet):

    def list(self, request):
        filters = {}        
        filters_errors = {}
        params = {k: v[0] for k, v in dict(request.query_params).items()}
        order_by = params.pop('order_by', 'id')
        
        if not Car.field_exists(order_by):
            filters_errors['order_by'] = _('Invalid field name')
        
        for k, v in params.items():
            if Car.field_exists(k) if '__' not in k else Car.field_exists(k.split('__')[0]):
                filters[k] = [int(string) if string.isdigit() else string.strip() for string in v.split(',')] if ('__in' in k or k[-1] == 's') else v
            else:
                filters_errors[k] = _('Field does not exist')
        
        if filters_errors:
            return Response (
                {'errors': filters_errors},
                status.HTTP_400_BAD_REQUEST,
            )  
        
        queryset_of_cars = CarService.get_cars(
            filters=filters, 
            order_by=order_by,
        )
        
        serializer_context = {
            'request': request,
        }

        cars_list_serializer = CarResponseSerializer(
            queryset_of_cars, 
            many = True,
            context = serializer_context,
        )

        return Response(cars_list_serializer.data)

    def create(self, request):        
        car_serializer = CarRequestSerializer(data=request.data)
        car_serializer.is_valid(raise_exception=True)

        serializer_context = {
            'request': request,
        }

        created_car = CarService.create_car(car_serializer.validated_data)
        if created_car:
            
            response_car_serializer = CarResponseSerializer(
                created_car,
                context = serializer_context,
            )

            return Response(
                response_car_serializer.data,
                status.HTTP_201_CREATED,
            )

    def retrieve(self, request, pk=None):
        car = CarService.get_car(pk)
        if not car:
            raise Http404
        self.check_object_permissions(self.request, car)
        serializer_context = {
            'request': request,
        }

        response_car_serializer = CarResponseSerializer(
            car,
            context = serializer_context,
        )

        return Response(response_car_serializer.data)

    def update(self, request, pk=None):
        car = CarService.get_car(pk)
        if not car:
            raise Http404
        self.check_object_permissions(self.request, car)
        serializer_context = {
            'request': request,
        }
        
        car_serializer = CarRequestSerializer(
            car, 
            data = request.data,
        )
        car_serializer.is_valid(raise_exception=True)

        updated_car = CarService.update_car(pk, car_serializer.validated_data)
        response_car_serializer = CarResponseSerializer(
            updated_car,
            context = serializer_context,
        )

        return Response(
            response_car_serializer.data,
            status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        car = CarService.get_car(pk)
        if not car:
            raise Http404
        self.check_object_permissions(self.request, car)
        serializer_context = {
            'request': request,
        }        

        car_serializer = CarRequestSerializer(
            car, 
            data = request.data,
            partial = True,
        )
        car_serializer.is_valid(raise_exception=True)

        updated_car = CarService.update_car(pk, car_serializer.validated_data)
        response_car_serializer = CarResponseSerializer(
            updated_car,
            context = serializer_context,
        )

        return Response(
            response_car_serializer.data,
            status.HTTP_201_CREATED,
        )
        
    def destroy(self, request, pk=None):
        car = CarService.get_car(pk)
        if not car:
            raise Http404
        self.check_object_permissions(self.request, car)

        if CarService.delete_car(pk):
            return Response(
                {'message': _('Car has been deleted')},
                status.HTTP_204_NO_CONTENT,
            )
        