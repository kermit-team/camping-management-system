from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from account.services import UserService
from account.token_generators import EmailVerificationTokenGenerator


class EmailVerificationView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request, uidb64=None, token=None):
        uid = urlsafe_base64_decode(uidb64).decode()
        service_response = UserService.get_user(pk=uid)
        token_generator = EmailVerificationTokenGenerator()
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_400_BAD_REQUEST,
            )

        user = service_response['content']
        if not user:
            return Response(
                _('Invalid link'),
                status.HTTP_400_BAD_REQUEST,
            )

        if user.is_active or not token_generator.check_token(user, token):
            return Response(
                _('Link is no longer valid'),
                status.HTTP_401_UNAUTHORIZED,
            )

        service_response = UserService.update_user(uid, {'is_active': True})
        if service_response['status'] == 'Error':
            return Response(
                json.loads(service_response['errors']),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({'message': _('E-mail has been successfully verified')})
