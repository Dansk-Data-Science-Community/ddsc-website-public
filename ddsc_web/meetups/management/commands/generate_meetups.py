from django.core.management.base import BaseCommand
from meetups.tasks import generate_meetup_events

class Command(BaseCommand):
    help = 'Generates upcoming meetup events based on recurring meetup patterns.'

    def handle(self, *args, **options):
        self.stdout.write("Starting generation of meetup events...")
        generate_meetup_events.delay() # Use .delay() to run as a Celery task
        self.stdout.write(self.style.SUCCESS("Meetup event generation task dispatched."))
