from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.utils.translation import gettext_lazy as _

from .layouts import full_name_layout


class FullNameForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput,
        required=True,
        help_text=_("Fornavn"),
        disabled=True,
    )
    last_name = forms.CharField(
        widget=forms.TextInput,
        required=True,
        help_text=_("Efternavn"),
        disabled=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.render_required_fields = False
        self.helper.form_tag = False
        self.helper.layout = Layout(
            full_name_layout,
        )
