"""
Views for Events app (Phase 2 Stub).
Defines all 5 stub views referenced in base.html:
- create_event
- attendance_tracker
- export_reports
- upcoming_events
- my_rsvps
All views render templates/events/placeholder.html.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import officer_required, member_required


@login_required
@officer_required
def create_event(request):
    """Stub view for Officer 'Create Event' feature."""
    return render(request, 'events/placeholder.html', {
        'feature_title': 'Create New Event',
        'badge_label': 'Officer Feature',
        'description': 'The Event Creation form and scheduler will be fully integrated here in Phase 2.',
        'back_url': 'accounts:officer_dashboard',
    })


@login_required
@officer_required
def attendance_tracker(request):
    """Stub view for Officer 'Attendance Tracker' feature."""
    return render(request, 'events/placeholder.html', {
        'feature_title': 'Attendance Tracker & Scanner',
        'badge_label': 'Officer Feature',
        'description': 'Live check-ins, QR code scanning, and roll-call tracking will be available in Phase 2.',
        'back_url': 'accounts:officer_dashboard',
    })


@login_required
@officer_required
def export_reports(request):
    """Stub view for Officer 'Export Reports' feature."""
    return render(request, 'events/placeholder.html', {
        'feature_title': 'Export Attendance & Event Reports',
        'badge_label': 'Officer Feature',
        'description': 'Automated PDF/CSV attendance rosters and analytical summaries will be exported here in Phase 2.',
        'back_url': 'accounts:officer_dashboard',
    })


@login_required
@member_required
def upcoming_events(request):
    """Stub view for Member 'Upcoming Events' listing."""
    return render(request, 'events/placeholder.html', {
        'feature_title': 'Organization Events Directory',
        'badge_label': 'Member Feature',
        'description': 'Browse all published campus organization events and RSVP in real time in Phase 2.',
        'back_url': 'accounts:member_dashboard',
    })


@login_required
@member_required
def my_rsvps(request):
    """Stub view for Member 'My RSVPs' listing."""
    return render(request, 'events/placeholder.html', {
        'feature_title': 'My Event RSVPs & Attendance History',
        'badge_label': 'Member Feature',
        'description': 'Review your confirmed RSVPs, ticket passes, and personal attendance history in Phase 2.',
        'back_url': 'accounts:member_dashboard',
    })
