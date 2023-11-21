from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_date(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'{value} не может быть больше {now}'
        )


def validate_score(value):
    if not (0 < value < 11):
        raise ValidationError(
            'Оценка не может быть больше 10 и меньше 0'
        )
