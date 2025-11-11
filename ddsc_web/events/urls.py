from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.event_list, name="event_list"),
    path(
        "register/<int:id>/<slug:slug>/", views.RegisterEvent.as_view(), name="register"
    ),
    path("<int:id>/<slug:slug>/", views.share_event, name="share"),
    path("unregister/<int:id>/<slug:slug>/", views.unregister_event, name="unregister"),
    path("create/", views.CreateEvent.as_view(), name="create_event"),
    path("edit/<int:id>/<slug:slug>/", views.EditEvent.as_view(), name="edit_event"),
    path("delete/<pk>/", views.DeleteEvent.as_view(), name="delete_event"),
    path("minimeetup/", views.MiniMeetupView.as_view(), name="mini_meetup"),
    path("consume/<token>/", views.consume_ticket, name="consume_ticket"),
]
