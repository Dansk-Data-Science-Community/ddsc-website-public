from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import delete_mailerlite_subscriber, upsert_mailerlite_subscriber
from .models import NewsSubscriber


@receiver(post_save, sender=NewsSubscriber)
def sync_mailerlite_subscribtion(sender, instance, created, **kwargs):
    if instance.allow_newsletters:
        upsert_mailerlite_subscriber.delay(
            instance.user.email, instance.user.get_full_name()
        )
    else:
        delete_mailerlite_subscriber.delay(instance.user.email)
