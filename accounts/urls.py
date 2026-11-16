"""
URL patterns for Accounts app (Auth, Profile, and Dashboards).
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Landing page
    path('', views.home_view, name='home'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Role Dashboards & Central Dispatcher
    path('dashboard/', views.dashboard_redirect_view, name='dashboard_redirect'),
    path('dashboard/officer/', views.officer_dashboard_view, name='officer_dashboard'),
    path('dashboard/member/', views.member_dashboard_view, name='member_dashboard'),

    # User Profile (Self only)
    path('profile/', views.profile_view, name='profile'),
]
