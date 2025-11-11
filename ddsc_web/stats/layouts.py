from crispy_forms.layout import Field, Div
from django.utils.translation import gettext_lazy as _

question_field_layout = Div(
    Field("question", type="text", css_class="form-control", required=True),
    css_class="form-row",
)

year_field_layout = Div(
    Field("year", type="number", css_class="form-control custom-select", required=True),
    css_class="form-row",
)
