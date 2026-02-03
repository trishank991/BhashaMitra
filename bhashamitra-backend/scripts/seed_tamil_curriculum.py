"""Seed complete Tamil curriculum (alphabet, vocabulary, grammar)."""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.curriculum.models.script import Script, AlphabetCategory, Letter
from apps.curriculum.models.vocabulary import VocabularyTheme, VocabularyWord
from apps.curriculum.models.grammar import GrammarTopic, GrammarRule


# Tamil Vowels (உயிர் எழுத்துக்கள்)
VOWELS = [
    {'char': 'அ', 'roman': 'a', 'ipa': 'ʌ', 'example': 'அம்மா', 'ex_roman': 'ammaa', 'ex_trans': 'mother'},
    {'char': 'ஆ', 'roman': 'aa', 'ipa': 'aː', 'example': 'ஆடு', 'ex_roman': 'aadu', 'ex_trans': 'goat'},
    {'char': 'இ', 'roman': 'i', 'ipa': 'i', 'example': 'இலை', 'ex_roman': 'ilai', 'ex_trans': 'leaf'},
    {'char': 'ஈ', 'roman': 'ee', 'ipa': 'iː', 'example': 'ஈ', 'ex_roman': 'ee', 'ex_trans': 'fly'},
    {'char': 'உ', 'roman': 'u', 'ipa': 'u', 'example': 'உப்பு', 'ex_roman': 'uppu', 'ex_trans': 'salt'},
    {'char': 'ஊ', 'roman': 'uu', 'ipa': 'uː', 'example': 'ஊசி', 'ex_roman': 'oosi', 'ex_trans': 'needle'},
    {'char': 'எ', 'roman': 'e', 'ipa': 'e', 'example': 'எலி', 'ex_roman': 'eli', 'ex_trans': 'rat'},
    {'char': 'ஏ', 'roman': 'e', 'ipa': 'eː', 'example': 'ஏர்', 'ex_roman': 'er', 'ex_trans': 'plough'},
    {'char': 'ஐ', 'roman': 'ai', 'ipa': 'aɪ', 'example': 'ஐந்து', 'ex_roman': 'ainthu', 'ex_trans': 'five'},
    {'char': 'ஒ', 'roman': 'o', 'ipa': 'o', 'example': 'ஒட்டகம்', 'ex_roman': 'ottakam', 'ex_trans': 'camel'},
    {'char': 'ஓ', 'roman': 'o', 'ipa': 'oː', 'example': 'ஓடு', 'ex_roman': 'odu', 'ex_trans': 'run'},
    {'char': 'ஔ', 'roman': 'au', 'ipa': 'aʊ', 'example': 'ஔவை', 'ex_roman': 'auvai', 'ex_trans': 'Auvai (poet)'},
]

# Tamil Consonants (மெய் எழுத்துக்கள்)
CONSONANTS = [
    {'char': 'க', 'roman': 'ka', 'ipa': 'k', 'example': 'கடல்', 'ex_roman': 'kadal', 'ex_trans': 'sea'},
    {'char': 'ங', 'roman': 'nga', 'ipa': 'ŋ', 'example': 'அங்கு', 'ex_roman': 'angu', 'ex_trans': 'there'},
    {'char': 'ச', 'roman': 'cha', 'ipa': 't͡ʃ', 'example': 'சந்தை', 'ex_roman': 'santhai', 'ex_trans': 'market'},
    {'char': 'ஞ', 'roman': 'nya', 'ipa': 'ɲ', 'example': 'ஞாயிறு', 'ex_roman': 'gnaayiru', 'ex_trans': 'Sunday'},
    {'char': 'ட', 'roman': 'ta', 'ipa': 'ʈ', 'example': 'டமாரம்', 'ex_roman': 'tamaaram', 'ex_trans': 'drum'},
    {'char': 'ண', 'roman': 'na', 'ipa': 'ɳ', 'example': 'கண்', 'ex_roman': 'kan', 'ex_trans': 'eye'},
    {'char': 'த', 'roman': 'tha', 'ipa': 't̪', 'example': 'தண்ணீர்', 'ex_roman': 'thanneer', 'ex_trans': 'water'},
    {'char': 'ந', 'roman': 'na', 'ipa': 'n', 'example': 'நாய்', 'ex_roman': 'naai', 'ex_trans': 'dog'},
    {'char': 'ப', 'roman': 'pa', 'ipa': 'p', 'example': 'பல்', 'ex_roman': 'pal', 'ex_trans': 'tooth'},
    {'char': 'ம', 'roman': 'ma', 'ipa': 'm', 'example': 'மலை', 'ex_roman': 'malai', 'ex_trans': 'mountain'},
    {'char': 'ய', 'roman': 'ya', 'ipa': 'j', 'example': 'யானை', 'ex_roman': 'yaanai', 'ex_trans': 'elephant'},
    {'char': 'ர', 'roman': 'ra', 'ipa': 'ɾ', 'example': 'ரயில்', 'ex_roman': 'rayil', 'ex_trans': 'train'},
    {'char': 'ல', 'roman': 'la', 'ipa': 'l', 'example': 'லட்டு', 'ex_roman': 'lattu', 'ex_trans': 'sweet'},
    {'char': 'வ', 'roman': 'va', 'ipa': 'ʋ', 'example': 'வண்டி', 'ex_roman': 'vandi', 'ex_trans': 'cart'},
    {'char': 'ழ', 'roman': 'zha', 'ipa': 'ɻ', 'example': 'தமிழ்', 'ex_roman': 'thamizh', 'ex_trans': 'Tamil'},
    {'char': 'ள', 'roman': 'la', 'ipa': 'ɭ', 'example': 'பள்ளி', 'ex_roman': 'palli', 'ex_trans': 'school'},
    {'char': 'ற', 'roman': 'ra', 'ipa': 'r', 'example': 'நெற்று', 'ex_roman': 'nerru', 'ex_trans': 'forehead'},
    {'char': 'ன', 'roman': 'na', 'ipa': 'n', 'example': 'மனம்', 'ex_roman': 'manam', 'ex_trans': 'mind'},
]

