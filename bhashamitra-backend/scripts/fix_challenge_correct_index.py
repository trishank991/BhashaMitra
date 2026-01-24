# BhashaMitra - Fix Challenges Missing correct_index
# ================================================
#
# This script fixes existing challenges where questions are missing the correct_index field.
# Run this on your production server or locally connected to production database.
#
# Usage:
#   1. Copy this file to your backend directory
#   2. Run: python scripts/fix_challenge_correct_index.py
#   Or run specific functions from Django shell

"""
Fix challenges with missing correct_index in questions.

This script:
1. Identifies all challenges where questions are missing correct_index
2. For vocabulary questions, matches the English word to find the correct Hindi answer
3. Updates the challenges with proper correct_index values
4. Generates a report of what was fixed
"""

import os
import sys
import json
import django
import logging
from datetime import datetime

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

try:
    django.setup()
except:
    # Try production settings
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.prod'
    django.setup()

from django.db import transaction

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================
# VOCABULARY MAPPING
# ============================================
# This maps English words to their correct Hindi translations
# Used to determine correct_index when it's missing

HINDI_VOCABULARY = {
    # Animals
    'bird': 'चिड़िया',
    'cat': 'बिल्ली',
    'dog': 'कुत्ता',
    'cow': 'गाय',
    'horse': 'घोड़ा',
    'elephant': 'हाथी',
    'lion': 'शेर',
    'tiger': 'बाघ',
    'monkey': 'बंदर',
    'crow': 'कौआ',
    'fish': 'मछली',
    'snake': 'साँप',
    'rabbit': 'खरगोश',
    'bear': 'भालू',
    'deer': 'हिरण',
    'goat': 'बकरी',
    'sheep': 'भेड़',
    'pig': 'सुअर',
    'rat': 'चूहा',
    'frog': 'मेंढक',

    # Family
    'mother': 'माँ',
    'father': 'पिता',
    'brother': 'भाई',
    'sister': 'बहन',
    'grandfather': 'दादा',
    'grandmother': 'दादी',
    'uncle': 'चाचा',
    'aunt': 'चाची',
    'son': 'बेटा',
    'daughter': 'बेटी',
    'husband': 'पति',
    'wife': 'पत्नी',
    'child': 'बच्चा',
    'baby': 'शिशु',
    'family': 'परिवार',

    # Body Parts
    'eye': 'आँख',
    'eyes': 'आँखें',
    'ear': 'कान',
    'ears': 'कान',
    'nose': 'नाक',
    'mouth': 'मुँह',
    'hand': 'हाथ',
    'hands': 'हाथ',
    'leg': 'पैर',
    'foot': 'पैर',
    'head': 'सिर',
    'hair': 'बाल',
    'face': 'चेहरा',
    'teeth': 'दाँत',
    'tongue': 'जीभ',
    'finger': 'उंगली',
    'heart': 'दिल',
    'stomach': 'पेट',

    # Colors
    'red': 'लाल',
    'blue': 'नीला',
    'green': 'हरा',
    'yellow': 'पीला',
    'white': 'सफेद',
    'black': 'काला',
    'orange': 'नारंगी',
    'pink': 'गुलाबी',
    'purple': 'बैंगनी',
    'brown': 'भूरा',
    'grey': 'धूसर',
    'gray': 'धूसर',

    # Numbers
    'one': 'एक',
    'two': 'दो',
    'three': 'तीन',
    'four': 'चार',
    'five': 'पाँच',
    'six': 'छह',
    'seven': 'सात',
    'eight': 'आठ',
    'nine': 'नौ',
    'ten': 'दस',
    'zero': 'शून्य',
    'hundred': 'सौ',
    'thousand': 'हज़ार',

    # Food
    'water': 'पानी',
    'milk': 'दूध',
    'rice': 'चावल',
    'bread': 'रोटी',
    'apple': 'सेब',
    'banana': 'केला',
    'mango': 'आम',
    'orange': 'संतरा',
    'food': 'खाना',
    'fruit': 'फल',
    'vegetable': 'सब्ज़ी',
    'sugar': 'चीनी',
    'salt': 'नमक',
    'tea': 'चाय',
    'coffee': 'कॉफ़ी',

    # Common Objects
    'house': 'घर',
    'home': 'घर',
    'door': 'दरवाज़ा',
    'window': 'खिड़की',
    'table': 'मेज़',
    'chair': 'कुर्सी',
    'bed': 'बिस्तर',
    'book': 'किताब',
    'pen': 'कलम',
    'paper': 'कागज़',
    'phone': 'फ़ोन',
    'computer': 'कंप्यूटर',
    'car': 'गाड़ी',
    'tree': 'पेड़',
    'flower': 'फूल',
    'sun': 'सूरज',
    'moon': 'चाँद',
    'star': 'तारा',
    'sky': 'आकाश',
    'rain': 'बारिश',
    'clock': 'घड़ी',
    'watch': 'घड़ी',
    'key': 'चाबी',
    'bag': 'बैग',
    'shoe': 'जूता',
    'shirt': 'कमीज़',

    # Greetings & Phrases
    'hello': 'नमस्ते',
    'goodbye': 'अलविदा',
    'good morning': 'शुभ प्रभात',
    'good night': 'शुभ रात्रि',
    'thank you': 'धन्यवाद',
    'thanks': 'धन्यवाद',
    'please': 'कृपया',
    'sorry': 'माफ़ कीजिए',
    'yes': 'हाँ',
    'no': 'नहीं',
    'welcome': 'स्वागत',

    # Actions/Verbs
    'eat': 'खाना',
    'drink': 'पीना',
    'sleep': 'सोना',
    'walk': 'चलना',
    'run': 'दौड़ना',
    'read': 'पढ़ना',
    'write': 'लिखना',
    'speak': 'बोलना',
    'listen': 'सुनना',
    'see': 'देखना',
    'come': 'आना',
    'go': 'जाना',
    'sit': 'बैठना',
    'stand': 'खड़ा होना',
    'play': 'खेलना',
    'sing': 'गाना',
    'dance': 'नाचना',
    'love': 'प्यार',
    'like': 'पसंद',

    # Adjectives
    'big': 'बड़ा',
    'small': 'छोटा',
    'good': 'अच्छा',
    'bad': 'बुरा',
    'hot': 'गर्म',
    'cold': 'ठंडा',
    'new': 'नया',
    'old': 'पुराना',
    'happy': 'खुश',
    'sad': 'दुखी',
    'beautiful': 'सुंदर',
    'fast': 'तेज़',
    'slow': 'धीमा',
    'easy': 'आसान',
    'hard': 'कठिन',
    'difficult': 'मुश्किल',

    # Time
    'today': 'आज',
    'tomorrow': 'कल',
    'yesterday': 'कल',
    'day': 'दिन',
    'night': 'रात',
    'morning': 'सुबह',
    'evening': 'शाम',
    'week': 'हफ़्ता',
    'month': 'महीना',
    'year': 'साल',
    'time': 'समय',

    # Places
    'school': 'स्कूल',
    'market': 'बाज़ार',
    'hospital': 'अस्पताल',
    'temple': 'मंदिर',
    'city': 'शहर',
    'village': 'गाँव',
    'country': 'देश',
    'road': 'सड़क',
    'garden': 'बगीचा',

    # Emotions
    'fear': 'डर',
    'anger': 'गुस्सा',
    'joy': 'खुशी',
    'peace': 'शांति',
    'hope': 'आशा',

    # Nature
    'river': 'नदी',
    'mountain': 'पहाड़',
    'sea': 'समुद्र',
    'forest': 'जंगल',
    'earth': 'धरती',
    'fire': 'आग',
    'air': 'हवा',
    'wind': 'हवा',
}


