"""Management command to seed Tamil curriculum."""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Seed complete Tamil curriculum (alphabet, vocabulary, grammar)'

    def handle(self, *args, **options):
        from scripts.seed_tamil_curriculum import seed_tamil_curriculum

        self.stdout.write(self.style.NOTICE('Starting Tamil curriculum seeding...'))
        self.stdout.write('')

        results = seed_tamil_curriculum()

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Tamil curriculum seeding complete!'))
        self.stdout.write(self.style.SUCCESS(f'  Letters: {results["letters"]}'))
        self.stdout.write(self.style.SUCCESS(f'  Words: {results["words"]}'))
        self.stdout.write(self.style.SUCCESS(f'  Grammar rules: {results["rules"]}'))
