from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.signing import BadSignature
from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView
from users.models import User

from .decorators import login_required_with_next, redirect_when_sold_out
from .forms import CreateEventForm, EventAddressForm, EventImageForm, RegisterEventForm
from .mixins import SaveEventMixin
from .models import Event, EventRegistration
from .signing import unsign_ticket_data
from .tasks import send_ticket_mail


def event_list(request):
    if user_is_eventeditor(request.user):
        events = Event.coming_events.all()
    else:
        events = Event.coming_events.filter(draft=False)
    events_dict = {event: event.images.first() for event in events}

    if not events:
        return render(
            request,
            "events/no_events.html",
            {
                "footer_class": "fixed-bottom",
            },
        )
    else:
        return render(
            request,
            "events/list.html",
            {
                "events_active": "active",
                "has_events": events.exists(),
                "events": events_dict.items(),
            },
        )


def user_is_eventeditor(user: User):
    return user.groups.filter(name="Eventeditor").exists() or user.is_superuser


def share_event(request, id, slug):
    event = get_object_or_404(
        Event,
        id=id,
        slug=slug,
        end_datetime__gt=timezone.now(),
    )
    images = event.images.all()

    return render(
        request,
        "events/share.html",
        {
            "events_active": "active",
            "event": event,
            "images": images,
        },
    )


# TODO: refaktorer datavalidering ud til form validering i forms.py for RegisterEvent viewet.
class RegisterEvent(View):
    register_event_template = "events/register_event.html"

    def setup(self, request, id, slug, *args, **kwargs):
        """
        Override setup method to initialize view by getting the event object.
        Then check if event is sold out and if user is authenticated. Redirect if necessary
        """
        super().setup(request, *args, **kwargs)
        self.event = get_object_or_404(
            Event,
            id=id,
            slug=slug,
            end_datetime__gt=timezone.now(),
        )
        if self.event.is_sold_out():
            return HttpResponseRedirect(reverse("events:event_list"))

    @login_required_with_next
    @redirect_when_sold_out
    def get(self, request, id, slug):
        self.form = RegisterEventForm(initial=self.__get_initial_data())
        return self.__render_register_event()

    def __get_initial_data(self):
        user = self.request.user
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }

    def __render_register_event(self):
        return render(
            self.request,
            self.register_event_template,
            {
                "events_active": "active",
                "event": self.event,
                "form": self.form,
            },
        )

    @login_required_with_next
    @redirect_when_sold_out
    def post(self, request, **kwargs):
        if not request.user.is_member:
            messages.error(
                self.request, _("You need to be a member to signup for an event")
            )
            return redirect("members:register_member")
        self.form = RegisterEventForm(data=request.POST)

        if self.form.is_valid():
            event_registration = self.__create_event_registration()
            self.__try_save_or_error(event_registration)
            send_ticket_mail.delay(request.user.id, event_registration.id)
            return redirect("users:dashboard")
        else:
            return self.__generic_error_message()

    def __create_event_registration(self):
        return EventRegistration(
            user=self.request.user,
            event=self.event,
        )

    def __try_save_or_error(self, event_registration):
        try:
            event_registration.save()
            return redirect("users:dashboard")
        except IntegrityError as e:
            if "UNIQUE constraint" in str(e.args):
                messages.error(self.request, _("Du er allerede tilmeldt dette event"))

    def __generic_error_message(self):
        return messages.error(self.request, _("Noget gik galt"))


class CreateEvent(LoginRequiredMixin, PermissionRequiredMixin, SaveEventMixin, View):
    permission_required = "events.add_event"
    create_event_template = "events/create_event.html"

    @transaction.atomic
    def post(self, request):
        self.event_form = CreateEventForm(data=request.POST)
        self.address_form = EventAddressForm(data=request.POST)
        self.event_image_form = EventImageForm(files=request.FILES, data=request.POST)

        if (
            self.event_form.is_valid()
            and self.address_form.is_valid()
            and self.event_image_form.is_valid()
        ):
            self.save_event()
            return redirect("events:event_list")
        else:
            return self.__render_create_event()

    def get(self, request):
        self.event_form = CreateEventForm()
        self.address_form = EventAddressForm()
        self.event_image_form = EventImageForm()
        return self.__render_create_event()

    def __render_create_event(self):
        return render(
            self.request,
            self.create_event_template,
            {
                "events_active": "active",
                "view_name": "create_event",
                "event_form": self.event_form,
                "address_form": self.address_form,
                "event_image_form": self.event_image_form,
            },
        )


class EditEvent(LoginRequiredMixin, PermissionRequiredMixin, SaveEventMixin, View):
    permission_required = "events.change_event"
    edit_event_template = "events/edit_event.html"

    @transaction.atomic
    def post(self, request, id, slug, **kwargs):
        event = get_object_or_404(
            Event,
            id=id,
            slug=slug,
            end_datetime__gt=timezone.now(),
        )

        self.event_form = CreateEventForm(instance=event, data=request.POST)
        self.address_form = EventAddressForm(instance=event.address, data=request.POST)
        self.event_image_form = EventImageForm(
            instance=event.get_first_image(), files=request.FILES, data=request.POST
        )

        if (
            self.event_form.is_valid()
            and self.address_form.is_valid()
            and self.event_image_form.is_valid()
        ):
            self.save_event()
            return redirect("events:event_list")
        else:
            return self.__render_edit_event(event)

    def get(self, request, id, slug, **kwargs):
        event = get_object_or_404(
            Event,
            id=id,
            slug=slug,
            end_datetime__gt=timezone.now(),
        )
        self.event_form = CreateEventForm(instance=event)
        self.address_form = EventAddressForm(instance=event.address)
        self.event_image_form = EventImageForm(instance=event.get_first_image())
        return self.__render_edit_event(event)

    def __render_edit_event(self, event):
        return render(
            self.request,
            self.edit_event_template,
            {
                "event": event,
                "events_active": "active",
                "view_name": "edit_event",
                "event_form": self.event_form,
                "address_form": self.address_form,
                "event_image_form": self.event_image_form,
            },
        )


class DeleteEvent(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "events.delete_event"
    model = Event
    success_url = "/events"


@login_required
def unregister_event(request, id, slug, **kwargs):
    user = request.user
    event_registration = get_object_or_404(
        EventRegistration,
        user=user,
        id=id,
        slug=slug,
    )
    if request.method == "POST":
        event_registration.delete()
        return HttpResponseRedirect(reverse("users:dashboard"))
    else:
        return render(
            request,
            "events/unregister_event.html",
            {
                "registration": event_registration,
            },
        )


class MiniMeetupView(TemplateView):
    template_name = "events/mini_meetup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events_active"] = "active"
        return context


@user_passes_test(lambda u: u.groups.filter(name="TicketConsumer").exists())
@login_required
def consume_ticket(request, token):
    if request.method == "GET":
        try:
            data = unsign_ticket_data(token)
        except BadSignature:
            return HttpResponseBadRequest("Bad signature")

        event_registration = get_object_or_404(
            EventRegistration, event__id=data["event_id"], token=data["token"]
        )
        if event_registration.status == EventRegistration.StatusChoice.ATTENDED:
            return HttpResponseBadRequest("Ticket already consumed")
        event_registration.status = EventRegistration.StatusChoice.ATTENDED
        event_registration.save()
        return render(
            request,
            "events/ticket_consumed.html",
            {
                "registration_success": True,
                "event_registration": event_registration,
            },
        )
