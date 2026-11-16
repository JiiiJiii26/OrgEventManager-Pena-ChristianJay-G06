"""
URL patterns for Events app (Phase 2 Stub).
Defines ALL 5 URL names referenced by base.html:
- create_event
- attendance_tracker
- export_reports
- upcoming_events
- my_rsvps
"""

from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Officer feature stubs
    path('create/', views.create_event, name='create_event'),
    path('attendance/', views.attendance_tracker, name='attendance_tracker'),
    path('reports/', views.export_reports, name='export_reports'),

    # Member feature stubs
    path('upcoming/', views.upcoming_events, name='upcoming_events'),
    path('my-rsvps/', views.my_rsvps, name='my_rsvps'),
]
