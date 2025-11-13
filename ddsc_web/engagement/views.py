"""API views for engagement tracking"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import ParticipationLevel, ActivityLog, EngagementGoal
from .serializers import ParticipationLevelSerializer, ActivityLogSerializer, EngagementGoalSerializer
from .services import EngagementService

class ParticipationLevelViewSet(viewsets.ReadOnlyModelViewSet):
    """Retrieve user participation levels"""
    queryset = ParticipationLevel.objects.all()
    serializer_class = ParticipationLevelSerializer
    
    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        """Get top engaged members"""
        top = EngagementService.get_leaderboard(10)
        serializer = self.get_serializer(top, many=True)
        return Response(serializer.data)

class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    """View activity logs"""
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ActivityLog.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get user activity statistics"""
        stats = EngagementService.get_user_stats(request.user)
        return Response(stats)

class EngagementGoalViewSet(viewsets.ModelViewSet):
    """Manage engagement goals"""
    serializer_class = EngagementGoalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return EngagementGoal.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        """Update goal progress"""
        goal = self.get_object()
        goal.update_progress()
        serializer = self.get_serializer(goal)
        return Response(serializer.data)
