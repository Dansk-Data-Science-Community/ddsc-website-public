from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Adds the eventeditor permissions group"

    def handle(self, *args, **options):
        permissions_list = Permission.objects.filter(
            codename__in=[
                "add_event",
                "change_event",
                "view_event",
                "delete_event",
                "view_event_registration",
            ]
        )
        event_group, created = Group.objects.get_or_create(name="Eventeditor")
        if created:

            event_group.permissions.add(*permissions_list)
            event_group.save()
            self.stdout.write(
                self.style.SUCCESS("Successfully added 'Eventeditor' permissions group")
            )
        # Create TicketConsumer group
        consumer_permissions_list = Permission.objects.filter(
            codename__in=["change_eventregistration"]
        )
        consumer_group, created = Group.objects.get_or_create(name="TicketConsumer")
        if created:
            consumer_group.permissions.add(*consumer_permissions_list)
            consumer_group.save()
            self.stdout.write(
                self.style.SUCCESS(
                    "Successfully added 'TicketConsumer' permissions group"
                )
            )
