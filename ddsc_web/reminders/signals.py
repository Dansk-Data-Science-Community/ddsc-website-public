from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from events.models import EventRegistration
from .models import Reminder
from .tasks import send_event_reminder

@receiver(post_save, sender=EventRegistration)
def create_and_schedule_reminders(sender, instance, created, **kwargs):
    """
    Create and schedule reminders when a new EventRegistration is created.
    """
    if created:
        event = instance.event
        now = timezone.now()

        # --- Create 24-hour reminder ---
        send_at_24h = event.start_datetime - timedelta(hours=24)
        if send_at_24h > now:
            reminder_24h = Reminder.objects.create(
                event_registration=instance,
                reminder_type=Reminder.ReminderTypeChoice.BEFORE_24_HOURS,
                send_at=send_at_24h,
            )
            # Schedule the Celery task
            send_event_reminder.apply_async(
                (str(reminder_24h.id),),
                eta=send_at_24h
            )

        # --- Create 1-hour reminder ---
        send_at_1h = event.start_datetime - timedelta(hours=1)
        if send_at_1h > now:
            reminder_1h = Reminder.objects.create(
                event_registration=instance,
                reminder_type=Reminder.ReminderTypeChoice.BEFORE_1_HOUR,
                send_at=send_at_1h,
            )
            # Schedule the Celery task
            send_event_reminder.apply_async(
                (str(reminder_1h.id),),
                eta=send_at_1h
            )
