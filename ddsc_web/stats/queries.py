from django.apps import apps
from django.db.models import Avg, Case, Count, Func, Max, Min, QuerySet, When
from django.db.models.expressions import RawSQL
from django.db.models.functions import TruncMonth

from .decorators import cache_query_result
from .models import SurveyData

YEARS_OF_EXPERIENCE_QUSTION = (
    "How many years of relevant full-time work experience do you have?"
)

YEARS_OF_EXPERIENCE_ANSWERS = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15+",
]


class Round(Func):
    function = "ROUND"
    template = "%(function)s(%(expressions)s, 0)"


class RawAnnotation(RawSQL):
    """
    RawSQL also aggregates the SQL to the `group by` clause which defeats the purpose of adding it to an Annotation.
    """

    def get_group_by_cols(self, *args, **kwargs):
        return []


def get_object_stats_by_month(
    app_name: str, model_name: str, datefield: str
) -> QuerySet:
    model_class = apps.get_model(app_name, model_name)
    return (
        model_class.objects.annotate(month=TruncMonth(datefield))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )


@cache_query_result(timeout=60 * 60 * 24)
def get_salary_stats_by_answer(question: str, years: list[int]) -> QuerySet:
    queryset = (
        SurveyData.objects.filter(
            question=question,
            year__in=years,
            answer__isnull=False,
            monthly_salary__isnull=False,
            monthly_salary__gt=0,
        )
        .exclude(answer="")
        .values("answer")
        .annotate(
            count=Count("user_id"),
            average=Round(
                Avg("monthly_salary"),
            ),
            min=Min("monthly_salary"),
            max=Max("monthly_salary"),
            median=RawAnnotation(
                "percentile_disc(%s) WITHIN GROUP (ORDER BY monthly_salary)", (0.5,)
            ),
        )
        .filter(count__gt=5)
    )
    if question == YEARS_OF_EXPERIENCE_QUSTION:
        return queryset.order_by(
            get_ordering_by_answer_list(YEARS_OF_EXPERIENCE_ANSWERS)
        )
    else:
        return queryset.order_by("-median")


def get_ordering_by_answer_list(answer_list: list[str]):
    return Case(*[When(answer=pk, then=pos) for pos, pk in enumerate(answer_list)])


def get_queryset_fields(queryset: QuerySet):
    return list(queryset[0].keys())


def get_field_values(queryset: QuerySet, field_name: str):
    return [row[field_name] for row in queryset]


def queryset_to_lists(queryset: QuerySet, field_names: list[str]):
    return {field: get_field_values(queryset, field) for field in field_names}
