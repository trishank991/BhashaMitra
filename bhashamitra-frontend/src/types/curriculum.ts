// Curriculum Hierarchy Types

export type ModuleType =
  | 'LISTENING'
  | 'SPEAKING'
  | 'VOCABULARY'
  | 'ALPHABET'
  | 'READING'
  | 'GRAMMAR'
  | 'STORIES'
  | 'SONGS'
  | 'GAMES'
  | 'CULTURE';

export type ContentType =
  | 'VOCABULARY_THEME'
  | 'VOCABULARY_WORD'
  | 'LETTER'
  | 'MATRA'
  | 'GRAMMAR_TOPIC'
  | 'GAME'
  | 'STORY'
  | 'SONG'
  | 'ASSESSMENT';

// Curriculum Level (L1-L10)
export interface CurriculumLevel {
  id: string;
  code: string; // L1, L2, etc.
  name_english: string;
  name_hindi: string;
  name_romanized: string;
  min_age: number;
  max_age: number;
  description: string;
  learning_objectives: string[];
  peppi_welcome: string;
  peppi_completion: string;
  emoji: string;
  theme_color: string;
  order: number;
  estimated_hours: number;
  is_active: boolean;
  module_count?: number;
  // Progress info (if child context)
  progress?: LevelProgress;
}

// Curriculum Module (within a level)
export interface CurriculumModule {
  id: string;
  level: string; // UUID of parent level
  code: string; // L1.M1, L2.M3, etc.
  name_english: string;
  name_hindi: string;
  name_romanized: string;
  module_type: ModuleType;
  description: string;
  peppi_intro: string;
  peppi_completion: string;
  emoji: string;
  order: number;
  estimated_minutes: number;
  is_active: boolean;
  lesson_count?: number;
  // Progress info (if child context)
  progress?: ModuleProgress;
}

// Lesson Type
export type LessonType = 'INTRODUCTION' | 'LEARNING' | 'PRACTICE' | 'REVIEW' | 'STORY' | 'ASSESSMENT';

// Lesson Content JSON Structure
export interface LessonContentSection {
  title: string;
  items: string[];
}

export interface LessonExercise {
  type: 'multiple_choice' | 'fill_blank' | 'matching' | 'pronunciation' | 'listen_repeat' | 'true_false';
  question: string;
  question_hindi?: string;
  options?: string[];
  correct?: string | number;
  audio_text?: string;
  blank_answer?: string;
  pairs?: { hindi: string; english: string }[];
}

export interface LessonContentJSON {
  introduction?: string;
  introduction_hindi?: string;
  sections?: LessonContentSection[];
  exercises?: LessonExercise[];
  summary?: string[];
}

// Lesson (within a module)
export interface Lesson {
  id: string;
  module: string; // UUID of parent module
  code: string; // L1.M1.LS1, etc.
  title_english: string;
  title_hindi: string;
  title_romanized: string;
  lesson_type: LessonType;
  description: string;
  peppi_intro: string;
  peppi_success: string;
  content: LessonContentJSON;
  order: number;
  estimated_minutes: number;
  points_available: number;
  mastery_threshold: number;
  is_free: boolean;
  is_active: boolean;
  contents?: LessonContent[];
  // Progress info (if child context)
  progress?: LessonProgress;
}

// Lesson Content (links lessons to content)
export interface LessonContent {
  id: string;
  lesson: string;
  content_type: ContentType;
  content_id: string;
  sequence_order: number;
  is_required: boolean;
}

// Progress Types
export interface LevelProgress {
  id: string;
  child: string;
  level: string;
  started_at: string;
  completed_at: string | null;
  modules_completed: number;
  total_points: number;
  is_complete: boolean;
}

export interface ModuleProgress {
  id: string;
  child: string;
  module: string;
  started_at: string;
  completed_at: string | null;
  lessons_completed: number;
  total_points: number;
  is_complete: boolean;
}

export interface LessonProgress {
  id: string;
  child: string;
  lesson: string;
  started_at: string;
  completed_at: string | null;
  score: number;
  attempts: number;
  best_score: number;
  is_complete: boolean;
  points_awarded?: number; // Points awarded when lesson is completed
}

// API Response types for curriculum
export interface CurriculumLevelWithProgress extends Omit<CurriculumLevel, 'progress'> {
  progress: LevelProgress | null;
  total_modules: number;
  completed_modules: number;
}

export interface CurriculumModuleWithProgress extends Omit<CurriculumModule, 'progress'> {
  progress: ModuleProgress | null;
  total_lessons: number;
  completed_lessons: number;
}

export interface LessonWithProgress extends Omit<Lesson, 'progress'> {
  progress: LessonProgress | null;
}

// Child's overall curriculum progress
export interface ChildCurriculumProgress {
  current_level: CurriculumLevel | null;
  levels_completed: number;
  total_points: number;
  current_streak: number;
  levels: CurriculumLevelWithProgress[];
}

