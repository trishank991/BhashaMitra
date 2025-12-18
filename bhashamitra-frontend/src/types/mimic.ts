/**
 * Peppi Mimic - Pronunciation Practice Types
 *
 * Kids listen to Peppi say a word, record their own pronunciation,
 * and get scored based on accuracy.
 */

import type { LanguageCode } from './index';

// Challenge categories
export type MimicCategory =
  | 'GREETING'
  | 'FAMILY'
  | 'FOOD'
  | 'NUMBERS'
  | 'COLORS'
  | 'ANIMALS'
  | 'FESTIVAL'
  | 'DAILY'
  | 'ACTIONS'
  | 'BODY';

export const MIMIC_CATEGORY_LABELS: Record<MimicCategory, string> = {
  GREETING: 'Greetings',
  FAMILY: 'Family Words',
  FOOD: 'Food & Drink',
  NUMBERS: 'Numbers',
  COLORS: 'Colors',
  ANIMALS: 'Animals',
  FESTIVAL: 'Festival Words',
  DAILY: 'Daily Words',
  ACTIONS: 'Action Words',
  BODY: 'Body Parts',
};

export const MIMIC_CATEGORY_ICONS: Record<MimicCategory, string> = {
  GREETING: '👋',
  FAMILY: '👨‍👩‍👧',
  FOOD: '🍎',
  NUMBERS: '🔢',
  COLORS: '🎨',
  ANIMALS: '🐾',
  FESTIVAL: '🎉',
  DAILY: '📅',
  ACTIONS: '🏃',
  BODY: '🖐️',
};

// Challenge difficulty levels
export type MimicDifficulty = 1 | 2 | 3;

export const MIMIC_DIFFICULTY_LABELS: Record<MimicDifficulty, string> = {
  1: 'Easy',
  2: 'Medium',
  3: 'Hard',
};

export const MIMIC_DIFFICULTY_COLORS: Record<MimicDifficulty, string> = {
  1: 'bg-green-100 text-green-800',
  2: 'bg-yellow-100 text-yellow-800',
  3: 'bg-red-100 text-red-800',
};

/**
 * A pronunciation challenge for kids to practice.
 */
export interface PeppiMimicChallenge {
  id: string;
  word: string;          // Word in native script (e.g., "नमस्ते")
  romanization: string;  // Transliteration (e.g., "Namaste")
  meaning: string;       // English meaning (e.g., "Hello")
  language: LanguageCode;
  category: MimicCategory;
  difficulty: MimicDifficulty;
  points_reward: number;
  audio_url: string;     // Peppi's pronunciation audio

  // Peppi's scripts for different outcomes
  peppi_intro?: string;
  peppi_perfect?: string;
  peppi_good?: string;
  peppi_try_again?: string;
}

/**
 * Challenge with child's progress info (from list endpoint).
 */
export interface PeppiMimicChallengeWithProgress extends PeppiMimicChallenge {
  best_stars: number;    // 0-3
  mastered: boolean;
  attempts: number;
}

/**
 * Detailed progress for a single challenge.
 */
export interface PeppiMimicChallengeProgress {
  best_score: number;
  best_stars: number;
  total_attempts: number;
  mastered: boolean;
  mastered_at: string | null;
}

/**
 * A child's pronunciation attempt.
 */
export interface PeppiMimicAttempt {
  id: string;
  challenge: string;
  challenge_word: string;
  audio_url: string;
  duration_ms: number;
  stt_transcription: string;
  stt_confidence: number;
  text_match_score: number;
  final_score: number;
  stars: number;
  points_earned: number;
  is_personal_best: boolean;
  shared_to_family: boolean;
  shared_at: string | null;
  created_at: string;
}

/**
 * Result returned after submitting an attempt.
 */
export interface PeppiMimicAttemptResult {
  attempt_id: string;
  transcription: string;
  score: number;
  stars: number;
  points_earned: number;
  is_personal_best: boolean;
  mastered: boolean;
  peppi_feedback: string;
  share_message: string;
  progress: {
    best_score: number;
    best_stars: number;
    total_attempts: number;
    total_points: number;
    mastered: boolean;
    mastered_at: string | null;
  };
}

/**
 * Overall progress summary for a child.
 */
export interface PeppiMimicProgressSummary {
  total_challenges: number;
  challenges_attempted: number;
  challenges_mastered: number;
  total_attempts: number;
  total_points: number;
  average_score: number;
  current_streak: number;
  categories: {
    category: MimicCategory;
    label: string;
    total: number;
    attempted: number;
    mastered: number;
  }[];
}

/**
 * Request payload for submitting an attempt.
 */
export interface MimicAttemptSubmitRequest {
  audio_url: string;
  duration_ms: number;
}

/**
 * Recording state for the UI.
 */
export type RecordingState = 'idle' | 'countdown' | 'recording' | 'processing' | 'complete';

/**
 * Recording result from MediaRecorder.
 */
export interface RecordingResult {
  blob: Blob;
  duration_ms: number;
  url: string;
}

/**
 * Star rating info for UI display.
 */
export interface StarRating {
  stars: number;
  label: string;
  color: string;
  emoji: string;
}

export const STAR_RATINGS: Record<number, StarRating> = {
  3: { stars: 3, label: 'Perfect!', color: 'text-yellow-500', emoji: '⭐⭐⭐' },
  2: { stars: 2, label: 'Great!', color: 'text-yellow-400', emoji: '⭐⭐' },
  1: { stars: 1, label: 'Good try!', color: 'text-gray-400', emoji: '⭐' },
  0: { stars: 0, label: 'Keep practicing!', color: 'text-gray-300', emoji: '' },
};

/**
 * Get star rating info.
 */
export function getStarRating(stars: number): StarRating {
  return STAR_RATINGS[stars] || STAR_RATINGS[0];
}

/**
 * Challenge filters for the list view.
 */
export interface MimicChallengeFilters {
  category?: MimicCategory;
  difficulty?: MimicDifficulty;
  mastered?: boolean;
}

/**
 * Peppi emotion states during mimic activity.
 */
export type PeppiMimicEmotion =
  | 'listening'
  | 'thinking'
  | 'excited'
  | 'celebrating'
  | 'encouraging'
  | 'proud';

export const PEPPI_MIMIC_EMOTIONS: Record<PeppiMimicEmotion, string> = {
  listening: '👂',
  thinking: '🤔',
  excited: '🤩',
  celebrating: '🎉',
  encouraging: '💪',
  proud: '🌟',
};
