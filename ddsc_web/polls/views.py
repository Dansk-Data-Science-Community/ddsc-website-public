from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Question, Choice, Pollsession, Answer, VoterSession
from .forms import QuestionChoiceForm


@login_required
def list_polls(request):
    poll_sessions = Pollsession.objects.filter(active=True)
    if poll_sessions:
        is_completed = [poll.user_has_completed(request.user) for poll in poll_sessions]
        context = {
            "polls_list": zip(poll_sessions, is_completed),
            "organisation_active": "active",
        }
        return render(request, "polls/index.html", context)
    else:
        return render(
            request,
            "polls/no_polls.html",
            {
                "organisation_active": "active",
            },
        )


@login_required
def poll_detail(request, poll_session_id):
    poll = get_object_or_404(Pollsession, pk=poll_session_id, active=True)
    voter_session, created = VoterSession.objects.get_or_create(
        poll_session=poll, user=request.user
    )
    if voter_session.is_completed:
        messages.error(request, _("Du har allerede svaret på afstemningen"))
        return HttpResponseRedirect(reverse("polls:list_polls"))
    question_forms = {
        question: QuestionChoiceForm(
            choice_queryset=question.choices.all(), initial={"question": question}
        )
        for question in poll.questions.all()
    }
    return render(
        request,
        "polls/poll_detail.html",
        {
            "poll": poll,
            "question_forms": question_forms.items(),
            "voter_session": voter_session,
            "organisation_active": "active",
        },
    )


@login_required
@transaction.atomic
def submit_poll(request, voter_session_id):
    voter_session = get_object_or_404(
        VoterSession, pk=voter_session_id, user=request.user
    )
    if voter_session.is_completed:
        messages.error(request, _("Du har allerede svaret på afstemningen"))
        return HttpResponseRedirect(reverse("polls:list_polls"))
    if request.method == "POST":
        if voter_session.poll_session.anonymous:
            answers_list = create_answer_objects(request)
        else:
            answers_list = create_answer_objects(request, user=request.user)

        Answer.objects.bulk_create(answers_list)
        voter_session.vote_completed_at = timezone.now()
        voter_session.save()
        messages.success(request, _("Tak for deltagelse i afstemningen"))
        return HttpResponseRedirect(reverse("polls:list_polls"))
    else:
        return HttpResponseRedirect(reverse("polls:list_polls"))


def create_answer_objects(request, user=None):
    question_choice = zip(
        request.POST.getlist("question"), request.POST.getlist("choice")
    )
    return [
        Answer(
            voter=user,
            question=Question(pk=question),
            choice=Choice(pk=choice),
        )
        for question, choice in question_choice
    ]


@login_required
@user_passes_test(lambda user: user.is_staff)
def poll_results(request, poll_session_id):
    poll = get_object_or_404(Pollsession, pk=poll_session_id)
    poll_results = poll.get_poll_results()
    return render(
        request,
        "polls/poll_result.html",
        {
            "poll_results": poll_results,
            "poll": poll,
            "organisation_active": "active",
        },
    )
