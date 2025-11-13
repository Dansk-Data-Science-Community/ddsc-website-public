from django.db import models
from django.utils import timezone


class ComingEvents(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(end_datetime__gt=timezone.now())