def extract_english_word(question_text):
    """
    Extract the English word from question text.
    Handles formats like:
    - "How do you say 'bird'?"
    - "What is 'cat' in Hindi?"
    - "Translate 'dog'"
    """
    import re

    # Try to find word in single quotes
    match = re.search(r"'([^']+)'", question_text)
    if match:
        return match.group(1).lower().strip()

    # Try to find word in double quotes
    match = re.search(r'"([^"]+)"', question_text)
    if match:
        return match.group(1).lower().strip()

    return None


def find_correct_index(question_text, options, vocabulary=HINDI_VOCABULARY):
    """
    Given a question and options, find the correct answer index.

    Args:
        question_text: The question string (e.g., "How do you say 'bird'?")
        options: List of Hindi options (e.g., ["दादा", "सेब", "बिल्ली", "चिड़िया"])
        vocabulary: Dictionary mapping English words to Hindi translations

    Returns:
        int: Index of correct answer, or None if not found
    """
    english_word = extract_english_word(question_text)

    if not english_word:
        logger.warning(f"Could not extract English word from: {question_text}")
        return None

    correct_hindi = vocabulary.get(english_word)

    if not correct_hindi:
        logger.warning(f"No Hindi translation found for: {english_word}")
        return None

    # Find the index of the correct answer in options
    for i, option in enumerate(options):
        # Clean up the option text for comparison
        option_clean = option.strip()
        if option_clean == correct_hindi:
            return i

    # Try partial matching (in case of slight variations)
    for i, option in enumerate(options):
        if correct_hindi in option or option in correct_hindi:
            logger.info(f"Partial match found for '{english_word}': {option} (index {i})")
            return i

    logger.warning(f"Correct answer '{correct_hindi}' not found in options: {options}")
    return None


