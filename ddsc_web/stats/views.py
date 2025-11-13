import math
from itertools import accumulate

from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.cache import cache_page

from .forms import QuestionForm, get_exclude_list
from .models import SurveyData
from .queries import (
    get_salary_stats_by_answer,
    get_object_stats_by_month,
    queryset_to_lists,
    get_queryset_fields,
)


class StatsView(View):
    @method_decorator(cache_page(60 * 60))
    def get(self, request, *args, **kwargs):
        user_stats = get_object_stats_by_month("users", "User", "date_joined")
        member_stats = get_object_stats_by_month("members", "Member", "created")
        event_stats = get_object_stats_by_month(
            "events",
            "EventRegistration",
            "created",
        )

        return render(
            request,
            "stats/stats.html",
            {
                "user_stats": get_labels_and_data(user_stats),
                "member_stats": get_labels_and_data(member_stats),
                "event_stats": get_labels_and_data(event_stats),
            },
        )


def get_labels_and_data(queryset):
    data = list(accumulate((row["total"] for row in queryset)))
    return {
        "labels": [row["month"].strftime("%b %Y") for row in queryset],
        "data": data,
        "stepsize": calculate_stepsize(data, number_of_steps=4),
    }


def calculate_stepsize(data: list[int], number_of_steps: int):
    max_number = max(data)
    return _round_to_nearest_integer(max_number / number_of_steps, nearest=50)


def _round_to_nearest_integer(number: float, nearest: int):
    return math.ceil(number / nearest) * nearest


class FrequencyView(View):
    def get(self, request, *args, **kwargs):
        question = (
            SurveyData.objects.exclude(question__in=get_exclude_list())
            .values("question")
            .last()
        )
        year = SurveyData.objects.values("year").first()
        form = QuestionForm(initial=question | year)

        salary_data = self.__get_salary_stats_by_answer(
            question.get("question"),
            [year.get("year")],
        )
        return self.__render_chart(
            request,
            salary_data,
            form,
        )

    def post(self, request, *args, **kwargs):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data["question"]
            years = form.cleaned_data["year"]

            salary_data = self.__get_salary_stats_by_answer(question, years)

            return self.__render_chart(
                request,
                salary_data,
                form,
            )
        else:
            messages.error(request, _(f"{form.errors}"))
            return redirect("stats:salary_survey")

    def __get_salary_stats_by_answer(self, question: str, years: list[int]):
        queryset = get_salary_stats_by_answer(question, years=years)
        fields = get_queryset_fields(queryset)
        return queryset_to_lists(queryset, fields)

    def __render_chart(
        self,
        request,
        salary_data: dict,
        form: QuestionForm,
    ):
        return render(
            request,
            "stats/salary_survey.html",
            {
                "form": form,
                **salary_data,
            },
        )
