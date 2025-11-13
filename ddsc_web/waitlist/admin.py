from django.contrib import admin
from django.utils.html import format_html
from .models import EventWaitlist

@admin.register(EventWaitlist)
class EventWaitlistAdmin(admin.ModelAdmin):
    list_display = ('position', 'email', 'event_name', 'status_badge', 'joined_at')
    list_filter = ('event_name', 'status', 'joined_at')
    search_fields = ('email', 'event_name')
    readonly_fields = ('position', 'joined_at', 'promoted_at')
    actions = ['promote_next', 'mark_registered', 'cancel_entry']
    fieldsets = (
        ('Queue Info', {'fields': ('email', 'event_name', 'position')}),
        ('Status', {'fields': ('status', 'notified')}),
        ('Timestamps', {'fields': ('joined_at', 'promoted_at')}),
    )
    
    def status_badge(self, obj):
        colors = {'waiting': '#ffc107', 'promoted': '#28a745', 'registered': '#17a2b8', 'cancelled': '#6c757d'}
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def promote_next(self, request, queryset):
        """Promote next person in queue"""
        event = queryset.first()
        if event:
            next_person = EventWaitlist.get_next_in_queue(event.event_name)
            if next_person:
                next_person.promote()
                self.message_user(request, f"Promoted {next_person.email}")
    promote_next.short_description = "Promote next in queue"
    
    def mark_registered(self, request, queryset):
        queryset.update(status='registered')
    mark_registered.short_description = "Mark as registered"
    
    def cancel_entry(self, request, queryset):
        queryset.update(status='cancelled')
    cancel_entry.short_description = "Cancel entries"
