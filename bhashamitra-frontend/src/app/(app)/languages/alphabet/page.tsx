'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { MainLayout } from '@/components/layout';
import { Card, Loading, ProgressBar, SpeakerButton } from '@/components/ui';
import { fadeInUp, staggerContainer } from '@/lib/constants';
import { useAudio } from '@/hooks/useAudio';
import { useSounds } from '@/hooks';
import { Celebration } from '@/components/animations';
import { AlphabetQuiz } from '@/components/curriculum';

// Twemoji CDN helper - converts example meaning to appropriate emoji image URL
const TWEMOJI_BASE = 'https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg';
const MEANING_TO_EMOJI: Record<string, string> = {
  'pomegranate': '1f352', 'mango': '1f96d', 'tamarind': '1f33f', 'sugarcane': '1f33e',
  'owl': '1f989', 'wool': '1f9f6', 'one': '31-fe0f-20e3', 'glasses': '1f453',
  'mortar': '1fad7', 'woman': '1f469', 'lotus': '1f338', 'rabbit': '1f430',
  'cow': '1f404', 'house': '1f3e0', 'spoon': '1f944', 'umbrella': '2614',
  'ship': '1f6a2', 'flag': '1f3f3', 'tomato': '1f345', 'cold': '1f976',
  'drum': '1f941', 'arrow': '1f3f9', 'star': '2b50', 'plate': '1f37d-fe0f',
  'medicine': '1f48a', 'bow': '1f3f9', 'tap': '1f6b0', 'kite': '1fa81',
  'fruit': '1f34f', 'goat': '1f410', 'bear': '1f43b', 'fish': '1f41f',
  'journey': '1f6eb', 'king': '1f451', 'laddu sweet': '1f36c', 'forest': '1f332',
  'lion': '1f981', 'hexagon': '1f533', 'apple': '1f34e', 'elephant': '1f418',
  'mother': '1f469', 'leaf': '1f343', 'fly': '1fab0', 'body': '1f9cd',
  'village': '1f3d8-fe0f', 'rat': '1f400', 'plough': '1f33e', 'five': '35-fe0f-20e3',
  'camel': '1f42b', 'tile': '1f9f1', 'poet': '1f4dd', 'stone': '1faa8',
  'rice': '1f35a', 'wisdom': '1f9e0', 'water': '1f4a7', 'crab': '1f980',
  'tooth': '1f9b7', 'mountain': '26f0-fe0f', 'rose': '1f339', 'banana': '1f34c',
  'tamil': '1f4d6', 'bangle': '1f48d', 'bird': '1f426', 'dew': '1f4a7',
  'potato': '1f954', 'pigeon': '1f54a-fe0f', 'limb': '1f4aa', 'sparrow': '1f426',
  'tune': '1f3b5', 'friend': '1f46b', 'box': '1f4e6', 'ear': '1f442',
  'milk': '1f95b', 'coconut': '1f965', 'flower': '1f338', 'yoga': '1f9d8',
  'rope': '1faa2', 'lassi': '1f95b', 'violin': '1f3bb', 'to read': '1f4d6',
  'color': '1f3a8', 'melon': '1f348', 'wing': '1f426', 'grain': '1f33e',
  'papaya': '1f348', 'yam': '1f954', 'banyan': '1f333', 'sweet potato': '1f954',
  'ocean': '1f30a',
};
const getTwemojiUrl = (meaning: string): string => {
  const code = MEANING_TO_EMOJI[meaning.toLowerCase()] || '1f4d6';
  return `${TWEMOJI_BASE}/${code}.svg`;
};

