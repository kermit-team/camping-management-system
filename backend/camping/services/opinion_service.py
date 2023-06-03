from datetime import date
from typing import Any, Dict, Optional

from django.utils.translation import gettext as _

from account.models import User
from camping.models import Opinion, CampingPlot, Reservation


class OpinionService:

    @staticmethod
    def author_able_to_review(author: User, camping_plot: CampingPlot) -> bool:
        ended_reservation = Reservation.objects.filter(
            user=author,
            camping_plot=camping_plot,
            date_to__lte=date.today(),
        ).exists()
        existing_opinion = Opinion.objects.filter(author=author, camping_plot=camping_plot).exists()

        return ended_reservation and not existing_opinion

    @staticmethod
    def get_opinions(
        order_by: str = 'id',
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        try:
            if filters:
                opinions = Opinion.objects.filter(**filters).order_by(order_by)
            else:
                opinions = Opinion.objects.all().order_by(order_by)
            response = {'status': 'Success', 'content': opinions}
        except Exception as err:
            response = {'status': 'Error', 'errors': [str(err)]}

        return response

    @staticmethod
    def get_opinion(pk: int) -> Dict[str, Any]:
        try:
            opinion = Opinion.objects.get(pk=pk)
            response = {'status': 'Success', 'content': opinion}
        except Exception as err:
            response = {'status': 'Error', 'errors': [str(err)]}

        return response

    @staticmethod
    def create_opinion(opinion_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if not OpinionService.author_able_to_review(
                author=opinion_data['author'],
                camping_plot=opinion_data['camping_plot'],
            ):
                raise Exception(_('User is unable to create opinion for the given camping plot'))

            opinion = Opinion.objects.create(**opinion_data)
            response = {'status': 'Success', 'content': opinion}
        except Exception as err:
            response = {'status': 'Error', 'errors': [str(err)]}

        return response

    @staticmethod
    def update_opinion(pk: int, opinion_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if opinion_data:
                Opinion.objects.filter(pk=pk).update(**opinion_data)
            opinion = Opinion.objects.get(pk=pk)
            response = {'status': 'Success', 'content': opinion}
        except Exception as err:
            response = {'status': 'Error', 'errors': [str(err)]}

        return response

    @staticmethod
    def delete_opinion(pk: int) -> Dict[str, Any]:
        try:
            opinion = Opinion.objects.get(pk=pk)
            opinion.delete()
            response = {'status': 'Success'}
        except Exception as err:
            response = {'status': 'Error', 'errors': [str(err)]}

        return response
