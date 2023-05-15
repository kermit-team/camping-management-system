from django.utils.translation import gettext as _

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from account.services import UserService, MailService

class PasswordResetView(APIView):
    
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = UserService.get_users(filters={'email': email}).first()

        if user:
            MailService.send_password_reset_mail(user)
            
            return Response({'message': _('The message has been sent')})
        
        return Response(
            {'message': _('The user with the specified email address was not found')},
            status.HTTP_400_BAD_REQUEST,
        )
