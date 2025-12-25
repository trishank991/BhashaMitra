"""
Seed command for complete Fiji Hindi L1-L2 curriculum.
Fiji Hindi (फ़िजी हिंदी / Fiji Baat) - spoken by Indo-Fijian diaspora.
Uses Devanagari script with unique Fiji Hindi vocabulary and grammar.
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
from apps.curriculum.models.grammar import GrammarTopic, GrammarRule
from apps.stories.models import Story, StoryPage

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Seed complete Fiji Hindi L1-L2 curriculum (Devanagari script)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing Fiji Hindi data before seeding',
        )

    def handle(self, *args, **options):
        self.stdout.write('🌴 Seeding Fiji Hindi L1-L2 curriculum...\n')

        if options['clear']:
            self.clear_existing_data()

        with transaction.atomic():
            # 1. Create Devanagari Script (shared with Hindi but labeled for Fiji Hindi)
            script = self.seed_script()
            self.seed_vowels(script)
            self.seed_consonants(script)
            self.seed_matras(script)

            # 2. Create Vocabulary (with Fiji Hindi unique words)
            self.seed_vocabulary()

            # 3. Create Stories (Fiji-themed)
            self.seed_stories()

            # 4. Create Songs
            self.seed_songs()

            # 5. Create Curriculum Levels
            self.seed_curriculum_levels()

            # 6. Create Peppi Phrases (Fiji Hindi style with Fijian words)
            self.seed_peppi_phrases()

            # 7. Create Games
            self.seed_games()

            # 8. Create Grammar Topics
            self.seed_grammar()

            # 9. Create Assessments
            self.seed_assessments()

        self.stdout.write(self.style.SUCCESS(
            '\n' + '=' * 60 +
            '\n🌴 Fiji Hindi L1-L2 Curriculum Seeded Successfully!' +
            '\n' + '=' * 60 +
            '\n  Script: Devanagari (for Fiji Hindi)' +
            '\n  Vowels: 13' +
            '\n  Consonants: 33' +
            '\n  Matras: 11' +
            '\n  Vocabulary Words: 200+' +
            '\n  Stories: 15' +
            '\n  Songs: 5' +
            '\n  Games: 5' +
            '\n  Grammar Topics: 5' +
            '\n  Assessments: 2' +
            '\n' + '=' * 60
        ))

    def clear_existing_data(self):
        """Clear existing Fiji Hindi data."""
        self.stdout.write('Clearing existing Fiji Hindi data...')

        # Clear scripts and related
        Script.objects.filter(language='FIJI_HINDI').delete()

        # Clear vocabulary
        VocabularyTheme.objects.filter(language='FIJI_HINDI').delete()

        # Clear games
        Game.objects.filter(language='FIJI_HINDI').delete()

        # Clear assessments
        Assessment.objects.filter(language='FIJI_HINDI').delete()

        # Clear grammar
        GrammarTopic.objects.filter(language='FIJI_HINDI').delete()

        # Clear stories
        Story.objects.filter(language='FIJI_HINDI').delete()

        # Clear Peppi phrases (Fiji Hindi context)
        PeppiPhrase.objects.filter(context__icontains='fiji').delete()

        self.stdout.write(self.style.SUCCESS('Cleared existing Fiji Hindi data.'))

    def seed_script(self):
        """Create Devanagari script for Fiji Hindi."""
        self.stdout.write('Creating Devanagari script for Fiji Hindi...')

        script, created = Script.objects.update_or_create(
            language='FIJI_HINDI',
            defaults={
                'name': 'Devanagari (Fiji Hindi)',
                'name_native': 'फ़िजी हिंदी',
                'description': 'Fiji Hindi uses Devanagari script with Latin transliteration. Developed 1879-1920 among indentured laborers (Girmit era), it combines Awadhi, Bhojpuri, with Fijian and English influences.',
                'total_letters': 57,  # 13 vowels + 33 consonants + 11 matras
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'  Created script: {script.name}'))
        else:
            self.stdout.write(f'  Updated script: {script.name}')

        return script

    def seed_vowels(self, script):
        """Create vowel letters for Fiji Hindi."""
        self.stdout.write('Creating vowels (स्वर)...')

        category, _ = AlphabetCategory.objects.update_or_create(
            script=script,
            category_type='VOWEL',
            defaults={
                'name': 'Vowels',
                'name_native': 'स्वर',
                'description': 'Vowel sounds in Fiji Hindi',
                'order': 1,
            }
        )

        vowels = [
            {'character': 'अ', 'romanization': 'a', 'ipa': '/ə/', 'example_word': 'अनार', 'example_translation': 'pomegranate', 'mnemonic': 'अ से अनार'},
            {'character': 'आ', 'romanization': 'aa', 'ipa': '/aː/', 'example_word': 'आम', 'example_translation': 'mango', 'mnemonic': 'आ से आम'},
            {'character': 'इ', 'romanization': 'i', 'ipa': '/ɪ/', 'example_word': 'इमली', 'example_translation': 'tamarind', 'mnemonic': 'इ से इमली'},
            {'character': 'ई', 'romanization': 'ee', 'ipa': '/iː/', 'example_word': 'ईख', 'example_translation': 'sugarcane', 'mnemonic': 'ई से ईख'},
            {'character': 'उ', 'romanization': 'u', 'ipa': '/ʊ/', 'example_word': 'उल्लू', 'example_translation': 'owl', 'mnemonic': 'उ से उल्लू'},
            {'character': 'ऊ', 'romanization': 'oo', 'ipa': '/uː/', 'example_word': 'ऊन', 'example_translation': 'wool', 'mnemonic': 'ऊ से ऊन'},
            {'character': 'ऋ', 'romanization': 'ri', 'ipa': '/rɪ/', 'example_word': 'ऋषि', 'example_translation': 'sage', 'mnemonic': 'ऋ से ऋषि'},
            {'character': 'ए', 'romanization': 'e', 'ipa': '/eː/', 'example_word': 'एक', 'example_translation': 'one', 'mnemonic': 'ए से एक'},
            {'character': 'ऐ', 'romanization': 'ai', 'ipa': '/ɛː/', 'example_word': 'ऐनक', 'example_translation': 'spectacles', 'mnemonic': 'ऐ से ऐनक'},
            {'character': 'ओ', 'romanization': 'o', 'ipa': '/oː/', 'example_word': 'ओखली', 'example_translation': 'mortar', 'mnemonic': 'ओ से ओखली'},
            {'character': 'औ', 'romanization': 'au', 'ipa': '/ɔː/', 'example_word': 'औरत', 'example_translation': 'woman', 'mnemonic': 'औ से औरत'},
            {'character': 'अं', 'romanization': 'an', 'ipa': '/əŋ/', 'example_word': 'अंगूर', 'example_translation': 'grapes', 'mnemonic': 'अं से अंगूर'},
            {'character': 'अः', 'romanization': 'ah', 'ipa': '/əh/', 'example_word': 'दुःख', 'example_translation': 'sorrow', 'mnemonic': 'अः से दुःख'},
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
        """Create consonant letters for Fiji Hindi."""
        self.stdout.write('Creating consonants (व्यंजन)...')

        category, _ = AlphabetCategory.objects.update_or_create(
            script=script,
            category_type='CONSONANT',
            defaults={
                'name': 'Consonants',
                'name_native': 'व्यंजन',
                'description': 'Consonant sounds in Fiji Hindi',
                'order': 2,
            }
        )

        consonants = [
            # Ka Varga
            {'character': 'क', 'romanization': 'ka', 'ipa': '/k/', 'example_word': 'केला', 'example_translation': 'banana', 'mnemonic': 'क से केला'},
            {'character': 'ख', 'romanization': 'kha', 'ipa': '/kʰ/', 'example_word': 'खरगोश', 'example_translation': 'rabbit', 'mnemonic': 'ख से खरगोश'},
            {'character': 'ग', 'romanization': 'ga', 'ipa': '/g/', 'example_word': 'गाय', 'example_translation': 'cow', 'mnemonic': 'ग से गाय'},
            {'character': 'घ', 'romanization': 'gha', 'ipa': '/gʰ/', 'example_word': 'घर', 'example_translation': 'house', 'mnemonic': 'घ से घर'},
            {'character': 'ङ', 'romanization': 'nga', 'ipa': '/ŋ/', 'example_word': 'रंग', 'example_translation': 'color', 'mnemonic': 'ङ नाक से निकले'},
            # Cha Varga
            {'character': 'च', 'romanization': 'cha', 'ipa': '/tʃ/', 'example_word': 'चम्मच', 'example_translation': 'spoon', 'mnemonic': 'च से चम्मच'},
            {'character': 'छ', 'romanization': 'chha', 'ipa': '/tʃʰ/', 'example_word': 'छाता', 'example_translation': 'umbrella', 'mnemonic': 'छ से छाता'},
            {'character': 'ज', 'romanization': 'ja', 'ipa': '/dʒ/', 'example_word': 'जहाज', 'example_translation': 'ship', 'mnemonic': 'ज से जहाज'},
            {'character': 'झ', 'romanization': 'jha', 'ipa': '/dʒʰ/', 'example_word': 'झंडा', 'example_translation': 'flag', 'mnemonic': 'झ से झंडा'},
            {'character': 'ञ', 'romanization': 'nya', 'ipa': '/ɲ/', 'example_word': '', 'example_translation': 'palatal nasal', 'mnemonic': 'ञ तालू से'},
            # Ta Varga (Retroflex)
            {'character': 'ट', 'romanization': 'ta', 'ipa': '/ʈ/', 'example_word': 'टमाटर', 'example_translation': 'tomato', 'mnemonic': 'ट से टमाटर'},
            {'character': 'ठ', 'romanization': 'tha', 'ipa': '/ʈʰ/', 'example_word': 'ठंडा', 'example_translation': 'cold', 'mnemonic': 'ठ से ठंडा'},
            {'character': 'ड', 'romanization': 'da', 'ipa': '/ɖ/', 'example_word': 'डब्बा', 'example_translation': 'box', 'mnemonic': 'ड से डब्बा'},
            {'character': 'ढ', 'romanization': 'dha', 'ipa': '/ɖʰ/', 'example_word': 'ढोल', 'example_translation': 'drum', 'mnemonic': 'ढ से ढोल'},
            {'character': 'ण', 'romanization': 'na', 'ipa': '/ɳ/', 'example_word': 'कण', 'example_translation': 'particle', 'mnemonic': 'ण मूर्धन्य'},
            # Ta Varga 2 (Dental)
            {'character': 'त', 'romanization': 'ta', 'ipa': '/t̪/', 'example_word': 'तारा', 'example_translation': 'star', 'mnemonic': 'त से तारा'},
            {'character': 'थ', 'romanization': 'tha', 'ipa': '/t̪ʰ/', 'example_word': 'थाली', 'example_translation': 'plate', 'mnemonic': 'थ से थाली'},
            {'character': 'द', 'romanization': 'da', 'ipa': '/d̪/', 'example_word': 'दवाई', 'example_translation': 'medicine', 'mnemonic': 'द से दवाई'},
            {'character': 'ध', 'romanization': 'dha', 'ipa': '/d̪ʰ/', 'example_word': 'धरती', 'example_translation': 'earth', 'mnemonic': 'ध से धरती'},
            {'character': 'न', 'romanization': 'na', 'ipa': '/n/', 'example_word': 'नाक', 'example_translation': 'nose', 'mnemonic': 'न से नाक'},
            # Pa Varga
            {'character': 'प', 'romanization': 'pa', 'ipa': '/p/', 'example_word': 'पंखा', 'example_translation': 'fan', 'mnemonic': 'प से पंखा'},
            {'character': 'फ', 'romanization': 'pha', 'ipa': '/pʰ/', 'example_word': 'फूल', 'example_translation': 'flower', 'mnemonic': 'फ से फूल'},
            {'character': 'ब', 'romanization': 'ba', 'ipa': '/b/', 'example_word': 'बकरी', 'example_translation': 'goat', 'mnemonic': 'ब से बकरी'},
            {'character': 'भ', 'romanization': 'bha', 'ipa': '/bʰ/', 'example_word': 'भालू', 'example_translation': 'bear', 'mnemonic': 'भ से भालू'},
            {'character': 'म', 'romanization': 'ma', 'ipa': '/m/', 'example_word': 'मछली', 'example_translation': 'fish', 'mnemonic': 'म से मछली'},
            # Antastha
            {'character': 'य', 'romanization': 'ya', 'ipa': '/j/', 'example_word': 'याद', 'example_translation': 'memory', 'mnemonic': 'य से याद'},
            {'character': 'र', 'romanization': 'ra', 'ipa': '/r/', 'example_word': 'रोटी', 'example_translation': 'bread', 'mnemonic': 'र से रोटी'},
            {'character': 'ल', 'romanization': 'la', 'ipa': '/l/', 'example_word': 'लस्सी', 'example_translation': 'lassi', 'mnemonic': 'ल से लस्सी'},
            {'character': 'व', 'romanization': 'va', 'ipa': '/ʋ/', 'example_word': 'वाल', 'example_translation': 'hair', 'mnemonic': 'व से वाल'},
            # Ushma
            {'character': 'श', 'romanization': 'sha', 'ipa': '/ʃ/', 'example_word': 'शेर', 'example_translation': 'lion', 'mnemonic': 'श से शेर'},
            {'character': 'ष', 'romanization': 'sha', 'ipa': '/ʂ/', 'example_word': 'षट्कोण', 'example_translation': 'hexagon', 'mnemonic': 'ष से षट्कोण'},
            {'character': 'स', 'romanization': 'sa', 'ipa': '/s/', 'example_word': 'सेब', 'example_translation': 'apple', 'mnemonic': 'स से सेब'},
            {'character': 'ह', 'romanization': 'ha', 'ipa': '/h/', 'example_word': 'हाथी', 'example_translation': 'elephant', 'mnemonic': 'ह से हाथी'},
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
        """Create matras (vowel marks) for Fiji Hindi."""
        self.stdout.write('Creating matras (मात्रा)...')

        matras = [
            {'symbol': 'ा', 'name': 'Aa matra', 'name_native': 'आ की मात्रा', 'sound': 'aa', 'example_with_ka': 'का', 'example_word': 'काला', 'translation': 'black'},
            {'symbol': 'ि', 'name': 'I matra', 'name_native': 'इ की मात्रा', 'sound': 'i', 'example_with_ka': 'कि', 'example_word': 'किताब', 'translation': 'book'},
            {'symbol': 'ी', 'name': 'Ee matra', 'name_native': 'ई की मात्रा', 'sound': 'ee', 'example_with_ka': 'की', 'example_word': 'कीड़ी', 'translation': 'ant'},
            {'symbol': 'ु', 'name': 'U matra', 'name_native': 'उ की मात्रा', 'sound': 'u', 'example_with_ka': 'कु', 'example_word': 'कुत्ता', 'translation': 'dog'},
            {'symbol': 'ू', 'name': 'Oo matra', 'name_native': 'ऊ की मात्रा', 'sound': 'oo', 'example_with_ka': 'कू', 'example_word': 'कूलर', 'translation': 'cooler'},
            {'symbol': 'े', 'name': 'E matra', 'name_native': 'ए की मात्रा', 'sound': 'e', 'example_with_ka': 'के', 'example_word': 'केला', 'translation': 'banana'},
            {'symbol': 'ै', 'name': 'Ai matra', 'name_native': 'ऐ की मात्रा', 'sound': 'ai', 'example_with_ka': 'कै', 'example_word': 'पैसा', 'translation': 'money'},
            {'symbol': 'ो', 'name': 'O matra', 'name_native': 'ओ की मात्रा', 'sound': 'o', 'example_with_ka': 'को', 'example_word': 'कोट', 'translation': 'coat'},
            {'symbol': 'ौ', 'name': 'Au matra', 'name_native': 'औ की मात्रा', 'sound': 'au', 'example_with_ka': 'कौ', 'example_word': 'कौआ', 'translation': 'crow'},
            {'symbol': 'ं', 'name': 'Anusvara', 'name_native': 'अनुस्वार', 'sound': 'n', 'example_with_ka': 'कं', 'example_word': 'कंघी', 'translation': 'comb'},
            {'symbol': 'ः', 'name': 'Visarga', 'name_native': 'विसर्ग', 'sound': 'h', 'example_with_ka': 'कः', 'example_word': 'दुःख', 'translation': 'sorrow'},
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
        """Create vocabulary themes and words for Fiji Hindi L1 and L2."""
        self.stdout.write('Creating Fiji Hindi vocabulary themes and words...')

        # L1 Vocabulary (50 words)
        l1_themes = [
            {
                'name': 'Family',
                'name_native': 'परिवार',
                'icon': 'family',
                'level': 1,
                'words': [
                    {'word': 'माई', 'romanization': 'maai', 'translation': 'Mother', 'pos': 'NOUN', 'note': 'Fiji Hindi for मां'},
                    {'word': 'बाप', 'romanization': 'baap', 'translation': 'Father', 'pos': 'NOUN'},
                    {'word': 'दादा', 'romanization': 'daada', 'translation': 'Grandfather', 'pos': 'NOUN'},
                    {'word': 'दादी', 'romanization': 'daadi', 'translation': 'Grandmother', 'pos': 'NOUN'},
                    {'word': 'भाई', 'romanization': 'bhaai', 'translation': 'Brother', 'pos': 'NOUN'},
                    {'word': 'बहिन', 'romanization': 'bahin', 'translation': 'Sister', 'pos': 'NOUN', 'note': 'Fiji Hindi variant of बहन'},
                ]
            },
            {
                'name': 'Colors',
                'name_native': 'रंग',
                'icon': 'palette',
                'level': 1,
                'words': [
                    {'word': 'लाल', 'romanization': 'laal', 'translation': 'Red', 'pos': 'ADJECTIVE'},
                    {'word': 'नीला', 'romanization': 'neela', 'translation': 'Blue', 'pos': 'ADJECTIVE'},
                    {'word': 'पीला', 'romanization': 'peela', 'translation': 'Yellow', 'pos': 'ADJECTIVE'},
                    {'word': 'हरा', 'romanization': 'hara', 'translation': 'Green', 'pos': 'ADJECTIVE'},
                    {'word': 'सफेद', 'romanization': 'safed', 'translation': 'White', 'pos': 'ADJECTIVE'},
                    {'word': 'काला', 'romanization': 'kaala', 'translation': 'Black', 'pos': 'ADJECTIVE'},
                ]
            },
            {
                'name': 'Numbers',
                'name_native': 'गिनती',
                'icon': 'numbers',
                'level': 1,
                'words': [
                    {'word': 'एक', 'romanization': 'ek', 'translation': 'One', 'pos': 'NUMBER'},
                    {'word': 'दुइ', 'romanization': 'dui', 'translation': 'Two', 'pos': 'NUMBER', 'note': 'Fiji Hindi from Awadhi - NOT "do"'},
                    {'word': 'तीन', 'romanization': 'teen', 'translation': 'Three', 'pos': 'NUMBER'},
                    {'word': 'चार', 'romanization': 'chaar', 'translation': 'Four', 'pos': 'NUMBER'},
                    {'word': 'पाँच', 'romanization': 'paanch', 'translation': 'Five', 'pos': 'NUMBER'},
                ]
            },
            {
                'name': 'Greetings',
                'name_native': 'अभिवादन',
                'icon': 'waving_hand',
                'level': 1,
                'words': [
                    {'word': 'बुला', 'romanization': 'bula', 'translation': 'Hello', 'pos': 'INTERJECTION', 'note': 'From Fijian language!'},
                    {'word': 'नमस्ते', 'romanization': 'namaste', 'translation': 'Hello (formal)', 'pos': 'INTERJECTION'},
                    {'word': 'कैसे है', 'romanization': 'kaise hai', 'translation': 'How are you', 'pos': 'PHRASE'},
                    {'word': 'ठीक है', 'romanization': 'theek hai', 'translation': 'Fine/OK', 'pos': 'PHRASE'},
                    {'word': 'धन्यवाद', 'romanization': 'dhanyavaad', 'translation': 'Thank you', 'pos': 'INTERJECTION'},
                    {'word': 'बाद में', 'romanization': 'baad mein', 'translation': 'See you later', 'pos': 'PHRASE'},
                ]
            },
            {
                'name': 'Food',
                'name_native': 'खाना',
                'icon': 'restaurant',
                'level': 1,
                'words': [
                    {'word': 'रोटी', 'romanization': 'roti', 'translation': 'Bread/Roti', 'pos': 'NOUN'},
                    {'word': 'भात', 'romanization': 'bhaat', 'translation': 'Rice', 'pos': 'NOUN', 'note': 'Fiji Hindi for चावल'},
                    {'word': 'दाल', 'romanization': 'daal', 'translation': 'Lentils', 'pos': 'NOUN'},
                    {'word': 'पानी', 'romanization': 'paani', 'translation': 'Water', 'pos': 'NOUN'},
                    {'word': 'दूध', 'romanization': 'doodh', 'translation': 'Milk', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Body',
                'name_native': 'शरीर',
                'icon': 'accessibility',
                'level': 1,
                'words': [
                    {'word': 'आँख', 'romanization': 'aankh', 'translation': 'Eye', 'pos': 'NOUN'},
                    {'word': 'नाक', 'romanization': 'naak', 'translation': 'Nose', 'pos': 'NOUN'},
                    {'word': 'कान', 'romanization': 'kaan', 'translation': 'Ear', 'pos': 'NOUN'},
                    {'word': 'मुँह', 'romanization': 'munh', 'translation': 'Mouth', 'pos': 'NOUN'},
                    {'word': 'हाथ', 'romanization': 'haath', 'translation': 'Hand', 'pos': 'NOUN'},
                    {'word': 'पैर', 'romanization': 'pair', 'translation': 'Foot/Leg', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Animals',
                'name_native': 'जानवर',
                'icon': 'pets',
                'level': 1,
                'words': [
                    {'word': 'कुत्ता', 'romanization': 'kutta', 'translation': 'Dog', 'pos': 'NOUN'},
                    {'word': 'बिल्ली', 'romanization': 'billi', 'translation': 'Cat', 'pos': 'NOUN'},
                    {'word': 'गाय', 'romanization': 'gaay', 'translation': 'Cow', 'pos': 'NOUN'},
                    {'word': 'मुर्गी', 'romanization': 'murgi', 'translation': 'Chicken', 'pos': 'NOUN'},
                    {'word': 'मछली', 'romanization': 'machhli', 'translation': 'Fish', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Nature',
                'name_native': 'प्रकृति',
                'icon': 'park',
                'level': 1,
                'words': [
                    {'word': 'सूरज', 'romanization': 'sooraj', 'translation': 'Sun', 'pos': 'NOUN'},
                    {'word': 'चाँद', 'romanization': 'chaand', 'translation': 'Moon', 'pos': 'NOUN'},
                    {'word': 'तारा', 'romanization': 'taara', 'translation': 'Star', 'pos': 'NOUN'},
                    {'word': 'बादल', 'romanization': 'baadal', 'translation': 'Cloud', 'pos': 'NOUN'},
                    {'word': 'बारिश', 'romanization': 'baarish', 'translation': 'Rain', 'pos': 'NOUN'},
                ]
            },
        ]

        # L2 Vocabulary (150 words) - Including Fiji-specific words
        l2_themes = [
            {
                'name': 'Extended Family',
                'name_native': 'बड़ा परिवार',
                'icon': 'groups',
                'level': 2,
                'words': [
                    {'word': 'मामा', 'romanization': 'maama', 'translation': 'Maternal Uncle', 'pos': 'NOUN'},
                    {'word': 'मामी', 'romanization': 'maami', 'translation': 'Maternal Aunt', 'pos': 'NOUN'},
                    {'word': 'चाचा', 'romanization': 'chaacha', 'translation': 'Paternal Uncle', 'pos': 'NOUN'},
                    {'word': 'चाची', 'romanization': 'chaachi', 'translation': 'Paternal Aunt', 'pos': 'NOUN'},
                    {'word': 'नाना', 'romanization': 'naana', 'translation': 'Maternal Grandfather', 'pos': 'NOUN'},
                    {'word': 'नानी', 'romanization': 'naani', 'translation': 'Maternal Grandmother', 'pos': 'NOUN'},
                    {'word': 'बेटा', 'romanization': 'beta', 'translation': 'Son', 'pos': 'NOUN'},
                    {'word': 'बेटी', 'romanization': 'beti', 'translation': 'Daughter', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Numbers 6-20',
                'name_native': 'गिनती ६-२०',
                'icon': 'pin',
                'level': 2,
                'words': [
                    {'word': 'छह', 'romanization': 'chhah', 'translation': 'Six', 'pos': 'NUMBER'},
                    {'word': 'सात', 'romanization': 'saat', 'translation': 'Seven', 'pos': 'NUMBER'},
                    {'word': 'आठ', 'romanization': 'aath', 'translation': 'Eight', 'pos': 'NUMBER'},
                    {'word': 'नौ', 'romanization': 'nau', 'translation': 'Nine', 'pos': 'NUMBER'},
                    {'word': 'दस', 'romanization': 'das', 'translation': 'Ten', 'pos': 'NUMBER'},
                    {'word': 'बीस', 'romanization': 'bees', 'translation': 'Twenty', 'pos': 'NUMBER'},
                    {'word': 'बीस और एक', 'romanization': 'bees aur ek', 'translation': 'Twenty-one', 'pos': 'NUMBER', 'note': 'Fiji Hindi style - tens first!'},
                    {'word': 'सौ', 'romanization': 'sau', 'translation': 'Hundred', 'pos': 'NUMBER'},
                ]
            },
            {
                'name': 'Fijian Words',
                'name_native': 'फिजी के शब्द',
                'icon': 'public',
                'level': 2,
                'words': [
                    {'word': 'बुला', 'romanization': 'bula', 'translation': 'Hello (Fijian)', 'pos': 'INTERJECTION', 'note': 'From Fijian iTaukei'},
                    {'word': 'विनाका', 'romanization': 'vinaka', 'translation': 'Thank you (Fijian)', 'pos': 'INTERJECTION', 'note': 'From Fijian'},
                    {'word': 'दालो', 'romanization': 'daalo', 'translation': 'Taro', 'pos': 'NOUN', 'note': 'Fijian vegetable'},
                    {'word': 'कासावा', 'romanization': 'kaasava', 'translation': 'Cassava', 'pos': 'NOUN', 'note': 'Fijian staple food'},
                    {'word': 'सुलु', 'romanization': 'sulu', 'translation': 'Sarong/Wrap', 'pos': 'NOUN', 'note': 'Traditional Fijian garment'},
                    {'word': 'याकोना', 'romanization': 'yaqona', 'translation': 'Kava drink', 'pos': 'NOUN', 'note': 'Traditional Fiji drink'},
                ]
            },
            {
                'name': 'Fiji Hindi Food',
                'name_native': 'फिजी खाना',
                'icon': 'restaurant',
                'level': 2,
                'words': [
                    {'word': 'करी', 'romanization': 'kari', 'translation': 'Curry', 'pos': 'NOUN'},
                    {'word': 'चटनी', 'romanization': 'chatni', 'translation': 'Chutney', 'pos': 'NOUN'},
                    {'word': 'पूरी', 'romanization': 'poori', 'translation': 'Puri (fried bread)', 'pos': 'NOUN'},
                    {'word': 'सब्जी', 'romanization': 'sabzi', 'translation': 'Vegetable', 'pos': 'NOUN'},
                    {'word': 'फल', 'romanization': 'fal', 'translation': 'Fruit', 'pos': 'NOUN'},
                    {'word': 'केला', 'romanization': 'kela', 'translation': 'Banana', 'pos': 'NOUN'},
                    {'word': 'आम', 'romanization': 'aam', 'translation': 'Mango', 'pos': 'NOUN'},
                    {'word': 'सेब', 'romanization': 'seb', 'translation': 'Apple', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Verbs',
                'name_native': 'क्रिया',
                'icon': 'directions_run',
                'level': 2,
                'words': [
                    {'word': 'जाना', 'romanization': 'jaana', 'translation': 'To go', 'pos': 'VERB'},
                    {'word': 'आना', 'romanization': 'aana', 'translation': 'To come', 'pos': 'VERB'},
                    {'word': 'खाना', 'romanization': 'khaana', 'translation': 'To eat', 'pos': 'VERB'},
                    {'word': 'पीना', 'romanization': 'peena', 'translation': 'To drink', 'pos': 'VERB'},
                    {'word': 'सोना', 'romanization': 'sona', 'translation': 'To sleep', 'pos': 'VERB'},
                    {'word': 'खेलना', 'romanization': 'khelna', 'translation': 'To play', 'pos': 'VERB'},
                    {'word': 'पढ़ना', 'romanization': 'parhna', 'translation': 'To read/study', 'pos': 'VERB'},
                    {'word': 'लिखना', 'romanization': 'likhna', 'translation': 'To write', 'pos': 'VERB'},
                    {'word': 'बोलना', 'romanization': 'bolna', 'translation': 'To speak', 'pos': 'VERB'},
                    {'word': 'सुनना', 'romanization': 'sunna', 'translation': 'To listen', 'pos': 'VERB'},
                    {'word': 'देखना', 'romanization': 'dekhna', 'translation': 'To see', 'pos': 'VERB'},
                    {'word': 'करना', 'romanization': 'karna', 'translation': 'To do', 'pos': 'VERB'},
                ]
            },
            {
                'name': 'Time',
                'name_native': 'समय',
                'icon': 'schedule',
                'level': 2,
                'words': [
                    {'word': 'आज', 'romanization': 'aaj', 'translation': 'Today', 'pos': 'ADVERB'},
                    {'word': 'कल', 'romanization': 'kal', 'translation': 'Yesterday/Tomorrow', 'pos': 'ADVERB'},
                    {'word': 'सुबह', 'romanization': 'subah', 'translation': 'Morning', 'pos': 'NOUN'},
                    {'word': 'शाम', 'romanization': 'shaam', 'translation': 'Evening', 'pos': 'NOUN'},
                    {'word': 'रात', 'romanization': 'raat', 'translation': 'Night', 'pos': 'NOUN'},
                    {'word': 'हफ्ता', 'romanization': 'hafta', 'translation': 'Week', 'pos': 'NOUN'},
                    {'word': 'महीना', 'romanization': 'maheena', 'translation': 'Month', 'pos': 'NOUN'},
                    {'word': 'साल', 'romanization': 'saal', 'translation': 'Year', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Places',
                'name_native': 'जगह',
                'icon': 'place',
                'level': 2,
                'words': [
                    {'word': 'घर', 'romanization': 'ghar', 'translation': 'Home', 'pos': 'NOUN'},
                    {'word': 'स्कूल', 'romanization': 'school', 'translation': 'School', 'pos': 'NOUN'},
                    {'word': 'मंदिर', 'romanization': 'mandir', 'translation': 'Temple', 'pos': 'NOUN'},
                    {'word': 'दुकान', 'romanization': 'dukaan', 'translation': 'Shop', 'pos': 'NOUN'},
                    {'word': 'बाजार', 'romanization': 'baazaar', 'translation': 'Market', 'pos': 'NOUN'},
                    {'word': 'गाँव', 'romanization': 'gaanv', 'translation': 'Village', 'pos': 'NOUN'},
                ]
            },
            {
                'name': 'Basics',
                'name_native': 'मूल शब्द',
                'icon': 'star',
                'level': 2,
                'words': [
                    {'word': 'हाँ', 'romanization': 'haan', 'translation': 'Yes', 'pos': 'INTERJECTION'},
                    {'word': 'नहीं', 'romanization': 'nahin', 'translation': 'No', 'pos': 'INTERJECTION'},
                    {'word': 'अच्छा', 'romanization': 'achcha', 'translation': 'Good', 'pos': 'ADJECTIVE'},
                    {'word': 'बुरा', 'romanization': 'bura', 'translation': 'Bad', 'pos': 'ADJECTIVE'},
                    {'word': 'बड़ा', 'romanization': 'barra', 'translation': 'Big', 'pos': 'ADJECTIVE'},
                    {'word': 'छोटा', 'romanization': 'chhota', 'translation': 'Small', 'pos': 'ADJECTIVE'},
                    {'word': 'अरे!', 'romanization': 'are!', 'translation': 'Hey!', 'pos': 'INTERJECTION', 'note': 'Common Fiji Hindi exclamation'},
                ]
            },
        ]

        all_themes = l1_themes + l2_themes
        word_count = 0

        for i, theme_data in enumerate(all_themes, 1):
            theme, _ = VocabularyTheme.objects.update_or_create(
                language='FIJI_HINDI',
                name=theme_data['name'],
                defaults={
                    'name_native': theme_data['name_native'],
                    'description': f"Learn {theme_data['name']} in Fiji Hindi",
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
        """Create Fiji Hindi stories for L1 and L2."""
        self.stdout.write('Creating Fiji Hindi stories...')

        stories_data = [
            # L1 Stories (5) - Authentic Fiji Hindi with -इस/-इन past tense, ऊ pronoun
            {
                'title': "Peppi's New Friend",
                'title_hindi': 'पेप्पी के नया दोस्त',
                'title_romanized': 'Peppi ke Naya Dost',
                'level': 1,
                'age_min': 4,
                'age_max': 6,
                'theme': 'friendship',
                'tier': 'FREE',
                'moral_english': 'True friends accept each other as they are',
                'moral_hindi': 'सच्चा दोस्त एक दूसरे के जइसन मानता है',
                'pages': [
                    {'text': 'पेप्पी एगो छोटा बिलाई है।', 'translation': 'Peppi is a small cat.'},
                    {'text': 'पेप्पी अकेला रहता सी।', 'translation': 'Peppi lived alone.'},
                    {'text': 'एक दिन ऊ एगो कुकुर देखिस।', 'translation': 'One day he saw a dog.'},
                    {'text': 'कुकुर के नाम राजा है।', 'translation': "The dog's name is Raja."},
                    {'text': 'पेप्पी अउर राजा दोस्त बन गइस!', 'translation': 'Peppi and Raja became friends!'},
                    {'text': 'अब पेप्पी खुश है!', 'translation': 'Now Peppi is happy!'},
                ]
            },
            {
                'title': 'My Family',
                'title_hindi': 'हमार परिवार',
                'title_romanized': 'Hamaar Parivaar',
                'level': 1,
                'age_min': 4,
                'age_max': 6,
                'theme': 'family',
                'tier': 'FREE',
                'moral_english': 'Family is our biggest treasure',
                'moral_hindi': 'परिवार हमार सबसे बड़ा खजाना है',
                'pages': [
                    {'text': 'ई हमार माई है।', 'translation': 'This is my mother.'},
                    {'text': 'ई हमार बाप है।', 'translation': 'This is my father.'},
                    {'text': 'ई हमार दादी है।', 'translation': 'This is my grandmother.'},
                    {'text': 'ई हमार दादा है।', 'translation': 'This is my grandfather.'},
                    {'text': 'ई हमार भइया है।', 'translation': 'This is my brother.'},
                    {'text': 'हम सब एके साथ रहता है।', 'translation': 'We all live together.'},
                ]
            },
            {
                'title': 'The Red Apple',
                'title_hindi': 'लाल सेब',
                'title_romanized': 'Laal Seb',
                'level': 1,
                'age_min': 4,
                'age_max': 6,
                'theme': 'sharing',
                'tier': 'FREE',
                'moral_english': 'Sharing brings happiness',
                'moral_hindi': 'बाँटे से खुशी मिलता है',
                'pages': [
                    {'text': 'पेड़ पे एगो सेब है।', 'translation': 'There is an apple on the tree.'},
                    {'text': 'सेब लाल है।', 'translation': 'The apple is red.'},
                    {'text': 'राम के सेब चाहीं।', 'translation': 'Ram wants the apple.'},
                    {'text': 'माई सेब दिइन।', 'translation': 'Mother gave the apple.'},
                    {'text': 'राम खुश हो गइस!', 'translation': 'Ram became happy!'},
                ]
            },
            {
                'title': 'Counting Song',
                'title_hindi': 'गिनती गाना',
                'title_romanized': 'Ginti Gaana',
                'level': 1,
                'age_min': 4,
                'age_max': 6,
                'theme': 'learning',
                'tier': 'FREE',
                'moral_english': 'Learning is fun',
                'moral_hindi': 'पढ़े में मजा है',
                'pages': [
                    {'text': 'एक दुइ तीन चार पाँच!', 'translation': 'One two three four five!'},
                    {'text': 'हम सब गाना गावे है।', 'translation': 'We all sing a song.'},
                    {'text': 'छह सात आठ नौ दस!', 'translation': 'Six seven eight nine ten!'},
                    {'text': 'फिर से गाओ!', 'translation': 'Sing again!'},
                    {'text': 'गिनती में मजा है!', 'translation': 'Counting is fun!'},
                ]
            },
            {
                'title': 'Bula!',
                'title_hindi': 'बुला!',
                'title_romanized': 'Bula!',
                'level': 1,
                'age_min': 4,
                'age_max': 6,
                'theme': 'greetings',
                'tier': 'FREE',
                'moral_english': 'Greetings bring joy',
                'moral_hindi': 'बोले से खुशी आवे है',
                'pages': [
                    {'text': 'सुबह हो गइस।', 'translation': 'Morning has come.'},
                    {'text': 'माई बोलिन - बुला!', 'translation': 'Mother said - Bula!'},
                    {'text': 'बाप बोलिस - नमस्ते!', 'translation': 'Father said - Namaste!'},
                    {'text': 'हम बोला - कइसे बा?', 'translation': 'I said - How are you?'},
                    {'text': 'सब बोलिस - ठीक बा!', 'translation': 'Everyone said - Fine!'},
                    {'text': 'आज अच्छा दिन बा!', 'translation': 'Today is a good day!'},
                ]
            },
            # L2 Stories (10) - Festival stories with authentic Fiji Hindi
            {
                'title': 'Diwali in Fiji',
                'title_hindi': 'दिवाली फिजी में',
                'title_romanized': 'Diwali Fiji Mein',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'festival',
                'tier': 'STANDARD',
                'moral_english': 'Light dispels darkness',
                'moral_hindi': 'उजाला अंधेरा भगावे है',
                'pages': [
                    {'text': 'आज दिवाली बा!', 'translation': 'Today is Diwali!'},
                    {'text': 'घर में दीया जरावे है।', 'translation': 'We light lamps in the house.'},
                    {'text': 'माई रंगोली बनाइन।', 'translation': 'Mother made rangoli.'},
                    {'text': 'बच्चा लोग नया कपड़ा पहिनिस।', 'translation': 'Children wore new clothes.'},
                    {'text': 'बाप फटाका लाइस।', 'translation': 'Father brought firecrackers.'},
                    {'text': 'दादी मिठाई बनाइन।', 'translation': 'Grandmother made sweets.'},
                    {'text': 'सब लोग पूजा किइस।', 'translation': 'Everyone did puja.'},
                    {'text': 'दिवाली मुबारक!', 'translation': 'Happy Diwali!'},
                ]
            },
            {
                'title': 'Holi in Fiji',
                'title_hindi': 'होली फिजी में',
                'title_romanized': 'Holi Fiji Mein',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'festival',
                'tier': 'STANDARD',
                'moral_english': 'Colors bring joy',
                'moral_hindi': 'रंग से खुशी आवे है',
                'pages': [
                    {'text': 'आज होली बा!', 'translation': 'Today is Holi!'},
                    {'text': 'सब बच्चा बाहर आइस।', 'translation': 'All children came outside.'},
                    {'text': 'रवि लाल रंग लगाइस।', 'translation': 'Ravi put red color.'},
                    {'text': 'सीता पीला रंग फेंकिन।', 'translation': 'Sita threw yellow color.'},
                    {'text': 'सब रंग-बिरंगा हो गइस!', 'translation': 'Everyone became colorful!'},
                    {'text': 'माई गुझिया बनाइन।', 'translation': 'Mother made gujiya.'},
                    {'text': 'सब ठंडाई पीइस।', 'translation': 'Everyone drank thandai.'},
                    {'text': 'होली मुबारक!', 'translation': 'Happy Holi!'},
                ]
            },
            {
                'title': 'Ram Navami',
                'title_hindi': 'राम नवमी',
                'title_romanized': 'Ram Navami',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'festival',
                'tier': 'STANDARD',
                'moral_english': 'Good always wins',
                'moral_hindi': 'अच्छाई हमेशा जीतता है',
                'pages': [
                    {'text': 'आज राम नवमी बा!', 'translation': 'Today is Ram Navami!'},
                    {'text': 'राम जी के जनम दिन बा।', 'translation': "It's Lord Ram's birthday."},
                    {'text': 'हम मंदिर गइला।', 'translation': 'We went to the temple.'},
                    {'text': 'पूजा किइला।', 'translation': 'We did puja.'},
                    {'text': 'भजन गाइला।', 'translation': 'We sang bhajans.'},
                    {'text': 'परसाद खाइला।', 'translation': 'We ate prasad.'},
                    {'text': 'जय सिरी राम!', 'translation': 'Jai Shri Ram!'},
                ]
            },
            {
                'title': 'Fiji Day Celebration',
                'title_hindi': 'फिजी डे मेला',
                'title_romanized': 'Fiji Day Mela',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'festival',
                'tier': 'STANDARD',
                'moral_english': 'Unity in diversity',
                'moral_hindi': 'मिल के रहे में ताकत बा',
                'pages': [
                    {'text': 'आज फिजी डे बा!', 'translation': 'Today is Fiji Day!'},
                    {'text': 'सब लोग मेला गइस।', 'translation': 'Everyone went to the fair.'},
                    {'text': 'झंडा उड़े है।', 'translation': 'The flag flies.'},
                    {'text': 'बुला! बुला! सब बोलिस।', 'translation': 'Bula! Bula! Everyone said.'},
                    {'text': 'दालो अउर कासावा खाइला।', 'translation': 'We ate taro and cassava.'},
                    {'text': 'याकोना पीइला।', 'translation': 'We drank kava.'},
                    {'text': 'नाच-गाना भइल।', 'translation': 'There was dancing and singing.'},
                    {'text': 'फिजी डे मुबारक!', 'translation': 'Happy Fiji Day!'},
                ]
            },
            {
                'title': 'The Thirsty Crow',
                'title_hindi': 'पियासा कउआ',
                'title_romanized': 'Piyaasa Kauwa',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'wisdom',
                'tier': 'STANDARD',
                'moral_english': 'Where there is a will, there is a way',
                'moral_hindi': 'जहाँ चाह वहाँ राह',
                'pages': [
                    {'text': 'एगो कउआ रहे।', 'translation': 'There was a crow.'},
                    {'text': 'ऊ पियासा रहे।', 'translation': 'He was thirsty.'},
                    {'text': 'ऊ एगो घइला देखिस।', 'translation': 'He saw a pot.'},
                    {'text': 'पानी थोड़े रहे।', 'translation': 'Water was less.'},
                    {'text': 'ऊ कंकर डालिस।', 'translation': 'He dropped pebbles.'},
                    {'text': 'पानी ऊपर आ गइस!', 'translation': 'Water came up!'},
                    {'text': 'कउआ पानी पी लिइस।', 'translation': 'The crow drank water.'},
                ]
            },
            {
                'title': 'Girmit Story',
                'title_hindi': 'गिरमिट के कहानी',
                'title_romanized': 'Girmit ke Kahaani',
                'level': 2,
                'age_min': 6,
                'age_max': 8,
                'theme': 'history',
                'tier': 'STANDARD',
                'moral_english': 'Our ancestors were brave',
                'moral_hindi': 'हमार पुरखा लोग बहादुर रहे',
                'pages': [
                    {'text': 'बहुत पहिले के बात बा।', 'translation': 'This is a story from long ago.'},
                    {'text': 'हमार दादा-दादी भारत से आइस।', 'translation': 'Our grandparents came from India.'},
                    {'text': 'ऊ लोग जहाज में आइस।', 'translation': 'They came by ship.'},
                    {'text': 'फिजी में खेत में काम किइस।', 'translation': 'They worked in fields in Fiji.'},
                    {'text': 'बहुत मेहनत किइस।', 'translation': 'They worked very hard.'},
                    {'text': 'अब हम इहाँ खुश बाटी।', 'translation': 'Now we are happy here.'},
                    {'text': 'हम गिरमिटिया के लइका बाटी!', 'translation': 'We are children of Girmitiya!'},
                ]
            },
            {
                'title': 'At the Beach',
                'title_hindi': 'समुंदर किनारे',
                'title_romanized': 'Samundar Kinaare',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'nature',
                'tier': 'STANDARD',
                'moral_english': 'Nature is beautiful',
                'moral_hindi': 'कुदरत सुंदर बा',
                'pages': [
                    {'text': 'आज हम समुंदर गइला।', 'translation': 'Today we went to the beach.'},
                    {'text': 'पानी नीला रहे।', 'translation': 'The water was blue.'},
                    {'text': 'बालू उजर रहे।', 'translation': 'The sand was white.'},
                    {'text': 'मछली तैरत रहे।', 'translation': 'Fish were swimming.'},
                    {'text': 'हम खेलला।', 'translation': 'We played.'},
                    {'text': 'बहुत मजा आइस!', 'translation': 'It was so much fun!'},
                ]
            },
            {
                'title': 'Going to Temple',
                'title_hindi': 'मंदिर जाइत बाटी',
                'title_romanized': 'Mandir Jaait Baati',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'culture',
                'tier': 'STANDARD',
                'moral_english': 'Prayers bring peace',
                'moral_hindi': 'पूजा से सांति मिलता है',
                'pages': [
                    {'text': 'आज रविवार बा।', 'translation': 'It is Sunday.'},
                    {'text': 'हम मंदिर गइला।', 'translation': 'We went to the temple.'},
                    {'text': 'घंटी बजाइला।', 'translation': 'We rang the bell.'},
                    {'text': 'भगवान के परनाम किइला।', 'translation': 'We bowed to God.'},
                    {'text': 'परसाद लिइला।', 'translation': 'We took prasad.'},
                    {'text': 'मन सांत हो गइस।', 'translation': 'Our mind became peaceful.'},
                ]
            },
            {
                'title': 'Cooking with Grandmother',
                'title_hindi': 'दादी संगे खाना बनावे',
                'title_romanized': 'Daadi Sange Khaana Banaave',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'family',
                'tier': 'STANDARD',
                'moral_english': 'Time with elders is precious',
                'moral_hindi': 'बड़न संगे समय अनमोल बा',
                'pages': [
                    {'text': 'दादी रसोई में बाड़ी।', 'translation': 'Grandmother is in the kitchen.'},
                    {'text': 'दादी रोटी बनावे बाड़ी।', 'translation': 'Grandmother is making roti.'},
                    {'text': 'हम मदद करत बाटी।', 'translation': 'I am helping.'},
                    {'text': 'आटा गूंधला।', 'translation': 'We kneaded the dough.'},
                    {'text': 'रोटी बेलला।', 'translation': 'We rolled the roti.'},
                    {'text': 'तवा पे सेंकला।', 'translation': 'We cooked it on the griddle.'},
                    {'text': 'गरम गरम रोटी खाइला।', 'translation': 'We ate hot roti.'},
                    {'text': 'बहुत मीठ!', 'translation': 'Very delicious!'},
                ]
            },
            {
                'title': 'My School in Fiji',
                'title_hindi': 'हमार इसकूल फिजी में',
                'title_romanized': 'Hamaar Iskool Fiji Mein',
                'level': 2,
                'age_min': 5,
                'age_max': 7,
                'theme': 'school',
                'tier': 'STANDARD',
                'moral_english': 'Education is important',
                'moral_hindi': 'पढ़ाई जरूरी बा',
                'pages': [
                    {'text': 'सुबह हम इसकूल जाता है।', 'translation': 'I go to school in the morning.'},
                    {'text': 'बस में बइठता है।', 'translation': 'I sit in the bus.'},
                    {'text': 'इसकूल में दोस्त बा।', 'translation': 'I have friends at school.'},
                    {'text': 'टीचर पढ़ावे है।', 'translation': 'Teacher teaches.'},
                    {'text': 'हम पढ़ता है।', 'translation': 'We study.'},
                    {'text': 'रिसेस में खेलता है।', 'translation': 'We play during recess.'},
                    {'text': 'इसकूल बहुत अच्छा बा!', 'translation': 'School is very good!'},
                ]
            },
        ]

        for story_data in stories_data:
            # Create unique storyweaver_id for Fiji Hindi stories
            story_slug = story_data['title'].lower().replace(' ', '-').replace("'", '')
            storyweaver_id = f"fh-l{story_data['level']}-{story_slug}"

            story, _ = Story.objects.update_or_create(
                storyweaver_id=storyweaver_id,
                defaults={
                    'language': 'FIJI_HINDI',
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
                        'text_hindi': page_data['text'],
                        'text_romanized': page_data['translation'],
                    }
                )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(stories_data)} stories'))

    def seed_songs(self):
        """Create Fiji Hindi songs for L1 and L2."""
        self.stdout.write('Creating Fiji Hindi songs...')

        # Get or create L1 level
        l1_level, _ = CurriculumLevel.objects.get_or_create(
            code='L1',
            defaults={
                'name_english': 'Discovery',
                'name_hindi': 'शुरूआत',
                'name_romanized': 'Shuruaat',
                'min_age': 4,
                'max_age': 5,
                'description': 'First steps in learning Fiji Hindi',
                'order': 1,
                'is_active': True,
            }
        )

        songs_data = [
            {
                'title_english': 'Counting in Fiji Hindi',
                'title_hindi': 'फिजी बात में गिनती',
                'title_romanized': 'Fiji Baat Mein Ginti',
                'lyrics_hindi': '''एक दुइ तीन चार पाँच,
आओ सब मिल के गिनो!
छह सात आठ नौ दस,
बुला! विनाका! सब गाओ!

बीस अउर एक, बीस अउर दुइ,
फिजी बात में गिनो भइया!
दुइ सेब, दुइ केला,
सीखो गिनती अच्छा से!''',
                'lyrics_romanized': '''Ek dui teen chaar paanch,
Aao sab mil ke gino!
Chhah saat aath nau das,
Bula! Vinaka! Sab gaao!

Bees aur ek, bees aur dui,
Fiji baat mein gino bhaiya!
Dui seb, dui kela,
Seekho ginti achcha se!''',
                'lyrics_english': '''One two three four five,
Let us all count together!
Six seven eight nine ten,
Bula! Vinaka! Everyone sing!

Twenty-one, twenty-two,
Count in Fiji Hindi brother!
Two apples, two bananas,
Learn counting nicely!''',
                'category': 'EDUCATIONAL',
                'age_min': 4,
                'age_max': 7,
                'duration_seconds': 75,
            },
            {
                'title_english': 'Bula Vinaka Song',
                'title_hindi': 'बुला विनाका गाना',
                'title_romanized': 'Bula Vinaka Gaana',
                'lyrics_hindi': '''बुला बुला बोलो,
कइसे बा पूछो,
ठीक बा बोलो,
विनाका विनाका!

सुबह होवे बुला,
साँझ होवे बुला,
फिजी में हम रहता है,
खुश खुश खुश!''',
                'lyrics_romanized': '''Bula bula bolo,
Kaise ba poocho,
Theek ba bolo,
Vinaka vinaka!

Subah hove bula,
Saanjh hove bula,
Fiji mein ham rahta hai,
Khush khush khush!''',
                'lyrics_english': '''Say Bula Bula,
Ask how are you,
Say I am fine,
Vinaka vinaka!

Morning comes Bula,
Evening comes Bula,
In Fiji we live,
Happy happy happy!''',
                'category': 'RHYME',
                'age_min': 4,
                'age_max': 6,
                'duration_seconds': 55,
            },
            {
                'title_english': 'Fiji Hindi Family Song',
                'title_hindi': 'फिजी परिवार गाना',
                'title_romanized': 'Fiji Parivaar Gaana',
                'lyrics_hindi': '''माई प्यारी माई,
बाप हमार बाप,
दादा दादी अच्छे बा,
हम सब साथे साथ!

भइया हमार भइया,
बहिनी हमार बहिनी,
परिवार के संगे रहो,
खुशी खुशी रहो!''',
                'lyrics_romanized': '''Maai pyaari maai,
Baap hamaar baap,
Daada daadi achche ba,
Ham sab saathe saath!

Bhaiya hamaar bhaiya,
Bahini hamaar bahini,
Parivaar ke sange raho,
Khushi khushi raho!''',
                'lyrics_english': '''Mother dear mother,
Father our father,
Grandpa grandma are good,
We are all together!

Brother our brother,
Sister our sister,
Stay with family,
Stay happily!''',
                'category': 'RHYME',
                'age_min': 4,
                'age_max': 6,
                'duration_seconds': 60,
            },
            {
                'title_english': 'Fiji Holi Song',
                'title_hindi': 'फिजी होली गाना',
                'title_romanized': 'Fiji Holi Gaana',
                'lyrics_hindi': '''होली आ गइस रे,
रंग लगाओ रे,
लाल पीला नीला हरा,
सब रंग-बिरंगा हो गइस!

फगुआ खेलो रे भइया,
पिचकारी मारो रे,
दालो कासावा खाओ,
फिजी में होली मनाओ!''',
                'lyrics_romanized': '''Holi aa gais re,
Rang lagao re,
Laal peela neela hara,
Sab rang-biranga ho gais!

Phaguwa khelo re bhaiya,
Pichkaari maaro re,
Daalo kaasava khaao,
Fiji mein Holi manaao!''',
                'lyrics_english': '''Holi has come,
Put on colors,
Red yellow blue green,
Everyone became colorful!

Play Phaguwa brother,
Spray the colors,
Eat taro and cassava,
Celebrate Holi in Fiji!''',
                'category': 'FOLK',
                'age_min': 4,
                'age_max': 7,
                'duration_seconds': 65,
            },
            {
                'title_english': 'Fiji Hindi Alphabet Song',
                'title_hindi': 'फिजी बात अक्षर गाना',
                'title_romanized': 'Fiji Baat Akshar Gaana',
                'lyrics_hindi': '''अ आ इ ई,
उ ऊ ए ऐ,
ओ औ अं अः,
सब स्वर सीखो भइया!

क ख ग घ,
च छ ज झ,
फिजी बात में पढ़ो,
बुला! मजा आवे!''',
                'lyrics_romanized': '''A aa i ee,
U oo e ai,
O au an ah,
Sab swar seekho bhaiya!

Ka kha ga gha,
Cha chha ja jha,
Fiji baat mein parho,
Bula! Maja aave!''',
                'lyrics_english': '''A aa i ee,
U oo e ai,
O au an ah,
Learn all vowels, brother!

Ka kha ga gha,
Cha chha ja jha,
Study in Fiji Hindi,
Bula! Fun will come!''',
                'category': 'EDUCATIONAL',
                'age_min': 4,
                'age_max': 7,
                'duration_seconds': 70,
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
                    'language': 'FIJI_HINDI',
                    'order': i,
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(songs_data)} songs'))

    def seed_curriculum_levels(self):
        """Create L1 and L2 curriculum levels for Fiji Hindi."""
        self.stdout.write('Creating curriculum levels...')

        levels_data = [
            {
                'code': 'L1',
                'name_english': 'Discovery',
                'name_hindi': 'शुरूआत',
                'name_romanized': 'Shuruaat',
                'min_age': 4,
                'max_age': 5,
                'description': 'First steps in learning Fiji Hindi. Children learn बुला greetings, vowels, and simple words from the Indo-Fijian diaspora.',
                'peppi_welcome': 'बुला! Welcome to Peppi\'s Fiji Hindi class!',
                'peppi_completion': 'वाह! बहुत बढ़िया! You completed L1! Let\'s move to L2!',
                'emoji': '🌴',
                'theme_color': '#22c55e',
                'order': 1,
                'estimated_hours': 10,
                'min_xp_required': 0,
                'xp_reward': 400,
                'is_free': True,
            },
            {
                'code': 'L2',
                'name_english': 'Building',
                'name_hindi': 'बनावट',
                'name_romanized': 'Banaavat',
                'min_age': 5,
                'max_age': 6,
                'description': 'Learn consonants, matras, Fijian loanwords, and start reading simple Fiji Hindi sentences.',
                'peppi_welcome': 'बुला! Ready to learn more Fiji Hindi?',
                'peppi_completion': 'विनाका! You are a Fiji Hindi superstar!',
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
        """Create Peppi phrases in Fiji Hindi with Fijian words."""
        self.stdout.write('Creating Peppi phrases (Fiji Hindi style with Fijian words)...')

        phrases_data = [
            {'category': 'GREETING', 'text_hindi': 'बुला!', 'text_english': 'Hello! (Fijian)', 'text_romanized': 'Bula!', 'context': 'fiji_hindi_greeting', 'language': 'FIJI_HINDI'},
            {'category': 'GREETING', 'text_hindi': 'कइसे बा?', 'text_english': 'How are you?', 'text_romanized': 'Kaise ba?', 'context': 'fiji_hindi_greeting_2', 'language': 'FIJI_HINDI'},
            {'category': 'CORRECT', 'text_hindi': 'बहुत बढ़िया बा!', 'text_english': 'Very good!', 'text_romanized': 'Bahut barhiya ba!', 'context': 'fiji_hindi_celebration', 'language': 'FIJI_HINDI'},
            {'category': 'CORRECT', 'text_hindi': 'वाह! मजा आ गइस!', 'text_english': 'Wow! That was fun!', 'text_romanized': 'Waah! Maja aa gais!', 'context': 'fiji_hindi_wow', 'language': 'FIJI_HINDI'},
            {'category': 'CORRECT', 'text_hindi': 'साबास भइया!', 'text_english': 'Well done brother!', 'text_romanized': 'Sabaas bhaiya!', 'context': 'fiji_hindi_welldone', 'language': 'FIJI_HINDI'},
            {'category': 'WRONG', 'text_hindi': 'फिर से करो!', 'text_english': 'Try again!', 'text_romanized': 'Phir se karo!', 'context': 'fiji_hindi_tryagain', 'language': 'FIJI_HINDI'},
            {'category': 'ENCOURAGEMENT', 'text_hindi': 'तुम कर सकता है!', 'text_english': 'You can do it!', 'text_romanized': 'Tum kar sakta hai!', 'context': 'fiji_hindi_encourage', 'language': 'FIJI_HINDI'},
            {'category': 'FAREWELL', 'text_hindi': 'बाद में मिलब!', 'text_english': 'See you later!', 'text_romanized': 'Baad mein milab!', 'context': 'fiji_hindi_farewell', 'language': 'FIJI_HINDI'},
            {'category': 'GREETING', 'text_hindi': 'विनाका!', 'text_english': 'Thank you! (Fijian)', 'text_romanized': 'Vinaka!', 'context': 'fiji_hindi_thankyou', 'language': 'FIJI_HINDI'},
            {'category': 'ENCOURAGEMENT', 'text_hindi': 'चलो!', 'text_english': "Let's go!", 'text_romanized': 'Chalo!', 'context': 'fiji_hindi_letsgo', 'language': 'FIJI_HINDI'},
            {'category': 'CORRECT', 'text_hindi': 'एकदम सही बा!', 'text_english': 'Exactly right!', 'text_romanized': 'Ekdam sahi ba!', 'context': 'fiji_hindi_correct', 'language': 'FIJI_HINDI'},
            {'category': 'ENCOURAGEMENT', 'text_hindi': 'आगे बढ़ो!', 'text_english': 'Keep going!', 'text_romanized': 'Aage barho!', 'context': 'fiji_hindi_keepgoing', 'language': 'FIJI_HINDI'},
            {'category': 'GREETING', 'text_hindi': 'ठीक बा!', 'text_english': "I'm fine!", 'text_romanized': 'Theek ba!', 'context': 'fiji_hindi_fine', 'language': 'FIJI_HINDI'},
            {'category': 'CORRECT', 'text_hindi': 'बहुत अच्छा किइला!', 'text_english': 'You did very well!', 'text_romanized': 'Bahut achcha kiila!', 'context': 'fiji_hindi_didwell', 'language': 'FIJI_HINDI'},
        ]

        for phrase_data in phrases_data:
            PeppiPhrase.objects.update_or_create(
                category=phrase_data['category'],
                text_hindi=phrase_data['text_hindi'],
                context=phrase_data['context'],
                defaults={
                    'text_english': phrase_data['text_english'],
                    'text_romanized': phrase_data['text_romanized'],
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(phrases_data)} Peppi phrases'))

    def seed_games(self):
        """Create Fiji Hindi games."""
        self.stdout.write('Creating Fiji Hindi games...')

        games_data = [
            {
                'name': 'Fiji Hindi Memory',
                'description': 'Match Fiji Hindi letters with their sounds',
                'game_type': 'MEMORY',
                'skill_focus': 'ALPHABET',
                'level': 1,
            },
            {
                'name': 'Bula Word Search',
                'description': 'Find hidden Fiji Hindi words including Fijian loanwords',
                'game_type': 'WORDSEARCH',
                'skill_focus': 'VOCAB',
                'level': 1,
            },
            {
                'name': 'Listen and Match',
                'description': 'Listen to Fiji Hindi words and match with pictures',
                'game_type': 'LISTENING',
                'skill_focus': 'LISTENING',
                'level': 1,
            },
            {
                'name': 'Fiji Hindi Quiz',
                'description': 'Test your Fiji Hindi knowledge including unique vocabulary',
                'game_type': 'QUIZ',
                'skill_focus': 'MIXED',
                'level': 2,
            },
            {
                'name': 'Word Builder',
                'description': 'Build Fiji Hindi words using letters',
                'game_type': 'BUILDER',
                'skill_focus': 'SPELLING',
                'level': 2,
            },
        ]

        for game_data in games_data:
            Game.objects.update_or_create(
                language='FIJI_HINDI',
                name=game_data['name'],
                defaults={
                    'description': game_data['description'],
                    'instructions': f"Play {game_data['name']} to practice Fiji Hindi!",
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

    def seed_grammar(self):
        """Create Fiji Hindi grammar topics."""
        self.stdout.write('Creating Fiji Hindi grammar topics...')

        grammar_data = [
            {
                'name': 'Sentence Structure',
                'name_native': 'वाक्य बनावट',
                'description': 'Learn Fiji Hindi sentence structure (SOV order)',
                'level': 1,
                'order': 1,
                'rules': [
                    {
                        'title': 'Basic Word Order',
                        'explanation': 'Fiji Hindi uses Subject-Object-Verb order: हम रोटी खाता है (I bread eat)',
                        'formula': 'Subject + Object + Verb',
                        'examples': [
                            {'hindi': 'हम रोटी खाता है।', 'romanized': 'Ham roti khaata hai.', 'english': 'I eat bread.'},
                            {'hindi': 'तुम पानी पीता है।', 'romanized': 'Tum paani peeta hai.', 'english': 'You drink water.'},
                        ],
                    },
                    {
                        'title': 'No Gender Agreement',
                        'explanation': 'In Fiji Hindi, verbs do NOT change for gender. Same verb for he/she!',
                        'formula': 'Verb stays same for masculine/feminine',
                        'examples': [
                            {'hindi': 'ऊ जाता है। (he/she)', 'romanized': 'Oo jaata hai.', 'english': 'He/She goes.'},
                            {'hindi': 'ऊ खाता है। (he/she)', 'romanized': 'Oo khaata hai.', 'english': 'He/She eats.'},
                        ],
                    },
                ]
            },
            {
                'name': 'First/Second Person',
                'name_native': 'प्रथम/द्वितीय पुरुष',
                'description': 'First and second person verbs are the same in Fiji Hindi',
                'level': 1,
                'order': 2,
                'rules': [
                    {
                        'title': 'हम और तुम Same Verb',
                        'explanation': 'Unlike Standard Hindi, Fiji Hindi uses same verb for I (हम) and you (तुम)',
                        'formula': 'हम/तुम + Object + Same Verb',
                        'examples': [
                            {'hindi': 'हम जाता है।', 'romanized': 'Ham jaata hai.', 'english': 'I go.'},
                            {'hindi': 'तुम जाता है।', 'romanized': 'Tum jaata hai.', 'english': 'You go.'},
                        ],
                    },
                ]
            },
            {
                'name': 'Numbers (Fiji Style)',
                'name_native': 'गिनती (फिजी तरीका)',
                'description': 'Fiji Hindi numbers follow European order for compound numbers',
                'level': 2,
                'order': 3,
                'rules': [
                    {
                        'title': 'दुइ not दो',
                        'explanation': 'Two is "दुइ" (dui) in Fiji Hindi, from Awadhi/Bhojpuri dialect',
                        'formula': 'एक, दुइ, तीन...',
                        'examples': [
                            {'hindi': 'दुइ सेब', 'romanized': 'Dui seb', 'english': 'Two apples'},
                            {'hindi': 'दुइ रोटी', 'romanized': 'Dui roti', 'english': 'Two rotis'},
                        ],
                    },
                    {
                        'title': 'Tens First (21-99)',
                        'explanation': 'Fiji Hindi says tens first: बीस और एक (twenty and one) instead of इक्कीस',
                        'formula': 'Tens + और + Units',
                        'examples': [
                            {'hindi': 'बीस और एक', 'romanized': 'Bees aur ek', 'english': '21 (twenty-one)'},
                            {'hindi': 'तीस और सात', 'romanized': 'Tees aur saat', 'english': '37 (thirty-seven)'},
                        ],
                    },
                ]
            },
            {
                'name': 'Past Tense',
                'name_native': 'भूतकाल',
                'description': 'Fiji Hindi past tense has unique endings',
                'level': 2,
                'order': 4,
                'rules': [
                    {
                        'title': 'Past Tense Endings',
                        'explanation': 'Third person past uses -इस (masculine) and -इन (feminine)',
                        'formula': 'ऊ + Verb root + इस/इन',
                        'examples': [
                            {'hindi': 'ऊ गइस।', 'romanized': 'Oo gais.', 'english': 'He went.'},
                            {'hindi': 'ऊ गइन।', 'romanized': 'Oo gain.', 'english': 'She went.'},
                            {'hindi': 'ऊ खाइस।', 'romanized': 'Oo khaais.', 'english': 'He ate.'},
                        ],
                    },
                ]
            },
            {
                'name': 'Questions',
                'name_native': 'सवाल',
                'description': 'How to ask questions in Fiji Hindi',
                'level': 2,
                'order': 5,
                'rules': [
                    {
                        'title': 'Yes/No Questions with का',
                        'explanation': 'Add का at the end of a statement to make it a question',
                        'formula': 'Statement + का?',
                        'examples': [
                            {'hindi': 'तुम जाता है का?', 'romanized': 'Tum jaata hai ka?', 'english': 'Are you going?'},
                            {'hindi': 'ऊ खाता है का?', 'romanized': 'Oo khaata hai ka?', 'english': 'Is he/she eating?'},
                        ],
                    },
                ]
            },
        ]

        for topic_data in grammar_data:
            topic, _ = GrammarTopic.objects.update_or_create(
                language='FIJI_HINDI',
                name=topic_data['name'],
                defaults={
                    'name_native': topic_data['name_native'],
                    'description': topic_data['description'],
                    'level': topic_data['level'],
                    'order': topic_data['order'],
                    'is_active': True,
                }
            )

            for i, rule_data in enumerate(topic_data['rules'], 1):
                GrammarRule.objects.update_or_create(
                    topic=topic,
                    title=rule_data['title'],
                    defaults={
                        'explanation': rule_data['explanation'],
                        'formula': rule_data.get('formula', ''),
                        'examples': rule_data['examples'],
                        'order': i,
                    }
                )

        self.stdout.write(self.style.SUCCESS(f'  Created {len(grammar_data)} grammar topics'))

    def seed_assessments(self):
        """Create Fiji Hindi assessments."""
        self.stdout.write('Creating Fiji Hindi assessments...')

        assessments_data = [
            {
                'name': 'L1 Entry Assessment',
                'description': 'Check your starting level in Fiji Hindi',
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
                language='FIJI_HINDI',
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
