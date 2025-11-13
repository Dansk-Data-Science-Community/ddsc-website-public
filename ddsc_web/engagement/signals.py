"""Signal handlers for engagement tracking"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ParticipationLevel

@receiver(post_save, sender=User)
def create_participation_level(sender, instance, created, **kwargs):
    """Auto-create participation level for new users"""
    if created:
        ParticipationLevel.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_participation_level(sender, instance, **kwargs):
    """Auto-save participation level"""
    if hasattr(instance, 'participation_level'):
        instance.participation_level.save()
