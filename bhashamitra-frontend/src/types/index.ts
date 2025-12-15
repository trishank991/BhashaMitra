// Subscription types
export type SubscriptionTier = 'FREE' | 'STANDARD' | 'PREMIUM';

export interface SubscriptionInfo {
  tier: SubscriptionTier;
  price: string;
  description: string;
  is_active: boolean;
  expires_at: string | null;
}

// User and Authentication types
export interface User {
  id: string;
  email: string;
  name: string;
  role: 'parent' | 'child';
  created_at: string;
  subscription_tier?: SubscriptionTier;
  subscription_expires_at?: string | null;
  subscription_info?: SubscriptionInfo;
  tts_provider?: 'cache_only' | 'svara' | 'sarvam';
}

export interface Parent extends User {
  role: 'parent';
  children: ChildProfile[];
}

export interface ChildProfile {
  id: string;
  name: string;
  age: number;
  avatar: string;
  // Language can be either a string (from API) or Language object (from frontend)
  language: LanguageCode | Language | string;
  level: number;
  xp?: number;
  streak?: number;
  badges?: Badge[];
  progress?: Progress;
  created_at: string;
  total_points?: number;
  date_of_birth?: string;
  peppi_addressing?: PeppiAddressing;
  peppi_gender?: PeppiGender;
}

// Language types
export type LanguageCode =
  | 'HINDI'
  | 'TAMIL'
  | 'TELUGU'
  | 'GUJARATI'
  | 'PUNJABI'
  | 'MALAYALAM'
  | 'BENGALI'
  | 'MARATHI'
  | 'KANNADA'
  | 'ODIA'
  | 'ASSAMESE'
  | 'URDU';

export interface Language {
  code: LanguageCode;
  name: string;
  nativeName: string;
  flag: string;
}

// Progress and Gamification
export interface Progress {
  storiesCompleted: number;
  wordsLearned: number;
  minutesPracticed: number;
  currentStreak: number;
  longestStreak: number;
  lastPracticeDate: string;
}

export interface Badge {
  id: string;
  name: string;
  description: string;
  icon: string;
  earnedAt: string;
  type: 'achievement' | 'streak' | 'milestone' | 'special';
}

export interface LeaderboardEntry {
  rank: number;
  childId: string;
  childName: string;
  avatar: string;
  xp: number;
  level: number;
}

// Story types
export interface Story {
  id: string;
  title: string;
  titleNative: string;
  description: string;
  language: LanguageCode;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  duration: number; // in minutes
  thumbnail: string;
  pages: StoryPage[];
  vocabulary: VocabularyWord[];
  isLocked: boolean;
  requiredLevel: number;
  xpReward: number;
}

export interface StoryPage {
  id: string;
  pageNumber: number;
  text: string;
  transliteration: string;
  translation: string;
  audioUrl?: string;
  imageUrl?: string;
  highlightWords: string[];
}

export interface VocabularyWord {
  id: string;
  word: string;
  transliteration: string;
  meaning: string;
  audioUrl?: string;
  exampleSentence: string;
  exampleTranslation: string;
}

// Peppi AI types
export type PeppiAddressing = 'BY_NAME' | 'CULTURAL';
export type PeppiGender = 'male' | 'female';

export interface PeppiState {
  mood: 'happy' | 'excited' | 'thinking' | 'encouraging' | 'celebrating' | 'sleepy';
  isTyping: boolean;
  currentMessage: string | null;
}

export interface PeppiMessage {
  id: string;
  type: 'greeting' | 'hint' | 'encouragement' | 'correction' | 'celebration' | 'explanation';
  text: string;
  timestamp: Date;
}

// Game types
export interface Game {
  id: string;
  name: string;
  description: string;
  type: 'word-match' | 'pronunciation' | 'fill-blank' | 'listen-write' | 'picture-word';
  difficulty: 'easy' | 'medium' | 'hard';
  xpReward: number;
  thumbnail: string;
}

export interface GameSession {
  gameId: string;
  startTime: Date;
  endTime?: Date;
  score: number;
  correctAnswers: number;
  totalQuestions: number;
  xpEarned: number;
}

// API Response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  results: T[];
  count: number;
  next: string | null;
  previous: string | null;
}

// Auth types
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  name: string;
  role: 'parent';
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

// TTS types
export interface TTSRequest {
  text: string;
  language: LanguageCode;
}

export interface TTSResponse {
  audio_url: string;
  cached: boolean;
  generation_time_ms: number;
}

// Festival types
export interface Festival {
  id: string;
  name: string;
  name_native: string;
  religion: 'HINDU' | 'MUSLIM' | 'SIKH' | 'CHRISTIAN' | 'JAIN' | 'BUDDHIST';
  description: string;
  typical_month: number;
  stories?: Story[];
}

export interface FestivalStory {
  id: string;
  festival_id: string;
  story_id: string;
  is_primary: boolean;
  story?: Story;
}
