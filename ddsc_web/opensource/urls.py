from django.urls import path
from . import views

app_name = "opensource"

urlpatterns = [
    path("", views.OpenSourceAwardView.as_view(), name="award"),
]
