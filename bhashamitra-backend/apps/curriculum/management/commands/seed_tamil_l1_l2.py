"""
Seed command for complete Tamil L1-L2 curriculum.
Following the same structure as Hindi/Punjabi curriculum.
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
    help = 'Seed complete Tamil L1-L2 curriculum (Tamil script)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing Tamil data before seeding',
        )

    def handle(self, *args, **options):
        self.stdout.write('Seeding Tamil L1-L2 curriculum...\n')

        if options['clear']:
            self.clear_existing_data()

        with transaction.atomic():
            # 1. Create Tamil Script and Letters
            script = self.seed_script()
            self.seed_vowels(script)
            self.seed_consonants(script)
            self.seed_grantha_letters(script)
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
            '\nTamil L1-L2 Curriculum Seeded Successfully!' +
            '\n' + '=' * 60 +
            '\n  Script: Tamil (தமிழ்)' +
            '\n  Vowels: 12' +
            '\n  Consonants: 18' +
            '\n  Grantha Letters: 6' +
            '\n  Matras: 12' +
            '\n  Vocabulary Words: 70' +
            '\n  Stories: 10' +
            '\n  Songs: 5' +
            '\n  Games: 5' +
            '\n  Assessments: 2' +
            '\n' + '=' * 60
        ))

    def clear_existing_data(self):
        """Clear existing Tamil data."""
        self.stdout.write('Clearing existing Tamil data...')

        # Clear scripts and related
        Script.objects.filter(language='TAMIL').delete()

        # Clear vocabulary
        VocabularyTheme.objects.filter(language='TAMIL').delete()

        # Clear games
        Game.objects.filter(language='TAMIL').delete()

        # Clear assessments
        Assessment.objects.filter(language='TAMIL').delete()

        # Clear Peppi phrases (Tamil context)
        PeppiPhrase.objects.filter(context__icontains='tamil').delete()

        self.stdout.write(self.style.SUCCESS('Cleared existing Tamil data.'))

    def seed_script(self):
        """Create Tamil script."""
        self.stdout.write('Creating Tamil script...')

        script, created = Script.objects.update_or_create(
            language='TAMIL',
            defaults={
                'name': 'Tamil Script',
                'name_native': 'தமிழ் எழுத்து',
                'description': 'Tamil script is one of the oldest living scripts, used for over 2000 years. It features 12 vowels, 18 consonants, and 216 compound letters.',
                'total_letters': 247,  # 12 vowels + 18 consonants + 216 compounds + 1 aytham
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'  Created script: {script.name}'))
        else:
            self.stdout.write(f'  Updated script: {script.name}')

        return script

    def seed_vowels(self, script):
        """Create vowel letters (உயிர் எழுத்துகள்)."""
        self.stdout.write('Creating vowels (உயிர் எழுத்துகள்)...')

        category, _ = AlphabetCategory.objects.update_or_create(
            script=script,
            category_type='VOWEL',
            defaults={
                'name': 'Vowels',
                'name_native': 'உயிர் எழுத்துகள்',
                'description': 'Life letters - 12 vowel sounds in Tamil script',
                'order': 1,
            }
        )

        vowels = [
            {'character': 'அ', 'romanization': 'a', 'ipa': '/ʌ/', 'type': 'SHORT', 'example_word': 'அம்மா', 'example_translation': 'mother', 'example_image': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=120&h=120&fit=crop', 'mnemonic': 'அ என்றால் அம்மா', 'peppi_song': 'அ அம்மா அன்பு தருவாள்!'},
            {'character': 'ஆ', 'romanization': 'aa', 'ipa': '/aː/', 'type': 'LONG', 'example_word': 'ஆடு', 'example_translation': 'goat', 'example_image': 'https://images.unsplash.com/photo-1524024973431-2ad916746881?w=120&h=120&fit=crop', 'mnemonic': 'ஆ ஆடு மேயும்', 'peppi_song': 'ஆ ஆடு மேயும் வயலில்!'},
            {'character': 'இ', 'romanization': 'i', 'ipa': '/ɪ/', 'type': 'SHORT', 'example_word': 'இலை', 'example_translation': 'leaf', 'example_image': 'https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?w=120&h=120&fit=crop', 'mnemonic': 'இ இலை பச்சை', 'peppi_song': 'இ இலை மரத்தில் இருக்கும்!'},
            {'character': 'ஈ', 'romanization': 'ee', 'ipa': '/iː/', 'type': 'LONG', 'example_word': 'ஈ', 'example_translation': 'fly', 'example_image': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=120&h=120&fit=crop', 'mnemonic': 'ஈ ஈ பறக்கும்', 'peppi_song': 'ஈ ஈ சிறகு விரிக்கும்!'},
            {'character': 'உ', 'romanization': 'u', 'ipa': '/ʊ/', 'type': 'SHORT', 'example_word': 'உடல்', 'example_translation': 'body', 'example_image': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=120&h=120&fit=crop', 'mnemonic': 'உ உடல் ஆரோக்கியம்', 'peppi_song': 'உ உடல் நல்லது வைத்திரு!'},
            {'character': 'ஊ', 'romanization': 'oo', 'ipa': '/uː/', 'type': 'LONG', 'example_word': 'ஊர்', 'example_translation': 'village', 'example_image': 'https://images.unsplash.com/photo-1516483638261-f4d223d13ce3?w=120&h=120&fit=crop', 'mnemonic': 'ஊ ஊர் சிறியது', 'peppi_song': 'ஊ ஊர் என் வீடு!'},
            {'character': 'எ', 'romanization': 'e', 'ipa': '/e/', 'type': 'SHORT', 'example_word': 'எலி', 'example_translation': 'rat', 'example_image': 'https://images.unsplash.com/photo-1425082661705-1834bfd09dca?w=120&h=120&fit=crop', 'mnemonic': 'எ எலி சிறியது', 'peppi_song': 'எ எலி ஓடும் வேகமாக!'},
            {'character': 'ஏ', 'romanization': 'ae', 'ipa': '/eː/', 'type': 'LONG', 'example_word': 'ஏர்', 'example_translation': 'plough', 'example_image': 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=120&h=120&fit=crop', 'mnemonic': 'ஏ ஏர் உழவு', 'peppi_song': 'ஏ ஏர் நிலம் உழும்!'},
            {'character': 'ஐ', 'romanization': 'ai', 'ipa': '/ʌɪ/', 'type': 'DIPHTHONG', 'example_word': 'ஐந்து', 'example_translation': 'five', 'example_image': 'https://images.unsplash.com/photo-1509228627152-72ae9ae6848d?w=120&h=120&fit=crop', 'mnemonic': 'ஐ ஐந்து விரல்', 'peppi_song': 'ஐ ஐந்து எண்ணு சரியாக!'},
            {'character': 'ஒ', 'romanization': 'o', 'ipa': '/o/', 'type': 'SHORT', 'example_word': 'ஒட்டகம்', 'example_translation': 'camel', 'example_image': 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=120&h=120&fit=crop', 'mnemonic': 'ஒ ஒட்டகம் பாலைவனம்', 'peppi_song': 'ஒ ஒட்டகம் மணலில் நடக்கும்!'},
            {'character': 'ஓ', 'romanization': 'oa', 'ipa': '/oː/', 'type': 'LONG', 'example_word': 'ஓடு', 'example_translation': 'tile', 'example_image': 'https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?w=120&h=120&fit=crop', 'mnemonic': 'ஓ ஓடு கூரை', 'peppi_song': 'ஓ ஓடு வீட்டில் இருக்கும்!'},
            {'character': 'ஔ', 'romanization': 'au', 'ipa': '/ʌʊ/', 'type': 'DIPHTHONG', 'example_word': 'ஔவை', 'example_translation': 'poet', 'example_image': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=120&h=120&fit=crop', 'mnemonic': 'ஔ ஔவையார் புலவர்', 'peppi_song': 'ஔ ஔவையார் கவிதை எழுதினார்!'},
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
                    'example_image': vowel['example_image'],
                    'order': i,
                    'is_active': True,
                }
            )

        # Add special character: ஃ (Aytham)
        special_cat, _ = AlphabetCategory.objects.update_or_create(
            script=script,
            category_type='SPECIAL',
            defaults={
                'name': 'Special Characters',
                'name_native': 'சிறப்பு எழுத்துகள்',
                'description': 'Special characters unique to Tamil',
                'order': 5,
            }
        )

        Letter.objects.update_or_create(
            category=special_cat,
            character='ஃ',
            defaults={
                'romanization': 'akh',
                'ipa': '/x/ or /h/',
                'pronunciation_guide': 'ஆய்தம் - Used in borrowed words and emphasis',
                'example_word': 'அஃது',
                'example_word_romanization': 'akhthu',
                'example_word_translation': 'that',
                'order': 1,
                'is_active': True,
            }
        )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(vowels)} vowels + 1 special character'))

    def seed_consonants(self, script):
        """Create consonant letters (மெய் எழுத்துகள்)."""
        self.stdout.write('Creating consonants (மெய் எழுத்துகள்)...')

        category, _ = AlphabetCategory.objects.update_or_create(
            script=script,
            category_type='CONSONANT',
            defaults={
                'name': 'Consonants',
                'name_native': 'மெய் எழுத்துகள்',
                'description': 'Body letters - 18 consonant sounds organized by articulation (Vallinam, Mellinam, Idaiyinam)',
                'order': 2,
            }
        )

        consonants = [
            # வல்லினம் (Vallinam) - Hard consonants
            {'character': 'க', 'romanization': 'ka', 'ipa': '/k~g/', 'group': 'VALLINAM', 'example_word': 'கல்', 'example_translation': 'stone', 'example_image': 'https://images.unsplash.com/photo-1519340241574-2cec6aef0c01?w=120&h=120&fit=crop', 'mnemonic': 'க கல் கனம்'},
            {'character': 'ச', 'romanization': 'cha', 'ipa': '/tʃ~s/', 'group': 'VALLINAM', 'example_word': 'சோறு', 'example_translation': 'rice', 'example_image': 'https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6?w=120&h=120&fit=crop', 'mnemonic': 'ச சோறு சாப்பிடு'},
            {'character': 'ட', 'romanization': 'ta', 'ipa': '/ʈ~ɖ/', 'group': 'VALLINAM', 'example_word': 'டம்', 'example_translation': 'drum', 'example_image': 'https://images.unsplash.com/photo-1519892300165-cb5542fb47c7?w=120&h=120&fit=crop', 'mnemonic': 'ட டம் ஒலிக்கும்'},
            {'character': 'த', 'romanization': 'tha', 'ipa': '/t̪~d̪/', 'group': 'VALLINAM', 'example_word': 'தண்ணீர்', 'example_translation': 'water', 'example_image': 'https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=120&h=120&fit=crop', 'mnemonic': 'த தண்ணீர் குடிக்க'},
            {'character': 'ப', 'romanization': 'pa', 'ipa': '/p~b/', 'group': 'VALLINAM', 'example_word': 'பல்', 'example_translation': 'tooth', 'example_image': 'https://images.unsplash.com/photo-1606811841689-23dfddce3e95?w=120&h=120&fit=crop', 'mnemonic': 'ப பல் வெள்ளை'},
            {'character': 'ற', 'romanization': 'ra', 'ipa': '/r/', 'group': 'VALLINAM', 'example_word': 'பறவை', 'example_translation': 'bird', 'example_image': 'https://images.unsplash.com/photo-1444464666168-49d633b86797?w=120&h=120&fit=crop', 'mnemonic': 'ற பறவை பறக்கும்'},

            # மெல்லினம் (Mellinam) - Soft/Nasal consonants
            {'character': 'ங', 'romanization': 'nga', 'ipa': '/ŋ/', 'group': 'MELLINAM', 'example_word': 'மாங்காய்', 'example_translation': 'mango', 'example_image': 'https://images.unsplash.com/photo-1553279768-865429fa0078?w=120&h=120&fit=crop', 'mnemonic': 'ங மாங்காய் இனிப்பு'},
            {'character': 'ஞ', 'romanization': 'nya', 'ipa': '/ɲ/', 'group': 'MELLINAM', 'example_word': 'ஞானம்', 'example_translation': 'wisdom', 'example_image': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=120&h=120&fit=crop', 'mnemonic': 'ஞ ஞானம் அறிவு'},
            {'character': 'ண', 'romanization': 'na', 'ipa': '/ɳ/', 'group': 'MELLINAM', 'example_word': 'பண்', 'example_translation': 'tune', 'example_image': 'https://images.unsplash.com/photo-1507838153414-b4b713384a76?w=120&h=120&fit=crop', 'mnemonic': 'ண பண் இசை'},
            {'character': 'ந', 'romanization': 'na', 'ipa': '/n̪/', 'group': 'MELLINAM', 'example_word': 'நண்டு', 'example_translation': 'crab', 'example_image': 'https://images.unsplash.com/photo-1550747545-c896b5f89ff7?w=120&h=120&fit=crop', 'mnemonic': 'ந நண்டு நடக்கும்'},
            {'character': 'ம', 'romanization': 'ma', 'ipa': '/m/', 'group': 'MELLINAM', 'example_word': 'மலை', 'example_translation': 'mountain', 'example_image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=120&h=120&fit=crop', 'mnemonic': 'ம மலை உயரம்'},
            {'character': 'ன', 'romanization': 'na', 'ipa': '/n/', 'group': 'MELLINAM', 'example_word': 'பனி', 'example_translation': 'dew', 'example_image': 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=120&h=120&fit=crop', 'mnemonic': 'ன பனி குளிர்'},

            # இடையினம் (Idaiyinam) - Medium consonants
            {'character': 'ய', 'romanization': 'ya', 'ipa': '/j/', 'group': 'IDAIYINAM', 'example_word': 'யானை', 'example_translation': 'elephant', 'example_image': 'https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=120&h=120&fit=crop', 'mnemonic': 'ய யானை பெரியது'},
            {'character': 'ர', 'romanization': 'ra', 'ipa': '/ɾ/', 'group': 'IDAIYINAM', 'example_word': 'ரோஜா', 'example_translation': 'rose', 'example_image': 'https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=120&h=120&fit=crop', 'mnemonic': 'ர ரோஜா மலர்'},
            {'character': 'ல', 'romanization': 'la', 'ipa': '/l/', 'group': 'IDAIYINAM', 'example_word': 'லட்டு', 'example_translation': 'laddu sweet', 'example_image': 'https://images.unsplash.com/photo-1666190094553-d8cfcfb80124?w=120&h=120&fit=crop', 'mnemonic': 'ல லட்டு இனிப்பு'},
            {'character': 'வ', 'romanization': 'va', 'ipa': '/ʋ/', 'group': 'IDAIYINAM', 'example_word': 'வாழை', 'example_translation': 'banana', 'example_image': 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=120&h=120&fit=crop', 'mnemonic': 'வ வாழை மஞ்சள்'},
            {'character': 'ழ', 'romanization': 'zha', 'ipa': '/ɻ/', 'group': 'IDAIYINAM', 'example_word': 'தமிழ்', 'example_translation': 'tamil', 'example_image': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=120&h=120&fit=crop', 'mnemonic': 'ழ தமிழ் அழகு'},
            {'character': 'ள', 'romanization': 'la', 'ipa': '/ɭ/', 'group': 'IDAIYINAM', 'example_word': 'வள்', 'example_translation': 'bangle', 'example_image': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=120&h=120&fit=crop', 'mnemonic': 'ள வள் அணிவு'},
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
                    'example_image': cons['example_image'],
                    'order': i,
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(consonants)} consonants'))

    def seed_grantha_letters(self, script):
        """Create Grantha letters (கிரந்த எழுத்துகள்) - borrowed from Sanskrit."""
        self.stdout.write('Creating Grantha letters (கிரந்த எழுத்துகள்)...')

        category, _ = AlphabetCategory.objects.update_or_create(
            script=script,
            category_type='GRANTHA',
            defaults={
                'name': 'Grantha Letters',
                'name_native': 'கிரந்த எழுத்துகள்',
                'description': 'Letters borrowed from Sanskrit for writing loanwords',
                'order': 3,
            }
        )

        grantha_letters = [
            {'character': 'ஜ', 'romanization': 'ja', 'ipa': '/dʒ/', 'example_word': 'ஜலம்', 'example_translation': 'water'},
            {'character': 'ஷ', 'romanization': 'sha', 'ipa': '/ʂ/', 'example_word': 'விஷம்', 'example_translation': 'poison'},
            {'character': 'ஸ', 'romanization': 'sa', 'ipa': '/s/', 'example_word': 'ஸரஸ்வதி', 'example_translation': 'Saraswati'},
            {'character': 'ஹ', 'romanization': 'ha', 'ipa': '/h/', 'example_word': 'ஹரி', 'example_translation': 'Hari'},
            {'character': 'க்ஷ', 'romanization': 'ksha', 'ipa': '/kʂ/', 'example_word': 'அக்ஷரம்', 'example_translation': 'letter'},
            {'character': 'ஶ்ரீ', 'romanization': 'shri', 'ipa': '/ʃriː/', 'example_word': 'ஶ்ரீ ராம்', 'example_translation': 'Shri Ram'},
        ]

        for i, letter in enumerate(grantha_letters, 1):
            Letter.objects.update_or_create(
                category=category,
                character=letter['character'],
                defaults={
                    'romanization': letter['romanization'],
                    'ipa': letter['ipa'],
                    'pronunciation_guide': f"Sanskrit borrowed letter for {letter['example_translation']}",
                    'example_word': letter['example_word'],
                    'example_word_romanization': letter['romanization'],
                    'example_word_translation': letter['example_translation'],
                    'order': i,
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(grantha_letters)} Grantha letters'))

    def seed_matras(self, script):
        """Create vowel signs (உயிர்மெய் குறியீடுகள்) - matras."""
        self.stdout.write('Creating matras (உயிர்மெய் குறியீடுகள்)...')

        matras = [
            {'symbol': 'ா', 'name': 'கானா', 'sound': 'aa', 'position': 'Right', 'example_with_ka': 'கா'},
            {'symbol': 'ி', 'name': 'கொம்பு', 'sound': 'i', 'position': 'Top-left', 'example_with_ka': 'கி'},
            {'symbol': 'ீ', 'name': 'கொம்பு+சுழி', 'sound': 'ee', 'position': 'Top-left+right', 'example_with_ka': 'கீ'},
            {'symbol': 'ு', 'name': 'சுழி', 'sound': 'u', 'position': 'Bottom', 'example_with_ka': 'கு'},
            {'symbol': 'ூ', 'name': 'குழி', 'sound': 'oo', 'position': 'Bottom', 'example_with_ka': 'கூ'},
            {'symbol': 'ெ', 'name': 'கொம்பு', 'sound': 'e', 'position': 'Left', 'example_with_ka': 'கெ'},
            {'symbol': 'ே', 'name': 'கொம்பு', 'sound': 'ae', 'position': 'Left+top', 'example_with_ka': 'கே'},
            {'symbol': 'ை', 'name': 'இரு கொம்பு', 'sound': 'ai', 'position': 'Left', 'example_with_ka': 'கை'},
            {'symbol': 'ொ', 'name': 'கொம்பு+ா', 'sound': 'o', 'position': 'Left+right', 'example_with_ka': 'கொ'},
            {'symbol': 'ோ', 'name': 'கொம்பு+ா', 'sound': 'oa', 'position': 'Left+top+right', 'example_with_ka': 'கோ'},
            {'symbol': 'ௌ', 'name': 'கொம்பு+ள', 'sound': 'au', 'position': 'Left+right', 'example_with_ka': 'கௌ'},
            {'symbol': '்', 'name': 'புள்ளி', 'sound': 'none (vowel killer)', 'position': 'Top', 'example_with_ka': 'க்'},
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
                'name_native': 'குடும்பம்',
                'icon': 'family',
                'level': 1,
                'words': [
                    {'word': 'அம்மா', 'romanization': 'Ammaa', 'translation': 'Mother', 'pos': 'NOUN'},
                    {'word': 'அப்பா', 'romanization': 'Appaa', 'translation': 'Father', 'pos': 'NOUN'},
                    {'word': 'பாட்டி', 'romanization': 'Paatti', 'translation': 'Grandmother', 'pos': 'NOUN'},
                    {'word': 'தாத்தா', 'romanization': 'Thaathaa', 'translation': 'Grandfather', 'pos': 'NOUN'},
                    {'word': 'அக்கா', 'romanization': 'Akkaa', 'translation': 'Elder sister', 'pos': 'NOUN'},
                    {'word': 'அண்ணா', 'romanization': 'Annaa', 'translation': 'Elder brother', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Colors',
                'name_native': 'நிறங்கள்',
                'icon': 'palette',
                'level': 1,
                'words': [
                    {'word': 'சிவப்பு', 'romanization': 'Sivappu', 'translation': 'Red', 'pos': 'ADJECTIVE'},
                    {'word': 'நீலம்', 'romanization': 'Neelam', 'translation': 'Blue', 'pos': 'ADJECTIVE'},
                    {'word': 'மஞ்சள்', 'romanization': 'Manjal', 'translation': 'Yellow', 'pos': 'ADJECTIVE'},
                    {'word': 'பச்சை', 'romanization': 'Pachchai', 'translation': 'Green', 'pos': 'ADJECTIVE'},
                ]
            },
            {
                'name': 'Numbers',
                'name_native': 'எண்கள்',
                'icon': 'numbers',
                'level': 1,
                'words': [
                    {'word': 'ஒன்று', 'romanization': 'Ondru', 'translation': 'One', 'pos': 'NUMBER'},
                    {'word': 'இரண்டு', 'romanization': 'Irandu', 'translation': 'Two', 'pos': 'NUMBER'},
                    {'word': 'மூன்று', 'romanization': 'Moondru', 'translation': 'Three', 'pos': 'NUMBER'},
                    {'word': 'நான்கு', 'romanization': 'Naangu', 'translation': 'Four', 'pos': 'NUMBER'},
                    {'word': 'ஐந்து', 'romanization': 'Ainthu', 'translation': 'Five', 'pos': 'NUMBER'},
                ]
            },
            {
                'name': 'Animals',
                'name_native': 'விலங்குகள்',
                'icon': 'pets',
                'level': 1,
                'words': [
                    {'word': 'நாய்', 'romanization': 'Naai', 'translation': 'Dog', 'pos': 'NOUN'},
                    {'word': 'பூனை', 'romanization': 'Poonai', 'translation': 'Cat', 'pos': 'NOUN'},
                    {'word': 'பசு', 'romanization': 'Pasu', 'translation': 'Cow', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Basics',
                'name_native': 'அடிப்படை',
                'icon': 'star',
                'level': 1,
                'words': [
                    {'word': 'தண்ணீர்', 'romanization': 'Thanneer', 'translation': 'Water', 'pos': 'NOUN'},
                    {'word': 'சாதம்', 'romanization': 'Saadham', 'translation': 'Rice', 'pos': 'NOUN'},
                ]
            },
        ]

        # L2 Vocabulary (50 words)
        l2_themes = [
            {
                'name': 'Extended Family',
                'name_native': 'பெரிய குடும்பம்',
                'icon': 'groups',
                'level': 2,
                'words': [
                    {'word': 'பெரியம்மா', 'romanization': 'Periyammaa', 'translation': 'Aunt (mother\'s elder sister)', 'pos': 'NOUN'},
                    {'word': 'பெரியப்பா', 'romanization': 'Periyappaa', 'translation': 'Uncle (father\'s elder brother)', 'pos': 'NOUN'},
                    {'word': 'சித்தி', 'romanization': 'Chitthi', 'translation': 'Aunt (mother\'s younger sister)', 'pos': 'NOUN'},
                    {'word': 'சித்தப்பா', 'romanization': 'Chithappaa', 'translation': 'Uncle (father\'s younger brother)', 'pos': 'NOUN'},
                    {'word': 'மாமா', 'romanization': 'Maamaa', 'translation': 'Uncle (maternal)', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'More Colors',
                'name_native': 'மேலும் நிறங்கள்',
                'icon': 'color_lens',
                'level': 2,
                'words': [
                    {'word': 'கருப்பு', 'romanization': 'Karuppu', 'translation': 'Black', 'pos': 'ADJECTIVE'},
                    {'word': 'வெள்ளை', 'romanization': 'Vellai', 'translation': 'White', 'pos': 'ADJECTIVE'},
                    {'word': 'ஆரஞ்சு', 'romanization': 'Aaranchu', 'translation': 'Orange', 'pos': 'ADJECTIVE'},
                ]
            },
            {
                'name': 'Numbers 6-10',
                'name_native': 'எண்கள் ௬-௧௦',
                'icon': 'pin',
                'level': 2,
                'words': [
                    {'word': 'ஆறு', 'romanization': 'Aaru', 'translation': 'Six', 'pos': 'NUMBER'},
                    {'word': 'ஏழு', 'romanization': 'Ezhu', 'translation': 'Seven', 'pos': 'NUMBER'},
                    {'word': 'எட்டு', 'romanization': 'Ettu', 'translation': 'Eight', 'pos': 'NUMBER'},
                    {'word': 'ஒன்பது', 'romanization': 'Onbathu', 'translation': 'Nine', 'pos': 'NUMBER'},
                    {'word': 'பத்து', 'romanization': 'Patthu', 'translation': 'Ten', 'pos': 'NUMBER'},
                ]
            },
            {
                'name': 'More Animals',
                'name_native': 'மேலும் விலங்குகள்',
                'icon': 'cruelty_free',
                'level': 2,
                'words': [
                    {'word': 'யானை', 'romanization': 'Yaanai', 'translation': 'Elephant', 'pos': 'NOUN'},
                    {'word': 'சிங்கம்', 'romanization': 'Singam', 'translation': 'Lion', 'pos': 'NOUN'},
                    {'word': 'புலி', 'romanization': 'Puli', 'translation': 'Tiger', 'pos': 'NOUN'},
                    {'word': 'குரங்கு', 'romanization': 'Kurangu', 'translation': 'Monkey', 'pos': 'NOUN'},
                    {'word': 'கிளி', 'romanization': 'Kili', 'translation': 'Parrot', 'pos': 'NOUN'},
                    {'word': 'மீன்', 'romanization': 'Meen', 'translation': 'Fish', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Fruits',
                'name_native': 'பழங்கள்',
                'icon': 'nutrition',
                'level': 2,
                'words': [
                    {'word': 'ஆப்பிள்', 'romanization': 'Aappil', 'translation': 'Apple', 'pos': 'NOUN'},
                    {'word': 'வாழைப்பழம்', 'romanization': 'Vaazhaipazham', 'translation': 'Banana', 'pos': 'NOUN'},
                    {'word': 'மாம்பழம்', 'romanization': 'Maambazham', 'translation': 'Mango', 'pos': 'NOUN'},
                    {'word': 'திராட்சை', 'romanization': 'Thiraatchai', 'translation': 'Grapes', 'pos': 'NOUN'},
                    {'word': 'ஆரஞ்சு பழம்', 'romanization': 'Aaranchu pazham', 'translation': 'Orange fruit', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Food & Drinks',
                'name_native': 'உணவு',
                'icon': 'local_cafe',
                'level': 2,
                'words': [
                    {'word': 'பால்', 'romanization': 'Paal', 'translation': 'Milk', 'pos': 'NOUN'},
                    {'word': 'இட்லி', 'romanization': 'Idli', 'translation': 'Idli', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Body Parts',
                'name_native': 'உடல் பாகங்கள்',
                'icon': 'accessibility',
                'level': 2,
                'words': [
                    {'word': 'தலை', 'romanization': 'Thalai', 'translation': 'Head', 'pos': 'NOUN'},
                    {'word': 'கண்', 'romanization': 'Kan', 'translation': 'Eye', 'pos': 'NOUN'},
                    {'word': 'மூக்கு', 'romanization': 'Mookku', 'translation': 'Nose', 'pos': 'NOUN'},
                    {'word': 'காது', 'romanization': 'Kaadhu', 'translation': 'Ear', 'pos': 'NOUN'},
                    {'word': 'வாய்', 'romanization': 'Vaai', 'translation': 'Mouth', 'pos': 'NOUN'},
                    {'word': 'கை', 'romanization': 'Kai', 'translation': 'Hand', 'pos': 'NOUN'},
                    {'word': 'கால்', 'romanization': 'Kaal', 'translation': 'Leg/Foot', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Actions',
                'name_native': 'செயல்கள்',
                'icon': 'directions_run',
                'level': 2,
                'words': [
                    {'word': 'சாப்பிடு', 'romanization': 'Saappidu', 'translation': 'To eat', 'pos': 'VERB'},
                    {'word': 'குடி', 'romanization': 'Kudi', 'translation': 'To drink', 'pos': 'VERB'},
                    {'word': 'தூங்கு', 'romanization': 'Thoongu', 'translation': 'To sleep', 'pos': 'VERB'},
                    {'word': 'விளையாடு', 'romanization': 'Vilaiyaadu', 'translation': 'To play', 'pos': 'VERB'},
                    {'word': 'படி', 'romanization': 'Padi', 'translation': 'To read/study', 'pos': 'VERB'},
                    {'word': 'எழுது', 'romanization': 'Ezhudhu', 'translation': 'To write', 'pos': 'VERB'},
                ]
            },
            {
                'name': 'Home',
                'name_native': 'வீடு',
                'icon': 'home',
                'level': 2,
                'words': [
                    {'word': 'வீடு', 'romanization': 'Veedu', 'translation': 'Home', 'pos': 'NOUN'},
                    {'word': 'அறை', 'romanization': 'Arai', 'translation': 'Room', 'pos': 'NOUN'},
                    {'word': 'கதவு', 'romanization': 'Kadhavu', 'translation': 'Door', 'pos': 'NOUN'},
                    {'word': 'ஜன்னல்', 'romanization': 'Jannal', 'translation': 'Window', 'pos': 'NOUN'},
                    {'word': 'மேசை', 'romanization': 'Mesai', 'translation': 'Table', 'pos': 'NOUN'},
                    {'word': 'நாற்காலி', 'romanization': 'Naarkaali', 'translation': 'Chair', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Nature',
                'name_native': 'இயற்கை',
                'icon': 'park',
                'level': 2,
                'words': [
                    {'word': 'சூரியன்', 'romanization': 'Sooriyan', 'translation': 'Sun', 'pos': 'NOUN'},
                    {'word': 'நிலா', 'romanization': 'Nilaa', 'translation': 'Moon', 'pos': 'NOUN'},
                    {'word': 'நட்சத்திரம்', 'romanization': 'Natchathiram', 'translation': 'Star', 'pos': 'NOUN'},
                    {'word': 'பூ', 'romanization': 'Poo', 'translation': 'Flower', 'pos': 'NOUN'},
                    {'word': 'மரம்', 'romanization': 'Maram', 'translation': 'Tree', 'pos': 'NOUN'},
                ]
            },
        ]

        all_themes = l1_themes + l2_themes
        word_count = 0

        for i, theme_data in enumerate(all_themes, 1):
            theme, _ = VocabularyTheme.objects.update_or_create(
                language='TAMIL',
                name=theme_data['name'],
                defaults={
                    'name_native': theme_data['name_native'],
                    'description': f"Learn {theme_data['name']} in Tamil",
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
        """Create Tamil stories for L1 and L2."""
        self.stdout.write('Creating Tamil stories...')

        stories_data = [
            # L1 Stories (3)
            {
                'title': "Peppi's New Friend",
                'title_hindi': 'பெப்பியின் புதிய நண்பன்',
                'title_romanized': "Peppiyin Pudhiya Nanban",
                'level': 1,
                'age_min': 4,
                'age_max': 6,
                'theme': 'friendship',
                'tier': 'FREE',
                'moral_english': 'True friends accept each other as they are',
                'moral_hindi': 'உண்மையான நண்பர்கள் ஒருவரை ஒருவர் ஏற்றுக்கொள்வார்கள்',
                'pages': [
                    {'text': 'பெப்பி ஒரு பூனை.', 'translation': 'Peppi is a cat.'},
                    {'text': 'பெப்பிக்கு நண்பன் வேண்டும்.', 'translation': 'Peppi wants a friend.'},
                    {'text': 'பெப்பி ஒரு நாயைப் பார்த்தது.', 'translation': 'Peppi saw a dog.'},
                    {'text': 'நாயின் பெயர் ராஜா.', 'translation': "The dog's name is Raja."},
                    {'text': 'பெப்பியும் ராஜாவும் நண்பர்கள் ஆனார்கள்!', 'translation': 'Peppi and Raja became friends!'},
                ]
            },
            {
                'title': 'The Red Apple',
                'title_hindi': 'சிவப்பு ஆப்பிள்',
                'title_romanized': 'Sivappu Aappil',
                'level': 1,
                'age_min': 4,
                'age_max': 6,
                'theme': 'sharing',
                'tier': 'FREE',
                'moral_english': 'Sharing brings happiness',
                'moral_hindi': 'பகிர்வு மகிழ்ச்சி தரும்',
                'pages': [
                    {'text': 'மரத்தில் ஒரு ஆப்பிள் இருக்கிறது.', 'translation': 'There is an apple on the tree.'},
                    {'text': 'ஆப்பிள் சிவப்பு நிறம்.', 'translation': 'The apple is red.'},
                    {'text': 'குழந்தை ஆப்பிள் வேண்டும்.', 'translation': 'The child wants the apple.'},
                    {'text': 'அம்மா ஆப்பிள் கொடுத்தார்.', 'translation': 'Mother gave the apple.'},
                    {'text': 'குழந்தை மகிழ்ச்சி!', 'translation': 'The child is happy!'},
                ]
            },
            {
                'title': 'My Family',
                'title_hindi': 'என் குடும்பம்',
                'title_romanized': 'En Kudumbam',
                'level': 1,
                'age_min': 4,
                'age_max': 6,
                'theme': 'family',
                'tier': 'FREE',
                'moral_english': 'Family is our biggest treasure',
                'moral_hindi': 'குடும்பம் நம் பெரிய செல்வம்',
                'pages': [
                    {'text': 'இது என் அம்மா.', 'translation': 'This is my mother.'},
                    {'text': 'இது என் அப்பா.', 'translation': 'This is my father.'},
                    {'text': 'இது என் அக்கா.', 'translation': 'This is my elder sister.'},
                    {'text': 'இது என் அண்ணா.', 'translation': 'This is my elder brother.'},
                    {'text': 'நாங்கள் எல்லோரும் ஒன்றாக வாழ்கிறோம்.', 'translation': 'We all live together.'},
                ]
            },
            # L2 Stories (7)
            {
                'title': 'Pongal Festival',
                'title_hindi': 'பொங்கல் திருநாள்',
                'title_romanized': 'Pongal Thirunaal',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'festival',
                'tier': 'STANDARD',
                'moral_english': 'Festivals bring joy and unity',
                'moral_hindi': 'திருவிழாக்கள் மகிழ்ச்சியும் ஒற்றுமையும் தரும்',
                'pages': [
                    {'text': 'இன்று பொங்கல் திருநாள்!', 'translation': 'Today is Pongal festival!'},
                    {'text': 'எல்லோரும் மகிழ்ச்சியாக இருக்கிறார்கள்.', 'translation': 'Everyone is happy.'},
                    {'text': 'அம்மா பொங்கல் வைக்கிறார்.', 'translation': 'Mother is making Pongal.'},
                    {'text': 'பொங்கலோ பொங்கல்!', 'translation': 'Pongal has overflowed!'},
                    {'text': 'குழந்தைகள் கோலம் போடுகிறார்கள்.', 'translation': 'Children draw kolam.'},
                    {'text': 'பொங்கல் வாழ்த்துக்கள்!', 'translation': 'Happy Pongal!'},
                ]
            },
            {
                'title': 'The Clever Crow',
                'title_hindi': 'புத்திசாலி காகம்',
                'title_romanized': 'Buddhisaali Kaagam',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'wisdom',
                'tier': 'STANDARD',
                'moral_english': 'Where there is a will, there is a way',
                'moral_hindi': 'முயற்சி திருவினை ஆக்கும்',
                'pages': [
                    {'text': 'ஒரு காகம் இருந்தது.', 'translation': 'There was a crow.'},
                    {'text': 'அதற்கு தாகம் எடுத்தது.', 'translation': 'It was thirsty.'},
                    {'text': 'ஒரு குடத்தைப் பார்த்தது.', 'translation': 'It saw a pot.'},
                    {'text': 'குடத்தில் கொஞ்சம் தண்ணீர் இருந்தது.', 'translation': 'There was little water in the pot.'},
                    {'text': 'காகம் கற்களைப் போட்டது.', 'translation': 'The crow dropped stones.'},
                    {'text': 'தண்ணீர் மேலே வந்தது!', 'translation': 'The water came up!'},
                    {'text': 'காகம் தண்ணீர் குடித்தது!', 'translation': 'The crow drank the water!'},
                ]
            },
            {
                'title': 'Diwali Festival',
                'title_hindi': 'தீபாவளி',
                'title_romanized': 'Deepavali',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'festival',
                'tier': 'STANDARD',
                'moral_english': 'Light dispels darkness',
                'moral_hindi': 'ஒளி இருளை அகற்றும்',
                'pages': [
                    {'text': 'இன்று தீபாவளி!', 'translation': 'Today is Diwali!'},
                    {'text': 'வீடு விளக்குகளால் அழகாக இருக்கிறது.', 'translation': 'The house is beautiful with lamps.'},
                    {'text': 'குழந்தைகள் புது ஆடை அணிகிறார்கள்.', 'translation': 'Children wear new clothes.'},
                    {'text': 'பட்டாசு வெடிக்கிறார்கள்.', 'translation': 'They burst crackers.'},
                    {'text': 'இனிப்பு சாப்பிடுகிறார்கள்.', 'translation': 'They eat sweets.'},
                    {'text': 'தீபாவளி வாழ்த்துக்கள்!', 'translation': 'Happy Diwali!'},
                ]
            },
            {
                'title': 'Going to School',
                'title_hindi': 'பள்ளிக்குச் செல்வோம்',
                'title_romanized': 'Pallikku Selvom',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'education',
                'tier': 'STANDARD',
                'moral_english': 'Education opens doors to the future',
                'moral_hindi': 'கல்வி எதிர்காலத்தைத் திறக்கும்',
                'pages': [
                    {'text': 'காலை ஆறு மணி.', 'translation': 'It is 6 AM.'},
                    {'text': 'ராணி எழுந்திருக்கிறாள்.', 'translation': 'Rani wakes up.'},
                    {'text': 'முகம் கழுவுகிறாள்.', 'translation': 'She washes her face.'},
                    {'text': 'சாப்பிட்டு விட்டு பள்ளிக்குப் போகிறாள்.', 'translation': 'She eats and goes to school.'},
                    {'text': 'பள்ளியில் படிக்கிறாள்.', 'translation': 'She studies at school.'},
                    {'text': 'நண்பர்களுடன் விளையாடுகிறாள்.', 'translation': 'She plays with friends.'},
                ]
            },
            {
                'title': 'The Elephant and the Mouse',
                'title_hindi': 'யானையும் எலியும்',
                'title_romanized': 'Yaanaiyum Eliyum',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'friendship',
                'tier': 'STANDARD',
                'moral_english': 'Never underestimate anyone',
                'moral_hindi': 'யாரையும் சிறியவர் என்று நினைக்காதே',
                'pages': [
                    {'text': 'ஒரு பெரிய யானை இருந்தது.', 'translation': 'There was a big elephant.'},
                    {'text': 'ஒரு சிறிய எலி இருந்தது.', 'translation': 'There was a small mouse.'},
                    {'text': 'யானை எலியை பார்த்து சிரித்தது.', 'translation': 'The elephant laughed at the mouse.'},
                    {'text': 'ஒரு நாள் யானை வலையில் சிக்கியது.', 'translation': 'One day the elephant got trapped.'},
                    {'text': 'எலி வலையை கடித்தது.', 'translation': 'The mouse bit the net.'},
                    {'text': 'யானை தப்பியது!', 'translation': 'The elephant escaped!'},
                    {'text': 'யானை நன்றி சொன்னது.', 'translation': 'The elephant said thank you.'},
                ]
            },
            {
                'title': 'Onam Festival',
                'title_hindi': 'ஓணம்',
                'title_romanized': 'Onam',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'festival',
                'tier': 'STANDARD',
                'moral_english': 'Good rulers are remembered forever',
                'moral_hindi': 'நல்ல அரசர்கள் நிரந்தரமாக நினைவில் இருப்பார்கள்',
                'pages': [
                    {'text': 'ஓணம் திருநாள்!', 'translation': 'Onam festival!'},
                    {'text': 'மாவேலி மன்னன் வருகிறார்.', 'translation': 'King Mahabali is coming.'},
                    {'text': 'பூக்களால் கோலம் போடுகிறார்கள்.', 'translation': 'They make flower kolam.'},
                    {'text': 'ஓணசாதம் சாப்பிடுகிறார்கள்.', 'translation': 'They eat Onam sadhya.'},
                    {'text': 'படகு பந்தயம் நடக்கிறது.', 'translation': 'Boat race happens.'},
                    {'text': 'ஓணம் வாழ்த்துக்கள்!', 'translation': 'Happy Onam!'},
                ]
            },
            {
                'title': 'Chennai Zoo',
                'title_hindi': 'சென்னை உயிரியல் பூங்கா',
                'title_romanized': 'Chennai Uyiriyal Poonka',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'animals',
                'tier': 'STANDARD',
                'moral_english': 'Love and protect all animals',
                'moral_hindi': 'அனைத்து விலங்குகளையும் நேசிக்கவும் பாதுகாக்கவும்',
                'pages': [
                    {'text': 'இன்று உயிரியல் பூங்காவிற்குச் செல்கிறோம்.', 'translation': 'Today we go to the zoo.'},
                    {'text': 'யானையைப் பார்க்கிறோம்.', 'translation': 'We see the elephant.'},
                    {'text': 'சிங்கத்தைப் பார்க்கிறோம்.', 'translation': 'We see the lion.'},
                    {'text': 'குரங்கு குதிக்கிறது.', 'translation': 'The monkey jumps.'},
                    {'text': 'கிளி பேசுகிறது.', 'translation': 'The parrot talks.'},
                    {'text': 'மிகவும் சந்தோஷம்!', 'translation': 'Very happy!'},
                ]
            },
        ]

        for story_data in stories_data:
            # Create unique storyweaver_id for Tamil stories
            story_slug = story_data['title'].lower().replace(' ', '-').replace("'", '')
            storyweaver_id = f"ta-l{story_data['level']}-{story_slug}"

            story, _ = Story.objects.update_or_create(
                storyweaver_id=storyweaver_id,
                defaults={
                    'language': 'TAMIL',
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
                        'text_hindi': page_data['text'],  # Tamil text in the hindi field
                        'text_romanized': page_data['translation'],
                    }
                )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(stories_data)} stories'))

    def seed_songs(self):
        """Create Tamil songs for L1 and L2."""
        self.stdout.write('Creating Tamil songs...')

        # Get or create L1 level
        l1_level, _ = CurriculumLevel.objects.get_or_create(
            code='L1',
            defaults={
                'name_english': 'Discovery',
                'name_hindi': 'கண்டுபிடிப்பு',
                'name_romanized': 'Kandupidippu',
                'min_age': 4,
                'max_age': 5,
                'description': 'First steps in learning Tamil',
                'order': 1,
                'is_active': True,
            }
        )

        songs_data = [
            {
                'title_english': 'Moon Moon Come Running',
                'title_hindi': 'நிலா நிலா ஓடி வா',
                'title_romanized': 'Nilaa Nilaa Odi Vaa',
                'lyrics_hindi': '''நிலா நிலா ஓடி வா
நில்லாமல் ஓடி வா
மலைமேலே ஏறி வா
மறைந்திட்டு வந்திடு வா

வெள்ளை நிறம் நிலவு
விண்ணில் ஒளிர்கிறது
கண்ணை மூடி தூங்கு
கனவில் விளையாடு!''',
                'lyrics_romanized': '''Nilaa nilaa odi vaa
Nillaamal odi vaa
Malaimele eri vaa
Maraindhittu vandhidu vaa

Vellai niram nilavu
Vinnil olirgiradhu
Kannai moodi thoongu
Kanavil vilaiyaadu!''',
                'lyrics_english': '''Moon moon come running
Come running without stopping
Climb up the mountain
Hide and come back

The moon is white
Shining in the sky
Close your eyes and sleep
Play in your dreams!''',
                'category': 'RHYME',
                'age_min': 4,
                'age_max': 6,
                'duration_seconds': 60,
            },
            {
                'title_english': "Grandma's Girl",
                'title_hindi': 'ஆத்தா மகளே',
                'title_romanized': 'Aathaa Magale',
                'lyrics_hindi': '''ஆத்தா மகளே ஆத்தா மகளே
அழகான பாப்பா நீ
சாப்பாடு சாப்பிடு
சந்தோஷமா இரு

பாட்டி சொல்வார் கதை
பாப்பா கேட்கும் நன்றாக
தூங்கும் நேரம் வந்தது
தூ தூ தூ தூங்கு!''',
                'lyrics_romanized': '''Aathaa magale aathaa magale
Azhagaana paappaa nee
Saappaadu saappidu
Santhoshamaa iru

Paatti solvaar kadhai
Paappaa ketkum nanraaga
Thoongum neram vandhadu
Thoo thoo thoo thoongu!''',
                'lyrics_english': '''Grandma's girl grandma's girl
You are a beautiful baby
Eat your food
Be happy

Grandma tells stories
Baby listens well
It's time to sleep
Sleep sleep sleep!''',
                'category': 'RHYME',
                'age_min': 4,
                'age_max': 6,
                'duration_seconds': 45,
            },
            {
                'title_english': 'Tamil Alphabet Song',
                'title_hindi': 'தமிழ் எழுத்துப் பாடல்',
                'title_romanized': 'Tamil Ezhuthup Paadal',
                'lyrics_hindi': '''அ ஆ இ ஈ உ ஊ
எ ஏ ஐ ஒ ஓ ஔ
உயிர் எழுத்து பன்னிரண்டு
உயிரோடு பாடுவோம்!

க ங ச ஞ ட ண
த ந ப ம ய ர
ல வ ழ ள ற ன
மெய் எழுத்து பதினெட்டு!

தமிழ் மொழி அழகு
தமிழ் படிப்போம் வாருங்கள்!''',
                'lyrics_romanized': '''A aa i ee u oo
E ae ai o oa au
Uyir ezhuthu pannirandu
Uyirodu paaduvoam!

Ka nga sa nya ta na
Tha na pa ma ya ra
La va zha la ra na
Mei ezhuthu pathinettu!

Tamil mozhi azhagu
Tamil padippoam vaarungal!''',
                'lyrics_english': '''A aa i ee u oo
E ae ai o oa au
Twelve life letters
Let us sing with life!

Ka nga sa nya ta na
Tha na pa ma ya ra
La va zha la ra na
Eighteen body letters!

Tamil language is beautiful
Come let us learn Tamil!''',
                'category': 'EDUCATIONAL',
                'age_min': 4,
                'age_max': 7,
                'duration_seconds': 90,
            },
            {
                'title_english': 'The Train',
                'title_hindi': 'ரயில் வண்டி',
                'title_romanized': 'Rail Vandi',
                'lyrics_hindi': '''சுக் சுக் ரயில் வண்டி
சுற்றி சுற்றி ஓடுது
ஊர் ஊராய் செல்லுது
உசாராக நிற்குது

கூ கூ என்று கத்தும்
குதூகலம் கொடுக்கும்
வேகமாக ஓடும்
வீட்டுக்கு கொண்டு சேர்க்கும்!''',
                'lyrics_romanized': '''Suk suk rail vandi
Sutri sutri odudhu
Oor ooraai selludhu
Usaaraaga nirkudhu

Koo koo endru kaththum
Kudhoogalam kodukkum
Vegamaaga odum
Veettukku kondu serkkum!''',
                'lyrics_english': '''Choo choo train
Runs round and round
Goes from town to town
Stops carefully

Says choo choo loudly
Gives excitement
Runs fast
Takes us home!''',
                'category': 'RHYME',
                'age_min': 4,
                'age_max': 6,
                'duration_seconds': 50,
            },
            {
                'title_english': 'Bharatanatyam Dance',
                'title_hindi': 'பரதநாட்டியம்',
                'title_romanized': 'Bharatanatyam',
                'lyrics_hindi': '''தாள தாள தகதிமி
தத்தோம் தரிகிட
கால் தூக்கி ஆடுவோம்
கலைஞராய் மாறுவோம்

கண் அசைவு அழகு
கை முத்திரை கலை
பரதம் ஆடுவோம்
பாரம்பரியம் காப்போம்!''',
                'lyrics_romanized': '''Thaala thaala thagathimi
Thaththom tharikida
Kaal thookki aaduvoam
Kalaignaraai maaruvoam

Kan asaivu azhagu
Kai muththirai kalai
Bharatham aaduvoam
Paarambaryam kaappoam!''',
                'lyrics_english': '''Thaala thaala thagathimi
Thaththom tharikida
Let us dance lifting our feet
Let us become artists

Eye movement is beautiful
Hand gestures are art
Let us dance Bharatam
Let us preserve tradition!''',
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
                    'language': 'TAMIL',
                    'order': i,
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(songs_data)} songs'))

    def seed_curriculum_levels(self):
        """Create L1 and L2 curriculum levels for Tamil."""
        self.stdout.write('Creating curriculum levels...')

        levels_data = [
            {
                'code': 'L1',
                'name_english': 'Discovery',
                'name_hindi': 'கண்டுபிடிப்பு',
                'name_romanized': 'Kandupidippu',
                'min_age': 4,
                'max_age': 5,
                'description': 'First steps in learning Tamil. Children learn basic greetings, vowels, and simple words.',
                'peppi_welcome': 'வணக்கம்! Welcome to Peppi\'s Tamil class!',
                'peppi_completion': 'அருமை! You completed L1! Let\'s move to L2!',
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
                'name_hindi': 'அடிப்படை கற்கள்',
                'name_romanized': 'Adippadai Karkal',
                'min_age': 5,
                'max_age': 6,
                'description': 'Learn consonants, matras, and start reading simple words and sentences.',
                'peppi_welcome': 'வணக்கம்! Ready to learn more Tamil?',
                'peppi_completion': 'சூப்பர்! You are a Tamil superstar!',
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
        """Create Peppi phrases in Tamil."""
        self.stdout.write('Creating Peppi phrases...')

        phrases_data = [
            {'category': 'GREETING', 'text_hindi': 'வணக்கம்!', 'text_english': 'Hello!', 'text_romanized': 'Vanakkam!', 'context': 'tamil_greeting'},
            {'category': 'CORRECT', 'text_hindi': 'அருமை!', 'text_english': 'Wonderful!', 'text_romanized': 'Arumai!', 'context': 'tamil_celebration'},
            {'category': 'CORRECT', 'text_hindi': 'வாவ்! சூப்பர்!', 'text_english': 'Wow! Super!', 'text_romanized': 'Wow! Super!', 'context': 'tamil_wow'},
            {'category': 'CORRECT', 'text_hindi': 'மிக நல்லது!', 'text_english': 'Very good!', 'text_romanized': 'Miga nalladhu!', 'context': 'tamil_verygood'},
            {'category': 'CORRECT', 'text_hindi': 'சபாஷ்!', 'text_english': 'Well done!', 'text_romanized': 'Sabaash!', 'context': 'tamil_welldone'},
            {'category': 'CORRECT', 'text_hindi': 'அட்டகாசம்!', 'text_english': 'Excellent!', 'text_romanized': 'Attakasam!', 'context': 'tamil_excellent'},
            {'category': 'WRONG', 'text_hindi': 'மறுபடியும் முயற்சி செய்!', 'text_english': 'Try again!', 'text_romanized': 'Marupadiyum muyarchi sei!', 'context': 'tamil_tryagain'},
            {'category': 'ENCOURAGEMENT', 'text_hindi': 'உன்னால் முடியும்!', 'text_english': 'You can do it!', 'text_romanized': 'Unnaal mudiyum!', 'context': 'tamil_encourage'},
            {'category': 'FAREWELL', 'text_hindi': 'போய் வருகிறேன்!', 'text_english': 'Goodbye!', 'text_romanized': 'Poi varugiren!', 'context': 'tamil_farewell'},
            {'category': 'GREETING', 'text_hindi': 'நன்றி!', 'text_english': 'Thank you!', 'text_romanized': 'Nandri!', 'context': 'tamil_thankyou'},
            {'category': 'ENCOURAGEMENT', 'text_hindi': 'வா போகலாம்!', 'text_english': "Let's go!", 'text_romanized': 'Vaa pogalaam!', 'context': 'tamil_letsgo'},
            {'category': 'ENCOURAGEMENT', 'text_hindi': 'தொடரு!', 'text_english': 'Keep going!', 'text_romanized': 'Thodaru!', 'context': 'tamil_keepgoing'},
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
        """Create Tamil games."""
        self.stdout.write('Creating Tamil games...')

        games_data = [
            {
                'name': 'Tamil Memory',
                'description': 'Match Tamil letters with their sounds',
                'game_type': 'MEMORY',
                'skill_focus': 'ALPHABET',
                'level': 1,
            },
            {
                'name': 'Tamil Word Search',
                'description': 'Find hidden Tamil words',
                'game_type': 'WORDSEARCH',
                'skill_focus': 'VOCAB',
                'level': 1,
            },
            {
                'name': 'Listen and Match',
                'description': 'Listen to Tamil words and match with pictures',
                'game_type': 'LISTENING',
                'skill_focus': 'LISTENING',
                'level': 1,
            },
            {
                'name': 'Tamil Quiz',
                'description': 'Test your Tamil knowledge',
                'game_type': 'QUIZ',
                'skill_focus': 'MIXED',
                'level': 2,
            },
            {
                'name': 'Word Builder',
                'description': 'Build Tamil words using letters',
                'game_type': 'BUILDER',
                'skill_focus': 'SPELLING',
                'level': 2,
            },
        ]

        for game_data in games_data:
            Game.objects.update_or_create(
                language='TAMIL',
                name=game_data['name'],
                defaults={
                    'description': game_data['description'],
                    'instructions': f"Play {game_data['name']} to practice Tamil!",
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
        """Create Tamil assessments."""
        self.stdout.write('Creating Tamil assessments...')

        assessments_data = [
            {
                'name': 'L1 Entry Assessment',
                'description': 'Check your starting level in Tamil',
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
                language='TAMIL',
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
