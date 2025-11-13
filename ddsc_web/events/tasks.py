from pathlib import Path

from celery.utils.log import get_task_logger
from ddsc_web.celery import celery_app
from django.contrib.auth import get_user_model
from django.core.files.temp import NamedTemporaryFile
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from shared.emails import create_email_with_images

from .models import EventRegistration

User = get_user_model()

logger = get_task_logger(__name__)


# TODO: This task now works, but has alot of I/O operations I am not sure we need them all.
# There might be a much better way to just download the file directly from S3 and point to the path.
# However, one upside of this method is, that the tempfiles are destroyed as soon as the file is closed.
# We should implement some context manager for this task to clean up the files if we hit an error.
@celery_app.task(name="send_ticket_mail")
def send_ticket_mail(user_id, event_registration_id):
    registration = EventRegistration.objects.get(pk=event_registration_id)
    user = User.objects.get(pk=user_id)
    mail_subject = f"{_('Din billet til')} {registration.event.title}"

    qr_code_temp = NamedTemporaryFile()
    event_image_temp = NamedTemporaryFile()

    write_qr_code_to_tempfile(qr_code_temp, registration)
    write_event_image_to_tempfile(event_image_temp, registration)

    html_message = render_to_string(
        "events/ticket_email.html",
        {
            "registration": registration,
            "qr_code_name": Path(qr_code_temp.name).name,
            "event_image_name": Path(event_image_temp.name).name,
        },
    )
    email = create_email_with_images(
        subject=mail_subject,
        text_content=None,
        html_content=html_message,
        sender=_("DDSC event billet"),
        recipient=user.email,
        image_paths=[Path(qr_code_temp.name), Path(event_image_temp.name)],
    )
    email.send()
    qr_code_temp.close()
    event_image_temp.close()


def write_qr_code_to_tempfile(file, registration: EventRegistration):
    qr_code_content = registration.qr_code.read()
    file.write(qr_code_content)
    file.flush()
    return True


def write_event_image_to_tempfile(file, registration: EventRegistration):
    event_image_content = registration.event.get_first_image().image.read()
    file.write(event_image_content)
    file.flush()
    return True
