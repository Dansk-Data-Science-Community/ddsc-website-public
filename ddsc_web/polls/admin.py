from django.contrib import admin
from .models import Question, Choice, Pollsession, VoterSession, Answer


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLine]


class QuestionLine(admin.TabularInline):
    model = Question
    extra = 3


class PollsessionAdmin(admin.ModelAdmin):
    model = Pollsession
    inlines = [QuestionLine]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Pollsession, PollsessionAdmin)
admin.site.register(VoterSession)
admin.site.register(Answer)
