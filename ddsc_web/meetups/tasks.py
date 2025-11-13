from celery import shared_task
from django.utils import timezone
from datetime import timedelta, date
from events.models import Event
from .models import RecurringMeetup

@shared_task
def generate_meetup_events():
    """
    Celery task to generate Event instances from RecurringMeetup patterns.
    """
    today = timezone.localdate()
    # Look ahead for 2 weeks to generate events
    two_weeks_from_now = today + timedelta(weeks=2)

    active_meetups = RecurringMeetup.objects.filter(active=True)

    for meetup in active_meetups:
        # Determine the next occurrence date based on last_generated_date or today
        start_date_for_generation = meetup.last_generated_date if meetup.last_generated_date else today

        # Iterate through dates to find occurrences
        current_date = start_date_for_generation
        while current_date <= two_weeks_from_now:
            if current_date.weekday() == meetup.day_of_week:
                # Check if an event for this specific occurrence already exists
                event_start_datetime = timezone.make_aware(
                    timezone.datetime.combine(current_date, meetup.start_time)
                )
                
                # Assuming meetups are 1 hour long for simplicity
                event_end_datetime = event_start_datetime + timedelta(hours=1)

                # Check for existing event to prevent duplicates
                if not Event.objects.filter(
                    title=meetup.title,
                    start_datetime=event_start_datetime,
                    location=meetup.location
                ).exists():
                    # Create the Event
                    Event.objects.create(
                        title=meetup.title,
                        slug=meetup.title.lower().replace(" ", "-"), # Simple slug generation
                        signup_type="DDSC", # Assuming DDSC signup for meetups
                        location=meetup.location,
                        start_datetime=event_start_datetime,
                        end_datetime=event_end_datetime,
                        summary=meetup.description, # Using description as summary
                        description=meetup.description,
                        maximum_attendees=100, # Default to 100 attendees
                        draft=False,
                    )
                    print(f"Generated event for {meetup.title} on {current_date}")

            # Move to the next day
            current_date += timedelta(days=1)
        
        # Update last_generated_date to today to avoid re-generating old events
        meetup.last_generated_date = today
        meetup.save()
