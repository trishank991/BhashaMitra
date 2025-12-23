"""
Seed L1 Songs, Stories, and Peppi Phrases.
Run: python manage.py seed_l1_songs_stories

This seeds:
- 5 Songs with full Hindi lyrics
- 4 Stories with 5-6 pages each
- 25+ Peppi Hinglish feedback phrases
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.curriculum.models import CurriculumLevel, Song, PeppiPhrase
from apps.stories.models import Story, StoryPage
from apps.children.models import Child


class Command(BaseCommand):
    help = 'Seed L1 songs, stories, and Peppi phrases'

    def add_arguments(self, parser):
        parser.add_argument('--songs', action='store_true', help='Seed songs only')
        parser.add_argument('--stories', action='store_true', help='Seed stories only')
        parser.add_argument('--peppi', action='store_true', help='Seed Peppi phrases only')

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write(self.style.SUCCESS('L1 SONGS, STORIES & PEPPI SEEDING'))
        self.stdout.write('=' * 60 + '\n')

        # Check what to seed
        seed_all = not any([options['songs'], options['stories'], options['peppi']])

        if seed_all or options['songs']:
            self._seed_songs()

        if seed_all or options['stories']:
            self._seed_stories()

        if seed_all or options['peppi']:
            self._seed_peppi_phrases()

        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('SEEDING COMPLETE!'))
        self.stdout.write('=' * 60)
        self._verify_counts()

    def _seed_songs(self):
        """Seed 5 songs with full lyrics."""
        self.stdout.write('\n🎵 Seeding Songs...')

        # Get L1 level
        try:
            l1 = CurriculumLevel.objects.get(code='L1')
        except CurriculumLevel.DoesNotExist:
            self.stdout.write(self.style.ERROR('  ❌ L1 level not found! Run seed_curriculum_levels first.'))
            return

        songs_data = [
            {
                'title_english': 'Namaste Song',
                'title_hindi': 'नमस्ते गीत',
                'title_romanized': 'Namaste Geet',
                'lyrics_hindi': '''🎵 नमस्ते, नमस्ते, नमस्ते जी!
सबको मिलकर बोलो नमस्ते जी!

नमस्ते सुबह में, नमस्ते शाम को,
नमस्ते कहो सब दोस्तों को!

🎵 धन्यवाद, धन्यवाद, धन्यवाद जी!
Thank you बोलो, धन्यवाद जी!

कोई दे तोहफा, कोई दे प्यार,
धन्यवाद बोलो बार-बार!

🎵 कृपया, कृपया, कृपया जी!
Please बोलो, कृपया जी!

कुछ माँगो तो बोलो कृपया,
सब खुश होंगे, मिलेगा सब कुछ!

🎵 अलविदा, अलविदा, अलविदा जी!
Bye-bye बोलो, अलविदा जी!

जाते वक्त बोलो अलविदा,
फिर मिलेंगे, अलविदा!

🎵 नमस्ते, धन्यवाद, कृपया, अलविदा!
ये हैं magic words, याद रखो सदा!''',
                'lyrics_romanized': '''Namaste, namaste, namaste ji!
Sabko milkar bolo namaste ji!

Namaste subah mein, namaste shaam ko,
Namaste kaho sab doston ko!

Dhanyavaad, dhanyavaad, dhanyavaad ji!
Thank you bolo, dhanyavaad ji!

Kripaya, kripaya, kripaya ji!
Please bolo, kripaya ji!

Alvida, alvida, alvida ji!
Bye-bye bolo, alvida ji!''',
                'lyrics_english': '''Hello, hello, hello!
Let's all say hello together!

Hello in the morning, hello in the evening,
Say hello to all your friends!

Thank you, thank you, thank you!
Say thank you!

Please, please, please!
Say please!

Goodbye, goodbye, goodbye!
Say bye-bye, goodbye!''',
                'duration_seconds': 90,
                'category': 'EDUCATIONAL',
                'actions': [
                    {'time': 0, 'action': 'wave_hands', 'text': 'Wave your hands!'},
                    {'time': 30, 'action': 'bow', 'text': 'Bow your head!'},
                ],
                'order': 1,
            },
            {
                'title_english': 'Counting Song (1-10)',
                'title_hindi': 'एक दो तीन',
                'title_romanized': 'Ek Do Teen',
                'lyrics_hindi': '''🎵 एक दो तीन, चार पाँच छह,
सात आठ नौ, और फिर है दस!

एक 🍎 सेब, दो 🍌 केले,
तीन 🍊 संतरे, कितने प्यारे!

🎵 एक दो तीन, चार पाँच छह,
सात आठ नौ, और फिर है दस!

चार 🦋 तितली, पाँच 🌸 फूल,
छह ⭐ तारे, ये है cool!

🎵 एक दो तीन, चार पाँच छह,
सात आठ नौ, और फिर है दस!

सात 🐦 चिड़िया, आठ 🐟 मछली,
नौ 🎈 गुब्बारे, उड़े बादल में!

🎵 दस 👏 ताली बजाओ!
एक से दस तक गाओ!

एक, दो, तीन, चार, पाँच,
छह, सात, आठ, नौ, दस!

🎉 वाह! You did it! बहुत अच्छे!''',
                'lyrics_romanized': '''Ek do teen, chaar paanch chhah,
Saat aath nau, aur phir hai das!

Ek seb, do kele,
Teen santare, kitne pyaare!

Chaar titli, paanch phool,
Chhah taare, ye hai cool!

Saat chidiya, aath machhli,
Nau gubbare, ude baadal mein!

Das taali bajao!
Ek se das tak gao!''',
                'lyrics_english': '''One two three, four five six,
Seven eight nine, and then is ten!

One apple, two bananas,
Three oranges, so lovely!

Four butterflies, five flowers,
Six stars, this is cool!

Seven birds, eight fish,
Nine balloons, flew to the clouds!

Ten claps!
Sing from one to ten!''',
                'duration_seconds': 120,
                'category': 'EDUCATIONAL',
                'actions': [
                    {'time': 0, 'action': 'show_fingers', 'text': 'Show fingers!'},
                    {'time': 60, 'action': 'clap', 'text': 'Clap 10 times!'},
                ],
                'order': 2,
            },
            {
                'title_english': 'Hindi Vowels Song',
                'title_hindi': 'अ से अनार',
                'title_romanized': 'A Se Anaar',
                'lyrics_hindi': '''🎵 अ से अनार, आ से आम,
इ से इमली, ई से ईख!

(Chorus)
ये है हिंदी वर्णमाला,
Peppi के साथ गाओ!

🎵 उ से उल्लू, ऊ से ऊन,
ए से एड़ी, ऐ से ऐनक!

(Chorus)
ये है हिंदी वर्णमाला,
Peppi के साथ गाओ!

🎵 ओ से ओखली, औ से औरत,
अं से अंगूर, अः से... वाह!

(Chorus)
ये है हिंदी वर्णमाला,
Peppi के साथ गाओ!

🎵 अ आ इ ई उ ऊ,
ए ऐ ओ औ अं अः!

ये हैं स्वर, याद करो,
Peppi के साथ गाओ!

🎉 शाबाश! You learned all the swar!''',
                'lyrics_romanized': '''A se anaar, aa se aam,
I se imli, ee se eekh!

Ye hai Hindi varnamala,
Peppi ke saath gao!

U se ullu, oo se oon,
E se edi, ai se ainak!

O se okhli, au se aurat,
An se angoor, aha se... waah!

A aa i ee u oo,
E ai o au an aha!''',
                'lyrics_english': '''A for Pomegranate, Aa for Mango,
I for Tamarind, Ee for Sugarcane!

This is Hindi alphabet,
Sing with Peppi!

U for Owl, Oo for Wool,
E for Heel, Ai for Glasses!

These are vowels, remember them,
Sing with Peppi!''',
                'duration_seconds': 150,
                'category': 'EDUCATIONAL',
                'actions': [
                    {'time': 0, 'action': 'trace_letter', 'text': 'Trace the letters!'},
                ],
                'order': 3,
            },
            {
                'title_english': 'My Family Song',
                'title_hindi': 'मेरा परिवार',
                'title_romanized': 'Mera Parivaar',
                'lyrics_hindi': '''🎵 ये है मेरा परिवार,
सबसे प्यारा परिवार!

माँ है मेरी, I love you माँ! 💕
पापा हैं मेरे, I love you पापा! 💙

🎵 ये है मेरा परिवार,
सबसे प्यारा परिवार!

दादी जी हैं, दादा जी हैं,
पापा के माँ-पापा हैं!

🎵 ये है मेरा परिवार,
सबसे प्यारा परिवार!

नानी जी हैं, नाना जी हैं,
माँ के माँ-पापा हैं!

🎵 ये है मेरा परिवार,
सबसे प्यारा परिवार!

भाई है मेरा, बहन है मेरी,
मिलकर खेलें, family है मेरी!

🎵 माँ, पापा, दादी, दादा,
नानी, नाना, भाई, बहन!

ये है मेरा परिवार,
सबसे प्यारा परिवार! 🏠❤️''',
                'lyrics_romanized': '''Ye hai mera parivaar,
Sabse pyaara parivaar!

Maa hai meri, I love you maa!
Papa hain mere, I love you papa!

Dadi ji hain, dada ji hain,
Papa ke maa-papa hain!

Nani ji hain, nana ji hain,
Maa ke maa-papa hain!

Bhai hai mera, behen hai meri,
Milkar khelen, family hai meri!''',
                'lyrics_english': '''This is my family,
The most lovely family!

My mother, I love you mom!
My father, I love you dad!

Grandma and grandpa are there,
They are dad's parents!

Nani and nana are there,
They are mom's parents!

I have a brother, I have a sister,
We play together, this is my family!''',
                'duration_seconds': 105,
                'category': 'EDUCATIONAL',
                'actions': [
                    {'time': 0, 'action': 'point_family', 'text': 'Point to your family!'},
                    {'time': 50, 'action': 'hug', 'text': 'Hug someone!'},
                ],
                'order': 4,
            },
            {
                'title_english': 'Colors Song',
                'title_hindi': 'रंगों का खेल',
                'title_romanized': 'Rangon Ka Khel',
                'lyrics_hindi': '''🎵 रंग-रंग, रंग-रंग,
देखो कितने रंग!

🔴 लाल है टमाटर, लाल है सेब,
Red color को लाल बोलो!

🟡 पीला है केला, पीला है सूरज,
Yellow color को पीला बोलो!

🎵 रंग-रंग, रंग-रंग,
देखो कितने रंग!

🟢 हरा है पत्ता, हरा है मेंढक,
Green color को हरा बोलो!

🔵 नीला है आसमान, नीला है पानी,
Blue color को नीला बोलो!

🎵 रंग-रंग, रंग-रंग,
देखो कितने रंग!

🟠 नारंगी है संतरा, orange है carrot,
Orange color को नारंगी बोलो!

💗 गुलाबी है फूल, pink है heart,
Pink color को गुलाबी बोलो!

🎵 लाल, पीला, हरा, नीला,
नारंगी, गुलाबी!

⬜ सफेद है बादल, ⬛ काला है रात,
सब रंग याद करो, दिन और रात!

🎉 वाह! Rainbow complete! 🌈''',
                'lyrics_romanized': '''Rang-rang, rang-rang,
Dekho kitne rang!

Laal hai tamaatar, laal hai seb,
Red color ko laal bolo!

Peela hai kela, peela hai sooraj,
Yellow color ko peela bolo!

Hara hai patta, hara hai mendhak,
Green color ko hara bolo!

Neela hai aasmaan, neela hai paani,
Blue color ko neela bolo!''',
                'lyrics_english': '''Colors, colors,
See how many colors!

Red is tomato, red is apple,
Say red for red color!

Yellow is banana, yellow is sun,
Say yellow for yellow color!

Green is leaf, green is frog,
Say green for green color!

Blue is sky, blue is water,
Say blue for blue color!''',
                'duration_seconds': 90,
                'category': 'EDUCATIONAL',
                'actions': [
                    {'time': 0, 'action': 'find_color', 'text': 'Find something red!'},
                    {'time': 30, 'action': 'find_color', 'text': 'Find something yellow!'},
                ],
                'order': 5,
            },
        ]

        for song_data in songs_data:
            song, created = Song.objects.update_or_create(
                title_hindi=song_data['title_hindi'],
                level=l1,
                defaults={
                    'title_english': song_data['title_english'],
                    'title_romanized': song_data['title_romanized'],
                    'lyrics_hindi': song_data['lyrics_hindi'],
                    'lyrics_romanized': song_data['lyrics_romanized'],
                    'lyrics_english': song_data['lyrics_english'],
                    'duration_seconds': song_data['duration_seconds'],
                    'category': song_data['category'],
                    'actions': song_data['actions'],
                    'order': song_data['order'],
                    'age_min': 3,
                    'age_max': 6,
                    'is_active': True,
                }
            )
            status = '✅ Created' if created else '♻️ Updated'
            self.stdout.write(f'  {status}: {song.title_english}')

        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(songs_data)} songs seeded'))

    def _seed_stories(self):
        """Seed 4 stories with complete pages."""
        self.stdout.write('\n📚 Seeding Stories...')

        stories_data = [
            {
                'storyweaver_id': 'BM_STORY_MEET_PEPPI',
                'title': 'Meet Peppi',
                'title_hindi': 'पेप्पी से मिलो',
                'title_romanized': 'Peppi Se Milo',
                'language': Child.Language.HINDI,
                'level': 1,
                'synopsis': 'Introduction to Peppi, our friendly cat teacher',
                'theme': 'introduction',
                'age_min': 3,
                'age_max': 6,
                'is_l1_content': True,
                'pages': [
                    {'page_number': 1, 'text_hindi': 'नमस्ते! मेरा नाम पेप्पी है।', 'text_english': 'Hello! My name is Peppi.', 'text_romanized': 'Namaste! Mera naam Peppi hai.'},
                    {'page_number': 2, 'text_hindi': 'मैं एक बिल्ली हूँ। एक प्यारी सी बिल्ली! 🐱', 'text_english': 'I am a cat. A cute little cat!', 'text_romanized': 'Main ek billi hoon. Ek pyaari si billi!'},
                    {'page_number': 3, 'text_hindi': 'मैं तुम्हारी दोस्त हूँ। हम साथ में Hindi सीखेंगे!', 'text_english': 'I am your friend. We will learn Hindi together!', 'text_romanized': 'Main tumhari dost hoon. Hum saath mein Hindi seekhenge!'},
                    {'page_number': 4, 'text_hindi': 'क्या तुम ready हो? Let\'s say नमस्ते!', 'text_english': 'Are you ready? Let\'s say hello!', 'text_romanized': 'Kya tum ready ho? Let\'s say namaste!'},
                    {'page_number': 5, 'text_hindi': 'वाह! बहुत अच्छे! तुम तो champion हो! 🌟', 'text_english': 'Wow! Very good! You are a champion!', 'text_romanized': 'Waah! Bahut achhe! Tum to champion ho!'},
                ],
            },
            {
                'storyweaver_id': 'BM_STORY_FAMILY',
                'title': 'My Family',
                'title_hindi': 'मेरा परिवार',
                'title_romanized': 'Mera Parivaar',
                'language': Child.Language.HINDI,
                'level': 1,
                'synopsis': 'Learn family member names with Aarya from Auckland',
                'theme': 'family',
                'age_min': 3,
                'age_max': 6,
                'is_l1_content': True,
                'pages': [
                    {'page_number': 1, 'text_hindi': 'ये है आर्या। आर्या Auckland में रहती है।', 'text_english': 'This is Aarya. Aarya lives in Auckland.', 'text_romanized': 'Ye hai Aarya. Aarya Auckland mein rehti hai.'},
                    {'page_number': 2, 'text_hindi': 'ये हैं आर्या की माँ। माँ बहुत प्यारी हैं। 💕', 'text_english': 'This is Aarya\'s mom. Mom is very lovely.', 'text_romanized': 'Ye hain Aarya ki maa. Maa bahut pyaari hain.'},
                    {'page_number': 3, 'text_hindi': 'ये हैं आर्या के पापा। पापा office जाते हैं। 💼', 'text_english': 'This is Aarya\'s dad. Dad goes to office.', 'text_romanized': 'Ye hain Aarya ke papa. Papa office jaate hain.'},
                    {'page_number': 4, 'text_hindi': 'दादी-दादा India में रहते हैं। Video call पर मिलते हैं! 📱', 'text_english': 'Grandma-grandpa live in India. We meet on video call!', 'text_romanized': 'Dadi-dada India mein rehte hain. Video call par milte hain!'},
                    {'page_number': 5, 'text_hindi': 'आर्या का छोटा भाई है - अर्जुन। वे साथ खेलते हैं! 🎮', 'text_english': 'Aarya has a little brother - Arjun. They play together!', 'text_romanized': 'Aarya ka chhota bhai hai - Arjun. Ve saath khelte hain!'},
                    {'page_number': 6, 'text_hindi': 'आर्या अपने परिवार से बहुत प्यार करती है। I love my family! ❤️', 'text_english': 'Aarya loves her family very much.', 'text_romanized': 'Aarya apne parivaar se bahut pyaar karti hai.'},
                ],
            },
            {
                'storyweaver_id': 'BM_STORY_JUNGLE',
                'title': 'Jungle Friends',
                'title_hindi': 'जंगल के दोस्त',
                'title_romanized': 'Jungle Ke Dost',
                'language': Child.Language.HINDI,
                'level': 1,
                'synopsis': 'Meet animals and learn their Hindi names',
                'theme': 'animals',
                'age_min': 3,
                'age_max': 6,
                'is_l1_content': True,
                'pages': [
                    {'page_number': 1, 'text_hindi': 'पेप्पी जंगल में गई। जंगल बहुत बड़ा था! 🌳', 'text_english': 'Peppi went to the jungle. The jungle was very big!', 'text_romanized': 'Peppi jungle mein gayi. Jungle bahut bada tha!'},
                    {'page_number': 2, 'text_hindi': 'पहले मिला शेर! शेर बोला - "गर्र्र!" 🦁', 'text_english': 'First she met a lion! The lion said - "Roar!"', 'text_romanized': 'Pehle mila sher! Sher bola - "Garrr!"'},
                    {'page_number': 3, 'text_hindi': 'फिर मिला हाथी! हाथी बहुत बड़ा था। "पों पों!" 🐘', 'text_english': 'Then she met an elephant! The elephant was very big.', 'text_romanized': 'Phir mila haathi! Haathi bahut bada tha. "Pon pon!"'},
                    {'page_number': 4, 'text_hindi': 'बंदर पेड़ पर था! बंदर बोला - "ऊ ऊ आ आ!" 🐒', 'text_english': 'The monkey was on the tree! The monkey said - "Ooh ooh ah ah!"', 'text_romanized': 'Bandar ped par tha! Bandar bola - "Oo oo aa aa!"'},
                    {'page_number': 5, 'text_hindi': 'मोर ने dance किया! मोर भारत का national bird है! 🦚', 'text_english': 'The peacock danced! Peacock is India\'s national bird!', 'text_romanized': 'Mor ne dance kiya! Mor Bharat ka national bird hai!'},
                    {'page_number': 6, 'text_hindi': 'सब animals पेप्पी के दोस्त बन गए! जंगल में party! 🎉', 'text_english': 'All animals became Peppi\'s friends! Party in the jungle!', 'text_romanized': 'Sab animals Peppi ke dost ban gaye! Jungle mein party!'},
                ],
            },
            {
                'storyweaver_id': 'BM_STORY_COLORS',
                'title': 'World of Colors',
                'title_hindi': 'रंगों की दुनिया',
                'title_romanized': 'Rangon Ki Duniya',
                'language': Child.Language.HINDI,
                'level': 1,
                'synopsis': 'Learn colors through a colorful rainbow adventure',
                'theme': 'colors',
                'age_min': 3,
                'age_max': 6,
                'is_l1_content': True,
                'pages': [
                    {'page_number': 1, 'text_hindi': 'बारिश के बाद आसमान में इंद्रधनुष आया! 🌈', 'text_english': 'After the rain, a rainbow appeared in the sky!', 'text_romanized': 'Baarish ke baad aasmaan mein indradhanush aaya!'},
                    {'page_number': 2, 'text_hindi': 'देखो लाल रंग! 🔴 सेब लाल है, टमाटर भी लाल!', 'text_english': 'Look, red color! Apple is red, tomato is also red!', 'text_romanized': 'Dekho laal rang! Seb laal hai, tamaatar bhi laal!'},
                    {'page_number': 3, 'text_hindi': 'पीला रंग है sunshine का! 🟡 सूरज पीला, केला भी पीला!', 'text_english': 'Yellow is the color of sunshine! Sun is yellow, banana too!', 'text_romanized': 'Peela rang hai sunshine ka! Sooraj peela, kela bhi peela!'},
                    {'page_number': 4, 'text_hindi': 'हरा रंग है nature का! 🟢 पत्ते हरे, घास भी हरी!', 'text_english': 'Green is the color of nature! Leaves are green, grass too!', 'text_romanized': 'Hara rang hai nature ka! Patte hare, ghaas bhi hari!'},
                    {'page_number': 5, 'text_hindi': 'नीला आसमान, नीला पानी! 🔵 Blue is everywhere!', 'text_english': 'Blue sky, blue water! Blue is everywhere!', 'text_romanized': 'Neela aasmaan, neela paani! Blue is everywhere!'},
                ],
            },
        ]

        for story_data in stories_data:
            pages = story_data.pop('pages')
            story, created = Story.objects.update_or_create(
                storyweaver_id=story_data['storyweaver_id'],
                defaults={
                    'title': story_data['title'],
                    'title_hindi': story_data['title_hindi'],
                    'title_romanized': story_data['title_romanized'],
                    'language': story_data['language'],
                    'level': story_data['level'],
                    'page_count': len(pages),
                    'cover_image_url': f"https://bhashamitra.com/images/stories/{story_data['storyweaver_id'].lower()}.png",
                    'synopsis': story_data['synopsis'],
                    'theme': story_data['theme'],
                    'age_min': story_data['age_min'],
                    'age_max': story_data['age_max'],
                    'is_l1_content': story_data['is_l1_content'],
                }
            )

            # Create pages
            for page_data in pages:
                StoryPage.objects.update_or_create(
                    story=story,
                    page_number=page_data['page_number'],
                    defaults={
                        'text_content': page_data['text_english'],
                        'text_hindi': page_data['text_hindi'],
                        'text_romanized': page_data['text_romanized'],
                    }
                )

            status = '✅ Created' if created else '♻️ Updated'
            self.stdout.write(f'  {status}: {story.title} ({len(pages)} pages)')

        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(stories_data)} stories seeded'))

    def _seed_peppi_phrases(self):
        """Seed Peppi feedback phrases."""
        self.stdout.write('\n🐱 Seeding Peppi Phrases...')

        phrases = [
            # Correct answers (5 variations)
            {'category': 'correct', 'text_hindi': 'बहुत अच्छे!', 'text_english': 'Very good!', 'audio_file': 'peppi_correct_1.mp3'},
            {'category': 'correct', 'text_hindi': 'वाह! Perfect!', 'text_english': 'Wow! Perfect!', 'audio_file': 'peppi_correct_2.mp3'},
            {'category': 'correct', 'text_hindi': 'हाँ! That\'s right!', 'text_english': 'Yes! That\'s right!', 'audio_file': 'peppi_correct_3.mp3'},
            {'category': 'correct', 'text_hindi': 'शाबाश! Champion!', 'text_english': 'Bravo! Champion!', 'audio_file': 'peppi_correct_4.mp3'},
            {'category': 'correct', 'text_hindi': 'Excellent! तुम तो genius हो!', 'text_english': 'Excellent! You\'re a genius!', 'audio_file': 'peppi_correct_5.mp3'},

            # Wrong answers - Encouraging (5 variations)
            {'category': 'wrong', 'text_hindi': 'ओह! कोई बात नहीं, try again!', 'text_english': 'Oh! No worries, try again!', 'audio_file': 'peppi_wrong_1.mp3'},
            {'category': 'wrong', 'text_hindi': 'Almost! एक बार और!', 'text_english': 'Almost! One more time!', 'audio_file': 'peppi_wrong_2.mp3'},
            {'category': 'wrong', 'text_hindi': 'Hmm, ज़रा सोचो...', 'text_english': 'Hmm, think a little...', 'audio_file': 'peppi_wrong_3.mp3'},
            {'category': 'wrong', 'text_hindi': 'नहीं, but you\'re learning! 💪', 'text_english': 'No, but you\'re learning!', 'audio_file': 'peppi_wrong_4.mp3'},
            {'category': 'wrong', 'text_hindi': 'Not quite! Listen again!', 'text_english': 'Not quite! Listen again!', 'audio_file': 'peppi_wrong_5.mp3'},

            # Streaks
            {'category': 'streak', 'text_hindi': 'Wow! तुम on fire हो! 🔥', 'text_english': 'Wow! You\'re on fire!', 'streak_count': 3, 'audio_file': 'peppi_streak_3.mp3'},
            {'category': 'streak', 'text_hindi': 'पाँच correct! Unstoppable! 🚀', 'text_english': 'Five correct! Unstoppable!', 'streak_count': 5, 'audio_file': 'peppi_streak_5.mp3'},
            {'category': 'streak', 'text_hindi': 'सात in a row! Superstar! ⭐', 'text_english': 'Seven in a row! Superstar!', 'streak_count': 7, 'audio_file': 'peppi_streak_7.mp3'},
            {'category': 'streak', 'text_hindi': 'दस! Perfect score! 🏆👑', 'text_english': 'Ten! Perfect score!', 'streak_count': 10, 'audio_file': 'peppi_streak_10.mp3'},

            # Greetings
            {'category': 'greeting', 'text_hindi': 'Good morning! तैयार हो?', 'text_english': 'Good morning! Ready?', 'context': 'morning', 'audio_file': 'peppi_morning.mp3'},
            {'category': 'greeting', 'text_hindi': 'Hello! Let\'s learn!', 'text_english': 'Hello! Let\'s learn!', 'context': 'afternoon', 'audio_file': 'peppi_afternoon.mp3'},
            {'category': 'greeting', 'text_hindi': 'Good evening! Fun time!', 'text_english': 'Good evening! Fun time!', 'context': 'evening', 'audio_file': 'peppi_evening.mp3'},
            {'category': 'greeting', 'text_hindi': 'तुम वापस आए! मुझे खुशी हुई!', 'text_english': 'You\'re back! I\'m happy!', 'context': 'return', 'audio_file': 'peppi_return.mp3'},

            # Farewells
            {'category': 'farewell', 'text_hindi': 'Bye bye! कल मिलेंगे!', 'text_english': 'Bye bye! See you tomorrow!', 'audio_file': 'peppi_bye_1.mp3'},
            {'category': 'farewell', 'text_hindi': 'अलविदा! You did great today!', 'text_english': 'Goodbye! You did great today!', 'audio_file': 'peppi_bye_2.mp3'},
            {'category': 'farewell', 'text_hindi': 'Good job! Rest now, come back soon!', 'text_english': 'Good job! Rest now, come back soon!', 'audio_file': 'peppi_bye_3.mp3'},

            # Encouragement
            {'category': 'encouragement', 'text_hindi': 'Take your time! कोई जल्दी नहीं!', 'text_english': 'Take your time! No hurry!', 'audio_file': 'peppi_encourage_1.mp3'},
            {'category': 'encouragement', 'text_hindi': 'You can do it! I believe in you!', 'text_english': 'You can do it! I believe in you!', 'audio_file': 'peppi_encourage_2.mp3'},
            {'category': 'encouragement', 'text_hindi': 'हिम्मत रखो! Don\'t give up!', 'text_english': 'Be brave! Don\'t give up!', 'audio_file': 'peppi_encourage_3.mp3'},

            # Completion
            {'category': 'completion', 'text_hindi': 'Lesson complete! 🎉 तुमने बहुत अच्छा किया!', 'text_english': 'Lesson complete! You did great!', 'audio_file': 'peppi_complete_1.mp3'},
            {'category': 'completion', 'text_hindi': 'वाह! All done! You\'re a star! ⭐', 'text_english': 'Wow! All done! You\'re a star!', 'audio_file': 'peppi_complete_2.mp3'},
            {'category': 'completion', 'text_hindi': 'Amazing work! Ready for the next one?', 'text_english': 'Amazing work! Ready for the next one?', 'audio_file': 'peppi_complete_3.mp3'},
        ]

        for phrase_data in phrases:
            PeppiPhrase.objects.update_or_create(
                text_hindi=phrase_data['text_hindi'],
                defaults={
                    'category': phrase_data['category'],
                    'text_english': phrase_data.get('text_english', ''),
                    'audio_file': phrase_data.get('audio_file', ''),
                    'streak_count': phrase_data.get('streak_count'),
                    'context': phrase_data.get('context', ''),
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(phrases)} Peppi phrases seeded'))

    def _verify_counts(self):
        """Verify seeded data counts."""
        self.stdout.write('\n📊 Verification:')

        try:
            from apps.curriculum.models import Song, PeppiPhrase
            from apps.stories.models import Story, StoryPage

            counts = {
                'Songs': Song.objects.filter(level__code='L1').count(),
                'Stories': Story.objects.filter(is_l1_content=True).count(),
                'Story Pages': StoryPage.objects.filter(story__is_l1_content=True).count(),
                'Peppi Phrases': PeppiPhrase.objects.count(),
            }

            for name, count in counts.items():
                status = '✅' if count > 0 else '❌'
                self.stdout.write(f'  {status} {name}: {count}')

        except Exception as e:
            self.stdout.write(f'  Error getting counts: {str(e)}')
