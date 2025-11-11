from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout
from django import forms

from .decorators import cache_function_result
from .models import SurveyData
from .layouts import question_field_layout, year_field_layout


def get_exclude_list() -> list[str]:
    return [
        "What tools do you use in your daily work?",
        "How much bonus did you receive last year, in DKK?",
        "What is your monthly salary in DKK, before tax and including pension?",
        "Do you agree to take part in this survey?",
        "What is your gender?",
        "Are you a Danish national/citizen?",
    ]


@cache_function_result(timeout=60 * 60 * 24)
def get_question_choices(exlude_list: list[str]) -> list[tuple[str, str]]:
    return [
        (q, q)
        for q in set(
            SurveyData.objects.values_list("question", flat=True)
            .exclude(question__in=exlude_list)
            .distinct()
        )
    ]


@cache_function_result(timeout=60 * 60 * 24)
def get_year_choices() -> list[tuple[int, int]]:
    return [
        (y, y) for y in sorted(set(SurveyData.objects.values_list("year", flat=True)))
    ]


class QuestionForm(forms.Form):
    question = forms.ChoiceField(
        choices=(),
        required=True,
        help_text=("Question to display data for."),
    )
    year = forms.MultipleChoiceField(
        choices=(),
        required=True,
        help_text=("Year(s) to display data for."),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["question"].choices = get_question_choices(get_exclude_list())
        self.fields["year"].choices = get_year_choices()
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.render_required_fields = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                question_field_layout,
                year_field_layout,
                css_class="form-group mb-1",
            ),
        )
