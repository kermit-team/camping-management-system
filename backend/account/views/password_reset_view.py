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
            
            return Response({'message': 'Wiadomość została wysłana'})
        
        return Response(
            {'message': 'Nie znaleziono użytkownika o podanym adresie e-mail.'},
            status.HTTP_400_BAD_REQUEST,
        )
