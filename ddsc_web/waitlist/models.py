from django.db import models
from django.utils import timezone

class EventWaitlist(models.Model):
    """FIFO event waitlist with auto-promotion"""
    email = models.EmailField()
    event_name = models.CharField(max_length=200)
    position = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('waiting', 'Waiting'),
            ('promoted', 'Promoted'),
            ('registered', 'Registered'),
            ('cancelled', 'Cancelled'),
        ],
        default='waiting'
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    promoted_at = models.DateTimeField(null=True, blank=True)
    notified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['position']
        indexes = [
            models.Index(fields=['event_name', 'status']),
            models.Index(fields=['position']),
        ]
    
    def __str__(self):
        return f"{self.email} - {self.event_name} (#{self.position})"
    
    def promote(self):
        """Promote from waitlist, mark notified"""
        self.status = 'promoted'
        self.promoted_at = timezone.now()
        self.notified = True
        self.save()
        return True
    
    @staticmethod
    def get_next_in_queue(event_name):
        """Get next waiting person in FIFO order"""
        return EventWaitlist.objects.filter(
            event_name=event_name,
            status='waiting'
        ).first()
