"""
Management command to seed complete grammar content for all languages.
Seeds: Topics, Rules (with examples), and Exercises
Languages: Tamil, Hindi, Punjabi
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.curriculum.models.grammar import GrammarTopic, GrammarRule, GrammarExercise


class Command(BaseCommand):
    help = 'Seed complete grammar content for all languages (Tamil, Hindi, Punjabi)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--language',
            type=str,
            help='Specific language: TAMIL, HINDI, PUNJABI (default: all)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing grammar data before seeding'
        )

    def handle(self, *args, **options):
        language = options.get('language')
        clear = options.get('clear', False)

        if clear:
            self.stdout.write(self.style.WARNING('Clearing existing grammar data...'))
            GrammarExercise.objects.all().delete()
            GrammarRule.objects.all().delete()
            GrammarTopic.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared all grammar data.'))

        languages_to_seed = [language.upper()] if language else ['TAMIL', 'HINDI', 'PUNJABI']

        for lang in languages_to_seed:
            self._seed_language(lang)

        self.stdout.write(self.style.SUCCESS('\n' + '=' * 50))
        self.stdout.write(self.style.SUCCESS('Grammar content seeding complete!'))

    def _seed_language(self, language):
        self.stdout.write(f'\n{"=" * 50}')
        self.stdout.write(self.style.HTTP_INFO(f'Seeding {language} grammar content...'))

        if language == 'TAMIL':
            self._seed_tamil_grammar()
        elif language == 'HINDI':
            self._seed_hindi_grammar()
        elif language == 'PUNJABI':
            self._seed_punjabi_grammar()
        else:
            self.stdout.write(self.style.ERROR(f'Unknown language: {language}'))

    # =========================================================================
    # TAMIL GRAMMAR
    # =========================================================================
    @transaction.atomic
    def _seed_tamil_grammar(self):
        stats = {'topics': 0, 'rules': 0, 'exercises': 0}

        # ----- Topic 1: Sentence Structure -----
        topic1, _ = GrammarTopic.objects.update_or_create(
            language='TAMIL',
            name='Sentence Structure',
            defaults={
                'name_native': 'வாக்கிய அமைப்பு',
                'description': 'Learn basic Tamil sentence structure (Subject-Object-Verb)',
                'description_simple': 'Tamil sentences follow SOV order - Subject comes first, then Object, then Verb.',
                'level': 1,
                'order': 1,
                'is_active': True
            }
        )
        stats['topics'] += 1

        # Rules for Topic 1
        rules1 = [
            {
                'title': 'Basic Word Order',
                'explanation': 'Tamil follows Subject-Object-Verb (SOV) order. Unlike English (SVO), the verb always comes at the end.',
                'explanation_simple': 'Tamil follows Subject-Object-Verb (SOV) order. The action word comes at the end.',
                'formula': 'Subject + Object + Verb',
                'examples': [
                    {'tamil': 'நான் சாதம் சாப்பிடுகிறேன்', 'romanized': 'Naan saadham saappidugiren', 'english': 'I eat rice', 'breakdown': 'நான்(I) + சாதம்(rice) + சாப்பிடுகிறேன்(eat)'},
                    {'tamil': 'அவள் புத்தகம் படிக்கிறாள்', 'romanized': 'Aval puththagam padikkiral', 'english': 'She reads a book', 'breakdown': 'அவள்(she) + புத்தகம்(book) + படிக்கிறாள்(reads)'},
                    {'tamil': 'அப்பா வேலை செய்கிறார்', 'romanized': 'Appaa velai seigiraar', 'english': 'Father works', 'breakdown': 'அப்பா(father) + வேலை(work) + செய்கிறார்(does)'},
                ],
                'order': 1
            },
            {
                'title': 'Subject Placement',
                'explanation': 'The subject (எழுவாய்) is the doer of the action and appears at the beginning of the sentence.',
                'explanation_simple': 'The subject (who does the action) comes first in Tamil.',
                'formula': 'எழுவாய் + ...',
                'examples': [
                    {'tamil': 'குழந்தை விளையாடுகிறது', 'romanized': 'Kuzhandhai vilaiyaadugiradu', 'english': 'The child plays', 'note': 'குழந்தை is the subject'},
                    {'tamil': 'நாய் ஓடுகிறது', 'romanized': 'Naai odugiradu', 'english': 'The dog runs', 'note': 'நாய் is the subject'},
                    {'tamil': 'பாட்டி கதை சொல்கிறாள்', 'romanized': 'Paatti kadhai solgiraal', 'english': 'Grandma tells a story', 'note': 'பாட்டி is the subject'},
                ],
                'order': 2
            },
            {
                'title': 'Object Placement',
                'explanation': 'The object (செயப்படுபொருள்) receives the action and comes after the subject but before the verb.',
                'explanation_simple': 'The object (what receives the action) comes in the middle.',
                'formula': '... + செயப்படுபொருள் + ...',
                'examples': [
                    {'tamil': 'அம்மா சாதம் சமைக்கிறாள்', 'romanized': 'Ammaa saadham samaikkiral', 'english': 'Mother cooks rice', 'note': 'சாதம்(rice) is the object'},
                    {'tamil': 'நான் தண்ணீர் குடிக்கிறேன்', 'romanized': 'Naan thanneer kudikkiren', 'english': 'I drink water', 'note': 'தண்ணீர்(water) is the object'},
                ],
                'order': 3
            },
            {
                'title': 'Verb Placement',
                'explanation': 'The verb (வினை) describes the action and must come at the end of the sentence in Tamil.',
                'explanation_simple': 'The verb (action word) always comes at the end in Tamil.',
                'formula': '... + வினை',
                'examples': [
                    {'tamil': 'பூனை தூங்குகிறது', 'romanized': 'Poonai thoongugiradu', 'english': 'The cat sleeps', 'note': 'தூங்குகிறது(sleeps) is at end'},
                    {'tamil': 'மழை பெய்கிறது', 'romanized': 'Mazhai peigiradu', 'english': 'It is raining', 'note': 'பெய்கிறது(rains) is at end'},
                ],
                'order': 4
            },
            {
                'title': 'Question Formation',
                'explanation': "To form a yes/no question in Tamil, add the question particle 'ஆ' (aa) at the end of the statement.",
                'explanation_simple': "Add 'ஆ' at the end to make a question.",
                'formula': 'Statement + ஆ?',
                'examples': [
                    {'tamil': 'நீ சாப்பிட்டாயா?', 'romanized': 'Nee saappittaayaa?', 'english': 'Did you eat?'},
                    {'tamil': 'இது உன் புத்தகமா?', 'romanized': 'Idhu un puththagamaa?', 'english': 'Is this your book?'},
                    {'tamil': 'அவன் வந்தானா?', 'romanized': 'Avan vandhaan aa?', 'english': 'Did he come?'},
                ],
                'order': 5
            },
        ]

        for rule_data in rules1:
            rule, _ = GrammarRule.objects.update_or_create(
                topic=topic1,
                title=rule_data['title'],
                defaults=rule_data
            )
            stats['rules'] += 1

            # Create exercises for each rule
            if rule_data['title'] == 'Basic Word Order':
                self._create_exercises(rule, [
                    {'type': 'REORDER', 'question': 'Arrange in correct order: சாப்பிடுகிறேன் / நான் / சாதம்', 'correct': 'நான் சாதம் சாப்பிடுகிறேன்', 'options': ['நான் சாதம் சாப்பிடுகிறேன்', 'நான் சாப்பிடுகிறேன் சாதம்', 'சாதம் நான் சாப்பிடுகிறேன்'], 'explanation': 'SOV order: Subject(நான்) + Object(சாதம்) + Verb(சாப்பிடுகிறேன்)'},
                    {'type': 'REORDER', 'question': 'Arrange: படிக்கிறாள் / அவள் / புத்தகம்', 'correct': 'அவள் புத்தகம் படிக்கிறாள்', 'options': ['அவள் புத்தகம் படிக்கிறாள்', 'அவள் படிக்கிறாள் புத்தகம்', 'புத்தகம் அவள் படிக்கிறாள்'], 'explanation': 'Subject + Object + Verb'},
                    {'type': 'TRANSLATE', 'question': 'I eat rice', 'correct': 'நான் சாதம் சாப்பிடுகிறேன்', 'explanation': 'Remember SOV order'},
                ])
                stats['exercises'] += 3
            elif rule_data['title'] == 'Subject Placement':
                self._create_exercises(rule, [
                    {'type': 'MC', 'question': 'What is the subject in: நாய் ஓடுகிறது?', 'correct': 'நாய்', 'options': ['நாய்', 'ஓடுகிறது'], 'explanation': 'நாய் (dog) is doing the action'},
                    {'type': 'FILL_BLANK', 'question': '_____ புத்தகம் படிக்கிறான் (He reads a book)', 'correct': 'அவன்', 'explanation': 'Subject must match the verb ending -ான்'},
                ])
                stats['exercises'] += 2
            elif rule_data['title'] == 'Verb Placement':
                self._create_exercises(rule, [
                    {'type': 'MC', 'question': 'What is the verb in: பூனை தூங்குகிறது?', 'correct': 'தூங்குகிறது', 'options': ['பூனை', 'தூங்குகிறது'], 'explanation': 'தூங்குகிறது (sleeps) is the action'},
                    {'type': 'FILL_BLANK', 'question': 'நான் தண்ணீர் _____ (I drink water)', 'correct': 'குடிக்கிறேன்', 'explanation': 'The verb must match the subject நான்'},
                ])
                stats['exercises'] += 2
            elif rule_data['title'] == 'Question Formation':
                self._create_exercises(rule, [
                    {'type': 'TRANSLATE', 'question': 'Convert to question: நீ சாப்பிட்டாய்', 'correct': 'நீ சாப்பிட்டாயா?', 'explanation': 'Add ஆ at the end'},
                    {'type': 'TRANSLATE', 'question': 'Convert to question: இது புத்தகம்', 'correct': 'இது புத்தகமா?', 'explanation': 'Add ஆ at the end'},
                ])
                stats['exercises'] += 2

        self.stdout.write(f'  Topic 1: Sentence Structure - {len(rules1)} rules')

        # ----- Topic 2: Case Markers -----
        topic2, _ = GrammarTopic.objects.update_or_create(
            language='TAMIL',
            name='Case Markers',
            defaults={
                'name_native': 'வேற்றுமை உருபுகள்',
                'description': 'Learn Tamil case markers (postpositions) that show grammatical relationships',
                'description_simple': 'Learn markers that show who does what to whom.',
                'level': 1,
                'order': 2,
                'is_active': True
            }
        )
        stats['topics'] += 1

        rules2 = [
            {
                'title': 'Accusative Case (ஐ)',
                'explanation': 'The accusative marker ஐ marks the direct object of a sentence - what receives the action.',
                'explanation_simple': 'Add ஐ to show what is being acted upon.',
                'formula': 'Object + ஐ',
                'examples': [
                    {'tamil': 'நான் புத்தகத்தை படிக்கிறேன்', 'romanized': 'Naan puththagaththai padikkiren', 'english': 'I read THE book'},
                    {'tamil': 'அவன் சாதத்தை சாப்பிடுகிறான்', 'romanized': 'Avan saadhaththai saappidugiraan', 'english': 'He eats THE rice'},
                ],
                'order': 1
            },
            {
                'title': 'Dative Case (க்கு)',
                'explanation': 'The dative marker க்கு/உக்கு indicates the recipient - to whom something is given or for whom.',
                'explanation_simple': "Add க்கு to mean 'to' or 'for' someone.",
                'formula': 'Recipient + க்கு/உக்கு',
                'examples': [
                    {'tamil': 'அம்மாவுக்கு கொடு', 'romanized': 'Ammaavukku kodu', 'english': 'Give TO mother'},
                    {'tamil': 'எனக்கு தெரியும்', 'romanized': 'Enakku theriyum', 'english': 'I know (to me it is known)'},
                    {'tamil': 'உனக்கு என்ன வேண்டும்?', 'romanized': 'Unakku enna vendum?', 'english': 'What do you want?'},
                ],
                'order': 2
            },
            {
                'title': 'Instrumental Case (ஆல்)',
                'explanation': 'The instrumental marker ஆல்/கொண்டு shows the means or instrument used to do something.',
                'explanation_simple': "Add ஆல் to mean 'with' or 'by means of'.",
                'formula': 'Instrument + ஆல்/கொண்டு',
                'examples': [
                    {'tamil': 'நான் பேனாவால் எழுதுகிறேன்', 'romanized': 'Naan penaavaal ezhudugiren', 'english': 'I write WITH a pen'},
                    {'tamil': 'கத்தியால் வெட்டு', 'romanized': 'Kaththiyaal vettu', 'english': 'Cut WITH a knife'},
                ],
                'order': 3
            },
            {
                'title': 'Locative Case (இல்)',
                'explanation': 'The locative marker இல் shows location - where something is or happens.',
                'explanation_simple': "Add இல் to mean 'in', 'at', or 'on'.",
                'formula': 'Place + இல்',
                'examples': [
                    {'tamil': 'வீட்டில் இருக்கிறேன்', 'romanized': 'Veettil irukkiren', 'english': 'I am IN the house'},
                    {'tamil': 'பள்ளியில் படிக்கிறேன்', 'romanized': 'Palliyil padikkiren', 'english': 'I study IN school'},
                ],
                'order': 4
            },
            {
                'title': 'Ablative Case (இல் இருந்து)',
                'explanation': 'The ablative marker இல் இருந்து shows origin or source - from where.',
                'explanation_simple': "Add இல் இருந்து to mean 'from'.",
                'formula': 'Source + இல் இருந்து',
                'examples': [
                    {'tamil': 'வீட்டில் இருந்து வந்தேன்', 'romanized': 'Veettil irundhu vandhen', 'english': 'I came FROM home'},
                    {'tamil': 'சென்னையில் இருந்து', 'romanized': 'Chennaiyil irundhu', 'english': 'From Chennai'},
                ],
                'order': 5
            },
            {
                'title': 'Genitive Case (உடைய/இன்)',
                'explanation': 'The genitive marker உடைய/இன் shows possession - whose.',
                'explanation_simple': "Add உடைய or இன் to show ownership.",
                'formula': 'Owner + உடைய/இன்',
                'examples': [
                    {'tamil': 'என்னுடைய புத்தகம்', 'romanized': 'Ennudaiya puththagam', 'english': 'MY book'},
                    {'tamil': 'அவளுடைய வீடு', 'romanized': 'Avaludaiya veedu', 'english': 'HER house'},
                    {'tamil': 'ராமனின் புத்தகம்', 'romanized': 'Raamanin puththagam', 'english': "Rama's book"},
                ],
                'order': 6
            },
        ]

        for rule_data in rules2:
            rule, _ = GrammarRule.objects.update_or_create(
                topic=topic2,
                title=rule_data['title'],
                defaults=rule_data
            )
            stats['rules'] += 1

        # Exercises for Case Markers
        first_rule = GrammarRule.objects.filter(topic=topic2).first()
        if first_rule:
            self._create_exercises(first_rule, [
                {'type': 'FILL_BLANK', 'question': 'நான் புத்தகத்_____ படிக்கிறேன் (I read THE book)', 'correct': 'ஐ', 'options': ['ஐ', 'க்கு', 'இல்'], 'explanation': 'ஐ marks the direct object'},
                {'type': 'FILL_BLANK', 'question': 'அம்மா_____ கொடு (Give TO mother)', 'correct': 'வுக்கு', 'options': ['ஐ', 'வுக்கு', 'இல்'], 'explanation': 'க்கு marks the recipient'},
                {'type': 'FILL_BLANK', 'question': 'நான் பேனா_____ எழுதுகிறேன் (I write WITH a pen)', 'correct': 'வால்', 'options': ['வால்', 'க்கு', 'தை'], 'explanation': 'ஆல் shows the instrument'},
                {'type': 'FILL_BLANK', 'question': 'வீட்ட_____ இருக்கிறேன் (I am IN the house)', 'correct': 'இல்', 'options': ['இல்', 'க்கு', 'ஐ'], 'explanation': 'இல் shows location'},
                {'type': 'MC', 'question': "Which marker means 'to/for'?", 'correct': 'க்கு', 'options': ['ஐ', 'க்கு', 'இல்', 'ஆல்'], 'explanation': 'க்கு is the dative marker'},
                {'type': 'MC', 'question': "Which marker means 'with/by'?", 'correct': 'ஆல்', 'options': ['ஐ', 'க்கு', 'இல்', 'ஆல்'], 'explanation': 'ஆல் is the instrumental marker'},
            ])
            stats['exercises'] += 6

        self.stdout.write(f'  Topic 2: Case Markers - {len(rules2)} rules')

        # ----- Topic 3: Pronouns -----
        topic3, _ = GrammarTopic.objects.update_or_create(
            language='TAMIL',
            name='Pronouns',
            defaults={
                'name_native': 'பெயர்ச்சொற்கள்',
                'description': 'Learn personal pronouns in Tamil - I, you, he, she, they, etc.',
                'description_simple': 'Words that replace names - I, you, he, she.',
                'level': 1,
                'order': 3,
                'is_active': True
            }
        )
        stats['topics'] += 1

        rules3 = [
            {
                'title': 'First Person Pronouns',
                'explanation': 'நான் (I) for singular, நாங்கள் (we-exclusive) and நாம் (we-inclusive) for plural.',
                'explanation_simple': 'நான் means I, நாங்கள்/நாம் mean we.',
                'formula': 'நான் (I) / நாங்கள் (We)',
                'examples': [
                    {'tamil': 'நான் படிக்கிறேன்', 'romanized': 'Naan padikkiren', 'english': 'I study'},
                    {'tamil': 'நாங்கள் விளையாடுகிறோம்', 'romanized': 'Naangal vilaiyaadugirōm', 'english': 'We play'},
                ],
                'order': 1
            },
            {
                'title': 'Second Person Pronouns',
                'explanation': 'நீ (informal you), நீங்கள் (formal you/plural). Use நீங்கள் for respect.',
                'explanation_simple': 'நீ is casual, நீங்கள் is polite.',
                'formula': 'நீ (informal) / நீங்கள் (formal)',
                'examples': [
                    {'tamil': 'நீ எங்கே போகிறாய்?', 'romanized': 'Nee enge pogiraai?', 'english': 'Where are you going?'},
                    {'tamil': 'நீங்கள் வாருங்கள்', 'romanized': 'Neengal vaarungal', 'english': 'Please come (formal)'},
                ],
                'order': 2
            },
            {
                'title': 'Third Person Pronouns',
                'explanation': 'அவன் (he), அவள் (she), அவர் (respectful he/she), அது (it), அவர்கள் (they).',
                'explanation_simple': 'அவன்=he, அவள்=she, அவர்=respectful, அது=it.',
                'formula': 'அவன்/அவள்/அவர்/அது',
                'examples': [
                    {'tamil': 'அவன் ஓடுகிறான்', 'romanized': 'Avan odugiraan', 'english': 'He runs'},
                    {'tamil': 'அவள் பாடுகிறாள்', 'romanized': 'Aval paadugiraal', 'english': 'She sings'},
                    {'tamil': 'அவர் வருகிறார்', 'romanized': 'Avar varugiraar', 'english': 'He/She comes (respectful)'},
                    {'tamil': 'அது என் புத்தகம்', 'romanized': 'Adhu en puththagam', 'english': 'That is my book'},
                ],
                'order': 3
            },
            {
                'title': 'Demonstrative Pronouns',
                'explanation': 'இது (this), அது (that), இவை (these), அவை (those) - for pointing at things.',
                'explanation_simple': 'இது=this (near), அது=that (far).',
                'formula': 'இது/இவை (near) | அது/அவை (far)',
                'examples': [
                    {'tamil': 'இது என் வீடு', 'romanized': 'Idhu en veedu', 'english': 'This is my house'},
                    {'tamil': 'இவை என் புத்தகங்கள்', 'romanized': 'Ivai en puththagangal', 'english': 'These are my books'},
                    {'tamil': 'அவை அழகான பூக்கள்', 'romanized': 'Avai azhagaana pookkal', 'english': 'Those are beautiful flowers'},
                ],
                'order': 4
            },
        ]

        for rule_data in rules3:
            rule, _ = GrammarRule.objects.update_or_create(
                topic=topic3,
                title=rule_data['title'],
                defaults=rule_data
            )
            stats['rules'] += 1

        # Exercises for Pronouns
        first_rule3 = GrammarRule.objects.filter(topic=topic3).first()
        if first_rule3:
            self._create_exercises(first_rule3, [
                {'type': 'MC', 'question': "How do you say 'I' in Tamil?", 'correct': 'நான்', 'options': ['நான்', 'நீ', 'அவன்'], 'explanation': 'நான் means I'},
                {'type': 'MC', 'question': "How do you say 'You' (informal) in Tamil?", 'correct': 'நீ', 'options': ['நான்', 'நீ', 'அவன்'], 'explanation': 'நீ is informal you'},
                {'type': 'MC', 'question': "What is the respectful 'He/She'?", 'correct': 'அவர்', 'options': ['அவன்', 'அவள்', 'அவர்'], 'explanation': 'அவர் is respectful'},
                {'type': 'FILL_BLANK', 'question': '_____ படிக்கிறேன் (I study)', 'correct': 'நான்', 'explanation': 'நான் matches verb ending -ஏன்'},
                {'type': 'MATCH', 'question': 'Match: நாங்கள் = ?', 'correct': 'We', 'options': ['I', 'We', 'You'], 'explanation': 'நாங்கள் means We'},
                {'type': 'TRANSLATE', 'question': 'He is going', 'correct': 'அவன் போகிறான்', 'explanation': 'அவன் + போகிறான்'},
            ])
            stats['exercises'] += 6

        self.stdout.write(f'  Topic 3: Pronouns - {len(rules3)} rules')

        # ----- Topic 4: Numbers -----
        topic4, _ = GrammarTopic.objects.update_or_create(
            language='TAMIL',
            name='Numbers',
            defaults={
                'name_native': 'எண்கள்',
                'description': 'Learn to count and use numbers in Tamil sentences',
                'description_simple': 'Learn Tamil numbers from 1 to 100.',
                'level': 1,
                'order': 4,
                'is_active': True
            }
        )
        stats['topics'] += 1

        rules4 = [
            {
                'title': 'Numbers 1-10',
                'explanation': 'Basic Tamil numbers: ஒன்று(1), இரண்டு(2), மூன்று(3), நான்கு(4), ஐந்து(5), ஆறு(6), ஏழு(7), எட்டு(8), ஒன்பது(9), பத்து(10)',
                'explanation_simple': 'Learn numbers one to ten in Tamil.',
                'formula': '௧-௰',
                'examples': [
                    {'tamil': 'ஒன்று', 'romanized': 'ondru', 'english': '1'},
                    {'tamil': 'இரண்டு', 'romanized': 'irandu', 'english': '2'},
                    {'tamil': 'மூன்று', 'romanized': 'moondru', 'english': '3'},
                    {'tamil': 'நான்கு', 'romanized': 'naangu', 'english': '4'},
                    {'tamil': 'ஐந்து', 'romanized': 'ainthu', 'english': '5'},
                ],
                'order': 1
            },
            {
                'title': 'Numbers 11-100',
                'explanation': 'பதினொன்று(11), இருபது(20), முப்பது(30), நாற்பது(40), ஐம்பது(50), நூறு(100)',
                'explanation_simple': 'Learn larger numbers in Tamil.',
                'formula': '௰௧-௱',
                'examples': [
                    {'tamil': 'பதினொன்று', 'romanized': 'padhinondru', 'english': '11'},
                    {'tamil': 'இருபது', 'romanized': 'irubadhu', 'english': '20'},
                    {'tamil': 'நூறு', 'romanized': 'nooru', 'english': '100'},
                ],
                'order': 2
            },
            {
                'title': 'Using Numbers in Sentences',
                'explanation': 'Numbers come before the noun they describe, like in English.',
                'explanation_simple': 'Put the number before what you are counting.',
                'formula': 'Number + Noun',
                'examples': [
                    {'tamil': 'இரண்டு ஆப்பிள்கள்', 'romanized': 'Irandu aapilkal', 'english': 'Two apples'},
                    {'tamil': 'எனக்கு ஐந்து வயது', 'romanized': 'Enakku ainthu vayasu', 'english': 'I am five years old'},
                    {'tamil': 'இது பத்து ரூபாய்', 'romanized': 'Idhu patthu roopai', 'english': 'This is ten rupees'},
                ],
                'order': 3
            },
        ]

        for rule_data in rules4:
            rule, _ = GrammarRule.objects.update_or_create(
                topic=topic4,
                title=rule_data['title'],
                defaults=rule_data
            )
            stats['rules'] += 1

        first_rule4 = GrammarRule.objects.filter(topic=topic4).first()
        if first_rule4:
            self._create_exercises(first_rule4, [
                {'type': 'MC', 'question': 'What is 5 in Tamil?', 'correct': 'ஐந்து', 'options': ['ஐந்து', 'மூன்று', 'இரண்டு'], 'explanation': 'ஐந்து = 5'},
                {'type': 'MC', 'question': 'What is ஏழு in English?', 'correct': '7', 'options': ['5', '6', '7'], 'explanation': 'ஏழு = 7'},
                {'type': 'TRANSLATE', 'question': 'Ten apples', 'correct': 'பத்து ஆப்பிள்கள்', 'explanation': 'பத்து = ten'},
                {'type': 'FILL_BLANK', 'question': 'I have _____ books (2 புத்தகங்கள்)', 'correct': 'இரண்டு', 'explanation': 'இரண்டு = 2'},
            ])
            stats['exercises'] += 4

        self.stdout.write(f'  Topic 4: Numbers - {len(rules4)} rules')

        # ----- Topic 5: Verb Conjugation -----
        topic5, _ = GrammarTopic.objects.update_or_create(
            language='TAMIL',
            name='Verb Conjugation',
            defaults={
                'name_native': 'வினை மாற்றம்',
                'description': 'Learn how verbs change based on who is doing the action (present tense)',
                'description_simple': 'Verbs change their endings based on who does the action.',
                'level': 2,
                'order': 5,
                'is_active': True
            }
        )
        stats['topics'] += 1

        rules5 = [
            {
                'title': 'Present Tense Endings',
                'explanation': 'Tamil verbs change endings based on the subject: -கிறேன்(I), -கிறாய்(you), -கிறான்(he), -கிறாள்(she), -கிறார்(respectful), -கிறது(it), -கிறோம்(we), -கிறார்கள்(they)',
                'explanation_simple': 'Different endings for I, you, he, she, etc.',
                'formula': 'Verb Root + கிற + Person Ending',
                'examples': [
                    {'tamil': 'செய்கிறேன்', 'romanized': 'seigiren', 'english': 'I do', 'breakdown': 'செய் + கிற + ேன்'},
                    {'tamil': 'செய்கிறாய்', 'romanized': 'seigiraai', 'english': 'You do', 'breakdown': 'செய் + கிற + ாய்'},
                    {'tamil': 'செய்கிறான்', 'romanized': 'seigiraan', 'english': 'He does', 'breakdown': 'செய் + கிற + ான்'},
                    {'tamil': 'செய்கிறாள்', 'romanized': 'seigiraal', 'english': 'She does', 'breakdown': 'செய் + கிற + ாள்'},
                ],
                'order': 1
            },
            {
                'title': 'Common Verbs - போ (go)',
                'explanation': 'போ (go): போகிறேன்(I go), போகிறாய்(you go), போகிறான்(he goes), போகிறாள்(she goes)',
                'explanation_simple': 'How to say "go" with different subjects.',
                'formula': 'போ + கிற + ending',
                'examples': [
                    {'tamil': 'நான் போகிறேன்', 'romanized': 'Naan pogiren', 'english': 'I go'},
                    {'tamil': 'அவன் போகிறான்', 'romanized': 'Avan pogiraan', 'english': 'He goes'},
                    {'tamil': 'அவள் போகிறாள்', 'romanized': 'Aval pogiraal', 'english': 'She goes'},
                ],
                'order': 2
            },
            {
                'title': 'Common Verbs - வா (come)',
                'explanation': 'வா (come): வருகிறேன்(I come), வருகிறான்(he comes). Note: வா becomes வரு before endings.',
                'explanation_simple': 'How to say "come" with different subjects.',
                'formula': 'வரு + கிற + ending',
                'examples': [
                    {'tamil': 'நான் வருகிறேன்', 'romanized': 'Naan varugiren', 'english': 'I come'},
                    {'tamil': 'அவர் வருகிறார்', 'romanized': 'Avar varugiraar', 'english': 'He/She comes (respectful)'},
                ],
                'order': 3
            },
            {
                'title': 'Common Verbs - சாப்பிடு (eat)',
                'explanation': 'சாப்பிடு (eat): சாப்பிடுகிறேன்(I eat), சாப்பிடுகிறான்(he eats), சாப்பிடுகிறாள்(she eats)',
                'explanation_simple': 'How to say "eat" with different subjects.',
                'formula': 'சாப்பிடு + கிற + ending',
                'examples': [
                    {'tamil': 'நான் சாப்பிடுகிறேன்', 'romanized': 'Naan saappidugiren', 'english': 'I eat'},
                    {'tamil': 'நாங்கள் சாப்பிடுகிறோம்', 'romanized': 'Naangal saappidugirōm', 'english': 'We eat'},
                ],
                'order': 4
            },
        ]

        for rule_data in rules5:
            rule, _ = GrammarRule.objects.update_or_create(
                topic=topic5,
                title=rule_data['title'],
                defaults=rule_data
            )
            stats['rules'] += 1

        first_rule5 = GrammarRule.objects.filter(topic=topic5).first()
        if first_rule5:
            self._create_exercises(first_rule5, [
                {'type': 'CONJUGATE', 'question': 'நான் + போ = ?', 'correct': 'போகிறேன்', 'options': ['போகிறேன்', 'போகிறான்', 'போகிறாள்'], 'explanation': 'I + go = போகிறேன்'},
                {'type': 'CONJUGATE', 'question': 'அவள் + படி = ?', 'correct': 'படிக்கிறாள்', 'options': ['படிக்கிறேன்', 'படிக்கிறான்', 'படிக்கிறாள்'], 'explanation': 'She + read = படிக்கிறாள்'},
                {'type': 'FILL_BLANK', 'question': 'நான் தண்ணீர் குடி_____', 'correct': 'க்கிறேன்', 'explanation': 'I drink = குடிக்கிறேன்'},
                {'type': 'FILL_BLANK', 'question': 'அவன் பள்ளிக்கு போ_____', 'correct': 'கிறான்', 'explanation': 'He goes = போகிறான்'},
                {'type': 'TRANSLATE', 'question': 'I am going', 'correct': 'நான் போகிறேன்', 'explanation': 'நான் + போகிறேன்'},
                {'type': 'TRANSLATE', 'question': 'She is reading', 'correct': 'அவள் படிக்கிறாள்', 'explanation': 'அவள் + படிக்கிறாள்'},
            ])
            stats['exercises'] += 6

        self.stdout.write(f'  Topic 5: Verb Conjugation - {len(rules5)} rules')
        self.stdout.write(self.style.SUCCESS(f'  TAMIL Total: {stats["topics"]} topics, {stats["rules"]} rules, {stats["exercises"]} exercises'))

    # =========================================================================
    # HINDI GRAMMAR
    # =========================================================================
    @transaction.atomic
    def _seed_hindi_grammar(self):
        stats = {'topics': 0, 'rules': 0, 'exercises': 0}

        # ----- Topic 1: Sentence Structure -----
        topic1, _ = GrammarTopic.objects.update_or_create(
            language='HINDI',
            name='Sentence Structure',
            defaults={
                'name_native': 'वाक्य रचना',
                'description': 'Learn basic Hindi sentence structure (Subject-Object-Verb)',
                'description_simple': 'Hindi sentences follow SOV order - Subject, Object, then Verb.',
                'level': 1,
                'order': 1,
                'is_active': True
            }
        )
        stats['topics'] += 1

        rules1 = [
            {
                'title': 'Basic Word Order',
                'explanation': 'Hindi follows Subject-Object-Verb (SOV) order. The verb always comes at the end.',
                'explanation_simple': 'In Hindi, say WHO does WHAT, then the ACTION at the end.',
                'formula': 'कर्ता + कर्म + क्रिया',
                'examples': [
                    {'hindi': 'मैं खाना खाता हूँ', 'romanized': 'Main khaana khaata hoon', 'english': 'I eat food', 'breakdown': 'मैं(I) + खाना(food) + खाता हूँ(eat)'},
                    {'hindi': 'वह किताब पढ़ती है', 'romanized': 'Voh kitaab padhti hai', 'english': 'She reads a book', 'breakdown': 'वह(she) + किताब(book) + पढ़ती है(reads)'},
                    {'hindi': 'राम स्कूल जाता है', 'romanized': 'Ram school jaata hai', 'english': 'Ram goes to school', 'breakdown': 'राम(Ram) + स्कूल(school) + जाता है(goes)'},
                ],
                'order': 1
            },
            {
                'title': 'Subject (कर्ता)',
                'explanation': 'The subject (कर्ता) is who does the action. It comes first in the sentence.',
                'explanation_simple': 'कर्ता is who does the action - put it first.',
                'formula': 'कर्ता + ...',
                'examples': [
                    {'hindi': 'बच्चा खेलता है', 'romanized': 'Bachcha khelta hai', 'english': 'The child plays', 'note': 'बच्चा is the subject'},
                    {'hindi': 'माँ खाना बनाती है', 'romanized': 'Maa khaana banaati hai', 'english': 'Mother makes food', 'note': 'माँ is the subject'},
                ],
                'order': 2
            },
            {
                'title': 'Object (कर्म)',
                'explanation': 'The object (कर्म) receives the action. It comes in the middle.',
                'explanation_simple': 'कर्म is what receives the action - put it in the middle.',
                'formula': '... + कर्म + ...',
                'examples': [
                    {'hindi': 'मैं पानी पीता हूँ', 'romanized': 'Main paani peeta hoon', 'english': 'I drink water', 'note': 'पानी is the object'},
                    {'hindi': 'वह गाना गाती है', 'romanized': 'Voh gaana gaati hai', 'english': 'She sings a song', 'note': 'गाना is the object'},
                ],
                'order': 3
            },
            {
                'title': 'Verb (क्रिया)',
                'explanation': 'The verb (क्रिया) shows the action. It always comes at the END in Hindi.',
                'explanation_simple': 'क्रिया is the action - put it at the END.',
                'formula': '... + क्रिया',
                'examples': [
                    {'hindi': 'कुत्ता भौंकता है', 'romanized': 'Kutta bhonkta hai', 'english': 'The dog barks', 'note': 'भौंकता है is at the end'},
                    {'hindi': 'बारिश होती है', 'romanized': 'Baarish hoti hai', 'english': 'It rains', 'note': 'होती है is at the end'},
                ],
                'order': 4
            },
            {
                'title': 'Question Formation',
                'explanation': "Add 'क्या' at the beginning to make a yes/no question. Word order stays the same.",
                'explanation_simple': "Add 'क्या' at the start to ask a question.",
                'formula': 'क्या + Statement?',
                'examples': [
                    {'hindi': 'क्या तुम खाना खाते हो?', 'romanized': 'Kya tum khaana khaate ho?', 'english': 'Do you eat food?'},
                    {'hindi': 'क्या वह जाती है?', 'romanized': 'Kya voh jaati hai?', 'english': 'Does she go?'},
                ],
                'order': 5
            },
        ]

        for rule_data in rules1:
            rule, _ = GrammarRule.objects.update_or_create(
                topic=topic1,
                title=rule_data['title'],
                defaults=rule_data
            )
            stats['rules'] += 1

        first_rule = GrammarRule.objects.filter(topic=topic1).first()
        if first_rule:
            self._create_exercises(first_rule, [
                {'type': 'REORDER', 'question': 'Arrange: खाता हूँ / मैं / खाना', 'correct': 'मैं खाना खाता हूँ', 'options': ['मैं खाना खाता हूँ', 'मैं खाता हूँ खाना', 'खाना मैं खाता हूँ'], 'explanation': 'SOV: Subject + Object + Verb'},
                {'type': 'MC', 'question': 'What is the subject in: राम स्कूल जाता है?', 'correct': 'राम', 'options': ['राम', 'स्कूल', 'जाता है'], 'explanation': 'राम is doing the action'},
                {'type': 'FILL_BLANK', 'question': 'मैं पानी _____ (पीता हूँ)', 'correct': 'पीता हूँ', 'explanation': 'Verb goes at the end'},
                {'type': 'TRANSLATE', 'question': 'I eat rice', 'correct': 'मैं चावल खाता हूँ', 'explanation': 'मैं(I) + चावल(rice) + खाता हूँ(eat)'},
                {'type': 'TRANSLATE', 'question': 'Convert: तुम जाते हो → Question', 'correct': 'क्या तुम जाते हो?', 'explanation': 'Add क्या at the beginning'},
            ])
            stats['exercises'] += 5

        self.stdout.write(f'  Topic 1: Sentence Structure - {len(rules1)} rules')

        # ----- Topic 2: Gender (लिंग) -----
        topic2, _ = GrammarTopic.objects.update_or_create(
            language='HINDI',
            name='Gender',
            defaults={
                'name_native': 'लिंग',
                'description': 'Learn grammatical gender in Hindi - masculine and feminine nouns',
                'description_simple': 'Hindi words have gender - masculine (पुल्लिंग) or feminine (स्त्रीलिंग).',
                'level': 1,
                'order': 2,
                'is_active': True
            }
        )
        stats['topics'] += 1

        rules2 = [
            {
                'title': 'Masculine Nouns (पुल्लिंग)',
                'explanation': 'Words ending in आ are usually masculine. Examples: लड़का, बेटा, कुत्ता, घोड़ा',
                'explanation_simple': 'Words ending in आ are usually for boys/men.',
                'formula': '___आ = Masculine',
                'examples': [
                    {'hindi': 'लड़का', 'romanized': 'ladka', 'english': 'boy'},
                    {'hindi': 'बेटा', 'romanized': 'beta', 'english': 'son'},
                    {'hindi': 'कुत्ता', 'romanized': 'kutta', 'english': 'dog (male)'},
                    {'hindi': 'घोड़ा', 'romanized': 'ghoda', 'english': 'horse (male)'},
                ],
                'order': 1
            },
            {
                'title': 'Feminine Nouns (स्त्रीलिंग)',
                'explanation': 'Words ending in ई are usually feminine. Change आ to ई for feminine form.',
                'explanation_simple': 'Words ending in ई are usually for girls/women.',
                'formula': '___ई = Feminine',
                'examples': [
                    {'hindi': 'लड़की', 'romanized': 'ladki', 'english': 'girl'},
                    {'hindi': 'बेटी', 'romanized': 'beti', 'english': 'daughter'},
                    {'hindi': 'कुत्ती', 'romanized': 'kutti', 'english': 'dog (female)'},
                    {'hindi': 'घोड़ी', 'romanized': 'ghodi', 'english': 'horse (female)'},
                ],
                'order': 2
            },
            {
                'title': 'Natural Gender',
                'explanation': 'Some words follow natural gender based on the being they describe.',
                'explanation_simple': 'Some words are naturally masculine or feminine.',
                'formula': 'Based on meaning',
                'examples': [
                    {'hindi': 'राजा → रानी', 'romanized': 'raja → rani', 'english': 'king → queen'},
                    {'hindi': 'पिता → माता', 'romanized': 'pita → mata', 'english': 'father → mother'},
                    {'hindi': 'शेर → शेरनी', 'romanized': 'sher → sherni', 'english': 'lion → lioness'},
                ],
                'order': 3
            },
            {
                'title': 'Gender Exceptions',
                'explanation': "Some words don't follow the आ/ई pattern. Memorize these.",
                'explanation_simple': 'Some words break the rules - just memorize them!',
                'formula': 'Exceptions',
                'examples': [
                    {'hindi': 'पानी (M)', 'romanized': 'paani', 'english': 'water (masculine)'},
                    {'hindi': 'दही (M)', 'romanized': 'dahi', 'english': 'yogurt (masculine)'},
                    {'hindi': 'रोटी (F)', 'romanized': 'roti', 'english': 'bread (feminine)'},
                    {'hindi': 'मिठाई (F)', 'romanized': 'mithai', 'english': 'sweet (feminine)'},
                ],
                'order': 4
            },
        ]

        for rule_data in rules2:
            rule, _ = GrammarRule.objects.update_or_create(
                topic=topic2,
                title=rule_data['title'],
                defaults=rule_data
            )
            stats['rules'] += 1

        first_rule2 = GrammarRule.objects.filter(topic=topic2).first()
        if first_rule2:
            self._create_exercises(first_rule2, [
                {'type': 'MC', 'question': 'लड़का is which gender?', 'correct': 'Masculine', 'options': ['Masculine', 'Feminine'], 'explanation': 'लड़का ends in आ = masculine'},
                {'type': 'MC', 'question': 'What is the feminine of बेटा?', 'correct': 'बेटी', 'options': ['बेटी', 'बेटा', 'बेटू'], 'explanation': 'Change आ to ई'},
                {'type': 'FILL_BLANK', 'question': 'लड़का → _____', 'correct': 'लड़की', 'explanation': 'Change आ to ई'},
                {'type': 'FILL_BLANK', 'question': 'राजा → _____', 'correct': 'रानी', 'explanation': 'King becomes Queen'},
                {'type': 'MC', 'question': 'पानी is which gender?', 'correct': 'Masculine', 'options': ['Masculine', 'Feminine'], 'explanation': 'Exception: पानी is masculine'},
            ])
            stats['exercises'] += 5

        self.stdout.write(f'  Topic 2: Gender - {len(rules2)} rules')

        # ----- Topic 3: Pronouns -----
        topic3, _ = GrammarTopic.objects.update_or_create(
            language='HINDI',
            name='Pronouns',
            defaults={
                'name_native': 'सर्वनाम',
                'description': 'Learn personal pronouns in Hindi - I, you, he, she, they',
                'description_simple': 'Words that replace names - I, you, he, she.',
                'level': 1,
                'order': 3,
                'is_active': True
            }
        )
        stats['topics'] += 1

        rules3 = [
            {
                'title': 'First Person',
                'explanation': 'मैं (I), हम (we). Use हम for formal "I" sometimes.',
                'explanation_simple': 'मैं = I, हम = we',
                'formula': 'मैं / हम',
                'examples': [
                    {'hindi': 'मैं जाता हूँ', 'romanized': 'Main jaata hoon', 'english': 'I go'},
                    {'hindi': 'हम खाते हैं', 'romanized': 'Hum khaate hain', 'english': 'We eat'},
                ],
                'order': 1
            },
            {
                'title': 'Second Person',
                'explanation': 'तू (very informal), तुम (informal), आप (formal/respectful)',
                'explanation_simple': 'तू = very casual, तुम = normal, आप = polite',
                'formula': 'तू / तुम / आप',
                'examples': [
                    {'hindi': 'तुम कहाँ जाते हो?', 'romanized': 'Tum kahan jaate ho?', 'english': 'Where do you go?'},
                    {'hindi': 'आप कैसे हैं?', 'romanized': 'Aap kaise hain?', 'english': 'How are you? (formal)'},
                ],
                'order': 2
            },
            {
                'title': 'Third Person',
                'explanation': 'वह (he/she singular), वे (they). यह (this), ये (these).',
                'explanation_simple': 'वह = he/she, वे = they',
                'formula': 'वह / वे / यह / ये',
                'examples': [
                    {'hindi': 'वह जाता है', 'romanized': 'Voh jaata hai', 'english': 'He goes'},
                    {'hindi': 'वह जाती है', 'romanized': 'Voh jaati hai', 'english': 'She goes'},
                    {'hindi': 'वे खाते हैं', 'romanized': 'Ve khaate hain', 'english': 'They eat'},
                ],
                'order': 3
            },
        ]

        for rule_data in rules3:
            rule, _ = GrammarRule.objects.update_or_create(
                topic=topic3,
                title=rule_data['title'],
                defaults=rule_data
            )
            stats['rules'] += 1

        first_rule3 = GrammarRule.objects.filter(topic=topic3).first()
        if first_rule3:
            self._create_exercises(first_rule3, [
                {'type': 'MC', 'question': "How do you say 'I' in Hindi?", 'correct': 'मैं', 'options': ['मैं', 'तुम', 'वह'], 'explanation': 'मैं = I'},
                {'type': 'MC', 'question': 'Which is the most respectful form of "you"?', 'correct': 'आप', 'options': ['तू', 'तुम', 'आप'], 'explanation': 'आप is formal/respectful'},
                {'type': 'FILL_BLANK', 'question': '_____ जाता हूँ (I go)', 'correct': 'मैं', 'explanation': 'मैं matches हूँ'},
                {'type': 'TRANSLATE', 'question': 'He goes', 'correct': 'वह जाता है', 'explanation': 'वह(he) + जाता है(goes)'},
            ])
            stats['exercises'] += 4

        self.stdout.write(f'  Topic 3: Pronouns - {len(rules3)} rules')

        # ----- Topic 4: Numbers -----
        topic4, _ = GrammarTopic.objects.update_or_create(
            language='HINDI',
            name='Numbers',
            defaults={
                'name_native': 'संख्याएँ',
                'description': 'Learn to count and use numbers in Hindi',
                'description_simple': 'Learn Hindi numbers from 1 to 100.',
                'level': 1,
                'order': 4,
                'is_active': True
            }
        )
        stats['topics'] += 1

        rules4 = [
            {
                'title': 'Numbers 1-10',
                'explanation': 'एक(1), दो(2), तीन(3), चार(4), पाँच(5), छह(6), सात(7), आठ(8), नौ(9), दस(10)',
                'explanation_simple': 'Learn numbers one to ten.',
                'formula': '१-१०',
                'examples': [
                    {'hindi': 'एक', 'romanized': 'ek', 'english': '1'},
                    {'hindi': 'दो', 'romanized': 'do', 'english': '2'},
                    {'hindi': 'तीन', 'romanized': 'teen', 'english': '3'},
                    {'hindi': 'पाँच', 'romanized': 'paanch', 'english': '5'},
                    {'hindi': 'दस', 'romanized': 'das', 'english': '10'},
                ],
                'order': 1
            },
            {
                'title': 'Numbers 11-100',
                'explanation': 'ग्यारह(11), बीस(20), तीस(30), चालीस(40), पचास(50), सौ(100)',
                'explanation_simple': 'Learn larger numbers.',
                'formula': '११-१००',
                'examples': [
                    {'hindi': 'ग्यारह', 'romanized': 'gyaarah', 'english': '11'},
                    {'hindi': 'बीस', 'romanized': 'bees', 'english': '20'},
                    {'hindi': 'सौ', 'romanized': 'sau', 'english': '100'},
                ],
                'order': 2
            },
        ]

        for rule_data in rules4:
            rule, _ = GrammarRule.objects.update_or_create(
                topic=topic4,
                title=rule_data['title'],
                defaults=rule_data
            )
            stats['rules'] += 1

        first_rule4 = GrammarRule.objects.filter(topic=topic4).first()
        if first_rule4:
            self._create_exercises(first_rule4, [
                {'type': 'MC', 'question': 'What is 5 in Hindi?', 'correct': 'पाँच', 'options': ['पाँच', 'तीन', 'दो'], 'explanation': 'पाँच = 5'},
                {'type': 'MC', 'question': 'What is सात in English?', 'correct': '7', 'options': ['5', '6', '7'], 'explanation': 'सात = 7'},
                {'type': 'TRANSLATE', 'question': 'Ten books', 'correct': 'दस किताबें', 'explanation': 'दस = ten'},
            ])
            stats['exercises'] += 3

        self.stdout.write(f'  Topic 4: Numbers - {len(rules4)} rules')

        # ----- Topic 5: Verb Conjugation -----
        topic5, _ = GrammarTopic.objects.update_or_create(
            language='HINDI',
            name='Verb Conjugation',
            defaults={
                'name_native': 'क्रिया रूप',
                'description': 'Learn how verbs change based on subject and gender',
                'description_simple': 'Verbs change based on who does the action and their gender.',
                'level': 2,
                'order': 5,
                'is_active': True
            }
        )
        stats['topics'] += 1

        rules5 = [
            {
                'title': 'Present Tense - Masculine',
                'explanation': 'For male subjects: -ता हूँ (I), -ता है (he), -ते हैं (they/you formal), -ते हो (you informal)',
                'explanation_simple': 'Add -ता/-ते for male subjects.',
                'formula': 'Verb + ता/ते + हूँ/है/हैं/हो',
                'examples': [
                    {'hindi': 'मैं खाता हूँ', 'romanized': 'Main khaata hoon', 'english': 'I eat (male)'},
                    {'hindi': 'वह खाता है', 'romanized': 'Voh khaata hai', 'english': 'He eats'},
                    {'hindi': 'वे खाते हैं', 'romanized': 'Ve khaate hain', 'english': 'They eat (male)'},
                ],
                'order': 1
            },
            {
                'title': 'Present Tense - Feminine',
                'explanation': 'For female subjects: -ती हूँ (I), -ती है (she), -ती हैं (they)',
                'explanation_simple': 'Add -ती for female subjects.',
                'formula': 'Verb + ती + हूँ/है/हैं',
                'examples': [
                    {'hindi': 'मैं खाती हूँ', 'romanized': 'Main khaati hoon', 'english': 'I eat (female)'},
                    {'hindi': 'वह खाती है', 'romanized': 'Voh khaati hai', 'english': 'She eats'},
                    {'hindi': 'वे खाती हैं', 'romanized': 'Ve khaati hain', 'english': 'They eat (female)'},
                ],
                'order': 2
            },
        ]

        for rule_data in rules5:
            rule, _ = GrammarRule.objects.update_or_create(
                topic=topic5,
                title=rule_data['title'],
                defaults=rule_data
            )
            stats['rules'] += 1

        first_rule5 = GrammarRule.objects.filter(topic=topic5).first()
        if first_rule5:
            self._create_exercises(first_rule5, [
                {'type': 'CONJUGATE', 'question': 'मैं (male) + खा = ?', 'correct': 'खाता हूँ', 'options': ['खाता हूँ', 'खाती हूँ', 'खाते हैं'], 'explanation': 'Male I = -ता हूँ'},
                {'type': 'CONJUGATE', 'question': 'वह (female) + जा = ?', 'correct': 'जाती है', 'options': ['जाता है', 'जाती है', 'जाते हैं'], 'explanation': 'Female she = -ती है'},
                {'type': 'FILL_BLANK', 'question': 'मैं पानी पी_____ हूँ (male)', 'correct': 'ता', 'explanation': 'Male = -ता'},
                {'type': 'TRANSLATE', 'question': 'She goes', 'correct': 'वह जाती है', 'explanation': 'वह + जाती है'},
            ])
            stats['exercises'] += 4

        self.stdout.write(f'  Topic 5: Verb Conjugation - {len(rules5)} rules')
        self.stdout.write(self.style.SUCCESS(f'  HINDI Total: {stats["topics"]} topics, {stats["rules"]} rules, {stats["exercises"]} exercises'))

    # =========================================================================
    # PUNJABI GRAMMAR
    # =========================================================================
    @transaction.atomic
    def _seed_punjabi_grammar(self):
        stats = {'topics': 0, 'rules': 0, 'exercises': 0}

        # ----- Topic 1: Sentence Structure -----
        topic1, _ = GrammarTopic.objects.update_or_create(
            language='PUNJABI',
            name='Sentence Structure',
            defaults={
                'name_native': 'ਵਾਕ ਬਣਤਰ',
                'description': 'Learn basic Punjabi sentence structure (Subject-Object-Verb)',
                'description_simple': 'Punjabi sentences follow SOV order - Subject, Object, then Verb.',
                'level': 1,
                'order': 1,
                'is_active': True
            }
        )
        stats['topics'] += 1

        rules1 = [
            {
                'title': 'Basic Word Order',
                'explanation': 'Punjabi follows Subject-Object-Verb (SOV) order like Hindi. The verb comes at the end.',
                'explanation_simple': 'In Punjabi, say WHO does WHAT, then the ACTION at the end.',
                'formula': 'ਕਰਤਾ + ਕਰਮ + ਕਿਰਿਆ',
                'examples': [
                    {'punjabi': 'ਮੈਂ ਰੋਟੀ ਖਾਂਦਾ ਹਾਂ', 'romanized': 'Main roti khaanda haan', 'english': 'I eat roti', 'breakdown': 'ਮੈਂ(I) + ਰੋਟੀ(roti) + ਖਾਂਦਾ ਹਾਂ(eat)'},
                    {'punjabi': 'ਉਹ ਕਿਤਾਬ ਪੜ੍ਹਦੀ ਹੈ', 'romanized': 'Oh kitaab parhdi hai', 'english': 'She reads a book', 'breakdown': 'ਉਹ(she) + ਕਿਤਾਬ(book) + ਪੜ੍ਹਦੀ ਹੈ(reads)'},
                    {'punjabi': 'ਬੱਚਾ ਖੇਡਦਾ ਹੈ', 'romanized': 'Bachcha khelda hai', 'english': 'The child plays', 'breakdown': 'ਬੱਚਾ(child) + ਖੇਡਦਾ ਹੈ(plays)'},
                ],
                'order': 1
            },
            {
                'title': 'Subject (ਕਰਤਾ)',
                'explanation': 'The subject (ਕਰਤਾ) does the action. It comes first.',
                'explanation_simple': 'ਕਰਤਾ is who does the action - put it first.',
                'formula': 'ਕਰਤਾ + ...',
                'examples': [
                    {'punjabi': 'ਕੁੱਤਾ ਭੌਂਕਦਾ ਹੈ', 'romanized': 'Kutta bhonkda hai', 'english': 'The dog barks', 'note': 'ਕੁੱਤਾ is the subject'},
                    {'punjabi': 'ਮਾਂ ਖਾਣਾ ਬਣਾਉਂਦੀ ਹੈ', 'romanized': 'Maa khaana banaundi hai', 'english': 'Mother makes food', 'note': 'ਮਾਂ is the subject'},
                ],
                'order': 2
            },
            {
                'title': 'Object (ਕਰਮ)',
                'explanation': 'The object (ਕਰਮ) receives the action. It comes in the middle.',
                'explanation_simple': 'ਕਰਮ is what receives the action.',
                'formula': '... + ਕਰਮ + ...',
                'examples': [
                    {'punjabi': 'ਮੈਂ ਪਾਣੀ ਪੀਂਦਾ ਹਾਂ', 'romanized': 'Main paani peenda haan', 'english': 'I drink water', 'note': 'ਪਾਣੀ is the object'},
                ],
                'order': 3
            },
            {
                'title': 'Verb (ਕਿਰਿਆ)',
                'explanation': 'The verb (ਕਿਰਿਆ) shows the action. It comes at the end.',
                'explanation_simple': 'ਕਿਰਿਆ is the action - put it at the END.',
                'formula': '... + ਕਿਰਿਆ',
                'examples': [
                    {'punjabi': 'ਮੀਂਹ ਪੈਂਦਾ ਹੈ', 'romanized': 'Meenh painda hai', 'english': 'It rains', 'note': 'ਪੈਂਦਾ ਹੈ is at the end'},
                ],
                'order': 4
            },
            {
                'title': 'Question Formation',
                'explanation': "Add 'ਕੀ' at the beginning to make a yes/no question.",
                'explanation_simple': "Add 'ਕੀ' at the start to ask a question.",
                'formula': 'ਕੀ + Statement?',
                'examples': [
                    {'punjabi': 'ਕੀ ਤੁਸੀਂ ਜਾਂਦੇ ਹੋ?', 'romanized': 'Ki tusi jaande ho?', 'english': 'Do you go?'},
                    {'punjabi': 'ਕੀ ਉਹ ਆਉਂਦਾ ਹੈ?', 'romanized': 'Ki oh aunda hai?', 'english': 'Does he come?'},
                ],
                'order': 5
            },
        ]

        for rule_data in rules1:
            rule, _ = GrammarRule.objects.update_or_create(
                topic=topic1,
                title=rule_data['title'],
                defaults=rule_data
            )
            stats['rules'] += 1

        first_rule = GrammarRule.objects.filter(topic=topic1).first()
        if first_rule:
            self._create_exercises(first_rule, [
                {'type': 'REORDER', 'question': 'Arrange: ਖਾਂਦਾ ਹਾਂ / ਮੈਂ / ਰੋਟੀ', 'correct': 'ਮੈਂ ਰੋਟੀ ਖਾਂਦਾ ਹਾਂ', 'options': ['ਮੈਂ ਰੋਟੀ ਖਾਂਦਾ ਹਾਂ', 'ਮੈਂ ਖਾਂਦਾ ਹਾਂ ਰੋਟੀ'], 'explanation': 'SOV: Subject + Object + Verb'},
                {'type': 'MC', 'question': 'What is the verb in: ਬੱਚਾ ਖੇਡਦਾ ਹੈ?', 'correct': 'ਖੇਡਦਾ ਹੈ', 'options': ['ਬੱਚਾ', 'ਖੇਡਦਾ ਹੈ'], 'explanation': 'ਖੇਡਦਾ ਹੈ is the action'},
                {'type': 'FILL_BLANK', 'question': 'ਮੈਂ ਪਾਣੀ _____ (ਪੀਂਦਾ ਹਾਂ)', 'correct': 'ਪੀਂਦਾ ਹਾਂ', 'explanation': 'Verb goes at the end'},
                {'type': 'TRANSLATE', 'question': 'I eat rice', 'correct': 'ਮੈਂ ਚੌਲ ਖਾਂਦਾ ਹਾਂ', 'explanation': 'ਮੈਂ(I) + ਚੌਲ(rice) + ਖਾਂਦਾ ਹਾਂ(eat)'},
                {'type': 'TRANSLATE', 'question': 'Convert: ਤੁਸੀਂ ਜਾਂਦੇ ਹੋ → Question', 'correct': 'ਕੀ ਤੁਸੀਂ ਜਾਂਦੇ ਹੋ?', 'explanation': 'Add ਕੀ at the beginning'},
            ])
            stats['exercises'] += 5

        self.stdout.write(f'  Topic 1: Sentence Structure - {len(rules1)} rules')

        # ----- Topic 2: Pronouns -----
        topic2, _ = GrammarTopic.objects.update_or_create(
            language='PUNJABI',
            name='Pronouns',
            defaults={
                'name_native': 'ਪੜਨਾਂਵ',
                'description': 'Learn personal pronouns in Punjabi',
                'description_simple': 'Words that replace names - I, you, he, she.',
                'level': 1,
                'order': 2,
                'is_active': True
            }
        )
        stats['topics'] += 1

        rules2 = [
            {
                'title': 'First Person',
                'explanation': 'ਮੈਂ (I), ਅਸੀਂ (we)',
                'explanation_simple': 'ਮੈਂ = I, ਅਸੀਂ = we',
                'formula': 'ਮੈਂ / ਅਸੀਂ',
                'examples': [
                    {'punjabi': 'ਮੈਂ ਜਾਂਦਾ ਹਾਂ', 'romanized': 'Main jaanda haan', 'english': 'I go'},
                    {'punjabi': 'ਅਸੀਂ ਖਾਂਦੇ ਹਾਂ', 'romanized': 'Aseen khaande haan', 'english': 'We eat'},
                ],
                'order': 1
            },
            {
                'title': 'Second Person',
                'explanation': 'ਤੂੰ (very informal), ਤੁਸੀਂ (formal/respectful)',
                'explanation_simple': 'ਤੂੰ = casual, ਤੁਸੀਂ = polite',
                'formula': 'ਤੂੰ / ਤੁਸੀਂ',
                'examples': [
                    {'punjabi': 'ਤੂੰ ਕਿੱਥੇ ਜਾਂਦਾ ਹੈਂ?', 'romanized': 'Tu kithe jaanda hain?', 'english': 'Where do you go? (informal)'},
                    {'punjabi': 'ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ?', 'romanized': 'Tusi kiven ho?', 'english': 'How are you? (formal)'},
                ],
                'order': 2
            },
            {
                'title': 'Third Person',
                'explanation': 'ਉਹ (he/she/they), ਇਹ (this/these)',
                'explanation_simple': 'ਉਹ = he/she/they, ਇਹ = this',
                'formula': 'ਉਹ / ਇਹ',
                'examples': [
                    {'punjabi': 'ਉਹ ਜਾਂਦਾ ਹੈ', 'romanized': 'Oh jaanda hai', 'english': 'He goes'},
                    {'punjabi': 'ਉਹ ਜਾਂਦੀ ਹੈ', 'romanized': 'Oh jaandi hai', 'english': 'She goes'},
                    {'punjabi': 'ਇਹ ਮੇਰੀ ਕਿਤਾਬ ਹੈ', 'romanized': 'Eh meri kitaab hai', 'english': 'This is my book'},
                ],
                'order': 3
            },
        ]

        for rule_data in rules2:
            rule, _ = GrammarRule.objects.update_or_create(
                topic=topic2,
                title=rule_data['title'],
                defaults=rule_data
            )
            stats['rules'] += 1

        first_rule2 = GrammarRule.objects.filter(topic=topic2).first()
        if first_rule2:
            self._create_exercises(first_rule2, [
                {'type': 'MC', 'question': "How do you say 'I' in Punjabi?", 'correct': 'ਮੈਂ', 'options': ['ਮੈਂ', 'ਤੂੰ', 'ਉਹ'], 'explanation': 'ਮੈਂ = I'},
                {'type': 'MC', 'question': "How do you say 'We' in Punjabi?", 'correct': 'ਅਸੀਂ', 'options': ['ਮੈਂ', 'ਅਸੀਂ', 'ਤੁਸੀਂ'], 'explanation': 'ਅਸੀਂ = We'},
                {'type': 'FILL_BLANK', 'question': '_____ ਜਾਂਦਾ ਹਾਂ (I go)', 'correct': 'ਮੈਂ', 'explanation': 'ਮੈਂ matches ਹਾਂ'},
                {'type': 'TRANSLATE', 'question': 'He is going', 'correct': 'ਉਹ ਜਾ ਰਿਹਾ ਹੈ', 'explanation': 'ਉਹ(he) + ਜਾ ਰਿਹਾ ਹੈ(is going)'},
                {'type': 'MATCH', 'question': 'Match: ਅਸੀਂ = ?', 'correct': 'We', 'options': ['I', 'We', 'You'], 'explanation': 'ਅਸੀਂ = We'},
            ])
            stats['exercises'] += 5

        self.stdout.write(f'  Topic 2: Pronouns - {len(rules2)} rules')

        # ----- Topic 3: Numbers -----
        topic3, _ = GrammarTopic.objects.update_or_create(
            language='PUNJABI',
            name='Numbers',
            defaults={
                'name_native': 'ਅੰਕ',
                'description': 'Learn to count and use numbers in Punjabi',
                'description_simple': 'Learn Punjabi numbers from 1 to 100.',
                'level': 1,
                'order': 3,
                'is_active': True
            }
        )
        stats['topics'] += 1

        rules3 = [
            {
                'title': 'Numbers 1-10',
                'explanation': 'ਇੱਕ(1), ਦੋ(2), ਤਿੰਨ(3), ਚਾਰ(4), ਪੰਜ(5), ਛੇ(6), ਸੱਤ(7), ਅੱਠ(8), ਨੌਂ(9), ਦਸ(10)',
                'explanation_simple': 'Learn numbers one to ten.',
                'formula': '੧-੧੦',
                'examples': [
                    {'punjabi': 'ਇੱਕ', 'romanized': 'ikk', 'english': '1'},
                    {'punjabi': 'ਦੋ', 'romanized': 'do', 'english': '2'},
                    {'punjabi': 'ਤਿੰਨ', 'romanized': 'tinn', 'english': '3'},
                    {'punjabi': 'ਪੰਜ', 'romanized': 'panj', 'english': '5'},
                    {'punjabi': 'ਦਸ', 'romanized': 'das', 'english': '10'},
                ],
                'order': 1
            },
            {
                'title': 'Numbers 11-100',
                'explanation': 'ਗਿਆਰਾਂ(11), ਵੀਹ(20), ਤੀਹ(30), ਚਾਲੀ(40), ਪੰਜਾਹ(50), ਸੌ(100)',
                'explanation_simple': 'Learn larger numbers.',
                'formula': '੧੧-੧੦੦',
                'examples': [
                    {'punjabi': 'ਗਿਆਰਾਂ', 'romanized': 'giaara', 'english': '11'},
                    {'punjabi': 'ਵੀਹ', 'romanized': 'veeh', 'english': '20'},
                    {'punjabi': 'ਸੌ', 'romanized': 'sau', 'english': '100'},
                ],
                'order': 2
            },
        ]

        for rule_data in rules3:
            rule, _ = GrammarRule.objects.update_or_create(
                topic=topic3,
                title=rule_data['title'],
                defaults=rule_data
            )
            stats['rules'] += 1

        first_rule3 = GrammarRule.objects.filter(topic=topic3).first()
        if first_rule3:
            self._create_exercises(first_rule3, [
                {'type': 'MC', 'question': 'What is 5 in Punjabi?', 'correct': 'ਪੰਜ', 'options': ['ਪੰਜ', 'ਤਿੰਨ', 'ਦੋ'], 'explanation': 'ਪੰਜ = 5'},
                {'type': 'MC', 'question': 'What is ਸੱਤ in English?', 'correct': '7', 'options': ['5', '6', '7'], 'explanation': 'ਸੱਤ = 7'},
                {'type': 'TRANSLATE', 'question': 'Ten books', 'correct': 'ਦਸ ਕਿਤਾਬਾਂ', 'explanation': 'ਦਸ = ten'},
            ])
            stats['exercises'] += 3

        self.stdout.write(f'  Topic 3: Numbers - {len(rules3)} rules')

        # ----- Topic 4: Gender -----
        topic4, _ = GrammarTopic.objects.update_or_create(
            language='PUNJABI',
            name='Gender',
            defaults={
                'name_native': 'ਲਿੰਗ',
                'description': 'Learn grammatical gender in Punjabi',
                'description_simple': 'Punjabi words have gender - masculine (ਪੁਲਿੰਗ) or feminine (ਇਸਤਰੀ ਲਿੰਗ).',
                'level': 1,
                'order': 4,
                'is_active': True
            }
        )
        stats['topics'] += 1

        rules4 = [
            {
                'title': 'Masculine Nouns (ਪੁਲਿੰਗ)',
                'explanation': 'Words ending in ਆ are usually masculine: ਮੁੰਡਾ, ਕੁੱਤਾ, ਘੋੜਾ',
                'explanation_simple': 'Words ending in ਆ are usually for boys/males.',
                'formula': '___ਆ = Masculine',
                'examples': [
                    {'punjabi': 'ਮੁੰਡਾ', 'romanized': 'munda', 'english': 'boy'},
                    {'punjabi': 'ਕੁੱਤਾ', 'romanized': 'kutta', 'english': 'dog (male)'},
                    {'punjabi': 'ਘੋੜਾ', 'romanized': 'ghoda', 'english': 'horse (male)'},
                ],
                'order': 1
            },
            {
                'title': 'Feminine Nouns (ਇਸਤਰੀ ਲਿੰਗ)',
                'explanation': 'Words ending in ਈ are usually feminine: ਕੁੜੀ, ਕੁੱਤੀ, ਘੋੜੀ',
                'explanation_simple': 'Words ending in ਈ are usually for girls/females.',
                'formula': '___ਈ = Feminine',
                'examples': [
                    {'punjabi': 'ਕੁੜੀ', 'romanized': 'kudi', 'english': 'girl'},
                    {'punjabi': 'ਕੁੱਤੀ', 'romanized': 'kutti', 'english': 'dog (female)'},
                    {'punjabi': 'ਘੋੜੀ', 'romanized': 'ghodi', 'english': 'horse (female)'},
                ],
                'order': 2
            },
        ]

        for rule_data in rules4:
            rule, _ = GrammarRule.objects.update_or_create(
                topic=topic4,
                title=rule_data['title'],
                defaults=rule_data
            )
            stats['rules'] += 1

        first_rule4 = GrammarRule.objects.filter(topic=topic4).first()
        if first_rule4:
            self._create_exercises(first_rule4, [
                {'type': 'MC', 'question': 'ਮੁੰਡਾ is which gender?', 'correct': 'Masculine', 'options': ['Masculine', 'Feminine'], 'explanation': 'ਮੁੰਡਾ ends in ਆ = masculine'},
                {'type': 'FILL_BLANK', 'question': 'ਮੁੰਡਾ → _____', 'correct': 'ਕੁੜੀ', 'explanation': 'Boy → Girl (different word)'},
                {'type': 'FILL_BLANK', 'question': 'ਕੁੱਤਾ → _____', 'correct': 'ਕੁੱਤੀ', 'explanation': 'Change ਆ to ਈ'},
            ])
            stats['exercises'] += 3

        self.stdout.write(f'  Topic 4: Gender - {len(rules4)} rules')

        # ----- Topic 5: Verb Conjugation -----
        topic5, _ = GrammarTopic.objects.update_or_create(
            language='PUNJABI',
            name='Verb Conjugation',
            defaults={
                'name_native': 'ਕਿਰਿਆ ਰੂਪ',
                'description': 'Learn how verbs change based on subject and gender',
                'description_simple': 'Verbs change based on who does the action.',
                'level': 2,
                'order': 5,
                'is_active': True
            }
        )
        stats['topics'] += 1

        rules5 = [
            {
                'title': 'Present Tense - Masculine',
                'explanation': 'For male subjects: -ਦਾ ਹਾਂ (I), -ਦਾ ਹੈ (he), -ਦੇ ਹਾਂ (we)',
                'explanation_simple': 'Add -ਦਾ/-ਦੇ for male subjects.',
                'formula': 'Verb + ਦਾ/ਦੇ + ਹਾਂ/ਹੈ',
                'examples': [
                    {'punjabi': 'ਮੈਂ ਖਾਂਦਾ ਹਾਂ', 'romanized': 'Main khaanda haan', 'english': 'I eat (male)'},
                    {'punjabi': 'ਉਹ ਖਾਂਦਾ ਹੈ', 'romanized': 'Oh khaanda hai', 'english': 'He eats'},
                    {'punjabi': 'ਅਸੀਂ ਖਾਂਦੇ ਹਾਂ', 'romanized': 'Aseen khaande haan', 'english': 'We eat'},
                ],
                'order': 1
            },
            {
                'title': 'Present Tense - Feminine',
                'explanation': 'For female subjects: -ਦੀ ਹਾਂ (I), -ਦੀ ਹੈ (she)',
                'explanation_simple': 'Add -ਦੀ for female subjects.',
                'formula': 'Verb + ਦੀ + ਹਾਂ/ਹੈ',
                'examples': [
                    {'punjabi': 'ਮੈਂ ਖਾਂਦੀ ਹਾਂ', 'romanized': 'Main khaandi haan', 'english': 'I eat (female)'},
                    {'punjabi': 'ਉਹ ਖਾਂਦੀ ਹੈ', 'romanized': 'Oh khaandi hai', 'english': 'She eats'},
                ],
                'order': 2
            },
        ]

        for rule_data in rules5:
            rule, _ = GrammarRule.objects.update_or_create(
                topic=topic5,
                title=rule_data['title'],
                defaults=rule_data
            )
            stats['rules'] += 1

        first_rule5 = GrammarRule.objects.filter(topic=topic5).first()
        if first_rule5:
            self._create_exercises(first_rule5, [
                {'type': 'CONJUGATE', 'question': 'ਮੈਂ (male) + ਖਾ = ?', 'correct': 'ਖਾਂਦਾ ਹਾਂ', 'options': ['ਖਾਂਦਾ ਹਾਂ', 'ਖਾਂਦੀ ਹਾਂ', 'ਖਾਂਦੇ ਹਾਂ'], 'explanation': 'Male I = -ਦਾ ਹਾਂ'},
                {'type': 'CONJUGATE', 'question': 'ਉਹ (female) + ਜਾ = ?', 'correct': 'ਜਾਂਦੀ ਹੈ', 'options': ['ਜਾਂਦਾ ਹੈ', 'ਜਾਂਦੀ ਹੈ', 'ਜਾਂਦੇ ਹਨ'], 'explanation': 'Female she = -ਦੀ ਹੈ'},
                {'type': 'TRANSLATE', 'question': 'She goes', 'correct': 'ਉਹ ਜਾਂਦੀ ਹੈ', 'explanation': 'ਉਹ + ਜਾਂਦੀ ਹੈ'},
            ])
            stats['exercises'] += 3

        self.stdout.write(f'  Topic 5: Verb Conjugation - {len(rules5)} rules')
        self.stdout.write(self.style.SUCCESS(f'  PUNJABI Total: {stats["topics"]} topics, {stats["rules"]} rules, {stats["exercises"]} exercises'))

    # =========================================================================
    # HELPER METHOD
    # =========================================================================
    def _create_exercises(self, rule, exercises_data):
        """Create exercises for a rule."""
        for i, ex in enumerate(exercises_data):
            GrammarExercise.objects.update_or_create(
                rule=rule,
                question=ex['question'],
                defaults={
                    'exercise_type': ex['type'],
                    'correct_answer': ex['correct'],
                    'options': ex.get('options', []),
                    'explanation': ex.get('explanation', ''),
                    'hint': ex.get('hint', ''),
                    'difficulty': ex.get('difficulty', 1),
                    'points': ex.get('points', 10),
                    'order': i + 1
                }
            )
