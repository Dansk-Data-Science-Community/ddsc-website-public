from django.contrib import admin
from django.utils.html import format_html
from .models import ParticipationLevel, EngagementOption, ActivityLog, EngagementGoal, EngagementTrend

@admin.register(ParticipationLevel)
class ParticipationLevelAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'level_badge', 'score', 'updated_at')
    list_filter = ('level', 'updated_at')
    search_fields = ('user__email', 'user__first_name')
    readonly_fields = ('updated_at', 'score')
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User'
    
    def level_badge(self, obj):
        colors = {'observer': '#6c757d', 'attendee': '#0dcaf0', 'organizer': '#0d6efd', 
                  'contributor': '#198754', 'ambassador': '#fd7e14'}
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.level, '#6c757d'),
            obj.get_level_display()
        )
    level_badge.short_description = 'Level'

@admin.register(EngagementOption)
class EngagementOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'engagement_points', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    fieldsets = (
        ('Engagement Option', {'fields': ('name', 'category', 'description')}),
        ('Configuration', {'fields': ('engagement_points', 'is_active')}),
    )

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'activity_type', 'points_earned', 'timestamp')
    list_filter = ('activity_type', 'timestamp', 'points_earned')
    search_fields = ('user__email', 'description')
    readonly_fields = ('timestamp', 'user', 'points_earned')
    date_hierarchy = 'timestamp'
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User'

@admin.register(EngagementGoal)
class EngagementGoalAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'title', 'progress_bar', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'title')
    readonly_fields = ('current_points', 'created_at', 'completed_at')
    actions = ['update_progress', 'mark_completed']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User'
    
    def progress_bar(self, obj):
        if obj.target_points == 0:
            return "N/A"
        progress = (obj.current_points / obj.target_points * 100)
        return format_html(
            '<div style="width:100px; background-color:#e9ecef; border-radius:5px; overflow:hidden;">'
            '<div style="width:{}%; height:20px; background-color:#198754;"></div></div> {:.0f}%',
            progress, progress
        )
    progress_bar.short_description = 'Progress'
    
    def update_progress(self, request, queryset):
        for goal in queryset:
            goal.update_progress()
        self.message_user(request, "Progress updated")
    update_progress.short_description = "Update progress"

@admin.register(EngagementTrend)
class EngagementTrendAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_activities', 'active_members', 'avg_score')
    list_filter = ('date',)
    readonly_fields = ('date', 'created_at')
    date_hierarchy = 'date'
    
    def avg_score(self, obj):
        return f"{obj.average_engagement_score:.2f}"
    avg_score.short_description = 'Avg Score'
