from django.http import Http404
from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ViewSet

from django.contrib.auth.models import Group
from account.serializers import GroupRequestSerializer, GroupResponseSerializer
from account.services import GroupService


class GroupViewSet(ViewSet):

    permission_classes = [IsAdminUser]

    def list(self, request):
        
        filters = {}        
        filters_errors = {}
        params = {k: v[0] for k, v in dict(request.query_params).items()}
        order_by = params.pop('order_by', 'id')
        
        if not Group.field_exists(order_by):
            filters_errors['order_by'] = _('Invalid field name')
        
        for k, v in params.items():
            if Group.field_exists(k) if '__' not in k else Group.field_exists(k.split('__')[0]):
                filters[k] = [int(string) if string.isdigit() else string.strip() for string in v.split(',')] if (',' in v) else v
            else:
                filters_errors[k] = _('Field does not exist')
        
        if filters_errors:
            return Response (
                {'errors': filters_errors},
                status.HTTP_400_BAD_REQUEST,
            )  
        
        queryset_of_groups = GroupService.get_groups(
            filters=filters, 
            order_by=order_by,
        )
         
        serializer_context = {
            'request': request,
        }

        groups_list_serializer = GroupResponseSerializer(
            queryset_of_groups, 
            many = True,
            context = serializer_context,
        )

        return Response(groups_list_serializer.data)

    def create(self, request):
        group_serializer = GroupRequestSerializer(data=request.data)
        group_serializer.is_valid(raise_exception=True)
        serializer_context = {
            'request': request,
        }

        created_group = GroupService.create_group(group_serializer.validated_data)
        response_group_serializer = GroupResponseSerializer(
            created_group,
            context = serializer_context,
        )

        return Response(
            response_group_serializer.data,
            status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None):
        group = GroupService.get_group(pk)
        if not group:
            raise Http404
        self.check_object_permissions(self.request, group)
        serializer_context = {
            'request': request,
        }

        response_group_serializer = GroupResponseSerializer(
            group,
            context = serializer_context,
        )

        return Response(response_group_serializer.data)

    def update(self, request, pk=None):
        group = GroupService.get_group(pk)
        if not group:
            raise Http404
        self.check_object_permissions(self.request, group)
        serializer_context = {
            'request': request,
        }
        
        group_serializer = GroupRequestSerializer(
            group, 
            data = request.data,
        )
        group_serializer.is_valid(raise_exception=True)

        updated_group = GroupService.update_group(pk, group_serializer.validated_data)
        response_group_serializer = GroupResponseSerializer(
            updated_group,
            context = serializer_context,
        )

        return Response(
            response_group_serializer.data,
            status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        group = GroupService.get_group(pk)
        if not group:
            raise Http404
        self.check_object_permissions(self.request, group)
        serializer_context = {
            'request': request,
        }
        
        group_serializer = GroupRequestSerializer(
            group, 
            data = request.data,
            partial = True,
        )
        group_serializer.is_valid(raise_exception=True)

        updated_group = GroupService.update_group(pk, group_serializer.validated_data)
        response_group_serializer = GroupResponseSerializer(
            updated_group,
            context = serializer_context,
        )

        return Response(
            response_group_serializer.data,
            status.HTTP_201_CREATED,
        )
    
    def destroy(self, request, pk=None):
        group = GroupService.get_group(pk)
        if not group:
            raise Http404
        self.check_object_permissions(self.request, group)

        if GroupService.delete_group(pk):
            return Response(
                {'message': _('Group has been deleted')},
                status.HTTP_204_NO_CONTENT,
            )
        