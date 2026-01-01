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
  tts_provider?: 'cache_only' | 'svara' | 'sarvam' | 'google_wavenet';
  email_verified?: boolean;
  is_onboarded?: boolean;
  onboarding_completed_at?: string | null;
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
  | 'URDU'
  | 'FIJI_HINDI';

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
  password_confirm: string;
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
export type FestivalReligion = 'HINDU' | 'MUSLIM' | 'SIKH' | 'CHRISTIAN' | 'JAIN' | 'BUDDHIST';

export type FestivalActivityType =
  | 'STORY'
  | 'CRAFT'
  | 'COOKING'
  | 'SONG'
  | 'GAME'
  | 'VOCABULARY'
  | 'QUIZ'
  | 'VIDEO';

export interface Festival {
  id: string;
  name: string;
  name_native: string;
  localized_name?: string;
  religion: FestivalReligion;
  description: string;
  significance?: string;
  typical_month: number;
  is_lunar_calendar?: boolean;
  image_url?: string;
  is_active?: boolean;
  activity_count?: number;
  story_count?: number;
  stories?: Story[];
  activities?: FestivalActivity[];
}

export interface FestivalStory {
  id: string;
  festival_id: string;
  story_id: string;
  is_primary: boolean;
  story?: Story;
}

export interface FestivalActivity {
  id: string;
  festival: string;
  festival_name?: string;
  title: string;
  activity_type: FestivalActivityType;
  description: string;
  instructions: string;
  materials_needed?: string[];
  min_age: number;
  max_age: number;
  duration_minutes: number;
  difficulty_level: number;
  points_reward: number;
  image_url?: string;
  video_url?: string;
  is_active: boolean;
  is_age_appropriate?: boolean;
}

export interface FestivalProgress {
  id: string;
  child: string;
  child_name?: string;
  festival: string;
  festival_name?: string;
  activity?: string;
  activity_title?: string;
  story?: string;
  story_title?: string;
  is_completed: boolean;
  completed_at?: string;
  points_earned: number;
  notes?: string;
  created_at: string;
}

export interface FestivalProgressSummary {
  total_items: number;
  completed_items: number;
  completion_rate: number;
  total_points: number;
  festivals: {
    festival__name: string;
    total: number;
    completed: number;
  }[];
}

export interface FestivalsByReligion {
  [key: string]: {
    name: string;
    count: number;
    festivals: Festival[];
  };
}

// Parent Dashboard types
export interface ChildSummary {
  id: string;
  name: string;
  avatar: string;
  level: number;
  total_xp: number;
  streak_count: number;
  xp_this_week: number;
  recent_activity_count: number;
}

export interface ParentDashboard {
  children: ChildSummary[];
  total_family_time: number;
  badges_this_week: number;
}

export interface Activity {
  id: string;
  child_name: string;
  activity_type: 'lesson' | 'game' | 'badge';
  description: string;
  timestamp: string;
}

export interface ChildProgress {
  id: string;
  name: string;
  avatar: string;
  level: number;
  total_xp: number;
  xp_to_next_level: number;
  streak_count: number;
  longest_streak: number;
  total_lessons_completed: number;
  total_games_played: number;
  badges_earned: Badge[];
  recent_activities: Activity[];
}

export interface ChildStats {
  xp_this_week: number;
  xp_this_month: number;
  lessons_this_week: number;
  games_this_week: number;
  time_spent_minutes: number;
  favorite_activity: string;
}

// Re-export types from feature modules
export * from './offline';
export * from './family';
export * from './parent';
export * from './teacher';
export * from './mimic';
export * from './curriculum';
export * from './songs';
export * from './peppi';

export interface FamilyInfo {
  id: string;
  name: string;
  parents: Parent[];
  children: ChildProfile[];
  created_at: string;
}
