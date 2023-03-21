from django.http import Http404
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from account.serializers import UserRegistrationSerializer, UserRequestSerializer, UserResponseSerializer, GroupSerializer
from account.services import UserService
from account.permissions import PostAnonElseStaffOrUserPermissions


class UserViewSet(ViewSet):

    user_service = UserService()
    permission_classes = [PostAnonElseStaffOrUserPermissions]

    def list(self, request):
        queryset_of_users = self.user_service.get_users()
        serializer_context = {
            'request': request,
        }

        users_list_serializer = UserResponseSerializer(
            queryset_of_users, 
            many = True,
            context = serializer_context,
        )

        return Response(
            users_list_serializer.data, 
            status = status.HTTP_200_OK,
        )

    def create(self, request):

        if 'groups' not in request.data:
            request.data['groups'] = list(Group.objects.filter(name='Uczniowie').values_list('id', flat=True))
        
        user_serializer = UserRegistrationSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)

        serializer_context = {
            'request': request,
        }

        created_user = self.user_service.create_user(user_serializer.validated_data)
        response_user_serializer = UserResponseSerializer(
            created_user,
            context = serializer_context,
        )
        print(response_user_serializer.data)

        return Response(
            response_user_serializer.data,
            status = status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk=None):
        user = self.user_service.get_user(pk)
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

        return Response(
            response_user_serializer.data,
            status = status.HTTP_200_OK,
        )

    def update(self, request, pk=None):
        user = self.user_service.get_user(pk)
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

        updated_user = self.user_service.update_user(user_serializer.validated_data, pk)
        response_user_serializer = UserResponseSerializer(
            updated_user,
            context = serializer_context,
        )

        return Response(
            response_user_serializer.data,
            status = status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        user = self.user_service.get_user(pk)
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
        print(user_serializer.initial_data)
        user_serializer.is_valid(raise_exception=True)
        
        print(user_serializer.validated_data)

        updated_user = self.user_service.update_user(user_serializer.validated_data, pk)
        response_user_serializer = UserResponseSerializer(
            updated_user,
            context = serializer_context,
        )

        return Response(
            response_user_serializer.data,
            status = status.HTTP_201_CREATED,
        )
        
    def destroy(self, request, pk=None):
        user = self.user_service.get_user(pk)
        if not user:
            raise Http404
        self.check_object_permissions(self.request, user)

        if self.user_service.delete_user(pk):
            return Response(
                {
                    'Status': 'User deleted'
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        