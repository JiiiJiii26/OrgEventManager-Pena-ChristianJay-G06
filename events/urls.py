"""
URL patterns for Events app.
Maps Officer CRUD views and preserves compatibility with base.html.
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

    # Phase 1 & 2 navigation endpoints
    path('attendance/', views.attendance_tracker, name='attendance_tracker'),
    path('reports/', views.export_reports, name='export_reports'),
    path('upcoming/', views.upcoming_events, name='upcoming_events'),
    path('my-rsvps/', views.my_rsvps, name='my_rsvps'),
]
