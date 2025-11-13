from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .tasks import (
    delete_mailerlite_subscriber,
    upsert_mailerlite_subscriber,
    send_confirmation_email,
    sync_subscriber_to_mailerlite,
)
from .models import NewsSubscriber


@receiver(post_save, sender=NewsSubscriber)
def sync_mailerlite_subscription(sender, instance, created, **kwargs):
    """
    Sync newsletter subscriptions with MailerLite.
    Only sync confirmed subscribers.
    """
    # Don't sync on initial creation - wait for email confirmation
    if created:
        return

    # Only sync if subscriber is confirmed
    if instance.is_confirmed and instance.allow_newsletters:
        sync_subscriber_to_mailerlite.delay(instance.id)
    elif not instance.allow_newsletters:
        # Remove from MailerLite if unsubscribed
        if instance.email:
            delete_mailerlite_subscriber.delay(instance.email)
        elif instance.user:
            delete_mailerlite_subscriber.delay(instance.user.email)


@receiver(post_delete, sender=NewsSubscriber)
def delete_mailerlite_subscriber_on_delete(sender, instance, **kwargs):
    """
    Automatically delete a MailerLite subscriber when a NewsSubscriber is deleted.
    """
    if instance.email:
        delete_mailerlite_subscriber.delay(instance.email)
    elif instance.user:
        delete_mailerlite_subscriber.delay(instance.user.email)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_subscriber_for_new_user(sender, instance, created, **kwargs):
    """
    Optionally create a newsletter subscriber when a new User registers.
    This can be enabled/disabled based on requirements.
    """
    if created and instance.email:
        # Check if subscriber already exists
        subscriber = NewsSubscriber.objects.filter(email=instance.email).first()
        if not subscriber:
            from .utils import generate_confirmation_token
            # Create subscriber linked to user
            subscriber = NewsSubscriber.objects.create(
                user=instance,
                email=instance.email,
                name=instance.get_full_name() if hasattr(instance, 'get_full_name') else '',
                confirmation_token=generate_confirmation_token(),
                is_confirmed=False,
            )
            # Note: You can uncomment below to auto-send confirmation emails to new users
            # send_confirmation_email.delay(subscriber.id)
