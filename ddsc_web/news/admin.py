from django.contrib import admin
from django.contrib.auth import get_user_model

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
        fields = ("email", "full_name", "frequency", "user_email")
        export_order = ("email", "full_name", "frequency", "user_email")

    def get_queryset(self):
        return super().get_queryset().filter(allow_newsletters=True)


@admin.register(NewsSubscriber)
class NewsSubscriberAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = NewsSubscriberResource
    list_display = ["email", "full_name", "frequency", "allow_newsletters", "confirmed_at"]
    list_filter = ["created", "allow_newsletters", "frequency"]
    search_fields = ["email", "full_name"]
    readonly_fields = ["created", "consent_timestamp", "confirmed_at", "unsubscribed_at"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(allow_newsletters=True)
