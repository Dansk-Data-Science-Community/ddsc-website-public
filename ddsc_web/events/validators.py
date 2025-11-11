from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_image_order(value):
    if not value > 0:
        raise ValidationError(
            _(
                "%(value)s er ugyldigt. Rækkefølgen på billedet skal angives som positivt tal"
            ),
            params={"value": value},
        )


def validate_maximum_attendees(value):
    if not value > 0:
        raise ValidationError(
            _(
                "%(value)s er ugyldigt. Maksimum deltagere skal være et positivt tal større end 0"
            ),
            params={"value": value},
        )
