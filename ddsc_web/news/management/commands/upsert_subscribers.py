from django.core.management.base import BaseCommand
from django.conf import settings

from news.mailerlite import (
    subscribe_to_newsletter,
    get_subscribers_list,
    forget_newsletter_subscriber,
)
from news.models import NewsSubscriber


MAILERLITE_API_URL = settings.MAILERLITE_API_URL
MAILERLITE_API_KEY = settings.MAILERLITE_API_KEY


def get_local_subscribers():
    subscribers = NewsSubscriber.get_mailing_list()
    return [
        {"email": subscriber.user.email, "name": subscriber.user.get_full_name()}
        for subscriber in subscribers
    ]


def get_new_subscribers_list(
    local_mailer_list: list[dict[str, str]],
    remote_mailer_list: list[dict[str, str]],
) -> list[dict[str, str]]:
    remote_emails = {entry["email"] for entry in remote_mailer_list}
    return [entry for entry in local_mailer_list if entry["email"] not in remote_emails]


def get_unsubscribed_list(
    local_mailer_list: list[dict[str, str]],
    remote_mailer_list: list[dict[str, str]],
) -> list[dict[str, str | int]]:
    local_emails = {entry["email"] for entry in local_mailer_list}
    return [entry for entry in remote_mailer_list if entry["email"] not in local_emails]


class Command(BaseCommand):
    help = "Synchronize newsletter subscribers with MailerLite"

    def handle(self, *args, **kwargs):
        local_subscribers = get_local_subscribers()
        mailerlite_subscribers = get_subscribers_list(
            api_url=MAILERLITE_API_URL,
            api_key=MAILERLITE_API_KEY,
        )
        new_subscribers = get_new_subscribers_list(
            local_mailer_list=local_subscribers,
            remote_mailer_list=mailerlite_subscribers,
        )
        unsubscribed = get_unsubscribed_list(
            local_mailer_list=local_subscribers,
            remote_mailer_list=mailerlite_subscribers,
        )
        self.__upsert_subscribers(new_subscribers)
        self.__delete_subscribers(unsubscribed)

    def __upsert_subscribers(self, new_subscribers: list[dict[str, str]]):
        for subscriber in new_subscribers:
            email = subscriber["email"]
            name = subscriber["name"]
            response = subscribe_to_newsletter(
                email,
                name,
                api_key=MAILERLITE_API_KEY,
                api_url=MAILERLITE_API_URL,
            )
            if response.status_code == 200:
                self.stdout.write(
                    self.style.WARNING(f"Email '{email}' has allready subscribed.")
                )
            elif response.status_code == 201:
                self.stdout.write(
                    self.style.SUCCESS(f"Email '{email}' was subscribed succesfully.")
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f"Failed to subscribe {email}: {response.content}")
                )

    def __delete_subscribers(self, unsubscribers: list[dict[str, str | int]]):
        for unsubscriber in unsubscribers:

            success = forget_newsletter_subscriber(
                subscriber_id=unsubscriber["id"],
                api_url=MAILERLITE_API_URL,
                api_key=MAILERLITE_API_KEY,
            )
            if not success:
                self.stdout.write(
                    self.style.ERROR(
                        f"Failed to unsubscribe email: '{unsubscriber['email']}'."
                    )
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Email '{unsubscriber['email']}' was unsubscribed succesfully."
                )
            )
