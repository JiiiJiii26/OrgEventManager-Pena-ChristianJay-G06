"""
Django admin configuration for Events app.
Registers Event and RSVP models with filtering, search, and list displays.
"""

from django.contrib import admin
from .models import Event, RSVP


class RSVPInline(admin.TabularInline):
    model = RSVP
    extra = 0
    readonly_fields = ('user', 'status', 'timestamp')
    can_delete = True


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'date_time',
        'venue',
        'capacity',
        'confirmed_attendees_display',
        'created_by',
        'created_at',
    )
    list_filter = ('date_time', 'venue', 'created_by')
    search_fields = ('title', 'venue', 'description', 'created_by__username')
    ordering = ('-date_time',)
    inlines = [RSVPInline]

    def confirmed_attendees_display(self, obj):
        return f"{obj.confirmed_count} / {obj.capacity}"
    confirmed_attendees_display.short_description = 'Confirmed RSVPs'


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status', 'timestamp')
    list_filter = ('status', 'timestamp', 'event')
    search_fields = ('user__username', 'user__email', 'user__full_name', 'event__title')
    ordering = ('-timestamp',)
