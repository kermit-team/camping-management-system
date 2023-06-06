from datetime import date
from typing import Any, Dict, Optional

from django.utils.translation import gettext as _
from rest_framework.utils import json

from camping.models import CampingPlot, Reservation


class CampingPlotService:

    @staticmethod
    def is_camping_plot_reserved(camping_plot: CampingPlot) -> bool:
        return Reservation.objects.filter(camping_plot=camping_plot, date_to__gte=date.today).exists()

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
            camping_plot = CampingPlot.objects.create(**camping_plot_data)
            response = {'status': 'Success', 'content': camping_plot}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response

    @staticmethod
    def update_camping_plot(pk: int, camping_plot_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if camping_plot_data:
                CampingPlot.objects.filter(pk=pk).update(**camping_plot_data)
            camping_plot = CampingPlot.objects.get(pk=pk)
            response = {'status': 'Success', 'content': camping_plot}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response

    @staticmethod
    def delete_camping_plot(pk: int) -> Dict[str, Any]:
        try:
            camping_plot = CampingPlot.objects.get(pk=pk)
            if CampingPlotService.is_camping_plot_reserved(camping_plot):
                raise Exception(json.dumps(
                    {'camping_plot': _("Camping plot is used in reservations")},
                ))

            camping_plot.delete()
            response = {'status': 'Success'}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response
