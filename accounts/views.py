"""
Views for OrgEventManager Accounts app.
Handles Registration, Login, Logout, Role Dashboards, and Profile management.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import CustomUserCreationForm, CustomLoginForm, ProfileUpdateForm
from .decorators import officer_required, member_required


def home_view(request):
    """
    Public landing page for OrgEventManager.
    Authenticated users are redirected directly to their role-specific dashboard.
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard_redirect')
    return render(request, 'home.html')


def register_view(request):
    """
    User registration view.
    Validates required fields, email format, unique username/email,
    and creates a new user with hashed password.
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard_redirect')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f"Account created successfully for {user.display_name}! "
                f"You are registered as a {user.get_role_display()}. Please log in."
            )
            return redirect('accounts:login')
        else:
            messages.error(request, 'Registration failed. Please correct the highlighted errors.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Login view supporting authentication via either Username OR Email.
    Redirects to the user's role-specific dashboard or safe next URL.
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard_redirect')

    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=identifier, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.display_name}!")

                # Handle next parameter if safe
                next_url = request.GET.get('next') or request.POST.get('next')
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)

                # Role-based dashboard redirect
                return redirect('accounts:dashboard_redirect')
            else:
                messages.error(request, 'Invalid username/email or password. Please try again.')
    else:
        form = CustomLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    Logout view that ends the user session and redirects to the login page.
    """
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('accounts:login')


@login_required
def dashboard_redirect_view(request):
    """
    Central dispatcher routing authenticated users to their role dashboard.
    """
    if request.user.is_officer:
        return redirect('accounts:officer_dashboard')
    return redirect('accounts:member_dashboard')


@login_required
@officer_required
def officer_dashboard_view(request):
    """
    Officer (Admin) Dashboard:
    Provides navigation for creating events, tracking attendance, and exporting reports.
    Queries real events authored by the officer.
    """
    from django.utils import timezone
    from events.models import Event

    if request.user.is_superuser:
        events = Event.objects.all().order_by('-date_time')
    else:
        events = Event.objects.filter(created_by=request.user).order_by('-date_time')

    total_events = events.count()
    upcoming_count = events.filter(date_time__gte=timezone.now()).count()
    total_capacity = sum(e.capacity for e in events)

    context = {
        'page_title': 'Officer Dashboard',
        'active_tab': 'officer_dashboard',
        'stats': {
            'total_events': total_events,
            'upcoming_events': upcoming_count,
            'total_capacity': total_capacity,
        },
        'events': events[:5],
    }
    return render(request, 'accounts/officer_dashboard.html', context)


@login_required
@member_required
def member_dashboard_view(request):
    """
    Member (Customer) Dashboard:
    Displays upcoming organization events, RSVP actions, and personal attendance history.
    Queries real events and user RSVPs from Supabase.
    """
    from django.utils import timezone
    from events.models import Event, RSVP

    all_upcoming = Event.objects.filter(date_time__gte=timezone.now()).order_by('date_time')
    user_rsvps = {
        r.event_id: r.status
        for r in RSVP.objects.filter(user=request.user)
    }

    my_confirmed_rsvps = RSVP.objects.filter(user=request.user, status='GOING').count()
    total_upcoming = all_upcoming.count()

    upcoming_list = []
    for ev in all_upcoming[:4]:
        upcoming_list.append({
            'event': ev,
            'user_rsvp_status': user_rsvps.get(ev.id),
        })

    context = {
        'page_title': 'Member Dashboard',
        'active_tab': 'member_dashboard',
        'stats': {
            'upcoming_events': total_upcoming,
            'my_rsvps': my_confirmed_rsvps,
            'attendance_rate': f"{int((my_confirmed_rsvps / total_upcoming * 100))}%" if total_upcoming else "100%",
        },
        'upcoming_events_data': upcoming_list,
    }
    return render(request, 'accounts/member_dashboard.html', context)


@login_required
def profile_view(request):
    """
    User Profile View & Edit.
    Users can view and update their own full name, email, contact number, and profile photo.
    Restricted strictly to the currently logged-in user (no arbitrary ID access).
    """
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Failed to update profile. Please check the errors below.')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})
