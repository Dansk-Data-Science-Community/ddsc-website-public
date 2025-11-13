from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings


def redirect_members(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_member:
            return HttpResponseRedirect(reverse("users:dashboard"))
        else:
            return func(request, *args, **kwargs)

    return wrapper


def login_required_with_next(func):
    """
    Decorator for views that check whether user is logged, redirecting to the log-in page if necessary.
    Sets next parameter in session to register member url.
    """

    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            request.session["next"] = reverse("members:register_member")
            return redirect(settings.LOGIN_URL)

    return wrapper
