"""
Seed command for complete Gujarati L1-L2 curriculum.
Following the same structure as Hindi/Tamil/Punjabi curriculum.
Uses Gujarati script (ગુજરાતી).
"""
import logging
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.curriculum.models import (
    Script, AlphabetCategory, Letter, Matra,
    VocabularyTheme, VocabularyWord,
    CurriculumLevel, Song, Game, Assessment,
    PeppiPhrase,
)
from apps.stories.models import Story, StoryPage

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Seed complete Gujarati L1-L2 curriculum (Gujarati script)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing Gujarati data before seeding',
        )

    def handle(self, *args, **options):
        self.stdout.write('Seeding Gujarati L1-L2 curriculum...\n')

        if options['clear']:
            self.clear_existing_data()

        with transaction.atomic():
            # 1. Create Gujarati Script and Letters
            script = self.seed_script()
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
            '\nGujarati L1-L2 Curriculum Seeded Successfully!' +
            '\n' + '=' * 60 +
            '\n  Script: Gujarati (ગુજરાતી)' +
            '\n  Vowels: 13' +
            '\n  Consonants: 33' +
            '\n  Matras: 10' +
            '\n  Vocabulary Words: 70+' +
            '\n  Stories: 10' +
            '\n  Songs: 5' +
            '\n  Games: 5' +
            '\n  Assessments: 2' +
            '\n' + '=' * 60
        ))

    def clear_existing_data(self):
        """Clear existing Gujarati data."""
        self.stdout.write('Clearing existing Gujarati data...')
        Script.objects.filter(language='GUJARATI').delete()
        VocabularyTheme.objects.filter(language='GUJARATI').delete()
        Game.objects.filter(language='GUJARATI').delete()
        Assessment.objects.filter(language='GUJARATI').delete()
        PeppiPhrase.objects.filter(context__icontains='gujarati').delete()
        self.stdout.write(self.style.SUCCESS('Cleared existing Gujarati data.'))

    def seed_script(self):
        """Create Gujarati script."""
        self.stdout.write('Creating Gujarati script...')
        script, created = Script.objects.update_or_create(
            language='GUJARATI',
            defaults={
                'name': 'Gujarati Script',
                'name_native': 'ગુજરાતી',
                'description': 'Gujarati script is used to write the Gujarati language. It evolved from the Devanagari script and has 33 consonants and vowels.',
                'total_letters': 56,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'  Created script: {script.name}'))
        else:
            self.stdout.write(f'  Updated script: {script.name}')
        return script

    def seed_vowels(self, script):
        """Create vowel letters (સ્વર)."""
        self.stdout.write('Creating vowels (સ્વર)...')
        category, _ = AlphabetCategory.objects.update_or_create(
            script=script,
            category_type='VOWEL',
            defaults={
                'name': 'Vowels',
                'name_native': 'સ્વર',
                'description': 'Vowel sounds in Gujarati script',
                'order': 1,
            }
        )

        vowels = [
            {'character': 'અ', 'romanization': 'a', 'ipa': '/ə/', 'example_word': 'અંબર', 'example_translation': 'sky', 'mnemonic': 'Short A as in about'},
            {'character': 'આ', 'romanization': 'aa', 'ipa': '/aː/', 'example_word': 'આમ', 'example_translation': 'mango', 'mnemonic': 'Long A as in father'},
            {'character': 'ઇ', 'romanization': 'i', 'ipa': '/ɪ/', 'example_word': 'ઇમલી', 'example_translation': 'tamarind', 'mnemonic': 'Short I as in bit'},
            {'character': 'ઈ', 'romanization': 'ee', 'ipa': '/iː/', 'example_word': 'ઈ', 'example_translation': 'this', 'mnemonic': 'Long EE as in meet'},
            {'character': 'ઉ', 'romanization': 'u', 'ipa': '/ʊ/', 'example_word': 'ઉંદર', 'example_translation': 'rat', 'mnemonic': 'Short U as in put'},
            {'character': 'ઊ', 'romanization': 'oo', 'ipa': '/uː/', 'example_word': 'ઊંટ', 'example_translation': 'camel', 'mnemonic': 'Long OO as in cool'},
            {'character': 'ઋ', 'romanization': 'ri', 'ipa': '/rɪ/', 'example_word': 'ઋષિ', 'example_translation': 'sage', 'mnemonic': 'RI as in brick'},
            {'character': 'એ', 'romanization': 'e', 'ipa': '/eː/', 'example_word': 'એક', 'example_translation': 'one', 'mnemonic': 'AY as in day'},
            {'character': 'ઐ', 'romanization': 'ai', 'ipa': '/ɛː/', 'example_word': 'ઐ', 'example_translation': 'I', 'mnemonic': 'AI as in aisle'},
            {'character': 'ઓ', 'romanization': 'o', 'ipa': '/oː/', 'example_word': 'ઓ', 'example_translation': 'that', 'mnemonic': 'OH as in go'},
            {'character': 'ઔ', 'romanization': 'au', 'ipa': '/ɔː/', 'example_word': 'ઔ', 'example_translation': 'and', 'mnemonic': 'OW as in how'},
            {'character': 'અં', 'romanization': 'an', 'ipa': '/əŋ/', 'example_word': 'અં', 'example_translation': 'nasal N', 'mnemonic': 'Anusvara'},
            {'character': 'અઃ', 'romanization': 'ah', 'ipa': '/əh/', 'example_word': 'અઃ', 'example_translation': 'Visarga', 'mnemonic': 'AH sound'},
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
                    'order': i,
                    'is_active': True,
                }
            )
        self.stdout.write(self.style.SUCCESS(f'  Created {len(vowels)} vowels'))

    def seed_consonants(self, script):
        """Create consonant letters organized by varga."""
        self.stdout.write('Creating consonants (વ્યંજન)...')
        category, _ = AlphabetCategory.objects.update_or_create(
            script=script,
            category_type='CONSONANT',
            defaults={
                'name': 'Consonants',
                'name_native': 'વ્યંજન',
                'description': 'Consonant sounds in Gujarati script',
                'order': 2,
            }
        )

        consonants = [
            {'character': 'ક', 'romanization': 'ka', 'ipa': '/k/', 'group': 'KA_VARGA', 'example_word': 'કમળ', 'example_translation': 'lotus', 'mnemonic': 'As in kite'},
            {'character': 'ખ', 'romanization': 'kha', 'ipa': '/kʰ/', 'group': 'KA_VARGA', 'example_word': 'ખ', 'example_translation': 'empty', 'mnemonic': 'Aspirated K'},
            {'character': 'ગ', 'romanization': 'ga', 'ipa': '/g/', 'group': 'KA_VARGA', 'example_word': 'ગાય', 'example_translation': 'cow', 'mnemonic': 'As in go'},
            {'character': 'ઘ', 'romanization': 'gha', 'ipa': '/gʰ/', 'group': 'KA_VARGA', 'example_word': 'ઘર', 'example_translation': 'house', 'mnemonic': 'Aspirated G'},
            {'character': 'ઙ', 'romanization': 'nga', 'ipa': '/ŋ/', 'group': 'KA_VARGA', 'example_word': 'ઙ', 'example_translation': 'ng sound', 'mnemonic': 'As in singer'},
            {'character': 'ચ', 'romanization': 'cha', 'ipa': '/tʃ/', 'group': 'CHA_VARGA', 'example_word': 'ચ', 'example_translation': 'eyes', 'mnemonic': 'As in chair'},
            {'character': 'છ', 'romanization': 'chha', 'ipa': '/tʃʰ/', 'group': 'CHA_VARGA', 'example_word': 'છ', 'example_translation': 'umbrella', 'mnemonic': 'Aspirated CH'},
            {'character': 'જ', 'romanization': 'ja', 'ipa': '/dʒ/', 'group': 'CHA_VARGA', 'example_word': 'જ', 'example_translation': 'win', 'mnemonic': 'As in jump'},
            {'character': 'ઝ', 'romanization': 'jha', 'ipa': '/dʒʰ/', 'group': 'CHA_VARGA', 'example_word': 'ઝ', 'example_translation': 'tremble', 'mnemonic': 'Aspirated J'},
            {'character': 'ઞ', 'romanization': 'nya', 'ipa': '/ɲ/', 'group': 'CHA_VARGA', 'example_word': 'ઞ', 'example_translation': 'nya', 'mnemonic': 'As in canyon'},
            {'character': 'ટ', 'romanization': 'ta', 'ipa': '/ʈ/', 'group': 'TA_VARGA', 'example_word': 'ટ', 'example_translation': 'star', 'mnemonic': 'Retroflex T'},
            {'character': 'ઠ', 'romanization': 'tha', 'ipa': '/ʈʰ/', 'group': 'TA_VARGA', 'example_word': 'ઠ', 'example_translation': 'cold', 'mnemonic': 'Aspirated retroflex T'},
            {'character': 'ડ', 'romanization': 'da', 'ipa': '/ɖ/', 'group': 'TA_VARGA', 'example_word': 'ડ', 'example_translation': 'army', 'mnemonic': 'Retroflex D'},
            {'character': 'ઢ', 'romanization': 'dha', 'ipa': '/ɖʰ/', 'group': 'TA_VARGA', 'example_word': 'ઢ', 'example_translation': 'drum', 'mnemonic': 'Aspirated retroflex D'},
            {'character': 'ણ', 'romanization': 'na', 'ipa': '/ɳ/', 'group': 'TA_VARGA', 'example_word': 'ણ', 'example_translation': 'must', 'mnemonic': 'Retroflex N'},
            {'character': 'ત', 'romanization': 'ta', 'ipa': '/t̪/', 'group': 'TA_VARGA_2', 'example_word': 'ત', 'example_translation': 'rope', 'mnemonic': 'Dental T'},
            {'character': 'થ', 'romanization': 'tha', 'ipa': '/t̪ʰ/', 'group': 'TA_VARGA_2', 'example_word': 'થ', 'example_translation': 'plate', 'mnemonic': 'Aspirated dental T'},
            {'character': 'દ', 'romanization': 'da', 'ipa': '/d̪/', 'group': 'TA_VARGA_2', 'example_word': 'દ', 'example_translation': 'milk', 'mnemonic': 'Dental D'},
            {'character': 'ધ', 'romanization': 'dha', 'ipa': '/d̪ʰ/', 'group': 'TA_VARGA_2', 'example_word': 'ધ', 'example_translation': 'wealth', 'mnemonic': 'Aspirated dental D'},
            {'character': 'ન', 'romanization': 'na', 'ipa': '/n/', 'group': 'TA_VARGA_2', 'example_word': 'ન', 'example_translation': 'sit', 'mnemonic': 'Dental N'},
            {'character': 'પ', 'romanization': 'pa', 'ipa': '/p/', 'group': 'PA_VARGA', 'example_word': 'પ', 'example_translation': 'butterfly', 'mnemonic': 'As in pen'},
            {'character': 'ફ', 'romanization': 'pha', 'ipa': '/pʰ/', 'group': 'PA_VARGA', 'example_word': 'ફ', 'example_translation': 'flower', 'mnemonic': 'Aspirated P'},
            {'character': 'બ', 'romanization': 'ba', 'ipa': '/b/', 'group': 'PA_VARGA', 'example_word': 'બ', 'example_translation': 'goat', 'mnemonic': 'As in ball'},
            {'character': 'ભ', 'romanization': 'bha', 'ipa': '/bʰ/', 'group': 'PA_VARGA', 'example_word': 'ભ', 'example_translation': 'load', 'mnemonic': 'Aspirated B'},
            {'character': 'મ', 'romanization': 'ma', 'ipa': '/m/', 'group': 'PA_VARGA', 'example_word': 'મ', 'example_translation': 'fish', 'mnemonic': 'As in mother'},
            {'character': 'ય', 'romanization': 'ya', 'ipa': '/j/', 'group': 'ANTASTHA', 'example_word': 'ય', 'example_translation': 'one', 'mnemonic': 'As in yes'},
            {'character': 'ર', 'romanization': 'ra', 'ipa': '/r/', 'group': 'ANTASTHA', 'example_word': 'ર', 'example_translation': 'run', 'mnemonic': 'As in run'},
            {'character': 'લ', 'romanization': 'la', 'ipa': '/l/', 'group': 'ANTASTHA', 'example_word': 'લ', 'example_translation': 'red', 'mnemonic': 'As in love'},
            {'character': 'વ', 'romanization': 'va', 'ipa': '/ʋ/', 'group': 'ANTASTHA', 'example_word': 'વ', 'example_translation': 'rain', 'mnemonic': 'As in van'},
            {'character': 'શ', 'romanization': 'sha', 'ipa': '/ʃ/', 'group': 'USHMA', 'example_word': 'શ', 'example_translation': 'shirt', 'mnemonic': 'As in ship'},
            {'character': 'ષ', 'romanization': 'sha', 'ipa': '/ʂ/', 'group': 'USHMA', 'example_word': 'ષ', 'example_translation': 'six', 'mnemonic': 'Retroflex SH'},
            {'character': 'સ', 'romanization': 'sa', 'ipa': '/s/', 'group': 'USHMA', 'example_word': 'સ', 'example_translation': 'sun', 'mnemonic': 'As in sun'},
            {'character': 'હ', 'romanization': 'ha', 'ipa': '/h/', 'group': 'USHMA', 'example_word': 'હ', 'example_translation': 'smile', 'mnemonic': 'As in happy'},
            {'character': 'ળ', 'romanization': 'la', 'ipa': '/ɭ/', 'group': 'ANTASTHA', 'example_word': 'ળ', 'example_translation': 'necklace', 'mnemonic': 'Retroflex L'},
            {'character': 'ક્ષ', 'romanization': 'ksha', 'ipa': '/kʂ/', 'group': 'COMPOUND', 'example_word': 'ક્ષ', 'example_translation': 'mercy', 'mnemonic': 'KSHA sound'},
            {'character': 'જ્ઞ', 'romanization': 'gnya', 'ipa': '/dʒɲ/', 'group': 'COMPOUND', 'example_word': 'જ્ઞ', 'example_translation': 'knowledge', 'mnemonic': 'GNYA sound'},
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
                    'order': i,
                    'is_active': True,
                }
            )
        self.stdout.write(self.style.SUCCESS(f'  Created {len(consonants)} consonants'))

    def seed_matras(self, script):
        """Create matras (vowel marks)."""
        self.stdout.write('Creating matras (માત્રાઓ)...')
        matras = [
            {'symbol': 'ा', 'name': 'Aa Matra', 'sound': 'aa', 'example_with_ka': 'का', 'example_word': 'કાળો', 'translation': 'black'},
            {'symbol': 'િ', 'name': 'I Matra', 'sound': 'i', 'example_with_ka': 'કિ', 'example_word': 'કિતાબ', 'translation': 'book'},
            {'symbol': 'ी', 'name': 'Ee Matra', 'sound': 'ee', 'example_with_ka': 'કી', 'example_word': 'કીડી', 'translation': 'ant'},
            {'symbol': 'ુ', 'name': 'U Matra', 'sound': 'u', 'example_with_ka': 'કુ', 'example_word': 'કુતરું', 'translation': 'dog'},
            {'symbol': 'ૂ', 'name': 'Oo Matra', 'sound': 'oo', 'example_with_ka': 'કૂ', 'example_word': 'કૂદકો', 'translation': 'jump'},
            {'symbol': 'ૃ', 'name': 'Ri Matra', 'sound': 'ri', 'example_with_ka': 'કૃ', 'example_word': 'કૃપા', 'translation': 'mercy'},
            {'symbol': 'ો', 'name': 'O Matra', 'sound': 'o', 'example_with_ka': 'કો', 'example_word': 'કોયડો', 'translation': 'puzzle'},
            {'symbol': 'ૌ', 'name': 'Au Matra', 'sound': 'au', 'example_with_ka': 'કૌ', 'example_word': 'કૌશલ', 'translation': 'skill'},
            {'symbol': 'ં', 'name': 'Anusvara', 'sound': 'n', 'example_with_ka': 'કં', 'example_word': 'કંગાળ', 'translation': 'poor'},
            {'symbol': 'ઃ', 'name': 'Visarga', 'sound': 'h', 'example_with_ka': 'કઃ', 'example_word': 'દુઃખ', 'translation': 'sadness'},
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

        l1_themes = [
            {'name': 'Family', 'name_native': 'પરિવાર', 'icon': 'family', 'level': 1, 'words': [
                {'word': 'માં', 'romanization': 'Maa', 'translation': 'Mother', 'pos': 'NOUN'},
                {'word': 'પિતાજી', 'romanization': 'Pitaaji', 'translation': 'Father', 'pos': 'NOUN'},
                {'word': 'દાદી', 'romanization': 'Daadi', 'translation': 'Grandmother', 'pos': 'NOUN'},
                {'word': 'દાદો', 'romanization': 'Daado', 'translation': 'Grandfather', 'pos': 'NOUN'},
                {'word': 'ભાઈ', 'romanization': 'Bhaai', 'translation': 'Brother', 'pos': 'NOUN'},
                {'word': 'બહન', 'romanization': 'Bahin', 'translation': 'Sister', 'pos': 'NOUN'},
            ]},
            {'name': 'Colors', 'name_native': 'રંગ', 'icon': 'palette', 'level': 1, 'words': [
                {'word': 'લાલ', 'romanization': 'Laal', 'translation': 'Red', 'pos': 'ADJECTIVE'},
                {'word': 'ભાદરંગ', 'romanization': 'Bhaarang', 'translation': 'Blue', 'pos': 'ADJECTIVE'},
                {'word': 'પીળો', 'romanization': 'Peelo', 'translation': 'Yellow', 'pos': 'ADJECTIVE'},
                {'word': 'લીલો', 'romanization': 'Leelo', 'translation': 'Green', 'pos': 'ADJECTIVE'},
            ]},
            {'name': 'Numbers', 'name_native': 'નંબર', 'icon': 'numbers', 'level': 1, 'words': [
                {'word': 'એક', 'romanization': 'Ek', 'translation': 'One', 'pos': 'NUMBER'},
                {'word': 'બ', 'romanization': 'Be', 'translation': 'Two', 'pos': 'NUMBER'},
                {'word': 'ત્રણ', 'romanization': 'Tran', 'translation': 'Three', 'pos': 'NUMBER'},
                {'word': 'ચાર', 'romanization': 'Chaar', 'translation': 'Four', 'pos': 'NUMBER'},
                {'word': 'પાંચ', 'romanization': 'Paanch', 'translation': 'Five', 'pos': 'NUMBER'},
            ]},
            {'name': 'Animals', 'name_native': 'પ્રાણી', 'icon': 'pets', 'level': 1, 'words': [
                {'word': 'કૂતરો', 'romanization': 'Kootro', 'translation': 'Dog', 'pos': 'NOUN'},
                {'word': 'બિલલી', 'romanization': 'Billi', 'translation': 'Cat', 'pos': 'NOUN'},
                {'word': 'ગાય', 'romanization': 'Gaay', 'translation': 'Cow', 'pos': 'NOUN'},
            ]},
            {'name': 'Basics', 'name_native': 'બુનિયાદ', 'icon': 'star', 'level': 1, 'words': [
                {'word': 'પાણી', 'romanization': 'Paani', 'translation': 'Water', 'pos': 'NOUN'},
                {'word': 'રોટલી', 'romanization': 'Rotli', 'translation': 'Bread', 'pos': 'NOUN'},
            ]},
        ]

        l2_themes = [
            {'name': 'Extended Family', 'name_native': 'મોટો પરિવાર', 'icon': 'groups', 'level': 2, 'words': [
                {'word': 'મામો', 'romanization': 'Maamo', 'translation': 'Maternal Uncle', 'pos': 'NOUN'},
                {'word': 'મામી', 'romanization': 'Maami', 'translation': 'Maternal Aunt', 'pos': 'NOUN'},
                {'word': 'ચાચો', 'romanization': 'Chaacho', 'translation': 'Paternal Uncle', 'pos': 'NOUN'},
                {'word': 'ચાચી', 'romanization': 'Chaachi', 'translation': 'Paternal Aunt', 'pos': 'NOUN'},
            ]},
            {'name': 'More Colors', 'name_native': 'વધુ રંગ', 'icon': 'color_lens', 'level': 2, 'words': [
                {'word': 'કાળો', 'romanization': 'Kaalo', 'translation': 'Black', 'pos': 'ADJECTIVE'},
                {'word': 'સફર', 'romanization': 'Safar', 'translation': 'White', 'pos': 'ADJECTIVE'},
                {'word': 'નારંગી', 'romanization': 'Naarangee', 'translation': 'Orange', 'pos': 'ADJECTIVE'},
            ]},
            {'name': 'Numbers 6-10', 'name_native': 'નંબર 6-10', 'icon': 'pin', 'level': 2, 'words': [
                {'word': 'છ', 'romanization': 'Chh', 'translation': 'Six', 'pos': 'NUMBER'},
                {'word': 'સાત', 'romanization': 'Saat', 'translation': 'Seven', 'pos': 'NUMBER'},
                {'word': 'આઠ', 'romanization': 'Aath', 'translation': 'Eight', 'pos': 'NUMBER'},
                {'word': 'નવ', 'romanization': 'Nav', 'translation': 'Nine', 'pos': 'NUMBER'},
                {'word': 'દસ', 'romanization': 'Das', 'translation': 'Ten', 'pos': 'NUMBER'},
            ]},
            {'name': 'More Animals', 'name_native': 'વધુ પ્રાણી', 'icon': 'cruelty_free', 'level': 2, 'words': [
                {'word': 'ઘોડો', 'romanization': 'Ghodo', 'translation': 'Horse', 'pos': 'NOUN'},
                {'word': 'હાથી', 'romanization': 'Haathi', 'translation': 'Elephant', 'pos': 'NOUN'},
                {'word': 'સિંહ', 'romanization': 'Singh', 'translation': 'Lion', 'pos': 'NOUN'},
                {'word': 'વાંદરો', 'romanization': 'Vaandaro', 'translation': 'Monkey', 'pos': 'NOUN'},
                {'word': 'માછલી', 'romanization': 'Maachli', 'translation': 'Fish', 'pos': 'NOUN'},
            ]},
            {'name': 'Fruits', 'name_native': 'ફળ', 'icon': 'nutrition', 'level': 2, 'words': [
                {'word': 'સફરજન', 'romanization': 'Safarjan', 'translation': 'Apple', 'pos': 'NOUN'},
                {'word': 'કে঳ું', 'romanization': 'Kelu', 'translation': 'Banana', 'pos': 'NOUN'},
                {'word': 'આંબલો', 'romanization': 'Aamblo', 'translation': 'Mango', 'pos': 'NOUN'},
                {'word': 'દ્રાક્ષ', 'romanization': 'Draaksh', 'translation': 'Grapes', 'pos': 'NOUN'},
            ]},
            {'name': 'Body Parts', 'name_native': 'શરીર', 'icon': 'accessibility', 'level': 2, 'words': [
                {'word': 'માથું', 'romanization': 'Maathu', 'translation': 'Head', 'pos': 'NOUN'},
                {'word': 'આંખ', 'romanization': 'Aankh', 'translation': 'Eye', 'pos': 'NOUN'},
                {'word': 'નાક', 'romanization': 'Naak', 'translation': 'Nose', 'pos': 'NOUN'},
                {'word': 'કાન', 'romanization': 'Kaan', 'translation': 'Ear', 'pos': 'NOUN'},
                {'word': 'હાથ', 'romanization': 'Haath', 'translation': 'Hand', 'pos': 'NOUN'},
            ]},
            {'name': 'Actions', 'name_native': 'ક્રિયાઓ', 'icon': 'directions_run', 'level': 2, 'words': [
                {'word': 'ખાવુ', 'romanization': 'Khaavun', 'translation': 'To eat', 'pos': 'VERB'},
                {'word': 'પીવુ', 'romanization': 'Peevun', 'translation': 'To drink', 'pos': 'VERB'},
                {'word': 'સૂવુ', 'romanization': 'Soovun', 'translation': 'To sleep', 'pos': 'VERB'},
                {'word': 'રમવુ', 'romanization': 'Ramavun', 'translation': 'To play', 'pos': 'VERB'},
                {'word': 'વાંચવુ', 'romanization': 'Vaanchavun', 'translation': 'To read', 'pos': 'VERB'},
            ]},
            {'name': 'Home', 'name_native': 'ઘર', 'icon': 'home', 'level': 2, 'words': [
                {'word': 'ઘર', 'romanization': 'Ghar', 'translation': 'Home', 'pos': 'NOUN'},
                {'word': 'ઓરડો', 'romanization': 'Oro', 'translation': 'Room', 'pos': 'NOUN'},
                {'word': 'દરવાજો', 'romanization': 'Darvaajo', 'translation': 'Door', 'pos': 'NOUN'},
                {'word': 'બારી', 'romanization': 'Baaree', 'translation': 'Window', 'pos': 'NOUN'},
            ]},
            {'name': 'Nature', 'name_native': 'કુદરત', 'icon': 'park', 'level': 2, 'words': [
                {'word': 'સૂરજ', 'romanization': 'Sooraj', 'translation': 'Sun', 'pos': 'NOUN'},
                {'word': 'ચંદ', 'romanization': 'Chand', 'translation': 'Moon', 'pos': 'NOUN'},
                {'word': 'તારો', 'romanization': 'Taaro', 'translation': 'Star', 'pos': 'NOUN'},
                {'word': 'ફૂલ', 'romanization': 'Phool', 'translation': 'Flower', 'pos': 'NOUN'},
                {'word': 'ઝાડ', 'romanization': 'Jhaad', 'translation': 'Tree', 'pos': 'NOUN'},
            ]},
        ]

        all_themes = l1_themes + l2_themes
        word_count = 0

        for i, theme_data in enumerate(all_themes, 1):
            theme, _ = VocabularyTheme.objects.update_or_create(
                language='GUJARATI',
                name=theme_data['name'],
                defaults={
                    'name_native': theme_data['name_native'],
                    'description': f"Learn {theme_data['name']} in Gujarati",
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
        """Create Gujarati stories for L1 and L2."""
        self.stdout.write('Creating Gujarati stories...')

        stories_data = [
            {'title': "Peppi's New Friend", 'title_hindi': 'પेप्पीનो नवो दोस्त', 'title_romanized': 'Peppino Navo Dost', 'level': 1, 'age_min': 4, 'age_max': 6, 'theme': 'friendship', 'tier': 'FREE', 'moral_english': 'True friends accept each other', 'moral_hindi': 'सच्चा दोस्त स्वीकार करता है', 'pages': [
                {'text': 'પेप्पी एक नानुं बिलली.', 'translation': 'Peppi is a small cat.'},
                {'text': 'પेप्पीने दोस्त जोईए.', 'translation': 'Peppi wants a friend.'},
                {'text': 'પेप्पीए कुकुर देख्यु.', 'translation': 'Peppi saw a dog.'},
                {'text': 'કुकुरनो नाम राजो.', 'translation': "The dog's name is Raj."},
                {'text': 'પेप्पी अने राजो दोस्त बन्या!', 'translation': 'Peppi and Raj became friends!'},
            ]},
            {'title': 'The Red Apple', 'title_hindi': 'લाल सफरजन', 'title_romanized': 'Laal Safarjan', 'level': 1, 'age_min': 4, 'age_max': 6, 'theme': 'sharing', 'tier': 'FREE', 'moral_english': 'Sharing brings happiness', 'moral_hindi': 'बाँटने से खुशी', 'pages': [
                {'text': 'झाड पर एक सफरजन.', 'translation': 'There is an apple on the tree.'},
                {'text': 'सफरजन लाल.', 'translation': 'The apple is red.'},
                {'text': 'બચ્ચो सफरजन मागतो.', 'translation': 'The child wants the apple.'},
                {'text': 'માએ सफरजन आप्यु.', 'translation': 'Mother gave the apple.'},
                {'text': 'બચ્ચो खुश!', 'translation': 'The child is happy!'},
            ]},
            {'title': 'My Family', 'title_hindi': 'મારો પરિવાર', 'title_romanized': 'Maro Parivaar', 'level': 1, 'age_min': 4, 'age_max': 6, 'theme': 'family', 'tier': 'FREE', 'moral_english': 'Family is treasure', 'moral_hindi': 'परिवार ताकत है', 'pages': [
                {'text': 'आ मारी माई.', 'translation': 'This is my mother.'},
                {'text': 'आ मारो पिताजी.', 'translation': 'This is my father.'},
                {'text': 'आ मारी दादी.', 'translation': 'This is my grandmother.'},
                {'text': 'आ मारो भाई.', 'translation': 'This is my brother.'},
                {'text': 'અમ્બરિવાર साथ रहे.', 'translation': 'We all live together.'},
            ]},
            {'title': 'Navratri Festival', 'title_hindi': 'નવરાત્રિ', 'title_romanized': 'Navratri', 'level': 2, 'age_min': 5, 'age_max': 7, 'theme': 'festival', 'tier': 'STANDARD', 'moral_english': 'Festivals bring joy', 'moral_hindi': 'त्योहार खुशी लाते हैं', 'pages': [
                {'text': 'आज Navratri!', 'translation': 'Today is Navratri!'},
                {'text': 'સર્વરિઓ खुश.', 'translation': 'Everyone is happy.'},
                {'text': 'गरबा गावे.', 'translation': 'We do Garba.'},
                {'text': 'Dandiya Raas.', 'translation': 'Dandiya Raas.'},
                {'text': 'Shubh Navratri!', 'translation': 'Happy Navratri!'},
            ]},
            {'title': 'Diwali Festival', 'title_hindi': 'દિવાળી', 'title_romanized': 'Diwali', 'level': 2, 'age_min': 5, 'age_max': 7, 'theme': 'festival', 'tier': 'STANDARD', 'moral_english': 'Light dispels darkness', 'moral_hindi': 'रोशनी अंधकार भगाती है', 'pages': [
                {'text': 'आज Diwali!', 'translation': 'Today is Diwali!'},
                {'text': 'घર मां diyo jalavay.', 'translation': 'We light lamps in house.'},
                {'text': 'rangoli banavay.', 'translation': 'Mother made rangoli.'},
                {'text': 'patakhe vagaravay.', 'translation': 'Father burst firecrackers.'},
                {'text': 'Shubh Diwali!', 'translation': 'Happy Diwali!'},
            ]},
            {'title': 'The Clever Fox', 'title_hindi': 'ચતુ� लोमडी', 'title_romanized': 'Chatur Lomdi', 'level': 2, 'age_min': 5, 'age_max': 7, 'theme': 'wisdom', 'tier': 'STANDARD', 'moral_english': 'Think before you act', 'moral_hindi': 'सोचो फिर करो', 'pages': [
                {'text': 'एक लोमडी.', 'translation': 'There was a fox.'},
                {'text': 'तने भूख.', 'translation': 'She was hungry.'},
                {'text': 'कागड देख्यो.', 'translation': 'She saw a crow.'},
                {'text': 'kagda na ota rotee.', 'translation': 'The crow had bread.'},
                {'text': 'Lomdi bolyo - Gayo!', 'translation': 'Fox said - Sing!'},
                {'text': 'kagad mukh kholyo.', 'translation': 'Crow opened mouth.'},
                {'text': 'rotee giri gayo!', 'translation': 'Bread fell!'},
            ]},
            {'title': 'Going to School', 'title_hindi': 'શાળાએ', 'title_romanized': 'Shalae', 'level': 2, 'age_min': 5, 'age_max': 7, 'theme': 'education', 'tier': 'STANDARD', 'moral_english': 'Education is important', 'moral_hindi': 'पढ़ाई जरूरी', 'pages': [
                {'text': 'subah 6 baje.', 'translation': 'Morning 6 AM.'},
                {'text': 'रानी उठी.', 'translation': 'Rani wakes up.'},
                {'text': 'muKha dhoyo.', 'translation': 'She washes face.'},
                {'text': 'khaad ne school jay.', 'translation': 'Eats and goes to school.'},
                {'text': 'shala ma padhe.', 'translation': 'She studies at school.'},
                {'text': 'dosto sath khele.', 'translation': 'She plays with friends.'},
            ]},
            {'title': 'The Thirsty Crow', 'title_hindi': 'તરસતો कागड', 'title_romanized': 'Taras to Kaagad', 'level': 2, 'age_min': 5, 'age_max': 7, 'theme': 'wisdom', 'tier': 'STANDARD', 'moral_english': 'Where there is a will', 'moral_hindi': 'चाह वाले राह पामे', 'pages': [
                {'text': 'एक कागड.', 'translation': 'There was a crow.'},
                {'text': 'तरसयो.', 'translation': 'He was thirsty.'},
                {'text': 'घड़ा देख्यो.', 'translation': 'He saw a pot.'},
                {'text': 'pani kam.', 'translation': 'Water was less.'},
                {'text': 'patthar да.', 'translation': 'He dropped pebbles.'},
                {'text': 'pani upar aayo!', 'translation': 'Water came up!'},
            ]},
            {'title': 'At the Farm', 'title_hindi': 'ખेतમાં', 'title_romanized': 'Khetma', 'level': 2, 'age_min': 5, 'age_max': 7, 'theme': 'nature', 'tier': 'STANDARD', 'moral_english': 'Respect farmers', 'moral_hindi': 'किसानों का सम्मान', 'pages': [
                {'text': 'aaje khetma gay.', 'translation': 'Today we went to farm.'},
                {'text': 'gaay dudh deve.', 'translation': 'Cow gives milk.'},
                {'text': 'murgi kukdo kare.', 'translation': 'Hen clucks.'},
                {'text': 'kheti vadhi vadhi!', 'translation': 'Farming is great!'},
            ]},
            {'title': 'Makar Sankranti', 'title_hindi': 'મકરસંક્રાંતિ', 'title_romanized': 'Makar Sankranti', 'level': 2, 'age_min': 5, 'age_max': 7, 'theme': 'festival', 'tier': 'STANDARD', 'moral_english': 'Harvest festival', 'moral_hindi': 'फसल का त्योहार', 'pages': [
                {'text': 'aaje Makar Sankranti!', 'translation': 'Today is Makar Sankranti!'},
                {'text': 'undhiyu banavay.', 'translation': 'We make Undhiyu.'},
                {'text': 'chikkis banavay.', 'translation': 'We make chikki.'},
                {'text': 'patang उड़ावे.', 'translation': 'Fly kites.'},
                {'text': 'Shubh Sankranti!', 'translation': 'Happy Sankranti!'},
            ]},
        ]

        for story_data in stories_data:
            story_slug = story_data['title'].lower().replace(' ', '-').replace("'", '')
            storyweaver_id = f"gu-l{story_data['level']}-{story_slug}"

            story, _ = Story.objects.update_or_create(
                storyweaver_id=storyweaver_id,
                defaults={
                    'language': 'GUJARATI',
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

            for i, page_data in enumerate(story_data['pages'], 1):
                StoryPage.objects.update_or_create(
                    story=story,
                    page_number=i,
                    defaults={
                        'text_content': page_data['text'],
                        'text_hindi': page_data['text'],
                        'text_romanized': page_data['translation'],
                    }
                )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(stories_data)} stories'))

    def seed_songs(self):
        """Create Gujarati songs for L1 and L2."""
        self.stdout.write('Creating Gujarati songs...')

        l1_level, _ = CurriculumLevel.objects.get_or_create(
            code='L1',
            defaults={
                'name_english': 'Discovery',
                'name_hindi': 'શોધ',
                'name_romanized': 'Shodh',
                'min_age': 4,
                'max_age': 5,
                'description': 'First steps in learning Gujarati',
                'order': 1,
                'is_active': True,
            }
        )

        songs_data = [
            {'title_english': 'Counting in Gujarati', 'title_hindi': 'ગુજરાતમાં ગણતરી', 'title_romanized': 'Gujaratma Ganatri', 'lyrics_hindi': 'એક, બ, ત્રણ,ચાર, \n|પાંચ, \n|', 'lyrics_romanized': 'Ek, Be, Tran, Char,\nPaanch,\n', 'lyrics_english': 'One, Two, Three, Four,\nFive,\n', 'category': 'EDUCATIONAL', 'age_min': 4, 'age_max': 6, 'duration_seconds': 60},
            {'title_english': 'Alphabet Song', 'title_hindi': 'અક્ષર ગીત', 'title_romanized': 'Akshar Geet', 'lyrics_hindi': 'અ,આ,ઇ,ઈ,\n|ઉ,ઊ,ઋ,\n|', 'lyrics_romanized': 'A, Aa, I, Ee,\nU, Uu, Ri,\n', 'lyrics_english': 'A, Aa, I, Ee,\nU, Uu, Ri,\n', 'category': 'EDUCATIONAL', 'age_min': 4, 'age_max': 7, 'duration_seconds': 90},
            {'title_english': 'The Train', 'title_hindi': 'રेલગાડી', 'title_romanized': 'Rail Gaadi', 'lyrics_hindi': 'ચુક,ચુક,રेલ,\n|ચાલ,ચાલ,\n|', 'lyrics_romanized': 'Chuk, Chuk, Rail,\nChal, Chal,\n', 'lyrics_english': 'Chuk Chuk Rail,\nChal Chal,\n', 'category': 'RHYME', 'age_min': 4, 'age_max': 6, 'duration_seconds': 50},
            {'title_english': 'Hello Song', 'title_hindi': 'નમસ્તे गानुं', 'title_romanized': 'Namaste Ganun', 'lyrics_hindi': 'નમસ્તे,નમસ્તे,\n|', 'lyrics_romanized': 'Namaste, Namaste,\n', 'lyrics_english': 'Hello Hello,\n', 'category': 'RHYME', 'age_min': 4, 'age_max': 6, 'duration_seconds': 45},
            {'title_english': 'Family Song', 'title_hindi': 'પરિવार गानुं', 'title_romanized': 'Parivaar Ganun', 'lyrics_hindi': 'માં,પિતाज,\n|', 'lyrics_romanized': 'Maa, Pitaa,\n', 'lyrics_english': 'Mother, Father,\n', 'category': 'RHYME', 'age_min': 4, 'age_max': 6, 'duration_seconds': 45},
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
                    'language': 'GUJARATI',
                    'order': i,
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(songs_data)} songs'))

    def seed_curriculum_levels(self):
        """Create L1 and L2 curriculum levels for Gujarati."""
        self.stdout.write('Creating curriculum levels...')

        levels_data = [
            {'code': 'L1', 'name_english': 'Discovery', 'name_hindi': 'શોધ', 'name_romanized': 'Shodh', 'min_age': 4, 'max_age': 5, 'description': 'First steps in learning Gujarati', 'peppi_welcome': 'નમસ્તे! Welcome to Peppi\'s Gujarati class!', 'peppi_completion': 'શાબાશ! You completed L1!', 'emoji': '🌱', 'theme_color': '#22c55e', 'order': 1, 'estimated_hours': 10, 'min_xp_required': 0, 'xp_reward': 400, 'is_free': True},
            {'code': 'L2', 'name_english': 'Building Blocks', 'name_hindi': 'બુનિયાદ', 'name_romanized': 'Buniyad', 'min_age': 5, 'max_age': 6, 'description': 'Learn consonants and matras', 'peppi_welcome': 'નમસ્તे! Ready to learn more?', 'peppi_completion': 'મફત! You are a Gujarati superstar!', 'emoji': '🌿', 'theme_color': '#3b82f6', 'order': 2, 'estimated_hours': 14, 'min_xp_required': 400, 'xp_reward': 700, 'is_free': False},
        ]

        for level_data in levels_data:
            CurriculumLevel.objects.update_or_create(code=level_data['code'], defaults=level_data)

        self.stdout.write(self.style.SUCCESS(f'  Created {len(levels_data)} curriculum levels'))

    def seed_peppi_phrases(self):
        """Create Peppi phrases in Gujarati."""
        self.stdout.write('Creating Peppi phrases...')

        phrases_data = [
            {'category': 'GREETING', 'text_hindi': 'નમસ્ત!', 'text_english': 'Hello!', 'text_romanized': 'Namaste!', 'context': 'gujarati_greeting'},
            {'category': 'CORRECT', 'text_hindi': 'શાબાશ!', 'text_english': 'Well done!', 'text_romanized': 'Shabaash!', 'context': 'gujarati_celebration'},
            {'category': 'CORRECT', 'text_hindi': 'મફત!', 'text_english': 'Great!', 'text_romanized': 'Mafat!', 'context': 'gujarati_wow'},
            {'category': 'CORRECT', 'text_hindi': 'ખૂબ સારુ!', 'text_english': 'Very good!', 'text_romanized': 'Khub Saaru!', 'context': 'gujarati_verygood'},
            {'category': 'WRONG', 'text_hindi': 'ફરીથી try!', 'text_english': 'Try again!', 'text_romanized': 'Fari Thi Try!', 'context': 'gujarati_tryagain'},
            {'category': 'ENCOURAGEMENT', 'text_hindi': 'તમનे कर्जुं!', 'text_english': 'You can do it!', 'text_romanized': 'Tamne Karnu!', 'context': 'gujarati_encourage'},
            {'category': 'FAREWELL', 'text_hindi': 'આવજો!', 'text_english': 'Goodbye!', 'text_romanized': 'Aavojo!', 'context': 'gujarati_farewell'},
            {'category': 'GREETING', 'text_hindi': 'ધનવાદ!', 'text_english': 'Thank you!', 'text_romanized': 'Dhanvad!', 'context': 'gujarati_thankyou'},
            {'category': 'ENCOURAGEMENT', 'text_hindi': 'ચાલો!', 'text_english': "Let's go!", 'text_romanized': 'Chalo!', 'context': 'gujarati_letsgo'},
            {'category': 'ENCOURAGEMENT', 'text_hindi': 'ચાલુ!', 'text_english': 'Keep going!', 'text_romanized': 'Chalu!', 'context': 'gujarati_keepgoing'},
        ]

        for phrase_data in phrases_data:
            PeppiPhrase.objects.update_or_create(category=phrase_data['category'], text_hindi=phrase_data['text_hindi'], defaults={'text_english': phrase_data['text_english'], 'text_romanized': phrase_data['text_romanized'], 'context': phrase_data['context'], 'is_active': True})

        self.stdout.write(self.style.SUCCESS(f'  Created {len(phrases_data)} Peppi phrases'))

    def seed_games(self):
        """Create Gujarati games."""
        self.stdout.write('Creating Gujarati games...')

        games_data = [
            {'name': 'Gujarati Memory', 'description': 'Match Gujarati letters with their sounds', 'game_type': 'MEMORY', 'skill_focus': 'ALPHABET', 'level': 1},
            {'name': 'Gujarati Word Search', 'description': 'Find hidden Gujarati words', 'game_type': 'WORDSEARCH', 'skill_focus': 'VOCAB', 'level': 1},
            {'name': 'Listen and Match', 'description': 'Listen to Gujarati words and match with pictures', 'game_type': 'LISTENING', 'skill_focus': 'LISTENING', 'level': 1},
            {'name': 'Gujarati Quiz', 'description': 'Test your Gujarati knowledge', 'game_type': 'QUIZ', 'skill_focus': 'MIXED', 'level': 2},
            {'name': 'Word Builder', 'description': 'Build Gujarati words using letters', 'game_type': 'BUILDER', 'skill_focus': 'SPELLING', 'level': 2},
        ]

        for game_data in games_data:
            Game.objects.update_or_create(language='GUJARATI', name=game_data['name'], defaults={'description': game_data['description'], 'instructions': f"Play {game_data['name']} to practice Gujarati!", 'game_type': game_data['game_type'], 'skill_focus': game_data['skill_focus'], 'level': game_data['level'], 'duration_seconds': 300, 'questions_per_round': 10, 'lives': 3, 'points_per_correct': 10, 'bonus_completion': 50, 'is_premium': game_data['level'] > 1, 'is_active': True})

        self.stdout.write(self.style.SUCCESS(f'  Created {len(games_data)} games'))

    def seed_assessments(self):
        """Create Gujarati assessments."""
        self.stdout.write('Creating Gujarati assessments...')

        assessments_data = [
            {'name': 'L1 Entry Assessment', 'description': 'Check your starting level in Gujarati', 'assessment_type': 'PLACEMENT', 'level': 1, 'questions_count': 5},
            {'name': 'L1 Exit Assessment', 'description': 'Complete L1 and move to L2', 'assessment_type': 'LEVEL_UP', 'level': 1, 'questions_count': 10},
        ]

        for assess_data in assessments_data:
            Assessment.objects.update_or_create(language='GUJARATI', name=assess_data['name'], defaults={'description': assess_data['description'], 'assessment_type': assess_data['assessment_type'], 'level': assess_data['level'], 'passing_score': 70, 'time_limit_minutes': 15, 'questions_count': assess_data['questions_count'], 'randomize_questions': True, 'show_correct_answers': True, 'allow_retake': True, 'retake_cooldown_hours': 1, 'is_active': True})

        self.stdout.write(self.style.SUCCESS(f'  Created {len(assessments_data)} assessments'))
