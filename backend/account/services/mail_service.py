from smtplib import SMTPException
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from account.token_generators import EmailVerificationTokenGenerator
from account.models.user import User

class MailService:

    @staticmethod
    def send_email_verification_mail(user: User):
        token_generator = EmailVerificationTokenGenerator()        
        token = token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        verification_url = f'email-verification/{uidb64}/{token}'
        
        context = {
            'name': user.first_name,
            'verification_url': verification_url,
        }
        html_message = render_to_string(
            template_name='account/email_verification_template.html', 
            context=context,
        )
        plain_message = strip_tags(html_message)
        
        try:
            send_mail(
                subject='Kemping Bajka - zweryfikuj swój adres e-mail', 
                message=plain_message,
                html_message=html_message,
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except SMTPException as e:
           print(e)

    @staticmethod
    def send_password_reset_mail(user: User):
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f'password-reset/confirm/{uidb64}/{token}'
        
        context = {
            'name': user.first_name,
            'reset_url': reset_url,
        }
        html_message = render_to_string(
            template_name='account/password_reset_template.html', 
            context=context,
        )
        plain_message = strip_tags(html_message)

        try:
            send_mail(
                subject='Kemping Bajka - zresetuj swoje hasło',  
                message=plain_message,
                html_message=html_message,
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except SMTPException as e:
            print(e)