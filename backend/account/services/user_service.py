from typing import Any, Dict, Optional

from django.contrib.auth.models import Group

from account.models import User


class UserService:

    @staticmethod
    def update_account_privilege_status(user: User) -> None:
        user_groups = user.groups.values_list('name', flat=True)

        if 'Administratorzy' in user_groups and not (user.is_superuser and user.is_staff):
            user.is_superuser = True
            user.is_staff = True
        elif 'Recepcjoniści' in user_groups and not (not user.is_superuser and user.is_staff):
            user.is_superuser = False
            user.is_staff = True
        elif 'Klienci' in user_groups and (user.is_superuser or user.is_staff):
            user.is_superuser = False
            user.is_staff = False
        user.save()

    @staticmethod
    def get_users(
        order_by: str = 'id',
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        try:
            if filters:
                users = User.objects.filter(**filters).order_by(order_by)
            else:
                users = User.objects.all().order_by(order_by)

            response = {'status': 'Success', 'content': users}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response

    @staticmethod
    def get_user(pk: int) -> Dict[str, Any]:
        try:
            user = User.objects.get(pk=pk)
            response = {'status': 'Success', 'content': user}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response

    @staticmethod
    def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            groups = user_data.pop('groups', list(Group.objects.filter(name='Klienci').values_list('id', flat=True)))
            user = User.objects.create_user(**user_data)
            if groups:
                user.groups.set(groups)
                UserService.update_account_privilege_status(user)
            response = {'status': 'Success', 'content': user}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response

    @staticmethod
    def update_user(pk: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            user = User.objects.get(pk=pk)
            password = user_data.pop('password', None)
            groups = user_data.pop('groups', None)

            if password:
                user.set_password(password)
                user.save()
            if groups:
                user.groups.set(groups)
                UserService.update_account_privilege_status(user)
            if user_data:
                User.objects.filter(pk=pk).update(**user_data)

            user = User.objects.get(pk=pk)
            response = {'status': 'Success', 'content': user}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response

    @staticmethod
    def delete_user(pk: int) -> Dict[str, Any]:
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            response = {'status': 'Success'}
        except Exception as err:
            response = {'status': 'Error', 'errors': str(err)}

        return response
