from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Seed test users for MVP launch testing'

    def handle(self, *args, **options):
        # Test users data
        test_users = [
            {
                'email': 'free@test.com',
                'password': 'test1234',
                'tier': 'FREE',
                'name': 'Free Test Parent',
                'email_verified': True,
                'onboarded': True
            },
            {
                'email': 'standard@test.com',
                'password': 'test1234',
                'tier': 'STANDARD',
                'name': 'Standard Test Parent',
                'email_verified': True,
                'onboarded': True,
                'expires_in_days': 30
            },
            {
                'email': 'premium@test.com',
                'password': 'test1234',
                'tier': 'PREMIUM',
                'name': 'Premium Test Parent',
                'email_verified': True,
                'onboarded': True,
                'expires_in_days': 30
            }
        ]

        created_count = 0
        
        for user_data in test_users:
            # Create or get user
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    'username': user_data['email'].split('@')[0],
                    'is_active': True
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✅ Created user: {user_data["email"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️  User already exists: {user_data["email"]}'))
            
            # Update user fields
            user.name = user_data['name']
            user.subscription_tier = user_data['tier']
            user.email_verified = user_data['email_verified']
            user.is_onboarded = user_data['onboarded']
            
            # Set subscription expiration for paid tiers
            if user_data['tier'] != 'FREE':
                expires_in_days = user_data.get('expires_in_days', 30)
                user.subscription_expires_at = timezone.now() + timedelta(days=expires_in_days)
            else:
                user.subscription_expires_at = None
            
            user.save()
            
            # Log user status
            tier_info = f"{user_data['tier']}"
            if user_data['tier'] != 'FREE':
                tier_info += f" (expires: {user.subscription_expires_at.strftime('%Y-%m-%d')})"
            
            self.stdout.write(f'  📊 Tier: {tier_info}')
            self.stdout.write(f'  ✅ Email Verified: {user.email_verified}')
            self.stdout.write(f'  ✅ Onboarded: {user.is_onboarded}')
            self.stdout.write(f'  🎯 TTS Provider: {user.tts_provider}')
            self.stdout.write('')
        
        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Successfully processed {len(test_users)} test users!')
        )
        self.stdout.write(f'📊 Created {created_count} new users')
        self.stdout.write('\n📋 Test Credentials:')
        self.stdout.write('  FREE: free@test.com / test1234')
        self.stdout.write('  STANDARD: standard@test.com / test1234')
        self.stdout.write('  PREMIUM: premium@test.com / test1234')
