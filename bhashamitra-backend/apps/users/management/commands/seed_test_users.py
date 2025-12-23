"""Seed test users for all subscription tiers."""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User
from apps.children.models import Child


class Command(BaseCommand):
    help = 'Create test users for all subscription tiers (FREE, STANDARD, PREMIUM)'

    def handle(self, *args, **options):
        test_users = [
            {
                'email': 'free@test.com',
                'password': 'test1234',
                'name': 'Free Tier Parent',
                'subscription_tier': 'FREE',
                'child_name': 'Aarav',
                'child_age': 5,
            },
            {
                'email': 'standard@test.com',
                'password': 'test1234',
                'name': 'Standard Tier Parent',
                'subscription_tier': 'STANDARD',
                'child_name': 'Priya',
                'child_age': 7,
            },
            {
                'email': 'premium@test.com',
                'password': 'test1234',
                'name': 'Premium Tier Parent',
                'subscription_tier': 'PREMIUM',
                'child_name': 'Arjun',
                'child_age': 10,
            },
        ]

        created_users = 0
        updated_users = 0
        created_children = 0

        for user_data in test_users:
            email = user_data['email']
            password = user_data['password']
            name = user_data['name']
            tier = user_data['subscription_tier']
            child_name = user_data['child_name']
            child_age = user_data['child_age']

            # Create or update user
            user, created = User.objects.update_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'name': name,
                    'subscription_tier': tier,
                    'subscription_expires_at': timezone.now() + timedelta(days=365) if tier != 'FREE' else None,
                }
            )

            # Set password
            user.set_password(password)
            user.save()

            if created:
                created_users += 1
                self.stdout.write(self.style.SUCCESS(f'Created user: {email} ({tier})'))
            else:
                updated_users += 1
                self.stdout.write(self.style.WARNING(f'Updated user: {email} ({tier})'))

            # Create child profile if doesn't exist
            # Calculate date of birth from age
            from datetime import date
            birth_year = date.today().year - child_age
            dob = date(birth_year, 6, 15)  # Use June 15 as default birthday

            child, child_created = Child.objects.get_or_create(
                user=user,
                name=child_name,
                defaults={
                    'date_of_birth': dob,
                    'avatar': '🧒' if child_age < 8 else '👦',
                    'language': 'HINDI',
                    'level': 1 if child_age <= 5 else (3 if child_age <= 7 else 6),
                }
            )

            if child_created:
                created_children += 1
                self.stdout.write(self.style.SUCCESS(f'  Created child: {child_name} (age {child_age})'))
            else:
                self.stdout.write(f'  Child exists: {child_name}')

        # Print summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('TEST ACCOUNTS CREATED'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write('')
        self.stdout.write('Login credentials (password: test1234):')
        self.stdout.write('')
        self.stdout.write(self.style.HTTP_INFO('FREE TIER:'))
        self.stdout.write('  Email: free@test.com')
        self.stdout.write('  Features: Cache-only TTS, 4 stories, no games/videos')
        self.stdout.write('')
        self.stdout.write(self.style.HTTP_INFO('STANDARD TIER ($12/mo):'))
        self.stdout.write('  Email: standard@test.com')
        self.stdout.write('  Features: Svara TTS, 8 stories, games/videos access')
        self.stdout.write('')
        self.stdout.write(self.style.HTTP_INFO('PREMIUM TIER ($20/mo):'))
        self.stdout.write('  Email: premium@test.com')
        self.stdout.write('  Features: Sarvam AI TTS, unlimited stories, all features')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Summary: {created_users} users created, {updated_users} updated, {created_children} children created'))
