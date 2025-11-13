from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator

User = get_user_model()


class NewsSubscriber(models.Model):
    EVENT_TYPE_CHOICES = [
        ('all', 'All Events'),
        ('meetup', 'Meetups'),
        ('workshop', 'Workshops'),
        ('conference', 'Conferences'),
        ('webinar', 'Webinars'),
    ]

    FREQUENCY_CHOICES = [
        ('immediate', 'Immediate (as events are posted)'),
        ('daily', 'Daily Digest'),
        ('weekly', 'Weekly Digest'),
        ('monthly', 'Monthly Digest'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
        validators=[EmailValidator()],
        help_text="Email address for newsletter subscription"
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text="Subscriber's name"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    allow_newsletters = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(
        default=False,
        help_text="Whether the subscriber has confirmed their email"
    )
    confirmation_token = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text="Token for email confirmation"
    )
    event_types = models.CharField(
        max_length=50,
        choices=EVENT_TYPE_CHOICES,
        default='all',
        help_text="Types of events to receive notifications about"
    )
    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default='weekly',
        help_text="How often to receive newsletters"
    )

    class Meta:
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"
        ordering = ['-created']

    def __str__(self):
        return f"{self.email} ({self.get_frequency_display()})"

    @property
    def subscriber_count(self):
        return self.objects.all().count()

    @classmethod
    def get_mailing_list(cls):
        return cls.objects.filter(allow_newsletters=True, is_confirmed=True)

    @classmethod
    def get_active_subscribers(cls):
        """Get all active and confirmed subscribers"""
        return cls.objects.filter(allow_newsletters=True, is_confirmed=True)
