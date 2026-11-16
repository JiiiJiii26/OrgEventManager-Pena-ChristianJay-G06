"""
Tests for Events app stub (Phase 2).
Verifies that all 5 URL names resolve and render without NoReverseMatch errors.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Event

User = get_user_model()


class EventsStubTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.officer = User.objects.create_user(
            username='officer_tester',
            email='officer_tester@university.edu',
            password='Password123!',
            role=User.UserRole.OFFICER
        )
        self.member = User.objects.create_user(
            username='member_tester',
            email='member_tester@university.edu',
            password='Password123!',
            role=User.UserRole.MEMBER
        )

    def test_minimal_event_model(self):
        event = Event.objects.create(title='Campus General Assembly')
        self.assertEqual(str(event), 'Campus General Assembly')
        self.assertIsNotNone(event.created_at)

    def test_officer_event_urls_resolve(self):
        self.client.login(username='officer_tester', password='Password123!')
        officer_routes = ['create_event', 'attendance_tracker', 'export_reports']
        for route_name in officer_routes:
            response = self.client.get(reverse(f'events:{route_name}'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'events/placeholder.html')

    def test_member_event_urls_resolve(self):
        self.client.login(username='member_tester', password='Password123!')
        member_routes = ['upcoming_events', 'my_rsvps']
        for route_name in member_routes:
            response = self.client.get(reverse(f'events:{route_name}'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'events/placeholder.html')
