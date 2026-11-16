"""
Events App Models (Phase 2 Stub).
Minimal Event model containing title and created_at only.
"""

from django.db import models


class Event(models.Model):
    """
    Minimal Event model for Phase 2 stub.
    Kept minimal so 0001_initial.py is trivial and correct.
    """
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
