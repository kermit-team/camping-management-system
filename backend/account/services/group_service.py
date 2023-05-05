from typing import Any, Dict, List, Optional, Union

from django.db.models import QuerySet
from django.db.utils import IntegrityError
from django.core.exceptions import FieldError, FieldDoesNotExist
from django.contrib.auth.models import Group


class GroupService:

    @staticmethod
    def get_groups(
        order_by: str = 'id',
        filters: Optional[Dict[str, Any]] = None) -> Union[QuerySet, List[Group]]:
        try:
            if filters:
                groups = Group.objects.filter(**filters).order_by(order_by)
            else:
                groups = Group.objects.all().order_by(order_by)
            return groups
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None

    @staticmethod
    def get_group(pk: int) -> Optional[Group]:
        try:
            group = Group.objects.get(pk=pk)
            return group
        except Group.DoesNotExist:
            return None

    @staticmethod
    def create_group(group_data: Dict[str, Any]) -> Optional[Group]:
        try:
            group = Group.objects.create(**group_data)
            return group
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None
        except IntegrityError:
            return None

    @staticmethod
    def update_group(pk: int, group_data: Dict[str, Any]) -> Optional[Group]:
        try:
            group = Group.objects.get(pk=pk)      
            
            if group_data:                    
                Group.objects.filter(pk=pk).update(**group_data)

            group = Group.objects.get(pk=pk)  
            return group
        except Group.DoesNotExist:
            return None
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None

    @staticmethod
    def delete_group(pk: int) -> bool:
        try:
            group = Group.objects.get(pk=pk)
            group.delete()
            return True
        except Group.DoesNotExist:
            return False