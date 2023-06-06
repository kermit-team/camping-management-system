from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from account.serializers import UserRequestSerializer
from account.services import UserService


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request, uidb64=None, token=None):
        uid = urlsafe_base64_decode(uidb64).decode()
        service_response = UserService.get_user(pk=uid)
        token_generator = PasswordResetTokenGenerator()
        password = request.data.get('password')

        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )
        user = service_response['content']

        if not (user and user.is_active):
            return Response(
                _('Invalid link'),
                status.HTTP_400_BAD_REQUEST,
            )
        if not token_generator.check_token(user, token):
            return Response(
                _('Link is no longer valid'),
                status.HTTP_401_UNAUTHORIZED,
            )

        user_serializer = UserRequestSerializer(
            user,
            data={'password': password},
            partial=True,
        )
        user_serializer.is_valid(raise_exception=True)

        service_response = UserService.update_user(uid, user_serializer.validated_data)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {'message': _('Password reset successfully completed')},
            status.HTTP_201_CREATED,
        )
