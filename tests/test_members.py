"""Test suite for members/engagement app"""
import pytest
from django.contrib.auth.models import User
from engagement.models import ParticipationLevel, ActivityLog, EngagementGoal

@pytest.mark.django_db
@pytest.mark.unit
class TestParticipationLevel:
    """ParticipationLevel model tests"""
    
    def test_create_participation_level(self, test_user):
        """Test creating participation level"""
        level = ParticipationLevel.objects.create(
            user=test_user,
            level='attendee',
            score=10
        )
        assert level.user == test_user
        assert level.level == 'attendee'
    
    def test_score_increment(self, test_user):
        """Test score increment method"""
        level = ParticipationLevel.objects.create(user=test_user, score=0)
        level.increment_score(5)
        assert level.score == 5
    
    def test_auto_create_on_user(self, user_factory):
        """Test auto-creation on new user"""
        user = user_factory(username='newuser')
        assert hasattr(user, 'participation_level')

@pytest.mark.django_db
@pytest.mark.unit
class TestActivityLog:
    """ActivityLog model tests"""
    
    def test_log_activity(self, test_user):
        """Test logging activity"""
        activity = ActivityLog.objects.create(
            user=test_user,
            activity_type='event_attend',
            points_earned=10
        )
        assert activity.user == test_user
        assert activity.points_earned == 10
    
    def test_activity_score_update(self, test_user):
        """Test that activity updates score"""
        ActivityLog.objects.create(
            user=test_user,
            activity_type='event_attend',
            points_earned=15
        )
        test_user.participation_level.refresh_from_db()
        assert test_user.participation_level.score >= 15

@pytest.mark.django_db
@pytest.mark.unit
class TestEngagementGoal:
    """EngagementGoal model tests"""
    
    def test_create_goal(self, test_user):
        """Test creating engagement goal"""
        goal = EngagementGoal.objects.create(
            user=test_user,
            title="Attend 5 Events",
            target_points=50
        )
        assert goal.user == test_user
        assert goal.target_points == 50
    
    def test_goal_progress(self, test_user):
        """Test goal progress tracking"""
        goal = EngagementGoal.objects.create(
            user=test_user,
            title="Test Goal",
            target_points=100,
            current_points=0
        )
        goal.current_points = 100
        goal.update_progress()
        assert goal.status == 'completed'

@pytest.mark.api
@pytest.mark.integration
class TestEngagementAPI:
    """Engagement API tests"""
    
    @pytest.mark.django_db
    def test_stats_endpoint(self, authenticated_api_client):
        """Test engagement stats endpoint"""
        response = authenticated_api_client.get('/api/v1/engagement/stats/')
        assert response.status_code == 200
    
    @pytest.mark.django_db
    def test_leaderboard_endpoint(self, api_client):
        """Test leaderboard endpoint"""
        response = api_client.get('/api/v1/engagement/leaderboard/')
        assert response.status_code == 200
