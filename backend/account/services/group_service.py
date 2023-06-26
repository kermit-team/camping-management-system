from typing import Any, Dict, Optional

from django.contrib.auth.models import Group

from account.serializers import errors_serializer


class GroupService:

    @staticmethod
    def get_groups(
        order_by: str = 'id',
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        try:
            if filters:
                groups = Group.objects.filter(**filters).order_by(order_by)
            else:
                groups = Group.objects.all().order_by(order_by)

            response = {'status': 'Success', 'content': groups}
        except Exception as err:
            response = {'status': 'Error', 'errors': errors_serializer(err)}

        return response

    @staticmethod
    def get_group(pk: int) -> Dict[str, Any]:
        try:
            group = Group.objects.get(pk=pk)
            response = {'status': 'Success', 'content': group}
        except Exception as err:
            response = {'status': 'Error', 'errors': errors_serializer(err)}

        return response

    @staticmethod
    def create_group(group_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            group = Group.objects.create(**group_data)
            response = {'status': 'Success', 'content': group}
        except Exception as err:
            response = {'status': 'Error', 'errors': errors_serializer(err)}

        return response

    @staticmethod
    def update_group(pk: int, group_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if group_data:
                Group.objects.filter(pk=pk).update(**group_data)
            group = Group.objects.get(pk=pk)

            response = {'status': 'Success', 'content': group}
        except Exception as err:
            response = {'status': 'Error', 'errors': errors_serializer(err)}

        return response

    @staticmethod
    def delete_group(pk: int) -> Dict[str, Any]:
        try:
            group = Group.objects.get(pk=pk)
            group.delete()
            response = {'status': 'Success'}
        except Exception as err:
            response = {'status': 'Error', 'errors': errors_serializer(err)}

        return response
