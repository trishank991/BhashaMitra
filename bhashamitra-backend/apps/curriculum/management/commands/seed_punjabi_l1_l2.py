"""
Seed command for complete Punjabi L1-L2 curriculum.
Following the same structure as Hindi curriculum.
"""
import logging
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.children.models import Child
from apps.curriculum.models import (
    Script, AlphabetCategory, Letter, Matra,
    VocabularyTheme, VocabularyWord,
    CurriculumLevel, CurriculumModule, Lesson,
    Song, Game, Assessment, AssessmentQuestion,
    PeppiPhrase, PeppiPersonality,
)
from apps.stories.models import Story, StoryPage

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Seed complete Punjabi L1-L2 curriculum (Gurmukhi script)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing Punjabi data before seeding',
        )

    def handle(self, *args, **options):
        self.stdout.write('Seeding Punjabi L1-L2 curriculum...\n')

        if options['clear']:
            self.clear_existing_data()

        with transaction.atomic():
            # 1. Create Gurmukhi Script and Letters
            script = self.seed_script()
            self.seed_vowel_holders(script)
            self.seed_vowels(script)
            self.seed_consonants(script)
            self.seed_matras(script)

            # 2. Create Vocabulary
            self.seed_vocabulary()

            # 3. Create Stories
            self.seed_stories()

            # 4. Create Songs
            self.seed_songs()

            # 5. Create Curriculum Levels
            self.seed_curriculum_levels()

            # 6. Create Peppi Phrases
            self.seed_peppi_phrases()

            # 7. Create Games
            self.seed_games()

            # 8. Create Assessments
            self.seed_assessments()

        self.stdout.write(self.style.SUCCESS(
            '\n' + '=' * 60 +
            '\nPunjabi L1-L2 Curriculum Seeded Successfully!' +
            '\n' + '=' * 60 +
            '\n  Script: Gurmukhi' +
            '\n  Vowel Holders: 3' +
            '\n  Vowels: 10' +
            '\n  Consonants: 32' +
            '\n  Matras: 10' +
            '\n  Vocabulary Words: 70' +
            '\n  Stories: 10' +
            '\n  Songs: 5' +
            '\n  Games: 5' +
            '\n  Assessments: 2' +
            '\n' + '=' * 60
        ))

    def clear_existing_data(self):
        """Clear existing Punjabi data."""
        self.stdout.write('Clearing existing Punjabi data...')

        # Clear scripts and related
        Script.objects.filter(language='PUNJABI').delete()

        # Clear vocabulary
        VocabularyTheme.objects.filter(language='PUNJABI').delete()

        # Clear games
        Game.objects.filter(language='PUNJABI').delete()

        # Clear assessments
        Assessment.objects.filter(language='PUNJABI').delete()

        # Clear Peppi phrases (Punjabi context)
        PeppiPhrase.objects.filter(context__icontains='punjabi').delete()

        self.stdout.write(self.style.SUCCESS('Cleared existing Punjabi data.'))

    def seed_script(self):
        """Create Gurmukhi script."""
        self.stdout.write('Creating Gurmukhi script...')

        script, created = Script.objects.update_or_create(
            language='PUNJABI',
            defaults={
                'name': 'Gurmukhi',
                'name_native': 'ਗੁਰਮੁਖੀ',
                'description': 'Gurmukhi is the script used to write Punjabi language. It was standardized by Guru Angad Dev Ji, the second Sikh Guru, in the 16th century.',
                'total_letters': 55,  # 3 holders + 10 vowels + 32 consonants + 10 matras
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'  Created script: {script.name}'))
        else:
            self.stdout.write(f'  Updated script: {script.name}')

        return script

    def seed_vowel_holders(self, script):
        """Create vowel holder categories and letters."""
        self.stdout.write('Creating vowel holders (ਮਾਤਰਾ ਵਾਹਕ)...')

        category, _ = AlphabetCategory.objects.update_or_create(
            script=script,
            category_type='VOWEL_HOLDER',
            defaults={
                'name': 'Vowel Holders',
                'name_native': 'ਮਾਤਰਾ ਵਾਹਕ',
                'description': 'Base letters that carry vowel sounds in Gurmukhi',
                'order': 1,
            }
        )

        vowel_holders = [
            {'character': 'ੳ', 'romanization': 'ura', 'ipa': 'ʊ', 'example_word': 'ਊਠ', 'example_translation': 'camel', 'pronunciation_guide': 'Base for ਉ ਊ ਓ ਔ sounds'},
            {'character': 'ਅ', 'romanization': 'aira', 'ipa': 'ə', 'example_word': 'ਅੱਖ', 'example_translation': 'eye', 'pronunciation_guide': 'Standalone vowel base'},
            {'character': 'ੲ', 'romanization': 'iri', 'ipa': 'ɪ', 'example_word': 'ਇਮਲੀ', 'example_translation': 'tamarind', 'pronunciation_guide': 'Base for ਇ ਈ ਏ ਐ sounds'},
        ]

        for i, vh in enumerate(vowel_holders, 1):
            Letter.objects.update_or_create(
                category=category,
                character=vh['character'],
                defaults={
                    'romanization': vh['romanization'],
                    'ipa': vh['ipa'],
                    'pronunciation_guide': vh['pronunciation_guide'],
                    'example_word': vh['example_word'],
                    'example_word_romanization': vh['romanization'],
                    'example_word_translation': vh['example_translation'],
                    'order': i,
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(vowel_holders)} vowel holders'))

    def seed_vowels(self, script):
        """Create vowel letters."""
        self.stdout.write('Creating vowels (ਸਵਰ)...')

        category, _ = AlphabetCategory.objects.update_or_create(
            script=script,
            category_type='VOWEL',
            defaults={
                'name': 'Vowels',
                'name_native': 'ਸਵਰ',
                'description': 'Vowel sounds in Gurmukhi script',
                'order': 2,
            }
        )

        vowels = [
            {'character': 'ਅ', 'romanization': 'a', 'ipa': '/ə/', 'example_word': 'ਅੰਬ', 'example_translation': 'mango', 'example_image': 'https://images.unsplash.com/photo-1553279768-865429fa0078?w=120&h=120&fit=crop', 'mnemonic': 'ਅ ਤੋਂ ਅੰਬ ਮਿੱਠਾ ਫਲ'},
            {'character': 'ਆ', 'romanization': 'aa', 'ipa': '/aː/', 'example_word': 'ਆਲੂ', 'example_translation': 'potato', 'example_image': 'https://images.unsplash.com/photo-1518977676601-b53f82afe9e7?w=120&h=120&fit=crop', 'mnemonic': 'ਆ ਤੋਂ ਆਲੂ ਸਵਾਦ ਵਧੀਆ'},
            {'character': 'ਇ', 'romanization': 'i', 'ipa': '/ɪ/', 'example_word': 'ਇਮਲੀ', 'example_translation': 'tamarind', 'example_image': 'https://images.unsplash.com/photo-1590502160462-58b41354f588?w=120&h=120&fit=crop', 'mnemonic': 'ਇ ਤੋਂ ਇਮਲੀ ਖੱਟੀ ਮਿੱਠੀ'},
            {'character': 'ਈ', 'romanization': 'ee', 'ipa': '/iː/', 'example_word': 'ਈਖ', 'example_translation': 'sugarcane', 'example_image': 'https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=120&h=120&fit=crop', 'mnemonic': 'ਈ ਤੋਂ ਈਖ ਮਿੱਠੀ ਮਿੱਠੀ'},
            {'character': 'ਉ', 'romanization': 'u', 'ipa': '/ʊ/', 'example_word': 'ਉੱਲੂ', 'example_translation': 'owl', 'example_image': 'https://images.unsplash.com/photo-1543549790-8b5f4a028cfb?w=120&h=120&fit=crop', 'mnemonic': 'ਉ ਤੋਂ ਉੱਲੂ ਰਾਤ ਨੂੰ ਜਾਗਦਾ'},
            {'character': 'ਊ', 'romanization': 'oo', 'ipa': '/uː/', 'example_word': 'ਊਠ', 'example_translation': 'camel', 'example_image': 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=120&h=120&fit=crop', 'mnemonic': 'ਊ ਤੋਂ ਊਠ ਰੇਗਿਸਤਾਨ ਦਾ ਜਹਾਜ਼'},
            {'character': 'ਏ', 'romanization': 'e', 'ipa': '/eː/', 'example_word': 'ਏਕ', 'example_translation': 'one', 'example_image': 'https://images.unsplash.com/photo-1509228627152-72ae9ae6848d?w=120&h=120&fit=crop', 'mnemonic': 'ਏ ਤੋਂ ਏਕ ਇੱਕ ਗਿਣਤੀ'},
            {'character': 'ਐ', 'romanization': 'ai', 'ipa': '/ɛː/', 'example_word': 'ਐਨਕ', 'example_translation': 'glasses', 'example_image': 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=120&h=120&fit=crop', 'mnemonic': 'ਐ ਤੋਂ ਐਨਕ ਚੰਗਾ ਦੇਖੋ'},
            {'character': 'ਓ', 'romanization': 'o', 'ipa': '/oː/', 'example_word': 'ਓਖਲੀ', 'example_translation': 'mortar', 'example_image': 'https://images.unsplash.com/photo-1506976785307-8732e854ad03?w=120&h=120&fit=crop', 'mnemonic': 'ਓ ਤੋਂ ਓਖਲੀ ਮਸਾਲੇ ਕੁੱਟੋ'},
            {'character': 'ਔ', 'romanization': 'au', 'ipa': '/ɔː/', 'example_word': 'ਔਰਤ', 'example_translation': 'woman', 'example_image': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=120&h=120&fit=crop', 'mnemonic': 'ਔ ਤੋਂ ਔਰਤ ਮਾਂ ਵਰਗੀ'},
        ]

        for i, vowel in enumerate(vowels, 1):
            Letter.objects.update_or_create(
                category=category,
                character=vowel['character'],
                defaults={
                    'romanization': vowel['romanization'],
                    'ipa': vowel['ipa'],
                    'pronunciation_guide': vowel['mnemonic'],
                    'example_word': vowel['example_word'],
                    'example_word_romanization': vowel['romanization'],
                    'example_word_translation': vowel['example_translation'],
                    'example_image': vowel.get('example_image', ''),
                    'order': i,
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(vowels)} vowels'))

    def seed_consonants(self, script):
        """Create consonant letters organized by varga."""
        self.stdout.write('Creating consonants (ਵਿਅੰਜਨ)...')

        category, _ = AlphabetCategory.objects.update_or_create(
            script=script,
            category_type='CONSONANT',
            defaults={
                'name': 'Consonants',
                'name_native': 'ਵਿਅੰਜਨ',
                'description': 'Consonant sounds in Gurmukhi script organized by articulation groups (varga)',
                'order': 3,
            }
        )

        consonants = [
            # Mool letters
            {'character': 'ਸ', 'romanization': 'sa', 'ipa': '/s/', 'group': 'MOOL', 'example_word': 'ਸੇਬ', 'example_translation': 'apple', 'example_image': 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=120&h=120&fit=crop', 'mnemonic': 'ਸ ਤੋਂ ਸੇਬ ਲਾਲ ਲਾਲ'},
            {'character': 'ਹ', 'romanization': 'ha', 'ipa': '/h/', 'group': 'MOOL', 'example_word': 'ਹਾਥੀ', 'example_translation': 'elephant', 'example_image': 'https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=120&h=120&fit=crop', 'mnemonic': 'ਹ ਤੋਂ ਹਾਥੀ ਵੱਡਾ ਵੱਡਾ'},
            # Ka Varga
            {'character': 'ਕ', 'romanization': 'ka', 'ipa': '/k/', 'group': 'KA_VARGA', 'example_word': 'ਕਬੂਤਰ', 'example_translation': 'pigeon', 'example_image': 'https://images.unsplash.com/photo-1555169062-013468b47731?w=120&h=120&fit=crop', 'mnemonic': 'ਕ ਤੋਂ ਕਬੂਤਰ ਗੁਟਰ ਗੂੰ'},
            {'character': 'ਖ', 'romanization': 'kha', 'ipa': '/kʰ/', 'group': 'KA_VARGA', 'example_word': 'ਖਰਗੋਸ਼', 'example_translation': 'rabbit', 'example_image': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=120&h=120&fit=crop', 'mnemonic': 'ਖ ਤੋਂ ਖਰਗੋਸ਼ ਤੇਜ਼ ਭੱਜੇ'},
            {'character': 'ਗ', 'romanization': 'ga', 'ipa': '/g/', 'group': 'KA_VARGA', 'example_word': 'ਗਾਂ', 'example_translation': 'cow', 'example_image': 'https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=120&h=120&fit=crop', 'mnemonic': 'ਗ ਤੋਂ ਗਾਂ ਦੁੱਧ ਦਿੰਦੀ'},
            {'character': 'ਘ', 'romanization': 'gha', 'ipa': '/gʰ/', 'group': 'KA_VARGA', 'example_word': 'ਘਰ', 'example_translation': 'house', 'example_image': 'https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=120&h=120&fit=crop', 'mnemonic': 'ਘ ਤੋਂ ਘਰ ਪਿਆਰਾ ਪਿਆਰਾ'},
            {'character': 'ਙ', 'romanization': 'nga', 'ipa': '/ŋ/', 'group': 'KA_VARGA', 'example_word': 'ਅੰਗ', 'example_translation': 'limb', 'example_image': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=120&h=120&fit=crop', 'mnemonic': 'ਙ ਨੱਕ ਵਿੱਚੋਂ ਆਵਾਜ਼'},
            # Cha Varga
            {'character': 'ਚ', 'romanization': 'cha', 'ipa': '/tʃ/', 'group': 'CHA_VARGA', 'example_word': 'ਚਿੜੀ', 'example_translation': 'sparrow', 'example_image': 'https://images.unsplash.com/photo-1486365227551-f3f90034a57c?w=120&h=120&fit=crop', 'mnemonic': 'ਚ ਤੋਂ ਚਿੜੀ ਚੂੰ ਚੂੰ'},
            {'character': 'ਛ', 'romanization': 'chha', 'ipa': '/tʃʰ/', 'group': 'CHA_VARGA', 'example_word': 'ਛਤਰੀ', 'example_translation': 'umbrella', 'example_image': 'https://images.unsplash.com/photo-1534309466160-70b22cc6252c?w=120&h=120&fit=crop', 'mnemonic': 'ਛ ਤੋਂ ਛਤਰੀ ਮੀਂਹ ਵਿੱਚ'},
            {'character': 'ਜ', 'romanization': 'ja', 'ipa': '/dʒ/', 'group': 'CHA_VARGA', 'example_word': 'ਜਹਾਜ਼', 'example_translation': 'ship', 'example_image': 'https://images.unsplash.com/photo-1534343821789-89dd78d50b53?w=120&h=120&fit=crop', 'mnemonic': 'ਜ ਤੋਂ ਜਹਾਜ਼ ਉੱਡਦਾ ਜਾਵੇ'},
            {'character': 'ਝ', 'romanization': 'jha', 'ipa': '/dʒʰ/', 'group': 'CHA_VARGA', 'example_word': 'ਝੰਡਾ', 'example_translation': 'flag', 'example_image': 'https://images.unsplash.com/photo-1569974507005-6dc61f97fb5c?w=120&h=120&fit=crop', 'mnemonic': 'ਝ ਤੋਂ ਝੰਡਾ ਲਹਿਰਾਵੇ'},
            {'character': 'ਞ', 'romanization': 'nya', 'ipa': '/ɲ/', 'group': 'CHA_VARGA', 'example_word': 'ਮਿੱਤਰ', 'example_translation': 'friend', 'example_image': 'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=120&h=120&fit=crop', 'mnemonic': 'ਞ ਨਾਸਿਕ ਧੁਨੀ'},
            # Ta Varga (Retroflex)
            {'character': 'ਟ', 'romanization': 'ta', 'ipa': '/ʈ/', 'group': 'TA_VARGA', 'example_word': 'ਟਮਾਟਰ', 'example_translation': 'tomato', 'example_image': 'https://images.unsplash.com/photo-1558818498-28c1e002674f?w=120&h=120&fit=crop', 'mnemonic': 'ਟ ਤੋਂ ਟਮਾਟਰ ਲਾਲ ਲਾਲ'},
            {'character': 'ਠ', 'romanization': 'tha', 'ipa': '/ʈʰ/', 'group': 'TA_VARGA', 'example_word': 'ਠੰਡਾ', 'example_translation': 'cold', 'example_image': 'https://images.unsplash.com/photo-1516912481808-3406841bd33c?w=120&h=120&fit=crop', 'mnemonic': 'ਠ ਤੋਂ ਠੰਡਾ ਬਰਫ਼ ਵਰਗਾ'},
            {'character': 'ਡ', 'romanization': 'da', 'ipa': '/ɖ/', 'group': 'TA_VARGA', 'example_word': 'ਡੱਬਾ', 'example_translation': 'box', 'example_image': 'https://images.unsplash.com/photo-1607166452427-7e4477079cb9?w=120&h=120&fit=crop', 'mnemonic': 'ਡ ਤੋਂ ਡੱਬਾ ਚੀਜ਼ਾਂ ਰੱਖੋ'},
            {'character': 'ਢ', 'romanization': 'dha', 'ipa': '/ɖʰ/', 'group': 'TA_VARGA', 'example_word': 'ਢੋਲ', 'example_translation': 'drum', 'example_image': 'https://images.unsplash.com/photo-1519892300165-cb5542fb47c7?w=120&h=120&fit=crop', 'mnemonic': 'ਢ ਤੋਂ ਢੋਲ ਭੰਗੜਾ ਪਾਓ'},
            {'character': 'ਣ', 'romanization': 'na', 'ipa': '/ɳ/', 'group': 'TA_VARGA', 'example_word': 'ਕੰਨ', 'example_translation': 'ear', 'example_image': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=120&h=120&fit=crop', 'mnemonic': 'ਣ ਜੀਭ ਉੱਪਰ ਨੱਕ ਦੀ ਆਵਾਜ਼'},
            # Ta Varga 2 (Dental)
            {'character': 'ਤ', 'romanization': 'ta', 'ipa': '/t̪/', 'group': 'TA_VARGA_2', 'example_word': 'ਤਾਰਾ', 'example_translation': 'star', 'example_image': 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=120&h=120&fit=crop', 'mnemonic': 'ਤ ਤੋਂ ਤਾਰਾ ਚਮਕਦਾ'},
            {'character': 'ਥ', 'romanization': 'tha', 'ipa': '/t̪ʰ/', 'group': 'TA_VARGA_2', 'example_word': 'ਥਾਲੀ', 'example_translation': 'plate', 'example_image': 'https://images.unsplash.com/photo-1544025162-d76694265947?w=120&h=120&fit=crop', 'mnemonic': 'ਥ ਤੋਂ ਥਾਲੀ ਖਾਣਾ ਖਾਓ'},
            {'character': 'ਦ', 'romanization': 'da', 'ipa': '/d̪/', 'group': 'TA_VARGA_2', 'example_word': 'ਦੁੱਧ', 'example_translation': 'milk', 'example_image': 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=120&h=120&fit=crop', 'mnemonic': 'ਦ ਤੋਂ ਦੁੱਧ ਚਿੱਟਾ ਚਿੱਟਾ'},
            {'character': 'ਧ', 'romanization': 'dha', 'ipa': '/d̪ʰ/', 'group': 'TA_VARGA_2', 'example_word': 'ਧਨੁਸ਼', 'example_translation': 'bow', 'example_image': 'https://images.unsplash.com/photo-1533381748829-78674b3e9632?w=120&h=120&fit=crop', 'mnemonic': 'ਧ ਤੋਂ ਧਨੁਸ਼ ਤੀਰ ਚਲਾਓ'},
            {'character': 'ਨ', 'romanization': 'na', 'ipa': '/n/', 'group': 'TA_VARGA_2', 'example_word': 'ਨਾਰੀਅਲ', 'example_translation': 'coconut', 'example_image': 'https://images.unsplash.com/photo-1550689960-d9c8ab6f7c4f?w=120&h=120&fit=crop', 'mnemonic': 'ਨ ਤੋਂ ਨਾਰੀਅਲ ਮਿੱਠਾ ਪਾਣੀ'},
            # Pa Varga
            {'character': 'ਪ', 'romanization': 'pa', 'ipa': '/p/', 'group': 'PA_VARGA', 'example_word': 'ਪਤੰਗ', 'example_translation': 'kite', 'example_image': 'https://images.unsplash.com/photo-1601580184474-24f0dbbcf7fe?w=120&h=120&fit=crop', 'mnemonic': 'ਪ ਤੋਂ ਪਤੰਗ ਉੱਚੀ ਉੱਡੇ'},
            {'character': 'ਫ', 'romanization': 'pha', 'ipa': '/pʰ/', 'group': 'PA_VARGA', 'example_word': 'ਫੁੱਲ', 'example_translation': 'flower', 'example_image': 'https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=120&h=120&fit=crop', 'mnemonic': 'ਫ ਤੋਂ ਫੁੱਲ ਸੁੰਦਰ ਸੁੰਦਰ'},
            {'character': 'ਬ', 'romanization': 'ba', 'ipa': '/b/', 'group': 'PA_VARGA', 'example_word': 'ਬੱਕਰੀ', 'example_translation': 'goat', 'example_image': 'https://images.unsplash.com/photo-1524024973431-2ad916746881?w=120&h=120&fit=crop', 'mnemonic': 'ਬ ਤੋਂ ਬੱਕਰੀ ਮੈਂ ਮੈਂ'},
            {'character': 'ਭ', 'romanization': 'bha', 'ipa': '/bʰ/', 'group': 'PA_VARGA', 'example_word': 'ਭਾਲੂ', 'example_translation': 'bear', 'example_image': 'https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=120&h=120&fit=crop', 'mnemonic': 'ਭ ਤੋਂ ਭਾਲੂ ਜੰਗਲ ਵਿੱਚ'},
            {'character': 'ਮ', 'romanization': 'ma', 'ipa': '/m/', 'group': 'PA_VARGA', 'example_word': 'ਮੱਛੀ', 'example_translation': 'fish', 'example_image': 'https://images.unsplash.com/photo-1544943910-4c1dc44aab44?w=120&h=120&fit=crop', 'mnemonic': 'ਮ ਤੋਂ ਮੱਛੀ ਪਾਣੀ ਵਿੱਚ'},
            # Antastha
            {'character': 'ਯ', 'romanization': 'ya', 'ipa': '/j/', 'group': 'ANTASTHA', 'example_word': 'ਯੋਗਾ', 'example_translation': 'yoga', 'example_image': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=120&h=120&fit=crop', 'mnemonic': 'ਯ ਤੋਂ ਯੋਗਾ ਸਿਹਤ ਚੰਗੀ'},
            {'character': 'ਰ', 'romanization': 'ra', 'ipa': '/r/', 'group': 'ANTASTHA', 'example_word': 'ਰੱਸੀ', 'example_translation': 'rope', 'example_image': 'https://images.unsplash.com/photo-1583395838144-09be6e04e84f?w=120&h=120&fit=crop', 'mnemonic': 'ਰ ਤੋਂ ਰੱਸੀ ਖਿੱਚ ਖਿੱਚ'},
            {'character': 'ਲ', 'romanization': 'la', 'ipa': '/l/', 'group': 'ANTASTHA', 'example_word': 'ਲੱਸੀ', 'example_translation': 'lassi', 'example_image': 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=120&h=120&fit=crop', 'mnemonic': 'ਲ ਤੋਂ ਲੱਸੀ ਠੰਡੀ ਮਿੱਠੀ'},
            {'character': 'ਵ', 'romanization': 'va', 'ipa': '/ʋ/', 'group': 'ANTASTHA', 'example_word': 'ਵਾਇਲਨ', 'example_translation': 'violin', 'example_image': 'https://images.unsplash.com/photo-1612225330812-01a9c6b355ec?w=120&h=120&fit=crop', 'mnemonic': 'ਵ ਤੋਂ ਵਾਇਲਨ ਸੰਗੀਤ ਸੁਣੋ'},
            {'character': 'ੜ', 'romanization': 'rha', 'ipa': '/ɽ/', 'group': 'ANTASTHA', 'example_word': 'ਪੜ੍ਹਨਾ', 'example_translation': 'to read', 'example_image': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=120&h=120&fit=crop', 'mnemonic': 'ੜ ਪੰਜਾਬੀ ਦੀ ਖ਼ਾਸ ਆਵਾਜ਼'},
        ]

        for i, cons in enumerate(consonants, 1):
            Letter.objects.update_or_create(
                category=category,
                character=cons['character'],
                defaults={
                    'romanization': cons['romanization'],
                    'ipa': cons['ipa'],
                    'pronunciation_guide': cons['mnemonic'],
                    'example_word': cons['example_word'],
                    'example_word_romanization': cons['romanization'],
                    'example_word_translation': cons['example_translation'],
                    'example_image': cons.get('example_image', ''),
                    'order': i,
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(consonants)} consonants'))

    def seed_matras(self, script):
        """Create matras (vowel marks)."""
        self.stdout.write('Creating matras (ਲਗਾਂ)...')

        matras = [
            {'symbol': 'ਾ', 'name': 'Kanna', 'name_native': 'ਕੰਨਾ', 'sound': 'aa', 'position': 'Right', 'example_with_ka': 'ਕਾ', 'example_word': 'ਕਾਲਾ', 'translation': 'black'},
            {'symbol': 'ਿ', 'name': 'Sihari', 'name_native': 'ਸਿਹਾਰੀ', 'sound': 'i', 'position': 'Left', 'example_with_ka': 'ਕਿ', 'example_word': 'ਕਿਤਾਬ', 'translation': 'book'},
            {'symbol': 'ੀ', 'name': 'Bihari', 'name_native': 'ਬਿਹਾਰੀ', 'sound': 'ee', 'position': 'Right', 'example_with_ka': 'ਕੀ', 'example_word': 'ਕੀੜੀ', 'translation': 'ant'},
            {'symbol': 'ੁ', 'name': 'Aunkar', 'name_native': 'ਔਂਕੜ', 'sound': 'u', 'position': 'Below', 'example_with_ka': 'ਕੁ', 'example_word': 'ਕੁੱਤਾ', 'translation': 'dog'},
            {'symbol': 'ੂ', 'name': 'Dulankar', 'name_native': 'ਦੁਲੈਂਕੜ', 'sound': 'oo', 'position': 'Below', 'example_with_ka': 'ਕੂ', 'example_word': 'ਕੂਲਰ', 'translation': 'cooler'},
            {'symbol': 'ੇ', 'name': 'Laanv', 'name_native': 'ਲਾਂਵਾਂ', 'sound': 'e', 'position': 'Top', 'example_with_ka': 'ਕੇ', 'example_word': 'ਕੇਲਾ', 'translation': 'banana'},
            {'symbol': 'ੈ', 'name': 'Dulaanv', 'name_native': 'ਦੁਲਾਵਾਂ', 'sound': 'ai', 'position': 'Top', 'example_with_ka': 'ਕੈ', 'example_word': 'ਪੈਸਾ', 'translation': 'money'},
            {'symbol': 'ੋ', 'name': 'Hora', 'name_native': 'ਹੋੜਾ', 'sound': 'o', 'position': 'Top+Right', 'example_with_ka': 'ਕੋ', 'example_word': 'ਕੋਟ', 'translation': 'coat'},
            {'symbol': 'ੌ', 'name': 'Kanaura', 'name_native': 'ਕਨੌੜਾ', 'sound': 'au', 'position': 'Top+Right', 'example_with_ka': 'ਕੌ', 'example_word': 'ਕੌਰ', 'translation': 'Kaur'},
            {'symbol': 'ੰ', 'name': 'Tippi', 'name_native': 'ਟਿੱਪੀ', 'sound': 'n (nasal)', 'position': 'Top', 'example_with_ka': 'ਕੰ', 'example_word': 'ਕੰਮ', 'translation': 'work'},
        ]

        for i, m in enumerate(matras, 1):
            Matra.objects.update_or_create(
                script=script,
                symbol=m['symbol'],
                defaults={
                    'name': m['name'],
                    'example_with_ka': m['example_with_ka'],
                    'order': i,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(matras)} matras'))

    def seed_vocabulary(self):
        """Create vocabulary themes and words for L1 and L2."""
        self.stdout.write('Creating vocabulary themes and words...')

        # L1 Vocabulary (20 words)
        l1_themes = [
            {
                'name': 'Family',
                'name_native': 'ਪਰਿਵਾਰ',
                'icon': 'family',
                'level': 1,
                'words': [
                    {'word': 'ਮਾਂ', 'romanization': 'Maa', 'translation': 'Mother', 'pos': 'NOUN'},
                    {'word': 'ਪਾਪਾ', 'romanization': 'Papa', 'translation': 'Father', 'pos': 'NOUN'},
                    {'word': 'ਦਾਦੀ', 'romanization': 'Daadi', 'translation': 'Grandmother', 'pos': 'NOUN'},
                    {'word': 'ਦਾਦਾ', 'romanization': 'Daada', 'translation': 'Grandfather', 'pos': 'NOUN'},
                    {'word': 'ਭੈਣ', 'romanization': 'Bhain', 'translation': 'Sister', 'pos': 'NOUN'},
                    {'word': 'ਵੀਰ', 'romanization': 'Veer', 'translation': 'Brother', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Colors',
                'name_native': 'ਰੰਗ',
                'icon': 'palette',
                'level': 1,
                'words': [
                    {'word': 'ਲਾਲ', 'romanization': 'Laal', 'translation': 'Red', 'pos': 'ADJECTIVE'},
                    {'word': 'ਨੀਲਾ', 'romanization': 'Neela', 'translation': 'Blue', 'pos': 'ADJECTIVE'},
                    {'word': 'ਪੀਲਾ', 'romanization': 'Peela', 'translation': 'Yellow', 'pos': 'ADJECTIVE'},
                    {'word': 'ਹਰਾ', 'romanization': 'Hara', 'translation': 'Green', 'pos': 'ADJECTIVE'},
                ]
            },
            {
                'name': 'Numbers',
                'name_native': 'ਸੰਖਿਆ',
                'icon': 'numbers',
                'level': 1,
                'words': [
                    {'word': 'ਇੱਕ', 'romanization': 'Ikk', 'translation': 'One', 'pos': 'NUMBER'},
                    {'word': 'ਦੋ', 'romanization': 'Do', 'translation': 'Two', 'pos': 'NUMBER'},
                    {'word': 'ਤਿੰਨ', 'romanization': 'Tinn', 'translation': 'Three', 'pos': 'NUMBER'},
                    {'word': 'ਚਾਰ', 'romanization': 'Chaar', 'translation': 'Four', 'pos': 'NUMBER'},
                    {'word': 'ਪੰਜ', 'romanization': 'Panj', 'translation': 'Five', 'pos': 'NUMBER'},
                ]
            },
            {
                'name': 'Animals',
                'name_native': 'ਜਾਨਵਰ',
                'icon': 'pets',
                'level': 1,
                'words': [
                    {'word': 'ਕੁੱਤਾ', 'romanization': 'Kutta', 'translation': 'Dog', 'pos': 'NOUN'},
                    {'word': 'ਬਿੱਲੀ', 'romanization': 'Billi', 'translation': 'Cat', 'pos': 'NOUN'},
                    {'word': 'ਗਾਂ', 'romanization': 'Gaan', 'translation': 'Cow', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Basics',
                'name_native': 'ਮੁੱਢਲੇ',
                'icon': 'star',
                'level': 1,
                'words': [
                    {'word': 'ਪਾਣੀ', 'romanization': 'Paani', 'translation': 'Water', 'pos': 'NOUN'},
                    {'word': 'ਰੋਟੀ', 'romanization': 'Roti', 'translation': 'Bread', 'pos': 'NOUN'},
                ]
            },
        ]

        # L2 Vocabulary (50 words)
        l2_themes = [
            {
                'name': 'Extended Family',
                'name_native': 'ਵੱਡਾ ਪਰਿਵਾਰ',
                'icon': 'groups',
                'level': 2,
                'words': [
                    {'word': 'ਨਾਨੀ', 'romanization': 'Naani', 'translation': 'Grandmother (maternal)', 'pos': 'NOUN'},
                    {'word': 'ਨਾਨਾ', 'romanization': 'Naana', 'translation': 'Grandfather (maternal)', 'pos': 'NOUN'},
                    {'word': 'ਚਾਚਾ', 'romanization': 'Chaacha', 'translation': 'Uncle (paternal)', 'pos': 'NOUN'},
                    {'word': 'ਚਾਚੀ', 'romanization': 'Chaachi', 'translation': 'Aunt (paternal)', 'pos': 'NOUN'},
                    {'word': 'ਮਾਮਾ', 'romanization': 'Maama', 'translation': 'Uncle (maternal)', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'More Colors',
                'name_native': 'ਹੋਰ ਰੰਗ',
                'icon': 'color_lens',
                'level': 2,
                'words': [
                    {'word': 'ਕਾਲਾ', 'romanization': 'Kaala', 'translation': 'Black', 'pos': 'ADJECTIVE'},
                    {'word': 'ਚਿੱਟਾ', 'romanization': 'Chitta', 'translation': 'White', 'pos': 'ADJECTIVE'},
                    {'word': 'ਸੰਤਰੀ', 'romanization': 'Santri', 'translation': 'Orange', 'pos': 'ADJECTIVE'},
                ]
            },
            {
                'name': 'Numbers 6-10',
                'name_native': 'ਸੰਖਿਆ ੬-੧੦',
                'icon': 'pin',
                'level': 2,
                'words': [
                    {'word': 'ਛੇ', 'romanization': 'Chheh', 'translation': 'Six', 'pos': 'NUMBER'},
                    {'word': 'ਸੱਤ', 'romanization': 'Satt', 'translation': 'Seven', 'pos': 'NUMBER'},
                    {'word': 'ਅੱਠ', 'romanization': 'Atth', 'translation': 'Eight', 'pos': 'NUMBER'},
                    {'word': 'ਨੌਂ', 'romanization': 'Naunh', 'translation': 'Nine', 'pos': 'NUMBER'},
                    {'word': 'ਦਸ', 'romanization': 'Das', 'translation': 'Ten', 'pos': 'NUMBER'},
                ]
            },
            {
                'name': 'More Animals',
                'name_native': 'ਹੋਰ ਜਾਨਵਰ',
                'icon': 'cruelty_free',
                'level': 2,
                'words': [
                    {'word': 'ਘੋੜਾ', 'romanization': 'Ghoda', 'translation': 'Horse', 'pos': 'NOUN'},
                    {'word': 'ਹਾਥੀ', 'romanization': 'Haathi', 'translation': 'Elephant', 'pos': 'NOUN'},
                    {'word': 'ਸ਼ੇਰ', 'romanization': 'Sher', 'translation': 'Lion', 'pos': 'NOUN'},
                    {'word': 'ਬਾਂਦਰ', 'romanization': 'Baandar', 'translation': 'Monkey', 'pos': 'NOUN'},
                    {'word': 'ਚਿੜੀ', 'romanization': 'Chidi', 'translation': 'Sparrow', 'pos': 'NOUN'},
                    {'word': 'ਮੱਛੀ', 'romanization': 'Machchhi', 'translation': 'Fish', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Fruits',
                'name_native': 'ਫਲ',
                'icon': 'nutrition',
                'level': 2,
                'words': [
                    {'word': 'ਸੇਬ', 'romanization': 'Seb', 'translation': 'Apple', 'pos': 'NOUN'},
                    {'word': 'ਕੇਲਾ', 'romanization': 'Kela', 'translation': 'Banana', 'pos': 'NOUN'},
                    {'word': 'ਆਮ', 'romanization': 'Aam', 'translation': 'Mango', 'pos': 'NOUN'},
                    {'word': 'ਅੰਗੂਰ', 'romanization': 'Angoor', 'translation': 'Grapes', 'pos': 'NOUN'},
                    {'word': 'ਸੰਤਰਾ', 'romanization': 'Santara', 'translation': 'Orange', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Drinks',
                'name_native': 'ਪੀਣ ਵਾਲੇ',
                'icon': 'local_cafe',
                'level': 2,
                'words': [
                    {'word': 'ਦੁੱਧ', 'romanization': 'Duddh', 'translation': 'Milk', 'pos': 'NOUN'},
                    {'word': 'ਲੱਸੀ', 'romanization': 'Lassi', 'translation': 'Lassi', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Body Parts',
                'name_native': 'ਸਰੀਰ ਦੇ ਅੰਗ',
                'icon': 'accessibility',
                'level': 2,
                'words': [
                    {'word': 'ਸਿਰ', 'romanization': 'Sir', 'translation': 'Head', 'pos': 'NOUN'},
                    {'word': 'ਅੱਖ', 'romanization': 'Akkh', 'translation': 'Eye', 'pos': 'NOUN'},
                    {'word': 'ਨੱਕ', 'romanization': 'Nakk', 'translation': 'Nose', 'pos': 'NOUN'},
                    {'word': 'ਕੰਨ', 'romanization': 'Kann', 'translation': 'Ear', 'pos': 'NOUN'},
                    {'word': 'ਮੂੰਹ', 'romanization': 'Moonh', 'translation': 'Mouth', 'pos': 'NOUN'},
                    {'word': 'ਹੱਥ', 'romanization': 'Hatth', 'translation': 'Hand', 'pos': 'NOUN'},
                    {'word': 'ਪੈਰ', 'romanization': 'Pair', 'translation': 'Foot', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Actions',
                'name_native': 'ਕਿਰਿਆ',
                'icon': 'directions_run',
                'level': 2,
                'words': [
                    {'word': 'ਖਾਣਾ', 'romanization': 'Khaana', 'translation': 'To eat', 'pos': 'VERB'},
                    {'word': 'ਪੀਣਾ', 'romanization': 'Peena', 'translation': 'To drink', 'pos': 'VERB'},
                    {'word': 'ਸੌਣਾ', 'romanization': 'Sauna', 'translation': 'To sleep', 'pos': 'VERB'},
                    {'word': 'ਖੇਡਣਾ', 'romanization': 'Khedna', 'translation': 'To play', 'pos': 'VERB'},
                    {'word': 'ਪੜ੍ਹਨਾ', 'romanization': 'Parhna', 'translation': 'To read', 'pos': 'VERB'},
                    {'word': 'ਲਿਖਣਾ', 'romanization': 'Likhna', 'translation': 'To write', 'pos': 'VERB'},
                ]
            },
            {
                'name': 'Home',
                'name_native': 'ਘਰ',
                'icon': 'home',
                'level': 2,
                'words': [
                    {'word': 'ਘਰ', 'romanization': 'Ghar', 'translation': 'Home', 'pos': 'NOUN'},
                    {'word': 'ਕਮਰਾ', 'romanization': 'Kamra', 'translation': 'Room', 'pos': 'NOUN'},
                    {'word': 'ਦਰਵਾਜ਼ਾ', 'romanization': 'Darvaaza', 'translation': 'Door', 'pos': 'NOUN'},
                    {'word': 'ਖਿੜਕੀ', 'romanization': 'Khidki', 'translation': 'Window', 'pos': 'NOUN'},
                    {'word': 'ਮੇਜ਼', 'romanization': 'Mez', 'translation': 'Table', 'pos': 'NOUN'},
                    {'word': 'ਕੁਰਸੀ', 'romanization': 'Kursi', 'translation': 'Chair', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Nature',
                'name_native': 'ਕੁਦਰਤ',
                'icon': 'park',
                'level': 2,
                'words': [
                    {'word': 'ਸੂਰਜ', 'romanization': 'Sooraj', 'translation': 'Sun', 'pos': 'NOUN'},
                    {'word': 'ਚੰਦ', 'romanization': 'Chand', 'translation': 'Moon', 'pos': 'NOUN'},
                    {'word': 'ਤਾਰਾ', 'romanization': 'Taara', 'translation': 'Star', 'pos': 'NOUN'},
                    {'word': 'ਫੁੱਲ', 'romanization': 'Phull', 'translation': 'Flower', 'pos': 'NOUN'},
                    {'word': 'ਰੁੱਖ', 'romanization': 'Rukkh', 'translation': 'Tree', 'pos': 'NOUN'},
                ]
            },
        ]

        all_themes = l1_themes + l2_themes
        word_count = 0

        for i, theme_data in enumerate(all_themes, 1):
            theme, _ = VocabularyTheme.objects.update_or_create(
                language='PUNJABI',
                name=theme_data['name'],
                defaults={
                    'name_native': theme_data['name_native'],
                    'description': f"Learn {theme_data['name']} in Punjabi",
                    'icon': theme_data['icon'],
                    'level': theme_data['level'],
                    'order': i,
                    'is_premium': theme_data['level'] > 1,
                    'is_active': True,
                }
            )

            for j, word_data in enumerate(theme_data['words'], 1):
                VocabularyWord.objects.update_or_create(
                    theme=theme,
                    word=word_data['word'],
                    defaults={
                        'romanization': word_data['romanization'],
                        'translation': word_data['translation'],
                        'part_of_speech': word_data['pos'],
                        'difficulty': theme_data['level'],
                        'order': j,
                    }
                )
                word_count += 1

        self.stdout.write(self.style.SUCCESS(f'  Created {len(all_themes)} themes with {word_count} words'))

    def seed_stories(self):
        """Create Punjabi stories for L1 and L2."""
        self.stdout.write('Creating Punjabi stories...')

        stories_data = [
            # L1 Stories (3)
            {
                'title': "Peppi's New Friend",
                'title_hindi': 'ਪੈੱਪੀ ਦਾ ਨਵਾਂ ਦੋਸਤ',
                'title_romanized': "Peppi da Navaan Dost",
                'level': 1,
                'age_min': 4,
                'age_max': 6,
                'theme': 'friendship',
                'tier': 'FREE',
                'moral_english': 'True friends accept each other as they are',
                'moral_hindi': 'ਸੱਚੇ ਦੋਸਤ ਇੱਕ ਦੂਜੇ ਨੂੰ ਜਿਵੇਂ ਹਨ ਮੰਨਦੇ ਹਨ',
                'pages': [
                    {'text': 'ਪੈੱਪੀ ਇੱਕ ਬਿੱਲੀ ਹੈ।', 'translation': 'Peppi is a cat.'},
                    {'text': 'ਪੈੱਪੀ ਨੂੰ ਦੋਸਤ ਚਾਹੀਦਾ।', 'translation': 'Peppi wants a friend.'},
                    {'text': 'ਪੈੱਪੀ ਨੇ ਇੱਕ ਕੁੱਤਾ ਦੇਖਿਆ।', 'translation': 'Peppi saw a dog.'},
                    {'text': 'ਕੁੱਤੇ ਦਾ ਨਾਮ ਮੋਤੀ ਹੈ।', 'translation': "The dog's name is Moti."},
                    {'text': 'ਪੈੱਪੀ ਅਤੇ ਮੋਤੀ ਦੋਸਤ ਬਣ ਗਏ!', 'translation': 'Peppi and Moti became friends!'},
                ]
            },
            {
                'title': 'The Red Apple',
                'title_hindi': 'ਲਾਲ ਸੇਬ',
                'title_romanized': 'Laal Seb',
                'level': 1,
                'age_min': 4,
                'age_max': 6,
                'theme': 'sharing',
                'tier': 'FREE',
                'moral_english': 'Sharing brings happiness',
                'moral_hindi': 'ਵੰਡਣ ਨਾਲ ਖੁਸ਼ੀ ਮਿਲਦੀ ਹੈ',
                'pages': [
                    {'text': 'ਰੁੱਖ ਤੇ ਇੱਕ ਸੇਬ ਹੈ।', 'translation': 'There is an apple on the tree.'},
                    {'text': 'ਸੇਬ ਲਾਲ ਹੈ।', 'translation': 'The apple is red.'},
                    {'text': 'ਬੱਚਾ ਸੇਬ ਲੈਣਾ ਚਾਹੁੰਦਾ।', 'translation': 'The child wants the apple.'},
                    {'text': 'ਮਾਂ ਨੇ ਸੇਬ ਦਿੱਤਾ।', 'translation': 'Mother gave the apple.'},
                    {'text': 'ਬੱਚਾ ਖੁਸ਼ ਹੈ!', 'translation': 'The child is happy!'},
                ]
            },
            {
                'title': 'My Family',
                'title_hindi': 'ਮੇਰਾ ਪਰਿਵਾਰ',
                'title_romanized': 'Mera Parivaar',
                'level': 1,
                'age_min': 4,
                'age_max': 6,
                'theme': 'family',
                'tier': 'FREE',
                'moral_english': 'Family is our biggest treasure',
                'moral_hindi': 'ਪਰਿਵਾਰ ਸਾਡਾ ਸਭ ਤੋਂ ਵੱਡਾ ਖ਼ਜ਼ਾਨਾ ਹੈ',
                'pages': [
                    {'text': 'ਇਹ ਮੇਰੀ ਮਾਂ ਹੈ।', 'translation': 'This is my mother.'},
                    {'text': 'ਇਹ ਮੇਰੇ ਪਾਪਾ ਹਨ।', 'translation': 'This is my father.'},
                    {'text': 'ਇਹ ਮੇਰੀ ਭੈਣ ਹੈ।', 'translation': 'This is my sister.'},
                    {'text': 'ਇਹ ਮੇਰਾ ਵੀਰ ਹੈ।', 'translation': 'This is my brother.'},
                    {'text': 'ਅਸੀਂ ਸਾਰੇ ਮਿਲ ਕੇ ਰਹਿੰਦੇ ਹਾਂ।', 'translation': 'We all live together.'},
                ]
            },
            # L2 Stories (7)
            {
                'title': 'Vaisakhi Fair',
                'title_hindi': 'ਵਿਸਾਖੀ ਦਾ ਮੇਲਾ',
                'title_romanized': 'Vaisakhi da Mela',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'festival',
                'tier': 'STANDARD',
                'moral_english': 'Festivals bring joy and unity',
                'moral_hindi': 'ਤਿਉਹਾਰ ਖੁਸ਼ੀ ਅਤੇ ਏਕਤਾ ਲਿਆਉਂਦੇ ਹਨ',
                'pages': [
                    {'text': 'ਅੱਜ ਵਿਸਾਖੀ ਹੈ!', 'translation': 'Today is Vaisakhi!'},
                    {'text': 'ਸਾਰੇ ਲੋਕ ਖੁਸ਼ ਹਨ।', 'translation': 'Everyone is happy.'},
                    {'text': 'ਲੋਕ ਭੰਗੜਾ ਪਾਉਂਦੇ ਹਨ।', 'translation': 'People do Bhangra.'},
                    {'text': 'ਬੱਚੇ ਝੂਲੇ ਝੂਲਦੇ ਹਨ।', 'translation': 'Children swing.'},
                    {'text': 'ਮਾਂ ਨੇ ਮਿੱਠੀ ਲੱਸੀ ਦਿੱਤੀ।', 'translation': 'Mother gave sweet lassi.'},
                    {'text': 'ਬੱਲੇ ਬੱਲੇ! ਵਿਸਾਖੀ ਮੁਬਾਰਕ!', 'translation': 'Hurray! Happy Vaisakhi!'},
                ]
            },
            {
                'title': 'The Clever Fox',
                'title_hindi': 'ਚਤੁਰ ਲੂੰਬੜੀ',
                'title_romanized': 'Chatur Loombdi',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'wisdom',
                'tier': 'STANDARD',
                'moral_english': 'Think before you act',
                'moral_hindi': 'ਕੰਮ ਕਰਨ ਤੋਂ ਪਹਿਲਾਂ ਸੋਚੋ',
                'pages': [
                    {'text': 'ਇੱਕ ਲੂੰਬੜੀ ਸੀ।', 'translation': 'There was a fox.'},
                    {'text': 'ਉਸਨੂੰ ਭੁੱਖ ਲੱਗੀ।', 'translation': 'She was hungry.'},
                    {'text': 'ਉਸਨੇ ਇੱਕ ਕਾਂ ਦੇਖਿਆ।', 'translation': 'She saw a crow.'},
                    {'text': 'ਕਾਂ ਕੋਲ ਰੋਟੀ ਸੀ।', 'translation': 'The crow had bread.'},
                    {'text': 'ਲੂੰਬੜੀ ਨੇ ਕਿਹਾ - ਗਾਓ!', 'translation': 'Fox said - Sing!'},
                    {'text': 'ਕਾਂ ਨੇ ਮੂੰਹ ਖੋਲ੍ਹਿਆ।', 'translation': 'Crow opened his mouth.'},
                    {'text': 'ਰੋਟੀ ਡਿੱਗ ਗਈ!', 'translation': 'The bread fell!'},
                ]
            },
            {
                'title': 'Lohri Festival',
                'title_hindi': 'ਲੋਹੜੀ ਦੀ ਰਾਤ',
                'title_romanized': 'Lohri di Raat',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'festival',
                'tier': 'STANDARD',
                'moral_english': 'Celebrate together with joy',
                'moral_hindi': 'ਖੁਸ਼ੀ ਨਾਲ ਮਿਲ ਕੇ ਮਨਾਓ',
                'pages': [
                    {'text': 'ਅੱਜ ਲੋਹੜੀ ਹੈ।', 'translation': 'Today is Lohri.'},
                    {'text': 'ਅੱਗ ਜਗਾਈ।', 'translation': 'The bonfire is lit.'},
                    {'text': 'ਲੋਕ ਭੰਗੜਾ ਪਾਉਂਦੇ ਹਨ।', 'translation': 'People dance Bhangra.'},
                    {'text': 'ਮੂੰਗਫਲੀ ਅਤੇ ਰਿਓੜੀਆਂ।', 'translation': 'Peanuts and sweets.'},
                    {'text': 'ਲੋਹੜੀ ਮੁਬਾਰਕ!', 'translation': 'Happy Lohri!'},
                ]
            },
            {
                'title': 'Day at Farm',
                'title_hindi': 'ਖੇਤ ਦਾ ਦਿਨ',
                'title_romanized': 'Khet da Din',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'nature',
                'tier': 'STANDARD',
                'moral_english': 'Respect nature and farmers',
                'moral_hindi': 'ਕੁਦਰਤ ਅਤੇ ਕਿਸਾਨਾਂ ਦਾ ਸਤਿਕਾਰ ਕਰੋ',
                'pages': [
                    {'text': 'ਅੱਜ ਖੇਤ ਗਏ।', 'translation': 'Today we went to the farm.'},
                    {'text': 'ਗਾਂ ਦੁੱਧ ਦਿੰਦੀ।', 'translation': 'The cow gives milk.'},
                    {'text': 'ਮੁਰਗੀ ਕੁਕੜੂੰ ਕੂ ਕਰਦੀ।', 'translation': 'The hen clucks.'},
                    {'text': 'ਕਣਕ ਸੁਨਹਿਰੀ।', 'translation': 'The wheat is golden.'},
                    {'text': 'ਖੇਤੀ ਬਹੁਤ ਵਧੀਆ!', 'translation': 'Farming is great!'},
                ]
            },
            {
                'title': 'The Thirsty Crow',
                'title_hindi': 'ਪਿਆਸਾ ਕਾਂ',
                'title_romanized': 'Pyaasa Kaaan',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'wisdom',
                'tier': 'STANDARD',
                'moral_english': 'Where there is a will, there is a way',
                'moral_hindi': 'ਜਿੱਥੇ ਚਾਹ ਉੱਥੇ ਰਾਹ',
                'pages': [
                    {'text': 'ਇੱਕ ਕਾਂ ਸੀ।', 'translation': 'There was a crow.'},
                    {'text': 'ਉਹ ਪਿਆਸਾ ਸੀ।', 'translation': 'He was thirsty.'},
                    {'text': 'ਉਸਨੇ ਘੜਾ ਦੇਖਿਆ।', 'translation': 'He saw a pot.'},
                    {'text': 'ਪਾਣੀ ਥੋੜਾ ਸੀ।', 'translation': 'Water was less.'},
                    {'text': 'ਕੰਕਰ ਪਾਏ।', 'translation': 'He dropped pebbles.'},
                    {'text': 'ਪਾਣੀ ਉੱਪਰ ਆਇਆ!', 'translation': 'Water came up!'},
                ]
            },
            {
                'title': "Guru Nanak's Birthday",
                'title_hindi': 'ਗੁਰਪੁਰਬ',
                'title_romanized': 'Gurpurab',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'festival',
                'tier': 'STANDARD',
                'moral_english': 'Service to others is service to God',
                'moral_hindi': 'ਲੋਕਾਂ ਦੀ ਸੇਵਾ ਹੀ ਰੱਬ ਦੀ ਸੇਵਾ',
                'pages': [
                    {'text': 'ਅੱਜ ਗੁਰਪੁਰਬ ਹੈ।', 'translation': "Today is Guru Nanak's birthday."},
                    {'text': 'ਗੁਰਦੁਆਰੇ ਗਏ।', 'translation': 'We went to Gurdwara.'},
                    {'text': 'ਲੰਗਰ ਛਕਿਆ।', 'translation': 'We ate langar.'},
                    {'text': 'ਸ਼ਬਦ ਸੁਣੇ।', 'translation': 'We listened to hymns.'},
                    {'text': 'ਸੇਵਾ ਕੀਤੀ।', 'translation': 'We did service.'},
                    {'text': 'ਵਾਹਿਗੁਰੂ!', 'translation': 'Waheguru!'},
                ]
            },
            {
                'title': 'Auckland Zoo',
                'title_hindi': 'ਆਕਲੈਂਡ ਚਿੜੀਆਘਰ',
                'title_romanized': 'Auckland Chidiyaghar',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'animals',
                'tier': 'STANDARD',
                'moral_english': 'Love and protect all animals',
                'moral_hindi': 'ਸਾਰੇ ਜਾਨਵਰਾਂ ਨੂੰ ਪਿਆਰ ਅਤੇ ਬਚਾਓ',
                'pages': [
                    {'text': 'ਅੱਜ ਚਿੜੀਆਘਰ ਗਏ।', 'translation': 'Today we went to the zoo.'},
                    {'text': 'ਸ਼ੇਰ ਦੇਖਿਆ।', 'translation': 'We saw a lion.'},
                    {'text': 'ਹਾਥੀ ਵੱਡਾ ਸੀ।', 'translation': 'The elephant was big.'},
                    {'text': 'ਬਾਂਦਰ ਕੁੱਦਦੇ ਸਨ।', 'translation': 'Monkeys were jumping.'},
                    {'text': 'ਕੀਵੀ ਪੰਛੀ ਦੇਖਿਆ!', 'translation': 'We saw a Kiwi bird!'},
                    {'text': 'ਬਹੁਤ ਮਜ਼ਾ ਆਇਆ!', 'translation': 'It was so much fun!'},
                ]
            },
        ]

        for story_data in stories_data:
            # Create unique storyweaver_id for Punjabi stories
            story_slug = story_data['title'].lower().replace(' ', '-').replace("'", '')
            storyweaver_id = f"pb-l{story_data['level']}-{story_slug}"

            story, _ = Story.objects.update_or_create(
                storyweaver_id=storyweaver_id,
                defaults={
                    'language': 'PUNJABI',
                    'slug': story_slug,
                    'title': story_data['title'],
                    'title_hindi': story_data['title_hindi'],
                    'title_romanized': story_data['title_romanized'],
                    'level': story_data['level'],
                    'page_count': len(story_data['pages']),
                    'age_min': story_data['age_min'],
                    'age_max': story_data['age_max'],
                    'is_l1_content': True,
                    'theme': story_data['theme'],
                    'tier': story_data['tier'],
                    'moral_english': story_data['moral_english'],
                    'moral_hindi': story_data['moral_hindi'],
                    'xp_reward': 30 if story_data['level'] == 1 else 50,
                    'estimated_minutes': 5,
                    'is_featured': story_data['tier'] == 'FREE',
                    'is_active': True,
                }
            )

            # Create story pages
            for i, page_data in enumerate(story_data['pages'], 1):
                StoryPage.objects.update_or_create(
                    story=story,
                    page_number=i,
                    defaults={
                        'text_content': page_data['text'],
                        'text_hindi': page_data['text'],  # Punjabi text in the hindi field
                        'text_romanized': page_data['translation'],
                    }
                )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(stories_data)} stories'))

    def seed_songs(self):
        """Create Punjabi songs for L1 and L2."""
        self.stdout.write('Creating Punjabi songs...')

        # Get or create L1 level
        l1_level, _ = CurriculumLevel.objects.get_or_create(
            code='L1',
            defaults={
                'name_english': 'Discovery',
                'name_hindi': 'ਖੋਜ',
                'name_romanized': 'Khoj',
                'min_age': 4,
                'max_age': 5,
                'description': 'First steps in learning Punjabi',
                'order': 1,
                'is_active': True,
            }
        )

        songs_data = [
            {
                'title_english': 'Hide and Seek',
                'title_hindi': 'ਅੱਖ ਮਿਚੌਲੀ',
                'title_romanized': 'Akkh Michauli',
                'lyrics_hindi': '''ਅੱਖ ਮਿਚੌਲੀ ਖੇਡੀਏ,
ਆਓ ਸਾਰੇ ਮਿਲ ਕੇ,
ਇੱਕ ਦੋ ਤਿੰਨ ਗਿਣੀਏ,
ਫਿਰ ਲੁਕ ਜਾਈਏ!''',
                'lyrics_romanized': '''Akkh michauli khediye,
Aao saare mil ke,
Ikk do tinn giniye,
Phir luk jaiye!''',
                'lyrics_english': '''Let us play hide and seek,
Come together everyone,
Let us count one two three,
Then hide away!''',
                'category': 'RHYME',
                'age_min': 4,
                'age_max': 6,
                'duration_seconds': 60,
            },
            {
                'title_english': 'Uncle Moon',
                'title_hindi': 'ਚੰਦਾ ਮਾਮਾ',
                'title_romanized': 'Chanda Mama',
                'lyrics_hindi': '''ਚੰਦਾ ਮਾਮਾ ਦੂਰ ਦੇ,
ਪੁਏ ਪਕਾਵੇ ਬੂਰ ਦੇ,
ਆਪ ਖਾਵੇ ਥਾਲੀ ਵਿੱਚ,
ਮੁੰਡੇ ਨੂੰ ਦੇ ਪਿਆਲੀ ਵਿੱਚ!''',
                'lyrics_romanized': '''Chanda mama door de,
Pue pakaave boor de,
Aap khaave thaali vich,
Munde nu de pyaali vich!''',
                'lyrics_english': '''Uncle Moon is far away,
Makes sweets of sugar powder,
Eats himself in a plate,
Gives the child in a small bowl!''',
                'category': 'RHYME',
                'age_min': 4,
                'age_max': 6,
                'duration_seconds': 45,
            },
            {
                'title_english': 'Alphabet Song',
                'title_hindi': 'ਵਰਣਮਾਲਾ ਗੀਤ',
                'title_romanized': 'Varnmala Geet',
                'lyrics_hindi': '''ਊੜਾ ਐੜਾ ਈੜੀ,
ਸੱਸਾ ਹਾਹਾ ਕੱਕਾ,
ਪੰਜਾਬੀ ਹੈ ਮਿੱਠੀ,
ਆਓ ਪੜ੍ਹੀਏ ਪੱਕਾ!''',
                'lyrics_romanized': '''Oorda aida eedi,
Sassa haaha kakka,
Punjabi hai mitthi,
Aao parhiye pakka!''',
                'lyrics_english': '''Oorda aida eedi,
Sassa haaha kakka,
Punjabi is sweet,
Let us read properly!''',
                'category': 'EDUCATIONAL',
                'age_min': 4,
                'age_max': 7,
                'duration_seconds': 90,
            },
            {
                'title_english': 'The Train',
                'title_hindi': 'ਰੇਲ ਗੱਡੀ',
                'title_romanized': 'Rail Gaddi',
                'lyrics_hindi': '''ਛੁੱਕ ਛੁੱਕ ਰੇਲ ਗੱਡੀ,
ਚੱਲੀ ਜਾਵੇ ਤੇਜ਼ੀ,
ਸਟੇਸ਼ਨ ਤੇ ਰੁਕੀ,
ਸਾਰੇ ਉੱਤਰੇ ਖੁਸ਼ੀ!''',
                'lyrics_romanized': '''Chhukk chhukk rail gaddi,
Challi jaave tezi,
Station te ruki,
Saare uttre khushi!''',
                'lyrics_english': '''Choo choo goes the train,
Running fast along,
It stopped at the station,
Everyone got off happy!''',
                'category': 'RHYME',
                'age_min': 4,
                'age_max': 6,
                'duration_seconds': 50,
            },
            {
                'title_english': 'Do Bhangra',
                'title_hindi': 'ਭੰਗੜਾ ਪਾਓ',
                'title_romanized': 'Bhangra Pao',
                'lyrics_hindi': '''ਬੱਲੇ ਬੱਲੇ ਭੰਗੜਾ ਪਾਓ,
ਹੱਥ ਉੱਚੇ ਕਰ ਕੇ ਨੱਚੋ,
ਢੋਲ ਦੀ ਧੁਨ ਤੇ ਝੂਮੋ,
ਖੁਸ਼ੀ ਨਾਲ ਗਾਓ!''',
                'lyrics_romanized': '''Balle balle bhangra pao,
Hatth uche kar ke nacho,
Dhol di dhun te jhoomo,
Khushi naal gao!''',
                'lyrics_english': '''Hurray hurray do Bhangra,
Dance with hands up high,
Sway to the drum beat,
Sing with happiness!''',
                'category': 'FOLK',
                'age_min': 5,
                'age_max': 8,
                'duration_seconds': 75,
            },
        ]

        for i, song_data in enumerate(songs_data, 1):
            Song.objects.update_or_create(
                level=l1_level,
                title_english=song_data['title_english'],
                defaults={
                    'title_hindi': song_data['title_hindi'],
                    'title_romanized': song_data['title_romanized'],
                    'lyrics_hindi': song_data['lyrics_hindi'],
                    'lyrics_romanized': song_data['lyrics_romanized'],
                    'lyrics_english': song_data['lyrics_english'],
                    'category': song_data['category'],
                    'age_min': song_data['age_min'],
                    'age_max': song_data['age_max'],
                    'duration_seconds': song_data['duration_seconds'],
                    'language': 'PUNJABI',
                    'order': i,
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(songs_data)} songs'))

    def seed_curriculum_levels(self):
        """Create L1 and L2 curriculum levels."""
        self.stdout.write('Creating curriculum levels...')

        levels_data = [
            {
                'code': 'L1',
                'name_english': 'Discovery',
                'name_hindi': 'ਖੋਜ',
                'name_romanized': 'Khoj',
                'min_age': 4,
                'max_age': 5,
                'description': 'First steps in learning Punjabi. Children learn basic greetings, vowels, and simple words.',
                'peppi_welcome': 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਜੀ! Welcome to Peppi\'s Punjabi class!',
                'peppi_completion': 'ਬੱਲੇ ਬੱਲੇ! You completed L1! Let\'s move to L2!',
                'emoji': '🌱',
                'theme_color': '#22c55e',
                'order': 1,
                'estimated_hours': 10,
                'min_xp_required': 0,
                'xp_reward': 400,
                'is_free': True,
            },
            {
                'code': 'L2',
                'name_english': 'Building Blocks',
                'name_hindi': 'ਬੁਨਿਆਦੀ ਪੱਥਰ',
                'name_romanized': 'Buniyadi Patthar',
                'min_age': 5,
                'max_age': 6,
                'description': 'Learn consonants, matras, and start reading simple words and sentences.',
                'peppi_welcome': 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ! Ready to learn more Punjabi?',
                'peppi_completion': 'ਵਾਹ ਜੀ ਵਾਹ! You are a Punjabi superstar!',
                'emoji': '🌿',
                'theme_color': '#3b82f6',
                'order': 2,
                'estimated_hours': 14,
                'min_xp_required': 400,
                'xp_reward': 700,
                'is_free': False,
            },
        ]

        for level_data in levels_data:
            CurriculumLevel.objects.update_or_create(
                code=level_data['code'],
                defaults=level_data
            )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(levels_data)} curriculum levels'))

    def seed_peppi_phrases(self):
        """Create Peppi phrases in Punjabi."""
        self.stdout.write('Creating Peppi phrases...')

        phrases_data = [
            {'category': 'GREETING', 'text_hindi': 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਜੀ!', 'text_english': 'Hello!', 'text_romanized': 'Sat Sri Akaal ji!', 'context': 'punjabi_greeting'},
            {'category': 'CORRECT', 'text_hindi': 'ਬੱਲੇ ਬੱਲੇ!', 'text_english': 'Hurray!', 'text_romanized': 'Balle Balle!', 'context': 'punjabi_celebration'},
            {'category': 'CORRECT', 'text_hindi': 'ਵਾਹ ਜੀ ਵਾਹ!', 'text_english': 'Wow!', 'text_romanized': 'Waah ji waah!', 'context': 'punjabi_wow'},
            {'category': 'CORRECT', 'text_hindi': 'ਸ਼ਾਬਾਸ਼!', 'text_english': 'Well done!', 'text_romanized': 'Shabaash!', 'context': 'punjabi_welldone'},
            {'category': 'CORRECT', 'text_hindi': 'ਬਹੁਤ ਵਧੀਆ!', 'text_english': 'Very good!', 'text_romanized': 'Bahut vadhiya!', 'context': 'punjabi_verygood'},
            {'category': 'WRONG', 'text_hindi': 'ਹੋਰ ਕੋਸ਼ਿਸ਼ ਕਰੋ!', 'text_english': 'Try again!', 'text_romanized': 'Hor koshish karo!', 'context': 'punjabi_tryagain'},
            {'category': 'ENCOURAGEMENT', 'text_hindi': 'ਤੁਸੀਂ ਕਰ ਸਕਦੇ ਹੋ!', 'text_english': 'You can do it!', 'text_romanized': 'Tusi kar sakde ho!', 'context': 'punjabi_encourage'},
            {'category': 'FAREWELL', 'text_hindi': 'ਅਲਵਿਦਾ!', 'text_english': 'Goodbye!', 'text_romanized': 'Alvida!', 'context': 'punjabi_farewell'},
            {'category': 'GREETING', 'text_hindi': 'ਧੰਨਵਾਦ!', 'text_english': 'Thank you!', 'text_romanized': 'Dhannvaad!', 'context': 'punjabi_thankyou'},
            {'category': 'ENCOURAGEMENT', 'text_hindi': 'ਚੱਲੋ ਜੀ!', 'text_english': "Let's go!", 'text_romanized': 'Challo ji!', 'context': 'punjabi_letsgo'},
        ]

        for phrase_data in phrases_data:
            PeppiPhrase.objects.update_or_create(
                category=phrase_data['category'],
                text_hindi=phrase_data['text_hindi'],
                defaults={
                    'text_english': phrase_data['text_english'],
                    'text_romanized': phrase_data['text_romanized'],
                    'context': phrase_data['context'],
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(phrases_data)} Peppi phrases'))

    def seed_games(self):
        """Create Punjabi games."""
        self.stdout.write('Creating Punjabi games...')

        games_data = [
            {
                'name': 'Gurmukhi Memory',
                'description': 'Match Punjabi letters with their sounds',
                'game_type': 'MEMORY',
                'skill_focus': 'ALPHABET',
                'level': 1,
            },
            {
                'name': 'Punjabi Word Search',
                'description': 'Find hidden Punjabi words',
                'game_type': 'WORDSEARCH',
                'skill_focus': 'VOCAB',
                'level': 1,
            },
            {
                'name': 'Listen and Match',
                'description': 'Listen to Punjabi words and match with pictures',
                'game_type': 'LISTENING',
                'skill_focus': 'LISTENING',
                'level': 1,
            },
            {
                'name': 'Punjabi Quiz',
                'description': 'Test your Punjabi knowledge',
                'game_type': 'QUIZ',
                'skill_focus': 'MIXED',
                'level': 2,
            },
            {
                'name': 'Word Builder',
                'description': 'Build Punjabi words using letters',
                'game_type': 'BUILDER',
                'skill_focus': 'SPELLING',
                'level': 2,
            },
        ]

        for game_data in games_data:
            Game.objects.update_or_create(
                language='PUNJABI',
                name=game_data['name'],
                defaults={
                    'description': game_data['description'],
                    'instructions': f"Play {game_data['name']} to practice Punjabi!",
                    'game_type': game_data['game_type'],
                    'skill_focus': game_data['skill_focus'],
                    'level': game_data['level'],
                    'duration_seconds': 300,
                    'questions_per_round': 10,
                    'lives': 3,
                    'points_per_correct': 10,
                    'bonus_completion': 50,
                    'is_premium': game_data['level'] > 1,
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(games_data)} games'))

    def seed_assessments(self):
        """Create Punjabi assessments."""
        self.stdout.write('Creating Punjabi assessments...')

        assessments_data = [
            {
                'name': 'L1 Entry Assessment',
                'description': 'Check your starting level in Punjabi',
                'assessment_type': 'PLACEMENT',
                'level': 1,
                'questions_count': 5,
            },
            {
                'name': 'L1 Exit Assessment',
                'description': 'Complete L1 and move to L2',
                'assessment_type': 'LEVEL_UP',
                'level': 1,
                'questions_count': 10,
            },
        ]

        for assess_data in assessments_data:
            Assessment.objects.update_or_create(
                language='PUNJABI',
                name=assess_data['name'],
                defaults={
                    'description': assess_data['description'],
                    'assessment_type': assess_data['assessment_type'],
                    'level': assess_data['level'],
                    'passing_score': 70,
                    'time_limit_minutes': 15,
                    'questions_count': assess_data['questions_count'],
                    'randomize_questions': True,
                    'show_correct_answers': True,
                    'allow_retake': True,
                    'retake_cooldown_hours': 1,
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(assessments_data)} assessments'))
