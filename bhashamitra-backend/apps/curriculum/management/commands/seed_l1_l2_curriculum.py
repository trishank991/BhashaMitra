"""
Comprehensive L1-L2 Hindi Curriculum Seed Command.
Seeds complete curriculum content including levels, modules, lessons, vocabulary, and stories.

Run: python manage.py seed_l1_l2_curriculum
"""

import uuid
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.curriculum.models import (
    CurriculumLevel, CurriculumModule, Lesson,
    VocabularyTheme, VocabularyWord
)
from apps.stories.models import Story, StoryPage
from apps.children.models import Child


class Command(BaseCommand):
    help = 'Seed L1 and L2 Hindi curriculum with complete content'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS('🚀 SEEDING L1-L2 HINDI CURRICULUM'))
        self.stdout.write(self.style.SUCCESS('=' * 60 + '\n'))

        with transaction.atomic():
            # 1. Create/Update Levels
            self.stdout.write('📊 Step 1: Creating Curriculum Levels...')
            self.seed_levels()

            # 2. Create L1 Content
            self.stdout.write('\n📚 Step 2: Creating L1 Modules and Lessons...')
            self.seed_l1_modules()
            self.seed_l1_lessons()

            # 3. Create L2 Content
            self.stdout.write('\n📖 Step 3: Creating L2 Modules and Lessons...')
            self.seed_l2_modules()
            self.seed_l2_lessons()

            # 4. Create Vocabulary
            self.stdout.write('\n📝 Step 4: Seeding Vocabulary (70 words)...')
            self.seed_vocabulary()

            # 5. Create Stories
            self.stdout.write('\n📕 Step 5: Seeding Stories (10 stories)...')
            self.seed_stories()

        self.print_summary()

    def seed_levels(self):
        """Create L1 and L2 levels with proficiency-based naming."""
        levels_data = [
            {
                'code': 'L1',
                'name_english': 'Discovery',
                'name_hindi': 'खोज',
                'name_romanized': 'Khoj',
                'min_age': 4,
                'max_age': 14,
                'description': 'Start your Hindi journey! Learn the beautiful sounds of Hindi vowels and discover your first words.',
                'learning_objectives': [
                    'Recognize all 13 Hindi vowels (स्वर)',
                    'Understand 20 essential sight words',
                    'Listen and identify basic Hindi sounds',
                    'Appreciate Hindi through songs and rhymes',
                    'Read 3 simple picture stories'
                ],
                'peppi_welcome': 'Namaste! 🙏 Welcome to your Hindi learning adventure! I am Peppi, your friend who will help you learn Hindi step by step!',
                'peppi_completion': '🎉 Amazing! You completed Level 1! You know 13 vowels and 20 words! Ready for Level 2?',
                'emoji': '🌱',
                'theme_color': '#10B981',
                'order': 1,
                'estimated_hours': 8,
                'min_xp_required': 0,
                'xp_reward': 100,
                'is_free': True,
            },
            {
                'code': 'L2',
                'name_english': 'Building Blocks',
                'name_hindi': 'नींव',
                'name_romanized': 'Neenv',
                'min_age': 4,
                'max_age': 14,
                'description': 'Learn all Hindi consonants and start reading words! Build the foundation for reading fluency.',
                'learning_objectives': [
                    'Recognize all 33 consonants (व्यंजन)',
                    'Apply 12 matras (vowel marks) to consonants',
                    'Read 50 vocabulary words across 5 themes',
                    'Form simple 2-3 word phrases',
                    'Read 7 stories with basic sentences'
                ],
                'peppi_welcome': 'Welcome back! 🌿 Ready to build your Hindi foundation? Let\'s learn all the consonants!',
                'peppi_completion': '🏆 Fantastic! You can now read Hindi! All 33 consonants and 12 matras mastered!',
                'emoji': '🧱',
                'theme_color': '#3B82F6',
                'order': 2,
                'estimated_hours': 15,
                'min_xp_required': 400,
                'xp_reward': 150,
                'is_free': False,
            }
        ]

        for level_data in levels_data:
            level, created = CurriculumLevel.objects.update_or_create(
                code=level_data['code'],
                defaults=level_data
            )
            status = '✅ Created' if created else '♻️ Updated'
            self.stdout.write(f'  {status}: {level.code} - {level.name_english}')

    def seed_l1_modules(self):
        """Create 4 modules for L1."""
        l1 = CurriculumLevel.objects.get(code='L1')

        modules_data = [
            {
                'code': 'L1_M1_MEET_HINDI',
                'name_english': 'Meet Hindi',
                'name_hindi': 'हिंदी से मिलो',
                'name_romanized': 'Hindi Se Milo',
                'description': 'Welcome to Hindi! Discover the beautiful Devanagari script.',
                'module_type': 'ALPHABET',
                'objectives': [
                    'Understand what Hindi is and where it\'s spoken',
                    'Recognize the Devanagari script visually',
                    'Feel excited about learning Hindi'
                ],
                'emoji': '👋',
                'order': 1,
                'estimated_minutes': 15,
                'xp_reward': 30,
                'peppi_intro': 'Namaste! I\'m Peppi! Let\'s discover Hindi together!',
            },
            {
                'code': 'L1_M2_VOWELS',
                'name_english': 'Vowels (स्वर)',
                'name_hindi': 'स्वर',
                'name_romanized': 'Swar',
                'description': 'Learn all 13 Hindi vowels - the musical foundation of Hindi!',
                'module_type': 'ALPHABET',
                'objectives': [
                    'Recognize all 13 Hindi vowels',
                    'Pronounce each vowel correctly',
                    'Identify vowels by sound'
                ],
                'emoji': '🎵',
                'order': 2,
                'estimated_minutes': 30,
                'xp_reward': 60,
                'peppi_intro': 'Time to learn vowels! अ आ इ ई - these are like music!',
            },
            {
                'code': 'L1_M3_FIRST_WORDS',
                'name_english': 'First Words',
                'name_hindi': 'पहले शब्द',
                'name_romanized': 'Pehle Shabd',
                'description': 'Learn your first 20 Hindi words!',
                'module_type': 'VOCABULARY',
                'objectives': [
                    'Recognize 20 essential Hindi words by sight and sound',
                    'Understand word meanings',
                    'Use words in simple contexts'
                ],
                'emoji': '📖',
                'order': 3,
                'estimated_minutes': 20,
                'xp_reward': 40,
                'peppi_intro': 'Let\'s learn your first words! माँ, पापा, नमस्ते!',
            },
            {
                'code': 'L1_M4_LISTENING',
                'name_english': 'Listening Fun',
                'name_hindi': 'सुनने का मज़ा',
                'name_romanized': 'Sunne Ka Maza',
                'description': 'Practice listening through songs, rhymes, and stories!',
                'module_type': 'LISTENING',
                'objectives': [
                    'Develop Hindi listening skills',
                    'Enjoy Hindi through music and stories',
                    'Recognize learned words in context'
                ],
                'emoji': '🎧',
                'order': 4,
                'estimated_minutes': 15,
                'xp_reward': 30,
                'peppi_intro': 'Listening time! Let\'s enjoy songs and stories!',
            },
        ]

        for mod_data in modules_data:
            module, created = CurriculumModule.objects.update_or_create(
                code=mod_data['code'],
                defaults={'level': l1, **mod_data}
            )
            status = '✅' if created else '♻️'
            self.stdout.write(f'  {status} {mod_data["name_english"]}')

    def seed_l1_lessons(self):
        """Create 16 lessons for L1 with full content."""
        # Module 1: Meet Hindi (3 lessons)
        m1 = CurriculumModule.objects.get(code='L1_M1_MEET_HINDI')
        m1_lessons = [
            {
                'code': 'L1_M1_L1',
                'title_english': 'Welcome to Hindi!',
                'title_hindi': 'हिंदी में स्वागत!',
                'title_romanized': 'Hindi Mein Swagat!',
                'lesson_type': 'INTRODUCTION',
                'order': 1,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': True,
                'peppi_intro': 'Namaste! 🙏 Welcome to Hindi!',
                'peppi_success': 'Great start! You learned about Hindi!',
                'content': {
                    'introduction': 'Namaste! 🙏 Welcome to your Hindi learning adventure! Hindi is one of the most spoken languages in the world. Over 600 million people speak Hindi!',
                    'introduction_hindi': 'नमस्ते! 🙏 हिंदी सीखने के सफ़र में आपका स्वागत है!',
                    'sections': [
                        {
                            'type': 'text',
                            'title': 'What is Hindi?',
                            'content': 'Hindi is spoken in India and by Indian families all around the world - including right here! When you learn Hindi, you can talk to grandparents, understand Bollywood songs, and connect with your culture.'
                        },
                        {
                            'type': 'audio',
                            'title': 'Listen to Hindi',
                            'audio_text': 'नमस्ते! मैं हिंदी बोलता हूँ।',
                            'audio_translation': 'Namaste! I speak Hindi.'
                        }
                    ],
                    'exercises': [
                        {
                            'type': 'multiple_choice',
                            'question': 'How many people speak Hindi in the world?',
                            'options': ['6 million', '60 million', '600 million', '6 billion'],
                            'correct_answer': 2,
                            'explanation': 'Over 600 million people speak Hindi worldwide!'
                        }
                    ],
                    'summary': 'Hindi is a beautiful language spoken by over 600 million people.'
                }
            },
            {
                'code': 'L1_M1_L2',
                'title_english': 'The Devanagari Script',
                'title_hindi': 'देवनागरी लिपि',
                'title_romanized': 'Devanagari Lipi',
                'lesson_type': 'LEARNING',
                'order': 2,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': True,
                'peppi_intro': 'Let\'s learn about Devanagari!',
                'peppi_success': 'Now you know about Devanagari script!',
                'content': {
                    'introduction': 'Hindi uses a special script called Devanagari. It looks different from English, but it\'s actually very logical and beautiful!',
                    'sections': [
                        {
                            'type': 'text',
                            'title': 'What is Devanagari?',
                            'content': 'Devanagari (देवनागरी) is the script used to write Hindi. Unlike English, Hindi is written exactly as it sounds! Each letter makes one sound.'
                        },
                        {
                            'type': 'interactive',
                            'title': 'The Magic Line',
                            'content': 'See that line on top? That\'s called Shirorekha (शिरोरेखा) - the headline! It connects all the letters in a word.'
                        }
                    ],
                    'exercises': [
                        {
                            'type': 'multiple_choice',
                            'question': 'What is the line on top of Hindi letters called?',
                            'options': ['Underline', 'Shirorekha', 'Matra', 'Halant'],
                            'correct_answer': 1
                        }
                    ],
                    'summary': 'Devanagari is the beautiful script used to write Hindi.'
                }
            },
            {
                'code': 'L1_M1_L3',
                'title_english': 'Vowels and Consonants',
                'title_hindi': 'स्वर और व्यंजन',
                'title_romanized': 'Swar aur Vyanjan',
                'lesson_type': 'LEARNING',
                'order': 3,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': True,
                'peppi_intro': 'Let\'s learn about vowels and consonants!',
                'peppi_success': 'You know the difference now!',
                'content': {
                    'introduction': 'Just like English has vowels and consonants, Hindi has them too!',
                    'sections': [
                        {
                            'type': 'text',
                            'title': 'Vowels = स्वर (Swar)',
                            'content': 'Vowels are sounds you can sing and hold. In Hindi, we call them Swar (स्वर). There are 13 vowels: अ आ इ ई उ ऊ ऋ ए ऐ ओ औ अं अः'
                        },
                        {
                            'type': 'text',
                            'title': 'Consonants = व्यंजन (Vyanjan)',
                            'content': 'Consonants need vowels to make full sounds. In Hindi, we call them Vyanjan (व्यंजन). There are 33 consonants.'
                        }
                    ],
                    'exercises': [
                        {
                            'type': 'multiple_choice',
                            'question': 'What are vowels called in Hindi?',
                            'options': ['व्यंजन (Vyanjan)', 'स्वर (Swar)', 'मात्रा (Matra)', 'अक्षर (Akshar)'],
                            'correct_answer': 1
                        },
                        {
                            'type': 'multiple_choice',
                            'question': 'How many vowels are in Hindi?',
                            'options': ['5', '10', '13', '26'],
                            'correct_answer': 2
                        }
                    ],
                    'summary': 'Hindi has 13 vowels (स्वर) and 33 consonants (व्यंजन).'
                }
            },
        ]

        for lesson_data in m1_lessons:
            Lesson.objects.update_or_create(
                code=lesson_data['code'],
                defaults={'module': m1, **lesson_data}
            )

        # Module 2: Vowels (6 lessons)
        m2 = CurriculumModule.objects.get(code='L1_M2_VOWELS')
        m2_lessons = [
            {
                'code': 'L1_M2_L1',
                'title_english': 'First Vowels: अ आ',
                'title_hindi': 'पहले स्वर: अ आ',
                'title_romanized': 'Pehle Swar: A Aa',
                'lesson_type': 'LEARNING',
                'order': 1,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': True,
                'content': {
                    'introduction': 'Let\'s start with the first two vowels! They\'re like the \'A\' sounds.',
                    'sections': [
                        {
                            'type': 'letter_intro',
                            'letter': 'अ',
                            'transliteration': 'a',
                            'pronunciation_guide': 'Like \'u\' in \'but\' or \'a\' in \'about\'',
                            'example_words': [{'word': 'अब', 'transliteration': 'ab', 'meaning': 'now'}],
                            'mnemonic': 'अ looks like a person bowing - say \'uh\' when you bow!'
                        },
                        {
                            'type': 'letter_intro',
                            'letter': 'आ',
                            'transliteration': 'aa',
                            'pronunciation_guide': 'Like \'a\' in \'father\' - longer than अ',
                            'example_words': [{'word': 'आम', 'transliteration': 'aam', 'meaning': 'mango'}],
                            'mnemonic': 'आ has an extra line - it\'s a LONGER \'aa\' sound!'
                        }
                    ],
                    'exercises': [
                        {
                            'type': 'audio_recognition',
                            'question': 'Which vowel do you hear?',
                            'audio_text': 'आ',
                            'options': ['अ', 'आ'],
                            'correct_answer': 1
                        }
                    ],
                    'summary': 'अ (a) is short like \'uh\', आ (aa) is long like \'aah\'.'
                }
            },
            {
                'code': 'L1_M2_L2',
                'title_english': 'Vowels: इ ई',
                'title_hindi': 'स्वर: इ ई',
                'title_romanized': 'Swar: I Ee',
                'lesson_type': 'LEARNING',
                'order': 2,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': True,
                'content': {
                    'introduction': 'Now let\'s learn the \'E\' sounds of Hindi!',
                    'sections': [
                        {
                            'type': 'letter_intro',
                            'letter': 'इ',
                            'transliteration': 'i',
                            'pronunciation_guide': 'Like \'i\' in \'bit\' - short sound',
                            'example_words': [{'word': 'इधर', 'transliteration': 'idhar', 'meaning': 'here'}]
                        },
                        {
                            'type': 'letter_intro',
                            'letter': 'ई',
                            'transliteration': 'ee',
                            'pronunciation_guide': 'Like \'ee\' in \'feet\' - longer than इ',
                            'example_words': [{'word': 'ईद', 'transliteration': 'Eid', 'meaning': 'Eid festival'}]
                        }
                    ],
                    'summary': 'इ (i) is short like \'ih\', ई (ee) is long like \'ee\'.'
                }
            },
            {
                'code': 'L1_M2_L3',
                'title_english': 'Vowels: उ ऊ',
                'title_hindi': 'स्वर: उ ऊ',
                'title_romanized': 'Swar: U Oo',
                'lesson_type': 'LEARNING',
                'order': 3,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': True,
                'content': {
                    'introduction': 'Time for the \'OO\' sounds!',
                    'sections': [
                        {
                            'type': 'letter_intro',
                            'letter': 'उ',
                            'transliteration': 'u',
                            'pronunciation_guide': 'Like \'u\' in \'put\' - short sound',
                            'example_words': [{'word': 'उल्लू', 'transliteration': 'ullu', 'meaning': 'owl'}]
                        },
                        {
                            'type': 'letter_intro',
                            'letter': 'ऊ',
                            'transliteration': 'oo',
                            'pronunciation_guide': 'Like \'oo\' in \'food\' - longer than उ',
                            'example_words': [{'word': 'ऊँट', 'transliteration': 'oont', 'meaning': 'camel'}]
                        }
                    ],
                    'summary': 'उ (u) is short, ऊ (oo) is long. You now know 6 vowels!'
                }
            },
            {
                'code': 'L1_M2_L4',
                'title_english': 'Vowels: ए ऐ',
                'title_hindi': 'स्वर: ए ऐ',
                'title_romanized': 'Swar: E Ai',
                'lesson_type': 'LEARNING',
                'order': 4,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': True,
                'content': {
                    'introduction': 'These vowels sound like \'ay\' and \'ai\'!',
                    'sections': [
                        {
                            'type': 'letter_intro',
                            'letter': 'ए',
                            'transliteration': 'e',
                            'pronunciation_guide': 'Like \'a\' in \'cake\' or \'ay\' in \'say\'',
                            'example_words': [{'word': 'एक', 'transliteration': 'ek', 'meaning': 'one'}]
                        },
                        {
                            'type': 'letter_intro',
                            'letter': 'ऐ',
                            'transliteration': 'ai',
                            'pronunciation_guide': 'Like \'ai\' in \'air\'',
                            'example_words': [{'word': 'ऐनक', 'transliteration': 'ainak', 'meaning': 'glasses'}]
                        }
                    ],
                    'summary': 'ए (e) sounds like \'ay\', ऐ (ai) sounds like \'ai\' in \'air\'.'
                }
            },
            {
                'code': 'L1_M2_L5',
                'title_english': 'Vowels: ओ औ',
                'title_hindi': 'स्वर: ओ औ',
                'title_romanized': 'Swar: O Au',
                'lesson_type': 'LEARNING',
                'order': 5,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': True,
                'content': {
                    'introduction': 'Almost there! These sound like \'O\' sounds!',
                    'sections': [
                        {
                            'type': 'letter_intro',
                            'letter': 'ओ',
                            'transliteration': 'o',
                            'pronunciation_guide': 'Like \'o\' in \'go\' or \'boat\'',
                            'example_words': [{'word': 'ओस', 'transliteration': 'os', 'meaning': 'dew'}]
                        },
                        {
                            'type': 'letter_intro',
                            'letter': 'औ',
                            'transliteration': 'au',
                            'pronunciation_guide': 'Like \'ow\' in \'cow\'',
                            'example_words': [{'word': 'और', 'transliteration': 'aur', 'meaning': 'and'}]
                        }
                    ],
                    'summary': 'ओ (o) sounds like \'oh\', औ (au) sounds like \'ow\'.'
                }
            },
            {
                'code': 'L1_M2_L6',
                'title_english': 'Special Vowels + Review',
                'title_hindi': 'विशेष स्वर + समीक्षा',
                'title_romanized': 'Vishesh Swar + Sameeksha',
                'lesson_type': 'REVIEW',
                'order': 6,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': True,
                'content': {
                    'introduction': 'The last 3 vowels are special sounds. Let\'s learn them and review all 13!',
                    'sections': [
                        {
                            'type': 'letter_intro',
                            'letter': 'ऋ',
                            'transliteration': 'ri',
                            'pronunciation_guide': 'Like \'ri\' in \'cricket\' - used in Sanskrit words',
                            'example_words': [{'word': 'ऋषि', 'transliteration': 'rishi', 'meaning': 'sage'}]
                        },
                        {
                            'type': 'letter_intro',
                            'letter': 'अं',
                            'transliteration': 'am/an',
                            'pronunciation_guide': 'Nasal sound',
                            'example_words': [{'word': 'अंगूर', 'transliteration': 'angoor', 'meaning': 'grapes'}]
                        },
                        {
                            'type': 'letter_intro',
                            'letter': 'अः',
                            'transliteration': 'ah',
                            'pronunciation_guide': 'Breathy \'ah\' sound',
                            'example_words': [{'word': 'दुःख', 'transliteration': 'dukh', 'meaning': 'sorrow'}]
                        },
                        {
                            'type': 'chart',
                            'title': 'All 13 Vowels!',
                            'content': 'अ आ इ ई उ ऊ ऋ ए ऐ ओ औ अं अः'
                        }
                    ],
                    'exercises': [
                        {
                            'type': 'multiple_choice',
                            'question': 'How many vowels are in Hindi?',
                            'options': ['10', '11', '12', '13'],
                            'correct_answer': 3
                        }
                    ],
                    'summary': '🎉 Congratulations! You learned all 13 Hindi vowels!'
                }
            },
        ]

        for lesson_data in m2_lessons:
            Lesson.objects.update_or_create(
                code=lesson_data['code'],
                defaults={'module': m2, **lesson_data}
            )

        # Module 3: First Words (4 lessons)
        m3 = CurriculumModule.objects.get(code='L1_M3_FIRST_WORDS')
        m3_lessons = [
            {
                'code': 'L1_M3_L1',
                'title_english': 'Family Words',
                'title_hindi': 'परिवार के शब्द',
                'title_romanized': 'Parivaar Ke Shabd',
                'lesson_type': 'LEARNING',
                'order': 1,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': True,
                'content': {
                    'introduction': 'Let\'s learn words for family members!',
                    'vocabulary': [
                        {'word': 'माँ', 'transliteration': 'maa', 'meaning': 'mother'},
                        {'word': 'पापा', 'transliteration': 'papa', 'meaning': 'father'},
                        {'word': 'दादी', 'transliteration': 'daadi', 'meaning': 'grandmother'},
                        {'word': 'दादा', 'transliteration': 'daada', 'meaning': 'grandfather'},
                        {'word': 'भाई', 'transliteration': 'bhai', 'meaning': 'brother'},
                        {'word': 'बहन', 'transliteration': 'behen', 'meaning': 'sister'}
                    ],
                    'summary': 'You learned 6 family words: माँ, पापा, दादी, दादा, भाई, बहन'
                }
            },
            {
                'code': 'L1_M3_L2',
                'title_english': 'Basic Words',
                'title_hindi': 'बुनियादी शब्द',
                'title_romanized': 'Buniyaadi Shabd',
                'lesson_type': 'LEARNING',
                'order': 2,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': True,
                'content': {
                    'introduction': 'These are words you\'ll use every day!',
                    'vocabulary': [
                        {'word': 'हाँ', 'transliteration': 'haan', 'meaning': 'yes'},
                        {'word': 'नहीं', 'transliteration': 'nahin', 'meaning': 'no'},
                        {'word': 'नमस्ते', 'transliteration': 'namaste', 'meaning': 'hello'},
                        {'word': 'धन्यवाद', 'transliteration': 'dhanyavaad', 'meaning': 'thank you'},
                        {'word': 'पानी', 'transliteration': 'paani', 'meaning': 'water'}
                    ],
                    'exercises': [
                        {
                            'type': 'multiple_choice',
                            'question': 'How do you say \'yes\' in Hindi?',
                            'options': ['नहीं', 'हाँ', 'नमस्ते', 'धन्यवाद'],
                            'correct_answer': 1
                        }
                    ],
                    'summary': 'You learned: हाँ, नहीं, नमस्ते, धन्यवाद, पानी'
                }
            },
            {
                'code': 'L1_M3_L3',
                'title_english': 'Food Words',
                'title_hindi': 'खाने के शब्द',
                'title_romanized': 'Khaane Ke Shabd',
                'lesson_type': 'LEARNING',
                'order': 3,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': True,
                'content': {
                    'introduction': 'Let\'s learn food and home words!',
                    'vocabulary': [
                        {'word': 'घर', 'transliteration': 'ghar', 'meaning': 'home'},
                        {'word': 'खाना', 'transliteration': 'khaana', 'meaning': 'food'},
                        {'word': 'दूध', 'transliteration': 'doodh', 'meaning': 'milk'},
                        {'word': 'रोटी', 'transliteration': 'roti', 'meaning': 'bread'},
                        {'word': 'चावल', 'transliteration': 'chaawal', 'meaning': 'rice'}
                    ],
                    'summary': 'You learned: घर, खाना, दूध, रोटी, चावल'
                }
            },
            {
                'code': 'L1_M3_L4',
                'title_english': 'Animals & Fruits',
                'title_hindi': 'जानवर और फल',
                'title_romanized': 'Jaanwar aur Phal',
                'lesson_type': 'LEARNING',
                'order': 4,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': True,
                'content': {
                    'introduction': 'Let\'s learn animals and fruits!',
                    'vocabulary': [
                        {'word': 'सेब', 'transliteration': 'seb', 'meaning': 'apple'},
                        {'word': 'केला', 'transliteration': 'kela', 'meaning': 'banana'},
                        {'word': 'गाय', 'transliteration': 'gaay', 'meaning': 'cow'},
                        {'word': 'कुत्ता', 'transliteration': 'kutta', 'meaning': 'dog'}
                    ],
                    'summary': '🎉 You learned all 20 L1 words!'
                }
            },
        ]

        for lesson_data in m3_lessons:
            Lesson.objects.update_or_create(
                code=lesson_data['code'],
                defaults={'module': m3, **lesson_data}
            )

        # Module 4: Listening Fun (3 lessons)
        m4 = CurriculumModule.objects.get(code='L1_M4_LISTENING')
        m4_lessons = [
            {
                'code': 'L1_M4_L1',
                'title_english': 'Hindi Rhyme: Machhli Jal Ki Rani',
                'title_hindi': 'मछली जल की रानी है',
                'title_romanized': 'Machhli Jal Ki Rani Hai',
                'lesson_type': 'LEARNING',
                'order': 1,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': True,
                'content': {
                    'introduction': 'Let\'s learn a famous Hindi nursery rhyme!',
                    'sections': [
                        {
                            'type': 'song',
                            'title': 'Machhli Jal Ki Rani Hai',
                            'lyrics_hindi': 'मछली जल की रानी है\nजीवन उसका पानी है\nहाथ लगाओ डर जाएगी\nबाहर निकालो मर जाएगी',
                            'lyrics_transliteration': 'Machhli jal ki rani hai\nJeevan uska paani hai',
                            'lyrics_english': 'The fish is the queen of water\nWater is her life'
                        }
                    ],
                    'exercises': [
                        {
                            'type': 'multiple_choice',
                            'question': 'What is the fish called in Hindi?',
                            'options': ['पानी', 'मछली', 'रानी', 'जल'],
                            'correct_answer': 1
                        }
                    ],
                    'summary': 'You learned the song and the word मछली (fish)!'
                }
            },
            {
                'code': 'L1_M4_L2',
                'title_english': 'Counting Song: Ek Do Teen',
                'title_hindi': 'गिनती: एक दो तीन',
                'title_romanized': 'Ginti: Ek Do Teen',
                'lesson_type': 'LEARNING',
                'order': 2,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': True,
                'content': {
                    'introduction': 'Let\'s learn to count in Hindi!',
                    'sections': [
                        {
                            'type': 'song',
                            'title': 'Counting 1-10',
                            'lyrics_hindi': 'एक दो तीन चार\nपाँच छह सात\nआठ नौ दस',
                            'lyrics_english': 'One two three four\nFive six seven\nEight nine ten'
                        }
                    ],
                    'summary': 'You can count 1-10 in Hindi!'
                }
            },
            {
                'code': 'L1_M4_L3',
                'title_english': 'Story Time: Namaste!',
                'title_hindi': 'कहानी: नमस्ते!',
                'title_romanized': 'Kahani: Namaste!',
                'lesson_type': 'STORY',
                'order': 3,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': True,
                'content': {
                    'introduction': 'Let\'s listen to a simple story!',
                    'sections': [
                        {
                            'type': 'story',
                            'title': 'A Day with Family',
                            'pages': [
                                {'hindi': 'नमस्ते! मैं राम हूँ।', 'english': 'Hello! I am Ram.'},
                                {'hindi': 'यह मेरी माँ हैं।', 'english': 'This is my mother.'},
                                {'hindi': 'यह मेरे पापा हैं।', 'english': 'This is my father.'},
                                {'hindi': 'मुझे पानी चाहिए।', 'english': 'I need water.'},
                                {'hindi': 'धन्यवाद, माँ!', 'english': 'Thank you, mom!'}
                            ]
                        }
                    ],
                    'exercises': [
                        {
                            'type': 'comprehension',
                            'question': 'What did Ram ask for?',
                            'options': ['खाना', 'पानी', 'दूध'],
                            'correct_answer': 1
                        }
                    ],
                    'summary': '🎉 You completed Level 1! You know 13 vowels and 20 words!'
                }
            },
        ]

        for lesson_data in m4_lessons:
            Lesson.objects.update_or_create(
                code=lesson_data['code'],
                defaults={'module': m4, **lesson_data}
            )

        self.stdout.write(f'  ✅ Created 16 L1 lessons')

    def seed_l2_modules(self):
        """Create 8 modules for L2."""
        l2 = CurriculumLevel.objects.get(code='L2')

        modules_data = [
            {
                'code': 'L2_M1_KA_GROUP',
                'name_english': 'Ka-Group (क-वर्ग)',
                'name_hindi': 'क-वर्ग',
                'name_romanized': 'Ka Varg',
                'description': 'Learn the first 5 consonants: क ख ग घ ङ',
                'module_type': 'ALPHABET',
                'objectives': ['Recognize and pronounce क ख ग घ ङ', 'Understand aspiration'],
                'emoji': '🔤',
                'order': 1,
                'estimated_minutes': 15,
                'xp_reward': 30,
            },
            {
                'code': 'L2_M2_CHA_GROUP',
                'name_english': 'Cha-Group (च-वर्ग)',
                'name_hindi': 'च-वर्ग',
                'name_romanized': 'Cha Varg',
                'description': 'Learn consonants: च छ ज झ ञ',
                'module_type': 'ALPHABET',
                'objectives': ['Recognize and pronounce च छ ज झ ञ'],
                'emoji': '🔤',
                'order': 2,
                'estimated_minutes': 15,
                'xp_reward': 30,
            },
            {
                'code': 'L2_M3_TA_RETROFLEX',
                'name_english': 'Ta-Group Retroflex (ट-वर्ग)',
                'name_hindi': 'ट-वर्ग',
                'name_romanized': 'Ta Varg Retroflex',
                'description': 'Learn retroflex consonants: ट ठ ड ढ ण',
                'module_type': 'ALPHABET',
                'objectives': ['Recognize retroflex sounds'],
                'emoji': '🔤',
                'order': 3,
                'estimated_minutes': 15,
                'xp_reward': 30,
            },
            {
                'code': 'L2_M4_TA_DENTAL',
                'name_english': 'Ta-Group Dental (त-वर्ग)',
                'name_hindi': 'त-वर्ग',
                'name_romanized': 'Ta Varg Dental',
                'description': 'Learn dental consonants: त थ द ध न',
                'module_type': 'ALPHABET',
                'objectives': ['Recognize dental sounds'],
                'emoji': '🔤',
                'order': 4,
                'estimated_minutes': 15,
                'xp_reward': 30,
            },
            {
                'code': 'L2_M5_PA_GROUP',
                'name_english': 'Pa-Group (प-वर्ग)',
                'name_hindi': 'प-वर्ग',
                'name_romanized': 'Pa Varg',
                'description': 'Learn labial consonants: प फ ब भ म',
                'module_type': 'ALPHABET',
                'objectives': ['Recognize labial sounds'],
                'emoji': '🔤',
                'order': 5,
                'estimated_minutes': 15,
                'xp_reward': 30,
            },
            {
                'code': 'L2_M6_MATRAS',
                'name_english': 'Matras (मात्राएँ)',
                'name_hindi': 'मात्राएँ',
                'name_romanized': 'Matrayen',
                'description': 'Learn how vowels attach to consonants - the key to reading!',
                'module_type': 'ALPHABET',
                'objectives': ['Understand how matras work', 'Apply all 12 matras'],
                'emoji': '🔗',
                'order': 6,
                'estimated_minutes': 25,
                'xp_reward': 50,
            },
            {
                'code': 'L2_M7_REMAINING',
                'name_english': 'Remaining Consonants',
                'name_hindi': 'बाकी व्यंजन',
                'name_romanized': 'Baaki Vyanjan',
                'description': 'Learn: य र ल व श ष स ह',
                'module_type': 'ALPHABET',
                'objectives': ['Complete all 33 consonants'],
                'emoji': '✨',
                'order': 7,
                'estimated_minutes': 20,
                'xp_reward': 40,
            },
            {
                'code': 'L2_M8_READING',
                'name_english': 'Reading & Sentences',
                'name_hindi': 'पढ़ना और वाक्य',
                'name_romanized': 'Padhna aur Vaakya',
                'description': 'Put it all together! Read words and simple sentences.',
                'module_type': 'READING',
                'objectives': ['Read multi-syllable words', 'Understand simple sentences'],
                'emoji': '📖',
                'order': 8,
                'estimated_minutes': 20,
                'xp_reward': 50,
            },
        ]

        for mod_data in modules_data:
            module, created = CurriculumModule.objects.update_or_create(
                code=mod_data['code'],
                defaults={'level': l2, **mod_data}
            )
            status = '✅' if created else '♻️'
            self.stdout.write(f'  {status} {mod_data["name_english"]}')

    def seed_l2_lessons(self):
        """Create lessons for L2 modules."""
        # Ka-Group lessons
        m1 = CurriculumModule.objects.get(code='L2_M1_KA_GROUP')
        ka_lessons = [
            {
                'code': 'L2_M1_L1',
                'title_english': 'Consonants: क ख',
                'title_hindi': 'व्यंजन: क ख',
                'title_romanized': 'Vyanjan: Ka Kha',
                'lesson_type': 'LEARNING',
                'order': 1,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'introduction': 'The first consonants! These sounds come from your throat.',
                    'sections': [
                        {
                            'type': 'letter_intro',
                            'letter': 'क',
                            'transliteration': 'ka',
                            'pronunciation_guide': 'Like \'k\' in \'kite\' - no extra breath',
                            'example_words': [
                                {'word': 'कमल', 'transliteration': 'kamal', 'meaning': 'lotus'},
                                {'word': 'कलम', 'transliteration': 'kalam', 'meaning': 'pen'}
                            ],
                            'mnemonic': 'क looks like a key 🔑'
                        },
                        {
                            'type': 'letter_intro',
                            'letter': 'ख',
                            'transliteration': 'kha',
                            'pronunciation_guide': 'Like \'k\' with a puff of air',
                            'example_words': [
                                {'word': 'खरगोश', 'transliteration': 'khargosh', 'meaning': 'rabbit'},
                                {'word': 'खाना', 'transliteration': 'khaana', 'meaning': 'food'}
                            ],
                            'mnemonic': 'ख has more lines = more breath = \'kh\'!'
                        }
                    ],
                    'exercises': [
                        {
                            'type': 'audio_recognition',
                            'question': 'Which letter has more breath?',
                            'audio_text': 'ख',
                            'options': ['क', 'ख'],
                            'correct_answer': 1
                        }
                    ]
                }
            },
            {
                'code': 'L2_M1_L2',
                'title_english': 'Consonants: ग घ ङ',
                'title_hindi': 'व्यंजन: ग घ ङ',
                'title_romanized': 'Vyanjan: Ga Gha Nga',
                'lesson_type': 'LEARNING',
                'order': 2,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'introduction': 'Three more consonants from Ka-group!',
                    'sections': [
                        {
                            'type': 'letter_intro',
                            'letter': 'ग',
                            'transliteration': 'ga',
                            'example_words': [
                                {'word': 'गाय', 'transliteration': 'gaay', 'meaning': 'cow'},
                                {'word': 'गाना', 'transliteration': 'gaana', 'meaning': 'song'}
                            ]
                        },
                        {
                            'type': 'letter_intro',
                            'letter': 'घ',
                            'transliteration': 'gha',
                            'example_words': [
                                {'word': 'घर', 'transliteration': 'ghar', 'meaning': 'home'},
                                {'word': 'घोड़ा', 'transliteration': 'ghoda', 'meaning': 'horse'}
                            ]
                        },
                        {
                            'type': 'letter_intro',
                            'letter': 'ङ',
                            'transliteration': 'nga',
                            'example_words': [{'word': 'रंग', 'transliteration': 'rang', 'meaning': 'color'}]
                        }
                    ]
                }
            },
            {
                'code': 'L2_M1_L3',
                'title_english': 'Ka-Group Practice',
                'title_hindi': 'क-वर्ग अभ्यास',
                'title_romanized': 'Ka Varg Abhyaas',
                'lesson_type': 'PRACTICE',
                'order': 3,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [
                        {
                            'type': 'chart',
                            'title': 'Ka-Group Complete',
                            'content': ['क (ka)', 'ख (kha)', 'ग (ga)', 'घ (gha)', 'ङ (nga)']
                        }
                    ],
                    'summary': 'You mastered the Ka-group: क ख ग घ ङ!'
                }
            },
        ]

        for lesson_data in ka_lessons:
            Lesson.objects.update_or_create(
                code=lesson_data['code'],
                defaults={'module': m1, **lesson_data}
            )

        # Cha-Group lessons
        m2 = CurriculumModule.objects.get(code='L2_M2_CHA_GROUP')
        cha_lessons = [
            {
                'code': 'L2_M2_L1',
                'title_english': 'Consonants: च छ',
                'title_hindi': 'व्यंजन: च छ',
                'title_romanized': 'Vyanjan: Cha Chha',
                'lesson_type': 'LEARNING',
                'order': 1,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [
                        {
                            'type': 'letter_intro',
                            'letter': 'च',
                            'transliteration': 'cha',
                            'example_words': [{'word': 'चाय', 'transliteration': 'chaay', 'meaning': 'tea'}]
                        },
                        {
                            'type': 'letter_intro',
                            'letter': 'छ',
                            'transliteration': 'chha',
                            'example_words': [{'word': 'छाता', 'transliteration': 'chhaata', 'meaning': 'umbrella'}]
                        }
                    ]
                }
            },
            {
                'code': 'L2_M2_L2',
                'title_english': 'Consonants: ज झ ञ',
                'title_hindi': 'व्यंजन: ज झ ञ',
                'title_romanized': 'Vyanjan: Ja Jha Nya',
                'lesson_type': 'LEARNING',
                'order': 2,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [
                        {
                            'type': 'letter_intro',
                            'letter': 'ज',
                            'transliteration': 'ja',
                            'example_words': [
                                {'word': 'जल', 'transliteration': 'jal', 'meaning': 'water'},
                                {'word': 'जंगल', 'transliteration': 'jungle', 'meaning': 'forest'}
                            ]
                        },
                        {
                            'type': 'letter_intro',
                            'letter': 'झ',
                            'transliteration': 'jha',
                            'example_words': [{'word': 'झंडा', 'transliteration': 'jhanda', 'meaning': 'flag'}]
                        },
                        {
                            'type': 'letter_intro',
                            'letter': 'ञ',
                            'transliteration': 'nya',
                            'example_words': [{'word': 'Used in conjuncts', 'transliteration': 'Rarely standalone'}]
                        }
                    ]
                }
            },
            {
                'code': 'L2_M2_L3',
                'title_english': 'Cha-Group Practice',
                'title_hindi': 'च-वर्ग अभ्यास',
                'title_romanized': 'Cha Varg Abhyaas',
                'lesson_type': 'PRACTICE',
                'order': 3,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [{'type': 'chart', 'content': ['च', 'छ', 'ज', 'झ', 'ञ']}],
                    'summary': 'You mastered the Cha-group: च छ ज झ ञ!'
                }
            },
        ]

        for lesson_data in cha_lessons:
            Lesson.objects.update_or_create(
                code=lesson_data['code'],
                defaults={'module': m2, **lesson_data}
            )

        # Ta-Group Retroflex lessons
        m3 = CurriculumModule.objects.get(code='L2_M3_TA_RETROFLEX')
        ta_retro_lessons = [
            {
                'code': 'L2_M3_L1',
                'title_english': 'Consonants: ट ठ',
                'title_hindi': 'व्यंजन: ट ठ',
                'title_romanized': 'Vyanjan: Ta Tha',
                'lesson_type': 'LEARNING',
                'order': 1,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [
                        {
                            'type': 'letter_intro',
                            'letter': 'ट',
                            'transliteration': 'ṭa',
                            'pronunciation_guide': 'Tongue curls back to touch roof',
                            'example_words': [{'word': 'टमाटर', 'transliteration': 'tamatar', 'meaning': 'tomato'}]
                        },
                        {
                            'type': 'letter_intro',
                            'letter': 'ठ',
                            'transliteration': 'ṭha',
                            'example_words': [{'word': 'ठंडा', 'transliteration': 'thanda', 'meaning': 'cold'}]
                        }
                    ]
                }
            },
            {
                'code': 'L2_M3_L2',
                'title_english': 'Consonants: ड ढ ण',
                'title_hindi': 'व्यंजन: ड ढ ण',
                'title_romanized': 'Vyanjan: Da Dha Na',
                'lesson_type': 'LEARNING',
                'order': 2,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [
                        {'type': 'letter_intro', 'letter': 'ड', 'transliteration': 'ḍa',
                         'example_words': [{'word': 'डर', 'transliteration': 'dar', 'meaning': 'fear'}]},
                        {'type': 'letter_intro', 'letter': 'ढ', 'transliteration': 'ḍha',
                         'example_words': [{'word': 'ढोल', 'transliteration': 'dhol', 'meaning': 'drum'}]},
                        {'type': 'letter_intro', 'letter': 'ण', 'transliteration': 'ṇa',
                         'example_words': [{'word': 'गुण', 'transliteration': 'gun', 'meaning': 'quality'}]}
                    ]
                }
            },
            {
                'code': 'L2_M3_L3',
                'title_english': 'Ta-Retroflex Practice',
                'title_hindi': 'ट-वर्ग अभ्यास',
                'title_romanized': 'Ta Varg Abhyaas',
                'lesson_type': 'PRACTICE',
                'order': 3,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'summary': 'You mastered the Ta-retroflex group: ट ठ ड ढ ण!'
                }
            },
        ]

        for lesson_data in ta_retro_lessons:
            Lesson.objects.update_or_create(
                code=lesson_data['code'],
                defaults={'module': m3, **lesson_data}
            )

        # Ta-Group Dental lessons
        m4 = CurriculumModule.objects.get(code='L2_M4_TA_DENTAL')
        ta_dental_lessons = [
            {
                'code': 'L2_M4_L1',
                'title_english': 'Consonants: त थ',
                'title_hindi': 'व्यंजन: त थ',
                'title_romanized': 'Vyanjan: Ta Tha',
                'lesson_type': 'LEARNING',
                'order': 1,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [
                        {
                            'type': 'letter_intro',
                            'letter': 'त',
                            'transliteration': 'ta',
                            'pronunciation_guide': 'Tongue touches back of upper teeth',
                            'example_words': [{'word': 'तारा', 'transliteration': 'taara', 'meaning': 'star'}]
                        },
                        {
                            'type': 'letter_intro',
                            'letter': 'थ',
                            'transliteration': 'tha',
                            'example_words': [{'word': 'थाली', 'transliteration': 'thaali', 'meaning': 'plate'}]
                        }
                    ]
                }
            },
            {
                'code': 'L2_M4_L2',
                'title_english': 'Consonants: द ध न',
                'title_hindi': 'व्यंजन: द ध न',
                'title_romanized': 'Vyanjan: Da Dha Na',
                'lesson_type': 'LEARNING',
                'order': 2,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [
                        {'type': 'letter_intro', 'letter': 'द', 'transliteration': 'da',
                         'example_words': [{'word': 'दूध', 'transliteration': 'doodh', 'meaning': 'milk'}]},
                        {'type': 'letter_intro', 'letter': 'ध', 'transliteration': 'dha',
                         'example_words': [{'word': 'धन', 'transliteration': 'dhan', 'meaning': 'wealth'}]},
                        {'type': 'letter_intro', 'letter': 'न', 'transliteration': 'na',
                         'example_words': [{'word': 'नमस्ते', 'transliteration': 'namaste', 'meaning': 'hello'}]}
                    ]
                }
            },
            {
                'code': 'L2_M4_L3',
                'title_english': 'Ta-Dental Practice',
                'title_hindi': 'त-वर्ग अभ्यास',
                'title_romanized': 'Ta Varg Abhyaas',
                'lesson_type': 'PRACTICE',
                'order': 3,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {'summary': 'You mastered the Ta-dental group: त थ द ध न!'}
            },
        ]

        for lesson_data in ta_dental_lessons:
            Lesson.objects.update_or_create(
                code=lesson_data['code'],
                defaults={'module': m4, **lesson_data}
            )

        # Pa-Group lessons
        m5 = CurriculumModule.objects.get(code='L2_M5_PA_GROUP')
        pa_lessons = [
            {
                'code': 'L2_M5_L1',
                'title_english': 'Consonants: प फ',
                'title_hindi': 'व्यंजन: प फ',
                'title_romanized': 'Vyanjan: Pa Pha',
                'lesson_type': 'LEARNING',
                'order': 1,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [
                        {'type': 'letter_intro', 'letter': 'प', 'transliteration': 'pa',
                         'example_words': [{'word': 'पानी', 'transliteration': 'paani', 'meaning': 'water'}]},
                        {'type': 'letter_intro', 'letter': 'फ', 'transliteration': 'pha',
                         'example_words': [{'word': 'फल', 'transliteration': 'phal', 'meaning': 'fruit'}]}
                    ]
                }
            },
            {
                'code': 'L2_M5_L2',
                'title_english': 'Consonants: ब भ म',
                'title_hindi': 'व्यंजन: ब भ म',
                'title_romanized': 'Vyanjan: Ba Bha Ma',
                'lesson_type': 'LEARNING',
                'order': 2,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [
                        {'type': 'letter_intro', 'letter': 'ब', 'transliteration': 'ba',
                         'example_words': [{'word': 'बस', 'transliteration': 'bas', 'meaning': 'bus'}]},
                        {'type': 'letter_intro', 'letter': 'भ', 'transliteration': 'bha',
                         'example_words': [{'word': 'भालू', 'transliteration': 'bhaaloo', 'meaning': 'bear'}]},
                        {'type': 'letter_intro', 'letter': 'म', 'transliteration': 'ma',
                         'example_words': [{'word': 'माँ', 'transliteration': 'maa', 'meaning': 'mother'}]}
                    ]
                }
            },
            {
                'code': 'L2_M5_L3',
                'title_english': 'All Consonant Groups Review',
                'title_hindi': 'सभी व्यंजन समीक्षा',
                'title_romanized': 'Sabhi Vyanjan Sameeksha',
                'lesson_type': 'REVIEW',
                'order': 3,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [{
                        'type': 'chart',
                        'title': '25 Consonants - The Main Groups',
                        'content': [
                            ['क-वर्ग', 'क ख ग घ ङ'],
                            ['च-वर्ग', 'च छ ज झ ञ'],
                            ['ट-वर्ग', 'ट ठ ड ढ ण'],
                            ['त-वर्ग', 'त थ द ध न'],
                            ['प-वर्ग', 'प फ ब भ म']
                        ]
                    }],
                    'summary': 'You learned 25 consonants in 5 groups!'
                }
            },
        ]

        for lesson_data in pa_lessons:
            Lesson.objects.update_or_create(
                code=lesson_data['code'],
                defaults={'module': m5, **lesson_data}
            )

        # Matras module
        m6 = CurriculumModule.objects.get(code='L2_M6_MATRAS')
        matra_lessons = [
            {
                'code': 'L2_M6_L1',
                'title_english': 'What are Matras?',
                'title_hindi': 'मात्राएँ क्या हैं?',
                'title_romanized': 'Matrayen Kya Hain?',
                'lesson_type': 'LEARNING',
                'order': 1,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'introduction': 'Matras are vowel symbols that attach to consonants!',
                    'sections': [
                        {
                            'type': 'concept',
                            'title': 'Vowels → Matras',
                            'content': 'When vowels join consonants, they become matras. Example: क + आ = का'
                        },
                        {
                            'type': 'table',
                            'title': 'Vowels and Their Matra Forms',
                            'content': [
                                ['Vowel', 'Matra', 'With क', 'Sound'],
                                ['अ', '(none)', 'क', 'ka'],
                                ['आ', 'ा', 'का', 'kaa'],
                                ['इ', 'ि', 'कि', 'ki'],
                                ['ई', 'ी', 'की', 'kee'],
                                ['उ', 'ु', 'कु', 'ku'],
                                ['ऊ', 'ू', 'कू', 'koo'],
                                ['ए', 'े', 'के', 'ke'],
                                ['ऐ', 'ै', 'कै', 'kai'],
                                ['ओ', 'ो', 'को', 'ko'],
                                ['औ', 'ौ', 'कौ', 'kau']
                            ]
                        }
                    ],
                    'summary': 'अ has no matra - it\'s the default. क alone = \'ka\'!'
                }
            },
            {
                'code': 'L2_M6_L2',
                'title_english': 'Aa-Matra (ा)',
                'title_hindi': 'आ की मात्रा',
                'title_romanized': 'Aa Ki Matra',
                'lesson_type': 'LEARNING',
                'order': 2,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [
                        {
                            'type': 'matra_intro',
                            'matra': 'ा',
                            'vowel': 'आ',
                            'position': 'Right side of consonant',
                            'examples': [
                                {'base': 'क', 'with_matra': 'का', 'word': 'काला', 'meaning': 'black'},
                                {'base': 'म', 'with_matra': 'मा', 'word': 'माँ', 'meaning': 'mother'},
                                {'base': 'प', 'with_matra': 'पा', 'word': 'पानी', 'meaning': 'water'}
                            ]
                        }
                    ]
                }
            },
            {
                'code': 'L2_M6_L3',
                'title_english': 'I-Matras (ि ी)',
                'title_hindi': 'इ और ई की मात्रा',
                'title_romanized': 'I aur Ee Ki Matra',
                'lesson_type': 'LEARNING',
                'order': 3,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [
                        {
                            'type': 'matra_intro',
                            'matra': 'ि',
                            'vowel': 'इ',
                            'position': 'LEFT side of consonant (special!)',
                            'examples': [{'base': 'द', 'with_matra': 'दि', 'word': 'दिन', 'meaning': 'day'}],
                            'tip': 'This is the ONLY matra that goes to the LEFT!'
                        },
                        {
                            'type': 'matra_intro',
                            'matra': 'ी',
                            'vowel': 'ई',
                            'position': 'Right side',
                            'examples': [{'base': 'न', 'with_matra': 'नी', 'word': 'नीला', 'meaning': 'blue'}]
                        }
                    ]
                }
            },
            {
                'code': 'L2_M6_L4',
                'title_english': 'U-Matras (ु ू)',
                'title_hindi': 'उ और ऊ की मात्रा',
                'title_romanized': 'U aur Oo Ki Matra',
                'lesson_type': 'LEARNING',
                'order': 4,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [
                        {
                            'type': 'matra_intro',
                            'matra': 'ु',
                            'vowel': 'उ',
                            'position': 'Below the consonant',
                            'examples': [{'base': 'क', 'with_matra': 'कु', 'word': 'कुत्ता', 'meaning': 'dog'}]
                        },
                        {
                            'type': 'matra_intro',
                            'matra': 'ू',
                            'vowel': 'ऊ',
                            'position': 'Below (longer curve)',
                            'examples': [{'base': 'फ', 'with_matra': 'फू', 'word': 'फूल', 'meaning': 'flower'}]
                        }
                    ]
                }
            },
            {
                'code': 'L2_M6_L5',
                'title_english': 'E/O Matras (े ै ो ौ)',
                'title_hindi': 'ए ऐ ओ औ की मात्राएँ',
                'title_romanized': 'E Ai O Au Ki Matrayen',
                'lesson_type': 'LEARNING',
                'order': 5,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [
                        {'type': 'matra_intro', 'matra': 'े', 'vowel': 'ए', 'position': 'Above (slanted line)',
                         'examples': [{'word': 'केला', 'meaning': 'banana'}]},
                        {'type': 'matra_intro', 'matra': 'ै', 'vowel': 'ऐ', 'position': 'Above (two slanted lines)',
                         'examples': [{'word': 'बैल', 'meaning': 'ox'}]},
                        {'type': 'matra_intro', 'matra': 'ो', 'vowel': 'ओ', 'position': 'Right side + above',
                         'examples': [{'word': 'रोटी', 'meaning': 'bread'}]},
                        {'type': 'matra_intro', 'matra': 'ौ', 'vowel': 'औ', 'position': 'Right + two lines above',
                         'examples': [{'word': 'कौआ', 'meaning': 'crow'}]}
                    ],
                    'summary': 'You learned all 12 matras! 🎉'
                }
            },
        ]

        for lesson_data in matra_lessons:
            Lesson.objects.update_or_create(
                code=lesson_data['code'],
                defaults={'module': m6, **lesson_data}
            )

        # Remaining Consonants module
        m7 = CurriculumModule.objects.get(code='L2_M7_REMAINING')
        remaining_lessons = [
            {
                'code': 'L2_M7_L1',
                'title_english': 'Semi-Vowels: य र ल व',
                'title_hindi': 'अन्तःस्थ: य र ल व',
                'title_romanized': 'Antahstha: Ya Ra La Va',
                'lesson_type': 'LEARNING',
                'order': 1,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [
                        {'type': 'letter_intro', 'letter': 'य', 'transliteration': 'ya',
                         'example_words': [{'word': 'याद', 'meaning': 'memory'}]},
                        {'type': 'letter_intro', 'letter': 'र', 'transliteration': 'ra',
                         'pronunciation_guide': 'Rolled \'r\'',
                         'example_words': [{'word': 'राम', 'meaning': 'Ram'}]},
                        {'type': 'letter_intro', 'letter': 'ल', 'transliteration': 'la',
                         'example_words': [{'word': 'लाल', 'meaning': 'red'}]},
                        {'type': 'letter_intro', 'letter': 'व', 'transliteration': 'va/wa',
                         'example_words': [{'word': 'वन', 'meaning': 'forest'}]}
                    ]
                }
            },
            {
                'code': 'L2_M7_L2',
                'title_english': 'Sibilants: श ष स',
                'title_hindi': 'ऊष्म: श ष स',
                'title_romanized': 'Ushma: Sha Sha Sa',
                'lesson_type': 'LEARNING',
                'order': 2,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [
                        {'type': 'letter_intro', 'letter': 'श', 'transliteration': 'sha',
                         'example_words': [{'word': 'शेर', 'meaning': 'lion'}]},
                        {'type': 'letter_intro', 'letter': 'ष', 'transliteration': 'sha',
                         'pronunciation_guide': 'Retroflex \'sh\''},
                        {'type': 'letter_intro', 'letter': 'स', 'transliteration': 'sa',
                         'example_words': [{'word': 'सेब', 'meaning': 'apple'}]}
                    ]
                }
            },
            {
                'code': 'L2_M7_L3',
                'title_english': 'The Final Consonant: ह',
                'title_hindi': 'अंतिम व्यंजन: ह',
                'title_romanized': 'Antim Vyanjan: Ha',
                'lesson_type': 'LEARNING',
                'order': 3,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [
                        {'type': 'letter_intro', 'letter': 'ह', 'transliteration': 'ha',
                         'example_words': [
                             {'word': 'हाथ', 'meaning': 'hand'},
                             {'word': 'हाथी', 'meaning': 'elephant'}
                         ]},
                        {
                            'type': 'celebration',
                            'title': '🎉 You Know All 33 Consonants!',
                            'content': 'Congratulations!'
                        }
                    ]
                }
            },
            {
                'code': 'L2_M7_L4',
                'title_english': 'Complete Consonant Chart',
                'title_hindi': 'पूर्ण व्यंजन चार्ट',
                'title_romanized': 'Poorn Vyanjan Chart',
                'lesson_type': 'REVIEW',
                'order': 4,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [{
                        'type': 'chart',
                        'title': 'All 33 Consonants',
                        'content': [
                            ['क-वर्ग', 'क ख ग घ ङ', 'Throat'],
                            ['च-वर्ग', 'च छ ज झ ञ', 'Palate'],
                            ['ट-वर्ग', 'ट ठ ड ढ ण', 'Retroflex'],
                            ['त-वर्ग', 'त थ द ध न', 'Dental'],
                            ['प-वर्ग', 'प फ ब भ म', 'Lips'],
                            ['Semi-vowels', 'य र ल व', 'Mixed'],
                            ['Sibilants', 'श ष स', 'Hissing'],
                            ['Aspirate', 'ह', 'Breath']
                        ]
                    }],
                    'summary': 'You mastered all 33 consonants!'
                }
            },
        ]

        for lesson_data in remaining_lessons:
            Lesson.objects.update_or_create(
                code=lesson_data['code'],
                defaults={'module': m7, **lesson_data}
            )

        # Reading module
        m8 = CurriculumModule.objects.get(code='L2_M8_READING')
        reading_lessons = [
            {
                'code': 'L2_M8_L1',
                'title_english': 'Reading Two-Letter Words',
                'title_hindi': 'दो अक्षर के शब्द',
                'title_romanized': 'Do Akshar Ke Shabd',
                'lesson_type': 'PRACTICE',
                'order': 1,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [{
                        'type': 'word_reading',
                        'words': [
                            {'word': 'घर', 'breakdown': 'घ + र', 'meaning': 'home'},
                            {'word': 'जल', 'breakdown': 'ज + ल', 'meaning': 'water'},
                            {'word': 'फल', 'breakdown': 'फ + ल', 'meaning': 'fruit'},
                            {'word': 'वन', 'breakdown': 'व + न', 'meaning': 'forest'},
                            {'word': 'कब', 'breakdown': 'क + ब', 'meaning': 'when'}
                        ]
                    }]
                }
            },
            {
                'code': 'L2_M8_L2',
                'title_english': 'Reading with Matras',
                'title_hindi': 'मात्राओं के साथ पढ़ना',
                'title_romanized': 'Matraon Ke Saath Padhna',
                'lesson_type': 'PRACTICE',
                'order': 2,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [{
                        'type': 'word_reading',
                        'words': [
                            {'word': 'नाम', 'breakdown': 'न + ा + म', 'meaning': 'name'},
                            {'word': 'काम', 'breakdown': 'क + ा + म', 'meaning': 'work'},
                            {'word': 'दूध', 'breakdown': 'द + ू + ध', 'meaning': 'milk'},
                            {'word': 'पीला', 'breakdown': 'प + ी + ल + ा', 'meaning': 'yellow'},
                            {'word': 'नीला', 'breakdown': 'न + ी + ल + ा', 'meaning': 'blue'},
                            {'word': 'केला', 'breakdown': 'क + े + ल + ा', 'meaning': 'banana'}
                        ]
                    }]
                }
            },
            {
                'code': 'L2_M8_L3',
                'title_english': 'Simple Sentences',
                'title_hindi': 'सरल वाक्य',
                'title_romanized': 'Saral Vaakya',
                'lesson_type': 'LEARNING',
                'order': 3,
                'estimated_minutes': 5,
                'points_available': 10,
                'is_free': False,
                'content': {
                    'sections': [{
                        'type': 'sentence_reading',
                        'sentences': [
                            {'hindi': 'यह घर है।', 'transliteration': 'Yah ghar hai.', 'english': 'This is a house.'},
                            {'hindi': 'वह गाय है।', 'transliteration': 'Vah gaay hai.', 'english': 'That is a cow.'},
                            {'hindi': 'मेरा नाम राम है।', 'transliteration': 'Mera naam Ram hai.', 'english': 'My name is Ram.'},
                            {'hindi': 'दूध सफ़ेद है।', 'transliteration': 'Doodh safed hai.', 'english': 'Milk is white.'},
                            {'hindi': 'सेब लाल है।', 'transliteration': 'Seb laal hai.', 'english': 'Apple is red.'}
                        ]
                    },
                    {
                        'type': 'grammar_tip',
                        'title': 'Hindi Sentence Pattern',
                        'content': 'Hindi sentences end with the verb! Subject + Object + Verb'
                    }]
                }
            },
            {
                'code': 'L2_M8_L4',
                'title_english': 'Level 2 Final Review',
                'title_hindi': 'Level 2 अंतिम समीक्षा',
                'title_romanized': 'Level 2 Antim Sameeksha',
                'lesson_type': 'REVIEW',
                'order': 4,
                'estimated_minutes': 5,
                'points_available': 20,
                'is_free': False,
                'content': {
                    'sections': [{
                        'type': 'summary',
                        'content': [
                            '✅ All 33 consonants (व्यंजन)',
                            '✅ All 12 matras (मात्राएँ)',
                            '✅ 50 new vocabulary words',
                            '✅ Reading simple words',
                            '✅ Understanding basic sentences'
                        ]
                    }],
                    'summary': '🎉 You completed Level 2! You can now read Hindi!'
                }
            },
        ]

        for lesson_data in reading_lessons:
            Lesson.objects.update_or_create(
                code=lesson_data['code'],
                defaults={'module': m8, **lesson_data}
            )

        self.stdout.write(f'  ✅ Created 28 L2 lessons')

    def seed_vocabulary(self):
        """Seed 70 vocabulary words - 20 L1, 50 L2."""
        # Get or create themes
        language = Child.Language.HINDI

        # Create themes if they don't exist
        themes_data = [
            {'name': 'Family', 'name_native': 'परिवार', 'icon': '👨‍👩‍👧‍👦', 'level': 1, 'order': 1},
            {'name': 'Basics', 'name_native': 'मूल शब्द', 'icon': '📌', 'level': 1, 'order': 2},
            {'name': 'Food', 'name_native': 'खाना', 'icon': '🍽️', 'level': 1, 'order': 3},
            {'name': 'Fruits', 'name_native': 'फल', 'icon': '🍎', 'level': 1, 'order': 4},
            {'name': 'Animals', 'name_native': 'जानवर', 'icon': '🐾', 'level': 1, 'order': 5},
            {'name': 'Colors', 'name_native': 'रंग', 'icon': '🎨', 'level': 2, 'order': 6},
            {'name': 'Numbers', 'name_native': 'संख्याएँ', 'icon': '🔢', 'level': 2, 'order': 7},
            {'name': 'Body Parts', 'name_native': 'शरीर के अंग', 'icon': '🫀', 'level': 2, 'order': 8},
            {'name': 'Actions', 'name_native': 'क्रियाएँ', 'icon': '🏃', 'level': 2, 'order': 9},
        ]

        themes = {}
        for t_data in themes_data:
            theme, _ = VocabularyTheme.objects.update_or_create(
                language=language,
                name=t_data['name'],
                defaults=t_data
            )
            themes[t_data['name']] = theme

        # L1 Words (20)
        l1_words = [
            # Family (6)
            ('Family', 'माँ', 'maa', 'mother', 'NOUN', 'F'),
            ('Family', 'पापा', 'papa', 'father', 'NOUN', 'M'),
            ('Family', 'दादी', 'daadi', 'grandmother', 'NOUN', 'F'),
            ('Family', 'दादा', 'daada', 'grandfather', 'NOUN', 'M'),
            ('Family', 'भाई', 'bhai', 'brother', 'NOUN', 'M'),
            ('Family', 'बहन', 'behen', 'sister', 'NOUN', 'F'),
            # Basics (5)
            ('Basics', 'हाँ', 'haan', 'yes', 'OTHER', 'NONE'),
            ('Basics', 'नहीं', 'nahin', 'no', 'OTHER', 'NONE'),
            ('Basics', 'नमस्ते', 'namaste', 'hello', 'OTHER', 'NONE'),
            ('Basics', 'धन्यवाद', 'dhanyavaad', 'thank you', 'OTHER', 'NONE'),
            ('Basics', 'पानी', 'paani', 'water', 'NOUN', 'M'),
            # Food (5)
            ('Food', 'घर', 'ghar', 'home', 'NOUN', 'M'),
            ('Food', 'खाना', 'khaana', 'food', 'NOUN', 'M'),
            ('Food', 'दूध', 'doodh', 'milk', 'NOUN', 'M'),
            ('Food', 'रोटी', 'roti', 'bread', 'NOUN', 'F'),
            ('Food', 'चावल', 'chaawal', 'rice', 'NOUN', 'M'),
            # Fruits (2)
            ('Fruits', 'सेब', 'seb', 'apple', 'NOUN', 'M'),
            ('Fruits', 'केला', 'kela', 'banana', 'NOUN', 'M'),
            # Animals (2)
            ('Animals', 'गाय', 'gaay', 'cow', 'NOUN', 'F'),
            ('Animals', 'कुत्ता', 'kutta', 'dog', 'NOUN', 'M'),
        ]

        l1_count = 0
        for theme_name, word, roman, trans, pos, gender in l1_words:
            _, created = VocabularyWord.objects.update_or_create(
                theme=themes[theme_name],
                word=word,
                defaults={
                    'romanization': roman,
                    'translation': trans,
                    'part_of_speech': pos,
                    'gender': gender,
                    'difficulty': 1,
                    'order': l1_count
                }
            )
            if created:
                l1_count += 1

        # L2 Words (50)
        l2_words = [
            # Colors (10)
            ('Colors', 'लाल', 'laal', 'red', 'ADJECTIVE', 'NONE'),
            ('Colors', 'नीला', 'neela', 'blue', 'ADJECTIVE', 'M'),
            ('Colors', 'पीला', 'peela', 'yellow', 'ADJECTIVE', 'M'),
            ('Colors', 'हरा', 'hara', 'green', 'ADJECTIVE', 'M'),
            ('Colors', 'काला', 'kaala', 'black', 'ADJECTIVE', 'M'),
            ('Colors', 'सफ़ेद', 'safed', 'white', 'ADJECTIVE', 'NONE'),
            ('Colors', 'नारंगी', 'naarangi', 'orange', 'ADJECTIVE', 'NONE'),
            ('Colors', 'गुलाबी', 'gulaabi', 'pink', 'ADJECTIVE', 'NONE'),
            ('Colors', 'बैंगनी', 'baingani', 'purple', 'ADJECTIVE', 'NONE'),
            ('Colors', 'भूरा', 'bhoora', 'brown', 'ADJECTIVE', 'M'),
            # Numbers (10)
            ('Numbers', 'एक', 'ek', 'one', 'NUMBER', 'NONE'),
            ('Numbers', 'दो', 'do', 'two', 'NUMBER', 'NONE'),
            ('Numbers', 'तीन', 'teen', 'three', 'NUMBER', 'NONE'),
            ('Numbers', 'चार', 'chaar', 'four', 'NUMBER', 'NONE'),
            ('Numbers', 'पाँच', 'paanch', 'five', 'NUMBER', 'NONE'),
            ('Numbers', 'छह', 'chhah', 'six', 'NUMBER', 'NONE'),
            ('Numbers', 'सात', 'saat', 'seven', 'NUMBER', 'NONE'),
            ('Numbers', 'आठ', 'aath', 'eight', 'NUMBER', 'NONE'),
            ('Numbers', 'नौ', 'nau', 'nine', 'NUMBER', 'NONE'),
            ('Numbers', 'दस', 'das', 'ten', 'NUMBER', 'NONE'),
            # Animals (10)
            ('Animals', 'बिल्ली', 'billi', 'cat', 'NOUN', 'F'),
            ('Animals', 'घोड़ा', 'ghoda', 'horse', 'NOUN', 'M'),
            ('Animals', 'हाथी', 'haathi', 'elephant', 'NOUN', 'M'),
            ('Animals', 'शेर', 'sher', 'lion', 'NOUN', 'M'),
            ('Animals', 'बंदर', 'bandar', 'monkey', 'NOUN', 'M'),
            ('Animals', 'चिड़िया', 'chidiya', 'bird', 'NOUN', 'F'),
            ('Animals', 'मछली', 'machhli', 'fish', 'NOUN', 'F'),
            ('Animals', 'खरगोश', 'khargosh', 'rabbit', 'NOUN', 'M'),
            ('Animals', 'कौआ', 'kauaa', 'crow', 'NOUN', 'M'),
            ('Animals', 'तितली', 'titli', 'butterfly', 'NOUN', 'F'),
            # Body Parts (10)
            ('Body Parts', 'सिर', 'sir', 'head', 'NOUN', 'M'),
            ('Body Parts', 'आँख', 'aankh', 'eye', 'NOUN', 'F'),
            ('Body Parts', 'नाक', 'naak', 'nose', 'NOUN', 'F'),
            ('Body Parts', 'कान', 'kaan', 'ear', 'NOUN', 'M'),
            ('Body Parts', 'मुँह', 'munh', 'mouth', 'NOUN', 'M'),
            ('Body Parts', 'हाथ', 'haath', 'hand', 'NOUN', 'M'),
            ('Body Parts', 'पैर', 'pair', 'foot', 'NOUN', 'M'),
            ('Body Parts', 'पेट', 'pet', 'stomach', 'NOUN', 'M'),
            ('Body Parts', 'बाल', 'baal', 'hair', 'NOUN', 'M'),
            ('Body Parts', 'दाँत', 'daant', 'teeth', 'NOUN', 'M'),
            # Actions (10)
            ('Actions', 'खाना', 'khaana', 'to eat', 'VERB', 'NONE'),
            ('Actions', 'पीना', 'peena', 'to drink', 'VERB', 'NONE'),
            ('Actions', 'सोना', 'sona', 'to sleep', 'VERB', 'NONE'),
            ('Actions', 'खेलना', 'khelna', 'to play', 'VERB', 'NONE'),
            ('Actions', 'पढ़ना', 'padhna', 'to read', 'VERB', 'NONE'),
            ('Actions', 'लिखना', 'likhna', 'to write', 'VERB', 'NONE'),
            ('Actions', 'देखना', 'dekhna', 'to see', 'VERB', 'NONE'),
            ('Actions', 'सुनना', 'sunna', 'to listen', 'VERB', 'NONE'),
            ('Actions', 'बोलना', 'bolna', 'to speak', 'VERB', 'NONE'),
            ('Actions', 'चलना', 'chalna', 'to walk', 'VERB', 'NONE'),
        ]

        l2_count = 0
        for theme_name, word, roman, trans, pos, gender in l2_words:
            _, created = VocabularyWord.objects.update_or_create(
                theme=themes[theme_name],
                word=word,
                defaults={
                    'romanization': roman,
                    'translation': trans,
                    'part_of_speech': pos,
                    'gender': gender,
                    'difficulty': 2,
                    'order': 20 + l2_count
                }
            )
            if created:
                l2_count += 1

        self.stdout.write(f'  ✅ Seeded {l1_count} L1 words + {l2_count} L2 words = {l1_count + l2_count} total')

    def seed_stories(self):
        """Seed 10 stories - 3 L1, 7 L2."""
        language = Child.Language.HINDI

        stories_data = [
            # L1 Stories (3)
            {
                'storyweaver_id': 'bm_l1_namaste',
                'title': 'Namaste!',
                'title_hindi': 'नमस्ते!',
                'title_romanized': 'Namaste!',
                'level': 1,
                'is_l1_content': True,
                'theme': 'family',
                'tier': 'free',
                'xp_reward': 15,
                'estimated_minutes': 2,
                'moral_english': 'Family is important.',
                'moral_hindi': 'परिवार सबसे महत्वपूर्ण है।',
                'pages': [
                    {'hindi': 'नमस्ते! मैं राम हूँ।', 'english': 'Hello! I am Ram.'},
                    {'hindi': 'यह मेरी माँ हैं।', 'english': 'This is my mother.'},
                    {'hindi': 'यह मेरे पापा हैं।', 'english': 'This is my father.'},
                    {'hindi': 'मुझे पानी चाहिए।', 'english': 'I need water.'},
                    {'hindi': 'धन्यवाद, माँ!', 'english': 'Thank you, mom!'},
                ]
            },
            {
                'storyweaver_id': 'bm_l1_family',
                'title': 'My Family',
                'title_hindi': 'मेरा परिवार',
                'title_romanized': 'Mera Parivaar',
                'level': 1,
                'is_l1_content': True,
                'theme': 'family',
                'tier': 'free',
                'xp_reward': 15,
                'estimated_minutes': 2,
                'moral_english': 'Love your family.',
                'moral_hindi': 'अपने परिवार से प्यार करो।',
                'pages': [
                    {'hindi': 'यह मेरा परिवार है।', 'english': 'This is my family.'},
                    {'hindi': 'मेरी माँ अच्छी हैं।', 'english': 'My mother is nice.'},
                    {'hindi': 'दादी कहानी सुनाती हैं।', 'english': 'Grandmother tells stories.'},
                    {'hindi': 'मेरा भाई खेलता है।', 'english': 'My brother plays.'},
                    {'hindi': 'मुझे अपना परिवार बहुत पसंद है!', 'english': 'I love my family!'},
                ]
            },
            {
                'storyweaver_id': 'bm_l1_fruits',
                'title': 'Colorful Fruits',
                'title_hindi': 'रंग-बिरंगे फल',
                'title_romanized': 'Rang-Birange Phal',
                'level': 1,
                'is_l1_content': True,
                'theme': 'fruits',
                'tier': 'free',
                'xp_reward': 15,
                'estimated_minutes': 2,
                'moral_english': 'Eating fruits is healthy.',
                'moral_hindi': 'फल खाना स्वास्थ्य के लिए अच्छा है।',
                'pages': [
                    {'hindi': 'देखो! कितने फल हैं!', 'english': 'Look! So many fruits!'},
                    {'hindi': 'सेब लाल है।', 'english': 'The apple is red.'},
                    {'hindi': 'केला पीला है।', 'english': 'The banana is yellow.'},
                    {'hindi': 'फल खाना अच्छा है।', 'english': 'Eating fruits is good.'},
                ]
            },
            # L2 Stories (7)
            {
                'storyweaver_id': 'bm_l2_fox',
                'title': 'The Clever Fox',
                'title_hindi': 'चतुर लोमड़ी',
                'title_romanized': 'Chatur Lomdi',
                'level': 2,
                'is_l1_content': False,
                'theme': 'moral',
                'tier': 'standard',
                'xp_reward': 20,
                'estimated_minutes': 3,
                'moral_english': "Don't be fooled by flattery.",
                'moral_hindi': 'चापलूसी में मत आओ!',
                'pages': [
                    {'hindi': 'एक कौआ था। उसके पास पनीर था।', 'english': 'There was a crow with cheese.'},
                    {'hindi': 'एक लोमड़ी आई।', 'english': 'A fox came.'},
                    {'hindi': "लोमड़ी बोली - 'कौआ जी, आप सुंदर हो!'", 'english': "'Dear crow, you are beautiful!'"},
                    {'hindi': "'कृपया गाना गाओ!'", 'english': "'Please sing!'"},
                    {'hindi': 'कौए ने मुँह खोला। पनीर गिर गया!', 'english': 'Crow opened mouth. Cheese fell!'},
                    {'hindi': 'सीख: चापलूसी में मत आओ!', 'english': "Moral: Don't be fooled by flattery!"},
                ]
            },
            {
                'storyweaver_id': 'bm_l2_crow',
                'title': 'The Thirsty Crow',
                'title_hindi': 'प्यासा कौआ',
                'title_romanized': 'Pyaasa Kauaa',
                'level': 2,
                'is_l1_content': False,
                'theme': 'moral',
                'tier': 'standard',
                'xp_reward': 20,
                'estimated_minutes': 3,
                'moral_english': "Where there's a will, there's a way.",
                'moral_hindi': 'जहाँ चाह वहाँ राह!',
                'pages': [
                    {'hindi': 'गर्मी का दिन था। एक कौआ प्यासा था।', 'english': 'Hot day. A crow was thirsty.'},
                    {'hindi': 'उसने एक घड़ा देखा। पानी नीचे था।', 'english': 'He saw a pot. Water was low.'},
                    {'hindi': 'कौए को उपाय सूझा!', 'english': 'Crow got an idea!'},
                    {'hindi': 'उसने पत्थर डाले। पानी ऊपर आया।', 'english': 'He dropped stones. Water rose.'},
                    {'hindi': 'कौए ने पानी पिया!', 'english': 'Crow drank water!'},
                    {'hindi': 'सीख: जहाँ चाह वहाँ राह!', 'english': "Where there's a will, there's a way!"},
                ]
            },
            {
                'storyweaver_id': 'bm_l2_lion',
                'title': 'The Lion and Mouse',
                'title_hindi': 'शेर और चूहा',
                'title_romanized': 'Sher aur Chooha',
                'level': 2,
                'is_l1_content': False,
                'theme': 'moral',
                'tier': 'standard',
                'xp_reward': 20,
                'estimated_minutes': 3,
                'moral_english': 'Small friends can help big.',
                'moral_hindi': 'छोटे मित्र भी काम आते हैं।',
                'pages': [
                    {'hindi': 'जंगल में एक शेर रहता था।', 'english': 'A lion lived in forest.'},
                    {'hindi': 'एक चूहा शेर पर चढ़ गया।', 'english': 'A mouse climbed on lion.'},
                    {'hindi': "चूहा बोला - 'मुझे छोड़ दो। मैं मदद करूँगा।'", 'english': "'Let me go. I'll help you.'"},
                    {'hindi': 'शेर ने छोड़ दिया।', 'english': 'Lion let him go.'},
                    {'hindi': 'एक दिन शेर जाल में फँसा।', 'english': 'One day lion got trapped.'},
                    {'hindi': 'चूहे ने जाल काटा। शेर आज़ाद!', 'english': 'Mouse cut net. Lion free!'},
                    {'hindi': 'वे दोस्त बन गए।', 'english': 'They became friends.'},
                ]
            },
            {
                'storyweaver_id': 'bm_l2_diwali',
                'title': 'Diwali Story',
                'title_hindi': 'राम जी की वापसी',
                'title_romanized': 'Ram Ji Ki Waapsi',
                'level': 2,
                'is_l1_content': False,
                'theme': 'festival',
                'tier': 'standard',
                'xp_reward': 25,
                'estimated_minutes': 3,
                'moral_english': 'Good always wins.',
                'moral_hindi': 'अच्छाई की हमेशा जीत होती है।',
                'pages': [
                    {'hindi': 'राम जी अयोध्या के राजकुमार थे।', 'english': 'Ram was prince of Ayodhya.'},
                    {'hindi': 'राम जी को 14 साल वन जाना पड़ा।', 'english': 'Ram had to go to forest for 14 years.'},
                    {'hindi': '14 साल बाद वे वापस आए।', 'english': 'After 14 years they returned.'},
                    {'hindi': 'लोगों ने दीये जलाए।', 'english': 'People lit lamps.'},
                    {'hindi': 'इसीलिए हम दीपावली मनाते हैं!', 'english': "That's why we celebrate Diwali!"},
                ]
            },
            {
                'storyweaver_id': 'bm_l2_colors',
                'title': 'World of Colors',
                'title_hindi': 'रंगों की दुनिया',
                'title_romanized': 'Rangon Ki Duniya',
                'level': 2,
                'is_l1_content': False,
                'theme': 'colors',
                'tier': 'standard',
                'xp_reward': 20,
                'estimated_minutes': 2,
                'moral_english': 'The world is beautiful.',
                'moral_hindi': 'दुनिया खूबसूरत है।',
                'pages': [
                    {'hindi': 'आसमान नीला है।', 'english': 'Sky is blue.'},
                    {'hindi': 'पत्ते हरे हैं।', 'english': 'Leaves are green.'},
                    {'hindi': 'सूरज पीला है।', 'english': 'Sun is yellow.'},
                    {'hindi': 'टमाटर लाल है।', 'english': 'Tomato is red.'},
                    {'hindi': 'दुनिया रंगीन है!', 'english': 'World is colorful!'},
                ]
            },
            {
                'storyweaver_id': 'bm_l2_counting',
                'title': 'Learn Counting',
                'title_hindi': 'गिनती सीखो',
                'title_romanized': 'Ginti Seekho',
                'level': 2,
                'is_l1_content': False,
                'theme': 'numbers',
                'tier': 'standard',
                'xp_reward': 20,
                'estimated_minutes': 2,
                'moral_english': 'Counting is fun.',
                'moral_hindi': 'गिनती मज़ेदार है।',
                'pages': [
                    {'hindi': 'एक सेब।', 'english': 'One apple.'},
                    {'hindi': 'दो केले।', 'english': 'Two bananas.'},
                    {'hindi': 'तीन संतरे।', 'english': 'Three oranges.'},
                    {'hindi': 'चार आम।', 'english': 'Four mangoes.'},
                    {'hindi': 'पाँच अंगूर।', 'english': 'Five grapes.'},
                    {'hindi': 'गिनती आ गई!', 'english': 'You learned counting!'},
                ]
            },
            {
                'storyweaver_id': 'bm_l2_animals',
                'title': 'Animal Fair',
                'title_hindi': 'जानवरों का मेला',
                'title_romanized': 'Jaanwaron Ka Mela',
                'level': 2,
                'is_l1_content': False,
                'theme': 'animals',
                'tier': 'standard',
                'xp_reward': 20,
                'estimated_minutes': 2,
                'moral_english': 'Everyone is unique.',
                'moral_hindi': 'हर कोई खास है।',
                'pages': [
                    {'hindi': 'जंगल में मेला लगा।', 'english': 'A fair came to jungle.'},
                    {'hindi': 'हाथी बड़ा है।', 'english': 'Elephant is big.'},
                    {'hindi': 'खरगोश छोटा है।', 'english': 'Rabbit is small.'},
                    {'hindi': 'शेर गरजता है।', 'english': 'Lion roars.'},
                    {'hindi': 'चिड़िया गाती है।', 'english': 'Bird sings.'},
                    {'hindi': 'सब खुश हैं!', 'english': 'Everyone is happy!'},
                ]
            },
        ]

        story_count = 0
        for story_data in stories_data:
            pages = story_data.pop('pages')

            story, created = Story.objects.update_or_create(
                storyweaver_id=story_data['storyweaver_id'],
                defaults={
                    'language': language,
                    'page_count': len(pages),
                    'slug': story_data['storyweaver_id'].replace('_', '-'),
                    **story_data
                }
            )

            if created:
                story_count += 1

            # Create pages
            for idx, page_data in enumerate(pages, 1):
                StoryPage.objects.update_or_create(
                    story=story,
                    page_number=idx,
                    defaults={
                        'text_content': page_data['english'],
                        'text_hindi': page_data['hindi'],
                        'text_romanized': ''
                    }
                )

        self.stdout.write(f'  ✅ Seeded {story_count} stories with pages')

    def print_summary(self):
        """Print final summary."""
        l1 = CurriculumLevel.objects.get(code='L1')
        l2 = CurriculumLevel.objects.get(code='L2')

        l1_modules = CurriculumModule.objects.filter(level=l1).count()
        l1_lessons = Lesson.objects.filter(module__level=l1).count()
        l2_modules = CurriculumModule.objects.filter(level=l2).count()
        l2_lessons = Lesson.objects.filter(module__level=l2).count()
        vocab_count = VocabularyWord.objects.count()
        story_count = Story.objects.filter(language=Child.Language.HINDI).count()

        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('🎉 L1-L2 CURRICULUM SEEDING COMPLETE!'))
        self.stdout.write('=' * 60)
        self.stdout.write(f'''
📊 Summary:
   L1 Discovery:
   • Modules: {l1_modules}
   • Lessons: {l1_lessons}

   L2 Building Blocks:
   • Modules: {l2_modules}
   • Lessons: {l2_lessons}

   Content:
   • Vocabulary Words: {vocab_count}
   • Stories: {story_count}

✅ Run migrations if needed: python manage.py migrate
✅ Test the curriculum in the frontend!
        ''')