# Tamil Vocabulary Themes
THEMES = [
    {
        'language': 'TAMIL',
        'name': 'Family',
        'name_native': 'குடும்பம்',
        'description': 'Learn words for family members',
        'icon': 'users',
        'level': 1,
        'order': 1,
        'words': [
            {'word': 'அம்மா', 'roman': 'ammaa', 'trans': 'mother', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'என் அம்மா நல்லவர்.'},
            {'word': 'அப்பா', 'roman': 'appaa', 'trans': 'father', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'என் அப்பா வேலைக்கு போகிறார்.'},
            {'word': 'அண்ணன்', 'roman': 'annan', 'trans': 'elder brother', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'என் அண்ணன் விளையாடுகிறான்.'},
            {'word': 'அக்கா', 'roman': 'akkaa', 'trans': 'elder sister', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'என் அக்கா படிக்கிறாள்.'},
            {'word': 'தம்பி', 'roman': 'thambi', 'trans': 'younger brother', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'என் தம்பி சிறியவன்.'},
            {'word': 'தங்கை', 'roman': 'thangai', 'trans': 'younger sister', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'என் தங்கை அழகாக இருக்கிறாள்.'},
            {'word': 'தாத்தா', 'roman': 'thaathaa', 'trans': 'grandfather', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'என் தாத்தா கதை சொல்கிறார்.'},
            {'word': 'பாட்டி', 'roman': 'paatti', 'trans': 'grandmother', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'என் பாட்டி சமைக்கிறார்.'},
            {'word': 'மாமா', 'roman': 'maamaa', 'trans': 'uncle (maternal)', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'என் மாமா டாக்டர்.'},
            {'word': 'அத்தை', 'roman': 'atthai', 'trans': 'aunt (paternal)', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'என் அத்தை ஆசிரியர்.'},
        ]
    },
    {
        'language': 'TAMIL',
        'name': 'Colors',
        'name_native': 'நிறங்கள்',
        'description': 'Learn words for colors',
        'icon': 'palette',
        'level': 1,
        'order': 2,
        'words': [
            {'word': 'சிவப்பு', 'roman': 'sivappu', 'trans': 'red', 'pos': 'ADJECTIVE', 'gender': 'NONE', 'sentence': 'ஆப்பிள் சிவப்பு நிறம்.'},
            {'word': 'பச்சை', 'roman': 'pachchai', 'trans': 'green', 'pos': 'ADJECTIVE', 'gender': 'NONE', 'sentence': 'இலை பச்சை நிறம்.'},
            {'word': 'நீலம்', 'roman': 'neelam', 'trans': 'blue', 'pos': 'ADJECTIVE', 'gender': 'NONE', 'sentence': 'வானம் நீலம்.'},
            {'word': 'மஞ்சள்', 'roman': 'manjal', 'trans': 'yellow', 'pos': 'ADJECTIVE', 'gender': 'NONE', 'sentence': 'வாழைப்பழம் மஞ்சள்.'},
            {'word': 'கருப்பு', 'roman': 'karuppu', 'trans': 'black', 'pos': 'ADJECTIVE', 'gender': 'NONE', 'sentence': 'காகம் கருப்பு.'},
            {'word': 'வெள்ளை', 'roman': 'vellai', 'trans': 'white', 'pos': 'ADJECTIVE', 'gender': 'NONE', 'sentence': 'பால் வெள்ளை.'},
            {'word': 'ஆரஞ்சு', 'roman': 'aranchu', 'trans': 'orange', 'pos': 'ADJECTIVE', 'gender': 'NONE', 'sentence': 'ஆரஞ்சுப்பழம் ஆரஞ்சு நிறம்.'},
            {'word': 'இளஞ்சிவப்பு', 'roman': 'ilanchivappu', 'trans': 'pink', 'pos': 'ADJECTIVE', 'gender': 'NONE', 'sentence': 'பூ இளஞ்சிவப்பு.'},
            {'word': 'ஊதா', 'roman': 'oothaa', 'trans': 'purple', 'pos': 'ADJECTIVE', 'gender': 'NONE', 'sentence': 'திராட்சை ஊதா நிறம்.'},
            {'word': 'பழுப்பு', 'roman': 'pazhuppu', 'trans': 'brown', 'pos': 'ADJECTIVE', 'gender': 'NONE', 'sentence': 'நாய் பழுப்பு நிறம்.'},
        ]
    },
    {
        'language': 'TAMIL',
        'name': 'Numbers',
        'name_native': 'எண்கள்',
        'description': 'Learn numbers in Tamil',
        'icon': 'hash',
        'level': 1,
        'order': 3,
        'words': [
            {'word': 'ஒன்று', 'roman': 'ondru', 'trans': 'one (1)', 'pos': 'NUMBER', 'gender': 'NONE', 'sentence': 'என்னிடம் ஒன்று புத்தகம் உள்ளது.'},
            {'word': 'இரண்டு', 'roman': 'irandu', 'trans': 'two (2)', 'pos': 'NUMBER', 'gender': 'NONE', 'sentence': 'எனக்கு இரண்டு கைகள் உள்ளன.'},
            {'word': 'மூன்று', 'roman': 'moondru', 'trans': 'three (3)', 'pos': 'NUMBER', 'gender': 'NONE', 'sentence': 'மூன்று பூனைகள் உள்ளன.'},
            {'word': 'நான்கு', 'roman': 'naangu', 'trans': 'four (4)', 'pos': 'NUMBER', 'gender': 'NONE', 'sentence': 'நாற்காலிக்கு நான்கு கால்கள் உள்ளன.'},
            {'word': 'ஐந்து', 'roman': 'ainthu', 'trans': 'five (5)', 'pos': 'NUMBER', 'gender': 'NONE', 'sentence': 'கையில் ஐந்து விரல்கள் உள்ளன.'},
            {'word': 'ஆறு', 'roman': 'aaru', 'trans': 'six (6)', 'pos': 'NUMBER', 'gender': 'NONE', 'sentence': 'ஆறு நாட்கள் கழிந்தன.'},
            {'word': 'ஏழு', 'roman': 'ezhu', 'trans': 'seven (7)', 'pos': 'NUMBER', 'gender': 'NONE', 'sentence': 'வாரத்தில் ஏழு நாட்கள் உள்ளன.'},
            {'word': 'எட்டு', 'roman': 'ettu', 'trans': 'eight (8)', 'pos': 'NUMBER', 'gender': 'NONE', 'sentence': 'சிலந்திக்கு எட்டு கால்கள் உள்ளன.'},
            {'word': 'ஒன்பது', 'roman': 'onbathu', 'trans': 'nine (9)', 'pos': 'NUMBER', 'gender': 'NONE', 'sentence': 'ஒன்பது கோள்கள் உள்ளன.'},
            {'word': 'பத்து', 'roman': 'paththu', 'trans': 'ten (10)', 'pos': 'NUMBER', 'gender': 'NONE', 'sentence': 'பத்து ரூபாய் கொடுங்கள்.'},
        ]
    },
    {
        'language': 'TAMIL',
        'name': 'Animals',
        'name_native': 'விலங்குகள்',
        'description': 'Learn words for animals',
        'icon': 'paw-print',
        'level': 1,
        'order': 4,
        'words': [
            {'word': 'நாய்', 'roman': 'naai', 'trans': 'dog', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'நாய் குரைக்கிறது.'},
            {'word': 'பூனை', 'roman': 'poonai', 'trans': 'cat', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'பூனை மியாவ் என்று கத்துகிறது.'},
            {'word': 'பசு', 'roman': 'pasu', 'trans': 'cow', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'பசு பால் தருகிறது.'},
            {'word': 'குதிரை', 'roman': 'kuthirai', 'trans': 'horse', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'குதிரை வேகமாக ஓடுகிறது.'},
            {'word': 'யானை', 'roman': 'yaanai', 'trans': 'elephant', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'யானை பெரியது.'},
            {'word': 'சிங்கம்', 'roman': 'singam', 'trans': 'lion', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'சிங்கம் காட்டு ராஜா.'},
            {'word': 'குரங்கு', 'roman': 'kurangu', 'trans': 'monkey', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'குரங்கு மரத்தில் ஏறுகிறது.'},
            {'word': 'பறவை', 'roman': 'paravai', 'trans': 'bird', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'பறவை பறக்கிறது.'},
            {'word': 'மீன்', 'roman': 'meen', 'trans': 'fish', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'மீன் தண்ணீரில் நீந்துகிறது.'},
            {'word': 'முயல்', 'roman': 'muyal', 'trans': 'rabbit', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'முயல் கேரட் சாப்பிடுகிறது.'},
        ]
    },
    {
        'language': 'TAMIL',
        'name': 'Food',
        'name_native': 'உணவு',
        'description': 'Learn words for food items',
        'icon': 'utensils',
        'level': 1,
        'order': 5,
        'words': [
            {'word': 'சோறு', 'roman': 'soru', 'trans': 'cooked rice', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'அம்மா சோறு சமைக்கிறார்.'},
            {'word': 'அரிசி', 'roman': 'arisi', 'trans': 'rice', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'அரிசி வெள்ளையாக உள்ளது.'},
            {'word': 'சாம்பார்', 'roman': 'saambaar', 'trans': 'sambar (lentil stew)', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'சாம்பார் சுவையாக உள்ளது.'},
            {'word': 'காய்கறி', 'roman': 'kaaikari', 'trans': 'vegetable', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'காய்கறி நல்லது.'},
            {'word': 'பால்', 'roman': 'paal', 'trans': 'milk', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'பால் குடிப்பது நல்லது.'},
            {'word': 'தண்ணீர்', 'roman': 'thanneer', 'trans': 'water', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'தண்ணீர் அவசியம்.'},
            {'word': 'பழம்', 'roman': 'pazham', 'trans': 'fruit', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'பழம் சாப்பிட வேண்டும்.'},
            {'word': 'இனிப்பு', 'roman': 'inippu', 'trans': 'sweet', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'இனிப்பு இனிப்பாக இருக்கும்.'},
            {'word': 'மாம்பழம்', 'roman': 'maampazham', 'trans': 'mango', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'மாம்பழம் பழங்களின் ராஜா.'},
            {'word': 'ஆப்பிள்', 'roman': 'aappil', 'trans': 'apple', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'ஆப்பிள் சிவப்பு.'},
        ]
    },
    {
        'language': 'TAMIL',
        'name': 'Body Parts',
        'name_native': 'உடல் உறுப்புகள்',
        'description': 'Learn words for body parts',
        'icon': 'hand',
        'level': 1,
        'order': 6,
        'words': [
            {'word': 'தலை', 'roman': 'thalai', 'trans': 'head', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'தலையில் மூளை உள்ளது.'},
            {'word': 'கண்', 'roman': 'kan', 'trans': 'eye', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'கண்களால் பார்க்கிறோம்.'},
            {'word': 'காது', 'roman': 'kaathu', 'trans': 'ear', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'காதுகளால் கேட்கிறோம்.'},
            {'word': 'மூக்கு', 'roman': 'mookku', 'trans': 'nose', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'மூக்கால் முகருகிறோம்.'},
            {'word': 'வாய்', 'roman': 'vaai', 'trans': 'mouth', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'வாயால் சாப்பிடுகிறோம்.'},
            {'word': 'கை', 'roman': 'kai', 'trans': 'hand', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'கையால் வேலை செய்கிறோம்.'},
            {'word': 'கால்', 'roman': 'kaal', 'trans': 'leg/foot', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'கால்களால் நடக்கிறோம்.'},
            {'word': 'விரல்', 'roman': 'viral', 'trans': 'finger', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'கையில் ஐந்து விரல்கள் உள்ளன.'},
            {'word': 'பல்', 'roman': 'pal', 'trans': 'tooth', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'பல்லால் மெல்கிறோம்.'},
            {'word': 'முடி', 'roman': 'mudi', 'trans': 'hair', 'pos': 'NOUN', 'gender': 'NONE', 'sentence': 'முடி தலையில் உள்ளது.'},
        ]
    },
    {
        'language': 'TAMIL',
        'name': 'Greetings',
        'name_native': 'வாழ்த்துக்கள்',
        'description': 'Learn common greetings and phrases',
        'icon': 'hand-wave',
        'level': 1,
        'order': 7,
        'words': [
            {'word': 'வணக்கம்', 'roman': 'vanakkam', 'trans': 'hello/greetings', 'pos': 'OTHER', 'gender': 'NONE', 'sentence': 'வணக்கம், எப்படி இருக்கிறீர்கள்?'},
            {'word': 'நன்றி', 'roman': 'nandri', 'trans': 'thank you', 'pos': 'OTHER', 'gender': 'NONE', 'sentence': 'உங்கள் உதவிக்கு நன்றி.'},
            {'word': 'காலை வணக்கம்', 'roman': 'kaalai vanakkam', 'trans': 'good morning', 'pos': 'OTHER', 'gender': 'NONE', 'sentence': 'காலை வணக்கம், இன்று நல்ல நாள்.'},
            {'word': 'இரவு வணக்கம்', 'roman': 'iravu vanakkam', 'trans': 'good night', 'pos': 'OTHER', 'gender': 'NONE', 'sentence': 'இரவு வணக்கம், இனிய கனவுகள்.'},
            {'word': 'தயவு செய்து', 'roman': 'thayavu seithu', 'trans': 'please', 'pos': 'OTHER', 'gender': 'NONE', 'sentence': 'தயவு செய்து இங்கே உட்காருங்கள்.'},
            {'word': 'மன்னிக்கவும்', 'roman': 'mannikkavum', 'trans': 'sorry/excuse me', 'pos': 'OTHER', 'gender': 'NONE', 'sentence': 'மன்னிக்கவும், என் தவறு.'},
            {'word': 'ஆம்', 'roman': 'aam', 'trans': 'yes', 'pos': 'OTHER', 'gender': 'NONE', 'sentence': 'ஆம், புரிந்து கொண்டேன்.'},
            {'word': 'இல்லை', 'roman': 'illai', 'trans': 'no', 'pos': 'OTHER', 'gender': 'NONE', 'sentence': 'இல்லை, எனக்கு வேண்டாம்.'},
            {'word': 'சந்திப்போம்', 'roman': 'santhippom', 'trans': 'goodbye (see you)', 'pos': 'OTHER', 'gender': 'NONE', 'sentence': 'சந்திப்போம், மீண்டும் சந்திப்போம்.'},
            {'word': 'வரவேற்பு', 'roman': 'varaveerpu', 'trans': 'welcome', 'pos': 'OTHER', 'gender': 'NONE', 'sentence': 'எங்கள் வீட்டிற்கு வரவேற்பு.'},
        ]
    },
    {
        'language': 'TAMIL',
        'name': 'Actions',
        'name_native': 'செயல்கள்',
        'description': 'Learn common action words (verbs)',
        'icon': 'activity',
        'level': 2,
        'order': 8,
        'words': [
            {'word': 'சாப்பிடு', 'roman': 'saappidu', 'trans': 'to eat', 'pos': 'VERB', 'gender': 'NONE', 'sentence': 'நான் சாப்பிடுகிறேன்.'},
            {'word': 'குடி', 'roman': 'kudi', 'trans': 'to drink', 'pos': 'VERB', 'gender': 'NONE', 'sentence': 'நான் தண்ணீர் குடிக்கிறேன்.'},
            {'word': 'தூங்கு', 'roman': 'thoongu', 'trans': 'to sleep', 'pos': 'VERB', 'gender': 'NONE', 'sentence': 'குழந்தைகள் சீக்கிரம் தூங்குகிறார்கள்.'},
            {'word': 'எழு', 'roman': 'ezhu', 'trans': 'to wake up', 'pos': 'VERB', 'gender': 'NONE', 'sentence': 'நான் காலையில் சீக்கிரம் எழுகிறேன்.'},
            {'word': 'நட', 'roman': 'nada', 'trans': 'to walk', 'pos': 'VERB', 'gender': 'NONE', 'sentence': 'நாங்கள் பூங்காவில் நடக்கிறோம்.'},
            {'word': 'ஓடு', 'roman': 'odu', 'trans': 'to run', 'pos': 'VERB', 'gender': 'NONE', 'sentence': 'அவன் வேகமாக ஓடுகிறான்.'},
            {'word': 'படி', 'roman': 'padi', 'trans': 'to read/study', 'pos': 'VERB', 'gender': 'NONE', 'sentence': 'எனக்கு புத்தகங்கள் படிக்க பிடிக்கும்.'},
            {'word': 'எழுது', 'roman': 'ezhuthu', 'trans': 'to write', 'pos': 'VERB', 'gender': 'NONE', 'sentence': 'அவன் கடிதம் எழுதுகிறான்.'},
            {'word': 'விளையாடு', 'roman': 'vilaiyaadu', 'trans': 'to play', 'pos': 'VERB', 'gender': 'NONE', 'sentence': 'குழந்தைகள் வெளியே விளையாடுகிறார்கள்.'},
            {'word': 'பார்', 'roman': 'paar', 'trans': 'to see/watch', 'pos': 'VERB', 'gender': 'NONE', 'sentence': 'நாங்கள் டிவி பார்க்கிறோம்.'},
        ]
    },
]

