from django.db import models, IntegrityError
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Pollsession(models.Model):
    title = models.CharField(
        max_length=200,
        help_text=_("Titlen på afstemningen"),
    )
    description = models.TextField(
        help_text=_("Beskrivelse af indholdet i afstemningen")
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        help_text=_("Forfatteren til afstemningen"),
        null=True,
        blank=True,
    )
    active = models.BooleanField(default=True)
    anonymous = models.BooleanField(
        default=False,
        help_text=_("Er afstemningen anonym?"),
    )
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def user_has_completed(self, user):
        try:
            return self.voter_sessions.get(user=user).is_completed
        except ObjectDoesNotExist:
            return False

    def votes_completed_count(self):
        return self.voter_sessions.filter(vote_completed_at__lte=timezone.now()).count()

    def get_poll_results(self):
        return {
            question: question.get_choice_vote_results()
            for question in self.questions.all()
        }


class VoterSession(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="voters",
    )
    poll_session = models.ForeignKey(
        Pollsession, on_delete=models.CASCADE, related_name="voter_sessions"
    )
    vote_started_at = models.DateTimeField(auto_now_add=True)
    vote_completed_at = models.DateTimeField(null=True)

    class Meta:
        unique_together = ["user", "poll_session"]

    def __str__(self):
        return f"{self.user.get_full_name()} started voting {self.vote_started_at}"

    @property
    def is_completed(self):
        if self.vote_completed_at:
            return self.vote_completed_at < timezone.now()
        else:
            return False


class Question(models.Model):
    poll_session = models.ForeignKey(
        Pollsession,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    text = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def get_choice_vote_results(self):
        return {
            choice: [
                choice.votes.all().count(),
                choice.get_choice_vote_proportion(),
            ]
            for choice in self.choices.all()
        }


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices",
    )
    text = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def get_choice_vote_proportion(self):
        zero_vote_proportion = 0
        try:
            return self.votes.all().count() / self.question.votes.all().count()
        except ZeroDivisionError:
            return zero_vote_proportion


class Answer(models.Model):
    voter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.question.choices.filter(choice=self.choice).exists():
            raise IntegrityError("Choice must be related to Question")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.question.text} - {self.choice.text}"
