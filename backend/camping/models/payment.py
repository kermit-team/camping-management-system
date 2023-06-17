from django.db import models
from django.utils.translation import gettext as _


class Payment(models.Model):
    class Status(models.TextChoices):
        WAITING_FOR_PAYMENT = "WFP", _('Waiting for payment')
        CANCELED = "C", _('Canceled')
        UNPAID = "UP", _('Unpaid')
        PAID = "P", _('Paid')
        RETURNED = "R", _('Returned')

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.WAITING_FOR_PAYMENT)
    stripe_checkout_id = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.price} - {self.status}'
