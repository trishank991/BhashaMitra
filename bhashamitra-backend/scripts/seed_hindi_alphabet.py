"""Seed Hindi Devanagari alphabet data."""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.curriculum.models.script import Script, AlphabetCategory, Letter, Matra


# Hindi Vowels (Swar)
VOWELS = [
    {'char': 'अ', 'roman': 'a', 'ipa': 'ə', 'example': 'अनार', 'ex_roman': 'anaar', 'ex_trans': 'pomegranate'},
    {'char': 'आ', 'roman': 'aa', 'ipa': 'aː', 'example': 'आम', 'ex_roman': 'aam', 'ex_trans': 'mango'},
    {'char': 'इ', 'roman': 'i', 'ipa': 'ɪ', 'example': 'इमली', 'ex_roman': 'imli', 'ex_trans': 'tamarind'},
    {'char': 'ई', 'roman': 'ee', 'ipa': 'iː', 'example': 'ईख', 'ex_roman': 'eekh', 'ex_trans': 'sugarcane'},
    {'char': 'उ', 'roman': 'u', 'ipa': 'ʊ', 'example': 'उल्लू', 'ex_roman': 'ullu', 'ex_trans': 'owl'},
    {'char': 'ऊ', 'roman': 'oo', 'ipa': 'uː', 'example': 'ऊन', 'ex_roman': 'oon', 'ex_trans': 'wool'},
    {'char': 'ऋ', 'roman': 'ri', 'ipa': 'ɾɪ', 'example': 'ऋषि', 'ex_roman': 'rishi', 'ex_trans': 'sage'},
    {'char': 'ए', 'roman': 'e', 'ipa': 'eː', 'example': 'एक', 'ex_roman': 'ek', 'ex_trans': 'one'},
    {'char': 'ऐ', 'roman': 'ai', 'ipa': 'ɛː', 'example': 'ऐनक', 'ex_roman': 'ainak', 'ex_trans': 'glasses'},
    {'char': 'ओ', 'roman': 'o', 'ipa': 'oː', 'example': 'ओखली', 'ex_roman': 'okhli', 'ex_trans': 'mortar'},
    {'char': 'औ', 'roman': 'au', 'ipa': 'ɔː', 'example': 'औरत', 'ex_roman': 'aurat', 'ex_trans': 'woman'},
    {'char': 'अं', 'roman': 'am', 'ipa': 'əm', 'example': 'अंगूर', 'ex_roman': 'angoor', 'ex_trans': 'grapes'},
    {'char': 'अः', 'roman': 'ah', 'ipa': 'əh', 'example': 'दुःख', 'ex_roman': 'dukh', 'ex_trans': 'sorrow'},
]

