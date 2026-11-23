"""
Events App Models - Phase 2 Core Feature.
Defines Event and RSVP models with attendance metrics and relational constraints.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone


class Event(models.Model):
    """
    Event model for organization events created and managed by Officers.
    """
    title = models.CharField(
        max_length=200,
        help_text='Title of the organization event.'
    )
    description = models.TextField(
        blank=True,
        default='',
        help_text='Detailed description, agenda, or guidelines for attendees.'
    )
    date_time = models.DateTimeField(
        default=timezone.now,
        help_text='Scheduled date and time of the event.'
    )
    venue = models.CharField(
        max_length=255,
        default='Campus Auditorium',
        help_text='Location, room, or meeting URL.'
    )
    capacity = models.PositiveIntegerField(
        default=50,
        help_text='Maximum number of allowed attendees.'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_events',
        null=True,
        blank=True,
        help_text='Officer who authored/organized this event.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_time', '-created_at']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return f"{self.title} ({self.date_time.strftime('%b %d, %Y %I:%M %p')})"

    @property
    def is_past(self):
        """Returns True if the event has already concluded."""
        return self.date_time < timezone.now()

    @property
    def confirmed_rsvps(self):
        """Returns QuerySet of confirmed attendee RSVPs."""
        return self.rsvps.filter(status='GOING').select_related('user')

    @property
    def confirmed_count(self):
        """Number of confirmed attendees."""
        return self.confirmed_rsvps.count()

    @property
    def available_spots(self):
        """Remaining RSVP slots before capacity is reached."""
        return max(0, self.capacity - self.confirmed_count)

    @property
    def is_full(self):
        """Returns True if confirmed RSVPs have reached maximum capacity."""
        return self.confirmed_count >= self.capacity

    def get_user_rsvp(self, user):
        """Helper to retrieve a specific user's RSVP status for this event."""
        if not user.is_authenticated:
            return None
        return self.rsvps.filter(user=user).first()


class RSVP(models.Model):
    """
    RSVP model capturing member attendance intentions for organization events.
    Constrained to one unique RSVP record per user per event.
    """
    class Status(models.TextChoices):
        GOING = 'GOING', 'Going'
        NOT_GOING = 'NOT_GOING', 'Not Going'

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='rsvps',
        help_text='Event being RSVPed to.'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rsvps',
        help_text='Student member submitting the RSVP.'
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.GOING,
        help_text='Attendance status.'
    )
    timestamp = models.DateTimeField(
        auto_now=True,
        help_text='Timestamp of the last status update.'
    )

    class Meta:
        unique_together = ('event', 'user')
        ordering = ['-timestamp']
        verbose_name = 'RSVP'
        verbose_name_plural = 'RSVPs'

    def __str__(self):
        return f"{self.user.username} -> {self.event.title} ({self.get_status_display()})"
