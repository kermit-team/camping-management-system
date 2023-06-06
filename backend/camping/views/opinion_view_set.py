from django.http import Http404
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.viewsets import ViewSet

from camping.models import Opinion
from camping.permissions import UserRelatedToObjectOrStaffPermissions
from camping.serializers import OpinionRequestSerializer, OpinionResponseSerializer
from camping.serializers.opinion_create_serializer import OpinionCreateSerializer
from camping.services import OpinionService


class OpinionViewSet(ViewSet):
    queryset = Opinion.objects.none()
    permission_classes = [UserRelatedToObjectOrStaffPermissions]

    @staticmethod
    def list(request):
        filters = {}
        filters_errors = {}
        params = {k: v[0] for k, v in dict(request.query_params).items()}
        order_by = params.pop('order_by', 'id')

        if not Opinion.field_exists(order_by):
            filters_errors['order_by'] = _('Invalid field name')

        for k, v in params.items():
            field_name = k if '__' not in k else k.split('__')[0]
            if Opinion.field_exists(field_name):
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

        service_response = OpinionService.get_opinions(
            filters=filters,
            order_by=order_by,
        )
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        opinions_list_serializer = OpinionResponseSerializer(service_response['content'], many=True)
        return Response(opinions_list_serializer.data)

    @staticmethod
    def create(request):
        opinion_serializer = OpinionCreateSerializer(data=request.data)
        opinion_serializer.is_valid(raise_exception=True)

        service_response = OpinionService.create_opinion(opinion_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        response_opinion_serializer = OpinionResponseSerializer(service_response['content'])
        return Response(
            response_opinion_serializer.data,
            status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None):
        service_response = OpinionService.get_opinion(pk)
        if service_response['status'] == 'Error':
            raise Http404
        opinion = service_response['content']
        self.check_object_permissions(request, opinion)

        response_opinion_serializer = OpinionResponseSerializer(opinion)
        return Response(response_opinion_serializer.data)

    def update(self, request, pk=None):
        service_response = OpinionService.get_opinion(pk)
        if service_response['status'] == 'Error':
            raise Http404
        opinion = service_response['content']
        self.check_object_permissions(request, opinion)

        opinion_serializer = OpinionRequestSerializer(
            opinion,
            data=request.data,
        )
        opinion_serializer.is_valid(raise_exception=True)

        service_response = OpinionService.update_opinion(pk, opinion_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        response_opinion_serializer = OpinionResponseSerializer(service_response['content'])
        return Response(
            response_opinion_serializer.data,
            status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        service_response = OpinionService.get_opinion(pk)
        if service_response['status'] == 'Error':
            raise Http404
        opinion = service_response['content']
        self.check_object_permissions(request, opinion)

        opinion_serializer = OpinionRequestSerializer(
            opinion,
            data=request.data,
            partial=True,
        )
        opinion_serializer.is_valid(raise_exception=True)

        service_response = OpinionService.update_opinion(pk, opinion_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        response_opinion_serializer = OpinionResponseSerializer(service_response['content'])
        return Response(
            response_opinion_serializer.data,
            status.HTTP_201_CREATED,
        )

    def destroy(self, request, pk=None):
        service_response = OpinionService.get_opinion(pk)
        if service_response['status'] == 'Error':
            raise Http404
        opinion = service_response['content']
        self.check_object_permissions(request, opinion)

        service_response = OpinionService.delete_opinion(pk)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {'message': _('Opinion has been deleted')},
            status.HTTP_204_NO_CONTENT,
        )
