"""DRF serializers for API endpoints"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ParticipationLevel, EngagementOption, ActivityLog, EngagementGoal

class ParticipationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipationLevel
        fields = ['level', 'score', 'updated_at']

class EngagementOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngagementOption
        fields = ['id', 'name', 'category', 'description', 'engagement_points', 'is_active']

class ActivityLogSerializer(serializers.ModelSerializer):
    activity_type_display = serializers.CharField(source='get_activity_type_display', read_only=True)
    class Meta:
        model = ActivityLog
        fields = ['id', 'activity_type', 'activity_type_display', 'description', 'points_earned', 'timestamp']

class EngagementGoalSerializer(serializers.ModelSerializer):
    progress_percent = serializers.SerializerMethodField()
    
    class Meta:
        model = EngagementGoal
        fields = ['id', 'title', 'description', 'target_points', 'current_points', 'progress_percent', 'status']
    
    def get_progress_percent(self, obj):
        if obj.target_points == 0:
            return 0
        return (obj.current_points / obj.target_points * 100)
