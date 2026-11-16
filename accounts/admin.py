"""
Django Admin configuration for CustomUser model.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserAdminChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Enhanced UserAdmin with support for custom role, full_name,
    contact_number, and profile_photo fields.
    """
    add_form = CustomUserCreationForm
    form = CustomUserAdminChangeForm
    model = CustomUser

    list_display = (
        'username',
        'email',
        'full_name',
        'role',
        'contact_number',
        'is_staff',
        'is_active',
        'date_joined',
    )
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'full_name', 'contact_number')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {
            'fields': ('full_name', 'email', 'contact_number', 'profile_photo')
        }),
        ('Role & Permissions', {
            'fields': (
                'role',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'full_name',
                'role',
                'contact_number',
                'password1',
                'password2',
            ),
        }),
    )
