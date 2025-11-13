from pathlib import Path

from celery.utils.log import get_task_logger
from ddsc_web.celery import celery_app
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from shared.emails import create_email_with_images
from django.conf import settings

User = get_user_model()

logger = get_task_logger(__name__)


@celery_app.task(name="send_welcome_email")
def send_welcome_email(user_id):
    user = User.objects.get(pk=user_id)
    mail_subject = _("Velkommen til Dansk Data Science Community")

    html_message = render_to_string(
        "members/welcome_email.html",
        {
            "full_name": user.get_full_name(),
            "logo": "ddsc-logo-base.png",
            "slack_invite": settings.SLACK_INVITATION_LINK,
        },
    )
    email = create_email_with_images(
        subject=mail_subject,
        text_content=None,
        html_content=html_message,
        sender=_("Dansk Data Science Community"),
        recipient=user.email,
        image_paths=[Path(settings.STATICFILES_DIRS[0]) / "ddsc-logo-base.png"],
    )
    email.send()
