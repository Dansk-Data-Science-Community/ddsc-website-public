from django.db import models
from django.utils.translation import gettext_lazy as _
from .validators import validate_fixed_digits


class AbstractAddress(models.Model):
    class Meta:
        abstract = True

    class RegionChoices(models.IntegerChoices):
        NORDJYLLAND = 1081, _("Region Nordjylland")
        MIDTJYLLAND = 1082, _("Region Midtjylland")
        SYDDANMARK = 1083, _("Region Syddanmark")
        HOVEDSTADEN = 1084, _("Region Hovedstaden")
        SJÆLLAND = 1085, _("Region Sjælland")

    address = models.CharField(max_length=250, help_text=_("Vejnavn og husnummer"))
    postal_code = models.PositiveIntegerField(
        help_text=_("Postnummer"), validators=[validate_fixed_digits]
    )
    city = models.CharField(max_length=250, help_text=_("Bynavn"))
    region = models.IntegerField(
        choices=RegionChoices.choices,
        help_text=_("Region"),
        null=True,
        blank=True,
    )
