from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from import_export.admin import ExportMixin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import NewsSubscriber

User = get_user_model()


class NewsSubscriberResource(resources.ModelResource):
    user_email = fields.Field(
        column_name="user_email",
        attribute="user",
        widget=ForeignKeyWidget(User, "email"),
    )

    class Meta:
        model = NewsSubscriber
        fields = (
            "email",
            "name",
            "user_email",
            "is_confirmed",
            "allow_newsletters",
            "event_types",
            "frequency",
            "created",
            "updated",
        )
        export_order = (
            "email",
            "name",
            "user_email",
            "is_confirmed",
            "allow_newsletters",
            "event_types",
            "frequency",
            "created",
            "updated",
        )

    def get_queryset(self):
        return super().get_queryset().filter(allow_newsletters=True, is_confirmed=True)


@admin.register(NewsSubscriber)
class NewsSubscriberAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = NewsSubscriberResource

    list_display = [
        "email",
        "name",
        "status_badge",
        "event_types",
        "frequency",
        "created",
        "actions_column",
    ]

    list_filter = [
        "is_confirmed",
        "allow_newsletters",
        "event_types",
        "frequency",
        "created",
    ]

    search_fields = ["email", "name"]

    readonly_fields = ["created", "updated", "confirmation_token"]

    fieldsets = (
        (_("Contact Information"), {
            "fields": ("email", "name", "user"),
        }),
        (_("Subscription Status"), {
            "fields": ("is_confirmed", "allow_newsletters"),
        }),
        (_("Preferences"), {
            "fields": ("event_types", "frequency"),
        }),
        (_("System Information"), {
            "fields": ("confirmation_token", "created", "updated"),
            "classes": ("collapse",),
        }),
    )

    actions = ["mark_as_confirmed", "send_confirmation_email_action", "export_active_subscribers"]

    def status_badge(self, obj):
        """Display a visual badge for subscription status"""
        if obj.is_confirmed and obj.allow_newsletters:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">✓ Active</span>'
            )
        elif not obj.is_confirmed:
            return format_html(
                '<span style="background-color: #ffc107; color: black; padding: 3px 10px; border-radius: 3px;">⏳ Pending</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #6c757d; color: white; padding: 3px 10px; border-radius: 3px;">✗ Inactive</span>'
            )
    status_badge.short_description = _("Status")

    def actions_column(self, obj):
        """Display action links for each subscriber"""
        if obj.confirmation_token:
            preferences_url = reverse('news:update_preferences') + f'?token={obj.confirmation_token}'
            unsubscribe_url = reverse('news:unsubscribe_token', args=[obj.confirmation_token])
            return format_html(
                '<a href="{}" target="_blank">Preferences</a> | <a href="{}" target="_blank">Unsubscribe</a>',
                preferences_url,
                unsubscribe_url,
            )
        return "-"
    actions_column.short_description = _("Actions")

    def mark_as_confirmed(self, request, queryset):
        """Admin action to manually confirm subscribers"""
        updated = queryset.update(is_confirmed=True)
        self.message_user(request, f"{updated} subscribers marked as confirmed.")
    mark_as_confirmed.short_description = _("Mark selected as confirmed")

    def send_confirmation_email_action(self, request, queryset):
        """Admin action to resend confirmation emails"""
        from .tasks import send_confirmation_email
        count = 0
        for subscriber in queryset.filter(is_confirmed=False):
            send_confirmation_email.delay(subscriber.id)
            count += 1
        self.message_user(request, f"Confirmation emails sent to {count} subscribers.")
    send_confirmation_email_action.short_description = _("Resend confirmation emails")

    def export_active_subscribers(self, request, queryset):
        """Export only active, confirmed subscribers"""
        from django.http import HttpResponse
        import csv

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="active_subscribers.csv"'

        writer = csv.writer(response)
        writer.writerow(['Email', 'Name', 'Event Types', 'Frequency', 'Created'])

        for subscriber in queryset.filter(is_confirmed=True, allow_newsletters=True):
            writer.writerow([
                subscriber.email,
                subscriber.name,
                subscriber.get_event_types_display(),
                subscriber.get_frequency_display(),
                subscriber.created.strftime('%Y-%m-%d'),
            ])

        return response
    export_active_subscribers.short_description = _("Export active subscribers to CSV")

    def get_queryset(self, request):
        """Show all subscribers in admin (not just active ones)"""
        return super().get_queryset(request)
