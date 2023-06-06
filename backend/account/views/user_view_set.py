from django.http import Http404
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.viewsets import ViewSet

from account.models import User
from account.permissions import PostAnonElseStaffOrUserPermissions
from account.serializers import UserRegistrationSerializer, UserRequestSerializer, UserResponseSerializer
from account.services import UserService, MailService


class UserViewSet(ViewSet):
    permission_classes = [PostAnonElseStaffOrUserPermissions]

    @staticmethod
    def list(request):
        filters = {}
        filters_errors = {}
        params = {k: v[0] for k, v in dict(request.query_params).items()}
        order_by = params.pop('order_by', 'id')

        if not User.field_exists(order_by):
            filters_errors['order_by'] = _('Invalid field name')

        for k, v in params.items():
            field_name = k if '__' not in k else k.split('__')[0]
            if User.field_exists(field_name):
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

        service_response = UserService.get_users(
            filters=filters,
            order_by=order_by,
        )
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        users_list_serializer = UserResponseSerializer(service_response['content'], many=True)
        return Response(users_list_serializer.data)

    @staticmethod
    def create(request):
        user_serializer = UserRegistrationSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)

        service_response = UserService.create_user(user_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        created_user = service_response['content']
        service_response = MailService.send_email_verification_mail(created_user)

        if service_response['status'] == 'Error':
            UserService.delete_user(created_user.id)
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        response_user_serializer = UserResponseSerializer(created_user)

        return Response(
            response_user_serializer.data,
            status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None):
        service_response = UserService.get_user(pk)
        if service_response['status'] == 'Error':
            raise Http404
        user = service_response['content']
        self.check_object_permissions(request, user)

        response_user_serializer = UserResponseSerializer(user)
        return Response(response_user_serializer.data)

    def update(self, request, pk=None):
        service_response = UserService.get_user(pk)
        if service_response['status'] == 'Error':
            raise Http404
        user = service_response['content']
        self.check_object_permissions(request, user)

        user_serializer = UserRequestSerializer(
            user,
            data=request.data,
        )
        user_serializer.is_valid(raise_exception=True)

        service_response = UserService.update_user(pk, user_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        response_user_serializer = UserResponseSerializer(service_response['content'])

        return Response(
            response_user_serializer.data,
            status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        service_response = UserService.get_user(pk)
        if service_response['status'] == 'Error':
            raise Http404
        user = service_response['content']
        self.check_object_permissions(request, user)

        user_serializer = UserRequestSerializer(
            user,
            data=request.data,
            partial=True,
        )
        user_serializer.is_valid(raise_exception=True)

        service_response = UserService.update_user(pk, user_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        response_user_serializer = UserResponseSerializer(service_response['content'])

        return Response(
            response_user_serializer.data,
            status.HTTP_201_CREATED,
        )

    def destroy(self, request, pk=None):
        service_response = UserService.get_user(pk)
        if service_response['status'] == 'Error':
            raise Http404
        user = service_response['content']
        self.check_object_permissions(request, user)

        service_response = UserService.delete_user(pk)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {'message': _('User has been deleted')},
            status.HTTP_204_NO_CONTENT,
        )
