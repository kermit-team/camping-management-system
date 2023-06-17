from datetime import date
from typing import Any, Dict, Optional

from django.db.models import Q as Query
from django.utils.translation import gettext as _
from rest_framework.utils import json

from account.models import User
from camping.models import Reservation, Payment, CampingPlot, Car
from camping.services import PaymentService


class ReservationService:

    @staticmethod
    def is_reservation_cancelable(reservation: Reservation) -> bool:
        delta = date.today() - reservation.date_from
        return delta.days >= 7

    @staticmethod
    def is_number_of_people_correct(number_of_adults: int, number_of_children: int) -> bool:
        return number_of_adults > 0 and (number_of_adults + number_of_children <= 10)

    @staticmethod
    def is_user_capable_of_booking(user: User, car: Car) -> bool:
        return user.id_card and user.cars.filter(registration_plate=car.registration_plate)

    @staticmethod
    def is_booking_from_date_correct(date_from: date) -> bool:
        return date_from >= date.today()

    @staticmethod
    def is_booking_period_correct(date_from: date, date_to: date) -> bool:
        return date_from < date_to

    @staticmethod
    def is_reservation_updatable(reservation: Reservation) -> bool:
        return reservation.payment.status == Payment.Status.WAITING_FOR_PAYMENT

    @staticmethod
    def is_camping_plot_available(camping_plot: CampingPlot, date_from: date, date_to: date) -> bool:
        return not Reservation.objects.filter(
            Query(date_from__lt=date_to, date_to__gt=date_from),
            ~Query(payment__status=Payment.Status.CANCELED),
            camping_plot=camping_plot,
        ).exists()

    @staticmethod
    def calculate_reservation_price(
        plot_price: float,
        price_per_adult: float,
        price_per_child: float,
        number_of_adults: int,
        number_of_children: int,
        days: int,
    ) -> float:
        return plot_price * days + price_per_adult * number_of_adults + price_per_child * number_of_children

    @staticmethod
    def get_reservations(
        order_by: str = 'id',
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        try:
            if filters:
                reservations = Reservation.objects.filter(**filters).order_by(order_by)
            else:
                reservations = Reservation.objects.all().order_by(order_by)
            response = {'status': 'Success', 'content': reservations}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response

    @staticmethod
    def get_reservation(pk: int) -> Dict[str, Any]:
        try:
            reservation = Reservation.objects.get(pk)
            response = {'status': 'Success', 'content': reservation}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response

    @staticmethod
    def create_reservation(reservation_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            errors = {}

            if not ReservationService.is_user_capable_of_booking(reservation_data['user'], reservation_data['car']):
                errors['user'] = _('User needs to have an assigned car and id card in order to make reservation')

            if not ReservationService.is_number_of_people_correct(
                reservation_data['number_of_adults'],
                reservation_data['number_of_children'],
            ):
                errors['number_of_people'] = _(
                    (
                        'A maximum of 10 people (not including babies) can be given in one reservation. ' +
                        'There must be one adult present'
                    ),
                )

            if not ReservationService.is_booking_from_date_correct(reservation_data['date_from']):
                errors['date_from'] = _('Unable to create reservation for date in past tense')

            if not ReservationService.is_booking_period_correct(
                reservation_data['date_from'],
                reservation_data['date_to'],
            ):
                errors['date_to'] = _(
                    (
                        "The date of the end of the reservation can't occur before " +
                        "the date of the beginning of the reservation"
                    ),
                )

            if not ReservationService.is_camping_plot_available(
                reservation_data['camping_plot'],
                reservation_data['date_from'],
                reservation_data['date_to'],
            ):
                errors['camping_plot'] = _("This parcel isn't available on the specified date")

            if errors:
                raise Exception(json.dumps(errors))

            payment_data = {
                'price': ReservationService.calculate_reservation_price(
                    reservation_data['camping_plot'].camping_section.plot_price,
                    reservation_data['camping_plot'].camping_section.price_per_adult,
                    reservation_data['camping_plot'].camping_section.price_per_child,
                    reservation_data['number_of_adults'],
                    reservation_data['number_of_children'],
                    (reservation_data['date_to'] - reservation_data['date_from']).days,
                ),
                'email': reservation_data['user'].email,
                'date_from': reservation_data['date_from'],
                'date_to': reservation_data['date_to'],
                'camping_plot': reservation_data['camping_plot'],
                'number_of_adults': reservation_data['number_of_adults'],
                'number_of_children': reservation_data['number_of_children']
            }

            service_response = PaymentService.create_payment(payment_data)
            if service_response['status'] == 'Error':
                raise Exception(service_response['errors'])

            reservation_data['payment'] = service_response['content']['payment']
            reservation = Reservation.objects.create(**reservation_data)

            response = {
                'status': 'Success',
                'content': {
                    'reservation': reservation,
                    'checkout_url': service_response['content']['checkout_session']['url'],
                },
            }
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response

    @staticmethod
    def update_reservation(pk: int, reservation_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            checkout_url = None
            if reservation_data:
                reservation = Reservation.objects.get(pk)
                errors = {}

                if not ReservationService.is_reservation_updatable(reservation):
                    errors['payment_status'] = _(
                        (
                            'The reservation has already been paid for.' +
                            'In order to change your reservation, please contact our customer service'
                        ),
                    )

                if not ReservationService.is_user_capable_of_booking(
                    reservation.user,
                    reservation_data.get('car', reservation.car),
                ):
                    errors['user'] = _('User needs to have an assigned car and id card in order to make reservation')

                if (
                    reservation_data.get('number_of_adults') or
                    reservation_data.get('number_of_children')
                ) and not ReservationService.is_number_of_people_correct(
                    reservation_data.get('number_of_adults', reservation.number_of_adults),
                    reservation_data.get('number_of_children', reservation.number_of_children),
                ):
                    errors['number_of_people'] = _(
                        (
                            'A maximum of 10 people (not including babies) can be given in one reservation.' +
                            'There must be one adult present'
                        ),
                    )

                if (
                    reservation_data.get('camping_plot') or
                    reservation_data.get('date_from') or
                    reservation_data.get('date_to')
                ):
                    if not ReservationService.is_booking_from_date_correct(
                        reservation_data.get('date_from', reservation.date_from),
                    ):
                        errors['date_from'] = _('Unable to create reservation for date in past tense')

                    if not ReservationService.is_booking_period_correct(
                        reservation_data.get('date_from', reservation.date_from),
                        reservation_data.get('date_to', reservation.date_to),
                    ):
                        errors['date_to'] = _(
                            (
                                "The date of the end of the reservation can't occur before " +
                                "the date of the beginning of the reservation"
                            ),
                        )

                    if not ReservationService.is_camping_plot_available(
                        reservation_data.get('camping_plot', reservation.camping_plot),
                        reservation_data.get('date_from', reservation.date_from),
                        reservation_data.get('date_to', reservation.date_to),
                    ):
                        errors['camping_plot'] = _("This parcel isn't available on the specified date")

                if errors:
                    raise Exception(json.dumps(errors))

                old_reservation_data = reservation.__dict__
                Reservation.objects.filter(pk=pk).update(**reservation_data)
                reservation = Reservation.objects.get(pk=pk)

                payment_data = {
                    'price': ReservationService.calculate_reservation_price(
                        reservation.camping_plot.camping_section.plot_price,
                        reservation.camping_plot.camping_section.price_per_adult,
                        reservation.camping_plot.camping_section.price_per_child,
                        reservation.number_of_adults,
                        reservation.number_of_children,
                        (reservation.date_to - reservation.date_from).days,
                    ),
                    'email': reservation.user.email,
                    'date_from': reservation.date_from,
                    'date_to': reservation.date_to,
                    'camping_plot': reservation.camping_plot,
                    'number_of_adults': reservation.number_of_adults,
                    'number_of_children': reservation.number_of_children
                }
                service_response = PaymentService.update_payment(reservation.payment.id, payment_data)
                if service_response['status'] == 'Error':
                    Reservation.objects.filter(pk=pk).update(**old_reservation_data)
                    raise Exception(service_response['errors'])
                checkout_url = service_response['checkout_session']['url']

            reservation = Reservation.objects.get(pk=pk)
            response = {
                'status': 'Success',
                'content': {
                    'reservation': reservation,
                },
            }
            if checkout_url:
                response['content']['checkout_url'] = checkout_url

        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response

    @staticmethod
    def delete_reservation(pk: int) -> Dict[str, Any]:
        try:
            reservation = Reservation.objects.get(pk)
            if not ReservationService.is_reservation_cancelable(reservation):
                raise Exception(json.dumps(
                    {'reservation': _("Reservation can no longer be cancelled")},
                ))

            reservation.delete()
            response = {'status': 'Success'}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response
