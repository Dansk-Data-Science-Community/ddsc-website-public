import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from news.models import NewsSubscriber
from shared.forms import FullNameForm

from .decorators import login_required_with_next, redirect_members
from .forms import EditMemberForm, MemberAddressForm, UserMemberForm
from .models import Member
from .tasks import send_welcome_email


@method_decorator([login_required_with_next, redirect_members], name="dispatch")
class RegisterMember(View):
    """
    View for member registration.
    If user is allready member, redirect user to dashboard.
    If user is not logged in, redirect user to login page.
    After succesfull login, redirect back to register member form.
    """

    register_member_template = "members/register.html"
    register_done_template = "members/register_done.html"

    def get(self, request):
        """
        Initialize register member form with users full name.
        """

        user = request.user
        member_form = UserMemberForm()
        user_form = FullNameForm(initial=self.__get_initial_data(user))
        return self.__render_register_member(user_form, member_form)

    def post(self, request):
        """
        Method for submitting form to register as member.
        Create member object and se value for allow_newsletters field.
        Send error message if form validation fails.
        """

        user = request.user
        member_form = UserMemberForm(data=request.POST)
        user_form = FullNameForm(
            data=request.POST,
            initial=self.__get_initial_data(user),
        )
        if member_form.is_valid() and user_form.is_valid():
            new_member = self.__create_new_member(user, member_form)
            self.__set_allow_newsletters(user, member_form)
            send_welcome_email.delay(user_id=user.id)
            return self.__render_register_done(new_member)
        else:
            return self.__message_error()

    def __get_initial_data(self, user):
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
        }

    def __render_register_member(self, user_form, member_form):
        return render(
            self.request,
            self.register_member_template,
            {
                "user_form": user_form,
                "member_form": member_form,
            },
        )

    def __create_new_member(self, user, member_form: UserMemberForm):
        new_member = member_form.save(commit=False)
        new_member.user = user
        return new_member.save()

    def __set_allow_newsletters(self, user, member_form: UserMemberForm):
        news_subscriber, created = NewsSubscriber.objects.get_or_create(user=user)
        news_subscriber.allow_newsletters = member_form.cleaned_data.get(
            "allow_newsletters"
        )
        return news_subscriber.save()

    def __render_register_done(self, new_member):
        return render(
            self.request,
            self.register_done_template,
            {
                "new_member": new_member,
            },
        )

    def __message_error(self):
        return messages.error(self.request, _("Der var fejl"))


@login_required
def edit_member(request):
    user = request.user
    if request.method == "POST":
        member_form = EditMemberForm(
            instance=user.member,
            data=request.POST,
        )
        if member_form.is_valid():
            member_form.save()
            news_subscriber, created = NewsSubscriber.objects.get_or_create(
                user=user,
            )
            news_subscriber.allow_newsletters = member_form.cleaned_data.get(
                "allow_newsletters"
            )
            news_subscriber.save()
            messages.success(request, _("Dit medlemsskab blev opdateret"))
        else:
            messages.error(request, _("Der var fejl i opdatering af dit medlemsskab"))
    else:
        member_form = EditMemberForm(
            instance=user.member,
            initial={
                "allow_newsletters": NewsSubscriber.objects.get(
                    user=user
                ).allow_newsletters
            },
        )
    return render(
        request,
        "members/edit.html",
        {
            "member_form": member_form,
        },
    )


@login_required
def unsubscribe(request):
    user = request.user
    if request.method == "POST":
        if user.is_member:
            user.member.delete()
            return HttpResponseRedirect(reverse("users:dashboard"))
    else:
        address_form = MemberAddressForm(instance=user.member.address)
        member_form = UserMemberForm(instance=user.member)
        return render(
            request,
            "members/edit.html",
            {
                "address_form": address_form,
                "member_form": member_form,
            },
        )


def board_members(request):
    board_members = Member.objects.filter(
        title__in=[
            Member.TitleChoice.BESTYRELSESMEDLEM,
            Member.TitleChoice.FORMAND,
            Member.TitleChoice.NÆSTFORMAND,
            Member.TitleChoice.SUPPLEANT,
        ]
    )
    return render(
        request,
        "members/board.html",
        {
            "board_members": board_members,
            "organisation_active": "active",
        },
    )


def articles(request):
    user_agent = request.META["HTTP_USER_AGENT"]
    if "Mobile" in user_agent:
        file_url = static(
            "Dansk_Data_Science_Community_foreningsvedtægter.pdf",
        )
        return HttpResponseRedirect(file_url)
    else:
        return render(
            request,
            "members/articles.html",
            {
                "organisation_active": "active",
            },
        )


def salary(request):
    return HttpResponseRedirect(settings.SALARY_URL)
