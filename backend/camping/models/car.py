from django.db import models


class Car(models.Model):

    registration_plate = models.CharField(max_length=25)

    def __str__(self):
        return self.registration_plate