# Hindi Consonants (Vyanjan)
CONSONANTS = [
    # Ka-varga (Guttural)
    {'char': 'क', 'roman': 'ka', 'ipa': 'kə', 'example': 'कमल', 'ex_roman': 'kamal', 'ex_trans': 'lotus'},
    {'char': 'ख', 'roman': 'kha', 'ipa': 'kʰə', 'example': 'खरगोश', 'ex_roman': 'khargosh', 'ex_trans': 'rabbit'},
    {'char': 'ग', 'roman': 'ga', 'ipa': 'gə', 'example': 'गाय', 'ex_roman': 'gaay', 'ex_trans': 'cow'},
    {'char': 'घ', 'roman': 'gha', 'ipa': 'gʱə', 'example': 'घर', 'ex_roman': 'ghar', 'ex_trans': 'house'},
    {'char': 'ङ', 'roman': 'nga', 'ipa': 'ŋə', 'example': 'रंग', 'ex_roman': 'rang', 'ex_trans': 'color'},
    # Cha-varga (Palatal)
    {'char': 'च', 'roman': 'cha', 'ipa': 'tʃə', 'example': 'चम्मच', 'ex_roman': 'chammach', 'ex_trans': 'spoon'},
    {'char': 'छ', 'roman': 'chha', 'ipa': 'tʃʰə', 'example': 'छाता', 'ex_roman': 'chhaata', 'ex_trans': 'umbrella'},
    {'char': 'ज', 'roman': 'ja', 'ipa': 'dʒə', 'example': 'जहाज', 'ex_roman': 'jahaaz', 'ex_trans': 'ship'},
    {'char': 'झ', 'roman': 'jha', 'ipa': 'dʒʱə', 'example': 'झंडा', 'ex_roman': 'jhanda', 'ex_trans': 'flag'},
    {'char': 'ञ', 'roman': 'nya', 'ipa': 'ɲə', 'example': 'ज्ञान', 'ex_roman': 'gyaan', 'ex_trans': 'knowledge'},
    # Ta-varga (Retroflex)
    {'char': 'ट', 'roman': 'ta', 'ipa': 'ʈə', 'example': 'टमाटर', 'ex_roman': 'tamaatar', 'ex_trans': 'tomato'},
    {'char': 'ठ', 'roman': 'tha', 'ipa': 'ʈʰə', 'example': 'ठंड', 'ex_roman': 'thand', 'ex_trans': 'cold'},
    {'char': 'ड', 'roman': 'da', 'ipa': 'ɖə', 'example': 'डमरू', 'ex_roman': 'damru', 'ex_trans': 'drum'},
    {'char': 'ढ', 'roman': 'dha', 'ipa': 'ɖʱə', 'example': 'ढोल', 'ex_roman': 'dhol', 'ex_trans': 'drum'},
    {'char': 'ण', 'roman': 'na', 'ipa': 'ɳə', 'example': 'बाण', 'ex_roman': 'baan', 'ex_trans': 'arrow'},
    # Ta-varga (Dental)
    {'char': 'त', 'roman': 'ta', 'ipa': 't̪ə', 'example': 'तारा', 'ex_roman': 'taara', 'ex_trans': 'star'},
    {'char': 'थ', 'roman': 'tha', 'ipa': 't̪ʰə', 'example': 'थाली', 'ex_roman': 'thaali', 'ex_trans': 'plate'},
    {'char': 'द', 'roman': 'da', 'ipa': 'd̪ə', 'example': 'दवाई', 'ex_roman': 'dawai', 'ex_trans': 'medicine'},
    {'char': 'ध', 'roman': 'dha', 'ipa': 'd̪ʱə', 'example': 'धनुष', 'ex_roman': 'dhanush', 'ex_trans': 'bow'},
    {'char': 'न', 'roman': 'na', 'ipa': 'nə', 'example': 'नल', 'ex_roman': 'nal', 'ex_trans': 'tap'},
    # Pa-varga (Labial)
    {'char': 'प', 'roman': 'pa', 'ipa': 'pə', 'example': 'पतंग', 'ex_roman': 'patang', 'ex_trans': 'kite'},
    {'char': 'फ', 'roman': 'pha', 'ipa': 'pʰə', 'example': 'फल', 'ex_roman': 'phal', 'ex_trans': 'fruit'},
    {'char': 'ब', 'roman': 'ba', 'ipa': 'bə', 'example': 'बकरी', 'ex_roman': 'bakri', 'ex_trans': 'goat'},
    {'char': 'भ', 'roman': 'bha', 'ipa': 'bʱə', 'example': 'भालू', 'ex_roman': 'bhalu', 'ex_trans': 'bear'},
    {'char': 'म', 'roman': 'ma', 'ipa': 'mə', 'example': 'मछली', 'ex_roman': 'machhli', 'ex_trans': 'fish'},
    # Antahstha (Semi-vowels)
    {'char': 'य', 'roman': 'ya', 'ipa': 'jə', 'example': 'यात्रा', 'ex_roman': 'yatra', 'ex_trans': 'journey'},
    {'char': 'र', 'roman': 'ra', 'ipa': 'ɾə', 'example': 'राजा', 'ex_roman': 'raja', 'ex_trans': 'king'},
    {'char': 'ल', 'roman': 'la', 'ipa': 'lə', 'example': 'लड्डू', 'ex_roman': 'laddu', 'ex_trans': 'sweet'},
    {'char': 'व', 'roman': 'va', 'ipa': 'ʋə', 'example': 'वन', 'ex_roman': 'van', 'ex_trans': 'forest'},
    # Ushma (Sibilants/Fricatives)
    {'char': 'श', 'roman': 'sha', 'ipa': 'ʃə', 'example': 'शेर', 'ex_roman': 'sher', 'ex_trans': 'lion'},
    {'char': 'ष', 'roman': 'sha', 'ipa': 'ʂə', 'example': 'षट्कोण', 'ex_roman': 'shatkon', 'ex_trans': 'hexagon'},
    {'char': 'स', 'roman': 'sa', 'ipa': 'sə', 'example': 'सेब', 'ex_roman': 'seb', 'ex_trans': 'apple'},
    {'char': 'ह', 'roman': 'ha', 'ipa': 'ɦə', 'example': 'हाथी', 'ex_roman': 'haathi', 'ex_trans': 'elephant'},
    # Additional consonants
    {'char': 'क्ष', 'roman': 'ksha', 'ipa': 'kʂə', 'example': 'क्षत्रिय', 'ex_roman': 'kshatriya', 'ex_trans': 'warrior'},
    {'char': 'त्र', 'roman': 'tra', 'ipa': 't̪ɾə', 'example': 'त्रिशूल', 'ex_roman': 'trishul', 'ex_trans': 'trident'},
    {'char': 'ज्ञ', 'roman': 'gya', 'ipa': 'gɲə', 'example': 'ज्ञान', 'ex_roman': 'gyaan', 'ex_trans': 'knowledge'},
]

