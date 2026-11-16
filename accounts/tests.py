"""
Comprehensive Unit & Integration Tests for OrgEventManager Accounts App.
Tests Custom User Model, Dual Auth (Username/Email), Role Access Control,
Registration with Password Hashing, and Self-Profile Management.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserModelTests(TestCase):
    """Unit tests for CustomUser model and role attributes."""

    def test_create_member_user(self):
        user = User.objects.create_user(
            username='student1',
            email='student1@university.edu',
            password='TestPassword123!',
            full_name='Juan Santos',
            role=User.UserRole.MEMBER
        )
        self.assertEqual(user.role, User.UserRole.MEMBER)
        self.assertTrue(user.is_member)
        self.assertFalse(user.is_officer)
        self.assertEqual(user.display_name, 'Juan Santos')
        # Password must be hashed, never plain text
        self.assertNotEqual(user.password, 'TestPassword123!')
        self.assertTrue(user.check_password('TestPassword123!'))

    def test_create_officer_user(self):
        officer = User.objects.create_user(
            username='lead_officer',
            email='officer@university.edu',
            password='TestPassword123!',
            full_name='Maria Clara',
            role=User.UserRole.OFFICER
        )
        self.assertEqual(officer.role, User.UserRole.OFFICER)
        self.assertTrue(officer.is_officer)
        self.assertFalse(officer.is_member)

    def test_email_uniqueness_enforced(self):
        User.objects.create_user(
            username='user1',
            email='duplicate@university.edu',
            password='Password123!',
            full_name='User One'
        )
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='user2',
                email='duplicate@university.edu',
                password='Password123!',
                full_name='User Two'
            )


class RegistrationAndAuthTests(TestCase):
    """Tests for Registration and Dual-Login (Username / Email)."""

    def setUp(self):
        self.client = Client()
        self.officer = User.objects.create_user(
            username='alex_officer',
            email='alex@university.edu',
            password='SecurePassword123!',
            full_name='Alex Rivera',
            role=User.UserRole.OFFICER
        )
        self.member = User.objects.create_user(
            username='taylor_member',
            email='taylor@university.edu',
            password='SecurePassword123!',
            full_name='Taylor Swift',
            role=User.UserRole.MEMBER
        )

    def test_registration_view_get(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_registration_success_hashes_password(self):
        payload = {
            'username': 'new_member',
            'email': 'newmember@university.edu',
            'full_name': 'New Student',
            'contact_number': '+63 912 345 6789',
            'role': User.UserRole.MEMBER,
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        response = self.client.post(reverse('accounts:register'), data=payload, follow=True)
        self.assertRedirects(response, reverse('accounts:login'))
        created = User.objects.filter(username='new_member').first()
        self.assertIsNotNone(created)
        self.assertNotEqual(created.password, 'StrongPass123!')
        self.assertTrue(created.check_password('StrongPass123!'))

    def test_login_with_username(self):
        response = self.client.post(reverse('accounts:login'), {
            'username_or_email': 'alex_officer',
            'password': 'SecurePassword123!',
        }, follow=True)
        # Should redirect to Officer dashboard
        self.assertRedirects(response, reverse('accounts:officer_dashboard'))

    def test_login_with_email(self):
        response = self.client.post(reverse('accounts:login'), {
            'username_or_email': 'taylor@university.edu',
            'password': 'SecurePassword123!',
        }, follow=True)
        # Should redirect to Member dashboard
        self.assertRedirects(response, reverse('accounts:member_dashboard'))

    def test_login_invalid_credentials_shows_error(self):
        response = self.client.post(reverse('accounts:login'), {
            'username_or_email': 'alex_officer',
            'password': 'WrongPassword!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username/email or password')

    def test_logout_redirects_to_login(self):
        self.client.login(username='alex_officer', password='SecurePassword123!')
        response = self.client.get(reverse('accounts:logout'), follow=True)
        self.assertRedirects(response, reverse('accounts:login'))


class RoleAccessControlTests(TestCase):
    """Tests enforcing role permissions on dashboards."""

    def setUp(self):
        self.client = Client()
        self.officer = User.objects.create_user(
            username='officer1',
            email='officer1@university.edu',
            password='Password123!',
            full_name='Officer One',
            role=User.UserRole.OFFICER
        )
        self.member = User.objects.create_user(
            username='member1',
            email='member1@university.edu',
            password='Password123!',
            full_name='Member One',
            role=User.UserRole.MEMBER
        )

    def test_unauthenticated_redirected_to_login(self):
        for path in [reverse('accounts:officer_dashboard'), reverse('accounts:member_dashboard'), reverse('accounts:profile')]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(reverse('accounts:login') in response.url)

    def test_officer_can_access_officer_dashboard(self):
        self.client.login(username='officer1', password='Password123!')
        response = self.client.get(reverse('accounts:officer_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/officer_dashboard.html')

    def test_member_blocked_from_officer_dashboard(self):
        self.client.login(username='member1', password='Password123!')
        response = self.client.get(reverse('accounts:officer_dashboard'), follow=True)
        # Should be redirected to their member dashboard with access denied error
        self.assertRedirects(response, reverse('accounts:member_dashboard'))
        self.assertContains(response, 'Access denied')

    def test_member_can_access_member_dashboard(self):
        self.client.login(username='member1', password='Password123!')
        response = self.client.get(reverse('accounts:member_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/member_dashboard.html')

    def test_officer_blocked_from_member_dashboard(self):
        self.client.login(username='officer1', password='Password123!')
        response = self.client.get(reverse('accounts:member_dashboard'), follow=True)
        # Should be redirected to officer dashboard with access denied error
        self.assertRedirects(response, reverse('accounts:officer_dashboard'))
        self.assertContains(response, 'Access denied')


class ProfileSelfAccessTests(TestCase):
    """Tests self-profile viewing and updates."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='johndoe',
            email='john@university.edu',
            password='Password123!',
            full_name='John Doe',
            contact_number='+63 900 000 0000',
            role=User.UserRole.MEMBER
        )

    def test_profile_view_and_update(self):
        self.client.login(username='johndoe', password='Password123!')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')

        # Update profile
        update_data = {
            'full_name': 'Jonathan Doe Jr.',
            'email': 'jonathan@university.edu',
            'contact_number': '+63 999 888 7777',
        }
        post_response = self.client.post(reverse('accounts:profile'), data=update_data, follow=True)
        self.assertRedirects(post_response, reverse('accounts:profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.full_name, 'Jonathan Doe Jr.')
        self.assertEqual(self.user.email, 'jonathan@university.edu')
        self.assertEqual(self.user.contact_number, '+63 999 888 7777')
