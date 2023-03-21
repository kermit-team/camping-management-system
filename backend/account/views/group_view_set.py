from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ViewSet

from account.serializers import GroupSerializer
from account.services import GroupService


class GroupViewSet(ViewSet):

    group_service = GroupService()
    permission_classes = [IsAdminUser]

    def list(self, request):
        queryset_of_groups = self.group_service.get_groups()
        serializer_context = {
            'request': request,
        }

        groups_list_serializer = GroupSerializer(
            queryset_of_groups, 
            many = True,
            context = serializer_context,
        )

        return Response(
            groups_list_serializer.data, 
            status = status.HTTP_200_OK,
        )

    def create(self, request):
        group_serializer = GroupSerializer(data=request.data)
        group_serializer.is_valid(raise_exception=True)
        serializer_context = {
            'request': request,
        }

        created_group = self.group_service.create_group(group_serializer.validated_data)
        response_group_serializer = GroupSerializer(
            created_group,
            context = serializer_context,
        )

        return Response(
            response_group_serializer.data,
            status = status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None):
        group = self.group_service.get_group(pk)
        if not group:
            raise Http404
        self.check_object_permissions(self.request, group)
        serializer_context = {
            'request': request,
        }

        response_group_serializer = GroupSerializer(
            group,
            context = serializer_context,
        )

        return Response(
            response_group_serializer.data,
            status = status.HTTP_200_OK,
        )

    def update(self, request, pk=None):
        group = self.group_service.get_group(pk)
        if not group:
            raise Http404
        self.check_object_permissions(self.request, group)
        serializer_context = {
            'request': request,
        }
        
        group_serializer = GroupSerializer(
            group, 
            data = request.data,
        )
        group_serializer.is_valid(raise_exception=True)

        updated_group = self.group_service.update_group(group_serializer.validated_data, pk)
        response_group_serializer = GroupSerializer(
            updated_group,
            context = serializer_context,
        )

        return Response(
            response_group_serializer.data,
            status = status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        group = self.group_service.get_group(pk)
        if not group:
            raise Http404
        self.check_object_permissions(self.request, group)
        serializer_context = {
            'request': request,
        }
        
        group_serializer = GroupSerializer(
            group, 
            data = request.data,
            partial = True,
        )
        group_serializer.is_valid(raise_exception=True)

        updated_group = self.group_service.update_group(group_serializer.validated_data, pk)
        response_group_serializer = GroupSerializer(
            updated_group,
            context = serializer_context,
        )

        return Response(
            response_group_serializer.data,
            status = status.HTTP_201_CREATED,
        )
        
    def destroy(self, request, pk=None):
        group = self.group_service.get_group(pk)
        if not group:
            raise Http404
        self.check_object_permissions(self.request, group)

        if self.group_service.delete_group(pk):
            return Response(
                {
                    'Status': 'Group deleted'
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        