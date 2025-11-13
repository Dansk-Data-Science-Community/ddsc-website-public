from django.urls import path
from .views import StatsView, FrequencyView
from . import api

app_name = "stats"

urlpatterns = [
    path("dashboard/", StatsView.as_view(), name="stats"),
    path("salary-survey/", FrequencyView.as_view(), name="salary_survey"),
    path("api/dashboard/", api.analytics_summary, name="analytics_summary_api"),
]
