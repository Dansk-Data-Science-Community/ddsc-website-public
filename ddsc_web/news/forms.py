from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import NewsSubscriber

EVENT_TOPIC_CHOICES = [
    ("meetups", _("Meetups & Networking")),
    ("talks", _("Talks & Panels")),
    ("opensource", _("Open Source Projects")),
    ("jobs", _("Career & Jobs")),
    ("education", _("Workshops & Courses")),
]


class NewsletterSignupForm(forms.Form):
    email = forms.EmailField(label=_("Email address"))
    full_name = forms.CharField(
        label=_("Full name"),
        required=False,
        help_text=_("Optional, helps personalize updates."),
    )
    frequency = forms.ChoiceField(
        label=_("Preferred cadence"),
        choices=NewsSubscriber.NewsletterFrequency.choices,
        initial=NewsSubscriber.NewsletterFrequency.WEEKLY,
    )
    interests = forms.MultipleChoiceField(
        label=_("Topics you care about"),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=EVENT_TOPIC_CHOICES,
    )
    consent_gdpr = forms.BooleanField(
        label=_("I agree to receive DDSC emails and can unsubscribe anytime."),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ["email", "full_name"]:
            self.fields[name].widget.attrs.setdefault("class", "form-control")
        self.fields["frequency"].widget.attrs.setdefault("class", "form-select")

    def save(self) -> NewsSubscriber:
        cleaned = self.cleaned_data
        subscriber, _ = NewsSubscriber.objects.update_or_create(
            email=cleaned["email"],
            defaults={
                "full_name": cleaned["full_name"],
                "frequency": cleaned["frequency"],
                "allow_newsletters": True,
                "interests": cleaned["interests"],
            },
        )
        subscriber.consent_timestamp = subscriber.consent_timestamp or timezone.now()
        subscriber.save()
        return subscriber
