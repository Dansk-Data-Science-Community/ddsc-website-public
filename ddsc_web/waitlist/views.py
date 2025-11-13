from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import EventWaitlist

class JoinWaitlistView(CreateView):
    """Join event waitlist"""
    model = EventWaitlist
    fields = ['email', 'event_name']
    template_name = 'waitlist/join.html'
    success_url = reverse_lazy('waitlist:status')
    
    def form_valid(self, form):
        # Auto-assign position (next available)
        event = form.cleaned_data['event_name']
        last = EventWaitlist.objects.filter(event_name=event).order_by('-position').first()
        form.instance.position = (last.position + 1) if last else 1
        messages.success(self.request, f"You're on the waitlist! Position: #{form.instance.position}")
        return super().form_valid(form)

class WaitlistStatusView(ListView):
    """View waitlist status"""
    model = EventWaitlist
    template_name = 'waitlist/status.html'
    context_object_name = 'waitlist'
    
    def get_queryset(self):
        event = self.request.GET.get('event')
        if event:
            return EventWaitlist.objects.filter(event_name=event)
        return EventWaitlist.objects.all()
