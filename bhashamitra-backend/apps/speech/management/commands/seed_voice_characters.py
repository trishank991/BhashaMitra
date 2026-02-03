"""
Management command to seed initial VoiceCharacter data.

Creates default Peppi characters for all supported languages with both male and female voices.

Usage:
    python manage.py seed_voice_characters
"""

from django.core.management.base import BaseCommand
from apps.speech.models import VoiceCharacter


class Command(BaseCommand):
    help = 'Seed initial VoiceCharacter data for Peppi across all languages'

    # Supported languages
    LANGUAGES = [
        'HINDI',
        'TAMIL',
        'GUJARATI',
        'PUNJABI',
        'TELUGU',
        'MALAYALAM',
        'BENGALI',
        'KANNADA',
        'MARATHI',
        'ODIA',
        'ASSAMESE',
        'URDU',
        'FIJI_HINDI',
    ]

    # Native names for Peppi in each language
    PEPPI_NATIVE_NAMES = {
        'HINDI': 'पेप्पी',
        'TAMIL': 'பெப்பி',
        'GUJARATI': 'પેપી',
        'PUNJABI': 'ਪੇਪੀ',
        'TELUGU': 'పెప్పి',
        'MALAYALAM': 'പെപ്പി',
        'BENGALI': 'পেপি',
        'KANNADA': 'ಪೆಪ್ಪಿ',
        'MARATHI': 'पेप्पी',
        'ODIA': 'ପେପ୍ପି',
        'ASSAMESE': 'পেপি',
        'URDU': 'پیپی',
        'FIJI_HINDI': 'पेप्पी',
    }

    # Warmth phrases per language
    WARMTH_PHRASES = {
        'HINDI': {
            'greeting': ['नमस्ते!', 'आओ!', 'चलो शुरू करें!'],
            'encouragement': ['शाबाश!', 'बहुत अच्छा!', 'तुम कर सकते हो!', 'वाह!'],
            'praise': ['बेहतरीन!', 'लाजवाब!', 'बहुत बढ़िया!', 'कमाल है!'],
            'try_again': ['फिर कोशिश करो!', 'चिंता मत करो!', 'एक बार और!'],
            'meow': ['म्याऊं!', 'मियाऊं!'],
        },
        'TAMIL': {
            'greeting': ['வணக்கம்!', 'வாங்க!', 'ஆரம்பிக்கலாம்!'],
            'encouragement': ['சபாஷ்!', 'நன்று!', 'உன்னால் முடியும்!', 'வாவ்!'],
            'praise': ['அருமை!', 'சூப்பர்!', 'மிக அருமை!'],
            'try_again': ['மீண்டும் முயற்சி செய்!', 'கவலை வேண்டாம்!'],
            'meow': ['மியாவ்!'],
        },
        'GUJARATI': {
            'greeting': ['નમસ્તે!', 'આવો!', 'ચાલો શરૂ કરીએ!'],
            'encouragement': ['શાબાશ!', 'બહુ સરસ!', 'તમે કરી શકો!', 'વાહ!'],
            'praise': ['બહુ સરસ!', 'લાજવાબ!', 'કમાલ!'],
            'try_again': ['ફરી પ્રયત્ન કરો!', 'ચિંતા ન કરો!'],
            'meow': ['મ્યાઉં!'],
        },
        'PUNJABI': {
            'greeting': ['ਸਤ ਸ੍ਰੀ ਅਕਾਲ!', 'ਆਓ!', 'ਸ਼ੁਰੂ ਕਰੀਏ!'],
            'encouragement': ['ਸ਼ਾਬਾਸ਼!', 'ਬਹੁਤ ਵਧੀਆ!', 'ਤੁਸੀਂ ਕਰ ਸਕਦੇ ਹੋ!', 'ਵਾਹ!'],
            'praise': ['ਬਹੁਤ ਵਧੀਆ!', 'ਲਾਜਵਾਬ!', 'ਕਮਾਲ!'],
            'try_again': ['ਫਿਰ ਕੋਸ਼ਿਸ਼ ਕਰੋ!', 'ਚਿੰਤਾ ਨਾ ਕਰੋ!'],
            'meow': ['ਮਿਆਊਂ!'],
        },
        'TELUGU': {
            'greeting': ['నమస్కారం!', 'రండి!', 'ప్రారంభిద్దాం!'],
            'encouragement': ['శాబాష్!', 'చాలా బాగుంది!', 'మీరు చేయగలరు!', 'వావ్!'],
            'praise': ['అద్భుతం!', 'చాలా బాగుంది!', 'సూపర్!'],
            'try_again': ['మళ్ళీ ప్రయత్నించండి!', 'బాధపడకండి!'],
            'meow': ['మియావ్!'],
        },
        'MALAYALAM': {
            'greeting': ['നമസ്കാരം!', 'വരൂ!', 'തുടങ്ങാം!'],
            'encouragement': ['വളരെ നല്ലത്!', 'ശരി!', 'നിങ്ങൾക്ക് കഴിയും!'],
            'praise': ['അതിമനോഹരം!', 'വളരെ നല്ലത്!', 'സൂപ്പർ!'],
            'try_again': ['വീണ്ടും ശ്രമിക്കൂ!', 'വിഷമിക്കേണ്ട!'],
            'meow': ['മിയാവ്!'],
        },
        'BENGALI': {
            'greeting': ['নমস্কার!', 'এসো!', 'শুরু করি!'],
            'encouragement': ['সাবাশ!', 'খুব ভালো!', 'তুমি পারবে!', 'বাহ!'],
            'praise': ['অসাধারণ!', 'দুর্দান্ত!', 'খুব সুন্দর!'],
            'try_again': ['আবার চেষ্টা করো!', 'চিন্তা কোরো না!'],
            'meow': ['মিয়াউ!'],
        },
        'KANNADA': {
            'greeting': ['ನಮಸ್ಕಾರ!', 'ಬನ್ನಿ!', 'ಪ್ರಾರಂಭಿಸೋಣ!'],
            'encouragement': ['ಶಾಬಾಸ್!', 'ಒಳ್ಳೆಯದು!', 'ನೀವು ಮಾಡಬಹುದು!', 'ವಾವ್!'],
            'praise': ['ಅದ್ಭುತ!', 'ಸೂಪರ್!', 'ತುಂಬಾ ಚೆನ್ನಾಗಿದೆ!'],
            'try_again': ['ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ!', 'ಚಿಂತಿಸಬೇಡಿ!'],
            'meow': ['ಮಿಯಾವ್!'],
        },
        'MARATHI': {
            'greeting': ['नमस्कार!', 'या!', 'सुरू करूया!'],
            'encouragement': ['शाबास!', 'छान!', 'तू करू शकतोस!', 'वा!'],
            'praise': ['अप्रतिम!', 'उत्तम!', 'खूप छान!'],
            'try_again': ['पुन्हा प्रयत्न कर!', 'काळजी करू नकोस!'],
            'meow': ['म्याऊ!'],
        },
        'ODIA': {
            'greeting': ['ନମସ୍କାର!', 'ଆସ!', 'ଆରମ୍ଭ କରିବା!'],
            'encouragement': ['ଶାବାଶ!', 'ବହୁତ ଭଲ!', 'ତୁମେ କରିପାରିବ!', 'ୱାଓ!'],
            'praise': ['ଅଦ୍ଭୁତ!', 'ସୁପର!', 'ବହୁତ ଭଲ!'],
            'try_again': ['ପୁଣି ଚେଷ୍ଟା କର!', 'ଚିନ୍ତା କର ନାହିଁ!'],
            'meow': ['ମିଆଉଁ!'],
        },
        'ASSAMESE': {
            'greeting': ['নমস্কাৰ!', 'আহা!', 'আৰম্ভ কৰোঁ!'],
            'encouragement': ['সাবাচ!', 'বহুত ভাল!', 'তুমি পাৰিবা!', 'বাঃ!'],
            'praise': ['অসাধাৰণ!', 'চুপাৰ!', 'বহুত ভাল!'],
            'try_again': ['আকৌ চেষ্টা কৰা!', 'চিন্তা নকৰিবা!'],
            'meow': ['মিয়াউ!'],
        },
        'URDU': {
            'greeting': ['السلام علیکم!', 'آؤ!', 'شروع کریں!'],
            'encouragement': ['شاباش!', 'بہت اچھا!', 'تم کر سکتے ہو!', 'واہ!'],
            'praise': ['بہترین!', 'لاجواب!', 'بہت عمدہ!'],
            'try_again': ['پھر کوشش کرو!', 'فکر نہ کرو!'],
            'meow': ['میاؤں!'],
        },
        'FIJI_HINDI': {
            'greeting': ['नमस्ते!', 'आओ!', 'शुरू करें!'],
            'encouragement': ['शाबाश!', 'बहुत अच्छा!', 'तुम कर सकते हो!', 'वाह!'],
            'praise': ['बहुत बढ़िया!', 'लाजवाब!', 'कमाल है!'],
            'try_again': ['फिर कोशिश करो!', 'चिंता मत करो!'],
            'meow': ['म्याऊं!'],
        },
    }

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Seeding VoiceCharacter data...'))

        created_count = 0
        updated_count = 0

        for language in self.LANGUAGES:
            # Create Female Peppi (default)
            female_peppi, created = VoiceCharacter.objects.get_or_create(
                character_type='PEPPI',
                language=language,
                gender='FEMALE',
                defaults={
                    'name': 'Peppi',
                    'name_native': self.PEPPI_NATIVE_NAMES.get(language, 'Peppi'),
                    'description': f'Female Peppi voice for {language} - Warm and encouraging AI tutor',
                    'voice_source': 'SARVAM_AI',
                    'voice_id': 'anushka',
                    'voice_model': 'bulbul:v2',
                    'speaking_rate': 0.7,
                    'pitch': 0.3,
                    'volume_gain_db': 0.0,
                    'warmth_phrases': self.WARMTH_PHRASES.get(language, {}),
                    'personality_traits': {
                        'tone': 'warm',
                        'energy': 'enthusiastic',
                        'patience': 'high',
                        'encouragement_level': 'high'
                    },
                    'is_active': True,
                    'is_default': True,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'  + Created Female Peppi for {language}')
                )
            else:
                # Update warmth phrases if needed
                if not female_peppi.warmth_phrases:
                    female_peppi.warmth_phrases = self.WARMTH_PHRASES.get(language, {})
                    female_peppi.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'  ~ Updated Female Peppi for {language}')
                    )

            # Create Male Peppi
            male_peppi, created = VoiceCharacter.objects.get_or_create(
                character_type='PEPPI',
                language=language,
                gender='MALE',
                defaults={
                    'name': 'Peppi',
                    'name_native': self.PEPPI_NATIVE_NAMES.get(language, 'Peppi'),
                    'description': f'Male Peppi voice for {language} - Warm and encouraging AI tutor',
                    'voice_source': 'SARVAM_AI',
                    'voice_id': 'arvind',
                    'voice_model': 'bulbul:v2',
                    'speaking_rate': 0.7,
                    'pitch': 0.4,
                    'volume_gain_db': 0.0,
                    'warmth_phrases': self.WARMTH_PHRASES.get(language, {}),
                    'personality_traits': {
                        'tone': 'warm',
                        'energy': 'enthusiastic',
                        'patience': 'high',
                        'encouragement_level': 'high'
                    },
                    'is_active': True,
                    'is_default': False,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'  + Created Male Peppi for {language}')
                )
            else:
                if not male_peppi.warmth_phrases:
                    male_peppi.warmth_phrases = self.WARMTH_PHRASES.get(language, {})
                    male_peppi.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'  ~ Updated Male Peppi for {language}')
                    )

            # Create Grandmother placeholder (for future cloned voice)
            grandma, created = VoiceCharacter.objects.get_or_create(
                character_type='GRANDMOTHER',
                language=language,
                gender='FEMALE',
                defaults={
                    'name': 'Grandmother',
                    'name_native': self._get_grandma_name(language),
                    'description': f'Grandmother voice for {language} - Warm storytelling voice (awaiting voice cloning)',
                    'voice_source': 'CLONED',  # Placeholder for future cloning
                    'voice_id': '',  # To be filled when voice is cloned
                    'speaking_rate': 0.6,  # Slower, more deliberate
                    'pitch': -1.0,  # Slightly lower for elderly voice
                    'volume_gain_db': 0.0,
                    'warmth_phrases': self.WARMTH_PHRASES.get(language, {}),
                    'personality_traits': {
                        'tone': 'loving',
                        'energy': 'calm',
                        'patience': 'very_high',
                        'storytelling': 'traditional'
                    },
                    'is_active': False,  # Inactive until voice is cloned
                    'is_default': True,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'  + Created Grandmother placeholder for {language}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSeeding complete! Created: {created_count}, Updated: {updated_count}'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Total voice characters: {VoiceCharacter.objects.count()}'
            )
        )

    def _get_grandma_name(self, language: str) -> str:
        """Get native name for grandmother in each language."""
        grandma_names = {
            'HINDI': 'दादी',
            'TAMIL': 'பாட்டி',
            'GUJARATI': 'દાદી',
            'PUNJABI': 'ਦਾਦੀ',
            'TELUGU': 'అమ్మమ్మ',
            'MALAYALAM': 'അമ്മൂമ്മ',
            'BENGALI': 'ঠাকুমা',
            'KANNADA': 'ಅಜ್ಜಿ',
            'MARATHI': 'आजी',
            'ODIA': 'ଆଈ',
            'ASSAMESE': 'আইতা',
            'URDU': 'دادی',
            'FIJI_HINDI': 'दादी',
        }
        return grandma_names.get(language, 'Grandmother')
