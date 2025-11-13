from django.utils import timezone
from django.db.models import Count

from events.models import Event

from .models import EventAttendanceMetric, PageView, UserActivityMetric


def record_page_view(*, path: str, session_key: str, user=None, user_agent: str = ""):
    PageView.objects.create(
        path=path,
        session_key=session_key,
        user=user if getattr(user, "is_authenticated", False) else None,
        user_agent=user_agent[:256],
    )


def snapshot_event_attendance():
    for event in Event.objects.filter(start_datetime__gte=timezone.now()):
        EventAttendanceMetric.objects.create(
            event=event,
            attendees=event.attendees.count(),
            capacity=event.maximum_attendees,
        )


def record_user_activity(*, user, action: str, context: dict | None = None):
    if not user or not user.is_authenticated:
        return
    UserActivityMetric.objects.create(
        user=user,
        action=action,
        context=context or {},
    )