# Tamil Grammar Topics and Rules
GRAMMAR_DATA = [
    {
        'topic': {
            'language': 'TAMIL',
            'name': 'Sentence Structure',
            'name_native': 'வாக்கிய அமைப்பு',
            'description': 'Learn basic Tamil sentence structure (Subject-Object-Verb)',
            'description_simple': 'Tamil sentences follow SOV word order: நான் (I) சோறு (rice) சாப்பிடுகிறேன் (eat)',
            'level': 1,
            'order': 1,
        },
        'rules': [
            {
                'title': 'Basic Word Order (சொல் வரிசை)',
                'explanation': 'Tamil follows Subject-Object-Verb (SOV) order. Example: நான் (I) தண்ணீர் (water) குடிக்கிறேன் (drink) = I drink water.',
                'explanation_simple': 'Tamil word order: Subject + Object + Verb',
                'formula': 'Subject + Object + Verb',
                'examples': [
                    'நான் தண்ணீர் குடிக்கிறேன்.',
                    'அவன் புத்தகம் படிக்கிறான்.',
                    'குழந்தைகள் விளையாடுகிறார்கள்.'
                ],
                'tips': 'Unlike English (SVO), Tamil places the verb at the end of the sentence.',
                'order': 1,
            }
        ]
    },
    {
        'topic': {
            'language': 'TAMIL',
            'name': 'Case Markers',
            'name_native': 'வேற்றுமை உருபுகள்',
            'description': 'Learn Tamil case markers (postpositions)',
            'description_simple': 'Tamil uses postpositions attached to nouns to show relationships',
            'level': 1,
            'order': 2,
        },
        'rules': [
            {
                'title': 'Accusative Case (-ஐ)',
                'explanation': 'The accusative marker -ஐ is added to nouns to show the direct object. Example: புத்தகம் (book) → புத்தகத்தை (the book as object)',
                'explanation_simple': 'Add -ஐ to show "the" object of an action',
                'formula': 'Noun + -ஐ',
                'examples': [
                    'நான் புத்தகத்தை படிக்கிறேன்.',
                    'அவன் பந்தை எறிகிறான்.'
                ],
                'tips': 'The accusative marker changes based on the noun ending.',
                'order': 1,
            },
            {
                'title': 'Locative Case (-இல்)',
                'explanation': 'The locative marker -இல் means "in" or "at". Example: வீடு (house) → வீட்டில் (in the house)',
                'explanation_simple': 'Add -இல் to mean "in" or "at" a place',
                'formula': 'Noun + -இல்',
                'examples': [
                    'நான் வீட்டில் இருக்கிறேன்.',
                    'பள்ளியில் படிக்கிறேன்.'
                ],
                'tips': 'Used for location, similar to "in" or "at" in English.',
                'order': 2,
            }
        ]
    },
    {
        'topic': {
            'language': 'TAMIL',
            'name': 'Pronouns',
            'name_native': 'பெயர்ச்சொற்கள்',
            'description': 'Learn personal pronouns in Tamil',
            'description_simple': 'Tamil pronouns: நான் (I), நீ (you), அவன் (he), அவள் (she)',
            'level': 1,
            'order': 3,
        },
        'rules': [
            {
                'title': 'Personal Pronouns (தனிப்பட்ட பெயர்ச்சொற்கள்)',
                'explanation': 'நான் (I), நீ (you-informal), நீங்கள் (you-formal), அவன் (he), அவள் (she), நாம்/நாங்கள் (we), அவர்கள் (they)',
                'explanation_simple': 'Tamil has different pronouns for informal and formal "you"',
                'formula': '',
                'examples': [
                    'நான் போகிறேன்.',
                    'நீ எங்கே இருக்கிறாய்?',
                    'நீங்கள் எப்படி இருக்கிறீர்கள்?'
                ],
                'tips': 'Use நீங்கள் (formal you) when speaking to elders or strangers.',
                'order': 1,
            }
        ]
    },
    {
        'topic': {
            'language': 'TAMIL',
            'name': 'Verb Conjugation',
            'name_native': 'வினை மாற்றம்',
            'description': 'Learn verb conjugation in Tamil',
            'description_simple': 'Tamil verbs change based on person, number, and gender',
            'level': 2,
            'order': 4,
        },
        'rules': [
            {
                'title': 'Present Tense (நிகழ்காலம்)',
                'explanation': 'Verb root + கிறு + person ending. Example: சாப்பிடு (eat) → சாப்பிடுகிறேன் (I eat), சாப்பிடுகிறான் (he eats)',
                'explanation_simple': 'Add -கிறு + ending to show present tense',
                'formula': 'Verb root + கிறு + ending',
                'examples': [
                    'நான் சாப்பிடுகிறேன்.',
                    'அவள் சாப்பிடுகிறாள்.',
                    'அவர்கள் சாப்பிடுகிறார்கள்.'
                ],
                'tips': 'The ending changes based on who is doing the action.',
                'order': 1,
            }
        ]
    },
    {
        'topic': {
            'language': 'TAMIL',
            'name': 'Numbers',
            'name_native': 'எண்கள்',
            'description': 'Learn to count and use numbers in sentences',
            'description_simple': 'Tamil numbers: ஒன்று, இரண்டு, மூன்று...',
            'level': 1,
            'order': 5,
        },
        'rules': [
            {
                'title': 'Cardinal Numbers 1-10 (எண்ணுதல்)',
                'explanation': 'ஒன்று, இரண்டு, மூன்று, நான்கு, ஐந்து, ஆறு, ஏழு, எட்டு, ஒன்பது, பத்து',
                'explanation_simple': 'Tamil has unique number words from 1-10',
                'formula': '',
                'examples': [
                    'என்னிடம் இரண்டு புத்தகங்கள் உள்ளன.',
                    'அறையில் ஐந்து நாற்காலிகள் உள்ளன.'
                ],
                'tips': 'Tamil uses different forms for counting objects vs. telling time.',
                'order': 1,
            }
        ]
    },
]


