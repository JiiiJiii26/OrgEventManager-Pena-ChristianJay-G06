"""
Automated unit & integration tests for Events app.
Tests Officer Event CRUD, past-date validation, Member RSVP logic,
capacity constraints, and role permissions.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import Event, RSVP

User = get_user_model()


class EventCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.officer = User.objects.create_user(
            username='officer_tester',
            email='officer_tester@university.edu',
            password='Password123!',
            role=User.UserRole.OFFICER,
            full_name='Officer Tester'
        )
        self.member = User.objects.create_user(
            username='member_tester',
            email='member_tester@university.edu',
            password='Password123!',
            role=User.UserRole.MEMBER,
            full_name='Member Tester'
        )

    def test_officer_can_create_event(self):
        self.client.login(username='officer_tester', password='Password123!')
        future_date = timezone.now() + timedelta(days=7)
        response = self.client.post(reverse('events:event_create'), {
            'title': 'General Orientation 2026',
            'description': 'Welcome assembly for all members.',
            'date_time': future_date.strftime('%Y-%m-%dT%H:%M'),
            'venue': 'Main Auditorium',
            'capacity': 100,
        }, follow=True)
        self.assertRedirects(response, reverse('events:officer_event_list'))
        created = Event.objects.filter(title='General Orientation 2026').first()
        self.assertIsNotNone(created)
        self.assertEqual(created.created_by, self.officer)
        self.assertEqual(created.capacity, 100)

    def test_event_cannot_be_scheduled_in_past(self):
        self.client.login(username='officer_tester', password='Password123!')
        past_date = timezone.now() - timedelta(days=2)
        response = self.client.post(reverse('events:event_create'), {
            'title': 'Past Gathering',
            'description': 'This event should fail validation.',
            'date_time': past_date.strftime('%Y-%m-%dT%H:%M'),
            'venue': 'Old Room',
            'capacity': 50,
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'date_time', 'Event date and time cannot be scheduled in the past.')
        self.assertFalse(Event.objects.filter(title='Past Gathering').exists())

    def test_officer_can_update_event(self):
        event = Event.objects.create(
            title='Old Title',
            venue='Room 101',
            capacity=30,
            date_time=timezone.now() + timedelta(days=3),
            created_by=self.officer
        )
        self.client.login(username='officer_tester', password='Password123!')
        new_date = timezone.now() + timedelta(days=5)
        response = self.client.post(reverse('events:event_update', args=[event.pk]), {
            'title': 'Updated Title',
            'description': 'Updated description.',
            'date_time': new_date.strftime('%Y-%m-%dT%H:%M'),
            'venue': 'Room 202',
            'capacity': 45,
        }, follow=True)
        self.assertRedirects(response, reverse('events:officer_event_list'))
        event.refresh_from_db()
        self.assertEqual(event.title, 'Updated Title')
        self.assertEqual(event.venue, 'Room 202')
        self.assertEqual(event.capacity, 45)

    def test_officer_can_delete_event(self):
        event = Event.objects.create(
            title='To Be Deleted',
            venue='Room 999',
            capacity=10,
            date_time=timezone.now() + timedelta(days=1),
            created_by=self.officer
        )
        self.client.login(username='officer_tester', password='Password123!')
        response = self.client.post(reverse('events:event_delete', args=[event.pk]), follow=True)
        self.assertRedirects(response, reverse('events:officer_event_list'))
        self.assertFalse(Event.objects.filter(pk=event.pk).exists())

    def test_member_denied_from_event_create(self):
        self.client.login(username='member_tester', password='Password123!')
        response = self.client.get(reverse('events:event_create'), follow=True)
        self.assertRedirects(response, reverse('accounts:member_dashboard'))
        self.assertContains(response, 'Access denied')


class RSVPAttendanceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.officer = User.objects.create_user(
            username='event_officer',
            email='officer@university.edu',
            password='Password123!',
            role=User.UserRole.OFFICER,
            full_name='Lead Officer'
        )
        self.member1 = User.objects.create_user(
            username='member_one',
            email='member1@university.edu',
            password='Password123!',
            role=User.UserRole.MEMBER,
            full_name='Member One'
        )
        self.member2 = User.objects.create_user(
            username='member_two',
            email='member2@university.edu',
            password='Password123!',
            role=User.UserRole.MEMBER,
            full_name='Member Two'
        )
        self.event = Event.objects.create(
            title='Coding Hackathon 2026',
            description='24-hour collaborative sprint.',
            date_time=timezone.now() + timedelta(days=10),
            venue='Innovation Hub',
            capacity=2,
            created_by=self.officer
        )

    def test_member_can_rsvp_going(self):
        self.client.login(username='member_one', password='Password123!')
        response = self.client.post(
            reverse('events:rsvp_event', args=[self.event.pk]),
            {'status': 'GOING'},
            follow=True
        )
        self.assertRedirects(response, reverse('events:event_detail', args=[self.event.pk]))
        rsvp = RSVP.objects.filter(event=self.event, user=self.member1).first()
        self.assertIsNotNone(rsvp)
        self.assertEqual(rsvp.status, 'GOING')
        self.assertEqual(self.event.confirmed_count, 1)
        self.assertEqual(self.event.available_spots, 1)

    def test_member_can_update_rsvp_to_not_going(self):
        RSVP.objects.create(event=self.event, user=self.member1, status='GOING')
        self.client.login(username='member_one', password='Password123!')
        response = self.client.post(
            reverse('events:rsvp_event', args=[self.event.pk]),
            {'status': 'NOT_GOING'},
            follow=True
        )
        self.assertRedirects(response, reverse('events:event_detail', args=[self.event.pk]))
        rsvp = RSVP.objects.filter(event=self.event, user=self.member1).first()
        self.assertEqual(rsvp.status, 'NOT_GOING')
        self.assertEqual(self.event.confirmed_count, 0)
        self.assertEqual(self.event.available_spots, 2)

    def test_capacity_limit_blocks_overflow_rsvp(self):
        # Fill event capacity (capacity=2)
        RSVP.objects.create(event=self.event, user=self.member1, status='GOING')
        other_user = User.objects.create_user(
            username='extra_user', email='extra@u.edu', password='Password123!'
        )
        RSVP.objects.create(event=self.event, user=other_user, status='GOING')
        self.assertTrue(self.event.is_full)

        # member2 tries to RSVP GOING to full event
        self.client.login(username='member_two', password='Password123!')
        response = self.client.post(
            reverse('events:rsvp_event', args=[self.event.pk]),
            {'status': 'GOING'},
            follow=True
        )
        self.assertRedirects(response, reverse('events:event_detail', args=[self.event.pk]))
        self.assertContains(response, 'has reached its maximum attendee capacity')
        self.assertFalse(RSVP.objects.filter(event=self.event, user=self.member2).exists())

    def test_officer_sees_attendee_roster_in_event_detail(self):
        RSVP.objects.create(event=self.event, user=self.member1, status='GOING')
        self.client.login(username='event_officer', password='Password123!')
        response = self.client.get(reverse('events:event_detail', args=[self.event.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Attendee Roster & Attendance Tracking')
        self.assertContains(response, 'Member One')
        self.assertContains(response, 'member1@university.edu')
