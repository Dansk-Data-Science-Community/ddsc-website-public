from crispy_forms.layout import Field, Div
from crispy_forms.bootstrap import PrependedText, PrependedAppendedText
from django.utils.translation import gettext_lazy as _

address_field_layout = Div(
    Field(
        PrependedText(
            "address",
            '<i class="fas fa-address-card"></i>',
            placeholder=_("Vejnavn og husnummer"),
        ),
        type="text",
        css_class="form-control",
    ),
    css_class="input-group",
)

city_postal_field_layout = Div(
    Field(
        PrependedText(
            "postal_code",
            '<i class="fas fa-address-card"></i>',
            placeholder=_("Postnummer"),
        ),
        type="text",
        css_class="form-control",
    ),
    Field(
        "city",
        placeholder=_("By"),
        type="text",
        css_class="form-control",
    ),
    css_class="input-group-prepend input-group",
)

sub_amount_field_layout = Div(
    Field(
        PrependedAppendedText(
            "subscription_amount",
            '<i class="fas fa-money-bill-alt"></i>',
            "kr.",
            placeholder=_("Kontingent beløb"),
        ),
        type="number",
        css_class="form-contorl",
    ),
    css_class="input-group",
)
