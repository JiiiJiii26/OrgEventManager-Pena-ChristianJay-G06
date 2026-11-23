"""
URL patterns for Events app.
Includes Officer CRUD, Member event directory, event details, and RSVP tracking.
"""

from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Officer CRUD
    path('create/', views.event_create, name='create_event'),
    path('create-new/', views.event_create, name='event_create'),
    path('manage/', views.officer_event_list, name='officer_event_list'),
    path('<int:pk>/edit/', views.event_update, name='event_update'),
    path('<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('attendance/', views.attendance_tracker, name='attendance_tracker'),
    path('reports/', views.export_reports, name='export_reports'),

    # Member Event Directory & RSVP
    path('', views.upcoming_events, name='event_list'),
    path('upcoming/', views.upcoming_events, name='upcoming_events'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('<int:pk>/rsvp/', views.rsvp_event, name='rsvp_event'),
    path('my-rsvps/', views.my_rsvps, name='my_rsvps'),
]
