"""
Views for Events app - Phase 2 Core Feature.
Implements Officer Event CRUD, Member RSVP attendance marking, and detail rosters.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from accounts.decorators import officer_required, member_required
from .models import Event, RSVP
from .forms import EventForm, RSVPForm


# ==============================================================================
# Officer CRUD Views
# ==============================================================================

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


create_event = event_create  # Alias for base.html compatibility


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
    Officer management table showing all events authored by this officer
    with live RSVP totals and quick actions.
    """
    if request.user.is_superuser:
        events = Event.objects.all().order_by('-date_time')
    else:
        events = Event.objects.filter(created_by=request.user).order_by('-date_time')

    return render(request, 'events/officer_event_list.html', {
        'events': events,
        'page_title': 'Officer Event Manager',
    })


@login_required
@officer_required
def attendance_tracker(request):
    """
    Officer Attendance Tracker: displays all organization events alongside
    confirmed attendee counts and roster inspection links.
    """
    events = Event.objects.all().order_by('-date_time')
    return render(request, 'events/attendance_tracker.html', {
        'events': events,
        'page_title': 'Live Attendance Tracker',
    })


@login_required
@officer_required
def export_reports(request):
    """
    Officer Export Reports stub / placeholder.
    """
    return render(request, 'events/placeholder.html', {
        'feature_title': 'Export Attendance & Event Reports',
        'badge_label': 'Officer Feature',
        'description': 'Automated PDF/CSV attendance rosters and analytical summaries will be exported here.',
        'back_url': 'accounts:officer_dashboard',
    })


# ==============================================================================
# Member & General Event Views
# ==============================================================================

@login_required
def upcoming_events(request):
    """
    Member View: Read-only directory of all future organization events.
    Displays venue, scheduled time, available spots, and the user's current RSVP status.
    """
    events = Event.objects.filter(date_time__gte=timezone.now()).order_by('date_time')

    # Annotate events with user's current RSVP status
    user_rsvps = {}
    if request.user.is_authenticated:
        user_rsvps = {
            r.event_id: r.status
            for r in RSVP.objects.filter(user=request.user)
        }

    events_data = []
    for ev in events:
        events_data.append({
            'event': ev,
            'user_rsvp_status': user_rsvps.get(ev.id),
        })

    return render(request, 'events/event_list.html', {
        'events_data': events_data,
        'page_title': 'Upcoming Organization Events',
    })


@login_required
def event_detail(request, pk):
    """
    Detailed event view:
    - Shows title, description, venue, scheduled date, capacity, and remaining spots.
    - Members: Interactive RSVP submission/toggle card.
    - Officers/Superusers: Full attendee roster table with member details and timestamps.
    """
    event = get_object_or_404(Event, pk=pk)
    user_rsvp = event.get_user_rsvp(request.user)
    attendees = event.rsvps.select_related('user').order_by('-timestamp')

    rsvp_form = RSVPForm(instance=user_rsvp) if user_rsvp else RSVPForm(initial={'status': RSVP.Status.GOING})

    return render(request, 'events/event_detail.html', {
        'event': event,
        'user_rsvp': user_rsvp,
        'attendees': attendees,
        'rsvp_form': rsvp_form,
        'page_title': event.title,
    })


@login_required
def rsvp_event(request, pk):
    """
    Handles POST requests from members marking or toggling their RSVP attendance.
    Validates capacity constraints before allowing a 'GOING' registration.
    """
    event = get_object_or_404(Event, pk=pk)

    if request.method != 'POST':
        return redirect('events:event_detail', pk=pk)

    status = request.POST.get('status', RSVP.Status.GOING)
    if status not in [RSVP.Status.GOING, RSVP.Status.NOT_GOING]:
        status = RSVP.Status.GOING

    existing_rsvp = RSVP.objects.filter(event=event, user=request.user).first()

    # Capacity check: cannot join if event is full and user was not already GOING
    if status == RSVP.Status.GOING and event.is_full and (not existing_rsvp or existing_rsvp.status != RSVP.Status.GOING):
        messages.error(
            request,
            f'Sorry, "{event.title}" has reached its maximum attendee capacity of {event.capacity}.'
        )
        return redirect('events:event_detail', pk=pk)

    rsvp_obj, created = RSVP.objects.update_or_create(
        event=event,
        user=request.user,
        defaults={'status': status}
    )

    if status == RSVP.Status.GOING:
        messages.success(
            request,
            f'You have successfully RSVPed as "Going" to {event.title}!'
        )
    else:
        messages.info(
            request,
            f'Your RSVP status has been updated to "Not Going" for {event.title}.'
        )

    return redirect('events:event_detail', pk=pk)


@login_required
@member_required
def my_rsvps(request):
    """
    Member View: Lists all events the member has registered attendance for.
    """
    rsvps = RSVP.objects.filter(user=request.user).select_related('event').order_by('-timestamp')

    return render(request, 'events/my_rsvps.html', {
        'rsvps': rsvps,
        'page_title': 'My Event RSVPs & Attendance History',
    })
