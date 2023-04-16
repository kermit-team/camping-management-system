from django.utils.http import urlsafe_base64_decode

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.services import UserService
from account.serializers import UserRequestSerializer

class PasswordResetConfirmView(APIView):
    
    permission_classes = [AllowAny]

    def post(self, request, uidb64=None, token=None):
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserService.get_user(pk=uid)
        token_generator = PasswordResetTokenGenerator()
        password = request.data.get('password')
            
        if not (user and user.is_active):
            return Response (
                {'message': 'Nieprawidłowy link'},
                status.HTTP_400_BAD_REQUEST,
            ) 
        if not token_generator.check_token(user, token):
            return Response (
                {'message': 'Link stracił ważność'},
                status.HTTP_401_UNAUTHORIZED,
            )

        user_data = {
            'password': password,
        }
        user_serializer = UserRequestSerializer(
            user, 
            data = user_data,
            partial = True,
        )
        user_serializer.is_valid(raise_exception=True)
        if UserService.update_user(uid, user_serializer.validated_data):
            return Response(
                {'message': 'Reset hasła zakończony pomyślnie'},
                status.HTTP_201_CREATED,
            )
