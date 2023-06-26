from django.db import models
from django.utils.translation import gettext as _

from account.models.user import User
from .camping_plot import CampingPlot


class Opinion(models.Model):
    class Rating(models.IntegerChoices):
        BAD = 1, _('Bad')
        DECENT = 2, _('Decent')
        OK = 3, _('Ok')
        GREAT = 4, _('Great')
        AWESOME = 5, _('Awesome')

    rating = models.IntegerField(choices=Rating.choices)
    description = models.CharField(default='', blank=True, max_length=500)
    author = models.ForeignKey(User, on_delete=models.RESTRICT)
    camping_plot = models.ForeignKey(CampingPlot, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.author.first_name} {self.author.last_name} - {self.description}'
