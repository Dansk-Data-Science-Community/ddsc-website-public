from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ParticipationLevel(models.Model):
    """Define engagement participation tiers"""
    LEVEL_CHOICES = [
        ('observer', 'Observer - Passive Viewing'),
        ('attendee', 'Attendee - Active Participation'),
        ('organizer', 'Organizer - Event Leadership'),
        ('contributor', 'Contributor - Content Creation'),
        ('ambassador', 'Ambassador - Community Leadership'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='participation_level')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='observer')
    score = models.PositiveIntegerField(default=0)  # Engagement score
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Participation Level"
        verbose_name_plural = "Participation Levels"
    
    def __str__(self):
        return f"{self.user.email} - {self.get_level_display()}"
    
    def increment_score(self, points):
        """Add engagement points"""
        self.score += points
        self.save()
        return self.score


class EngagementOption(models.Model):
    """Track available engagement methods/opportunities"""
    CATEGORY_CHOICES = [
        ('event', 'Event Participation'),
        ('content', 'Content Creation'),
        ('community', 'Community Support'),
        ('learning', 'Learning & Development'),
        ('leadership', 'Leadership Role'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    engagement_points = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Engagement Option"
        verbose_name_plural = "Engagement Options"
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class ActivityLog(models.Model):
    """Log all user engagement activities"""
    ACTIVITY_TYPES = [
        ('event_attend', 'Event Attendance'),
        ('event_organize', 'Event Organization'),
        ('content_create', 'Content Created'),
        ('content_comment', 'Content Comment'),
        ('help_provided', 'Help/Support Provided'),
        ('skill_shared', 'Skill Shared'),
        ('feedback_given', 'Feedback Given'),
        ('challenge_completed', 'Challenge Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    engagement_option = models.ForeignKey(EngagementOption, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    points_earned = models.PositiveIntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)  # Store extra context
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['activity_type', '-timestamp']),
        ]
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"
    
    def __str__(self):
        return f"{self.user.email} - {self.get_activity_type_display()} ({self.timestamp.strftime('%Y-%m-%d')})"
    
    def save(self, *args, **kwargs):
        """Auto-update participation level on activity log"""
        super().save(*args, **kwargs)
        level, created = ParticipationLevel.objects.get_or_create(user=self.user)
        level.increment_score(self.points_earned)


class EngagementGoal(models.Model):
    """Track member engagement goals"""
    GOAL_STATUS = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='engagement_goals')
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_points = models.PositiveIntegerField()
    current_points = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=GOAL_STATUS, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        progress = (self.current_points / self.target_points * 100) if self.target_points else 0
        return f"{self.user.email} - {self.title} ({progress:.0f}%)"
    
    def update_progress(self):
        """Recalculate points from activity logs"""
        points = self.user.activities.filter(
            timestamp__gte=self.created_at
        ).aggregate(models.Sum('points_earned'))['points_earned__sum'] or 0
        self.current_points = points
        if self.current_points >= self.target_points and self.status == 'active':
            self.status = 'completed'
            self.completed_at = timezone.now()
        self.save()


class EngagementTrend(models.Model):
    """Track engagement trends over time (daily snapshot)"""
    date = models.DateField()
    total_activities = models.PositiveIntegerField(default=0)
    active_members = models.PositiveIntegerField(default=0)
    average_engagement_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['date']
    
    def __str__(self):
        return f"Engagement Snapshot - {self.date}"
