from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.subscriptions.models import Plan
from apps.locations.models import SavedLocation
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds initial billing plans, cities, and a test user account for dynamic testing'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database metrics...')

        # 1. Billing Plans
        pro_plan, _ = Plan.objects.get_or_create(
            name='Aether Pro',
            defaults={
                'price': 9.99,
                'features': ['Hyperlocal radar alerts', 'Unlimited custom weather warning rules', 'Hourly AI Chat advisor responses', 'Farming seed guides'],
                'is_active': True
            }
        )
        ent_plan, _ = Plan.objects.get_or_create(
            name='Aether Enterprise',
            defaults={
                'price': 49.99,
                'features': ['Multiple custom locations monitoring', 'Custom Doppler sweep notifications', 'Priority API keys access', 'Dedicated agricultural logs digests'],
                'is_active': True
            }
        )
        self.stdout.write('Billing Plans populated.')

        # 2. Test User Account
        test_email = 'test@weather.app'
        user = User.objects.filter(email=test_email).first()
        if not user:
            user = User.objects.create_user(
                email=test_email,
                username='meteorologist',
                password='password123',
                is_email_verified=True,
                is_phone_verified=True,
            )
            self.stdout.write(f"Test account generated: {test_email} / password123")
        else:
            self.stdout.write('Test account already exists.')

        # 3. Add default bookmarked cities
        SavedLocation.objects.get_or_create(
            user=user,
            latitude=28.6139,
            longitude=77.2090,
            defaults={'name': 'New Delhi', 'country': 'IN', 'state': 'Delhi'}
        )
        SavedLocation.objects.get_or_create(
            user=user,
            latitude=51.5074,
            longitude=-0.1278,
            defaults={'name': 'London', 'country': 'GB', 'state': 'England'}
        )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully! Ready for action.'))
