from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime


def validate_date(value):
    now = datetime.datetime.now()
    if value > now:
        raise ValidationError(
            f'{value} не может быть больше {now}'
        )
