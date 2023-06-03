from django.db import models
from django.utils.translation import gettext as _

from .reservation import Reservation


class Payment(models.Model):
    class Method(models.TextChoices):
        PAYPAL = "PAYPAL", _('Paypal')
        PAYU = "PAYU", _('PayU')
        BLIK = "BLIK", _('BLIK')
        CREDIT_CARD = "CC", _('Credit card')
        TRADITIONAL_TRANSFER = "TT", _('Traditional transfer')

    class Status(models.TextChoices):
        WAITING_FOR_PAYMENT = "WFP", _('Waiting for payment')
        IN_PROGRESS = "IP", _('In progress')
        CANCELED = "C", _('Canceled')
        APPROVED = "A", _('Approved')
        RETURNED = "R", _('Returned')

    method = models.CharField(max_length=10, choices=Method.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.WAITING_FOR_PAYMENT)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    reservation = models.ForeignKey(Reservation, related_name='payment', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.price} - {self.status}'
