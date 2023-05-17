from typing import Any, Dict, List, Optional, Union

from django.db.models import QuerySet
from django.db.utils import IntegrityError
from django.core.exceptions import FieldError, FieldDoesNotExist

from camping.models import CampingPlot


class CampingPlotService:

    @staticmethod
    def get_camping_plots(
        order_by: str = 'id',
        filters: Optional[Dict[str, Any]] = None) -> Optional[Union[QuerySet, List[CampingPlot]]]:
        try:
            if filters:
                camping_plots = CampingPlot.objects.filter(**filters).order_by(order_by)
            else:
                camping_plots = CampingPlot.objects.all().order_by(order_by)
            return camping_plots
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None
            
    @staticmethod
    def get_camping_plot(pk: int) -> Optional[CampingPlot]:
        try:
            camping_plot = CampingPlot.objects.get(pk=pk)
            return camping_plot
        except CampingPlot.DoesNotExist:
            return None
    
    @staticmethod
    def create_camping_plot(camping_plot_data: Dict[str, Any]) -> Optional[CampingPlot]:
        try:
            camping_plot = CampingPlot.objects.create_camping_plot(**camping_plot_data)
                    
            return camping_plot
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None
        except IntegrityError:
            return None

    @staticmethod
    def update_camping_plot(pk: int, camping_plot_data: Dict[str, Any]) -> Optional[CampingPlot]:
        try:
            if camping_plot_data:                    
                CampingPlot.objects.filter(pk=pk).update(**camping_plot_data)
                camping_plot = CampingPlot.objects.get(pk=pk)
                return camping_plot
            
        except CampingPlot.DoesNotExist:
            return None
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None


    @staticmethod
    def delete_camping_plot(pk:int) -> bool:
        try:
            camping_plot = CampingPlot.objects.get(pk=pk)
            camping_plot.delete()
            return True
        except CampingPlot.DoesNotExist:
            return False
        