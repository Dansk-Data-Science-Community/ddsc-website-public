from django.db import models
from django.utils.translation import gettext_lazy as _
from events.models import Event # Import the existing Event model
from tinymce.models import HTMLField # For rich text description

class RecurringMeetup(models.Model):
    class DayOfWeek(models.IntegerChoices):
        MONDAY = 0, _("Monday")
        TUESDAY = 1, _("Tuesday")
        WEDNESDAY = 2, _("Wednesday")
        THURSDAY = 3, _("Thursday")
        FRIDAY = 4, _("Friday")
        SATURDAY = 5, _("Saturday")
        SUNDAY = 6, _("Sunday")

    class Frequency(models.TextChoices):
        WEEKLY = "WEEKLY", _("Weekly")
        BI_WEEKLY = "BI_WEEKLY", _("Bi-Weekly")
        MONTHLY = "MONTHLY", _("Monthly")

    title = models.CharField(max_length=200, help_text=_("Title of the recurring meetup"))
    description = HTMLField(help_text=_("Description of the meetup (RTF)"))
    location = models.CharField(max_length=200, help_text=_("Location of the meetup"))
    start_time = models.TimeField(help_text=_("Time of day the meetup starts"))
    day_of_week = models.IntegerField(choices=DayOfWeek.choices, help_text=_("Day of the week the meetup occurs"))
    frequency = models.CharField(max_length=20, choices=Frequency.choices, default=Frequency.WEEKLY)
    active = models.BooleanField(default=True, help_text=_("Whether this recurring meetup is active"))
    last_generated_date = models.DateField(null=True, blank=True, help_text=_("Last date an event was generated for this meetup"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_day_of_week_display()}s at {self.start_time})"

    class Meta:
        verbose_name = _("Recurring Meetup")
        verbose_name_plural = _("Recurring Meetups")
        ordering = ["day_of_week", "start_time"]
