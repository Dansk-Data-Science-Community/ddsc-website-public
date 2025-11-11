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
        ),
        type="text",
        css_class="form-control",
    ),
    Field(
        "last_name",
        placeholder=_("efternavn"),
        type="text",
        css_class="form-control",
    ),
    css_class="input-group-prepend form-group",
)

# TODO: following this https://simpleisbetterthancomplex.com/tutorial/2019/01/03/how-to-use-date-picker-with-django.html
start_time_layout = Div(
    Div(
        Field(
            PrependedText(
                "start_datetime",
                '<i class="fas fa-hourglass-start"></i>',
                placeholder=_("starttidspunkt"),
            ),
            css_class="form-control",
            type="datetime-local",
        ),
        css_class="input-group date",
        id="datetimepicker1",
        data_target_input="nearest",
    ),
    data_target="#datetimepicker1",
    data_toggle="datetimepicker",
)

end_time_layout = Div(
    Div(
        Field(
            PrependedText(
                "end_datetime",
                '<i class="fas fa-hourglass-end"></i>',
                placeholder=_("sluttidspunkt"),
            ),
            css_class="form-control",
            type="datetime-local",
        ),
        css_class="input-group date",
        id="datetimepicker2",
        data_target_input="nearest",
    ),
    data_target="#datetimepicker2",
    data_toggle="datetimepicker",
)


title_field_layout = Div(
    Field(
        PrependedText(
            "title",
            '<i class="fas fa-heading"></i>',
            placeholder=_("titel"),
        ),
        type="text",
        css_class="form-control",
    ),
)

location_field_layout = Div(
    Field(
        PrependedText(
            "location",
            '<i class="fas fa-location-arrow"></i>',
            placeholder=_("sted"),
        ),
        type="text",
        css_class="form-control",
    ),
)

signup_type_field_layout = Div(
    Field(
        PrependedText(
            "signup_type",
            '<i class="fas fa-user-plus"></i>',
            placeholder=_("tilmeldingstype"),
        ),
        type="text",
        css_class="form-control",
    ),
)

signup_link_field_layout = Div(
    Field(
        PrependedText(
            "signup_link",
            '<i class="fas fa-link"></i>',
            placeholder=_("eksternt tilmeldingslink"),
        ),
        type="url",
        css_class="form-control",
    ),
)

maximum_attendees_field_layout = Div(
    Field(
        PrependedText(
            "maximum_attendees",
            '<i class="fas fa-users"></i>',
            placeholder=_("maks antal deltagere"),
        ),
        type="number",
        css_class="form-control",
    ),
)

summary_field_layout = Div(
    Field(
        "summary",
        placeholder=_("event resumé"),
        type="text",
        css_class="form-control",
        rows=5,
    ),
)

description_field_layout = Div(
    Field(
        "description",
        placeholder=_("event beskrivelse"),
        type="text",
        css_class="form-control",
    )
)


city_field_layout = Div(
    Field(
        PrependedText(
            "city",
            '<i class="fa-solid fa-city"></i>',
            placeholder=_("bynavn"),
        ),
        type="text",
        css_class="form-control",
    )
)


streetname_and_number_field_layout = Div(
    Field(
        PrependedText(
            "address",
            '<i class="fa-solid fa-house"></i>',
            placeholder=_("vejnavn og husnummer"),
        ),
        type="text",
        css_class="form-control",
    )
)


postal_code_field_layout = Div(
    Field(
        PrependedText(
            "postal_code",
            "",
            placeholder=_("postnummer"),
        ),
        type="text",
        css_class="form-control",
    )
)

eventimage_field_layout = Div(
    Field(
        "image",
        placeholder=_("billed"),
        css_class="form-control",
    ),
    css_class="input-group-prepend form-group",
)

accept_terms_layout = Field(
    "accept_terms",
    HTML(
        """
            <p class="text-center links" style="font-size: 0.75rem;" for="id_accept_terms">
                {}<a href="#" data-toggle="modal" data-target=".privacy">{}</a>
            </p>
        """.format(
            _("Læs og acceptér"), _("betingelserne for tilmelding")
        )
    ),
    css_class="form-check-input",
)


registration_terms_field_layout = Div(
    Field(
        PrependedText(
            "registration_terms",
            '<i class="fas fa-file-contract"></i>',
            placeholder=_("tilmendingsbetingelser"),
        ),
        type="text",
        css_class="form-control",
    ),
)
