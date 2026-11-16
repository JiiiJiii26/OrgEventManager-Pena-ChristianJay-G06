"""
Role-based access control decorators and mixins for OrgEventManager.
"""

from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin


def role_required(allowed_roles):
    """
    Decorator to restrict view access to specific user roles (e.g. 'OFFICER', 'MEMBER').
    Superusers are granted access across roles.
    If unauthorized, redirects user to their appropriate dashboard with an error alert.
    """
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check authentication
            if not request.user.is_authenticated:
                messages.error(request, 'Please log in to access this page.')
                return redirect('accounts:login')

            # Superusers bypass role checks
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Check if user's role is in allowed roles
            user_role = getattr(request.user, 'role', None)
            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)

            # Unauthorized role access attempt
            messages.error(
                request,
                f"Access denied: You do not have permission to view that page. "
                f"Required role: {', '.join(allowed_roles)}."
            )

            # Redirect user safely to their own role dashboard
            if user_role == 'OFFICER':
                return redirect('accounts:officer_dashboard')
            else:
                return redirect('accounts:member_dashboard')

        return _wrapped_view
    return decorator


def officer_required(view_func):
    """Convenience decorator restricting view to Officers only."""
    return role_required(['OFFICER'])(view_func)


def member_required(view_func):
    """Convenience decorator restricting view to Members only."""
    return role_required(['MEMBER'])(view_func)


class RoleRequiredMixin(AccessMixin):
    """
    Class-Based View mixin for enforcing role access.
    """
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.is_superuser or getattr(request.user, 'role', None) in self.allowed_roles:
            return super().dispatch(request, *args, **kwargs)

        messages.error(request, 'Access denied: You do not have permission to view that page.')
        if getattr(request.user, 'role', None) == 'OFFICER':
            return redirect('accounts:officer_dashboard')
        return redirect('accounts:member_dashboard')