def seed_tamil_alphabet():
    """Seed the complete Tamil alphabet."""
    # Create Script
    script, _ = Script.objects.update_or_create(
        language='TAMIL',
        defaults={
            'name': 'Tamil',
            'name_native': 'தமிழ்',
            'description': 'The Tamil script is one of the oldest writing systems in the world. It is written left to right and has a distinctive rounded appearance.',
            'total_letters': len(VOWELS) + len(CONSONANTS),
        }
    )

    # Create Categories
    vowel_cat, _ = AlphabetCategory.objects.update_or_create(
        script=script,
        category_type='VOWEL',
        defaults={
            'name': 'Vowels',
            'name_native': 'உயிர் எழுத்துக்கள்',
            'description': 'Tamil vowels (Uyir Ezhuthukkal) - the foundation of pronunciation',
            'order': 1,
        }
    )

    consonant_cat, _ = AlphabetCategory.objects.update_or_create(
        script=script,
        category_type='CONSONANT',
        defaults={
            'name': 'Consonants',
            'name_native': 'மெய் எழுத்துக்கள்',
            'description': 'Tamil consonants (Mei Ezhuthukkal) - combined with vowels to form syllables',
            'order': 2,
        }
    )

    # Seed Vowels
    for i, v in enumerate(VOWELS):
        Letter.objects.update_or_create(
            category=vowel_cat,
            character=v['char'],
            defaults={
                'romanization': v['roman'],
                'ipa': v['ipa'],
                'example_word': v['example'],
                'example_word_romanization': v['ex_roman'],
                'example_word_translation': v['ex_trans'],
                'pronunciation_guide': f"Pronounced like '{v['roman']}' in English",
                'order': i + 1,
                'is_active': True,
            }
        )

    # Seed Consonants
    for i, c in enumerate(CONSONANTS):
        Letter.objects.update_or_create(
            category=consonant_cat,
            character=c['char'],
            defaults={
                'romanization': c['roman'],
                'ipa': c['ipa'],
                'example_word': c['example'],
                'example_word_romanization': c['ex_roman'],
                'example_word_translation': c['ex_trans'],
                'pronunciation_guide': f"Pronounced like '{c['roman']}' in English",
                'order': i + 1,
                'is_active': True,
            }
        )

    print(f"Tamil Alphabet: {len(VOWELS)} vowels, {len(CONSONANTS)} consonants")
    return len(VOWELS) + len(CONSONANTS)


