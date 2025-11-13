from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Avg, Count, F
from django.http import JsonResponse
from django.utils import timezone

from .models import EventAttendanceMetric, PageView, UserActivityMetric


def staff_required(view):
    return login_required(user_passes_test(lambda u: u.is_staff)(view))


@staff_required
def analytics_summary(request):
    since = timezone.now() - timezone.timedelta(days=7)
    return JsonResponse(
        {
            "pageviews": PageView.objects.filter(created_at__gte=since).count(),
            "active_users": UserActivityMetric.objects.filter(created_at__gte=since)
            .values("user")
            .distinct()
            .count(),
            "avg_event_fill": EventAttendanceMetric.objects.annotate(
                fill=F("attendees") * 1.0 / F("capacity")
            ).aggregate(avg=Avg("fill"))["avg"],
        }
    )
