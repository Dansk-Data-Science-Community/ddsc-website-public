"""Mobile-optimized DRF serializers"""
from rest_framework import serializers
from django.contrib.auth.models import User
from pages.models import Page
from oss.models import OpenSourceProject
from waitlist.models import EventWaitlist

class UserMobileSerializer(serializers.ModelSerializer):
    """Mobile-optimized user serializer"""
    engagement_level = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'engagement_level']
    
    def get_engagement_level(self, obj):
        if hasattr(obj, 'participation_level'):
            return obj.participation_level.level
        return 'observer'

class PageMobileSerializer(serializers.ModelSerializer):
    """Mobile-optimized page serializer - minimal payload"""
    class Meta:
        model = Page
        fields = ['id', 'title', 'slug', 'content', 'published', 'created_at']
        read_only_fields = ['id', 'created_at']

class OSSProjectMobileSerializer(serializers.ModelSerializer):
    """Mobile-optimized OSS project serializer"""
    category_label = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = OpenSourceProject
        fields = ['id', 'name', 'slug', 'github_url', 'github_stars', 'languages', 'featured', 'category_label']

class WaitlistMobileSerializer(serializers.ModelSerializer):
    """Mobile-optimized waitlist serializer"""
    position_label = serializers.SerializerMethodField()
    
    class Meta:
        model = EventWaitlist
        fields = ['id', 'email', 'event_name', 'position', 'position_label', 'status', 'joined_at']
    
    def get_position_label(self, obj):
        return f"#{obj.position}"

class AuthTokenSerializer(serializers.Serializer):
    """Mobile auth token response"""
    token = serializers.CharField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    expires_in = serializers.SerializerMethodField()
    
    def get_expires_in(self, obj):
        return "30 days"

class APIErrorSerializer(serializers.Serializer):
    """Mobile API error response"""
    error = serializers.CharField()
    message = serializers.CharField()
    status_code = serializers.IntegerField()
    timestamp = serializers.DateTimeField()

class APISuccessSerializer(serializers.Serializer):
    """Mobile API success wrapper"""
    success = serializers.BooleanField(default=True)
    data = serializers.JSONField()
    message = serializers.CharField(required=False, allow_blank=True)