def analyze_challenges():
    """
    Analyze all challenges and report which ones have missing correct_index.
    """
    from apps.challenges.models import Challenge

    challenges = Challenge.objects.all()

    report = {
        'total': 0,
        'healthy': 0,
        'broken': 0,
        'broken_challenges': []
    }

    for challenge in challenges:
        report['total'] += 1
        questions = challenge.questions or []

        has_issues = False
        missing_count = 0

        for i, q in enumerate(questions):
            if q.get('correct_index') is None:
                has_issues = True
                missing_count += 1

        if has_issues:
            report['broken'] += 1
            report['broken_challenges'].append({
                'code': challenge.code,
                'title': challenge.title,
                'question_count': len(questions),
                'missing_correct_index': missing_count,
            })
        else:
            report['healthy'] += 1

    return report


def fix_challenge(challenge_code, dry_run=True):
    """
    Fix a specific challenge by adding correct_index to questions.

    Args:
        challenge_code: The challenge code (e.g., 'PPG2')
        dry_run: If True, only report what would be changed without saving

    Returns:
        dict: Report of what was fixed
    """
    from apps.challenges.models import Challenge

    try:
        challenge = Challenge.objects.get(code=challenge_code)
    except Challenge.DoesNotExist:
        logger.error(f"Challenge {challenge_code} not found")
        return {'error': f'Challenge {challenge_code} not found'}

    questions = challenge.questions or []
    fixed_count = 0
    results = []

    for i, q in enumerate(questions):
        question_text = q.get('question', '')
        options = q.get('options', [])
        current_correct_index = q.get('correct_index')

        result = {
            'question_index': i,
            'question': question_text[:50] + '...' if len(question_text) > 50 else question_text,
            'had_correct_index': current_correct_index is not None,
            'old_correct_index': current_correct_index,
            'new_correct_index': None,
            'fixed': False,
        }

        if current_correct_index is None:
            # Try to determine the correct index
            new_correct_index = find_correct_index(question_text, options)

            if new_correct_index is not None:
                result['new_correct_index'] = new_correct_index
                result['fixed'] = True

                if not dry_run:
                    q['correct_index'] = new_correct_index

                fixed_count += 1
                logger.info(f"Fixed Q{i}: '{question_text[:30]}...' -> correct_index={new_correct_index}")
            else:
                logger.warning(f"Could not determine correct_index for Q{i}: '{question_text[:30]}...'")

        results.append(result)

    if not dry_run and fixed_count > 0:
        challenge.questions = questions
        challenge.save()
        logger.info(f"Saved challenge {challenge_code} with {fixed_count} fixes")

    return {
        'challenge_code': challenge_code,
        'challenge_title': challenge.title,
        'total_questions': len(questions),
        'fixed_count': fixed_count,
        'dry_run': dry_run,
        'details': results,
    }


@transaction.atomic
def fix_all_challenges(dry_run=True):
    """
    Fix all challenges that have missing correct_index.

    Args:
        dry_run: If True, only report what would be changed without saving

    Returns:
        dict: Summary report
    """
    from apps.challenges.models import Challenge

    challenges = Challenge.objects.all()

    summary = {
        'timestamp': datetime.now().isoformat(),
        'dry_run': dry_run,
        'total_challenges': 0,
        'challenges_fixed': 0,
        'questions_fixed': 0,
        'challenges_skipped': 0,
        'details': [],
    }

    for challenge in challenges:
        summary['total_challenges'] += 1

        # Check if this challenge needs fixing
        questions = challenge.questions or []
        needs_fix = any(q.get('correct_index') is None for q in questions)

        if not needs_fix:
            summary['challenges_skipped'] += 1
            continue

        # Fix this challenge
        result = fix_challenge(challenge.code, dry_run=dry_run)

        if result.get('fixed_count', 0) > 0:
            summary['challenges_fixed'] += 1
            summary['questions_fixed'] += result['fixed_count']

        summary['details'].append(result)

    return summary


