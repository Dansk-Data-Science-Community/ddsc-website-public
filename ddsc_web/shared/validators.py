from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_fixed_digits(value):
    FIXED_DIGITS = 4
    if not len(str(value)) == FIXED_DIGITS:
        raise ValidationError(
            _("%(value)s er ugyldigt. Postnummeret skal have 4 cifre"),
            params={"value": value},
        )
