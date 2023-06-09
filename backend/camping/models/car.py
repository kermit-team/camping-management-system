from django.db import models

from account.models import User


class Car(models.Model):
    registration_plate = models.CharField(unique=True, max_length=25)
    drivers = models.ManyToManyField(User, related_name='cars')

    def __str__(self):
        return self.registration_plate
