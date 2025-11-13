from django.test import TestCase
from django.contrib.auth.models import User
from .models import ParticipationLevel, EngagementOption, ActivityLog, EngagementGoal
from .services import EngagementService

class EngagementTrackingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", username="testuser", password="pass")
        self.option = EngagementOption.objects.create(
            name="Event Attendance",
            category="event",
            description="Attend a DDSC event",
            engagement_points=10
        )
    
    def test_participation_level_creation(self):
        self.assertTrue(hasattr(self.user, 'participation_level'))
        self.assertEqual(self.user.participation_level.level, 'observer')
    
    def test_activity_logging(self):
        activity = EngagementService.log_activity(
            self.user, 'event_attend', self.option, "Attended workshop", 10
        )
        self.assertEqual(activity.points_earned, 10)
        self.assertEqual(self.user.activities.count(), 1)
    
    def test_score_accumulation(self):
        EngagementService.log_activity(self.user, 'event_attend', self.option, points=10)
        EngagementService.log_activity(self.user, 'event_attend', self.option, points=5)
        self.user.participation_level.refresh_from_db()
        self.assertEqual(self.user.participation_level.score, 15)
    
    def test_user_stats(self):
        EngagementService.log_activity(self.user, 'event_attend', self.option, points=10)
        stats = EngagementService.get_user_stats(self.user)
        self.assertEqual(stats['total_activities'], 1)
        self.assertEqual(stats['total_points'], 10)
    
    def test_engagement_goal(self):
        goal = EngagementGoal.objects.create(
            user=self.user,
            title="Participate in 5 events",
            description="Attend 5 DDSC events",
            target_points=50
        )
        EngagementService.log_activity(self.user, 'event_attend', self.option, points=25)
        EngagementService.log_activity(self.user, 'event_attend', self.option, points=25)
        goal.update_progress()
        self.assertEqual(goal.current_points, 50)
        self.assertEqual(goal.status, 'completed')