# Hindi Matras (Vowel marks)
MATRAS = [
    {'symbol': 'ा', 'name': 'aa matra', 'example_ka': 'का'},
    {'symbol': 'ि', 'name': 'i matra', 'example_ka': 'कि'},
    {'symbol': 'ी', 'name': 'ee matra', 'example_ka': 'की'},
    {'symbol': 'ु', 'name': 'u matra', 'example_ka': 'कु'},
    {'symbol': 'ू', 'name': 'oo matra', 'example_ka': 'कू'},
    {'symbol': 'ृ', 'name': 'ri matra', 'example_ka': 'कृ'},
    {'symbol': 'े', 'name': 'e matra', 'example_ka': 'के'},
    {'symbol': 'ै', 'name': 'ai matra', 'example_ka': 'कै'},
    {'symbol': 'ो', 'name': 'o matra', 'example_ka': 'को'},
    {'symbol': 'ौ', 'name': 'au matra', 'example_ka': 'कौ'},
    {'symbol': 'ं', 'name': 'anusvara', 'example_ka': 'कं'},
    {'symbol': 'ः', 'name': 'visarga', 'example_ka': 'कः'},
]


def seed_hindi_alphabet():
    """Seed the complete Hindi Devanagari alphabet."""
    # Create Script
    script, _ = Script.objects.update_or_create(
        language='HINDI',
        defaults={
            'name': 'Devanagari',
            'name_native': 'देवनागरी',
            'description': 'The Devanagari script is used for Hindi and other Indian languages. It is written left to right and has a distinctive horizontal line running along the top of the letters.',
            'total_letters': len(VOWELS) + len(CONSONANTS),
        }
    )

    # Create Categories
    vowel_cat, _ = AlphabetCategory.objects.update_or_create(
        script=script,
        category_type='VOWEL',
        defaults={
            'name': 'Vowels',
            'name_native': 'स्वर',
            'description': 'Hindi vowels (Swar) - the foundation of pronunciation',
            'order': 1,
        }
    )

    consonant_cat, _ = AlphabetCategory.objects.update_or_create(
        script=script,
        category_type='CONSONANT',
        defaults={
            'name': 'Consonants',
            'name_native': 'व्यंजन',
            'description': 'Hindi consonants (Vyanjan) - combined with vowels to form syllables',
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

    # Seed Matras
    for i, m in enumerate(MATRAS):
        Matra.objects.update_or_create(
            script=script,
            symbol=m['symbol'],
            defaults={
                'name': m['name'],
                'example_with_ka': m['example_ka'],
                'order': i + 1,
            }
        )

    print(f"Hindi Alphabet: {len(VOWELS)} vowels, {len(CONSONANTS)} consonants, {len(MATRAS)} matras")
    return len(VOWELS) + len(CONSONANTS) + len(MATRAS)


if __name__ == '__main__':
    seed_hindi_alphabet()
