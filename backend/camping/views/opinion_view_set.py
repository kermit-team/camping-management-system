from django.http import Http404
from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from camping.models import Opinion
from camping.serializers import OpinionRequestSerializer, OpinionResponseSerializer
from camping.services import OpinionService


class OpinionViewSet(ViewSet):

    def list(self, request):
        filters = {}        
        filters_errors = {}
        params = {k: v[0] for k, v in dict(request.query_params).items()}
        order_by = params.pop('order_by', 'id')
        
        if not Opinion.field_exists(order_by):
            filters_errors['order_by'] = _('Invalid field name')
        
        for k, v in params.items():
            if Opinion.field_exists(k) if '__' not in k else Opinion.field_exists(k.split('__')[0]):
                filters[k] = [int(string) if string.isdigit() else string.strip() for string in v.split(',')] if ('__in' in k or k[-1] == 's') else v
            else:
                filters_errors[k] = _('Field does not exist')
        
        if filters_errors:
            return Response (
                {'errors': filters_errors},
                status.HTTP_400_BAD_REQUEST,
            )  
        
        queryset_of_opinions = OpinionService.get_opinions(
            filters=filters, 
            order_by=order_by,
        )
        
        serializer_context = {
            'request': request,
        }

        opinions_list_serializer = OpinionResponseSerializer(
            queryset_of_opinions, 
            many = True,
            context = serializer_context,
        )

        return Response(opinions_list_serializer.data)

    def create(self, request):        
        opinion_serializer = OpinionRequestSerializer(data=request.data)
        opinion_serializer.is_valid(raise_exception=True)

        serializer_context = {
            'request': request,
        }

        created_opinion = OpinionService.create_opinion(opinion_serializer.validated_data)
        if created_opinion:
            
            response_opinion_serializer = OpinionResponseSerializer(
                created_opinion,
                context = serializer_context,
            )

            return Response(
                response_opinion_serializer.data,
                status.HTTP_201_CREATED,
            )

    def retrieve(self, request, pk=None):
        opinion = OpinionService.get_opinion(pk)
        if not opinion:
            raise Http404
        self.check_object_permissions(self.request, opinion)
        serializer_context = {
            'request': request,
        }

        response_opinion_serializer = OpinionResponseSerializer(
            opinion,
            context = serializer_context,
        )

        return Response(response_opinion_serializer.data)

    def update(self, request, pk=None):
        opinion = OpinionService.get_opinion(pk)
        if not opinion:
            raise Http404
        self.check_object_permissions(self.request, opinion)
        serializer_context = {
            'request': request,
        }
        
        opinion_serializer = OpinionRequestSerializer(
            opinion, 
            data = request.data,
        )
        opinion_serializer.is_valid(raise_exception=True)

        updated_opinion = OpinionService.update_opinion(pk, opinion_serializer.validated_data)
        response_opinion_serializer = OpinionResponseSerializer(
            updated_opinion,
            context = serializer_context,
        )

        return Response(
            response_opinion_serializer.data,
            status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        opinion = OpinionService.get_opinion(pk)
        if not opinion:
            raise Http404
        self.check_object_permissions(self.request, opinion)
        serializer_context = {
            'request': request,
        }        

        opinion_serializer = OpinionRequestSerializer(
            opinion, 
            data = request.data,
            partial = True,
        )
        opinion_serializer.is_valid(raise_exception=True)

        updated_opinion = OpinionService.update_opinion(pk, opinion_serializer.validated_data)
        response_opinion_serializer = OpinionResponseSerializer(
            updated_opinion,
            context = serializer_context,
        )

        return Response(
            response_opinion_serializer.data,
            status.HTTP_201_CREATED,
        )
        
    def destroy(self, request, pk=None):
        opinion = OpinionService.get_opinion(pk)
        if not opinion:
            raise Http404
        self.check_object_permissions(self.request, opinion)

        if OpinionService.delete_opinion(pk):
            return Response(
                {'message': _('Opinion has been deleted')},
                status.HTTP_204_NO_CONTENT,
            )
        