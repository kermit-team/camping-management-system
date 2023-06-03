from django.core.exceptions import FieldDoesNotExist
from django.db.models import Model


def model_field_exists(cls: Model, field: str) -> bool:
    try:
        cls._meta.get_field(field)
        return True
    except FieldDoesNotExist:
        return False


Model.field_exists = classmethod(model_field_exists)
