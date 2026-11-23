"""
Django admin configuration for Events app.
"""

from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_time', 'venue', 'capacity', 'created_by', 'created_at')
    list_filter = ('date_time', 'venue', 'created_by')
    search_fields = ('title', 'venue', 'description', 'created_by__username')
    ordering = ('-date_time',)
