from django.views.generic import TemplateView

from news.forms import NewsletterSignupForm


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("newsletter_form", NewsletterSignupForm())
        return context


__all__ = ["HomePageView"]
