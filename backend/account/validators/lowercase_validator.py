import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class LowercaseValidator:
    @staticmethod
    def validate(password, user=None):
        if not re.findall(r'[a-z]', password):
            raise ValidationError(
                _('The password must contain at least 1 lowercase letter, a-z.'),
                code='password_no_lower',
            )

    @staticmethod
    def get_help_text():
        return _(
            'Your password must contain at least 1 lowercase letter, a-z.',
        )
