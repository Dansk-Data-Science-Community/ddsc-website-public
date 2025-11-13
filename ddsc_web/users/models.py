from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from image_cropping import ImageCropField, ImageRatioField

from .fields import LowercaseEmailField
from .managers import UserManager

UPLOAD_FOLDER = "profile_images/%Y/%m/%d/"


class User(AbstractBaseUser, PermissionsMixin):
    email = LowercaseEmailField(
        verbose_name=_("email address"),
        unique=True,
        error_messages={
            "unique": _("bruger er allerede oprettet med denne email adresse"),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Bestemmer om en bruger kan logge ind som administrator"),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Bestemmer om en bruger er aktiv eller ej"),
    )
    is_verified = models.BooleanField(
        _("verified"),
        default=False,
        help_text=_("Bestemmer om brugeren har bekræftet validiteten af sin email"),
    )
    date_joined = models.DateTimeField(_("Oprettet dato"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    @cached_property
    def is_member(self):
        return hasattr(self, "member")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_profile_completion_percentage(self):
        """
        Calculate profile completion percentage based on key fields.
        Returns an integer between 0 and 100.
        """
        completion = 0
        
        # First name: 25%
        if self.first_name and self.first_name.strip():
            completion += 25
        
        # Last name: 25%
        if self.last_name and self.last_name.strip():
            completion += 25
        
        # Birthdate: 25%
        if hasattr(self, 'profile') and self.profile.birthdate:
            completion += 25
        
        # Profile image: 25%
        if hasattr(self, 'profile') and self.profile.has_image:
            completion += 25
        
        return completion

    class Meta:
        ordering = ["id"]
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email


class Profile(models.Model):
    """Users profile"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(
        null=True,
        blank=True,
        help_text=_("Fødselsdato"),
        verbose_name=_("Fødselsdato"),
    )

    @property
    def age(self):
        return timezone.now().year - self.birthdate.year if self.birthdate else None

    @property
    def has_image(self):
        try:
            if self.image.image:
                return True
            else:
                return False
        except ObjectDoesNotExist:
            return False

    def __str__(self):
        return f"{self.user.get_full_name()}"


# TODO: måske det er på tide at prøve et andet modul til image cropping.
# https://github.com/ninapavlich/django-imagekit-cropper.
# TODO: til produktion bør der implementeres Spaces med privat storage af billeder.
# https://testdriven.io/blog/django-digitalocean-spaces/#private-media-files
class ProfileImage(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name="image",
    )
    image = ImageCropField(
        upload_to=UPLOAD_FOLDER,
        help_text=_("Profilbillede der vises offentligt"),
        null=True,
        blank=True,
    )
    cropping_detail = ImageRatioField("image", "300x300", size_warning=True)
    cropping_list = ImageRatioField("image", "600x600", size_warning=True)
    cropping_member = ImageRatioField("image", "150x150")
