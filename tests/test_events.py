"""Test suite for events app"""
import pytest
from waitlist.models import EventWaitlist

@pytest.mark.django_db
@pytest.mark.unit
class TestEventWaitlist:
    """EventWaitlist model tests"""
    
    def test_create_waitlist_entry(self):
        """Test creating a waitlist entry"""
        entry = EventWaitlist.objects.create(
            email="user@test.com",
            event_name="Meetup 2025",
            position=1,
            status="waiting"
        )
        assert entry.email == "user@test.com"
        assert entry.position == 1
    
    def test_waitlist_fifo_ordering(self):
        """Test FIFO ordering"""
        EventWaitlist.objects.create(email="a@test.com", event_name="Event", position=1)
        EventWaitlist.objects.create(email="b@test.com", event_name="Event", position=2)
        EventWaitlist.objects.create(email="c@test.com", event_name="Event", position=3)
        
        ordered = EventWaitlist.objects.filter(event_name="Event").order_by('position')
        assert ordered[0].email == "a@test.com"
        assert ordered[2].email == "c@test.com"
    
    def test_waitlist_status_change(self):
        """Test status transitions"""
        entry = EventWaitlist.objects.create(
            email="user@test.com",
            event_name="Event",
            position=1,
            status="waiting"
        )
        entry.status = "promoted"
        entry.save()
        entry.refresh_from_db()
        assert entry.status == "promoted"
    
    @pytest.mark.api
    def test_join_endpoint(self, api_client):
        """Test join waitlist endpoint"""
        response = api_client.post('/api/v1/waitlist/join/', {
            'email': 'new@test.com',
            'event_name': 'Hackathon'
        })
        assert response.status_code == 200
        assert response.json()['success'] is True
