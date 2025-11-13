from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    # Newsletter landing page
    path("newsletter/", views.newsletter_landing, name="newsletter_landing"),

    # Subscription endpoints
    path("subscribe/", views.subscribe_widget, name="subscribe_widget"),
    path("confirmation-pending/", views.confirmation_pending, name="confirmation_pending"),
    path("confirm/<str:token>/", views.confirm_subscription, name="confirm_subscription"),

    # Preferences management
    path("preferences/", views.update_preferences, name="update_preferences"),

    # Unsubscribe workflows
    path("unsubscribe/", views.unsubscribe, name="unsubscribe"),
    path("unsubscribe/<str:token>/", views.unsubscribe, name="unsubscribe_token"),

    # Resubscribe
    path("resubscribe/", views.resubscribe, name="resubscribe"),

    # Legacy endpoint (redirects to confirmation_pending)
    path("success/", views.subscribe_success, name="news_success"),
]
