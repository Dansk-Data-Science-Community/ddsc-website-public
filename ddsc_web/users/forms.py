from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Div, Field, Layout, Submit, HTML
from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .tasks import send_mail
import datetime

from .layouts import (
    email_field_layout,
    full_name_layout,
    password_layout,
    accept_terms_layout,
)
from .models import Profile, ProfileImage

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput,
        required=True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
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
            Div(
                password_layout,
                css_class="input-group form-group",
            ),
            ButtonHolder(
                Submit(
                    "submit",
                    _("Log ind"),
                    css_class="btn button-color text-white-50 float-right",
                )
            ),
        )


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label=_("Adgangskode"),
        widget=forms.PasswordInput(attrs={"placeholder": _("adgangskode")}),
    )
    password2 = forms.CharField(
        label=_("Gentag adgangskode"),
        widget=forms.PasswordInput(attrs={"placeholder": _("gentag adgangskode")}),
    )
    accept_terms = forms.BooleanField(widget=forms.CheckboxInput, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.render_required_fields = False
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.layout = Layout(
            Div(
                email_field_layout,
                css_class="input-group form-group",
            ),
            full_name_layout,
            Div(
                password_layout,
                css_class="input-group",
            ),
            Div(
                Field(
                    PrependedText(
                        "password2",
                        '<i class="fas fa-key"></i>',
                        placeholder=_("gentag adgangskode"),
                    ),
                    type="password",
                    css_class="form-control",
                ),
                accept_terms_layout,
                css_class="input-group form-group",
            ),
            ButtonHolder(
                Submit(
                    "submit",
                    _("Opret"),
                    css_class="btn button-color text-white-50 float-right",
                )
            ),
        )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError(_("Adgangskoderne er ikke ens."))
        return cd["password2"]


# TODO: Formularen skal tilpasses, så label står foran felt. Gælder alle tre nedenstående forms
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.render_required_fields = True
        self.helper.form_tag = False
        self.fields["first_name"].label = _("Fornavn")
        self.fields["last_name"].label = _("Efternavn")
        self.helper.layout = Layout(
            full_name_layout,
            Div(
                email_field_layout,
                css_class="input-group form-group",
            ),
        )


class DateInput(forms.DateInput):
    input_type = "date"


def year_choices():
    return [year for year in range(1920, datetime.date.today().year + 1)]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("birthdate",)
        widgets = {
            "birthdate": forms.SelectDateWidget(years=year_choices()),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.render_required_fields = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Field(
                    PrependedText(
                        "birthdate",
                        '<i class="fas fa-calendar"></i>',
                    ),
                    css_class="input-group",
                ),
                css_class="input-group",
            )
        )


# TODO: Der skal findes en widget til at uploade billeder med i django som er simpelt. Måske med cropping.
# https://gist.github.com/anhtran/f6d91a41da2bd5bbfc17868b7f528a88
class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = ProfileImage
        fields = ("image",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.render_required_fields = False
        self.helper.form_tag = False
        self.helper.use_custom_control = True
        self.helper.layout = Layout(
            Div(
                Field("image"),
                css_class="input-group form-group",
            ),
        )


class ChangePasswordForm(auth_forms.PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Adgangskode"),
        widget=forms.PasswordInput(attrs={"placeholder": _("nuværende adgangskode")}),
    )
    new_password1 = forms.CharField(
        label=_("Ny adgangskode"),
        widget=forms.PasswordInput(attrs={"placeholder": _("ny adgangskode")}),
    )
    new_password2 = forms.CharField(
        label=_("Gentag ny adgangskode"),
        widget=forms.PasswordInput(attrs={"placeholder": _("gentag ny adgangskode")}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.render_required_fields = False
        self.helper.layout = Layout(
            Div(
                Field(
                    PrependedText(
                        "old_password",
                        '<i class="fas fa-key"></i>',
                        placeholder=_("nuværende adgangskode"),
                    ),
                    type="password",
                    css_class="form-control",
                ),
                css_class="input-group form-group",
            ),
            Div(
                Field(
                    PrependedText(
                        "new_password1",
                        '<i class="fas fa-key"></i>',
                        placeholder=_("ny adgangskode"),
                    ),
                    type="password",
                    css_class="form-control",
                ),
                css_class="input-group",
            ),
            Div(
                Field(
                    PrependedText(
                        "new_password2",
                        '<i class="fas fa-key"></i>',
                        placeholder=_("gentag ny adgangskode"),
                    ),
                    type="password",
                    css_class="form-control",
                ),
                css_class="input-group form-group",
            ),
            ButtonHolder(
                Submit(
                    "submit",
                    _("Gem"),
                    css_class="btn button-color text-white-50 float-right",
                )
            ),
            ButtonHolder(
                Submit(
                    "#",
                    _("Tilbage"),
                    css_class="btn btn-secondary text-white-50 float-right mr-2",
                    onclick="javascript:history.back();",
                )
            ),
        )

    def clean_repeat_new_password(self):
        cd = self.cleaned_data
        if cd["new_password"] != cd["repeat_new_password"]:
            raise forms.ValidationError(_("Adgangskoderne er ikke ens."))
        return cd["repeat_new_password"]


class PasswordResetForm(auth_forms.PasswordResetForm):
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
            ButtonHolder(
                Submit(
                    "submit",
                    _("Send mail"),
                    css_class="btn button-color text-white-50 float-right",
                )
            ),
        )

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        context["user"] = context["user"].id

        send_mail.delay(
            subject_template_name=subject_template_name,
            email_template_name=email_template_name,
            context=context,
            from_email=from_email,
            to_email=to_email,
            html_email_template_name=html_email_template_name,
        )


class SetPasswordForm(auth_forms.SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput,
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.render_required_fields = False
        self.helper.help_text_inline = False
        self.helper.layout = Layout(
            Div(
                Field(
                    PrependedText(
                        "new_password1",
                        '<i class="fas fa-key"></i>',
                        placeholder=_("ny adgangskode"),
                    ),
                    type="password",
                    css_class="form-control",
                ),
                css_class="input-group",
            ),
            Div(
                Field(
                    PrependedText(
                        "new_password2",
                        '<i class="fas fa-key"></i>',
                        placeholder=_("gentag adgangskode"),
                    ),
                    type="password",
                    css_class="form-control",
                ),
                css_class="input-group form-group",
            ),
            ButtonHolder(
                Submit(
                    "submit",
                    _("Bekræft"),
                    css_class="btn button-color text-white-50 float-right",
                )
            ),
        )
