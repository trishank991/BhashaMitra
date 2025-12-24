import { Language, LanguageCode } from '@/types';

// API Configuration - Production default (v2)
// For local dev: set NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1 in .env.local
const PRODUCTION_API = 'https://bhashamitra.onrender.com/api/v1';
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || PRODUCTION_API;

// Supported Languages
export const SUPPORTED_LANGUAGES: Record<LanguageCode, Language> = {
  HINDI: {
    code: 'HINDI',
    name: 'Hindi',
    nativeName: 'हिन्दी',
    flag: '🇮🇳',
  },
  TAMIL: {
    code: 'TAMIL',
    name: 'Tamil',
    nativeName: 'தமிழ்',
    flag: '🇮🇳',
  },
  TELUGU: {
    code: 'TELUGU',
    name: 'Telugu',
    nativeName: 'తెలుగు',
    flag: '🇮🇳',
  },
  GUJARATI: {
    code: 'GUJARATI',
    name: 'Gujarati',
    nativeName: 'ગુજરાતી',
    flag: '🇮🇳',
  },
  PUNJABI: {
    code: 'PUNJABI',
    name: 'Punjabi',
    nativeName: 'ਪੰਜਾਬੀ',
    flag: '🇮🇳',
  },
  MALAYALAM: {
    code: 'MALAYALAM',
    name: 'Malayalam',
    nativeName: 'മലയാളം',
    flag: '🇮🇳',
  },
  BENGALI: {
    code: 'BENGALI',
    name: 'Bengali',
    nativeName: 'বাংলা',
    flag: '🇮🇳',
  },
  MARATHI: {
    code: 'MARATHI',
    name: 'Marathi',
    nativeName: 'मराठी',
    flag: '🇮🇳',
  },
  KANNADA: {
    code: 'KANNADA',
    name: 'Kannada',
    nativeName: 'ಕನ್ನಡ',
    flag: '🇮🇳',
  },
  ODIA: {
    code: 'ODIA',
    name: 'Odia',
    nativeName: 'ଓଡ଼ିଆ',
    flag: '🇮🇳',
  },
  ASSAMESE: {
    code: 'ASSAMESE',
    name: 'Assamese',
    nativeName: 'অসমীয়া',
    flag: '🇮🇳',
  },
  URDU: {
    code: 'URDU',
    name: 'Urdu',
    nativeName: 'اردو',
    flag: '🇵🇰',
  },
  FIJI_HINDI: {
    code: 'FIJI_HINDI',
    name: 'Fiji Hindi',
    nativeName: 'फ़िजी हिंदी',
    flag: '🇫🇯',
  },
};

// XP and Level Configuration
export const XP_PER_LEVEL = 100;
export const STREAK_BONUS_XP = 10;
export const STORY_COMPLETION_XP = 50;
export const WORD_LEARNED_XP = 5;
export const GAME_WIN_XP = 25;

// Level titles for gamification
export const LEVEL_TITLES: Record<number, string> = {
  1: 'Word Explorer',
  2: 'Letter Learner',
  3: 'Sound Seeker',
  4: 'Story Starter',
  5: 'Language Scout',
  6: 'Word Warrior',
  7: 'Grammar Guardian',
  8: 'Story Sage',
  9: 'Language Legend',
  10: 'Master Linguist',
};

// Peppi Messages
export const PEPPI_GREETINGS = [
  "Namaste! Ready to learn today?",
  "Hello, little learner! Let's have fun!",
  "Meow! I'm so happy to see you!",
  "Welcome back, my friend!",
  "Let's explore some amazing stories together!",
];

export const PEPPI_ENCOURAGEMENTS = [
  "You're doing great! Keep going!",
  "Wow, that was purr-fect!",
  "I knew you could do it!",
  "Amazing work! You're a star!",
  "That's the spirit! Try again!",
];

export const PEPPI_CELEBRATIONS = [
  "Hooray! You did it!",
  "Fantastic job! High-paw!",
  "You're absolutely brilliant!",
  "Gold star for you!",
  "That deserves a happy dance!",
];

// Avatar options for children
export const CHILD_AVATARS = [
  { id: 'tiger', emoji: '🐯', name: 'Tiger' },
  { id: 'elephant', emoji: '🐘', name: 'Elephant' },
  { id: 'peacock', emoji: '🦚', name: 'Peacock' },
  { id: 'lion', emoji: '🦁', name: 'Lion' },
  { id: 'monkey', emoji: '🐵', name: 'Monkey' },
  { id: 'parrot', emoji: '🦜', name: 'Parrot' },
  { id: 'butterfly', emoji: '🦋', name: 'Butterfly' },
  { id: 'lotus', emoji: '🪷', name: 'Lotus' },
];

// Difficulty levels
export const DIFFICULTY_COLORS = {
  beginner: 'bg-success-100 text-success-700',
  intermediate: 'bg-warning-100 text-warning-700',
  advanced: 'bg-error-100 text-error-700',
} as const;

// Animation variants for Framer Motion
export const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
};

export const fadeIn = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  exit: { opacity: 0 },
};

export const scaleIn = {
  initial: { opacity: 0, scale: 0.9 },
  animate: { opacity: 1, scale: 1 },
  exit: { opacity: 0, scale: 0.9 },
};

export const slideInRight = {
  initial: { opacity: 0, x: 50 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: -50 },
};

export const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1,
    },
  },
};
