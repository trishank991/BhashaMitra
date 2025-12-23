// Song Types for L1 Curriculum

export type SongCategory = 'RHYME' | 'FOLK' | 'EDUCATIONAL' | 'FESTIVAL';

export interface Song {
  id: string;
  title_english: string;
  title_hindi: string;
  title_romanized: string;
  lyrics_hindi: string;
  lyrics_romanized: string;
  lyrics_english: string;
  age_min: number;
  age_max: number;
  level: string;
  level_code?: string;
  level_name?: string;
  duration_seconds: number;
  audio_url: string;
  video_url: string;
  category: SongCategory;
  actions: string[];
  order: number;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface SongWithProgress extends Song {
  times_played: number;
  last_played: string | null;
  is_favorite: boolean;
}

// Song category display info
export const SONG_CATEGORY_INFO: Record<SongCategory, { label: string; emoji: string; color: string }> = {
  RHYME: { label: 'Nursery Rhyme', emoji: '🎶', color: 'bg-pink-100 text-pink-600' },
  FOLK: { label: 'Folk Song', emoji: '🎵', color: 'bg-purple-100 text-purple-600' },
  EDUCATIONAL: { label: 'Learning Song', emoji: '📚', color: 'bg-blue-100 text-blue-600' },
  FESTIVAL: { label: 'Festival Song', emoji: '🎉', color: 'bg-orange-100 text-orange-600' },
};
