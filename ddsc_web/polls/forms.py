from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django import forms
from django.utils.translation import gettext_lazy as _


class QuestionChoiceForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=None, label=_("Vælg"))
    question = forms.ModelChoiceField(queryset=None, widget=forms.HiddenInput())

    def __init__(self, choice_queryset, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["choice"].queryset = choice_queryset
