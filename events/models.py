"""
Events App Models - Phase 2 Core Feature.
Defines Event model with full CRUD attributes and relationship to CustomUser.
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
