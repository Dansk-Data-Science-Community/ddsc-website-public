from django.contrib import admin
from .models import Profile, User, ProfileImage
from django.contrib.auth.admin import UserAdmin


class ProfileImageInline(admin.StackedInline):
    model = ProfileImage
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "profile"
    fields = [
        "image",
    ]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = (ProfileImageInline,)
    fields = [
        "user",
        "birthdate",
    ]


@admin.register(ProfileImage)
class ProfileImageAdmin(admin.ModelAdmin):
    pass


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"


class CustomUserAdmin(UserAdmin):
    search_fields = ["email", "first_name", "last_name"]
    inlines = (ProfileInline,)
    list_display = (
        "first_name",
        "last_name",
        "email",
        "date_joined",
        "is_staff",
        "is_verified",
    )
    ordering = ("-date_joined",)
    list_filter = ("date_joined",)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            self.add_fieldsets = (
                (
                    None,
                    {
                        "fields": (
                            "email",
                            "first_name",
                            "last_name",
                            "password1",
                            "password2",
                        ),
                        "description": '<p class="text-primary">Please complete this form to create user.</p>',
                    },
                ),
            )
            return self.add_fieldsets

        self.fieldsets = (
            (None, {"fields": ("email", "first_name", "last_name")}),
            (
                "Advanced",
                {
                    "fields": (
                        "password",
                        "is_active",
                        "is_staff",
                        "is_superuser",
                        "is_verified",
                        "groups",
                        "user_permissions",
                    )
                },
            ),
            (
                "Statistics",
                {
                    "fields": (
                        "last_login",
                        "date_joined",
                    )
                },
            ),
        )
        return self.fieldsets

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super().add_view(*args, **kwargs)


admin.site.register(User, CustomUserAdmin)
