from __future__ import annotations

import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class NewsSubscriber(models.Model):
    class NewsletterFrequency(models.TextChoices):
        WEEKLY = "weekly", _("Weekly Highlights")
        MONTHLY = "monthly", _("Monthly Roundup")
        EVENTS_ONLY = "events", _("Event Alerts Only")

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    allow_newsletters = models.BooleanField(default=True)
    frequency = models.CharField(
        max_length=20,
        choices=NewsletterFrequency.choices,
        default=NewsletterFrequency.WEEKLY,
    )
    interests = models.JSONField(default=list, blank=True)
    consent_timestamp = models.DateTimeField(blank=True, null=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)
    confirm_token = models.UUIDField(default=uuid.uuid4, editable=False)

    @property
    def subscriber_count(self):
        return self.objects.all().count()

    @classmethod
    def get_mailing_list(self):
        return self.objects.filter(allow_newsletters=True)

    def mark_confirmed(self) -> None:
        self.confirmed_at = timezone.now()
        self.allow_newsletters = True
        self.unsubscribed_at = None
        self.save(update_fields=["confirmed_at", "allow_newsletters", "unsubscribed_at"])

    def unsubscribe(self) -> None:
        self.allow_newsletters = False
        self.unsubscribed_at = timezone.now()
        self.save(update_fields=["allow_newsletters", "unsubscribed_at"])

    def update_preferences(self, *, interests: list[str], frequency: str) -> None:
        self.interests = interests
        self.frequency = frequency
        self.save(update_fields=["interests", "frequency"])
