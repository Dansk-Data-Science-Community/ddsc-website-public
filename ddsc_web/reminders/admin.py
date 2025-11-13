from django.contrib import admin
from .models import Reminder

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('event_registration', 'reminder_type', 'send_at', 'status')
    list_filter = ('status', 'reminder_type')
    readonly_fields = ('created_at', 'updated_at')