def print_report(report):
    """Pretty print a report."""
    print("\n" + "="*60)
    print("CHALLENGE FIX REPORT")
    print("="*60)
    print(f"Timestamp: {report.get('timestamp', 'N/A')}")
    print(f"Dry Run: {report.get('dry_run', True)}")
    print(f"\nTotal Challenges: {report.get('total_challenges', 0)}")
    print(f"Challenges Fixed: {report.get('challenges_fixed', 0)}")
    print(f"Questions Fixed: {report.get('questions_fixed', 0)}")
    print(f"Challenges Skipped (already OK): {report.get('challenges_skipped', 0)}")

    if report.get('details'):
        print("\n" + "-"*60)
        print("DETAILS:")
        print("-"*60)
        for detail in report['details']:
            print(f"\n  Challenge: {detail.get('challenge_code')} - {detail.get('challenge_title')}")
            print(f"  Questions: {detail.get('total_questions')}, Fixed: {detail.get('fixed_count')}")

            for q in detail.get('details', []):
                if q.get('fixed'):
                    print(f"    ✓ Q{q['question_index']}: {q['question']} -> index {q['new_correct_index']}")
                elif not q.get('had_correct_index'):
                    print(f"    ✗ Q{q['question_index']}: {q['question']} -> COULD NOT FIX")

    print("\n" + "="*60)


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Fix challenges with missing correct_index')
    parser.add_argument('--dry-run', action='store_true', default=True,
                        help='Only report what would be changed (default: True)')
    parser.add_argument('--apply', action='store_true',
                        help='Actually apply the fixes (disables dry-run)')
    parser.add_argument('--challenge', type=str,
                        help='Fix a specific challenge by code (e.g., PPG2)')
    parser.add_argument('--analyze', action='store_true',
                        help='Only analyze and report broken challenges')

    args = parser.parse_args()

    dry_run = not args.apply

    if args.analyze:
        print("\nAnalyzing challenges...")
        report = analyze_challenges()
        print(f"\nTotal Challenges: {report['total']}")
        print(f"Healthy: {report['healthy']}")
        print(f"Broken: {report['broken']}")

        if report['broken_challenges']:
            print("\nBroken Challenges:")
            for bc in report['broken_challenges']:
                print(f"  - {bc['code']}: {bc['title']} ({bc['missing_correct_index']}/{bc['question_count']} missing)")

    elif args.challenge:
        print(f"\nFixing challenge: {args.challenge}")
        print(f"Dry run: {dry_run}")
        result = fix_challenge(args.challenge, dry_run=dry_run)
        print_report({'details': [result], **result})

    else:
        print("\nFixing all challenges...")
        print(f"Dry run: {dry_run}")
        report = fix_all_challenges(dry_run=dry_run)
        print_report(report)

        if dry_run:
            print("\n⚠️  This was a DRY RUN. No changes were saved.")
            print("    Run with --apply to actually fix the challenges.")


# ============================================
# DJANGO SHELL QUICK COMMANDS
# ============================================
"""
Quick commands to run from Django shell:

# Analyze all challenges
from scripts.fix_challenge_correct_index import analyze_challenges
report = analyze_challenges()
print(report)

# Fix a specific challenge (dry run)
from scripts.fix_challenge_correct_index import fix_challenge
result = fix_challenge('PPG2', dry_run=True)
print(result)

# Fix a specific challenge (apply)
from scripts.fix_challenge_correct_index import fix_challenge
result = fix_challenge('PPG2', dry_run=False)
print(result)

# Fix all challenges (dry run)
from scripts.fix_challenge_correct_index import fix_all_challenges, print_report
report = fix_all_challenges(dry_run=True)
print_report(report)

# Fix all challenges (apply)
from scripts.fix_challenge_correct_index import fix_all_challenges, print_report
report = fix_all_challenges(dry_run=False)
print_report(report)
"""
