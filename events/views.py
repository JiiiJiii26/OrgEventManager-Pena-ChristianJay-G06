"""
Views for Events app.
Implements Officer CRUD views and keeps aliases for base.html compatibility.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import officer_required, member_required
from .models import Event
from .forms import EventForm


@login_required
@officer_required
def event_create(request):
    """
    Officer view to create a new organization event.
    Automatically assigns created_by to the logged-in officer.
    """
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(
                request,
                f'Event "{event.title}" has been successfully published!'
            )
            return redirect('events:officer_event_list')
        else:
            messages.error(request, 'Please correct the errors in the event form.')
    else:
        form = EventForm()

    return render(request, 'events/event_form.html', {
        'form': form,
        'page_title': 'Create New Event',
        'is_update': False,
    })


# Alias for base.html compatibility
create_event = event_create


@login_required
@officer_required
def event_update(request, pk):
    """
    Officer view to edit an existing organization event.
    """
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'Event "{event.title}" details have been updated successfully!'
            )
            return redirect('events:officer_event_list')
        else:
            messages.error(request, 'Please correct the highlighted errors.')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/event_form.html', {
        'form': form,
        'event': event,
        'page_title': f'Edit Event: {event.title}',
        'is_update': True,
    })


@login_required
@officer_required
def event_delete(request, pk):
    """
    Officer view to confirm and delete an event.
    """
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        title = event.title
        event.delete()
        messages.success(request, f'Event "{title}" has been permanently deleted.')
        return redirect('events:officer_event_list')

    return render(request, 'events/event_confirm_delete.html', {
        'event': event,
        'page_title': f'Confirm Deletion: {event.title}',
    })


@login_required
@officer_required
def officer_event_list(request):
    """
    Officer management table showing all events authored by this officer.
    """
    if request.user.is_superuser:
        events = Event.objects.all().order_by('-date_time')
    else:
        events = Event.objects.filter(created_by=request.user).order_by('-date_time')

    return render(request, 'events/officer_event_list.html', {
        'events': events,
        'page_title': 'Officer Event Manager',
    })


# Placeholder / stub endpoints preserved for Phase 1 base.html compatibility
@login_required
@officer_required
def attendance_tracker(request):
    return render(request, 'events/placeholder.html', {
        'feature_title': 'Attendance Tracker & Scanner',
        'badge_label': 'Officer Feature',
        'description': 'Live check-ins, QR code scanning, and roll-call tracking will be available in Phase 2.',
        'back_url': 'accounts:officer_dashboard',
    })


@login_required
@officer_required
def export_reports(request):
    return render(request, 'events/placeholder.html', {
        'feature_title': 'Export Attendance & Event Reports',
        'badge_label': 'Officer Feature',
        'description': 'Automated PDF/CSV attendance rosters and analytical summaries will be exported here.',
        'back_url': 'accounts:officer_dashboard',
    })


@login_required
@member_required
def upcoming_events(request):
    return render(request, 'events/placeholder.html', {
        'feature_title': 'Organization Events Directory',
        'badge_label': 'Member Feature',
        'description': 'Browse all published campus organization events and RSVP in real time.',
        'back_url': 'accounts:member_dashboard',
    })


@login_required
@member_required
def my_rsvps(request):
    return render(request, 'events/placeholder.html', {
        'feature_title': 'My Event RSVPs & Attendance History',
        'badge_label': 'Member Feature',
        'description': 'Review your confirmed RSVPs, ticket passes, and personal attendance history.',
        'back_url': 'accounts:member_dashboard',
    })
