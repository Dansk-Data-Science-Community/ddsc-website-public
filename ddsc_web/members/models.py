from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from shared.models import AbstractAddress

User = get_user_model()


class Member(models.Model):
    class TitleChoice(models.TextChoices):
        FORMAND = "Formand", _("Formand")
        NÆSTFORMAND = "Næstformand", _("Næstformand")
        ØVRIGT_MEDLEM = "Øvrigt medlem", _("Øvrigt medlem")
        BESTYRELSESMEDLEM = "Bestyrelsesmedlem", _("Bestyrelsesmedlem")
        SUPPLEANT = "Suppleant", _("Suppleant")

    class StatusChoice(models.TextChoices):
        PENDING = "Afventer godkendelse", _("Afventer godkendelse")
        ACTIVE = "Aktiv", _("Aktiv")

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        help_text=_("Medlem af foreningen DDSC"),
        related_name="member",
        error_messages={
            "unique": _("Du er allerede medlem af foreningen."),
        },
    )
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(
        max_length=25,
        blank=True,
        choices=TitleChoice.choices,
        default=TitleChoice.ØVRIGT_MEDLEM,
    )
    job_title = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name=_("Titel"),
        help_text=_(
            "Din stillingsbetegnelse, fx. Data Analyst, Data Scientist, Data Engineer etc."
        ),
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoice.choices,
        default=StatusChoice.ACTIVE,
        help_text=_("Administrations felt til skift i medlemmers aktuelle status"),
    )
    slug = models.SlugField(max_length=200, blank=True)

    # Privacy Settings
    is_public = models.BooleanField(default=False, help_text=_("Make profile visible in the member directory"))
    show_email = models.BooleanField(default=False, help_text=_("Show email address on public profile"))
    show_job_title = models.BooleanField(default=True, help_text=_("Show job title on public profile"))
    show_address = models.BooleanField(default=False, help_text=_("Show address on public profile"))

    # Searchable Attributes
    bio = models.TextField(blank=True, null=True, help_text=_("A short biography about yourself"))
    skills = models.CharField(max_length=500, blank=True, null=True, help_text=_("Comma-separated list of skills (e.g., Python, Django, Data Science)"))
    linkedin_url = models.URLField(blank=True, null=True, verbose_name=_("LinkedIn Profile URL"))
    github_url = models.URLField(blank=True, null=True, verbose_name=_("GitHub Profile URL"))

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.get_full_name())
        super().save(*args, **kwargs)


class Address(AbstractAddress):
    member = models.OneToOneField(
        Member,
        on_delete=models.CASCADE,
        help_text=_("Medlemsadresse til kontingent betaling etc."),
        related_name="address",
    )
