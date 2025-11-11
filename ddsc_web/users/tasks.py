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
