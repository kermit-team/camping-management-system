from django.utils.http import urlsafe_base64_decode

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from account.token_generators import EmailVerificationTokenGenerator
from account.services import UserService


class EmailVerificationView(APIView):
    
    permission_classes = [AllowAny]

    def get(self, request, uidb64=None, token=None):
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserService.get_user(pk=uid)
        token_generator = EmailVerificationTokenGenerator()        
        
        if not user:
            return Response (
                {'message': 'Nieprawidłowy link'},
                status.HTTP_400_BAD_REQUEST,
            ) 
            
        if user.is_active or not token_generator.check_token(user, token):
            return Response (
                {'message': 'Link stracił ważność'},
                status.HTTP_401_UNAUTHORIZED,
            )

        UserService.update_user(uid, {'is_active': True})

        return Response()