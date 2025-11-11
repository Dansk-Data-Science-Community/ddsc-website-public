from email.mime.image import MIMEImage
from pathlib import Path

from django.core.mail import EmailMultiAlternatives


# the function for sending an email
def create_email_with_images(
    subject: str,
    text_content: str,
    image_paths: Path,
    html_content=None,
    sender=None,
    recipient=None,
):
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=sender,
        to=recipient if isinstance(recipient, list) else [recipient],
    )
    email.attach_alternative(html_content, "text/html")
    email.content_subtype = "html"  # set the primary content to be text/html
    email.mixed_subtype = (
        "related"  # it is an important part that ensures embedding of an image
    )
    for image_path in image_paths:
        add_image(email, image_path)

    return email


def add_image(email: EmailMultiAlternatives, image_path: Path):
    with open(image_path, mode="rb") as f:
        image = MIMEImage(f.read())
        email.attach(image)
        image.add_header("Content-ID", f"<{image_path.name}>")
