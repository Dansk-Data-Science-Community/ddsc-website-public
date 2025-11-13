from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def login_required_with_next(func):
    """
    Decorator for get and post methods. Checks if user is authenticated.
    Sets next url in session to requested event and redirects.
    """

    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            self.request.session["next"] = self.event.get_absolute_url()
            return redirect(settings.LOGIN_URL)
        else:
            return func(self, request, *args, **kwargs)

    return wrapper


def redirect_when_sold_out(func):
    """
    Decorator for get and post methods. Checks if event is sold out.
    Redirect if necessary.
    """

    def wrapper(self, request, *args, **kwargs):
        if self.event.is_sold_out():
            messages.error(
                self.request, _("Der er desværre ikke flere pladser til eventet")
            )
            return HttpResponseRedirect(reverse("events:event_list"))
        else:
            return func(self, request, *args, **kwargs)

    return wrapper
