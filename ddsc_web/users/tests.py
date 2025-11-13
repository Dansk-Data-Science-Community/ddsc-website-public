from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from unittest.mock import patch

from .tokens import account_activation_token

User = get_user_model()


class ActivationFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="new@ddsc.io",
            password="test123",
            first_name="New",
            last_name="Member",
        )

    @patch("ddsc_web.users.views.onboarding_welcome_sequence.delay")
    def test_activation_triggers_onboarding_sequence(self, mock_delay):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)

        response = self.client.get(reverse("users:activate", args=[uid, token]))

        self.assertRedirects(response, reverse("users:dashboard"))
        mock_delay.assert_called_once_with(self.user.pk)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)
