from django.http import Http404
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from account.models import User
from account.serializers import UserRegistrationSerializer, UserRequestSerializer, UserResponseSerializer
from account.services import UserService, MailService
from account.permissions import PostAnonElseStaffOrUserPermissions


class UserViewSet(ViewSet):

    permission_classes = [PostAnonElseStaffOrUserPermissions]

    def list(self, request):
        filters = {}        
        filters_errors = {}
        params = {k: v[0] for k, v in dict(request.query_params).items()}
        order_by = params.pop('order_by', 'id')
        
        if not User.field_exists(order_by):
            filters_errors['order_by'] = _('Invalid field name')
        
        for k, v in params.items():
            if User.field_exists(k) if '__' not in k else User.field_exists(k.split('__')[0]):
                filters[k] = [int(string) if string.isdigit() else string.strip() for string in v.split(',')] if ('__in' in k or k[-1] == 's') else v
            else:
                filters_errors[k] = _('Field does not exist')
        
        if filters_errors:
            return Response (
                {'errors': filters_errors},
                status.HTTP_400_BAD_REQUEST,
            )  
        
        queryset_of_users = UserService.get_users(
            filters=filters, 
            order_by=order_by,
        )
        
        serializer_context = {
            'request': request,
        }

        users_list_serializer = UserResponseSerializer(
            queryset_of_users, 
            many = True,
            context = serializer_context,
        )

        return Response(users_list_serializer.data)

    def create(self, request):        
        user_data = request.data.copy()
        if 'groups' not in user_data:
            user_data['groups'] = list(Group.objects.filter(name='Klienci').values_list('id', flat=True))
        user_serializer = UserRegistrationSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)

        serializer_context = {
            'request': request,
        }

        created_user = UserService.create_user(user_serializer.validated_data)
        if created_user:
            
            MailService.send_email_verification_mail(created_user)        
            response_user_serializer = UserResponseSerializer(
                created_user,
                context = serializer_context,
            )

            return Response(
                response_user_serializer.data,
                status.HTTP_201_CREATED,
            )

    def retrieve(self, request, pk=None):
        user = UserService.get_user(pk)
        if not user:
            raise Http404
        self.check_object_permissions(self.request, user)
        serializer_context = {
            'request': request,
        }

        response_user_serializer = UserResponseSerializer(
            user,
            context = serializer_context,
        )

        return Response(response_user_serializer.data)

    def update(self, request, pk=None):
        user = UserService.get_user(pk)
        if not user:
            raise Http404
        self.check_object_permissions(self.request, user)
        serializer_context = {
            'request': request,
        }
        
        user_serializer = UserRequestSerializer(
            user, 
            data = request.data,
        )
        user_serializer.is_valid(raise_exception=True)

        updated_user = UserService.update_user(pk, user_serializer.validated_data)
        response_user_serializer = UserResponseSerializer(
            updated_user,
            context = serializer_context,
        )

        return Response(
            response_user_serializer.data,
            status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        user = UserService.get_user(pk)
        if not user:
            raise Http404
        self.check_object_permissions(self.request, user)
        serializer_context = {
            'request': request,
        }        

        user_serializer = UserRequestSerializer(
            user, 
            data = request.data,
            partial = True,
        )
        user_serializer.is_valid(raise_exception=True)

        updated_user = UserService.update_user(pk, user_serializer.validated_data)
        response_user_serializer = UserResponseSerializer(
            updated_user,
            context = serializer_context,
        )

        return Response(
            response_user_serializer.data,
            status.HTTP_201_CREATED,
        )
        
    def destroy(self, request, pk=None):
        user = UserService.get_user(pk)
        if not user:
            raise Http404
        self.check_object_permissions(self.request, user)

        if UserService.delete_user(pk):
            return Response(
                {'message': _('User has been deleted')},
                status.HTTP_204_NO_CONTENT,
            )
        