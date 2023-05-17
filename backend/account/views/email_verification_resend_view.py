from django.utils.translation import gettext as _

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from account.services import UserService, MailService


class EmailVerificationResendView(APIView):
    
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = UserService.get_users(filters={'email': email}).first()

        if not user:
            return Response(
                {'message': _('The user with the specified email address was not found')},
                status.HTTP_400_BAD_REQUEST,
            )
        
        if user.is_active:
            return Response(
                {'message': _('The user with the specified email address was already verified')},
                status.HTTP_400_BAD_REQUEST,
            )
            
        MailService.send_password_reset_mail(user)
        return Response({'message': _('The message has been sent')})
        
        
