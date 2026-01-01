"""Management command to seed verified Hindi letters."""
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.curriculum.models import VerifiedLetter


class Command(BaseCommand):
    help = 'Seeds verified Hindi vowels and consonants with pronunciation guides'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Hindi letter seeding...'))

        # Hindi Vowels (स्वर)
        vowels = [
            {'char': 'अ', 'roman': 'a', 'sound': 'a as in about', 'example_word': 'अनार', 'example_meaning': 'pomegranate', 'example_image': 'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=120&h=120&fit=crop'},
            {'char': 'आ', 'roman': 'aa', 'sound': 'aa as in father', 'example_word': 'आम', 'example_meaning': 'mango', 'example_image': 'https://images.unsplash.com/photo-1553279768-865429fa0078?w=120&h=120&fit=crop'},
            {'char': 'इ', 'roman': 'i', 'sound': 'i as in bit', 'example_word': 'इमली', 'example_meaning': 'tamarind', 'example_image': 'https://images.unsplash.com/photo-1590502160462-58b41354f588?w=120&h=120&fit=crop'},
            {'char': 'ई', 'roman': 'ee', 'sound': 'ee as in feet', 'example_word': 'ईख', 'example_meaning': 'sugarcane', 'example_image': 'https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=120&h=120&fit=crop'},
            {'char': 'उ', 'roman': 'u', 'sound': 'u as in put', 'example_word': 'उल्लू', 'example_meaning': 'owl', 'example_image': 'https://images.unsplash.com/photo-1543549790-8b5f4a028cfb?w=120&h=120&fit=crop'},
            {'char': 'ऊ', 'roman': 'oo', 'sound': 'oo as in boot', 'example_word': 'ऊन', 'example_meaning': 'wool', 'example_image': 'https://images.unsplash.com/photo-1544967082-d9d25d867d66?w=120&h=120&fit=crop'},
            {'char': 'ए', 'roman': 'e', 'sound': 'e as in bet', 'example_word': 'एक', 'example_meaning': 'one', 'example_image': 'https://images.unsplash.com/photo-1509228627152-72ae9ae6848d?w=120&h=120&fit=crop'},
            {'char': 'ऐ', 'roman': 'ai', 'sound': 'ai as in bat', 'example_word': 'ऐनक', 'example_meaning': 'glasses', 'example_image': 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=120&h=120&fit=crop'},
            {'char': 'ओ', 'roman': 'o', 'sound': 'o as in go', 'example_word': 'ओखली', 'example_meaning': 'mortar', 'example_image': 'https://images.unsplash.com/photo-1506976785307-8732e854ad03?w=120&h=120&fit=crop'},
            {'char': 'औ', 'roman': 'au', 'sound': 'au as in taught', 'example_word': 'औरत', 'example_meaning': 'woman', 'example_image': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=120&h=120&fit=crop'},
        ]

        # Hindi Consonants (व्यंजन)
        consonants = [
            {'char': 'क', 'roman': 'ka', 'sound': 'k', 'example_word': 'कमल', 'example_meaning': 'lotus', 'example_image': 'https://images.unsplash.com/photo-1474557157379-8aa74a6ef541?w=120&h=120&fit=crop'},
            {'char': 'ख', 'roman': 'kha', 'sound': 'kh', 'example_word': 'खरगोश', 'example_meaning': 'rabbit', 'example_image': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=120&h=120&fit=crop'},
            {'char': 'ग', 'roman': 'ga', 'sound': 'g', 'example_word': 'गाय', 'example_meaning': 'cow', 'example_image': 'https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=120&h=120&fit=crop'},
            {'char': 'घ', 'roman': 'gha', 'sound': 'gh', 'example_word': 'घर', 'example_meaning': 'house', 'example_image': 'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=120&h=120&fit=crop'},
            {'char': 'च', 'roman': 'cha', 'sound': 'ch', 'example_word': 'चम्मच', 'example_meaning': 'spoon', 'example_image': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=120&h=120&fit=crop'},
            {'char': 'छ', 'roman': 'chha', 'sound': 'chh', 'example_word': 'छाता', 'example_meaning': 'umbrella', 'example_image': 'https://images.unsplash.com/photo-1534309466160-70b22cc6252c?w=120&h=120&fit=crop'},
            {'char': 'ज', 'roman': 'ja', 'sound': 'j', 'example_word': 'जहाज', 'example_meaning': 'ship', 'example_image': 'https://images.unsplash.com/photo-1534609178244-86f2ab3cd59d?w=120&h=120&fit=crop'},
            {'char': 'झ', 'roman': 'jha', 'sound': 'jh', 'example_word': 'झंडा', 'example_meaning': 'flag', 'example_image': 'https://images.unsplash.com/photo-1569974507005-6dc61f97fb5c?w=120&h=120&fit=crop'},
            {'char': 'ट', 'roman': 'ta', 'sound': 't (hard)', 'example_word': 'टमाटर', 'example_meaning': 'tomato', 'example_image': 'https://images.unsplash.com/photo-1546470427-227c7369cfc0?w=120&h=120&fit=crop'},
            {'char': 'ठ', 'roman': 'tha', 'sound': 'th (hard)', 'example_word': 'ठंड', 'example_meaning': 'cold', 'example_image': 'https://images.unsplash.com/photo-1491002052546-bf38f186af56?w=120&h=120&fit=crop'},
            {'char': 'ड', 'roman': 'da', 'sound': 'd (hard)', 'example_word': 'डमरू', 'example_meaning': 'drum', 'example_image': 'https://images.unsplash.com/photo-1519892300165-cb5542fb47c7?w=120&h=120&fit=crop'},
            {'char': 'ढ', 'roman': 'dha', 'sound': 'dh (hard)', 'example_word': 'ढोल', 'example_meaning': 'drum', 'example_image': 'https://images.unsplash.com/photo-1543443258-92b04ad5ec6b?w=120&h=120&fit=crop'},
            {'char': 'ण', 'roman': 'na', 'sound': 'n (retroflex)', 'example_word': 'बाण', 'example_meaning': 'arrow', 'example_image': 'https://images.unsplash.com/photo-1579783483458-83d02161294e?w=120&h=120&fit=crop'},
            {'char': 'त', 'roman': 'ta', 'sound': 't (soft)', 'example_word': 'तारा', 'example_meaning': 'star', 'example_image': 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=120&h=120&fit=crop'},
            {'char': 'थ', 'roman': 'tha', 'sound': 'th (soft)', 'example_word': 'थाली', 'example_meaning': 'plate', 'example_image': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=120&h=120&fit=crop'},
            {'char': 'द', 'roman': 'da', 'sound': 'd (soft)', 'example_word': 'दवाई', 'example_meaning': 'medicine', 'example_image': 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=120&h=120&fit=crop'},
            {'char': 'ध', 'roman': 'dha', 'sound': 'dh (soft)', 'example_word': 'धनुष', 'example_meaning': 'bow', 'example_image': 'https://images.unsplash.com/photo-1510925758641-869d353cecc7?w=120&h=120&fit=crop'},
            {'char': 'न', 'roman': 'na', 'sound': 'n', 'example_word': 'नल', 'example_meaning': 'tap', 'example_image': 'https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=120&h=120&fit=crop'},
            {'char': 'प', 'roman': 'pa', 'sound': 'p', 'example_word': 'पतंग', 'example_meaning': 'kite', 'example_image': 'https://images.unsplash.com/photo-1517479149777-5f3b1511d5ad?w=120&h=120&fit=crop'},
            {'char': 'फ', 'roman': 'pha', 'sound': 'ph/f', 'example_word': 'फल', 'example_meaning': 'fruit', 'example_image': 'https://images.unsplash.com/photo-1619566636858-adf3ef46400b?w=120&h=120&fit=crop'},
            {'char': 'ब', 'roman': 'ba', 'sound': 'b', 'example_word': 'बकरी', 'example_meaning': 'goat', 'example_image': 'https://images.unsplash.com/photo-1524024973431-2ad916746881?w=120&h=120&fit=crop'},
            {'char': 'भ', 'roman': 'bha', 'sound': 'bh', 'example_word': 'भालू', 'example_meaning': 'bear', 'example_image': 'https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=120&h=120&fit=crop'},
            {'char': 'म', 'roman': 'ma', 'sound': 'm', 'example_word': 'मछली', 'example_meaning': 'fish', 'example_image': 'https://images.unsplash.com/photo-1524704654690-b56c05c78a00?w=120&h=120&fit=crop'},
            {'char': 'य', 'roman': 'ya', 'sound': 'y', 'example_word': 'यात्रा', 'example_meaning': 'journey', 'example_image': 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=120&h=120&fit=crop'},
            {'char': 'र', 'roman': 'ra', 'sound': 'r', 'example_word': 'राजा', 'example_meaning': 'king', 'example_image': 'https://images.unsplash.com/photo-1578632292335-df3abbb0d586?w=120&h=120&fit=crop'},
            {'char': 'ल', 'roman': 'la', 'sound': 'l', 'example_word': 'लड्डू', 'example_meaning': 'sweet', 'example_image': 'https://images.unsplash.com/photo-1666190094553-d8cfcfb80124?w=120&h=120&fit=crop'},
            {'char': 'व', 'roman': 'va', 'sound': 'v/w', 'example_word': 'वन', 'example_meaning': 'forest', 'example_image': 'https://images.unsplash.com/photo-1448375240586-882707db888b?w=120&h=120&fit=crop'},
            {'char': 'श', 'roman': 'sha', 'sound': 'sh', 'example_word': 'शेर', 'example_meaning': 'lion', 'example_image': 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=120&h=120&fit=crop'},
            {'char': 'ष', 'roman': 'sha', 'sound': 'sh (retroflex)', 'example_word': 'षट्कोण', 'example_meaning': 'hexagon', 'example_image': 'https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?w=120&h=120&fit=crop'},
            {'char': 'स', 'roman': 'sa', 'sound': 's', 'example_word': 'सेब', 'example_meaning': 'apple', 'example_image': 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=120&h=120&fit=crop'},
            {'char': 'ह', 'roman': 'ha', 'sound': 'h', 'example_word': 'हाथी', 'example_meaning': 'elephant', 'example_image': 'https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=120&h=120&fit=crop'},
        ]

        # Combine all letters
        all_letters = vowels + consonants
        created_count = 0
        updated_count = 0

        for letter_data in all_letters:
            # Check if letter already exists
            letter, created = VerifiedLetter.objects.get_or_create(
                language='HINDI',
                character=letter_data['char'],
                defaults={
                    'romanization': letter_data['roman'],
                    'pronunciation_guide': letter_data['sound'],
                    'example_word': letter_data['example_word'],
                    'example_word_meaning': letter_data['example_meaning'],
                    'example_image': letter_data.get('example_image'),
                    'status': 'VERIFIED',
                    'verified_at': timezone.now(),
                    'pronunciation_accuracy': 5,
                    'example_relevance': 5,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {letter.character} ({letter.romanization})'))
            else:
                # Update existing letter to ensure data is current
                letter.romanization = letter_data['roman']
                letter.pronunciation_guide = letter_data['sound']
                letter.example_word = letter_data['example_word']
                letter.example_word_meaning = letter_data['example_meaning']
                letter.example_image = letter_data.get('example_image')
                letter.status = 'VERIFIED'
                letter.verified_at = timezone.now()
                letter.pronunciation_accuracy = 5
                letter.example_relevance = 5
                letter.save()
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'↻ Updated: {letter.character} ({letter.romanization})'))

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS(f'Hindi Letter Seeding Complete!'))
        self.stdout.write(self.style.SUCCESS(f'Created: {created_count} letters'))
        self.stdout.write(self.style.SUCCESS(f'Updated: {updated_count} letters'))
        self.stdout.write(self.style.SUCCESS(f'Total: {created_count + updated_count} letters'))
        self.stdout.write(self.style.SUCCESS(f'  - Vowels (स्वर): {len(vowels)}'))
        self.stdout.write(self.style.SUCCESS(f'  - Consonants (व्यंजन): {len(consonants)}'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
