from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class NewsSubscriber(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True)
    allow_newsletters = models.BooleanField(default=True)

    @property
    def subscriber_count(self):
        return self.objects.all().count()

    @classmethod
    def get_mailing_list(self):
        return self.objects.filter(allow_newsletters=True)
