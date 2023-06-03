import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class UppercaseValidator:
    @staticmethod
    def validate(password, user=None):
        if not re.findall(r'[A-Z]', password):
            raise ValidationError(
                _('The password must contain at least 1 uppercase letter, A-Z.'),
                code='password_no_upper',
            )

    @staticmethod
    def get_help_text():
        return _(
            'Your password must contain at least 1 uppercase letter, A-Z.',
        )
