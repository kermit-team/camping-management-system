from typing import Any, Dict, List, Optional, Union

from django.db.models import QuerySet
from django.db.utils import IntegrityError
from django.core.exceptions import FieldError, FieldDoesNotExist

from account.models import User


class UserService:

    @staticmethod
    def get_users(
        order_by: str = 'id',
        filters: Optional[Dict[str, Any]] = None) -> Optional[Union[QuerySet, List[User]]]:
        try:
            if filters:
                users = User.objects.filter(**filters).order_by(order_by)
            else:
                users = User.objects.all().order_by(order_by)
            return users
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None
            
    @staticmethod
    def get_user(pk: int) -> Optional[User]:
        try:
            user = User.objects.get(pk=pk)
            return user
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def create_user(user_data: Dict[str, Any]) -> Optional[User]:
        try:
            groups = user_data.pop('groups', None)
            user = User.objects.create_user(**user_data)
            if groups:
                user.groups.set(groups)
                    
            return user
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None
        except IntegrityError:
            return None

    @staticmethod
    def update_user(pk: int, user_data: Dict[str, Any]) -> Optional[User]:
        try:
            user = User.objects.get(pk=pk)
            password = user_data.pop('password', None)
            groups = user_data.pop('groups', None)
            
            if password:
                user.set_password(password)
                user.save()
            if groups:
                user.groups.set(groups)
            if user_data:                    
                User.objects.filter(pk=pk).update(**user_data)

            user = User.objects.get(pk=pk)
            return user
        except User.DoesNotExist:
            return None
        except FieldError:
            return None
        except FieldDoesNotExist:
            return None


    @staticmethod
    def delete_user(pk:int) -> bool:
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return True
        except User.DoesNotExist:
            return False
        