from django.db.models import Model
from django.core.exceptions import FieldDoesNotExist

@classmethod
def model_field_exists(cls: Model, field: str) -> bool:
    try:
        cls._meta.get_field(field)
        return True
    except FieldDoesNotExist:
        return False

Model.field_exists = model_field_exists