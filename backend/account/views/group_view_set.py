from django.contrib.auth.models import Group
from django.http import Http404
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.viewsets import ViewSet

from account.serializers import GroupRequestSerializer, GroupResponseSerializer
from account.services import GroupService


class GroupViewSet(ViewSet):
    permission_classes = [IsAdminUser]

    @staticmethod
    def list(request):
        filters = {}
        filters_errors = {}
        params = {k: v[0] for k, v in dict(request.query_params).items()}
        order_by = params.pop('order_by', 'id')

        if not Group.field_exists(order_by):
            filters_errors['order_by'] = _('Invalid field name')

        for k, v in params.items():
            field_name = k if '__' not in k else k.split('__')[0]
            if Group.field_exists(field_name):
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

        service_response = GroupService.get_groups(
            filters=filters,
            order_by=order_by,
        )

        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        groups_list_serializer = GroupResponseSerializer(service_response['content'], many=True)
        return Response(groups_list_serializer.data)

    @staticmethod
    def create(request):
        group_serializer = GroupRequestSerializer(data=request.data)
        group_serializer.is_valid(raise_exception=True)

        service_response = GroupService.create_group(group_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        response_group_serializer = GroupResponseSerializer(service_response['content'])
        return Response(
            response_group_serializer.data,
            status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None):
        service_response = GroupService.get_group(pk)
        if service_response['status'] == 'Error':
            raise Http404
        group = service_response['content']
        self.check_object_permissions(request, group)

        response_group_serializer = GroupResponseSerializer(group)
        return Response(response_group_serializer.data)

    def update(self, request, pk=None):
        service_response = GroupService.get_group(pk)
        if service_response['status'] == 'Error':
            raise Http404
        group = service_response['content']
        self.check_object_permissions(request, group)

        group_serializer = GroupRequestSerializer(
            group,
            data=request.data,
        )
        group_serializer.is_valid(raise_exception=True)

        service_response = GroupService.update_group(pk, group_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        response_group_serializer = GroupResponseSerializer(service_response['content'])

        return Response(
            response_group_serializer.data,
            status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        service_response = GroupService.get_group(pk)
        if service_response['status'] == 'Error':
            raise Http404
        group = service_response['content']
        self.check_object_permissions(request, group)

        group_serializer = GroupRequestSerializer(
            group,
            data=request.data,
            partial=True,
        )
        group_serializer.is_valid(raise_exception=True)

        service_response = GroupService.update_group(pk, group_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        response_group_serializer = GroupResponseSerializer(service_response['content'])

        return Response(
            response_group_serializer.data,
            status.HTTP_201_CREATED,
        )

    def destroy(self, request, pk=None):
        service_response = GroupService.get_group(pk)
        if service_response['status'] == 'Error':
            raise Http404
        group = service_response['content']
        self.check_object_permissions(request, group)

        service_response = GroupService.delete_group(pk)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(
            {'message': _('Group has been deleted')},
            status.HTTP_204_NO_CONTENT,
        )
