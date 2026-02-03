"""Management command to create test users for all tiers."""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.children.models import Child

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test users for all subscription tiers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete existing test users before creating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Deleting existing test users...')
            User.objects.filter(email__endswith='@test.com').delete()
            self.stdout.write(self.style.SUCCESS('Deleted test users'))

        test_users = [
            # FREE TIER
            {
                'email': 'parent.free@test.com',
                'password': 'Test@123',
                'name': 'Test Free Parent',
                'tier': 'FREE',
                'children': [
                    {'name': 'Free Child 1', 'avatar': '🐼'},
                ],
            },
            # STANDARD TIER
            {
                'email': 'parent.standard@test.com',
                'password': 'Test@123',
                'name': 'Test Standard Parent',
                'tier': 'STANDARD',
                'children': [
                    {'name': 'Standard Child 1', 'avatar': '🦊'},
                    {'name': 'Standard Child 2', 'avatar': '🐰'},
                ],
            },
            # PREMIUM TIER
            {
                'email': 'parent.premium@test.com',
                'password': 'Test@123',
                'name': 'Test Premium Parent',
                'tier': 'PREMIUM',
                'children': [
                    {'name': 'Premium Child 1', 'avatar': '🦁'},
                    {'name': 'Premium Child 2', 'avatar': '🐯'},
                    {'name': 'Premium Child 3', 'avatar': '🐻'},
                ],
            },
        ]

        for user_data in test_users:
            email = user_data['email']
            children_data = user_data.pop('children')
            
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'password': user_data.pop('password'),
                    'name': user_data['name'],
                    'subscription_tier': user_data['tier'],
                }
            )
            
            if created:
                user.set_password(user_data.get('password', 'Test@123'))
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created user: {email}'))
            else:
                user.name = user_data['name']
                user.subscription_tier = user_data['tier']
                user.save()
                self.stdout.write(f'Updated user: {email}')

            # Create children
            for i, child_data in enumerate(children_data):
                child, child_created = Child.objects.get_or_create(
                    parent=user,
                    name=child_data['name'],
                    defaults={
                        'avatar': child_data['avatar'],
                        'language': 'HI',
                    }
                )
                if child_created:
                    self.stdout.write(f'  Created child: {child_data["name"]}')

        self.stdout.write(self.style.SUCCESS('\nTest users created successfully!'))
        self.stdout.write('\nTest Accounts:')
        self.stdout.write('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        for user_data in test_users:
            self.stdout.write(f'\n{user_data["tier"]} TIER:')
            self.stdout.write(f'  Email: {user_data["email"]}')
            self.stdout.write(f'  Password: {user_data["password"]}')
            self.stdout.write(f'  Children: {len(user_data["children"])}')
        self.stdout.write('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
