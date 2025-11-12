from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Div, Layout, Submit
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE
from django.utils import timezone

from .layouts import (
    email_field_layout,
    full_name_layout,
    start_time_layout,
    end_time_layout,
    title_field_layout,
    location_field_layout,
    signup_type_field_layout,
    signup_link_field_layout,
    maximum_attendees_field_layout,
    summary_field_layout,
    description_field_layout,
    city_field_layout,
    postal_code_field_layout,
    streetname_and_number_field_layout,
    eventimage_field_layout,
    accept_terms_layout,
    registration_terms_field_layout,
)
from .models import Event, Address, EventImage, RegistrationTerms

User = get_user_model()


class RegisterEventForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput,
        disabled=True,
        required=False,
    )
    first_name = forms.CharField(
        widget=forms.TextInput,
        disabled=True,
        required=False,
    )
    last_name = forms.CharField(
        widget=forms.TextInput,
        disabled=True,
        required=False,
    )
    accept_terms = forms.BooleanField(
        widget=forms.CheckboxInput,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.render_required_fields = False
        self.helper.layout = Layout(
            Div(
                email_field_layout,
                css_class="input-group form-group",
            ),
            full_name_layout,
            Div(
                accept_terms_layout,
                css_class="input-group form-group",
            ),
            ButtonHolder(
                Submit(
                    "submit",
                    _("Tilmeld"),
                    css_class="btn button-color text-white-50 text-center",
                )
            ),
        )


class CreateEventForm(forms.ModelForm):
    datetime_format = "%d-%m-%Y %H:%M"

    description = forms.CharField(
        widget=TinyMCE(attrs={"cols": 80, "rows": 30}),
        help_text=_("Beskrivelse af indholdet i eventet"),
    )
    title = forms.CharField(
        help_text=_("Titel på eventet"),
        max_length=20,
    )
    start_datetime = forms.DateTimeField(
        help_text=_("Starttidspunkt for eventet"),
        input_formats=[datetime_format],
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control datetimepicker-input",
                "data-target": "#datetimepicker1",
            }
        ),
    )
    end_datetime = forms.DateTimeField(
        input_formats=[datetime_format],
        help_text=_("Sluttidspunkt for eventet"),
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control datetimepicker-input",
                "data-target": "#datetimepicker2",
            }
        ),
    )
    signup_type = forms.ChoiceField(
        help_text=_("Hvilken tilmeldingstype skal eventet have?"),
        choices=Event.SignupTypeChoice.choices,
    )
    summary = forms.CharField(
        widget=forms.Textarea,
        help_text=_("Resumé af eventet"),
    )
    registration_terms = forms.ModelChoiceField(
        RegistrationTerms.objects.all(),
        required=True,
        empty_label=_("Ingen vilkår"),
        help_text=_("Vælg vilkår for tilmelding"),
    )

    class Meta:
        model = Event
        exclude = (
            "id",
            "registrations",
            "slug",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.render_required_fields = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                title_field_layout,
                Div(
                    start_time_layout,
                    end_time_layout,
                    css_class="input-group-prepend form-group",
                ),
                location_field_layout,
                signup_type_field_layout,
                registration_terms_field_layout,
                signup_link_field_layout,
                maximum_attendees_field_layout,
                summary_field_layout,
                css_class="col-9 mx-auto",
            ),
            description_field_layout,
        )

    def clean(self):
        cleaned_data = super().clean()
        self.__validate_datetime(cleaned_data)
        self.__validate_registration_link(cleaned_data)

    def __validate_datetime(self, cleaned_data):
        start_datetime = cleaned_data.get("start_datetime")
        end_datetime = cleaned_data.get("end_datetime")
        now = timezone.now()
        if start_datetime < now or end_datetime < now:
            raise forms.ValidationError(_("Tidspunkterne skal være i fremtiden"))

        if not start_datetime < end_datetime:
            raise forms.ValidationError(
                _("Start tidspunkt skal være før slut tidspunktet")
            )

    def __validate_registration_link(self, cleaned_data):
        signup_type = cleaned_data.get("signup_type")
        signup_link = cleaned_data.get("signup_link", None)
        if not signup_type == "DDSC" and not signup_link:
            raise forms.ValidationError(
                _(
                    "Tilmeldingslinket skal være udfyldt hvis tilmeldingstypen ikke er DDSC"
                )
            )


class EventAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = (
            "id",
            "event",
            "region",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.render_required_fields = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                streetname_and_number_field_layout,
                Div(
                    city_field_layout,
                    postal_code_field_layout,
                    css_class="input-group-prepend form-group",
                ),
                css_class="col-9 mx-auto",
            ),
        )


class EventImageForm(forms.ModelForm):
    class Meta:
        model = EventImage
        fields = ("image",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.render_required_fields = True
        self.helper.use_custom_control = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                eventimage_field_layout,
                css_class="col-9 mx-auto",
            ),
        )
