import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class SpecialCharacterValidator:
    @staticmethod
    def validate(password, user=None):
        if not re.findall(r'[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _(r'The password must contain at least 1 symbol: [()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]'),
                code='password_no_symbol',
            )

    @staticmethod
    def get_help_text():
        return _(
            r'Your password must contain at least 1 symbol: [()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]',
        )
