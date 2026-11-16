"""
Management command to seed test accounts for OrgEventManager.
Creates one Officer account and one Member account with securely hashed passwords.
Usage:
    python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds one Officer account and one Member test account with hashed passwords.'

    def handle(self, *args, **options):
        # 1. Officer Account
        officer_data = {
            'username': 'officer_alex',
            'email': 'officer@university.edu',
            'full_name': 'Alex Rivera (Student Council VP)',
            'role': User.UserRole.OFFICER,
            'contact_number': '+63 917 111 2222',
            'is_staff': True,  # Allows admin site access
        }
        officer_password = 'Password123!'

        officer, created = User.objects.get_or_create(
            username=officer_data['username'],
            defaults=officer_data
        )
        officer.set_password(officer_password)
        officer.role = User.UserRole.OFFICER
        officer.full_name = officer_data['full_name']
        officer.email = officer_data['email']
        officer.contact_number = officer_data['contact_number']
        officer.is_staff = True
        officer.save()

        if created:
            self.stdout.write(self.style.SUCCESS(
                f"[CREATED] Officer Account: {officer.username} | Email: {officer.email} | Role: {officer.role}"
            ))
        else:
            self.stdout.write(self.style.WARNING(
                f"[UPDATED] Officer Account: {officer.username} | Email: {officer.email} | Role: {officer.role}"
            ))

        # 2. Member Account
        member_data = {
            'username': 'member_taylor',
            'email': 'member@university.edu',
            'full_name': 'Taylor Santos (Active Member)',
            'role': User.UserRole.MEMBER,
            'contact_number': '+63 918 333 4444',
            'is_staff': False,
        }
        member_password = 'Password123!'

        member, created = User.objects.get_or_create(
            username=member_data['username'],
            defaults=member_data
        )
        member.set_password(member_password)
        member.role = User.UserRole.MEMBER
        member.full_name = member_data['full_name']
        member.email = member_data['email']
        member.contact_number = member_data['contact_number']
        member.is_staff = False
        member.save()

        if created:
            self.stdout.write(self.style.SUCCESS(
                f"[CREATED] Member Account: {member.username} | Email: {member.email} | Role: {member.role}"
            ))
        else:
            self.stdout.write(self.style.WARNING(
                f"[UPDATED] Member Account: {member.username} | Email: {member.email} | Role: {member.role}"
            ))

        self.stdout.write(self.style.SUCCESS(
            "\n"
            "===============================================================\n"
            "  TEST ACCOUNTS SEEDED SUCCESSFULLY:\n"
            "  1. Officer: username='officer_alex' or email='officer@university.edu'\n"
            "              password='Password123!'\n"
            "  2. Member:  username='member_taylor' or email='member@university.edu'\n"
            "              password='Password123!'\n"
            "===============================================================\n"
        ))
