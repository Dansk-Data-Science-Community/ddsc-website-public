from django.contrib import admin
from .models import OpenSourceProject

@admin.register(OpenSourceProject)
class OpenSourceProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'github_stars', 'featured', 'active', 'created_at')
    list_filter = ('featured', 'active', 'created_at')
    search_fields = ('name', 'description', 'languages')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'github_owner_repo')
    fieldsets = (
        ('Project Info', {'fields': ('name', 'slug', 'description')}),
        ('GitHub', {'fields': ('github_url', 'github_stars', 'github_owner_repo')}),
        ('Details', {'fields': ('languages', 'featured', 'active')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
