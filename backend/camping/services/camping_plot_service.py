from datetime import date
from typing import Any, Dict, Optional

from django.db.models import Q as Query
from django.utils.translation import gettext as _
from rest_framework.utils import json

from camping.models import CampingPlot, Reservation, Payment, CampingSection


class CampingPlotService:

    @staticmethod
    def is_booking_from_date_correct(date_from: date) -> bool:
        return date_from >= date.today()

    @staticmethod
    def is_booking_period_correct(date_from: date, date_to: date) -> bool:
        return date_from < date_to

    @staticmethod
    def is_camping_plot_in_incoming_reservations(camping_plot: CampingPlot) -> bool:
        return Reservation.objects.filter(camping_plot=camping_plot, date_to__gte=date.today()).exists()

    @staticmethod
    def position_exists_in_section(position, camping_section: CampingSection):
        return CampingPlot.objects.filter(position=position, camping_section=camping_section).exists()

    @staticmethod
    def get_available_camping_plots(date_from: date, date_to: date) -> Dict[str, Any]:
        try:
            errors = {}

            if not CampingPlotService.is_booking_from_date_correct(date_from):
                errors['date_from'] = _('Unable to create reservation for date in past tense')

            if not CampingPlotService.is_booking_period_correct(date_from, date_to):
                errors['date_to'] = _(
                    (
                        "The date of the end of the reservation can't occur before " +
                        "the date of the beginning of the reservation"
                    ),
                )

            if errors:
                raise Exception(json.dumps(errors))

            reserved_camping_plots = Reservation.objects.filter(
                Query(date_from__lt=date_to, date_to__gt=date_from),
                ~Query(payment__status=Payment.Status.CANCELED),
            ).values_list('camping_plot', flat=True)

            camping_plots = CampingPlot.objects.exclude(pk__in=reserved_camping_plots)

            response = {'status': 'Success', 'content': camping_plots}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response

    @staticmethod
    def get_camping_plots(
        order_by: str = 'id',
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        try:
            if filters:
                camping_plots = CampingPlot.objects.filter(**filters).order_by(order_by)
            else:
                camping_plots = CampingPlot.objects.all().order_by(order_by)
            response = {'status': 'Success', 'content': camping_plots}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response

    @staticmethod
    def get_camping_plot(pk: int) -> Dict[str, Any]:
        try:
            camping_plot = CampingPlot.objects.get(pk=pk)
            response = {'status': 'Success', 'content': camping_plot}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response

    @staticmethod
    def create_camping_plot(camping_plot_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            errors = {}

            if CampingPlotService.position_exists_in_section(
                camping_plot_data['position'],
                camping_plot_data['camping_section'],
            ):
                errors['position'] = _('Given position already exists in this camping section')

            if errors:
                raise Exception(json.dumps(errors))

            camping_plot = CampingPlot.objects.create(**camping_plot_data)
            response = {'status': 'Success', 'content': camping_plot}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response

    @staticmethod
    def update_camping_plot(pk: int, camping_plot_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if camping_plot_data:
                errors = {}
                camping_plot = CampingPlot.objects.get(pk=pk)

                if (
                    camping_plot_data.get('position') or
                    camping_plot_data.get('camping_section')
                ) and CampingPlotService.position_exists_in_section(
                    camping_plot_data.get('position', camping_plot.position),
                    camping_plot_data.get('camping_section', camping_plot.camping_section),
                ):
                    errors['position'] = _('Given position already exists in this camping section')

                if errors:
                    raise Exception(json.dumps(errors))

                CampingPlot.objects.filter(pk=pk).update(**camping_plot_data)
            camping_plot = CampingPlot.objects.get(pk=pk)
            response = {'status': 'Success', 'content': camping_plot}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response

    @staticmethod
    def delete_camping_plot(pk: int) -> Dict[str, Any]:
        try:
            errors = {}
            camping_plot = CampingPlot.objects.get(pk=pk)

            if CampingPlotService.is_camping_plot_in_incoming_reservations(camping_plot):
                errors['camping_plot'] = _("Camping plot is used in reservations")
            
            if errors:
                raise Exception(json.dumps(errors))

            camping_plot.delete()
            response = {'status': 'Success'}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response
