from __future__ import absolute_import, unicode_literals
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from celery.utils.log import get_task_logger
from django.utils.translation import gettext_lazy as _
from ddsc_web.celery import celery_app
from .models import User
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from pathlib import Path
from shared.emails import create_email_with_images

from .slack import post_greeting

logger = get_task_logger(__name__)


@celery_app.task(name="send_activation_email")
def send_activation_email(domain, scheme, pk):
    mail_subject = _("Aktiver din konto")
    user = User.objects.get(pk=pk)
    message = render_to_string(
        "auth/activation_email.html",
        {
            "user": user,
            "protocol": scheme,
            "domain": domain,
            "uid": urlsafe_base64_encode(force_bytes(pk)),
            "token": account_activation_token.make_token(user),
        },
    )
    user.email_user(mail_subject, message)
    logger.info(f"Activation email sent to {user}")


@celery_app.task(name="send_password_reset_email")
def send_mail(
    subject_template_name,
    email_template_name,
    context,
    from_email,
    to_email,
    html_email_template_name,
):
    context["user"] = User.objects.get(pk=context["user"])

    PasswordResetForm.send_mail(
        None,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name,
    )


@celery_app.task(name="onboarding_welcome_sequence")
def onboarding_welcome_sequence(user_id: int):
    user = User.objects.get(pk=user_id)
    _send_welcome_email(user)
    _notify_slack(user)


def _send_welcome_email(user: User) -> None:
    sender = getattr(settings, "WELCOME_EMAIL_SENDER", None)
    if not sender:
        logger.info("welcome_email_sender_missing")
        return
    html = render_to_string(
        "users/emails/welcome.html",
        {
            "full_name": user.get_full_name() or user.email,
            "slack_link": getattr(settings, "SLACK_INVITATION_LINK", "https://ddsc.dk/slack"),
        },
    )
    logo_path = Path(settings.STATICFILES_DIRS[0]) / "ddsc-logo-base.png"
    email = create_email_with_images(
        subject=_("Velkommen til DDSC"),
        text_content=None,
        html_content=html,
        sender=sender,
        recipient=user.email,
        image_paths=[logo_path] if logo_path.exists() else [],
    )
    email.send()
    logger.info("welcome_email_sent", extra={"user": user.email})


def _notify_slack(user: User) -> None:
    webhook = getattr(settings, "SLACK_WEBHOOK_URL", None)
    channel = getattr(settings, "SLACK_WELCOME_CHANNEL", "#ddsc-welcome")
    if not webhook:
        logger.info("slack_webhook_missing")
        return
    post_greeting(webhook, channel, full_name=user.get_full_name(), email=user.email)
