"""Seed Hindi vocabulary themes and words."""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.curriculum.models.vocabulary import VocabularyTheme, VocabularyWord


THEMES = [
    {
        'language': 'HINDI',
        'name': 'Family',
        'name_native': 'परिवार',
        'description': 'Learn words for family members',
        'icon': 'users',
        'level': 1,
        'order': 1,
        'words': [
            {'word': 'माँ', 'roman': 'maa', 'trans': 'mother', 'pos': 'NOUN', 'gender': 'F', 'sentence': 'मेरी माँ बहुत अच्छी हैं।'},
            {'word': 'पिता', 'roman': 'pita', 'trans': 'father', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'मेरे पिता काम पर जाते हैं।'},
            {'word': 'भाई', 'roman': 'bhai', 'trans': 'brother', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'मेरा भाई खेलता है।'},
            {'word': 'बहन', 'roman': 'bahan', 'trans': 'sister', 'pos': 'NOUN', 'gender': 'F', 'sentence': 'मेरी बहन पढ़ती है।'},
            {'word': 'दादा', 'roman': 'dada', 'trans': 'grandfather (paternal)', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'मेरे दादा कहानी सुनाते हैं।'},
            {'word': 'दादी', 'roman': 'dadi', 'trans': 'grandmother (paternal)', 'pos': 'NOUN', 'gender': 'F', 'sentence': 'मेरी दादी खाना बनाती हैं।'},
            {'word': 'नाना', 'roman': 'nana', 'trans': 'grandfather (maternal)', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'मेरे नाना बगीचे में काम करते हैं।'},
            {'word': 'नानी', 'roman': 'nani', 'trans': 'grandmother (maternal)', 'pos': 'NOUN', 'gender': 'F', 'sentence': 'मेरी नानी मिठाई बनाती हैं।'},
            {'word': 'चाचा', 'roman': 'chacha', 'trans': 'uncle (paternal)', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'मेरे चाचा डॉक्टर हैं।'},
            {'word': 'चाची', 'roman': 'chachi', 'trans': 'aunt (paternal uncle wife)', 'pos': 'NOUN', 'gender': 'F', 'sentence': 'मेरी चाची शिक्षिका हैं।'},
        ]
    },
    {
        'language': 'HINDI',
        'name': 'Colors',
        'name_native': 'रंग',
        'description': 'Learn words for colors',
        'icon': 'palette',
        'level': 1,
        'order': 2,
        'words': [
            {'word': 'लाल', 'roman': 'laal', 'trans': 'red', 'pos': 'ADJECTIVE', 'gender': 'NONE', 'sentence': 'सेब लाल है।'},
            {'word': 'नीला', 'roman': 'neela', 'trans': 'blue', 'pos': 'ADJECTIVE', 'gender': 'M', 'sentence': 'आसमान नीला है।'},
            {'word': 'पीला', 'roman': 'peela', 'trans': 'yellow', 'pos': 'ADJECTIVE', 'gender': 'M', 'sentence': 'केला पीला है।'},
            {'word': 'हरा', 'roman': 'hara', 'trans': 'green', 'pos': 'ADJECTIVE', 'gender': 'M', 'sentence': 'पत्ता हरा है।'},
            {'word': 'काला', 'roman': 'kaala', 'trans': 'black', 'pos': 'ADJECTIVE', 'gender': 'M', 'sentence': 'कौआ काला है।'},
            {'word': 'सफ़ेद', 'roman': 'safed', 'trans': 'white', 'pos': 'ADJECTIVE', 'gender': 'NONE', 'sentence': 'दूध सफ़ेद है।'},
            {'word': 'नारंगी', 'roman': 'narangi', 'trans': 'orange', 'pos': 'ADJECTIVE', 'gender': 'NONE', 'sentence': 'संतरा नारंगी है।'},
            {'word': 'गुलाबी', 'roman': 'gulaabi', 'trans': 'pink', 'pos': 'ADJECTIVE', 'gender': 'NONE', 'sentence': 'फूल गुलाबी है।'},
            {'word': 'बैंगनी', 'roman': 'baingani', 'trans': 'purple', 'pos': 'ADJECTIVE', 'gender': 'NONE', 'sentence': 'अंगूर बैंगनी हैं।'},
            {'word': 'भूरा', 'roman': 'bhura', 'trans': 'brown', 'pos': 'ADJECTIVE', 'gender': 'M', 'sentence': 'कुत्ता भूरा है।'},
        ]
    },
    {
        'language': 'HINDI',
        'name': 'Numbers',
        'name_native': 'संख्याएँ',
        'description': 'Learn numbers in Hindi',
        'icon': 'hash',
        'level': 1,
        'order': 3,
        'words': [
            {'word': 'एक', 'roman': 'ek', 'trans': 'one (1)', 'pos': 'NUMBER', 'gender': 'NONE', 'sentence': 'मेरे पास एक किताब है।'},
            {'word': 'दो', 'roman': 'do', 'trans': 'two (2)', 'pos': 'NUMBER', 'gender': 'NONE', 'sentence': 'मेरे दो हाथ हैं।'},
            {'word': 'तीन', 'roman': 'teen', 'trans': 'three (3)', 'pos': 'NUMBER', 'gender': 'NONE', 'sentence': 'तीन बिल्लियाँ हैं।'},
            {'word': 'चार', 'roman': 'chaar', 'trans': 'four (4)', 'pos': 'NUMBER', 'gender': 'NONE', 'sentence': 'कुर्सी के चार पैर हैं।'},
            {'word': 'पाँच', 'roman': 'paanch', 'trans': 'five (5)', 'pos': 'NUMBER', 'gender': 'NONE', 'sentence': 'हाथ में पाँच उंगलियाँ हैं।'},
            {'word': 'छह', 'roman': 'chhah', 'trans': 'six (6)', 'pos': 'NUMBER', 'gender': 'NONE', 'sentence': 'छह दिन बीत गए।'},
            {'word': 'सात', 'roman': 'saat', 'trans': 'seven (7)', 'pos': 'NUMBER', 'gender': 'NONE', 'sentence': 'सप्ताह में सात दिन होते हैं।'},
            {'word': 'आठ', 'roman': 'aath', 'trans': 'eight (8)', 'pos': 'NUMBER', 'gender': 'NONE', 'sentence': 'मकड़ी के आठ पैर होते हैं।'},
            {'word': 'नौ', 'roman': 'nau', 'trans': 'nine (9)', 'pos': 'NUMBER', 'gender': 'NONE', 'sentence': 'नौ ग्रह हैं।'},
            {'word': 'दस', 'roman': 'das', 'trans': 'ten (10)', 'pos': 'NUMBER', 'gender': 'NONE', 'sentence': 'दस रुपये दो।'},
        ]
    },
    {
        'language': 'HINDI',
        'name': 'Animals',
        'name_native': 'जानवर',
        'description': 'Learn words for animals',
        'icon': 'paw-print',
        'level': 1,
        'order': 4,
        'words': [
            {'word': 'कुत्ता', 'roman': 'kutta', 'trans': 'dog', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'कुत्ता भौंकता है।'},
            {'word': 'बिल्ली', 'roman': 'billi', 'trans': 'cat', 'pos': 'NOUN', 'gender': 'F', 'sentence': 'बिल्ली म्याऊं करती है।'},
            {'word': 'गाय', 'roman': 'gaay', 'trans': 'cow', 'pos': 'NOUN', 'gender': 'F', 'sentence': 'गाय दूध देती है।'},
            {'word': 'घोड़ा', 'roman': 'ghoda', 'trans': 'horse', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'घोड़ा तेज़ दौड़ता है।'},
            {'word': 'हाथी', 'roman': 'haathi', 'trans': 'elephant', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'हाथी बड़ा होता है।'},
            {'word': 'शेर', 'roman': 'sher', 'trans': 'lion', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'शेर जंगल का राजा है।'},
            {'word': 'बंदर', 'roman': 'bandar', 'trans': 'monkey', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'बंदर पेड़ पर चढ़ता है।'},
            {'word': 'चिड़िया', 'roman': 'chidiya', 'trans': 'bird', 'pos': 'NOUN', 'gender': 'F', 'sentence': 'चिड़िया उड़ती है।'},
            {'word': 'मछली', 'roman': 'machhli', 'trans': 'fish', 'pos': 'NOUN', 'gender': 'F', 'sentence': 'मछली पानी में तैरती है।'},
            {'word': 'खरगोश', 'roman': 'khargosh', 'trans': 'rabbit', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'खरगोश गाजर खाता है।'},
        ]
    },
    {
        'language': 'HINDI',
        'name': 'Food',
        'name_native': 'खाना',
        'description': 'Learn words for food items',
        'icon': 'utensils',
        'level': 1,
        'order': 5,
        'words': [
            {'word': 'रोटी', 'roman': 'roti', 'trans': 'bread/flatbread', 'pos': 'NOUN', 'gender': 'F', 'sentence': 'माँ रोटी बनाती हैं।'},
            {'word': 'चावल', 'roman': 'chaawal', 'trans': 'rice', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'चावल सफ़ेद होता है।'},
            {'word': 'दाल', 'roman': 'daal', 'trans': 'lentils', 'pos': 'NOUN', 'gender': 'F', 'sentence': 'दाल में प्रोटीन होता है।'},
            {'word': 'सब्ज़ी', 'roman': 'sabzi', 'trans': 'vegetable', 'pos': 'NOUN', 'gender': 'F', 'sentence': 'सब्ज़ी स्वादिष्ट है।'},
            {'word': 'दूध', 'roman': 'doodh', 'trans': 'milk', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'दूध पीना अच्छा है।'},
            {'word': 'पानी', 'roman': 'paani', 'trans': 'water', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'पानी ज़रूरी है।'},
            {'word': 'फल', 'roman': 'phal', 'trans': 'fruit', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'फल खाना चाहिए।'},
            {'word': 'मिठाई', 'roman': 'mithai', 'trans': 'sweets', 'pos': 'NOUN', 'gender': 'F', 'sentence': 'मिठाई मीठी होती है।'},
            {'word': 'आम', 'roman': 'aam', 'trans': 'mango', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'आम फलों का राजा है।'},
            {'word': 'सेब', 'roman': 'seb', 'trans': 'apple', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'सेब लाल होता है।'},
        ]
    },
    {
        'language': 'HINDI',
        'name': 'Body Parts',
        'name_native': 'शरीर के अंग',
        'description': 'Learn words for body parts',
        'icon': 'hand',
        'level': 1,
        'order': 6,
        'words': [
            {'word': 'सिर', 'roman': 'sir', 'trans': 'head', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'सिर में दिमाग होता है।'},
            {'word': 'आँख', 'roman': 'aankh', 'trans': 'eye', 'pos': 'NOUN', 'gender': 'F', 'sentence': 'आँखों से देखते हैं।'},
            {'word': 'कान', 'roman': 'kaan', 'trans': 'ear', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'कानों से सुनते हैं।'},
            {'word': 'नाक', 'roman': 'naak', 'trans': 'nose', 'pos': 'NOUN', 'gender': 'F', 'sentence': 'नाक से सूंघते हैं।'},
            {'word': 'मुँह', 'roman': 'munh', 'trans': 'mouth', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'मुँह से खाते हैं।'},
            {'word': 'हाथ', 'roman': 'haath', 'trans': 'hand', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'हाथ से काम करते हैं।'},
            {'word': 'पैर', 'roman': 'pair', 'trans': 'foot/leg', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'पैरों से चलते हैं।'},
            {'word': 'उंगली', 'roman': 'ungli', 'trans': 'finger', 'pos': 'NOUN', 'gender': 'F', 'sentence': 'हाथ में पाँच उंगलियाँ होती हैं।'},
            {'word': 'दाँत', 'roman': 'daant', 'trans': 'tooth', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'दाँतों से चबाते हैं।'},
            {'word': 'बाल', 'roman': 'baal', 'trans': 'hair', 'pos': 'NOUN', 'gender': 'M', 'sentence': 'बाल सिर पर होते हैं।'},
        ]
    },
    {
        'language': 'HINDI',
        'name': 'Greetings',
        'name_native': 'अभिवादन',
        'description': 'Learn common greetings and phrases',
        'icon': 'hand-wave',
        'level': 1,
        'order': 7,
        'words': [
            {'word': 'नमस्ते', 'roman': 'namaste', 'trans': 'hello/greetings', 'pos': 'OTHER', 'gender': 'NONE', 'sentence': 'नमस्ते, आप कैसे हैं?'},
            {'word': 'धन्यवाद', 'roman': 'dhanyavaad', 'trans': 'thank you', 'pos': 'OTHER', 'gender': 'NONE', 'sentence': 'आपकी मदद के लिए धन्यवाद।'},
            {'word': 'शुभ प्रभात', 'roman': 'shubh prabhaat', 'trans': 'good morning', 'pos': 'OTHER', 'gender': 'NONE', 'sentence': 'शुभ प्रभात, आज मौसम अच्छा है।'},
            {'word': 'शुभ रात्रि', 'roman': 'shubh ratri', 'trans': 'good night', 'pos': 'OTHER', 'gender': 'NONE', 'sentence': 'शुभ रात्रि, अच्छे सपने देखो।'},
            {'word': 'कृपया', 'roman': 'kripaya', 'trans': 'please', 'pos': 'OTHER', 'gender': 'NONE', 'sentence': 'कृपया यहाँ बैठिए।'},
            {'word': 'माफ़ कीजिए', 'roman': 'maaf kijiye', 'trans': 'sorry/excuse me', 'pos': 'OTHER', 'gender': 'NONE', 'sentence': 'माफ़ कीजिए, मुझसे गलती हो गई।'},
            {'word': 'हाँ', 'roman': 'haan', 'trans': 'yes', 'pos': 'OTHER', 'gender': 'NONE', 'sentence': 'हाँ, मैं समझ गया।'},
            {'word': 'नहीं', 'roman': 'nahin', 'trans': 'no', 'pos': 'OTHER', 'gender': 'NONE', 'sentence': 'नहीं, मुझे नहीं चाहिए।'},
            {'word': 'अलविदा', 'roman': 'alvida', 'trans': 'goodbye', 'pos': 'OTHER', 'gender': 'NONE', 'sentence': 'अलविदा, फिर मिलेंगे।'},
            {'word': 'स्वागत है', 'roman': 'swagat hai', 'trans': 'welcome', 'pos': 'OTHER', 'gender': 'NONE', 'sentence': 'हमारे घर में आपका स्वागत है।'},
        ]
    },
    {
        'language': 'HINDI',
        'name': 'Actions',
        'name_native': 'क्रियाएँ',
        'description': 'Learn common action words (verbs)',
        'icon': 'activity',
        'level': 2,
        'order': 8,
        'words': [
            {'word': 'खाना', 'roman': 'khaana', 'trans': 'to eat', 'pos': 'VERB', 'gender': 'NONE', 'sentence': 'मैं खाना खाता हूँ।'},
            {'word': 'पीना', 'roman': 'peena', 'trans': 'to drink', 'pos': 'VERB', 'gender': 'NONE', 'sentence': 'मैं पानी पीता हूँ।'},
            {'word': 'सोना', 'roman': 'sona', 'trans': 'to sleep', 'pos': 'VERB', 'gender': 'NONE', 'sentence': 'बच्चे जल्दी सोते हैं।'},
            {'word': 'जागना', 'roman': 'jaagna', 'trans': 'to wake up', 'pos': 'VERB', 'gender': 'NONE', 'sentence': 'मैं सुबह जल्दी जागता हूँ।'},
            {'word': 'चलना', 'roman': 'chalna', 'trans': 'to walk', 'pos': 'VERB', 'gender': 'NONE', 'sentence': 'हम पार्क में चलते हैं।'},
            {'word': 'दौड़ना', 'roman': 'daudna', 'trans': 'to run', 'pos': 'VERB', 'gender': 'NONE', 'sentence': 'वह तेज़ दौड़ता है।'},
            {'word': 'पढ़ना', 'roman': 'padhna', 'trans': 'to read', 'pos': 'VERB', 'gender': 'NONE', 'sentence': 'मुझे किताबें पढ़ना पसंद है।'},
            {'word': 'लिखना', 'roman': 'likhna', 'trans': 'to write', 'pos': 'VERB', 'gender': 'NONE', 'sentence': 'वह पत्र लिखता है।'},
            {'word': 'खेलना', 'roman': 'khelna', 'trans': 'to play', 'pos': 'VERB', 'gender': 'NONE', 'sentence': 'बच्चे बाहर खेलते हैं।'},
            {'word': 'देखना', 'roman': 'dekhna', 'trans': 'to see/watch', 'pos': 'VERB', 'gender': 'NONE', 'sentence': 'हम टीवी देखते हैं।'},
        ]
    },
]


def seed_vocabulary():
    """Seed all vocabulary themes and words."""
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

    print(f"Vocabulary: {total_themes} themes, {total_words} words")
    return total_words


if __name__ == '__main__':
    seed_vocabulary()
