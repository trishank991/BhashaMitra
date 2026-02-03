"""
Seed command for the basic structure of the Punjabi (Gurmukhi) curriculum.
"""
import logging
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.children.models import Child
from apps.curriculum.models import (
    Script, AlphabetCategory, Letter
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Seed basic structure for Punjabi L1 curriculum (Gurmukhi script)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing Punjabi data before seeding',
        )

    def handle(self, *args, **options):
        self.stdout.write('🚜 Seeding Punjabi L1 curriculum structure...\n')

        if options['clear']:
            self.clear_existing_data()

        with transaction.atomic():
            script = self.seed_script()
            self.seed_vowels(script)
            self.seed_consonants(script)
            # self.seed_additional_letters(script) # Future use

        self.stdout.write(self.style.SUCCESS(
            '\n' + '=' * 60 +
            '\n🚜 Punjabi L1 Curriculum Structure Seeded Successfully!' +
            '\n' + '=' * 60
        ))

    def clear_existing_data(self):
        """Clear existing Punjabi data."""
        self.stdout.write('Clearing existing Punjabi data...')
        Script.objects.filter(language='PUNJABI').delete()
        self.stdout.write(self.style.SUCCESS('Cleared existing Punjabi data.'))

    def seed_script(self):
        """Create Gurmukhi script for Punjabi."""
        self.stdout.write('Creating Gurmukhi script for Punjabi...')

        script, created = Script.objects.update_or_create(
            language='PUNJABI',
            defaults={
                'name': 'Gurmukhi (Punjabi)',
                'name_native': 'ਗੁਰਮੁਖੀ',
                'description': 'The Gurmukhi script is used for writing the Punjabi language. It was standardized by the second Sikh guru, Guru Angad Dev.',
                'total_letters': 35,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'  Created script: {script.name}'))
        else:
            self.stdout.write(f'  Updated script: {script.name}')

        return script

    def seed_vowels(self, script):
        """Create vowel letters for Punjabi."""
        self.stdout.write('Creating vowels (ਸਵਰ)...')

        category, _ = AlphabetCategory.objects.update_or_create(
            script=script,
            category_type='VOWEL',
            defaults={
                'name': 'Vowels',
                'name_native': 'ਸਵਰ',
                'description': 'Vowel sounds in Punjabi, based on three carrier letters.',
                'order': 1,
            }
        )

        # Vowel carriers
        vowels = [
            {'character': 'ੳ', 'romanization': 'Ura', 'example_word': 'ਊਠ', 'example_translation': 'Camel'},
            {'character': 'ਅ', 'romanization': 'Aira', 'example_word': 'ਅੰਬ', 'example_translation': 'Mango'},
            {'character': 'ੲ', 'romanization': 'Iri', 'example_word': 'ਇੱਲ', 'example_translation': 'Eagle'},
        ]

        for i, vowel in enumerate(vowels, 1):
            Letter.objects.update_or_create(
                category=category,
                character=vowel['character'],
                defaults={
                    'romanization': vowel['romanization'],
                    'example_word': vowel['example_word'],
                    'example_word_translation': vowel['example_translation'],
                    'example_image': f"https://picsum.photos/seed/punjabi-vowel-{i}/120",
                    'order': i,
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(vowels)} vowel carriers'))


    def seed_consonants(self, script):
        """Create consonant letters for Punjabi."""
        self.stdout.write('Creating consonants (ਵਿਅੰਜਨ)...')

        category, _ = AlphabetCategory.objects.update_or_create(
            script=script,
            category_type='CONSONANT',
            defaults={
                'name': 'Consonants',
                'name_native': 'ਵਿਅੰਜਨ',
                'description': 'Consonant sounds in Punjabi.',
                'order': 2,
            }
        )

        consonants = [
            {'character': 'ਸ', 'romanization': 'sa', 'example_word': 'ਸੇਬ', 'example_translation': 'Apple'},
            {'character': 'ਹ', 'romanization': 'ha', 'example_word': 'ਹਾਥੀ', 'example_translation': 'Elephant'},
            {'character': 'ਕ', 'romanization': 'ka', 'example_word': 'ਕਬੂਤਰ', 'example_translation': 'Pigeon'},
            {'character': 'ਖ', 'romanization': 'kha', 'example_word': 'ਖਰਗੋਸ਼', 'example_translation': 'Rabbit'},
            {'character': 'ਗ', 'romanization': 'ga', 'example_word': 'ਗਾਂ', 'example_translation': 'Cow'},
            {'character': 'ਘ', 'romanization': 'gha', 'example_word': 'ਘਰ', 'example_translation': 'House'},
            {'character': 'ਙ', 'romanization': 'nga', 'example_word': '', 'example_translation': ''},
            {'character': 'ਚ', 'romanization': 'ca', 'example_word': 'ਚਮਚਾ', 'example_translation': 'Spoon'},
            {'character': 'ਛ', 'romanization': 'cha', 'example_word': 'ਛਤਰੀ', 'example_translation': 'Umbrella'},
            {'character': 'ਜ', 'romanization': 'ja', 'example_word': 'ਜਹਾਜ਼', 'example_translation': 'Ship'},
            {'character': 'ਝ', 'romanization': 'jha', 'example_word': 'ਝੰਡਾ', 'example_translation': 'Flag'},
            {'character': 'ਞ', 'romanization': 'nya', 'example_word': '', 'example_translation': ''},
            {'character': 'ਟ', 'romanization': 'tta', 'example_word': 'ਟਮਾਟਰ', 'example_translation': 'Tomato'},
            {'character': 'ਠ', 'romanization': 'ttha', 'example_word': 'ਠੰਡ', 'example_translation': 'Cold'},
            {'character': 'ਡ', 'romanization': 'dda', 'example_word': 'ਡੱਡੂ', 'example_translation': 'Frog'},
            {'character': 'ਢ', 'romanization': 'ddha', 'example_word': 'ਢੋਲ', 'example_translation': 'Drum'},
            {'character': 'ਣ', 'romanization': 'nna', 'example_word': '', 'example_translation': ''},
            {'character': 'ਤ', 'romanization': 'ta', 'example_word': 'ਤੋਤਾ', 'example_translation': 'Parrot'},
            {'character': 'ਥ', 'romanization': 'tha', 'example_word': 'ਥਾਲੀ', 'example_translation': 'Plate'},
            {'character': 'ਦ', 'romanization': 'da', 'example_word': 'ਦਵਾਤ', 'example_translation': 'Inkpot'},
            {'character': 'ਧ', 'romanization': 'dha', 'example_word': 'ਧਰਤੀ', 'example_translation': 'Earth'},
            {'character': 'ਨ', 'romanization': 'na', 'example_word': 'ਨਲਕਾ', 'example_translation': 'Tap'},
            {'character': 'ਪ', 'romanization': 'pa', 'example_word': 'ਪਤੰਗ', 'example_translation': 'Kite'},
            {'character': 'ਫ', 'romanization': 'pha', 'example_word': 'ਫਲ', 'example_translation': 'Fruit'},
            {'character': 'ਬ', 'romanization': 'ba', 'example_word': 'ਬੱਸ', 'example_translation': 'Bus'},
            {'character': 'ਭ', 'romanization': 'bha', 'example_word': 'ਭੇਡ', 'example_translation': 'Sheep'},
            {'character': 'ਮ', 'romanization': 'ma', 'example_word': 'ਮੱਛੀ', 'example_translation': 'Fish'},
            {'character': 'ਯ', 'romanization': 'ya', 'example_word': 'ਯੱਕਾ', 'example_translation': 'Yacht'},
            {'character': 'ਰ', 'romanization': 'ra', 'example_word': 'ਰਾਜਾ', 'example_translation': 'King'},
            {'character': 'ਲ', 'romanization': 'la', 'example_word': 'ਲੜਕੀ', 'example_translation': 'Girl'},
            {'character': 'ਵ', 'romanization': 'va', 'example_word': 'ਵੈਨ', 'example_translation': 'Van'},
            {'character': 'ੜ', 'romanization': 'rha', 'example_word': '', 'example_translation': ''},
        ]

        for i, cons in enumerate(consonants, 1):
            Letter.objects.update_or_create(
                category=category,
                character=cons['character'],
                defaults={
                    'romanization': cons['romanization'],
                    'example_word': cons['example_word'],
                    'example_word_translation': cons['example_translation'],
                    'example_image': f"https://picsum.photos/seed/punjabi-consonant-{i}/120",
                    'order': i,
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(consonants)} consonants'))
