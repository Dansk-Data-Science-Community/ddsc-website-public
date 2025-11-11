from crispy_forms.layout import Field, Div, HTML
from crispy_forms.bootstrap import PrependedText
from django.utils.translation import gettext_lazy as _


email_field_layout = Field(
    PrependedText(
        "email",
        '<i class="fas fa-envelope"></i>',
        placeholder=_("email adresse"),
    ),
    type="text",
    css_class="form-control",
)

full_name_layout = Div(
    Field(
        PrependedText(
            "first_name",
            '<i class="fas fa-user"></i>',
            placeholder=_("fornavn"),
            label=_("fornavn"),
        ),
        type="text",
        css_class="form-control",
    ),
    Field(
        "last_name",
        placeholder=_("efternavn"),
        label=_("efternavn"),
        type="text",
        css_class="form-control",
    ),
    css_class="input-group-prepend form-group",
)

password_layout = Field(
    PrependedText(
        "password",
        '<i class="fas fa-key"></i>',
        placeholder=_("adgangskode"),
    ),
    type="password",
    css_class="form-control",
)

accept_terms_layout = Field(
    "accept_terms",
    HTML(
        """<p class="text-white-50 text-center links" style="font-size: 0.75rem;" for="id_accept_terms">
                {}<a href="#" data-toggle="modal" data-target=".privacy">{}</a>
            </p>
        """.format(
            _("Læs og acceptér"), _("betingelserne for databeskyttelse")
        )
    ),
    css_class="form-check-input",
)
