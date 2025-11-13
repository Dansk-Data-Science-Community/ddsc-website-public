import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class Reminder(models.Model):
    class ReminderTypeChoice(models.TextChoices):
        BEFORE_24_HOURS = "24_HOURS", _("24 hours before")
        BEFORE_1_HOUR = "1_HOUR", _("1 hour before")

    class ReminderStatusChoice(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        SENT = "SENT", _("Sent")
        ERROR = "ERROR", _("Error")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_registration = models.ForeignKey(
        "events.EventRegistration",
        on_delete=models.CASCADE,
        related_name="reminders",
    )
    reminder_type = models.CharField(
        max_length=20,
        choices=ReminderTypeChoice.choices,
    )
    send_at = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=ReminderStatusChoice.choices,
        default=ReminderStatusChoice.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reminder for {self.event_registration.user} for event {self.event_registration.event.title} at {self.send_at}"

    class Meta:
        ordering = ["-send_at"]
