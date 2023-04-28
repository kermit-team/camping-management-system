from django.http import Http404
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from account.serializers import UserRegistrationSerializer, UserRequestSerializer, UserResponseSerializer
from account.services import UserService, MailService
from account.permissions import PostAnonElseStaffOrUserPermissions


class UserViewSet(ViewSet):

    permission_classes = [PostAnonElseStaffOrUserPermissions]

    def list(self, request):
        
        filters = {
            k: (v.split(',') if '__in' in k else v) 
            for k,v in request.query_params.items()
        }
        order_by = filters.pop('order_by', 'id')
        
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
        if 'groups' not in request.data:
            request.data['groups'] = list(Group.objects.filter(name='Klienci').values_list('id', flat=True))
        
        user_serializer = UserRegistrationSerializer(data=request.data)
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
        