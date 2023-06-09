from datetime import date
from typing import Any, Dict, Optional

from django.utils.translation import gettext as _
from rest_framework.utils import json

from account.serializers import errors_serializer
from camping.models import CampingSection, Reservation


class CampingSectionService:

    @staticmethod
    def is_camping_section_in_incoming_reservations(camping_section: CampingSection) -> bool:
        return Reservation.objects.filter(
            camping_plot__camping_section=camping_section,
            date_to__gte=date.today(),
        ).exists()

    @staticmethod
    def get_camping_sections(
        order_by: str = 'id',
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        try:
            if filters:
                camping_sections = CampingSection.objects.filter(**filters).order_by(order_by)
            else:
                camping_sections = CampingSection.objects.all().order_by(order_by)
            response = {'status': 'Success', 'content': camping_sections}
        except Exception as err:
            response = {'status': 'Error', 'errors': errors_serializer(err)}

        return response

    @staticmethod
    def get_camping_section(pk: int) -> Dict[str, Any]:
        try:
            camping_section = CampingSection.objects.get(pk=pk)
            response = {'status': 'Success', 'content': camping_section}
        except Exception as err:
            response = {'status': 'Error', 'errors': errors_serializer(err)}

        return response

    @staticmethod
    def create_camping_section(camping_section_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            camping_section = CampingSection.objects.create(**camping_section_data)
            response = {'status': 'Success', 'content': camping_section}
        except Exception as err:
            response = {'status': 'Error', 'errors': errors_serializer(err)}

        return response

    @staticmethod
    def update_camping_section(pk: int, camping_section_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if camping_section_data:
                CampingSection.objects.filter(pk=pk).update(**camping_section_data)
            camping_section = CampingSection.objects.get(pk=pk)
            response = {'status': 'Success', 'content': camping_section}
        except Exception as err:
            response = {'status': 'Error', 'errors': errors_serializer(err)}

        return response

    @staticmethod
    def delete_camping_section(pk: int) -> Dict[str, Any]:
        try:
            errors = {}
            camping_section = CampingSection.objects.get(pk=pk)
            if CampingSectionService.is_camping_section_in_incoming_reservations(camping_section):
                errors['camping_section'] = _("Camping section is used in incoming reservations")

            if errors:
                raise Exception(json.dumps(errors))

            camping_section.delete()
            response = {'status': 'Success'}
        except Exception as err:
            response = {'status': 'Error', 'errors': errors_serializer(err)}

        return response
