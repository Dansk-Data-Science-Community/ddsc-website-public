from __future__ import absolute_import, unicode_literals
from celery.utils.log import get_task_logger
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from ddsc_web.celery import celery_app
from .mailerlite import (
    get_newsletter_subscriber_id,
    forget_newsletter_subscriber,
    subscribe_to_newsletter,
)

MAILERLITE_API_URL = settings.MAILERLITE_API_URL
MAILERLITE_API_KEY = settings.MAILERLITE_API_KEY


logger = get_task_logger(__name__)


@celery_app.task(name="delete_mailerlite_subscriber")
def delete_mailerlite_subscriber(email: str):
    subscriber_id = get_newsletter_subscriber_id(
        email,
        api_url=MAILERLITE_API_URL,
        api_key=MAILERLITE_API_KEY,
    )
    success = forget_newsletter_subscriber(
        subscriber_id,
        api_url=MAILERLITE_API_URL,
        api_key=MAILERLITE_API_KEY,
    )
    if success:
        logger.info(f"Subscriber was succesfully deleted")
    else:
        logger.error(f"Subscriber was not found")


@celery_app.task(name="upsert_mailerlite_subscriber")
def upsert_mailerlite_subscriber(
    email: str,
    name: str,
):
    response = subscribe_to_newsletter(
        email,
        name,
        api_url=MAILERLITE_API_URL,
        api_key=MAILERLITE_API_KEY,
    )
    if response.status_code == 200:
        logger.info(f"Email '{email}' has previously subscribed.")
    elif response.status_code == 201:
        logger.info(f"Email '{email}' was subscribed succesfully.")
    else:
        response.raise_for_status()