def seed_tamil_vocabulary():
    """Seed all Tamil vocabulary themes and words."""
    total_themes = 0
    total_words = 0

    for theme_data in THEMES:
        words_data = theme_data.pop('words')

        theme, _ = VocabularyTheme.objects.update_or_create(
            language=theme_data['language'],
            name=theme_data['name'],
            defaults={
                'name_native': theme_data['name_native'],
                'description': theme_data['description'],
                'icon': theme_data['icon'],
                'level': theme_data['level'],
                'order': theme_data['order'],
                'is_premium': False,
                'is_active': True,
            }
        )
        total_themes += 1

        for i, w in enumerate(words_data):
            VocabularyWord.objects.update_or_create(
                theme=theme,
                word=w['word'],
                defaults={
                    'romanization': w['roman'],
                    'translation': w['trans'],
                    'part_of_speech': w['pos'],
                    'gender': w['gender'],
                    'example_sentence': w.get('sentence', ''),
                    'difficulty': 1,
                    'order': i + 1,
                }
            )
            total_words += 1

        # Restore words for next iteration
        theme_data['words'] = words_data

    print(f"Tamil Vocabulary: {total_themes} themes, {total_words} words")
    return total_words


def seed_tamil_grammar():
    """Seed Tamil grammar topics and rules."""
    total_topics = 0
    total_rules = 0

    for data in GRAMMAR_DATA:
        topic_data = data['topic']
        rules_data = data['rules']

        topic, _ = GrammarTopic.objects.update_or_create(
            language=topic_data['language'],
            name=topic_data['name'],
            defaults={
                'name_native': topic_data['name_native'],
                'description': topic_data['description'],
                'description_simple': topic_data.get('description_simple', ''),
                'level': topic_data['level'],
                'order': topic_data['order'],
                'is_active': True,
            }
        )
        total_topics += 1

        for rule_data in rules_data:
            GrammarRule.objects.update_or_create(
                topic=topic,
                title=rule_data['title'],
                defaults={
                    'explanation': rule_data['explanation'],
                    'explanation_simple': rule_data.get('explanation_simple', ''),
                    'formula': rule_data.get('formula', ''),
                    'examples': rule_data.get('examples', []),
                    'exceptions': rule_data.get('exceptions', []),
                    'tips': rule_data.get('tips', ''),
                    'order': rule_data['order'],
                }
            )
            total_rules += 1

    print(f"Tamil Grammar: {total_topics} topics, {total_rules} rules")
    return total_rules


