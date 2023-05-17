from typing import Any, Dict, List, Optional, Union

from django.db.models import QuerySet
from django.db.utils import IntegrityError
from django.core.exceptions import FieldError, FieldDoesNotExist

from camping.models import CampingSection


class CampingSectionService:

    @staticmethod
    def get_camping_sections(
        order_by: str = 'id',
        filters: Optional[Dict[str, Any]] = None) -> Optional[Union[QuerySet, List[CampingSection]]]:
        try:
            if filters:
                camping_sections = CampingSection.objects.filter(**filters).order_by(order_by)
            else:
                camping_sections = CampingSection.objects.all().order_by(order_by)
            return camping_sections
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None
            
    @staticmethod
    def get_camping_section(pk: int) -> Optional[CampingSection]:
        try:
            camping_section = CampingSection.objects.get(pk=pk)
            return camping_section
        except CampingSection.DoesNotExist:
            return None
    
    @staticmethod
    def create_camping_section(camping_section_data: Dict[str, Any]) -> Optional[CampingSection]:
        try:
            camping_section = CampingSection.objects.create_camping_section(**camping_section_data)
                    
            return camping_section
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None
        except IntegrityError:
            return None

    @staticmethod
    def update_camping_section(pk: int, camping_section_data: Dict[str, Any]) -> Optional[CampingSection]:
        try:
            if camping_section_data:                    
                CampingSection.objects.filter(pk=pk).update(**camping_section_data)
                camping_section = CampingSection.objects.get(pk=pk)
                return camping_section
            
        except CampingSection.DoesNotExist:
            return None
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None


    @staticmethod
    def delete_camping_section(pk:int) -> bool:
        try:
            camping_section = CampingSection.objects.get(pk=pk)
            camping_section.delete()
            return True
        except CampingSection.DoesNotExist:
            return False
        