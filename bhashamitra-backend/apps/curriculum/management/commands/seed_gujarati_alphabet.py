"""
Seed command for Gujarati alphabet with example images.
Creates Script, AlphabetCategory, and Letter objects for Gujarati.
"""
import logging
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.children.models import Child
from apps.curriculum.models import Script, AlphabetCategory, Letter

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Seed Gujarati alphabet with vowels, consonants, and example images'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing Gujarati alphabet data before seeding',
        )

    def handle(self, *args, **options):
        self.stdout.write('Seeding Gujarati alphabet...\n')

        if options['clear']:
            self.clear_existing_data()

        with transaction.atomic():
            # Create Gujarati Script and Letters
            script = self.seed_script()
            self.seed_vowels(script)
            self.seed_consonants(script)

        self.stdout.write(self.style.SUCCESS(
            '\n' + '=' * 60 +
            '\nGujarati Alphabet Seeded Successfully!' +
            '\n' + '=' * 60 +
            '\n  Script: Gujarati (ગુજરાતી લિપિ)' +
            '\n  Vowels: 14' +
            '\n  Consonants: 34' +
            '\n  Total Letters: 48' +
            '\n' + '=' * 60
        ))

    def clear_existing_data(self):
        """Clear existing Gujarati alphabet data."""
        self.stdout.write('Clearing existing Gujarati alphabet data...')
        Script.objects.filter(language='GUJARATI').delete()
        self.stdout.write(self.style.SUCCESS('Cleared existing Gujarati data.'))

    def seed_script(self):
        """Create Gujarati script."""
        self.stdout.write('Creating Gujarati script...')

        script, created = Script.objects.update_or_create(
            language='GUJARATI',
            defaults={
                'name': 'Gujarati Script',
                'name_native': 'ગુજરાતી લિપિ',
                'description': 'Gujarati script (વર્ણમાળા) is an abugida script used for writing the Gujarati language. It has 48 letters: 14 vowels and 34 consonants.',
                'total_letters': 48,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'  Created script: {script.name}'))
        else:
            self.stdout.write(f'  Updated script: {script.name}')

        return script

    def seed_vowels(self, script):
        """Create vowel letters (સ્વર - Swar)."""
        self.stdout.write('Creating vowels (સ્વર)...')

        category, _ = AlphabetCategory.objects.update_or_create(
            script=script,
            category_type='VOWEL',
            defaults={
                'name': 'Vowels',
                'name_native': 'સ્વર',
                'description': 'Gujarati vowel letters - 14 independent vowel sounds',
                'order': 1,
            }
        )

        vowels = [
            {
                'character': 'અ',
                'romanization': 'a',
                'ipa': '/ə/',
                'pronunciation_guide': 'a as in about',
                'example_word': 'અનાર',
                'example_word_romanization': 'anaar',
                'example_word_translation': 'Pomegranate',
                'example_image': 'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=120&h=120&fit=crop',
            },
            {
                'character': 'આ',
                'romanization': 'aa',
                'ipa': '/aː/',
                'pronunciation_guide': 'aa as in father',
                'example_word': 'આમ',
                'example_word_romanization': 'aam',
                'example_word_translation': 'Mango',
                'example_image': 'https://images.unsplash.com/photo-1553279768-865429fa0078?w=120&h=120&fit=crop',
            },
            {
                'character': 'ઇ',
                'romanization': 'i',
                'ipa': '/ɪ/',
                'pronunciation_guide': 'i as in bit',
                'example_word': 'ઇમલી',
                'example_word_romanization': 'imli',
                'example_word_translation': 'Tamarind',
                'example_image': 'https://images.unsplash.com/photo-1590502160462-58b41354f588?w=120&h=120&fit=crop',
            },
            {
                'character': 'ઈ',
                'romanization': 'ee',
                'ipa': '/iː/',
                'pronunciation_guide': 'ee as in feet',
                'example_word': 'ઈંડું',
                'example_word_romanization': 'indu',
                'example_word_translation': 'Egg',
                'example_image': 'https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=120&h=120&fit=crop',
            },
            {
                'character': 'ઉ',
                'romanization': 'u',
                'ipa': '/ʊ/',
                'pronunciation_guide': 'u as in put',
                'example_word': 'ઉલ્લુ',
                'example_word_romanization': 'ullu',
                'example_word_translation': 'Owl',
                'example_image': 'https://images.unsplash.com/photo-1543549790-8b5f4a028cfb?w=120&h=120&fit=crop',
            },
            {
                'character': 'ઊ',
                'romanization': 'oo',
                'ipa': '/uː/',
                'pronunciation_guide': 'oo as in boot',
                'example_word': 'ઊન',
                'example_word_romanization': 'oon',
                'example_word_translation': 'Wool',
                'example_image': 'https://images.unsplash.com/photo-1544967082-d9d25d867d66?w=120&h=120&fit=crop',
            },
            {
                'character': 'એ',
                'romanization': 'e',
                'ipa': '/e/',
                'pronunciation_guide': 'e as in bet',
                'example_word': 'એક',
                'example_word_romanization': 'ek',
                'example_word_translation': 'One',
                'example_image': 'https://images.unsplash.com/photo-1509228627152-72ae9ae6848d?w=120&h=120&fit=crop',
            },
            {
                'character': 'ઐ',
                'romanization': 'ai',
                'ipa': '/ʌɪ/',
                'pronunciation_guide': 'ai as in aisle',
                'example_word': 'ઐનક',
                'example_word_romanization': 'ainak',
                'example_word_translation': 'Glasses',
                'example_image': 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=120&h=120&fit=crop',
            },
            {
                'character': 'ઓ',
                'romanization': 'o',
                'ipa': '/o/',
                'pronunciation_guide': 'o as in go',
                'example_word': 'ઓખલી',
                'example_word_romanization': 'okhali',
                'example_word_translation': 'Mortar',
                'example_image': 'https://images.unsplash.com/photo-1506976785307-8732e854ad03?w=120&h=120&fit=crop',
            },
            {
                'character': 'ઔ',
                'romanization': 'au',
                'ipa': '/ʌʊ/',
                'pronunciation_guide': 'au as in taught',
                'example_word': 'ઔરત',
                'example_word_romanization': 'aurat',
                'example_word_translation': 'Woman',
                'example_image': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=120&h=120&fit=crop',
            },
            {
                'character': 'અં',
                'romanization': 'am',
                'ipa': '/əm/',
                'pronunciation_guide': 'nasal a',
                'example_word': 'અંગ',
                'example_word_romanization': 'ang',
                'example_word_translation': 'Limb',
                'example_image': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=120&h=120&fit=crop',
            },
            {
                'character': 'અઃ',
                'romanization': 'ah',
                'ipa': '/əh/',
                'pronunciation_guide': 'aspirated a',
                'example_word': 'દુઃખ',
                'example_word_romanization': 'duhkha',
                'example_word_translation': 'Sorrow',
                'example_image': 'https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=120&h=120&fit=crop',
            },
            {
                'character': 'ઋ',
                'romanization': 'ri',
                'ipa': '/rɪ/',
                'pronunciation_guide': 'vowel ri',
                'example_word': 'ઋષિ',
                'example_word_romanization': 'rishi',
                'example_word_translation': 'Sage',
                'example_image': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=120&h=120&fit=crop',
            },
            {
                'character': 'ૠ',
                'romanization': 'ree',
                'ipa': '/riː/',
                'pronunciation_guide': 'long vowel ri',
                'example_word': '',
                'example_word_romanization': '',
                'example_word_translation': 'Rare usage',
                'example_image': '',
            },
        ]

        for i, vowel in enumerate(vowels, 1):
            Letter.objects.update_or_create(
                category=category,
                character=vowel['character'],
                defaults={
                    'romanization': vowel['romanization'],
                    'ipa': vowel['ipa'],
                    'pronunciation_guide': vowel['pronunciation_guide'],
                    'example_word': vowel['example_word'],
                    'example_word_romanization': vowel['example_word_romanization'],
                    'example_word_translation': vowel['example_word_translation'],
                    'example_image': vowel.get('example_image') or None,
                    'order': i,
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(vowels)} vowels'))

    def seed_consonants(self, script):
        """Create consonant letters (વ્યંજન - Vyanjan)."""
        self.stdout.write('Creating consonants (વ્યંજન)...')

        category, _ = AlphabetCategory.objects.update_or_create(
            script=script,
            category_type='CONSONANT',
            defaults={
                'name': 'Consonants',
                'name_native': 'વ્યંજન',
                'description': 'Gujarati consonant letters - 34 consonant sounds grouped by articulation',
                'order': 2,
            }
        )

        consonants = [
            # Velar/Guttural (ક વર્ગ)
            {
                'character': 'ક',
                'romanization': 'ka',
                'ipa': '/k/',
                'pronunciation_guide': 'k as in kite',
                'example_word': 'કમળ',
                'example_word_romanization': 'kamal',
                'example_word_translation': 'Lotus',
                'example_image': 'https://images.unsplash.com/photo-1474557157379-8aa74a6ef541?w=120&h=120&fit=crop',
            },
            {
                'character': 'ખ',
                'romanization': 'kha',
                'ipa': '/kʰ/',
                'pronunciation_guide': 'kh as in khan',
                'example_word': 'ખરગોશ',
                'example_word_romanization': 'khargosh',
                'example_word_translation': 'Rabbit',
                'example_image': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=120&h=120&fit=crop',
            },
            {
                'character': 'ગ',
                'romanization': 'ga',
                'ipa': '/ɡ/',
                'pronunciation_guide': 'g as in go',
                'example_word': 'ગાય',
                'example_word_romanization': 'gaay',
                'example_word_translation': 'Cow',
                'example_image': 'https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=120&h=120&fit=crop',
            },
            {
                'character': 'ઘ',
                'romanization': 'gha',
                'ipa': '/ɡʰ/',
                'pronunciation_guide': 'gh as in ghost',
                'example_word': 'ઘર',
                'example_word_romanization': 'ghar',
                'example_word_translation': 'House',
                'example_image': 'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=120&h=120&fit=crop',
            },
            {
                'character': 'ઙ',
                'romanization': 'nga',
                'ipa': '/ŋ/',
                'pronunciation_guide': 'ng as in sing',
                'example_word': 'અંગ',
                'example_word_romanization': 'ang',
                'example_word_translation': 'Limb',
                'example_image': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=120&h=120&fit=crop',
            },
            # Palatal (ચ વર્ગ)
            {
                'character': 'ચ',
                'romanization': 'cha',
                'ipa': '/tʃ/',
                'pronunciation_guide': 'ch as in chair',
                'example_word': 'ચમચી',
                'example_word_romanization': 'chamchi',
                'example_word_translation': 'Spoon',
                'example_image': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=120&h=120&fit=crop',
            },
            {
                'character': 'છ',
                'romanization': 'chha',
                'ipa': '/tʃʰ/',
                'pronunciation_guide': 'chh as in church',
                'example_word': 'છાતા',
                'example_word_romanization': 'chhaataa',
                'example_word_translation': 'Umbrella',
                'example_image': 'https://images.unsplash.com/photo-1534309466160-70b22cc6252c?w=120&h=120&fit=crop',
            },
            {
                'character': 'જ',
                'romanization': 'ja',
                'ipa': '/dʒ/',
                'pronunciation_guide': 'j as in jump',
                'example_word': 'જહાજ',
                'example_word_romanization': 'jahaaj',
                'example_word_translation': 'Ship',
                'example_image': 'https://images.unsplash.com/photo-1534609178244-86f2ab3cd59d?w=120&h=120&fit=crop',
            },
            {
                'character': 'ઝ',
                'romanization': 'jha',
                'ipa': '/dʒʰ/',
                'pronunciation_guide': 'jh as in hedgehog',
                'example_word': 'ઝંડો',
                'example_word_romanization': 'jhando',
                'example_word_translation': 'Flag',
                'example_image': 'https://images.unsplash.com/photo-1569974507005-6dc61f97fb5c?w=120&h=120&fit=crop',
            },
            {
                'character': 'ઞ',
                'romanization': 'nya',
                'ipa': '/ɲ/',
                'pronunciation_guide': 'ny as in canyon',
                'example_word': '',
                'example_word_romanization': '',
                'example_word_translation': 'Rare usage',
                'example_image': '',
            },
            # Retroflex (ટ વર્ગ)
            {
                'character': 'ટ',
                'romanization': 'ta',
                'ipa': '/ʈ/',
                'pronunciation_guide': 't (hard)',
                'example_word': 'ટમેટું',
                'example_word_romanization': 'tametu',
                'example_word_translation': 'Tomato',
                'example_image': 'https://images.unsplash.com/photo-1546470427-227c7369cfc0?w=120&h=120&fit=crop',
            },
            {
                'character': 'ઠ',
                'romanization': 'tha',
                'ipa': '/ʈʰ/',
                'pronunciation_guide': 'th (hard)',
                'example_word': 'ઠંડી',
                'example_word_romanization': 'thandi',
                'example_word_translation': 'Cold',
                'example_image': 'https://images.unsplash.com/photo-1491002052546-bf38f186af56?w=120&h=120&fit=crop',
            },
            {
                'character': 'ડ',
                'romanization': 'da',
                'ipa': '/ɖ/',
                'pronunciation_guide': 'd (hard)',
                'example_word': 'ડમરું',
                'example_word_romanization': 'damru',
                'example_word_translation': 'Drum',
                'example_image': 'https://images.unsplash.com/photo-1519892300165-cb5542fb47c7?w=120&h=120&fit=crop',
            },
            {
                'character': 'ઢ',
                'romanization': 'dha',
                'ipa': '/ɖʰ/',
                'pronunciation_guide': 'dh (hard)',
                'example_word': 'ઢોલ',
                'example_word_romanization': 'dhol',
                'example_word_translation': 'Drum',
                'example_image': 'https://images.unsplash.com/photo-1543443258-92b04ad5ec6b?w=120&h=120&fit=crop',
            },
            {
                'character': 'ણ',
                'romanization': 'na',
                'ipa': '/ɳ/',
                'pronunciation_guide': 'n (retroflex)',
                'example_word': 'બાણ',
                'example_word_romanization': 'baan',
                'example_word_translation': 'Arrow',
                'example_image': 'https://images.unsplash.com/photo-1579783483458-83d02161294e?w=120&h=120&fit=crop',
            },
            # Dental (ત વર્ગ)
            {
                'character': 'ત',
                'romanization': 'ta',
                'ipa': '/t̪/',
                'pronunciation_guide': 't as in top',
                'example_word': 'તારો',
                'example_word_romanization': 'taaro',
                'example_word_translation': 'Star',
                'example_image': 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=120&h=120&fit=crop',
            },
            {
                'character': 'થ',
                'romanization': 'tha',
                'ipa': '/t̪ʰ/',
                'pronunciation_guide': 'th as in think',
                'example_word': 'થાળી',
                'example_word_romanization': 'thaali',
                'example_word_translation': 'Plate',
                'example_image': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=120&h=120&fit=crop',
            },
            {
                'character': 'દ',
                'romanization': 'da',
                'ipa': '/d̪/',
                'pronunciation_guide': 'd as in door',
                'example_word': 'દવા',
                'example_word_romanization': 'davaa',
                'example_word_translation': 'Medicine',
                'example_image': 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=120&h=120&fit=crop',
            },
            {
                'character': 'ધ',
                'romanization': 'dha',
                'ipa': '/d̪ʰ/',
                'pronunciation_guide': 'dh as in dharma',
                'example_word': 'ધનુષ',
                'example_word_romanization': 'dhanush',
                'example_word_translation': 'Bow',
                'example_image': 'https://images.unsplash.com/photo-1510925758641-869d353cecc7?w=120&h=120&fit=crop',
            },
            {
                'character': 'ન',
                'romanization': 'na',
                'ipa': '/n/',
                'pronunciation_guide': 'n as in name',
                'example_word': 'નળ',
                'example_word_romanization': 'nal',
                'example_word_translation': 'Tap',
                'example_image': 'https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=120&h=120&fit=crop',
            },
            # Labial (પ વર્ગ)
            {
                'character': 'પ',
                'romanization': 'pa',
                'ipa': '/p/',
                'pronunciation_guide': 'p as in pen',
                'example_word': 'પતંગ',
                'example_word_romanization': 'patang',
                'example_word_translation': 'Kite',
                'example_image': 'https://images.unsplash.com/photo-1517479149777-5f3b1511d5ad?w=120&h=120&fit=crop',
            },
            {
                'character': 'ફ',
                'romanization': 'pha',
                'ipa': '/pʰ/',
                'pronunciation_guide': 'ph/f as in phone',
                'example_word': 'ફળ',
                'example_word_romanization': 'phal',
                'example_word_translation': 'Fruit',
                'example_image': 'https://images.unsplash.com/photo-1619566636858-adf3ef46400b?w=120&h=120&fit=crop',
            },
            {
                'character': 'બ',
                'romanization': 'ba',
                'ipa': '/b/',
                'pronunciation_guide': 'b as in ball',
                'example_word': 'બકરી',
                'example_word_romanization': 'bakri',
                'example_word_translation': 'Goat',
                'example_image': 'https://images.unsplash.com/photo-1524024973431-2ad916746881?w=120&h=120&fit=crop',
            },
            {
                'character': 'ભ',
                'romanization': 'bha',
                'ipa': '/bʰ/',
                'pronunciation_guide': 'bh as in abhor',
                'example_word': 'ભાલુ',
                'example_word_romanization': 'bhaalu',
                'example_word_translation': 'Bear',
                'example_image': 'https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=120&h=120&fit=crop',
            },
            {
                'character': 'મ',
                'romanization': 'ma',
                'ipa': '/m/',
                'pronunciation_guide': 'm as in mother',
                'example_word': 'માછલી',
                'example_word_romanization': 'maachhli',
                'example_word_translation': 'Fish',
                'example_image': 'https://images.unsplash.com/photo-1524704654690-b56c05c78a00?w=120&h=120&fit=crop',
            },
            # Semivowels and Sibilants
            {
                'character': 'ય',
                'romanization': 'ya',
                'ipa': '/j/',
                'pronunciation_guide': 'y as in yes',
                'example_word': 'યાત્રા',
                'example_word_romanization': 'yaatraa',
                'example_word_translation': 'Journey',
                'example_image': 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=120&h=120&fit=crop',
            },
            {
                'character': 'ર',
                'romanization': 'ra',
                'ipa': '/ɾ/',
                'pronunciation_guide': 'r as in run',
                'example_word': 'રાજા',
                'example_word_romanization': 'raajaa',
                'example_word_translation': 'King',
                'example_image': 'https://images.unsplash.com/photo-1578632292335-df3abbb0d586?w=120&h=120&fit=crop',
            },
            {
                'character': 'લ',
                'romanization': 'la',
                'ipa': '/l/',
                'pronunciation_guide': 'l as in love',
                'example_word': 'લાડુ',
                'example_word_romanization': 'laadu',
                'example_word_translation': 'Laddu Sweet',
                'example_image': 'https://images.unsplash.com/photo-1666190094553-d8cfcfb80124?w=120&h=120&fit=crop',
            },
            {
                'character': 'વ',
                'romanization': 'va',
                'ipa': '/ʋ/',
                'pronunciation_guide': 'v as in van',
                'example_word': 'વન',
                'example_word_romanization': 'van',
                'example_word_translation': 'Forest',
                'example_image': 'https://images.unsplash.com/photo-1448375240586-882707db888b?w=120&h=120&fit=crop',
            },
            {
                'character': 'શ',
                'romanization': 'sha',
                'ipa': '/ʃ/',
                'pronunciation_guide': 'sh as in ship',
                'example_word': 'શેર',
                'example_word_romanization': 'sher',
                'example_word_translation': 'Lion',
                'example_image': 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=120&h=120&fit=crop',
            },
            {
                'character': 'ષ',
                'romanization': 'sha',
                'ipa': '/ʂ/',
                'pronunciation_guide': 'sh (retroflex)',
                'example_word': '',
                'example_word_romanization': '',
                'example_word_translation': 'Rare usage',
                'example_image': '',
            },
            {
                'character': 'સ',
                'romanization': 'sa',
                'ipa': '/s/',
                'pronunciation_guide': 's as in sun',
                'example_word': 'સફરજન',
                'example_word_romanization': 'sapharjan',
                'example_word_translation': 'Apple',
                'example_image': 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=120&h=120&fit=crop',
            },
            {
                'character': 'હ',
                'romanization': 'ha',
                'ipa': '/ɦ/',
                'pronunciation_guide': 'h as in house',
                'example_word': 'હાથી',
                'example_word_romanization': 'haathi',
                'example_word_translation': 'Elephant',
                'example_image': 'https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=120&h=120&fit=crop',
            },
            {
                'character': 'ળ',
                'romanization': 'la',
                'ipa': '/ɭ/',
                'pronunciation_guide': 'l (retroflex)',
                'example_word': '',
                'example_word_romanization': '',
                'example_word_translation': 'Rare usage',
                'example_image': '',
            },
        ]

        for i, consonant in enumerate(consonants, 1):
            Letter.objects.update_or_create(
                category=category,
                character=consonant['character'],
                defaults={
                    'romanization': consonant['romanization'],
                    'ipa': consonant['ipa'],
                    'pronunciation_guide': consonant['pronunciation_guide'],
                    'example_word': consonant['example_word'],
                    'example_word_romanization': consonant['example_word_romanization'],
                    'example_word_translation': consonant['example_word_translation'],
                    'example_image': consonant.get('example_image') or None,
                    'order': i,
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(consonants)} consonants'))
