from django.views.generic import TemplateView

from news.forms import NewsletterSignupForm
from stats.collectors import record_page_view, record_user_activity


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("newsletter_form", NewsletterSignupForm())
        return context

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        session_key = request.session.session_key or request.session.cycle_key()
        record_page_view(
            path=request.path,
            session_key=session_key,
            user=request.user,
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:256],
        )
        record_user_activity(user=request.user, action="view_home")
        return response


__all__ = ["HomePageView"]
