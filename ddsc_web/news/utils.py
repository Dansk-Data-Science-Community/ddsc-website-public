import secrets
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.conf import settings
from .models import NewsSubscriber


def generate_confirmation_token():
    """Generate a secure random token for email confirmation"""
    return secrets.token_urlsafe(48)


def get_subscriber_by_token(token):
    """
    Retrieve a subscriber by their confirmation token

    Args:
        token (str): The confirmation token

    Returns:
        NewsSubscriber or None: The subscriber if found, None otherwise
    """
    try:
        return NewsSubscriber.objects.get(confirmation_token=token)
    except NewsSubscriber.DoesNotExist:
        return None


def is_valid_email(email):
    """
    Validate an email address

    Args:
        email (str): Email address to validate

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def build_confirmation_url(token, request=None):
    """
    Build the full URL for email confirmation

    Args:
        token (str): The confirmation token
        request: Django request object (optional)

    Returns:
        str: Full URL for confirmation
    """
    path = reverse('news:confirm_subscription', kwargs={'token': token})

    if request:
        return request.build_absolute_uri(path)

    # Fallback to settings
    site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
    return f"{site_url}{path}"


def build_unsubscribe_url(token, request=None):
    """
    Build the full URL for unsubscribing

    Args:
        token (str): The subscriber's token
        request: Django request object (optional)

    Returns:
        str: Full URL for unsubscribe
    """
    path = reverse('news:unsubscribe_token', kwargs={'token': token})

    if request:
        return request.build_absolute_uri(path)

    # Fallback to settings
    site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
    return f"{site_url}{path}"


def build_preferences_url(token, request=None):
    """
    Build the full URL for managing preferences

    Args:
        token (str): The subscriber's token
        request: Django request object (optional)

    Returns:
        str: Full URL for preferences
    """
    path = reverse('news:update_preferences') + f'?token={token}'

    if request:
        return request.build_absolute_uri(path)

    # Fallback to settings
    site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
    return f"{site_url}{path}"


def get_subscriber_by_email(email):
    """
    Retrieve a subscriber by email address

    Args:
        email (str): Email address

    Returns:
        NewsSubscriber or None: The subscriber if found, None otherwise
    """
    try:
        return NewsSubscriber.objects.get(email=email.lower().strip())
    except NewsSubscriber.DoesNotExist:
        return None
