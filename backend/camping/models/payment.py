from django.db import models
from django.utils.translation import gettext as _

from .reservation import Reservation


class Payment(models.Model):

    class Method(models.TextChoices):
        PAYPAL = _('Paypal')
        PAYU = _('PayU')
        BLIK = _('BLIK')
        CREDIT_CARD = _('Credit card')
        TRADITIONAL_TRANSFER = _('Traditional transfer')

    class Status(models.TextChoices):
        WAITING_FOR_PAYMENT = _('Waiting for payment')
        IN_PROGRESS = _('In progress')
        CANCELED = _('Canceled')
        APPROVED = _('Approved')
    
    method = models.CharField(max_length=25, choices=Method.choices)
    status = models.CharField(max_length=25, choices=Status.choices, default=Status.WAITING_FOR_PAYMENT)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    reservation = models.ForeignKey(Reservation, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.price} - {self.status}'