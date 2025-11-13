from django.test import TestCase
from .models import EventWaitlist

class WaitlistTests(TestCase):
    def setUp(self):
        EventWaitlist.objects.create(email="a@test.com", event_name="Meetup", position=1)
        EventWaitlist.objects.create(email="b@test.com", event_name="Meetup", position=2)
    
    def test_fifo_order(self):
        first = EventWaitlist.get_next_in_queue("Meetup")
        self.assertEqual(first.email, "a@test.com")
    
    def test_promotion(self):
        person = EventWaitlist.get_next_in_queue("Meetup")
        person.promote()
        self.assertEqual(person.status, 'promoted')
        self.assertTrue(person.notified)
    
    def test_position_increment(self):
        entries = EventWaitlist.objects.filter(event_name="Meetup")
        self.assertEqual(entries.count(), 2)
        self.assertEqual(entries[0].position, 1)
        self.assertEqual(entries[1].position, 2)
