from django.contrib import admin

from .models import Event, EventImage, Address, EventRegistration, RegistrationTerms
from image_cropping import ImageCroppingMixin
from import_export import resources
from import_export.admin import ExportMixin


@admin.register(RegistrationTerms)
class RegistrationTermsAdmin(admin.ModelAdmin):
    pass


class ImageInline(ImageCroppingMixin, admin.StackedInline):
    model = EventImage
    can_delete = True
    verbose_name_plural = "event images"
    fk_name = "event"
    fields = ["image", "order"]


class AddressInline(admin.TabularInline):
    model = Address
    can_delete = True
    verbose_name_plural = "Addresses"


class EventRegistrationResource(resources.ModelResource):
    class Meta:
        model = EventRegistration
        fields = (
            "event__id",
            "event__title",
            "user__first_name",
            "user__last_name",
            "created",
            "status",
        )
        export_order = (
            "event__id",
            "event__title",
            "user__first_name",
            "user__last_name",
            "created",
            "status",
        )


@admin.register(EventRegistration)
class EventRegistrationAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = EventRegistrationResource
    list_display = ("event", "user", "created", "status")
    list_filter = ("status", "event__title")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "start_datetime",
        "end_datetime",
        "created",
        "number_of_registrations",
        "registration_terms",
    ]
    list_filter = ["created", "title"]
    readonly_fields = [
        "created",
        "slug",
    ]
    inlines = [
        ImageInline,
        AddressInline,
    ]

    def number_of_registrations(self, obj):
        return obj.registrations.count()

    number_of_registrations.short_description = "Number of registrations"
