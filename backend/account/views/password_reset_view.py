from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from account.services import UserService, MailService


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        email = request.data.get('email')
        service_response = UserService.get_users(filters={'email': email})
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        user = service_response['content'].first()
        if not user:
            return Response(
                _('The user with the specified email address was not found'),
                status.HTTP_400_BAD_REQUEST,
            )

        service_response = MailService.send_password_reset_mail(user)
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({'message': _('The message has been sent')})
