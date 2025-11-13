from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Reminder


@shared_task
def send_event_reminder(reminder_id):
    """
    Celery task to send an event reminder email.
    """
    try:
        reminder = Reminder.objects.get(id=reminder_id)
    except Reminder.DoesNotExist:
        return f"Reminder with id {reminder_id} not found."

    if reminder.status != "PENDING":
        return f"Reminder {reminder_id} is not in PENDING state. Current state: {reminder.status}"

    registration = reminder.event_registration
    user = registration.user
    event = registration.event

    subject = f"Reminder: {event.title} is starting soon!"
    
    # Basic text content for now
    # In a real scenario, we would use HTML templates
    time_until_event = event.start_datetime - timezone.now()
    hours_until = time_until_event.total_seconds() // 3600
    
    message = (
        f"Hi {user.first_name},\n\n"
        f"This is a reminder that the event '{event.title}' is starting in about {int(hours_until)} hours, "
        f"at {event.start_datetime.strftime('%Y-%m-%d %H:%M')}.\n\n"
        f"We look forward to seeing you there!\n\n"
        f"Best regards,\n"
        f"The DDSC Team"
    )

    try:
        send_mail(
            subject,
            message,
            "noreply@ddsc.io",  # From email
            [user.email],       # To email
            fail_silently=False,
        )
        reminder.status = Reminder.ReminderStatusChoice.SENT
        reminder.save()
        return f"Successfully sent reminder {reminder_id} to {user.email}"
    except Exception as e:
        reminder.status = Reminder.ReminderStatusChoice.ERROR
        reminder.save()
        return f"Error sending reminder {reminder_id}: {e}"

