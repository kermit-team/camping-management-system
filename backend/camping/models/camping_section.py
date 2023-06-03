from django.db import models


class CampingSection(models.Model):
    name = models.CharField(max_length=5)
    plot_price = models.DecimalField(max_digits=6, decimal_places=2)
    price_per_adult = models.DecimalField(max_digits=5, decimal_places=2)
    price_per_child = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
