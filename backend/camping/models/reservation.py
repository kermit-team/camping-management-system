from django.db import models
from django.utils.translation import gettext as _

from account.models.user import User
from .car import Car
from .camping_plot import CampingPlot


class Reservation(models.Model):

    date_from = models.DateField()
    date_to = models.DateField()
    number_of_adults = models.SmallIntegerField()
    number_of_children = models.SmallIntegerField()
    number_of_babies = models.SmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    car = models.ForeignKey(Car, on_delete=models.RESTRICT)
    camping_plot = models.ForeignKey(CampingPlot, on_delete=models.RESTRICT)

    def __str__(self):
        return _(f'{self.user.first_name} {self.user.first_name}, plot {self.camping_plot}, {self.date_from}-{self.date_from}')