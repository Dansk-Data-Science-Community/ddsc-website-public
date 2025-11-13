from django.db import models


class SurveyData(models.Model):
    class Meta:
        ordering = ["year", "question"]
        indexes = [
            models.Index(fields=["question", "year"]),
        ]

    user_id = models.IntegerField(null=False, blank=False)
    question = models.CharField(max_length=750, db_index=True)
    answer = models.TextField(null=True, blank=True)
    year = models.IntegerField(db_index=True)
    monthly_salary = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField()


class PageView(models.Model):
    path = models.CharField(max_length=512, db_index=True)
    user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=64, db_index=True)
    user_agent = models.CharField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class EventAttendanceMetric(models.Model):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, related_name="analytics")
    attendees = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    captured_at = models.DateTimeField(auto_now_add=True)


class UserActivityMetric(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    action = models.CharField(max_length=64)
    context = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
