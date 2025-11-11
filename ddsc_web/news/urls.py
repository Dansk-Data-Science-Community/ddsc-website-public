from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path("success/", views.subscribe_to_news, name="news_success"),
]
