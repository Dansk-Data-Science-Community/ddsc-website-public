from __future__ import absolute_import, unicode_literals
from celery.utils.log import get_task_logger
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from ddsc_web.celery import celery_app
from .mailerlite import (
    get_newsletter_subscriber_id,
    forget_newsletter_subscriber,
    subscribe_to_newsletter,
)
from .models import NewsSubscriber
from .utils import (
    build_confirmation_url,
    build_unsubscribe_url,
    build_preferences_url,
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


@celery_app.task(name="send_confirmation_email")
def send_confirmation_email(subscriber_id: int):
    """
    Send a confirmation email to a new subscriber

    Args:
        subscriber_id: The ID of the NewsSubscriber
    """
    try:
        subscriber = NewsSubscriber.objects.get(id=subscriber_id)
    except NewsSubscriber.DoesNotExist:
        logger.error(f"Subscriber with ID {subscriber_id} not found")
        return

    if not subscriber.confirmation_token:
        logger.error(f"Subscriber {subscriber.email} has no confirmation token")
        return

    # Build URLs
    confirmation_url = build_confirmation_url(subscriber.confirmation_token)
    unsubscribe_url = build_unsubscribe_url(subscriber.confirmation_token)

    # Prepare context
    context = {
        'subscriber': subscriber,
        'confirmation_url': confirmation_url,
        'unsubscribe_url': unsubscribe_url,
    }

    # Render templates
    subject = _('Bekræft din tilmelding til DDSC Nyhedsbrev')
    text_content = render_to_string('news/emails/confirmation_email.txt', context)
    html_content = render_to_string('news/emails/confirmation_email.html', context)

    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@ddsc.io',
        to=[subscriber.email],
    )
    email.attach_alternative(html_content, "text/html")

    # Send email
    try:
        email.send()
        logger.info(f"Confirmation email sent to {subscriber.email}")
    except Exception as e:
        logger.error(f"Failed to send confirmation email to {subscriber.email}: {str(e)}")


@celery_app.task(name="send_welcome_email")
def send_welcome_email(subscriber_id: int):
    """
    Send a welcome email to a newly confirmed subscriber

    Args:
        subscriber_id: The ID of the NewsSubscriber
    """
    try:
        subscriber = NewsSubscriber.objects.get(id=subscriber_id)
    except NewsSubscriber.DoesNotExist:
        logger.error(f"Subscriber with ID {subscriber_id} not found")
        return

    if not subscriber.is_confirmed:
        logger.warning(f"Subscriber {subscriber.email} is not confirmed yet")
        return

    # Build URLs
    unsubscribe_url = build_unsubscribe_url(subscriber.confirmation_token)
    preferences_url = build_preferences_url(subscriber.confirmation_token)

    # Prepare context
    context = {
        'subscriber': subscriber,
        'unsubscribe_url': unsubscribe_url,
        'preferences_url': preferences_url,
    }

    # Render templates
    subject = _('Velkommen til DDSC Nyhedsbrev!')
    text_content = render_to_string('news/emails/welcome_email.txt', context)
    html_content = render_to_string('news/emails/welcome_email.html', context)

    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@ddsc.io',
        to=[subscriber.email],
    )
    email.attach_alternative(html_content, "text/html")

    # Send email
    try:
        email.send()
        logger.info(f"Welcome email sent to {subscriber.email}")
    except Exception as e:
        logger.error(f"Failed to send welcome email to {subscriber.email}: {str(e)}")


@celery_app.task(name="sync_subscriber_to_mailerlite")
def sync_subscriber_to_mailerlite(subscriber_id: int):
    """
    Sync a confirmed subscriber to MailerLite

    Args:
        subscriber_id: The ID of the NewsSubscriber
    """
    try:
        subscriber = NewsSubscriber.objects.get(id=subscriber_id)
    except NewsSubscriber.DoesNotExist:
        logger.error(f"Subscriber with ID {subscriber_id} not found")
        return

    if not subscriber.is_confirmed:
        logger.warning(f"Subscriber {subscriber.email} is not confirmed, skipping MailerLite sync")
        return

    # Sync to MailerLite
    upsert_mailerlite_subscriber(
        email=subscriber.email,
        name=subscriber.name or subscriber.email,
    )


@celery_app.task(name="send_unsubscribe_confirmation_email")
def send_unsubscribe_confirmation_email(subscriber_id: int):
    """
    Send a confirmation email when someone unsubscribes

    Args:
        subscriber_id: The ID of the NewsSubscriber
    """
    try:
        subscriber = NewsSubscriber.objects.get(id=subscriber_id)
    except NewsSubscriber.DoesNotExist:
        logger.error(f"Subscriber with ID {subscriber_id} not found")
        return

    # Build URLs
    from django.urls import reverse
    resubscribe_url = f"https://ddsc.io{reverse('news:newsletter_landing')}"

    # Prepare context
    context = {
        'subscriber': subscriber,
        'resubscribe_url': resubscribe_url,
    }

    # Render templates
    subject = _('Du er afmeldt DDSC Nyhedsbrev')
    text_content = render_to_string('news/emails/unsubscribe_confirmation.txt', context)
    html_content = render_to_string('news/emails/unsubscribe_confirmation.html', context)

    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@ddsc.io',
        to=[subscriber.email],
    )
    email.attach_alternative(html_content, "text/html")

    # Send email
    try:
        email.send()
        logger.info(f"Unsubscribe confirmation email sent to {subscriber.email}")
    except Exception as e:
        logger.error(f"Failed to send unsubscribe confirmation to {subscriber.email}: {str(e)}")
