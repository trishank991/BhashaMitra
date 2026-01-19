/**
 * Challenge System Types
 *
 * Viral quiz sharing - Create challenges and share via short links.
 * Anyone can play without signing up!
 */

export type ChallengeCategory =
  | 'alphabet'
  | 'vocabulary'
  | 'grammar'
  | 'numbers'
  | 'colors'
  | 'animals'
  | 'family'
  | 'food'
  | 'greetings';

export type ChallengeDifficulty = 'easy' | 'medium' | 'hard';

export type LanguageCode =
  | 'HINDI'
  | 'TAMIL'
  | 'GUJARATI'
  | 'PUNJABI'
  | 'TELUGU'
  | 'MALAYALAM'
  | 'FIJI_HINDI';

export interface ChallengeQuestion {
  id: number;
  type: 'alphabet_recognition' | 'vocabulary_to_english' | 'english_to_vocabulary';
  question: string;
  prompt: string;
  prompt_native?: string;
  romanization?: string;
  choices: string[];
  correct_index?: number; // Only present for creators, not participants
  image_url?: string;
  audio_url?: string;
  hint?: string;
}

export interface Challenge {
  id: string;
  code: string;
  title: string;
  title_native?: string;
  language: LanguageCode;
  language_name: string;
  category: ChallengeCategory;
  difficulty: ChallengeDifficulty;
  question_count: number;
  time_limit_seconds: number;
  questions: ChallengeQuestion[];
  is_active: boolean;
  total_attempts: number;
  total_completions: number;
  average_score: number;
  participant_count: number;
  expires_at?: string;
  is_expired: boolean;
  share_url: string;
  creator_name: string;
  created_at: string;
}

export interface PublicChallenge {
  id: string;
  code: string;
  title: string;
  title_native?: string;
  language: LanguageCode;
  language_name: string;
  category: ChallengeCategory;
  difficulty: ChallengeDifficulty;
  question_count: number;
  time_limit_seconds: number;
  questions: Omit<ChallengeQuestion, 'correct_index'>[]; // No answers!
  is_expired: boolean;
  creator_name: string;
}

export interface ChallengeAttempt {
  id: string;
  challenge: string;
  challenge_title: string;
  participant_name: string;
  participant_location?: string;
  score: number;
  max_score: number;
  percentage: number;
  time_taken_seconds: number;
  answers: DetailedResult[];
  is_completed: boolean;
  completed_at?: string;
  rank?: number;
  created_at: string;
}

export interface DetailedResult {
  question_id: number;
  correct: boolean;
  user_answer: number;
  correct_answer: number;
}

export interface ChallengeResult {
  score: number;
  max_score: number;
  percentage: number;
  time_taken_seconds: number;
  rank: number;
  total_participants: number;
  detailed_results: DetailedResult[];
  challenge_title: string;
  share_url: string;
}

export interface LeaderboardEntry {
  id: string;
  participant_name: string;
  participant_location?: string;
  score: number;
  max_score: number;
  percentage: number;
  time_taken_seconds: number;
  rank: number;
  completed_at: string;
}

export interface Leaderboard {
  challenge_title: string;
  challenge_code: string;
  total_participants: number;
  average_score: number;
  leaderboard: LeaderboardEntry[];
}

export interface ChallengeQuota {
  challenges_created_today: number;
  total_challenges_created: number;
  last_reset_date: string;
  can_create: boolean;
  message: string;
}

export interface CategoryOption {
  value: ChallengeCategory;
  label: string;
  item_count: number;
}

export interface CreateChallengeInput {
  title: string;
  title_native?: string;
  language: LanguageCode;
  category: ChallengeCategory;
  difficulty: ChallengeDifficulty;
  question_count: number;
  time_limit_seconds: number;
  child_id?: string;
}

export interface StartAttemptInput {
  participant_name: string;
  participant_location?: string;
}

export interface SubmitAnswersInput {
  attempt_id: string;
  answers: number[];
  time_taken_seconds: number;
}
