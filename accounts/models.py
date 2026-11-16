"""
Custom User Model for OrgEventManager with role-based access control.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user model supporting Officer (Admin) and Member (Customer) roles,
    unique email, contact details, and custom profile photo uploads.
    """
    class UserRole(models.TextChoices):
        OFFICER = 'OFFICER', 'Officer'
        MEMBER = 'MEMBER', 'Member'

    # Required unique email address
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.',
        },
        help_text='Required unique email address for login and notifications.'
    )

    # Full legal / display name
    full_name = models.CharField(
        max_length=150,
        help_text='Full name of the student organization member or officer.'
    )

    # Role designation: Officer (Admin) or Member (Customer)
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.MEMBER,
        help_text='Role in the organization (Officer or Member).'
    )

    # Optional contact number
    contact_number = models.CharField(
        max_length=25,
        blank=True,
        help_text='Active mobile or telephone contact number.'
    )

    # Optional profile photo (handled via MEDIA_ROOT/profile_photos/)
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        blank=True,
        null=True,
        help_text='Optional avatar image.'
    )

    # Ensure email and full_name are required when running createsuperuser
    REQUIRED_FIELDS = ['email', 'full_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_officer(self):
        """Returns True if the user has an Officer role or is a superuser."""
        return self.role == self.UserRole.OFFICER or self.is_superuser

    @property
    def is_member(self):
        """Returns True if the user has a Member role."""
        return self.role == self.UserRole.MEMBER

    @property
    def display_name(self):
        """Returns full name if available, otherwise falls back to username."""
        return self.full_name.strip() if self.full_name else self.username
