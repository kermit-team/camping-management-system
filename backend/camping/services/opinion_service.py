from typing import Any, Dict, List, Optional, Union

from django.db.models import QuerySet
from django.db.utils import IntegrityError
from django.core.exceptions import FieldError, FieldDoesNotExist

from camping.models import Opinion


class OpinionService:

    @staticmethod
    def get_opinions(
        order_by: str = 'id',
        filters: Optional[Dict[str, Any]] = None) -> Optional[Union[QuerySet, List[Opinion]]]:
        try:
            if filters:
                opinions = Opinion.objects.filter(**filters).order_by(order_by)
            else:
                opinions = Opinion.objects.all().order_by(order_by)
            return opinions
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None
            
    @staticmethod
    def get_opinion(pk: int) -> Optional[Opinion]:
        try:
            opinion = Opinion.objects.get(pk=pk)
            return opinion
        except Opinion.DoesNotExist:
            return None
    
    @staticmethod
    def create_opinion(opinion_data: Dict[str, Any]) -> Optional[Opinion]:
        try:
            opinion = Opinion.objects.create_opinion(**opinion_data)
                    
            return opinion
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None
        except IntegrityError:
            return None

    @staticmethod
    def update_opinion(pk: int, opinion_data: Dict[str, Any]) -> Optional[Opinion]:
        try:
            if opinion_data:                    
                Opinion.objects.filter(pk=pk).update(**opinion_data)
                opinion = Opinion.objects.get(pk=pk)
                return opinion
            
        except Opinion.DoesNotExist:
            return None
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None


    @staticmethod
    def delete_opinion(pk:int) -> bool:
        try:
            opinion = Opinion.objects.get(pk=pk)
            opinion.delete()
            return True
        except Opinion.DoesNotExist:
            return False
        