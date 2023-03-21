from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from account.managers import UserManager


class User(AbstractUser):

    username = None
    email = models.EmailField(
        'E-mail', 
        max_length = 255, 
        unique = True,
    )
    first_name = models.CharField(
        max_length=150,
    )
    last_name = models.CharField(
        max_length=150,
    )
    phone_number = PhoneNumberField(
        null = True,
        blank = True,
        unique = True,
    )
    avatar = models.ImageField(
        default = 'avatar.png',
        upload_to = 'accounts_avatar',
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
    ]

    objects = UserManager()

    def __str__(self):
        return self.email
