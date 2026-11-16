"""
Authentication and Profile Forms for OrgEventManager.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    Registration form with required fields, role selection, unique email validation,
    and automatic password hashing via UserCreationForm.
    """
    full_name = forms.CharField(
        max_length=150,
        required=True,
        label='Full Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. Maria Santos',
            'autocomplete': 'name',
        })
    )

    email = forms.EmailField(
        required=True,
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. maria.santos@university.edu',
            'autocomplete': 'email',
        })
    )

    contact_number = forms.CharField(
        max_length=25,
        required=False,
        label='Contact Number (Optional)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. +63 917 123 4567',
            'autocomplete': 'tel',
        })
    )

    role = forms.ChoiceField(
        choices=User.UserRole.choices,
        initial=User.UserRole.MEMBER,
        required=True,
        label='Account Role',
        help_text='Select Member for general attendees, or Officer for event organizers.',
        widget=forms.Select(attrs={
            'class': 'form-control form-select',
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
            'email',
            'full_name',
            'contact_number',
            'role',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply clean styling classes to username and password fields
        for field_name in ['username', 'password1', 'password2']:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError('Username is required.')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('A user with that username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Email address is required.')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('A user with that email already exists.')
        return email.lower()


class CustomLoginForm(forms.Form):
    """
    Login form allowing users to authenticate with either Username or Email.
    """
    username_or_email = forms.CharField(
        label='Username or Email',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username or email address',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
        })
    )


class ProfileUpdateForm(forms.ModelForm):
    """
    Form allowing users to view and update their own profile details.
    """
    email = forms.EmailField(
        required=True,
        label='Email Address',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = [
            'full_name',
            'email',
            'contact_number',
            'profile_photo',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Email address is required.')
        # Check uniqueness excluding the current user instance
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('This email address is already in use by another account.')
        return email.lower()


class CustomUserAdminChangeForm(UserChangeForm):
    """Admin change form for CustomUser."""
    class Meta(UserChangeForm.Meta):
        model = User
