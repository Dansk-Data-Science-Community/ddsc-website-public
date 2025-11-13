from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, TemplateView
from django.core.mail import send_mail

from .forms import NewsletterSignupForm
from .models import NewsSubscriber
from .tasks import upsert_mailerlite_subscriber


class NewsletterSignupView(FormView):
    template_name = "news/newsletter_landing.html"
    form_class = NewsletterSignupForm
    success_url = reverse_lazy("news:newsletter_thanks")

    def form_valid(self, form):
        subscriber = form.save()
        self._enqueue_mailerlite(subscriber)
        self._send_confirmation_email(subscriber)
        if subscriber.email:
            self.request.session["newsletter_email"] = subscriber.email
        messages.success(
            self.request,
            _("Thanks! Please confirm your subscription via the email we just sent."),
        )
        return super().form_valid(form)

    def _enqueue_mailerlite(self, subscriber: NewsSubscriber) -> None:
        if not subscriber.email:
            return
        name = subscriber.full_name or (subscriber.user.get_full_name() if subscriber.user else "")
        upsert_mailerlite_subscriber.delay(subscriber.email, name)

    def _send_confirmation_email(self, subscriber: NewsSubscriber) -> None:
        if not subscriber.email:
            return
        confirm_url = self.request.build_absolute_uri(
            reverse("news:newsletter_confirm", args=[subscriber.confirm_token])
        )
        unsubscribe_url = self.request.build_absolute_uri(
            reverse("news:newsletter_unsubscribe", args=[subscriber.confirm_token])
        )
        subject = _("Confirm your DDSC newsletter subscription")
        body = _(
            "Hi {name},\n\nThanks for joining the DDSC newsletter! "
            "Please confirm your subscription by visiting {confirm_url}.\n\n"
            "If you didn't request this, you can ignore this email or unsubscribe here: {unsubscribe_url}."
        ).format(
            name=subscriber.full_name or _("friend"),
            confirm_url=confirm_url,
            unsubscribe_url=unsubscribe_url,
        )
        sender = getattr(settings, "DEFAULT_FROM_EMAIL", "news@ddsc.dk")
        send_mail(subject, body, sender, [subscriber.email])


class NewsletterThankYouView(TemplateView):
    template_name = "news/subscribe_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subscriber_email"] = self.request.POST.get("email") or self.request.session.get(
            "newsletter_email"
        )
        return context


class NewsletterConfirmView(TemplateView):
    template_name = "news/newsletter_confirmed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subscriber = get_object_or_404(NewsSubscriber, confirm_token=kwargs["token"])
        subscriber.mark_confirmed()
        context["subscriber"] = subscriber
        return context


class NewsletterUnsubscribeView(TemplateView):
    template_name = "news/newsletter_unsubscribed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subscriber = get_object_or_404(NewsSubscriber, confirm_token=kwargs["token"])
        subscriber.unsubscribe()
        context["subscriber"] = subscriber
        return context
