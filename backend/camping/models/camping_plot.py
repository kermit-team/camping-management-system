from django.db import models

from .camping_section import CampingSection


class CampingPlot(models.Model):
    position = models.CharField(max_length=5)
    camping_section = models.ForeignKey(CampingSection, on_delete=models.CASCADE)

    def __str__(self):
        return self.camping_section.name + self.position
