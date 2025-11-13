from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path("newsletter/", views.NewsletterSignupView.as_view(), name="newsletter_signup"),
    path(
        "newsletter/thanks/",
        views.NewsletterThankYouView.as_view(),
        name="newsletter_thanks",
    ),
    path(
        "newsletter/confirm/<uuid:token>/",
        views.NewsletterConfirmView.as_view(),
        name="newsletter_confirm",
    ),
    path(
        "newsletter/unsubscribe/<uuid:token>/",
        views.NewsletterUnsubscribeView.as_view(),
        name="newsletter_unsubscribe",
    ),
]
