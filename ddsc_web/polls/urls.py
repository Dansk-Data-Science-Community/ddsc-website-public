from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path("", views.list_polls, name="list_polls"),
    path("<int:poll_session_id>/", views.poll_detail, name="poll_detail"),
    path("<int:voter_session_id>/vote/", views.submit_poll, name="submit_poll"),
    path("<int:poll_session_id>/results/", views.poll_results, name="poll_results"),
]