def seed_tamil_curriculum():
    """Seed the complete Tamil curriculum."""
    print("=" * 60)
    print("SEEDING TAMIL CURRICULUM")
    print("=" * 60)
    print()

    # Seed alphabet
    print("1. Seeding Tamil alphabet...")
    letters_count = seed_tamil_alphabet()
    print(f"   ✓ Created {letters_count} letters")
    print()

    # Seed vocabulary
    print("2. Seeding Tamil vocabulary...")
    words_count = seed_tamil_vocabulary()
    print(f"   ✓ Created {words_count} words")
    print()

    # Seed grammar
    print("3. Seeding Tamil grammar...")
    rules_count = seed_tamil_grammar()
    print(f"   ✓ Created {rules_count} grammar rules")
    print()

    print("=" * 60)
    print("TAMIL CURRICULUM SEEDING COMPLETE!")
    print("=" * 60)
    print(f"Total items created:")
    print(f"  - Letters: {letters_count}")
    print(f"  - Vocabulary words: {words_count}")
    print(f"  - Grammar rules: {rules_count}")
    print(f"  - TOTAL: {letters_count + words_count + rules_count}")
    print("=" * 60)

    return {
        'letters': letters_count,
        'words': words_count,
        'rules': rules_count,
    }


if __name__ == '__main__':
    seed_tamil_curriculum()
