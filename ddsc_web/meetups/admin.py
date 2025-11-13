from django.contrib import admin
from .models import RecurringMeetup

@admin.register(RecurringMeetup)
class RecurringMeetupAdmin(admin.ModelAdmin):
    list_display = ('title', 'day_of_week', 'start_time', 'frequency', 'active', 'last_generated_date')
    list_filter = ('active', 'day_of_week', 'frequency')
    search_fields = ('title', 'location')
    readonly_fields = ('created_at', 'updated_at')
