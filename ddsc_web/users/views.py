from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from .tasks import send_activation_email

from .forms import (
    LoginForm,
    ProfileEditForm,
    ProfileImageForm,
    UserEditForm,
    UserRegistrationForm,
)
from .tokens import account_activation_token

User = get_user_model()


class UserLogin(View):

    form_class = LoginForm
    login_template = "auth/login.html"
    activation_pending_template = "auth/activation_pending.html"
    login_error_message = _("Ugyldigt login")

    def get(self, request):
        """
        Method for get requests to /users/login/. Checks to see if user is allready logged in.
        If so, we redirect user to /users/dashboard/.
        """
        if request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        else:
            form = self.form_class()
            return render(
                request,
                self.login_template,
                {"form": form},
            )

    def post(self, request):
        """
        Method called for submitting to the login form on /users/login/
        Checks 1) if form data is valid, 2) if credentials are a valid user
        3) if user has a verified email.
        """
        form = LoginForm(request.POST)
        if not form.is_valid():
            return self.__error_message_and_redirect()

        user = self.__authenticate_user(form)
        if not self.__user_is_authenticated(user):
            return self.__error_message_and_redirect()

        if not user.is_verified:
            self.__send_activation_email(user)
            return self.__render_activation_pending(user)

        return self.__login_user_and_redirect(user)

    def __error_message_and_redirect(self):
        messages.error(self.request, self.login_error_message)
        return redirect("users:login")

    def __authenticate_user(self, form):
        """
        Check if username and password are valid user credentials.
        If they are not, 'authenticate()' returns None
        """
        cd = form.cleaned_data
        user = authenticate(
            self.request,
            username=cd["email"],
            password=cd["password"],
        )
        return user

    def __user_is_authenticated(self, user):
        if user is None:
            return False
        else:
            return True

    def __send_activation_email(self, user):
        send_activation_email.delay(
            get_current_site(self.request).domain,
            self.request.scheme,
            user.pk,
        )
        return True

    def __render_activation_pending(self, user):
        return render(
            self.request,
            self.activation_pending_template,
            {"user": user},
        )

    def __login_user_and_redirect(self, user):
        login(self.request, user)
        return HttpResponseRedirect(self.__get_redirect_url())

    def __get_redirect_url(self):
        return self.request.session.get("next", settings.LOGIN_REDIRECT_URL)


# TODO: vi skal have et class view med metoder til at sende en mail til brugeren med aktivering af konto
def register(request):
    """
    User register form. Creates a new user instance
    and triggers signal to create a profile for the user
    """
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            send_activation_email.delay(
                get_current_site(request).domain,
                request.scheme,
                new_user.pk,
            )
            return render(request, "users/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "users/register.html", {"user_form": user_form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()
        return render(
            request,
            "auth/activation_done.html",
            {
                "user": user,
            },
        )
    else:
        return render(request, "auth/activation_failed.html", {})


@login_required
def dashboard(request):
    registrations = request.user.event_registrations.filter(
        event__end_datetime__gt=timezone.now()
    )
    return render(
        request,
        "users/dashboard.html",
        {
            "dasboard_active": "active",
            "user": request.user,
            "registrations": registrations,
            "footer_class": "fixed-bottom",
        },
    )


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST)
        image_form = ProfileImageForm(
            instance=request.user.profile.image, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid() and image_form.is_valid():
            user_form.save()
            profile_form.save()
            image_form.save()
            messages.success(request, _("Din profil blev opdateret"))
        else:
            messages.error(request, _("Der var fejl i opdatering af din profil"))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        image_form = ProfileImageForm(instance=request.user.profile.image)
    return render(
        request,
        "users/edit.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "image_form": image_form,
        },
    )


@login_required
def edit_image(request):
    user = request.user
    if request.method == "POST":
        image_form = ProfileImageForm(instance=user.profile.image, files=request.FILES)
        if image_form.is_valid():
            image_form.save()
            messages.success(request, _("Dit profil billede blev opdateret"))
            return HttpResponseRedirect(reverse("users:edit"))
        else:
            messages.error(request, _("Der var fejl i opdatering af dit profilbillede"))
    else:
        user_form = UserEditForm(instance=user)
        profile_form = ProfileEditForm(instance=user.profile)
        image_form = ProfileImageForm(instance=user.profile.image)
        return render(
            request,
            "users/edit.html",
            {
                "user_form": user_form,
                "profile_form": profile_form,
                "image_form": image_form,
            },
        )


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)
