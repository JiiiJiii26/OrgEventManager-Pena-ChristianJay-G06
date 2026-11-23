"""
Forms for Events app.
Handles Event creation/updating and Member RSVP submissions.
"""

from django import forms
from django.utils import timezone
from .models import Event, RSVP


class EventForm(forms.ModelForm):
    """
    Form for Officers to create and update organization events.
    Enforces validation ensuring event dates cannot be scheduled in the past.
    """
    class Meta:
        model = Event
        fields = ['title', 'description', 'date_time', 'venue', 'capacity']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Tech Stack Workshop 2026',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Provide details, objectives, prerequisites, and instructions for attendees...',
            }),
            'date_time': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                }
            ),
            'venue': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. CS Lab 301 / University Auditorium',
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'e.g. 50',
            }),
        }

    def clean_date_time(self):
        date_time = self.cleaned_data.get('date_time')
        if date_time and date_time < timezone.now():
            raise forms.ValidationError('Event date and time cannot be scheduled in the past.')
        return date_time

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity is not None and capacity <= 0:
            raise forms.ValidationError('Event capacity must be at least 1 attendee.')
        return capacity


class RSVPForm(forms.ModelForm):
    """
    Form for Members to indicate attendance status (GOING / NOT_GOING).
    """
    class Meta:
        model = RSVP
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control form-select',
            })
        }