// Hindi Alphabet Data (Devanagari) with example words and images
const HINDI_VOWELS = [
  { char: 'अ', roman: 'a', sound: 'a as in about', exampleWord: 'अनार', exampleMeaning: 'Pomegranate', exampleImage: 'https://images.unsplash.com/photo-1541344999736-83eca272f6fc?w=120&h=120&fit=crop' },
  { char: 'आ', roman: 'aa', sound: 'aa as in father', exampleWord: 'आम', exampleMeaning: 'Mango', exampleImage: 'https://images.unsplash.com/photo-1553279768-865429fa0078?w=120&h=120&fit=crop' },
  { char: 'इ', roman: 'i', sound: 'i as in bit', exampleWord: 'इमली', exampleMeaning: 'Tamarind', exampleImage: 'https://images.unsplash.com/photo-1590502160462-58b41354f588?w=120&h=120&fit=crop' },
  { char: 'ई', roman: 'ee', sound: 'ee as in feet', exampleWord: 'ईख', exampleMeaning: 'Sugarcane', exampleImage: 'https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=120&h=120&fit=crop' },
  { char: 'उ', roman: 'u', sound: 'u as in put', exampleWord: 'उल्लू', exampleMeaning: 'Owl', exampleImage: 'https://images.unsplash.com/photo-1543549790-8b5f4a028cfb?w=120&h=120&fit=crop' },
  { char: 'ऊ', roman: 'oo', sound: 'oo as in boot', exampleWord: 'ऊन', exampleMeaning: 'Wool', exampleImage: 'https://images.unsplash.com/photo-1544967082-d9d25d867d66?w=120&h=120&fit=crop' },
  { char: 'ए', roman: 'e', sound: 'e as in bet', exampleWord: 'एक', exampleMeaning: 'One', exampleImage: 'https://images.unsplash.com/photo-1509228627152-72ae9ae6848d?w=120&h=120&fit=crop' },
  { char: 'ऐ', roman: 'ai', sound: 'ai as in bat', exampleWord: 'ऐनक', exampleMeaning: 'Glasses', exampleImage: 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=120&h=120&fit=crop' },
  { char: 'ओ', roman: 'o', sound: 'o as in go', exampleWord: 'ओखली', exampleMeaning: 'Mortar', exampleImage: 'https://images.unsplash.com/photo-1506976785307-8732e854ad03?w=120&h=120&fit=crop' },
  { char: 'औ', roman: 'au', sound: 'au as in taught', exampleWord: 'औरत', exampleMeaning: 'Woman', exampleImage: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=120&h=120&fit=crop' },
];

const HINDI_CONSONANTS = [
  { char: 'क', roman: 'ka', sound: 'k', exampleWord: 'कमल', exampleMeaning: 'Lotus', exampleImage: 'https://images.unsplash.com/photo-1474557157379-8aa74a6ef541?w=120&h=120&fit=crop' },
  { char: 'ख', roman: 'kha', sound: 'kh', exampleWord: 'खरगोश', exampleMeaning: 'Rabbit', exampleImage: 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=120&h=120&fit=crop' },
  { char: 'ग', roman: 'ga', sound: 'g', exampleWord: 'गाय', exampleMeaning: 'Cow', exampleImage: 'https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=120&h=120&fit=crop' },
  { char: 'घ', roman: 'gha', sound: 'gh', exampleWord: 'घर', exampleMeaning: 'House', exampleImage: 'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=120&h=120&fit=crop' },
  { char: 'च', roman: 'cha', sound: 'ch', exampleWord: 'चम्मच', exampleMeaning: 'Spoon', exampleImage: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=120&h=120&fit=crop' },
  { char: 'छ', roman: 'chha', sound: 'chh', exampleWord: 'छाता', exampleMeaning: 'Umbrella', exampleImage: 'https://images.unsplash.com/photo-1534309466160-70b22cc6252c?w=120&h=120&fit=crop' },
  { char: 'ज', roman: 'ja', sound: 'j', exampleWord: 'जहाज', exampleMeaning: 'Ship', exampleImage: 'https://images.unsplash.com/photo-1534609178244-86f2ab3cd59d?w=120&h=120&fit=crop' },
  { char: 'झ', roman: 'jha', sound: 'jh', exampleWord: 'झंडा', exampleMeaning: 'Flag', exampleImage: 'https://images.unsplash.com/photo-1569974507005-6dc61f97fb5c?w=120&h=120&fit=crop' },
  { char: 'ट', roman: 'ta', sound: 't (hard)', exampleWord: 'टमाटर', exampleMeaning: 'Tomato', exampleImage: 'https://images.unsplash.com/photo-1546470427-227c7369cfc0?w=120&h=120&fit=crop' },
  { char: 'ठ', roman: 'tha', sound: 'th (hard)', exampleWord: 'ठंड', exampleMeaning: 'Cold', exampleImage: 'https://images.unsplash.com/photo-1491002052546-bf38f186af56?w=120&h=120&fit=crop' },
  { char: 'ड', roman: 'da', sound: 'd (hard)', exampleWord: 'डमरू', exampleMeaning: 'Drum', exampleImage: 'https://images.unsplash.com/photo-1519892300165-cb5542fb47c7?w=120&h=120&fit=crop' },
  { char: 'ढ', roman: 'dha', sound: 'dh (hard)', exampleWord: 'ढोल', exampleMeaning: 'Drum', exampleImage: 'https://images.unsplash.com/photo-1543443258-92b04ad5ec6b?w=120&h=120&fit=crop' },
  { char: 'ण', roman: 'na', sound: 'n (retroflex)', exampleWord: 'बाण', exampleMeaning: 'Arrow', exampleImage: 'https://images.unsplash.com/photo-1579783483458-83d02161294e?w=120&h=120&fit=crop' },
  { char: 'त', roman: 'ta', sound: 't (soft)', exampleWord: 'तारा', exampleMeaning: 'Star', exampleImage: 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=120&h=120&fit=crop' },
  { char: 'थ', roman: 'tha', sound: 'th (soft)', exampleWord: 'थाली', exampleMeaning: 'Plate', exampleImage: 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=120&h=120&fit=crop' },
  { char: 'द', roman: 'da', sound: 'd (soft)', exampleWord: 'दवाई', exampleMeaning: 'Medicine', exampleImage: 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=120&h=120&fit=crop' },
  { char: 'ध', roman: 'dha', sound: 'dh (soft)', exampleWord: 'धनुष', exampleMeaning: 'Bow', exampleImage: 'https://images.unsplash.com/photo-1510925758641-869d353cecc7?w=120&h=120&fit=crop' },
  { char: 'न', roman: 'na', sound: 'n', exampleWord: 'नल', exampleMeaning: 'Tap', exampleImage: 'https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=120&h=120&fit=crop' },
  { char: 'प', roman: 'pa', sound: 'p', exampleWord: 'पतंग', exampleMeaning: 'Kite', exampleImage: 'https://images.unsplash.com/photo-1517479149777-5f3b1511d5ad?w=120&h=120&fit=crop' },
  { char: 'फ', roman: 'pha', sound: 'ph/f', exampleWord: 'फल', exampleMeaning: 'Fruit', exampleImage: 'https://images.unsplash.com/photo-1619566636858-adf3ef46400b?w=120&h=120&fit=crop' },
  { char: 'ब', roman: 'ba', sound: 'b', exampleWord: 'बकरी', exampleMeaning: 'Goat', exampleImage: 'https://images.unsplash.com/photo-1524024973431-2ad916746881?w=120&h=120&fit=crop' },
  { char: 'भ', roman: 'bha', sound: 'bh', exampleWord: 'भालू', exampleMeaning: 'Bear', exampleImage: 'https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=120&h=120&fit=crop' },
  { char: 'म', roman: 'ma', sound: 'm', exampleWord: 'मछली', exampleMeaning: 'Fish', exampleImage: 'https://images.unsplash.com/photo-1524704654690-b56c05c78a00?w=120&h=120&fit=crop' },
  { char: 'य', roman: 'ya', sound: 'y', exampleWord: 'यात्रा', exampleMeaning: 'Journey', exampleImage: 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=120&h=120&fit=crop' },
  { char: 'र', roman: 'ra', sound: 'r', exampleWord: 'राजा', exampleMeaning: 'King', exampleImage: 'https://images.unsplash.com/photo-1578632292335-df3abbb0d586?w=120&h=120&fit=crop' },
  { char: 'ल', roman: 'la', sound: 'l', exampleWord: 'लड्डू', exampleMeaning: 'Laddu Sweet', exampleImage: 'https://images.unsplash.com/photo-1666190094553-d8cfcfb80124?w=120&h=120&fit=crop' },
  { char: 'व', roman: 'va', sound: 'v/w', exampleWord: 'वन', exampleMeaning: 'Forest', exampleImage: 'https://images.unsplash.com/photo-1448375240586-882707db888b?w=120&h=120&fit=crop' },
  { char: 'श', roman: 'sha', sound: 'sh', exampleWord: 'शेर', exampleMeaning: 'Lion', exampleImage: 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=120&h=120&fit=crop' },
  { char: 'ष', roman: 'sha', sound: 'sh (retroflex)', exampleWord: 'षट्कोण', exampleMeaning: 'Hexagon', exampleImage: 'https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?w=120&h=120&fit=crop' },
  { char: 'स', roman: 'sa', sound: 's', exampleWord: 'सेब', exampleMeaning: 'Apple', exampleImage: 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=120&h=120&fit=crop' },
  { char: 'ह', roman: 'ha', sound: 'h', exampleWord: 'हाथी', exampleMeaning: 'Elephant', exampleImage: 'https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=120&h=120&fit=crop' },
];

// Tamil Alphabet Data with example words and images
const TAMIL_VOWELS = [
  { char: 'அ', roman: 'a', sound: 'a as in about', exampleWord: 'அம்மா', exampleMeaning: 'Mother', exampleImage: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=120&h=120&fit=crop' },
  { char: 'ஆ', roman: 'aa', sound: 'aa as in father', exampleWord: 'ஆடு', exampleMeaning: 'Goat', exampleImage: 'https://images.unsplash.com/photo-1524024973431-2ad916746881?w=120&h=120&fit=crop' },
  { char: 'இ', roman: 'i', sound: 'i as in bit', exampleWord: 'இலை', exampleMeaning: 'Leaf', exampleImage: 'https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?w=120&h=120&fit=crop' },
  { char: 'ஈ', roman: 'ee', sound: 'ee as in feet', exampleWord: 'ஈ', exampleMeaning: 'Fly', exampleImage: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=120&h=120&fit=crop' },
  { char: 'உ', roman: 'u', sound: 'u as in put', exampleWord: 'உடல்', exampleMeaning: 'Body', exampleImage: 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=120&h=120&fit=crop' },
  { char: 'ஊ', roman: 'oo', sound: 'oo as in boot', exampleWord: 'ஊர்', exampleMeaning: 'Village', exampleImage: 'https://images.unsplash.com/photo-1516483638261-f4d223d13ce3?w=120&h=120&fit=crop' },
  { char: 'எ', roman: 'e', sound: 'e as in bet', exampleWord: 'எலி', exampleMeaning: 'Rat', exampleImage: 'https://images.unsplash.com/photo-1425082661705-1834bfd09dca?w=120&h=120&fit=crop' },
  { char: 'ஏ', roman: 'e', sound: 'e as in they', exampleWord: 'ஏர்', exampleMeaning: 'Plough', exampleImage: 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=120&h=120&fit=crop' },
  { char: 'ஐ', roman: 'ai', sound: 'ai as in aisle', exampleWord: 'ஐந்து', exampleMeaning: 'Five', exampleImage: 'https://images.unsplash.com/photo-1509228627152-72ae9ae6848d?w=120&h=120&fit=crop' },
  { char: 'ஒ', roman: 'o', sound: 'o as in go', exampleWord: 'ஒட்டகம்', exampleMeaning: 'Camel', exampleImage: 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=120&h=120&fit=crop' },
  { char: 'ஓ', roman: 'o', sound: 'o as in boat', exampleWord: 'ஓடு', exampleMeaning: 'Tile', exampleImage: 'https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?w=120&h=120&fit=crop' },
  { char: 'ஔ', roman: 'au', sound: 'au as in house', exampleWord: 'ஔவை', exampleMeaning: 'Poet', exampleImage: 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=120&h=120&fit=crop' },
];

const TAMIL_CONSONANTS = [
  { char: 'க', roman: 'ka', sound: 'k/g', exampleWord: 'கல்', exampleMeaning: 'Stone', exampleImage: 'https://images.unsplash.com/photo-1519340241574-2cec6aef0c01?w=120&h=120&fit=crop' },
  { char: 'ங', roman: 'nga', sound: 'ng', exampleWord: 'மாங்காய்', exampleMeaning: 'Mango', exampleImage: 'https://images.unsplash.com/photo-1553279768-865429fa0078?w=120&h=120&fit=crop' },
  { char: 'ச', roman: 'cha', sound: 'ch/s', exampleWord: 'சோறு', exampleMeaning: 'Rice', exampleImage: 'https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6?w=120&h=120&fit=crop' },
  { char: 'ஞ', roman: 'nya', sound: 'ny', exampleWord: 'ஞானம்', exampleMeaning: 'Wisdom', exampleImage: 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=120&h=120&fit=crop' },
  { char: 'ட', roman: 'ta', sound: 't (hard)', exampleWord: 'டம்', exampleMeaning: 'Drum', exampleImage: 'https://images.unsplash.com/photo-1519892300165-cb5542fb47c7?w=120&h=120&fit=crop' },
  { char: 'ண', roman: 'na', sound: 'n (retroflex)', exampleWord: 'பண்', exampleMeaning: 'Tune', exampleImage: 'https://images.unsplash.com/photo-1507838153414-b4b713384a76?w=120&h=120&fit=crop' },
  { char: 'த', roman: 'tha', sound: 'th', exampleWord: 'தண்ணீர்', exampleMeaning: 'Water', exampleImage: 'https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=120&h=120&fit=crop' },
  { char: 'ந', roman: 'na', sound: 'n', exampleWord: 'நண்டு', exampleMeaning: 'Crab', exampleImage: 'https://images.unsplash.com/photo-1550747545-c896b5f89ff7?w=120&h=120&fit=crop' },
  { char: 'ப', roman: 'pa', sound: 'p/b', exampleWord: 'பல்', exampleMeaning: 'Tooth', exampleImage: 'https://images.unsplash.com/photo-1606811841689-23dfddce3e95?w=120&h=120&fit=crop' },
  { char: 'ம', roman: 'ma', sound: 'm', exampleWord: 'மலை', exampleMeaning: 'Mountain', exampleImage: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=120&h=120&fit=crop' },
  { char: 'ய', roman: 'ya', sound: 'y', exampleWord: 'யானை', exampleMeaning: 'Elephant', exampleImage: 'https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=120&h=120&fit=crop' },
  { char: 'ர', roman: 'ra', sound: 'r', exampleWord: 'ரோஜா', exampleMeaning: 'Rose', exampleImage: 'https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=120&h=120&fit=crop' },
  { char: 'ல', roman: 'la', sound: 'l', exampleWord: 'லட்டு', exampleMeaning: 'Laddu Sweet', exampleImage: 'https://images.unsplash.com/photo-1666190094553-d8cfcfb80124?w=120&h=120&fit=crop' },
  { char: 'வ', roman: 'va', sound: 'v/w', exampleWord: 'வாழை', exampleMeaning: 'Banana', exampleImage: 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=120&h=120&fit=crop' },
  { char: 'ழ', roman: 'zha', sound: 'zh (retroflex)', exampleWord: 'தமிழ்', exampleMeaning: 'Tamil', exampleImage: 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=120&h=120&fit=crop' },
  { char: 'ள', roman: 'la', sound: 'l (retroflex)', exampleWord: 'வள்', exampleMeaning: 'Bangle', exampleImage: 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=120&h=120&fit=crop' },
  { char: 'ற', roman: 'ra', sound: 'r (hard)', exampleWord: 'பறவை', exampleMeaning: 'Bird', exampleImage: 'https://images.unsplash.com/photo-1444464666168-49d633b86797?w=120&h=120&fit=crop' },
  { char: 'ன', roman: 'na', sound: 'n (alveolar)', exampleWord: 'பனி', exampleMeaning: 'Dew', exampleImage: 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=120&h=120&fit=crop' },
];

// Punjabi Alphabet Data (Gurmukhi) with example words and images
const PUNJABI_VOWELS = [
  { char: 'ਅ', roman: 'a', sound: 'a as in about', exampleWord: 'ਅੰਬ', exampleMeaning: 'Mango', exampleImage: 'https://images.unsplash.com/photo-1553279768-865429fa0078?w=120&h=120&fit=crop' },
  { char: 'ਆ', roman: 'aa', sound: 'aa as in father', exampleWord: 'ਆਲੂ', exampleMeaning: 'Potato', exampleImage: 'https://images.unsplash.com/photo-1518977676601-b53f82afe9e7?w=120&h=120&fit=crop' },
  { char: 'ਇ', roman: 'i', sound: 'i as in bit', exampleWord: 'ਇਮਲੀ', exampleMeaning: 'Tamarind', exampleImage: 'https://images.unsplash.com/photo-1590502160462-58b41354f588?w=120&h=120&fit=crop' },
  { char: 'ਈ', roman: 'ee', sound: 'ee as in feet', exampleWord: 'ਈਖ', exampleMeaning: 'Sugarcane', exampleImage: 'https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=120&h=120&fit=crop' },
  { char: 'ਉ', roman: 'u', sound: 'u as in put', exampleWord: 'ਉੱਲੂ', exampleMeaning: 'Owl', exampleImage: 'https://images.unsplash.com/photo-1543549790-8b5f4a028cfb?w=120&h=120&fit=crop' },
  { char: 'ਊ', roman: 'oo', sound: 'oo as in boot', exampleWord: 'ਊਠ', exampleMeaning: 'Camel', exampleImage: 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=120&h=120&fit=crop' },
  { char: 'ਏ', roman: 'e', sound: 'e as in they', exampleWord: 'ਏਕ', exampleMeaning: 'One', exampleImage: 'https://images.unsplash.com/photo-1509228627152-72ae9ae6848d?w=120&h=120&fit=crop' },
  { char: 'ਐ', roman: 'ai', sound: 'ai as in bat', exampleWord: 'ਐਨਕ', exampleMeaning: 'Glasses', exampleImage: 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=120&h=120&fit=crop' },
  { char: 'ਓ', roman: 'o', sound: 'o as in go', exampleWord: 'ਓਖਲੀ', exampleMeaning: 'Mortar', exampleImage: 'https://images.unsplash.com/photo-1506976785307-8732e854ad03?w=120&h=120&fit=crop' },
  { char: 'ਔ', roman: 'au', sound: 'au as in taught', exampleWord: 'ਔਰਤ', exampleMeaning: 'Woman', exampleImage: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=120&h=120&fit=crop' },
];

const PUNJABI_CONSONANTS = [
  { char: 'ਕ', roman: 'ka', sound: 'k as in kite', exampleWord: 'ਕਬੂਤਰ', exampleMeaning: 'Pigeon', exampleImage: 'https://images.unsplash.com/photo-1555169062-013468b47731?w=120&h=120&fit=crop' },
  { char: 'ਖ', roman: 'kha', sound: 'kh as in khan', exampleWord: 'ਖਰਗੋਸ਼', exampleMeaning: 'Rabbit', exampleImage: 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=120&h=120&fit=crop' },
  { char: 'ਗ', roman: 'ga', sound: 'g as in go', exampleWord: 'ਗਾਂ', exampleMeaning: 'Cow', exampleImage: 'https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=120&h=120&fit=crop' },
  { char: 'ਘ', roman: 'gha', sound: 'gh as in ghost', exampleWord: 'ਘਰ', exampleMeaning: 'House', exampleImage: 'https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=120&h=120&fit=crop' },
  { char: 'ਙ', roman: 'nga', sound: 'ng as in sing', exampleWord: 'ਅੰਗ', exampleMeaning: 'Limb', exampleImage: 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=120&h=120&fit=crop' },
  { char: 'ਚ', roman: 'cha', sound: 'ch as in chair', exampleWord: 'ਚਿੜੀ', exampleMeaning: 'Sparrow', exampleImage: 'https://images.unsplash.com/photo-1486365227551-f3f90034a57c?w=120&h=120&fit=crop' },
  { char: 'ਛ', roman: 'chha', sound: 'chh as in church hill', exampleWord: 'ਛਤਰੀ', exampleMeaning: 'Umbrella', exampleImage: 'https://images.unsplash.com/photo-1534309466160-70b22cc6252c?w=120&h=120&fit=crop' },
  { char: 'ਜ', roman: 'ja', sound: 'j as in jump', exampleWord: 'ਜਹਾਜ਼', exampleMeaning: 'Ship', exampleImage: 'https://images.unsplash.com/photo-1534343821789-89dd78d50b53?w=120&h=120&fit=crop' },
  { char: 'ਝ', roman: 'jha', sound: 'jh as in hedgehog', exampleWord: 'ਝੰਡਾ', exampleMeaning: 'Flag', exampleImage: 'https://images.unsplash.com/photo-1569974507005-6dc61f97fb5c?w=120&h=120&fit=crop' },
  { char: 'ਞ', roman: 'nya', sound: 'ny as in canyon', exampleWord: 'ਮਿੱਤਰ', exampleMeaning: 'Friend', exampleImage: 'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=120&h=120&fit=crop' },
  { char: 'ਟ', roman: 'ta', sound: 't (hard)', exampleWord: 'ਟਮਾਟਰ', exampleMeaning: 'Tomato', exampleImage: 'https://images.unsplash.com/photo-1558818498-28c1e002674f?w=120&h=120&fit=crop' },
  { char: 'ਠ', roman: 'tha', sound: 'th (hard)', exampleWord: 'ਠੰਡਾ', exampleMeaning: 'Cold', exampleImage: 'https://images.unsplash.com/photo-1516912481808-3406841bd33c?w=120&h=120&fit=crop' },
  { char: 'ਡ', roman: 'da', sound: 'd (hard)', exampleWord: 'ਡੱਬਾ', exampleMeaning: 'Box', exampleImage: 'https://images.unsplash.com/photo-1607166452427-7e4477079cb9?w=120&h=120&fit=crop' },
  { char: 'ਢ', roman: 'dha', sound: 'dh (hard)', exampleWord: 'ਢੋਲ', exampleMeaning: 'Drum', exampleImage: 'https://images.unsplash.com/photo-1519892300165-cb5542fb47c7?w=120&h=120&fit=crop' },
  { char: 'ਣ', roman: 'na', sound: 'n (retroflex)', exampleWord: 'ਕੰਨ', exampleMeaning: 'Ear', exampleImage: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=120&h=120&fit=crop' },
  { char: 'ਤ', roman: 'ta', sound: 't as in top', exampleWord: 'ਤਾਰਾ', exampleMeaning: 'Star', exampleImage: 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=120&h=120&fit=crop' },
  { char: 'ਥ', roman: 'tha', sound: 'th as in think', exampleWord: 'ਥਾਲੀ', exampleMeaning: 'Plate', exampleImage: 'https://images.unsplash.com/photo-1544025162-d76694265947?w=120&h=120&fit=crop' },
  { char: 'ਦ', roman: 'da', sound: 'd as in door', exampleWord: 'ਦੁੱਧ', exampleMeaning: 'Milk', exampleImage: 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=120&h=120&fit=crop' },
  { char: 'ਧ', roman: 'dha', sound: 'dh as in dharma', exampleWord: 'ਧਨੁਸ਼', exampleMeaning: 'Bow', exampleImage: 'https://images.unsplash.com/photo-1533381748829-78674b3e9632?w=120&h=120&fit=crop' },
  { char: 'ਨ', roman: 'na', sound: 'n as in name', exampleWord: 'ਨਾਰੀਅਲ', exampleMeaning: 'Coconut', exampleImage: 'https://images.unsplash.com/photo-1550689960-d9c8ab6f7c4f?w=120&h=120&fit=crop' },
  { char: 'ਪ', roman: 'pa', sound: 'p as in pen', exampleWord: 'ਪਤੰਗ', exampleMeaning: 'Kite', exampleImage: 'https://images.unsplash.com/photo-1601580184474-24f0dbbcf7fe?w=120&h=120&fit=crop' },
  { char: 'ਫ', roman: 'pha', sound: 'ph as in phone', exampleWord: 'ਫੁੱਲ', exampleMeaning: 'Flower', exampleImage: 'https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=120&h=120&fit=crop' },
  { char: 'ਬ', roman: 'ba', sound: 'b as in ball', exampleWord: 'ਬੱਕਰੀ', exampleMeaning: 'Goat', exampleImage: 'https://images.unsplash.com/photo-1524024973431-2ad916746881?w=120&h=120&fit=crop' },
  { char: 'ਭ', roman: 'bha', sound: 'bh as in abhor', exampleWord: 'ਭਾਲੂ', exampleMeaning: 'Bear', exampleImage: 'https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=120&h=120&fit=crop' },
  { char: 'ਮ', roman: 'ma', sound: 'm as in mother', exampleWord: 'ਮੱਛੀ', exampleMeaning: 'Fish', exampleImage: 'https://images.unsplash.com/photo-1544943910-4c1dc44aab44?w=120&h=120&fit=crop' },
  { char: 'ਯ', roman: 'ya', sound: 'y as in yes', exampleWord: 'ਯੋਗਾ', exampleMeaning: 'Yoga', exampleImage: 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=120&h=120&fit=crop' },
  { char: 'ਰ', roman: 'ra', sound: 'r as in run', exampleWord: 'ਰੱਸੀ', exampleMeaning: 'Rope', exampleImage: 'https://images.unsplash.com/photo-1583395838144-09be6e04e84f?w=120&h=120&fit=crop' },
  { char: 'ਲ', roman: 'la', sound: 'l as in love', exampleWord: 'ਲੱਸੀ', exampleMeaning: 'Lassi', exampleImage: 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=120&h=120&fit=crop' },
  { char: 'ਵ', roman: 'va', sound: 'v as in van', exampleWord: 'ਵਾਇਲਨ', exampleMeaning: 'Violin', exampleImage: 'https://images.unsplash.com/photo-1612225330812-01a9c6b355ec?w=120&h=120&fit=crop' },
  { char: 'ੜ', roman: 'rha', sound: 'r (flap)', exampleWord: 'ਪੜ੍ਹਨਾ', exampleMeaning: 'To Read', exampleImage: 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=120&h=120&fit=crop' },
  { char: 'ਸ', roman: 'sa', sound: 's as in sun', exampleWord: 'ਸੇਬ', exampleMeaning: 'Apple', exampleImage: 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=120&h=120&fit=crop' },
  { char: 'ਹ', roman: 'ha', sound: 'h as in house', exampleWord: 'ਹਾਥੀ', exampleMeaning: 'Elephant', exampleImage: 'https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=120&h=120&fit=crop' },
];

// Gujarati Alphabet Data with example words and images
const GUJARATI_VOWELS = [
  { char: 'અ', roman: 'a', sound: 'a as in about', exampleWord: 'અનાર', exampleMeaning: 'Pomegranate', exampleImage: 'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=120&h=120&fit=crop' },
  { char: 'આ', roman: 'aa', sound: 'aa as in father', exampleWord: 'આમ', exampleMeaning: 'Mango', exampleImage: 'https://images.unsplash.com/photo-1553279768-865429fa0078?w=120&h=120&fit=crop' },
  { char: 'ઇ', roman: 'i', sound: 'i as in bit', exampleWord: 'ઇમલી', exampleMeaning: 'Tamarind', exampleImage: 'https://images.unsplash.com/photo-1590502160462-58b41354f588?w=120&h=120&fit=crop' },
  { char: 'ઈ', roman: 'ee', sound: 'ee as in feet', exampleWord: 'ઈંડું', exampleMeaning: 'Egg', exampleImage: 'https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=120&h=120&fit=crop' },
  { char: 'ઉ', roman: 'u', sound: 'u as in put', exampleWord: 'ઉલ્લુ', exampleMeaning: 'Owl', exampleImage: 'https://images.unsplash.com/photo-1543549790-8b5f4a028cfb?w=120&h=120&fit=crop' },
  { char: 'ઊ', roman: 'oo', sound: 'oo as in boot', exampleWord: 'ઊન', exampleMeaning: 'Wool', exampleImage: 'https://images.unsplash.com/photo-1544967082-d9d25d867d66?w=120&h=120&fit=crop' },
  { char: 'એ', roman: 'e', sound: 'e as in bet', exampleWord: 'એક', exampleMeaning: 'One', exampleImage: 'https://images.unsplash.com/photo-1509228627152-72ae9ae6848d?w=120&h=120&fit=crop' },
  { char: 'ઐ', roman: 'ai', sound: 'ai as in aisle', exampleWord: 'ઐનક', exampleMeaning: 'Glasses', exampleImage: 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=120&h=120&fit=crop' },
  { char: 'ઓ', roman: 'o', sound: 'o as in go', exampleWord: 'ઓખલી', exampleMeaning: 'Mortar', exampleImage: 'https://images.unsplash.com/photo-1506976785307-8732e854ad03?w=120&h=120&fit=crop' },
  { char: 'ઔ', roman: 'au', sound: 'au as in taught', exampleWord: 'ઔરત', exampleMeaning: 'Woman', exampleImage: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=120&h=120&fit=crop' },
];

const GUJARATI_CONSONANTS = [
  { char: 'ક', roman: 'ka', sound: 'k as in kite', exampleWord: 'કમળ', exampleMeaning: 'Lotus', exampleImage: 'https://images.unsplash.com/photo-1474557157379-8aa74a6ef541?w=120&h=120&fit=crop' },
  { char: 'ખ', roman: 'kha', sound: 'kh as in khan', exampleWord: 'ખરગોશ', exampleMeaning: 'Rabbit', exampleImage: 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=120&h=120&fit=crop' },
  { char: 'ગ', roman: 'ga', sound: 'g as in go', exampleWord: 'ગાય', exampleMeaning: 'Cow', exampleImage: 'https://images.unsplash.com/photo-1570042225831-d98fa7577f1e?w=120&h=120&fit=crop' },
  { char: 'ઘ', roman: 'gha', sound: 'gh as in ghost', exampleWord: 'ઘર', exampleMeaning: 'House', exampleImage: 'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=120&h=120&fit=crop' },
  { char: 'ચ', roman: 'cha', sound: 'ch as in chair', exampleWord: 'ચમચી', exampleMeaning: 'Spoon', exampleImage: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=120&h=120&fit=crop' },
  { char: 'છ', roman: 'chha', sound: 'chh as in church', exampleWord: 'છાતા', exampleMeaning: 'Umbrella', exampleImage: 'https://images.unsplash.com/photo-1534309466160-70b22cc6252c?w=120&h=120&fit=crop' },
  { char: 'જ', roman: 'ja', sound: 'j as in jump', exampleWord: 'જહાજ', exampleMeaning: 'Ship', exampleImage: 'https://images.unsplash.com/photo-1534609178244-86f2ab3cd59d?w=120&h=120&fit=crop' },
  { char: 'ઝ', roman: 'jha', sound: 'jh as in hedgehog', exampleWord: 'ઝંડો', exampleMeaning: 'Flag', exampleImage: 'https://images.unsplash.com/photo-1569974507005-6dc61f97fb5c?w=120&h=120&fit=crop' },
  { char: 'ટ', roman: 'ta', sound: 't (hard)', exampleWord: 'ટમેટું', exampleMeaning: 'Tomato', exampleImage: 'https://images.unsplash.com/photo-1546470427-227c7369cfc0?w=120&h=120&fit=crop' },
  { char: 'ઠ', roman: 'tha', sound: 'th (hard)', exampleWord: 'ઠંડી', exampleMeaning: 'Cold', exampleImage: 'https://images.unsplash.com/photo-1491002052546-bf38f186af56?w=120&h=120&fit=crop' },
  { char: 'ડ', roman: 'da', sound: 'd (hard)', exampleWord: 'ડમરું', exampleMeaning: 'Drum', exampleImage: 'https://images.unsplash.com/photo-1519892300165-cb5542fb47c7?w=120&h=120&fit=crop' },
  { char: 'ઢ', roman: 'dha', sound: 'dh (hard)', exampleWord: 'ઢોલ', exampleMeaning: 'Drum', exampleImage: 'https://images.unsplash.com/photo-1543443258-92b04ad5ec6b?w=120&h=120&fit=crop' },
  { char: 'ણ', roman: 'na', sound: 'n (retroflex)', exampleWord: 'બાણ', exampleMeaning: 'Arrow', exampleImage: 'https://images.unsplash.com/photo-1579783483458-83d02161294e?w=120&h=120&fit=crop' },
  { char: 'ત', roman: 'ta', sound: 't as in top', exampleWord: 'તારો', exampleMeaning: 'Star', exampleImage: 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=120&h=120&fit=crop' },
  { char: 'થ', roman: 'tha', sound: 'th as in think', exampleWord: 'થાળી', exampleMeaning: 'Plate', exampleImage: 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=120&h=120&fit=crop' },
  { char: 'દ', roman: 'da', sound: 'd as in door', exampleWord: 'દવા', exampleMeaning: 'Medicine', exampleImage: 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=120&h=120&fit=crop' },
  { char: 'ધ', roman: 'dha', sound: 'dh as in dharma', exampleWord: 'ધનુષ', exampleMeaning: 'Bow', exampleImage: 'https://images.unsplash.com/photo-1510925758641-869d353cecc7?w=120&h=120&fit=crop' },
  { char: 'ન', roman: 'na', sound: 'n as in name', exampleWord: 'નળ', exampleMeaning: 'Tap', exampleImage: 'https://images.unsplash.com/photo-1585704032915-c3400ca199e7?w=120&h=120&fit=crop' },
  { char: 'પ', roman: 'pa', sound: 'p as in pen', exampleWord: 'પતંગ', exampleMeaning: 'Kite', exampleImage: 'https://images.unsplash.com/photo-1517479149777-5f3b1511d5ad?w=120&h=120&fit=crop' },
  { char: 'ફ', roman: 'pha', sound: 'ph/f as in phone', exampleWord: 'ફળ', exampleMeaning: 'Fruit', exampleImage: 'https://images.unsplash.com/photo-1619566636858-adf3ef46400b?w=120&h=120&fit=crop' },
  { char: 'બ', roman: 'ba', sound: 'b as in ball', exampleWord: 'બકરી', exampleMeaning: 'Goat', exampleImage: 'https://images.unsplash.com/photo-1524024973431-2ad916746881?w=120&h=120&fit=crop' },
  { char: 'ભ', roman: 'bha', sound: 'bh as in abhor', exampleWord: 'ભાલુ', exampleMeaning: 'Bear', exampleImage: 'https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=120&h=120&fit=crop' },
  { char: 'મ', roman: 'ma', sound: 'm as in mother', exampleWord: 'માછલી', exampleMeaning: 'Fish', exampleImage: 'https://images.unsplash.com/photo-1524704654690-b56c05c78a00?w=120&h=120&fit=crop' },
  { char: 'ય', roman: 'ya', sound: 'y as in yes', exampleWord: 'યાત્રા', exampleMeaning: 'Journey', exampleImage: 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=120&h=120&fit=crop' },
  { char: 'ર', roman: 'ra', sound: 'r as in run', exampleWord: 'રાજા', exampleMeaning: 'King', exampleImage: 'https://images.unsplash.com/photo-1578632292335-df3abbb0d586?w=120&h=120&fit=crop' },
  { char: 'લ', roman: 'la', sound: 'l as in love', exampleWord: 'લાડુ', exampleMeaning: 'Laddu Sweet', exampleImage: 'https://images.unsplash.com/photo-1666190094553-d8cfcfb80124?w=120&h=120&fit=crop' },
  { char: 'વ', roman: 'va', sound: 'v as in van', exampleWord: 'વન', exampleMeaning: 'Forest', exampleImage: 'https://images.unsplash.com/photo-1448375240586-882707db888b?w=120&h=120&fit=crop' },
  { char: 'શ', roman: 'sha', sound: 'sh as in ship', exampleWord: 'શેર', exampleMeaning: 'Lion', exampleImage: 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=120&h=120&fit=crop' },
  { char: 'સ', roman: 'sa', sound: 's as in sun', exampleWord: 'સફરજન', exampleMeaning: 'Apple', exampleImage: 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=120&h=120&fit=crop' },
  { char: 'હ', roman: 'ha', sound: 'h as in house', exampleWord: 'હાથી', exampleMeaning: 'Elephant', exampleImage: 'https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=120&h=120&fit=crop' },
];

// Fiji Hindi Alphabet Data (Devanagari - same script as Hindi, different vocabulary)
// Fiji Hindi is spoken in Fiji and uses familiar words from the Fiji Hindi community
const FIJI_HINDI_VOWELS = [
  { char: 'अ', roman: 'a', sound: 'a as in about', exampleWord: 'अनार', exampleMeaning: 'Pomegranate', exampleImage: 'https://images.unsplash.com/photo-1541344999736-83eca272f6fc?w=120&h=120&fit=crop' },
  { char: 'आ', roman: 'aa', sound: 'aa as in father', exampleWord: 'आम', exampleMeaning: 'Mango', exampleImage: 'https://images.unsplash.com/photo-1553279768-865429fa0078?w=120&h=120&fit=crop' },
  { char: 'इ', roman: 'i', sound: 'i as in bit', exampleWord: 'इमली', exampleMeaning: 'Tamarind', exampleImage: 'https://images.unsplash.com/photo-1590502160462-58b41354f588?w=120&h=120&fit=crop' },
  { char: 'ई', roman: 'ee', sound: 'ee as in feet', exampleWord: 'ईख', exampleMeaning: 'Sugarcane', exampleImage: 'https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=120&h=120&fit=crop' },
  { char: 'उ', roman: 'u', sound: 'u as in put', exampleWord: 'उल्लू', exampleMeaning: 'Owl', exampleImage: 'https://images.unsplash.com/photo-1543549790-8b5f4a028cfb?w=120&h=120&fit=crop' },
  { char: 'ऊ', roman: 'oo', sound: 'oo as in boot', exampleWord: 'ऊन', exampleMeaning: 'Wool', exampleImage: 'https://images.unsplash.com/photo-1544967082-d9d25d867d66?w=120&h=120&fit=crop' },
  { char: 'ए', roman: 'e', sound: 'e as in bet', exampleWord: 'एक', exampleMeaning: 'One', exampleImage: 'https://images.unsplash.com/photo-1509228627152-72ae9ae6848d?w=120&h=120&fit=crop' },
  { char: 'ऐ', roman: 'ai', sound: 'ai as in bat', exampleWord: 'ऐनक', exampleMeaning: 'Glasses', exampleImage: 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=120&h=120&fit=crop' },
  { char: 'ओ', roman: 'o', sound: 'o as in go', exampleWord: 'ओखली', exampleMeaning: 'Mortar', exampleImage: 'https://images.unsplash.com/photo-1506976785307-8732e854ad03?w=120&h=120&fit=crop' },
  { char: 'औ', roman: 'au', sound: 'au as in taught', exampleWord: 'औरत', exampleMeaning: 'Woman', exampleImage: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=120&h=120&fit=crop' },
];

const FIJI_HINDI_CONSONANTS = [
  { char: 'क', roman: 'ka', sound: 'k as in kite', exampleWord: 'केला', exampleMeaning: 'Banana', exampleImage: 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=120&h=120&fit=crop' },
  { char: 'ख', roman: 'kha', sound: 'kh as in khan', exampleWord: 'खरबूजा', exampleMeaning: 'Melon', exampleImage: 'https://images.unsplash.com/photo-1571575173700-afb9492e6a50?w=120&h=120&fit=crop' },
  { char: 'ग', roman: 'ga', sound: 'g as in go', exampleWord: 'गन्ना', exampleMeaning: 'Sugarcane', exampleImage: 'https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=120&h=120&fit=crop' },
  { char: 'घ', roman: 'gha', sound: 'gh as in ghost', exampleWord: 'घर', exampleMeaning: 'House', exampleImage: 'https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=120&h=120&fit=crop' },
  { char: 'ङ', roman: 'nga', sound: 'ng as in sing', exampleWord: 'रंग', exampleMeaning: 'Color', exampleImage: 'https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=120&h=120&fit=crop' },
  { char: 'च', roman: 'cha', sound: 'ch as in chair', exampleWord: 'चावल', exampleMeaning: 'Rice', exampleImage: 'https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6?w=120&h=120&fit=crop' },
  { char: 'छ', roman: 'chha', sound: 'chh as in church hill', exampleWord: 'छाता', exampleMeaning: 'Umbrella', exampleImage: 'https://images.unsplash.com/photo-1534309466160-70b22cc6252c?w=120&h=120&fit=crop' },
  { char: 'ज', roman: 'ja', sound: 'j as in jump', exampleWord: 'जहाज़', exampleMeaning: 'Ship', exampleImage: 'https://images.unsplash.com/photo-1534343821789-89dd78d50b53?w=120&h=120&fit=crop' },
  { char: 'झ', roman: 'jha', sound: 'jh as in hedgehog', exampleWord: 'झंडा', exampleMeaning: 'Flag', exampleImage: 'https://images.unsplash.com/photo-1569974507005-6dc61f97fb5c?w=120&h=120&fit=crop' },
  { char: 'ञ', roman: 'nya', sound: 'ny as in canyon', exampleWord: 'पंख', exampleMeaning: 'Wing', exampleImage: 'https://images.unsplash.com/photo-1444464666168-49d633b86797?w=120&h=120&fit=crop' },
  { char: 'ट', roman: 'ta', sound: 't (hard)', exampleWord: 'टमाटर', exampleMeaning: 'Tomato', exampleImage: 'https://images.unsplash.com/photo-1558818498-28c1e002674f?w=120&h=120&fit=crop' },
  { char: 'ठ', roman: 'tha', sound: 'th (hard)', exampleWord: 'ठंडा', exampleMeaning: 'Cold', exampleImage: 'https://images.unsplash.com/photo-1516912481808-3406841bd33c?w=120&h=120&fit=crop' },
  { char: 'ड', roman: 'da', sound: 'd (hard)', exampleWord: 'डिब्बा', exampleMeaning: 'Box', exampleImage: 'https://images.unsplash.com/photo-1607166452427-7e4477079cb9?w=120&h=120&fit=crop' },
  { char: 'ढ', roman: 'dha', sound: 'dh (hard)', exampleWord: 'ढोल', exampleMeaning: 'Drum', exampleImage: 'https://images.unsplash.com/photo-1519892300165-cb5542fb47c7?w=120&h=120&fit=crop' },
  { char: 'ण', roman: 'na', sound: 'n (retroflex)', exampleWord: 'कण', exampleMeaning: 'Grain', exampleImage: 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=120&h=120&fit=crop' },
  { char: 'त', roman: 'ta', sound: 't as in top', exampleWord: 'तारा', exampleMeaning: 'Star', exampleImage: 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=120&h=120&fit=crop' },
  { char: 'थ', roman: 'tha', sound: 'th as in think', exampleWord: 'थाली', exampleMeaning: 'Plate', exampleImage: 'https://images.unsplash.com/photo-1544025162-d76694265947?w=120&h=120&fit=crop' },
  { char: 'द', roman: 'da', sound: 'd as in door', exampleWord: 'दूध', exampleMeaning: 'Milk', exampleImage: 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=120&h=120&fit=crop' },
  { char: 'ध', roman: 'dha', sound: 'dh as in dharma', exampleWord: 'धनुष', exampleMeaning: 'Bow', exampleImage: 'https://images.unsplash.com/photo-1533381748829-78674b3e9632?w=120&h=120&fit=crop' },
  { char: 'न', roman: 'na', sound: 'n as in name', exampleWord: 'नारियल', exampleMeaning: 'Coconut', exampleImage: 'https://images.unsplash.com/photo-1550689960-d9c8ab6f7c4f?w=120&h=120&fit=crop' },
  { char: 'प', roman: 'pa', sound: 'p as in pen', exampleWord: 'पपीता', exampleMeaning: 'Papaya', exampleImage: 'https://images.unsplash.com/photo-1517282009859-f000ec3b26fe?w=120&h=120&fit=crop' },
  { char: 'फ', roman: 'pha', sound: 'ph as in phone', exampleWord: 'फल', exampleMeaning: 'Fruit', exampleImage: 'https://images.unsplash.com/photo-1619566636858-adf3ef46400b?w=120&h=120&fit=crop' },
  { char: 'ब', roman: 'ba', sound: 'b as in ball', exampleWord: 'बकरी', exampleMeaning: 'Goat', exampleImage: 'https://images.unsplash.com/photo-1524024973431-2ad916746881?w=120&h=120&fit=crop' },
  { char: 'भ', roman: 'bha', sound: 'bh as in abhor', exampleWord: 'भालू', exampleMeaning: 'Bear', exampleImage: 'https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=120&h=120&fit=crop' },
  { char: 'म', roman: 'ma', sound: 'm as in mother', exampleWord: 'मछली', exampleMeaning: 'Fish', exampleImage: 'https://images.unsplash.com/photo-1544943910-4c1dc44aab44?w=120&h=120&fit=crop' },
  { char: 'य', roman: 'ya', sound: 'y as in yes', exampleWord: 'याम', exampleMeaning: 'Yam', exampleImage: 'https://images.unsplash.com/photo-1590165482129-1b8b27698780?w=120&h=120&fit=crop' },
  { char: 'र', roman: 'ra', sound: 'r as in run', exampleWord: 'रस्सी', exampleMeaning: 'Rope', exampleImage: 'https://images.unsplash.com/photo-1583395838144-09be6e04e84f?w=120&h=120&fit=crop' },
  { char: 'ल', roman: 'la', sound: 'l as in love', exampleWord: 'लस्सी', exampleMeaning: 'Lassi', exampleImage: 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=120&h=120&fit=crop' },
  { char: 'व', roman: 'va', sound: 'v as in van', exampleWord: 'वट', exampleMeaning: 'Banyan', exampleImage: 'https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=120&h=120&fit=crop' },
  { char: 'श', roman: 'sha', sound: 'sh as in ship', exampleWord: 'शकरकंद', exampleMeaning: 'Sweet Potato', exampleImage: 'https://images.unsplash.com/photo-1590165482129-1b8b27698780?w=120&h=120&fit=crop' },
  { char: 'ष', roman: 'sha', sound: 'sh (retroflex)', exampleWord: 'षट्कोण', exampleMeaning: 'Hexagon', exampleImage: 'https://images.unsplash.com/photo-1509228627152-72ae9ae6848d?w=120&h=120&fit=crop' },
  { char: 'स', roman: 'sa', sound: 's as in sun', exampleWord: 'समुद्र', exampleMeaning: 'Ocean', exampleImage: 'https://images.unsplash.com/photo-1505118380757-91f5f5632de0?w=120&h=120&fit=crop' },
  { char: 'ह', roman: 'ha', sound: 'h as in house', exampleWord: 'हाथी', exampleMeaning: 'Elephant', exampleImage: 'https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=120&h=120&fit=crop' },
];

export default function AlphabetPage() {
  const router = useRouter();
  const [isHydrated, setIsHydrated] = useState(false);
  const [selectedLetter, setSelectedLetter] = useState<typeof HINDI_VOWELS[0] | null>(null);
  const [activeTab, setActiveTab] = useState<'vowels' | 'consonants'>('vowels');
  const { isAuthenticated, activeChild } = useAuthStore();

  // Get current language from active child, default to Hindi
  // Handle both string and object formats from API
  const currentLanguage = activeChild?.language
    ? (typeof activeChild.language === 'string' ? activeChild.language : activeChild.language.code)
    : 'HINDI';

  // Select alphabet data based on language
  const getAlphabetData = () => {
    switch (currentLanguage) {
      case 'TAMIL':
        return { vowels: TAMIL_VOWELS, consonants: TAMIL_CONSONANTS };
      case 'PUNJABI':
        return { vowels: PUNJABI_VOWELS, consonants: PUNJABI_CONSONANTS };
      case 'GUJARATI':
        return { vowels: GUJARATI_VOWELS, consonants: GUJARATI_CONSONANTS };
      case 'FIJI_HINDI':
        return { vowels: FIJI_HINDI_VOWELS, consonants: FIJI_HINDI_CONSONANTS };
      case 'HINDI':
      default:
        return { vowels: HINDI_VOWELS, consonants: HINDI_CONSONANTS };
    }
  };
  const { vowels: VOWELS, consonants: CONSONANTS } = getAlphabetData();

  // Language-specific metadata with full Tailwind class strings (required for purge)
  const languageMetadata = {
    HINDI: {
      title: 'Hindi Alphabet',
      subtitle: 'देवनागरी वर्णमाला - Devanagari Script',
      vowelLabel: 'Vowels (स्वर)',
      consonantLabel: 'Consonants (व्यंजन)',
      totalLetters: 41,
      gradientClass: 'from-orange-50 to-red-50',
      textColorClass: 'text-orange-500',
      bgColorClass: 'bg-orange-500',
      letterGradient: 'from-orange-100 to-red-100 hover:from-orange-200 hover:to-red-200',
      connector: 'से',
    },
    TAMIL: {
      title: 'Tamil Alphabet',
      subtitle: 'தமிழ் எழுத்துக்கள் - Tamil Script',
      vowelLabel: 'Vowels (உயிர்)',
      consonantLabel: 'Consonants (மெய்)',
      totalLetters: 30,
      gradientClass: 'from-blue-50 to-indigo-50',
      textColorClass: 'text-blue-500',
      bgColorClass: 'bg-blue-500',
      letterGradient: 'from-blue-100 to-indigo-100 hover:from-blue-200 hover:to-indigo-200',
      connector: '-',
    },
    PUNJABI: {
      title: 'Punjabi Alphabet',
      subtitle: 'ਗੁਰਮੁਖੀ ਲਿਪੀ - Gurmukhi Script',
      vowelLabel: 'Vowels (ਸਵਰ)',
      consonantLabel: 'Consonants (ਵਿਅੰਜਨ)',
      totalLetters: 42,
      gradientClass: 'from-amber-50 to-orange-50',
      textColorClass: 'text-amber-500',
      bgColorClass: 'bg-amber-500',
      letterGradient: 'from-amber-100 to-orange-100 hover:from-amber-200 hover:to-orange-200',
      connector: 'ਤੋਂ',
    },
    FIJI_HINDI: {
      title: 'Fiji Hindi Alphabet',
      subtitle: 'फ़िजी हिंदी वर्णमाला - Fiji Hindi Script',
      vowelLabel: 'Vowels (स्वर)',
      consonantLabel: 'Consonants (व्यंजन)',
      totalLetters: 41,
      gradientClass: 'from-teal-50 to-cyan-50',
      textColorClass: 'text-teal-500',
      bgColorClass: 'bg-teal-500',
      letterGradient: 'from-teal-100 to-cyan-100 hover:from-teal-200 hover:to-cyan-200',
      connector: 'से',
    },
    GUJARATI: {
      title: 'Gujarati Alphabet',
      subtitle: 'ગુજરાતી લિપિ - Gujarati Script',
      vowelLabel: 'Vowels (સ્વર)',
      consonantLabel: 'Consonants (વ્યંજન)',
      totalLetters: 40,
      gradientClass: 'from-pink-50 to-rose-50',
      textColorClass: 'text-pink-500',
      bgColorClass: 'bg-pink-500',
      letterGradient: 'from-pink-100 to-rose-100 hover:from-pink-200 hover:to-rose-200',
      connector: 'થી',
    },
  };

  const metadata = languageMetadata[currentLanguage as keyof typeof languageMetadata] || languageMetadata.HINDI;

  // Audio playback hook
  const { isPlaying, isLoading, playAudio, stopAudio, error: audioError } = useAudio({
    language: currentLanguage,
    voiceStyle: 'kid_friendly',
  });

  // Sound effects hook
  const { onClick, onCorrect } = useSounds();

  // Progress tracking state
  const [viewedLetters, setViewedLetters] = useState<Set<string>>(new Set());
  const [milestones, setMilestones] = useState({ vowels: false, complete: false });
  const [showCelebration, setShowCelebration] = useState(false);

  // Quiz state
  const [showQuiz, setShowQuiz] = useState(false);
  const [quizType, setQuizType] = useState<'vowels' | 'consonants' | 'all'>('vowels');

  // Handle playing letter audio
  // Always use "letter + connector + exampleWord" pattern for clearer TTS pronunciation
  // Single letters are hard for TTS to pronounce clearly
  const handlePlayLetter = (letter: typeof VOWELS[0], e?: React.MouseEvent) => {
    if (e) {
      e.stopPropagation(); // Prevent opening modal when clicking speaker
    }
    if (isPlaying) {
      stopAudio();
    } else {
      // Always include example word for clearer pronunciation (not just premium)
      let textToSpeak = letter.char;
      if (letter.exampleWord) {
        // Use language-appropriate connector from metadata
        const connector = metadata.connector || 'से';
        if (currentLanguage === 'TAMIL') {
          // Tamil uses a different pattern: "க, உதாரணமாக கல்" (letter, for example, word)
          textToSpeak = `${letter.char}, உதாரணமாக ${letter.exampleWord}`;
        } else {
          // Hindi, Punjabi, Fiji Hindi use: "letter connector word"
          textToSpeak = `${letter.char} ${connector} ${letter.exampleWord}`;
        }
      }
      playAudio(textToSpeak);
      // Play success sound when audio plays successfully
      onCorrect();
      console.log('[Alphabet] Playing audio for letter:', letter.char, 'Text:', textToSpeak);
    }
  };

  // Handle letter tap - marks as viewed and plays click sound
  const handleLetterTap = (letter: typeof VOWELS[0]) => {
    // Play click sound
    onClick();
    console.log('[Alphabet] Letter tapped:', letter.char);

    // Mark letter as viewed
    setViewedLetters(prev => {
      const newSet = new Set(prev);
      newSet.add(letter.char);
      return newSet;
    });

    // Open the letter modal
    setSelectedLetter(letter);
  };

  // Load progress from localStorage on mount
  useEffect(() => {
    setIsHydrated(true);

    // Load viewed letters from localStorage
    const storageKey = `alphabet_progress_${currentLanguage.toLowerCase()}`;
    const savedProgress = localStorage.getItem(storageKey);
    if (savedProgress) {
      try {
        const parsedProgress = JSON.parse(savedProgress);
        setViewedLetters(new Set(parsedProgress));
        console.log('[Alphabet] Loaded progress from localStorage:', parsedProgress.length, 'letters');
      } catch (e) {
        console.error('[Alphabet] Error loading progress:', e);
      }
    }

    // Load milestones from localStorage
    const milestonesKey = `alphabet_milestones_${currentLanguage.toLowerCase()}`;
    const savedMilestones = localStorage.getItem(milestonesKey);
    if (savedMilestones) {
      try {
        const parsedMilestones = JSON.parse(savedMilestones);
        setMilestones(parsedMilestones);
        console.log('[Alphabet] Loaded milestones from localStorage:', parsedMilestones);
      } catch (e) {
        console.error('[Alphabet] Error loading milestones:', e);
      }
    }
  }, [currentLanguage]);

  // Save progress to localStorage whenever it changes
  useEffect(() => {
    if (!isHydrated) return;

    const storageKey = `alphabet_progress_${currentLanguage.toLowerCase()}`;
    localStorage.setItem(storageKey, JSON.stringify(Array.from(viewedLetters)));
    console.log('[Alphabet] Saved progress to localStorage:', viewedLetters.size, 'letters');
  }, [viewedLetters, isHydrated, currentLanguage]);

  // Save milestones to localStorage whenever they change
  useEffect(() => {
    if (!isHydrated) return;

    const milestonesKey = `alphabet_milestones_${currentLanguage.toLowerCase()}`;
    localStorage.setItem(milestonesKey, JSON.stringify(milestones));
  }, [milestones, isHydrated, currentLanguage]);

  // Milestone detection logic
  useEffect(() => {
    if (!isHydrated || viewedLetters.size === 0) return;

    const vowelChars = VOWELS.map(v => v.char);
    const viewedVowels = Array.from(viewedLetters).filter(l => vowelChars.includes(l)).length;
    const totalVowels = VOWELS.length;
    const totalLetters = metadata.totalLetters;

    // Check vowels milestone
    if (viewedVowels === totalVowels && !milestones.vowels) {
      console.log('[Alphabet] Vowels milestone reached!');
      setShowCelebration(true);
      setMilestones(prev => ({ ...prev, vowels: true }));
    }

    // Check complete milestone
    if (viewedLetters.size === totalLetters && !milestones.complete) {
      console.log('[Alphabet] Complete milestone reached!');
      setShowCelebration(true);
      setMilestones(prev => ({ ...prev, complete: true }));
    }
  }, [viewedLetters, isHydrated, VOWELS, metadata.totalLetters, milestones, currentLanguage]);

  useEffect(() => {
    if (!isHydrated) return;
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isHydrated, isAuthenticated, router]);

  if (!isHydrated || !isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading size="lg" text="Loading..." />
      </div>
    );
  }

  const letters = activeTab === 'vowels' ? VOWELS : CONSONANTS;

  return (
    <MainLayout>
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-6"
      >
        {/* Header */}
        <motion.div variants={fadeInUp} className="flex items-center gap-3">
          <Link href="anguages" className="text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{metadata.title}</h1>
            <p className="text-gray-500">{metadata.subtitle}</p>
          </div>
        </motion.div>

        {/* Progress */}
        <motion.div variants={fadeInUp}>
          <Card className={`bg-gradient-to-r ${metadata.gradientClass}`}>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">Your Progress</span>
              <span className={`text-sm ${metadata.textColorClass}`}>
                {viewedLetters.size} / {metadata.totalLetters} letters
              </span>
            </div>
            <ProgressBar value={(viewedLetters.size / metadata.totalLetters) * 100} variant="primary" />
          </Card>
        </motion.div>

        {/* Tabs */}
        <motion.div variants={fadeInUp} className="flex gap-2">
          <button
            onClick={() => setActiveTab('vowels')}
            className={`flex-1 py-3 px-4 rounded-xl font-medium transition-colors ${
              activeTab === 'vowels'
                ? `${metadata.bgColorClass} text-white`
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            {metadata.vowelLabel}
            <span className="ml-2 text-sm opacity-80">{VOWELS.length}</span>
          </button>
          <button
            onClick={() => setActiveTab('consonants')}
            className={`flex-1 py-3 px-4 rounded-xl font-medium transition-colors ${
              activeTab === 'consonants'
                ? `${metadata.bgColorClass} text-white`
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            {metadata.consonantLabel}
            <span className="ml-2 text-sm opacity-80">{CONSONANTS.length}</span>
          </button>
        </motion.div>

        {/* Selected Letter Detail */}
        {selectedLetter && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
            onClick={() => setSelectedLetter(null)}
          >
            <Card className="w-full max-w-sm bg-white" onClick={(e) => e.stopPropagation()}>
              <div className="text-center">
                <p className={`text-8xl font-bold ${metadata.textColorClass} mb-4`}>
                  {selectedLetter.char}
                </p>
                <p className="text-2xl text-gray-700 mb-2">{selectedLetter.roman}</p>
                <p className="text-gray-500 mb-2">{selectedLetter.sound}</p>

                {/* Show example word with image */}
                {selectedLetter.exampleWord && (
                  <div className="bg-gradient-to-r from-amber-50 to-yellow-50 rounded-xl px-4 py-3 mb-4">
                    {/* Example image - using Twemoji */}
                    {selectedLetter.exampleMeaning && (
                      <div className="flex justify-center mb-2">
                        <div className="w-20 h-20 rounded-lg overflow-hidden shadow-md border-2 border-amber-200 bg-amber-50 flex items-center justify-center">
                          <img
                            src={getTwemojiUrl(selectedLetter.exampleMeaning)}
                            alt={selectedLetter.exampleMeaning || selectedLetter.exampleWord}
                            className="w-14 h-14 object-contain"
                          />
                        </div>
                      </div>
                    )}
                    {/* Example text */}
                    <p className="text-lg text-amber-700 font-bold">
                      {`${selectedLetter.char} ${metadata.connector} ${selectedLetter.exampleWord}`}
                    </p>
                    {selectedLetter.exampleMeaning && (
                      <p className="text-sm text-amber-600">
                        ({selectedLetter.exampleMeaning})
                      </p>
                    )}
                  </div>
                )}

                {/* Listen to pronunciation button */}
                <div className="flex flex-col items-center gap-3 mb-4">
                  <SpeakerButton
                    isPlaying={isPlaying}
                    isLoading={isLoading}
                    onClick={() => handlePlayLetter(selectedLetter)}
                    size="lg"
                  />
                  <span className="text-sm text-gray-500">
                    {isLoading ? 'Loading...' : isPlaying ? 'Playing...' : 'Tap to hear'}
                  </span>
                  {audioError && (
                    <span className="text-xs text-red-500">{audioError}</span>
                  )}
                </div>

                <button
                  onClick={() => {
                    stopAudio();
                    setSelectedLetter(null);
                  }}
                  className={`mt-2 px-6 py-2 ${metadata.bgColorClass} text-white rounded-xl font-medium hover:opacity-90 transition-colors`}
                >
                  Close
                </button>
              </div>
            </Card>
          </motion.div>
        )}

        {/* Letters Grid */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-4">
            {activeTab === 'vowels' ? metadata.vowelLabel : metadata.consonantLabel}
          </h2>
          <div className="grid grid-cols-5 gap-2">
            {letters.map((letter, index) => (
              <motion.button
                key={letter.char}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.02 }}
                onClick={() => handleLetterTap(letter)}
                className={`relative aspect-square bg-gradient-to-br ${metadata.letterGradient} rounded-xl flex flex-col items-center justify-center transition-colors shadow-sm hover:shadow-md`}
              >
                {/* Viewed indicator */}
                {viewedLetters.has(letter.char) && (
                  <div className="absolute top-1 left-1">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                      className="w-4 h-4 text-green-500"
                    >
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clipRule="evenodd" />
                    </svg>
                  </div>
                )}
                {/* Audio indicator */}
                <div className="absolute top-1 right-1">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                    className="w-3 h-3 text-purple-400"
                  >
                    <path d="M10 3.75a.75.75 0 00-1.264-.546L4.703 7H3.167a.75.75 0 00-.7.48A6.985 6.985 0 002 10c0 .887.165 1.737.468 2.52.111.29.39.48.7.48h1.535l4.033 3.796A.75.75 0 0010 16.25V3.75zM15.95 5.05a.75.75 0 00-1.06 1.061 5.5 5.5 0 010 7.778.75.75 0 001.06 1.06 7 7 0 000-9.899z" />
                    <path d="M13.829 7.172a.75.75 0 00-1.061 1.06 2.5 2.5 0 010 3.536.75.75 0 001.06 1.06 4 4 0 000-5.656z" />
                  </svg>
                </div>
                <span className="text-2xl font-bold text-gray-800">{letter.char}</span>
                <span className="text-xs text-gray-500">{letter.roman}</span>
              </motion.button>
            ))}
          </div>
        </motion.div>

        {/* Celebration Animation */}
        <Celebration
          show={showCelebration}
          onComplete={() => setShowCelebration(false)}
          type="confetti"
        />

        {/* Quiz Section */}
        {viewedLetters.size >= VOWELS.length && (
          <motion.div variants={fadeInUp}>
            <Card className="bg-gradient-to-r from-green-50 to-teal-50 border-2 border-green-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-3xl">📝</span>
                  <div>
                    <h3 className="font-bold text-green-800">Ready for a Quiz?</h3>
                    <p className="text-sm text-green-600">Test what you&apos;ve learned!</p>
                  </div>
                </div>
                <button
                  onClick={() => {
                    setQuizType(viewedLetters.size >= VOWELS.length + CONSONANTS.length ? 'all' : 'vowels');
                    setShowQuiz(true);
                  }}
                  className="px-4 py-2 bg-green-500 text-white rounded-xl font-medium hover:bg-green-600 transition-colors"
                >
                  Start Quiz
                </button>
              </div>
            </Card>
          </motion.div>
        )}

        {/* Learning Tip */}
        <motion.div variants={fadeInUp}>
          <Card className="bg-yellow-50 border-2 border-yellow-200">
            <div className="flex items-start gap-3">
              <span className="text-2xl">🔊</span>
              <div>
                <h3 className="font-bold text-yellow-800">Listen & Learn!</h3>
                <p className="text-sm text-yellow-700 mt-1">
                  Tap any letter to see details, then tap the speaker button to hear the correct pronunciation!
                </p>
              </div>
            </div>
          </Card>
        </motion.div>
      </motion.div>

      {/* Quiz Modal */}
      {showQuiz && (
        <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <AlphabetQuiz
              letters={(quizType === 'vowels' ? VOWELS : [...VOWELS, ...CONSONANTS]).map(l => ({
                char: l.char,
                roman: l.roman,
                sound: l.sound,
                exampleWord: l.exampleWord,
              }))}
              quizType="sound-to-letter"
              language={currentLanguage}
              onComplete={(score, passed) => {
                setShowQuiz(false);
                if (passed) {
                  setShowCelebration(true);
                }
              }}
              onBack={() => setShowQuiz(false)}
            />
          </div>
        </div>
      )}
    </MainLayout>
  );
}
