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
            placeholder=_("Fornavn"),
        ),
        type="text",
        css_class="form-control",
    ),
    Field(
        "last_name",
        placeholder=_("Efternavn"),
        type="text",
        css_class="form-control",
    ),
    css_class="input-group-prepend form-group",
)


accept_terms_layout = Field(
    "accept_terms",
    HTML(
        """<p class="text-center links" style="font-size: 0.75rem;" for="id_accept_terms">
                {}<a href="#" data-toggle="modal" data-target=".privacy">{}</a>
            </p>
        """.format(
            _("Læs og acceptér"), _("betingelserne for databeskyttelse")
        )
    ),
    css_class="form-check-input",
)

allow_newsletters_layout = Field(
    "allow_newsletters",
    HTML(
        """<p class="text-center" style="font-size: 0.75rem;" for="id_accept_terms">
                {}
            </p>
        """.format(
            _("Ja tak, jeg vil gerne modtage nyhedsbreve fra DDSC")
        )
    ),
    css_class="form-check-input",
)

job_title_layout = Div(
    Field(
        PrependedText(
            "job_title",
            '<i class="fas fa-briefcase"></i>',
        ),
        type="text",
        placeholder=_("Stillingsbetegnelse"),
    ),
    css_class="input-group",
)
