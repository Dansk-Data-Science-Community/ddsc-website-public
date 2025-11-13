from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .models import NewsSubscriber


class NewsletterSignupTests(TestCase):
    @patch("ddsc_web.news.views.upsert_mailerlite_subscriber.delay")
    @patch("ddsc_web.news.views.send_mail")
    def test_signup_persists_preferences_and_sends_confirmation(
        self,
        mock_send_mail,
        mock_task_delay,
    ):
        payload = {
            "email": "test@example.com",
            "full_name": "Test User",
            "frequency": NewsSubscriber.NewsletterFrequency.MONTHLY,
            "interests": ["meetups", "talks"],
            "consent_gdpr": True,
        }
        response = self.client.post(reverse("news:newsletter_signup"), data=payload)
        self.assertRedirects(response, reverse("news:newsletter_thanks"))

        subscriber = NewsSubscriber.objects.get(email="test@example.com")
        self.assertEqual(subscriber.frequency, NewsSubscriber.NewsletterFrequency.MONTHLY)
        self.assertListEqual(subscriber.interests, ["meetups", "talks"])
        mock_send_mail.assert_called_once()
        mock_task_delay.assert_called_once_with("test@example.com", "Test User")

    def test_consent_required(self):
        payload = {
            "email": "test@example.com",
            "full_name": "Test User",
            "frequency": NewsSubscriber.NewsletterFrequency.MONTHLY,
            "interests": ["meetups"],
        }
        response = self.client.post(reverse("news:newsletter_signup"), data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I agree to receive DDSC emails")
        self.assertFalse(NewsSubscriber.objects.filter(email="test@example.com").exists())
