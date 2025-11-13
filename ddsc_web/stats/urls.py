from django.urls import path
from .views import StatsView, FrequencyView

app_name = "stats"

urlpatterns = [
    path("dashboard/", StatsView.as_view(), name="stats"),
    path("salary-survey/", FrequencyView.as_view(), name="salary_survey"),
]
