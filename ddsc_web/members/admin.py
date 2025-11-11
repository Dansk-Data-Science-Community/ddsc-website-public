from django.contrib import admin
from .models import Member, Address


class AddressInline(admin.TabularInline):
    model = Address
    can_delete = True
    verbose_name_plural = "Addresses"


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    inlines = (AddressInline,)
    search_fields = ["user__email", "user__first_name", "user__last_name", "title"]
    fields = [
        "user",
        "title",
        "created",
        "status",
        "slug",
    ]
    list_filter = ["title", "status", "created"]
    list_display = (
        "user",
        "title",
        "created",
        "status",
        "slug",
    )
    readonly_fields = [
        "created",
    ]