// Teacher Character Types
export type TeacherCharacterType = 'CAT' | 'OWL';

// Teacher (Peppi for L1-L5, Gyan for L6-L10)
export interface CurriculumTeacher {
  id: string;
  name: string;
  name_hindi: string;
  character_type: TeacherCharacterType;
  breed?: string;
  personality: string;
  voice_style: string;
  avatar_url?: string;
  intro_message?: string;
  encouragement_phrases: string[];
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

// Classroom Theme Types
export type ClassroomThemeType =
  | 'GARDEN'
  | 'TREEHOUSE'
  | 'FOREST'
  | 'MEADOW'
  | 'NIGHT_SKY'
  | 'LIBRARY'
  | 'MOUNTAIN'
  | 'SPACE'
  | 'PALACE'
  | 'ROYAL_COURT';

// Classroom (themed learning environment for each level)
export interface Classroom {
  id: string;
  level: string; // UUID
  level_code?: string;
  level_name?: string;
  name: string;
  name_hindi: string;
  theme: ClassroomThemeType;
  description?: string;
  elements: string[];
  background_color: string;
  background_image_url?: string;
  unlock_animation?: string;
  ambient_sounds: string[];
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

// Classroom detail with level info
export interface ClassroomWithLevel extends Classroom {
  level_info: {
    code: string;
    name_english: string;
    name_hindi: string;
    emoji: string;
    theme_color: string;
  };
}

// Teacher info by character type
export const TEACHER_INFO: Record<TeacherCharacterType, { name: string; emoji: string; levels: string }> = {
  CAT: { name: 'Peppi', emoji: '🐱', levels: 'L1-L5' },
  OWL: { name: 'Gyan', emoji: '🦉', levels: 'L6-L10' },
};

// Classroom themes with visual info
export const CLASSROOM_THEMES: Record<ClassroomThemeType, { name: string; name_hindi: string; emoji: string; color: string }> = {
  GARDEN: { name: 'Garden', name_hindi: 'बगीचा', emoji: '🌸', color: '#90EE90' },
  TREEHOUSE: { name: 'Treehouse', name_hindi: 'पेड़ का घर', emoji: '🏡', color: '#8B7355' },
  FOREST: { name: 'Forest', name_hindi: 'वन', emoji: '🌲', color: '#228B22' },
  MEADOW: { name: 'Meadow', name_hindi: 'मैदान', emoji: '🌻', color: '#FFDB58' },
  NIGHT_SKY: { name: 'Night Sky', name_hindi: 'तारों भरा आकाश', emoji: '🌙', color: '#191970' },
  LIBRARY: { name: 'Library', name_hindi: 'पुस्तकालय', emoji: '📚', color: '#8B4513' },
  MOUNTAIN: { name: 'Mountain', name_hindi: 'पर्वत', emoji: '🏔️', color: '#4682B4' },
  SPACE: { name: 'Space', name_hindi: 'अंतरिक्ष', emoji: '🚀', color: '#000033' },
  PALACE: { name: 'Palace', name_hindi: 'महल', emoji: '💎', color: '#E6E6FA' },
  ROYAL_COURT: { name: 'Royal Court', name_hindi: 'राजदरबार', emoji: '👑', color: '#FFD700' },
};

// Letter Depth (for L1-L10 progressive learning)
export type LetterDepth = 'DEEP' | 'EXPOSURE';

export const LETTER_DEPTH_INFO: Record<LetterDepth, { label: string; description: string; color: string }> = {
  DEEP: { label: 'Deep Learning', description: 'Full mastery with writing practice', color: '#22c55e' },
  EXPOSURE: { label: 'Exposure', description: 'Introduction and recognition only', color: '#3b82f6' },
};

// Module type display info
export const MODULE_TYPE_INFO: Record<ModuleType, { label: string; emoji: string; color: string }> = {
  LISTENING: { label: 'Listening & Recognition', emoji: '👂', color: '#3b82f6' },
  SPEAKING: { label: 'Speaking & Pronunciation', emoji: '🗣️', color: '#10b981' },
  VOCABULARY: { label: 'Vocabulary Building', emoji: '📚', color: '#8b5cf6' },
  ALPHABET: { label: 'Alphabet & Letters', emoji: '🔤', color: '#f59e0b' },
  READING: { label: 'Reading Practice', emoji: '📖', color: '#ec4899' },
  GRAMMAR: { label: 'Grammar Concepts', emoji: '📝', color: '#6366f1' },
  STORIES: { label: 'Story Time', emoji: '📕', color: '#ef4444' },
  SONGS: { label: 'Songs & Rhymes', emoji: '🎵', color: '#14b8a6' },
  GAMES: { label: 'Games & Activities', emoji: '🎮', color: '#f97316' },
  CULTURE: { label: 'Cultural Learning', emoji: '🏛️', color: '#84cc16' },
};
