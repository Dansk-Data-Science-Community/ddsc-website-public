"""Engagement tracking service layer"""
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from .models import ActivityLog, ParticipationLevel, EngagementOption, EngagementGoal, EngagementTrend

class EngagementService:
    """Service for engagement operations"""
    
    @staticmethod
    def log_activity(user, activity_type, engagement_option=None, description="", points=0):
        """Log user activity"""
        activity = ActivityLog.objects.create(
            user=user,
            activity_type=activity_type,
            engagement_option=engagement_option,
            description=description,
            points_earned=points,
        )
        return activity
    
    @staticmethod
    def get_user_stats(user):
        """Get user engagement statistics"""
        activities = user.activities.all()
        goals = user.engagement_goals.filter(status='active')
        
        return {
            'total_activities': activities.count(),
            'total_points': activities.aggregate(Sum('points_earned'))['points_earned__sum'] or 0,
            'active_goals': goals.count(),
            'participation_level': user.participation_level.level if hasattr(user, 'participation_level') else 'observer',
        }
    
    @staticmethod
    def get_leaderboard(top_n=10):
        """Get top engaged members"""
        return ParticipationLevel.objects.select_related('user').order_by('-score')[:top_n]
    
    @staticmethod
    def get_activity_report(days=30):
        """Get activity report for past N days"""
        cutoff = timezone.now() - timedelta(days=days)
        activities = ActivityLog.objects.filter(timestamp__gte=cutoff)
        
        return {
            'total_activities': activities.count(),
            'unique_members': activities.values('user').distinct().count(),
            'by_type': dict(activities.values('activity_type').annotate(count=Count('activity_type')).values_list('activity_type', 'count')),
            'total_points': activities.aggregate(Sum('points_earned'))['points_earned__sum'] or 0,
        }
    
    @staticmethod
    def create_daily_snapshot():
        """Create daily engagement trend snapshot"""
        today = timezone.now().date()
        activities = ActivityLog.objects.filter(timestamp__date=today)
        
        snapshot = EngagementTrend.objects.create(
            date=today,
            total_activities=activities.count(),
            active_members=activities.values('user').distinct().count(),
            average_engagement_score=ParticipationLevel.objects.all().aggregate(Avg('score'))['score__avg'] or 0,
        )
        return snapshot
