import qrcode
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from image_cropping import ImageCropField, ImageRatioField
from shared.models import AbstractAddress
from tinymce.models import HTMLField
from django.conf import settings
from ddsc_web.settings.custom_storages import PrivateMediaStorage

from .fields import TokenField
from .managers import ComingEvents
from .signing import sign_ticket_data
from .validators import validate_image_order, validate_maximum_attendees

UPLOAD_FOLDER = "images/%Y/%m/%d/"
QR_CODE_UPLOAD_FOLDER = "event/registrations/%Y/%m/%d/"

User = get_user_model()


class Event(models.Model):
    class SignupTypeChoice(models.TextChoices):
        DDSC_SIGNUP = "DDSC", _("DDSC tilmelding")
        EXTERNAL_SIGNUP = "External", _("Ekstern tilmelding")

    class Meta:
        ordering = ["-start_datetime"]
        default_manager_name = "objects"

    title = models.CharField(
        max_length=200,
        help_text=_("Titel på eventet"),
        unique=True,
    )
    slug = models.SlugField(max_length=200, blank=True)
    signup_link = models.URLField(
        help_text=_(
            "Link til event på en ekstern side, hvis det findes. fx. billetto.dk"
        ),
        blank=True,
        null=True,
    )
    draft = models.BooleanField(default=False)
    signup_type = models.CharField(
        help_text=_("Hvilken tilmeldingstype skal eventet have?"),
        blank=False,
        null=False,
        max_length=25,
        choices=SignupTypeChoice.choices,
    )
    location = models.CharField(
        max_length=200,
        help_text=_("Navn på stedet hvor eventet afholdes"),
    )
    start_datetime = models.DateTimeField(
        help_text=_("Start dato og tidspunkt for eventet")
    )
    end_datetime = models.DateTimeField(
        help_text=_("Slut dato og tidspunkt for eventet")
    )
    summary = models.CharField(max_length=200)
    description = HTMLField(
        help_text=_("Beskrivelse af indholdet i eventet (RTF)"),
    )
    created = models.DateTimeField(auto_now_add=True)
    registrations = models.ManyToManyField(
        User,
        through="EventRegistration",
    )
    maximum_attendees = models.PositiveIntegerField(
        validators=[validate_maximum_attendees]
    )
    registration_terms = models.ForeignKey(
        "RegistrationTerms",
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
        related_name="events",
    )
    coming_events = ComingEvents()
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse("events:register", args=[self.id, self.slug])

    def get_share_url(self):
        return reverse("events:share", args=[self.id, self.slug])

    def get_first_image(self):
        return self.images.first()

    def has_available_tickets(self):
        return self.attendees.all().count() < self.maximum_attendees

    def is_sold_out(self):
        return self.attendees.all().count() >= self.maximum_attendees

    def save(self, *args, **kwargs):
        # if not self.slug:
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class EventImage(models.Model):
    class Meta:
        ordering = ["order"]

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = ImageCropField(
        upload_to=UPLOAD_FOLDER,
        help_text=_(
            "Billed der viser eventet. Vil blive vist på siden sammen med titlen"
        ),
    )
    cropping_detail = ImageRatioField("image", "1850x900", size_warning=True)
    cropping_list = ImageRatioField("image", "900x600", size_warning=True)
    order = models.PositiveIntegerField(validators=[validate_image_order], default=1)


class Address(AbstractAddress):

    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
        related_name="address",
    )


class EventRegistration(models.Model):
    class StatusChoice(models.TextChoices):
        PENDING = "Pending", _("Pending")
        ATTENDED = "Attended", _("Attended")

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="attendees",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="event_registrations",
    )
    created = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(
        upload_to=QR_CODE_UPLOAD_FOLDER,
        help_text=_("QR kode for tilmeldingen."),
        storage=PrivateMediaStorage(),
    )
    slug = models.SlugField(max_length=200, blank=True)
    token = TokenField()
    status = models.CharField(
        max_length=25,
        choices=StatusChoice.choices,
        default="Pending",
    )

    class Meta:
        unique_together = [["event", "user"]]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.event.title} {self.user.first_name}")
        self.generate_qrcode()
        super(EventRegistration, self).save(*args, **kwargs)

    def generate_qrcode(self):

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        ticket_data = {
            "event_id": self.event.pk,
            "token": self.token,
        }
        signed_data = sign_ticket_data(ticket_data)
        qr.add_data(settings.CONSUME_TICKET_ENDPOINT + signed_data)
        qr.make(fit=True)

        filename = "event_registration.png"

        temp_image_file = NamedTemporaryFile()

        img = qr.make_image()
        img.save(temp_image_file.name)

        with open(temp_image_file.name, "rb") as reopen:
            django_file = File(reopen)
            self.qr_code.save(filename, django_file, save=False)

    def __str__(self):
        return f"Registration: {self.user} - {self.event} - {self.created.date()}"


class RegistrationTerms(models.Model):
    class TermsType(models.TextChoices):
        CUSTOM = "Custom", _("Custom")
        STANDARD = "Standard", _("Standard")

    terms = HTMLField(
        help_text=_("Vilkår for tilmelding til eventet (RTF)"),
    )
    type = models.CharField(
        max_length=25,
        choices=TermsType.choices,
        default="Standard",
    )
    name = models.CharField(max_length=200, default="DDSC Standard")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
