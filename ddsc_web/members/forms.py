from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import Address, Member
from .layouts import address_field_layout, city_postal_field_layout
from shared.layouts import (
    accept_terms_layout,
    allow_newsletters_layout,
    job_title_layout,
)

User = get_user_model()


class MemberAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("address", "postal_code", "city")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.render_required_fields = False
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                address_field_layout,
            ),
            city_postal_field_layout,
        )


class UserMemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ("accept_terms", "allow_newsletters", "job_title")

    accept_terms = forms.BooleanField(
        widget=forms.CheckboxInput,
        required=True,
    )

    job_title = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": _("stillingsbetegnelse"), "size": 35}
        ),
        required=True,
    )

    allow_newsletters = forms.BooleanField(
        widget=forms.CheckboxInput,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.render_required_fields = False
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                job_title_layout,
                css_class="input-group form-group",
            ),
            Div(
                accept_terms_layout,
                css_class="input-group form-group mb-1",
            ),
            Div(
                allow_newsletters_layout,
                css_class="input-group form-group mb-1",
            ),
        )


class EditMemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ("allow_newsletters", "job_title")

    allow_newsletters = forms.BooleanField(
        widget=forms.CheckboxInput,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.render_required_fields = False
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                job_title_layout,
                allow_newsletters_layout,
                css_class="input-group form-group mb-1",
            ),
        )
