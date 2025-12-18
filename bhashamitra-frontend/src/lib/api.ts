import { API_BASE_URL } from './constants';
import {
  ApiResponse,
  LoginCredentials,
  RegisterData,
  User,
  ChildProfile,
  Story,
  PaginatedResponse,
  TTSRequest,
  TTSResponse,
  LanguageCode,
  Festival,
  FestivalActivity,
  FestivalProgress,
  FestivalProgressSummary,
  FestivalsByReligion,
  FestivalReligion,
  PeppiGender,
  PeppiAddressing,
  // Mimic types
  PeppiMimicChallenge,
  PeppiMimicChallengeWithProgress,
  PeppiMimicAttemptResult,
  PeppiMimicProgressSummary,
  MimicAttemptSubmitRequest,
  MimicCategory,
  MimicDifficulty,
  MimicChallengeFilters
} from '@/types';

// Response types matching backend
interface LoginResponse {
  data: {
    user: {
      id: string;
      email: string;
      name: string;
      role: string;
      avatar_url: string | null;
      created_at: string;
      subscription_tier?: string;
      subscription_expires_at?: string | null;
      subscription_info?: Record<string, unknown>;
      tts_provider?: string;
    };
    session: {
      access_token: string;
      refresh_token: string;
    };
  };
}

interface RegisterResponse {
  data: {
    user: {
      id: string;
      email: string;
      name: string;
      role: string;
      subscription_tier?: string;
      subscription_expires_at?: string | null;
      subscription_info?: Record<string, unknown>;
      tts_provider?: string;
    };
    session: {
      access_token: string;
      refresh_token: string;
    };
  };
}

class ApiClient {
  private baseUrl: string;
  private accessToken: string | null = null;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  setAccessToken(token: string | null) {
    console.log('[api] setAccessToken called with:', token ? 'TOKEN_SET' : 'NULL');
    this.accessToken = token;
  }

  getAccessToken(): string | null {
    return this.accessToken;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseUrl}${endpoint}`;

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      const data = await response.json();

      if (!response.ok) {
        return {
          success: false,
          error: data.detail || data.message || data.error || 'An error occurred',
        };
      }

      return {
        success: true,
        data,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Network error',
      };
    }
  }

  // Auth endpoints - using /auth/ prefix
  async login(credentials: LoginCredentials): Promise<ApiResponse<LoginResponse>> {
    return this.request<LoginResponse>('/auth/login/', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  }

  async register(data: RegisterData): Promise<ApiResponse<RegisterResponse>> {
    return this.request<RegisterResponse>('/auth/register/', {
      method: 'POST',
      body: JSON.stringify({
        email: data.email,
        password: data.password,
        name: data.name,
      }),
    });
  }

  async refreshToken(refreshToken: string): Promise<ApiResponse<{ access: string }>> {
    return this.request<{ access: string }>('/auth/refresh/', {
      method: 'POST',
      body: JSON.stringify({ refresh: refreshToken }),
    });
  }

  async getProfile(): Promise<ApiResponse<User>> {
    return this.request<User>('/auth/me/');
  }

  // Children endpoints
  async getChildren(): Promise<ApiResponse<ChildProfile[]>> {
    // API returns paginated response {next, previous, results}
    const response = await this.request<{ results: ChildProfile[] }>('/children/');
    if (response.success && response.data) {
      return {
        success: true,
        data: response.data.results || [],
      };
    }
    return {
      success: response.success,
      error: response.error,
      data: [],
    };
  }

  async createChild(data: Partial<ChildProfile>): Promise<ApiResponse<ChildProfile>> {
    return this.request<ChildProfile>('/children/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateChild(id: string, data: Partial<ChildProfile>): Promise<ApiResponse<ChildProfile>> {
    return this.request<ChildProfile>(`/children/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  async deleteChild(id: string): Promise<ApiResponse<void>> {
    return this.request<void>(`/children/${id}/`, {
      method: 'DELETE',
    });
  }

  // Stories endpoints
  async getStories(language?: LanguageCode, page?: number): Promise<ApiResponse<PaginatedResponse<Story>>> {
    const params = new URLSearchParams();
    if (language) params.append('language', language);
    if (page) params.append('page', page.toString());

    const queryString = params.toString();
    // API returns { data: [...], meta: {...} } format
    const response = await this.request<{ data: Story[]; meta: { total: number } }>(`/stories/${queryString ? `?${queryString}` : ''}`);
    if (response.success && response.data) {
      // Transform to PaginatedResponse format expected by frontend
      return {
        success: true,
        data: {
          results: response.data.data || [],
          count: response.data.meta?.total || 0,
          next: null,
          previous: null,
        },
      };
    }
    return {
      success: false,
      error: response.error,
      data: { results: [], count: 0, next: null, previous: null },
    };
  }

  async getStory(id: string): Promise<ApiResponse<Story>> {
    return this.request<Story>(`/stories/${id}/`);
  }

  async markStoryComplete(id: string, childId: string): Promise<ApiResponse<{ xp_earned: number }>> {
    return this.request<{ xp_earned: number }>(`/stories/${id}/complete/`, {
      method: 'POST',
      body: JSON.stringify({ child_id: childId }),
    });
  }

  // TTS endpoints
  async textToSpeech(request: TTSRequest): Promise<ApiResponse<TTSResponse>> {
    return this.request<TTSResponse>('/speech/tts/', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Get TTS audio as a Blob for direct playback
   * Uses kid-friendly voices powered by Indic Parler-TTS
   */
  async getAudio(
    text: string,
    language: string = 'HINDI',
    voiceStyle: 'kid_friendly' | 'calm_story' | 'enthusiastic' | 'male_teacher' = 'kid_friendly'
  ): Promise<{ success: boolean; audioBlob?: Blob; audioUrl?: string; error?: string }> {
    const url = `${this.baseUrl}/speech/tts/`;

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          text,
          language,
          voice_style: voiceStyle,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        return {
          success: false,
          error: errorData.detail || 'Failed to generate audio',
        };
      }

      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);

      return {
        success: true,
        audioBlob,
        audioUrl,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Network error',
      };
    }
  }

  // Progress endpoints
  async getProgress(childId: string): Promise<ApiResponse<ChildProfile['progress']>> {
    return this.request<ChildProfile['progress']>(`/children/${childId}/progress/`);
  }

  async updateProgress(childId: string, data: Partial<ChildProfile['progress']>): Promise<ApiResponse<ChildProfile['progress']>> {
    return this.request<ChildProfile['progress']>(`/children/${childId}/progress/`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  // Leaderboard
  async getLeaderboard(language?: LanguageCode): Promise<ApiResponse<{ rank: number; childId: string; childName: string; avatar: string; xp: number; level: number }[]>> {
    const params = language ? `?language=${language}` : '';
    return this.request(`/leaderboard/${params}`);
  }

  // ========================================
  // CURRICULUM ENDPOINTS
  // ========================================

  // Vocabulary endpoints
  async getVocabularyThemes(childId: string): Promise<ApiResponse<VocabularyTheme[]>> {
    // API returns { data: [...] } format
    const response = await this.request<{ data: VocabularyTheme[] }>(`/children/${childId}/curriculum/vocabulary/themes/`);
    if (response.success && response.data) {
      return { success: true, data: response.data.data || [] };
    }
    return { success: false, error: response.error, data: [] };
  }

  async getThemeWords(childId: string, themeId: string): Promise<ApiResponse<VocabularyWord[]>> {
    const response = await this.request<{ data: VocabularyWord[] }>(`/children/${childId}/curriculum/vocabulary/themes/${themeId}/words/`);
    if (response.success && response.data) {
      return { success: true, data: response.data.data || [] };
    }
    return { success: false, error: response.error, data: [] };
  }

  /**
   * Get vocabulary words for games - fetches from the first available theme
   * Returns words in a format ready for game use
   */
  async getGameVocabulary(childId: string, limit: number = 10): Promise<ApiResponse<GameWord[]>> {
    // First get themes
    const themesRes = await this.getVocabularyThemes(childId);
    if (!themesRes.success || !themesRes.data || themesRes.data.length === 0) {
      return { success: false, error: 'No vocabulary themes found', data: [] };
    }

    // Get words from the first theme (usually Family or Colors - beginner friendly)
    const firstTheme = themesRes.data[0];
    const wordsRes = await this.getThemeWords(childId, firstTheme.id);

    if (!wordsRes.success || !wordsRes.data) {
      return { success: false, error: 'No words found', data: [] };
    }

    // Transform to game format
    const gameWords: GameWord[] = wordsRes.data.slice(0, limit).map(w => ({
      word: w.word,
      romanized: w.romanization,
      english: w.translation,
      audioUrl: w.pronunciation_audio_url,
    }));

    return { success: true, data: gameWords };
  }

  async getFlashcardsDue(childId: string, limit?: number): Promise<ApiResponse<Flashcard[]>> {
    const params = limit ? `?limit=${limit}` : '';
    return this.request<Flashcard[]>(`/children/${childId}/curriculum/vocabulary/flashcards/due/${params}`);
  }

  async reviewFlashcard(childId: string, wordId: string, quality: number): Promise<ApiResponse<FlashcardReviewResult>> {
    return this.request<FlashcardReviewResult>(`/children/${childId}/curriculum/vocabulary/flashcards/review/`, {
      method: 'POST',
      body: JSON.stringify({ word_id: wordId, quality }),
    });
  }

  // Alphabet/Script endpoints
  async getScripts(childId: string): Promise<ApiResponse<Script[]>> {
    return this.request<Script[]>(`/children/${childId}/curriculum/alphabet/scripts/`);
  }

  async getScriptLetters(childId: string, scriptId: string): Promise<ApiResponse<Letter[]>> {
    return this.request<Letter[]>(`/children/${childId}/curriculum/alphabet/scripts/${scriptId}/letters/`);
  }

  async getAlphabetProgress(childId: string): Promise<ApiResponse<AlphabetProgress>> {
    return this.request<AlphabetProgress>(`/children/${childId}/curriculum/alphabet/progress/`);
  }

  // Grammar endpoints
  async getGrammarTopics(childId: string): Promise<ApiResponse<GrammarTopic[]>> {
    // API returns { data: [...] } format
    const response = await this.request<{ data: GrammarTopic[] }>(`/children/${childId}/curriculum/grammar/topics/`);
    if (response.success && response.data) {
      return { success: true, data: response.data.data || [] };
    }
    return { success: false, error: response.error, data: [] };
  }

  async getTopicRules(childId: string, topicId: string): Promise<ApiResponse<GrammarRule[]>> {
    const response = await this.request<{ data: GrammarRule[] }>(`/children/${childId}/curriculum/grammar/topics/${topicId}/rules/`);
    if (response.success && response.data) {
      return { success: true, data: response.data.data || [] };
    }
    return { success: false, error: response.error, data: [] };
  }

  async getGrammarExercises(childId: string, topicId: string): Promise<ApiResponse<GrammarExercise[]>> {
    return this.request<GrammarExercise[]>(`/children/${childId}/curriculum/grammar/topics/${topicId}/exercises/`);
  }

  async submitGrammarExercise(childId: string, exerciseId: string, answer: string): Promise<ApiResponse<ExerciseResult>> {
    return this.request<ExerciseResult>(`/children/${childId}/curriculum/grammar/exercises/${exerciseId}/submit/`, {
      method: 'POST',
      body: JSON.stringify({ answer }),
    });
  }

  // ========================================
  // FESTIVAL ENDPOINTS
  // ========================================

  async getFestivals(params?: {
    religion?: FestivalReligion;
    month?: number;
    language?: LanguageCode;
  }): Promise<ApiResponse<Festival[]>> {
    const queryParams = new URLSearchParams();
    if (params?.religion) queryParams.append('religion', params.religion);
    if (params?.month) queryParams.append('month', params.month.toString());
    if (params?.language) queryParams.append('language', params.language);

    const queryString = queryParams.toString();
    const response = await this.request<Festival[]>(`/festivals/festivals/${queryString ? `?${queryString}` : ''}`);
    if (response.success && response.data) {
      return { success: true, data: response.data || [] };
    }
    return { success: false, error: response.error, data: [] };
  }

  async getFestival(id: string, language?: LanguageCode): Promise<ApiResponse<Festival>> {
    const params = language ? `?language=${language}` : '';
    return this.request<Festival>(`/festivals/festivals/${id}/${params}`);
  }

  async getUpcomingFestivals(): Promise<ApiResponse<Festival[]>> {
    const response = await this.request<Festival[]>('/festivals/festivals/upcoming/');
    if (response.success && response.data) {
      return { success: true, data: response.data || [] };
    }
    return { success: false, error: response.error, data: [] };
  }

  async getFestivalsByReligion(): Promise<ApiResponse<FestivalsByReligion>> {
    return this.request<FestivalsByReligion>('/festivals/festivals/by-religion/');
  }

  async getFestivalStories(festivalId: string): Promise<ApiResponse<Story[]>> {
    const response = await this.request<Story[]>(`/festivals/festivals/${festivalId}/stories/`);
    if (response.success && response.data) {
      return { success: true, data: response.data || [] };
    }
    return { success: false, error: response.error, data: [] };
  }

  async getFestivalActivities(
    festivalId: string,
    params?: { age?: number; type?: string }
  ): Promise<ApiResponse<FestivalActivity[]>> {
    const queryParams = new URLSearchParams();
    if (params?.age) queryParams.append('age', params.age.toString());
    if (params?.type) queryParams.append('type', params.type);

    const queryString = queryParams.toString();
    const response = await this.request<FestivalActivity[]>(
      `/festivals/festivals/${festivalId}/activities/${queryString ? `?${queryString}` : ''}`
    );
    if (response.success && response.data) {
      return { success: true, data: response.data || [] };
    }
    return { success: false, error: response.error, data: [] };
  }

  // ========================================
  // FESTIVAL ACTIVITY ENDPOINTS
  // ========================================

  async getAllFestivalActivities(params?: {
    festival?: string;
    type?: string;
    age?: number;
  }): Promise<ApiResponse<FestivalActivity[]>> {
    const queryParams = new URLSearchParams();
    if (params?.festival) queryParams.append('festival', params.festival);
    if (params?.type) queryParams.append('type', params.type);
    if (params?.age) queryParams.append('age', params.age.toString());

    const queryString = queryParams.toString();
    const response = await this.request<FestivalActivity[]>(
      `/festivals/festival-activities/${queryString ? `?${queryString}` : ''}`
    );
    if (response.success && response.data) {
      return { success: true, data: response.data || [] };
    }
    return { success: false, error: response.error, data: [] };
  }

  async getFestivalActivity(id: string): Promise<ApiResponse<FestivalActivity>> {
    return this.request<FestivalActivity>(`/festivals/festival-activities/${id}/`);
  }

  // ========================================
  // FESTIVAL PROGRESS ENDPOINTS
  // ========================================

  async getFestivalProgress(params?: {
    child?: string;
    festival?: string;
    completed?: boolean;
  }): Promise<ApiResponse<FestivalProgress[]>> {
    const queryParams = new URLSearchParams();
    if (params?.child) queryParams.append('child', params.child);
    if (params?.festival) queryParams.append('festival', params.festival);
    if (params?.completed !== undefined) queryParams.append('completed', params.completed.toString());

    const queryString = queryParams.toString();
    const response = await this.request<FestivalProgress[]>(
      `/festivals/festival-progress/${queryString ? `?${queryString}` : ''}`
    );
    if (response.success && response.data) {
      return { success: true, data: response.data || [] };
    }
    return { success: false, error: response.error, data: [] };
  }

  async createFestivalProgress(data: {
    child: string;
    festival: string;
    activity?: string;
    story?: string;
  }): Promise<ApiResponse<FestivalProgress>> {
    return this.request<FestivalProgress>('/festivals/festival-progress/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async completeFestivalProgress(progressId: string): Promise<ApiResponse<{
    message: string;
    points_earned: number;
    progress: FestivalProgress;
  }>> {
    return this.request(`/festivals/festival-progress/${progressId}/complete/`, {
      method: 'POST',
    });
  }

  async getFestivalProgressSummary(childId: string): Promise<ApiResponse<FestivalProgressSummary>> {
    return this.request<FestivalProgressSummary>(`/festivals/festival-progress/summary/?child=${childId}`);
  }

  // ========================================
  // PEPPI NARRATION ENDPOINTS
  // ========================================

  async getPeppiNarration(storyId: string, language: string, gender: PeppiGender): Promise<ApiResponse<{ audio_url: string; cached: boolean }>> {
    return this.request<{ audio_url: string; cached: boolean }>(`/peppi/narrate/story/${storyId}/?language=${language}&gender=${gender}`);
  }

  async generatePeppiNarration(text: string, language: string, gender: PeppiGender): Promise<ApiResponse<{ audio_url: string }>> {
    return this.request<{ audio_url: string }>('/peppi/narrate/', {
      method: 'POST',
      body: JSON.stringify({ text, language, gender }),
    });
  }

  // ========================================
  // CHILD PEPPI PREFERENCES
  // ========================================

  async updateChildPeppiPreference(
    childId: string,
    data: { peppi_addressing: PeppiAddressing; peppi_gender: PeppiGender }
  ): Promise<ApiResponse<ChildProfile>> {
    return this.request<ChildProfile>(`/children/${childId}/`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  // ========================================
  // PEPPI MIMIC ENDPOINTS
  // ========================================

  /**
   * Get list of mimic challenges with child's progress.
   * @param childId Child UUID
   * @param filters Optional filters for category, difficulty, mastered status
   */
  async getMimicChallenges(
    childId: string,
    filters?: MimicChallengeFilters
  ): Promise<ApiResponse<PeppiMimicChallengeWithProgress[]>> {
    const params = new URLSearchParams();
    if (filters?.category) params.append('category', filters.category);
    if (filters?.difficulty) params.append('difficulty', filters.difficulty.toString());
    if (filters?.mastered !== undefined) params.append('mastered', filters.mastered.toString());

    const queryString = params.toString();
    const response = await this.request<PeppiMimicChallengeWithProgress[]>(
      `/children/${childId}/mimic/challenges/${queryString ? `?${queryString}` : ''}`
    );
    if (response.success && response.data) {
      return { success: true, data: response.data || [] };
    }
    return { success: false, error: response.error, data: [] };
  }

  /**
   * Get a single challenge with full details and Peppi scripts.
   * @param childId Child UUID
   * @param challengeId Challenge UUID
   */
  async getMimicChallenge(
    childId: string,
    challengeId: string
  ): Promise<ApiResponse<PeppiMimicChallenge & { progress: { best_score: number; best_stars: number; total_attempts: number; mastered: boolean; mastered_at: string | null } }>> {
    return this.request(`/children/${childId}/mimic/challenges/${challengeId}/`);
  }

  /**
   * Submit a pronunciation attempt for scoring.
   * @param childId Child UUID
   * @param challengeId Challenge UUID
   * @param data Audio URL and duration
   */
  async submitMimicAttempt(
    childId: string,
    challengeId: string,
    data: MimicAttemptSubmitRequest
  ): Promise<ApiResponse<PeppiMimicAttemptResult>> {
    return this.request<PeppiMimicAttemptResult>(
      `/children/${childId}/mimic/challenges/${challengeId}/attempt/`,
      {
        method: 'POST',
        body: JSON.stringify(data),
      }
    );
  }

  /**
   * Get overall mimic progress summary for a child.
   * @param childId Child UUID
   */
  async getMimicProgress(
    childId: string
  ): Promise<ApiResponse<PeppiMimicProgressSummary>> {
    return this.request<PeppiMimicProgressSummary>(`/children/${childId}/mimic/progress/`);
  }

  /**
   * Mark an attempt as shared to family.
   * @param childId Child UUID
   * @param attemptId Attempt UUID
   */
  async shareMimicAttempt(
    childId: string,
    attemptId: string
  ): Promise<ApiResponse<{ success: boolean; shared_at: string }>> {
    return this.request(`/children/${childId}/mimic/attempts/${attemptId}/share/`, {
      method: 'PATCH',
      body: JSON.stringify({ shared_to_family: true }),
    });
  }

  /**
   * Upload audio recording for mimic attempt.
   * Uses FormData for file upload.
   * Returns the URL of the uploaded audio.
   */
  async uploadMimicAudio(
    childId: string,
    audioBlob: Blob,
    filename: string = 'recording.webm'
  ): Promise<ApiResponse<{ audio_url: string }>> {
    const formData = new FormData();
    formData.append('audio', audioBlob, filename);
    formData.append('child_id', childId);

    const url = `${this.baseUrl}/speech/upload-audio/`;
    const headers: Record<string, string> = {};
    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers,
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        return {
          success: false,
          error: data.detail || data.message || 'Failed to upload audio',
        };
      }

      return {
        success: true,
        data,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Network error',
      };
    }
  }
}

// Curriculum Types
export interface VocabularyTheme {
  id: string;
  name: string;
  name_native: string;
  description: string;
  icon: string;
  level: number;
  word_count: number;
  progress?: {
    words_started: number;
    words_mastered: number;
    words_due: number;
    progress_percentage: number;
  };
}

export interface VocabularyWord {
  id: string;
  word: string;
  romanization: string;
  translation: string;
  part_of_speech: string;
  gender: string;
  example_sentence: string;
  pronunciation_audio_url?: string;
  image_url?: string;
}

export interface Flashcard {
  word_id: string;
  word: string;
  romanization: string;
  translation: string;
  part_of_speech: string;
  gender: string;
  pronunciation_audio_url?: string;
  is_new: boolean;
}

export interface FlashcardReviewResult {
  success: boolean;
  next_review: string;
  interval_days: number;
}

export interface Script {
  id: string;
  language: string;
  name: string;
  name_native: string;
  description: string;
  total_letters: number;
}

export interface Letter {
  id: string;
  character: string;
  romanization: string;
  ipa: string;
  category: string;
  example_word: string;
  example_word_translation: string;
  audio_url?: string;
  pronunciation_guide: string;
}

export interface AlphabetProgress {
  total_letters: number;
  letters_mastered: number;
  progress_percentage: number;
  next_letters: Letter[];
}

export interface GrammarTopic {
  id: string;
  name: string;
  name_native: string;
  description: string;
  level: number;
  rules_count?: number;
  progress?: {
    exercises_attempted: number;
    exercises_correct: number;
    accuracy: number;
    mastered: boolean;
  };
}

export interface GrammarRule {
  id: string;
  title: string;
  explanation: string;
  formula?: string;
  examples: string[];
  tips?: string;
}

export interface GrammarExercise {
  id: string;
  exercise_type: string;
  question: string;
  options?: string[];
  hint?: string;
  difficulty: number;
  points: number;
}

export interface ExerciseResult {
  is_correct: boolean;
  correct_answer: string;
  explanation: string;
  points_earned: number;
}

export interface GameWord {
  word: string;
  romanized: string;
  english: string;
  audioUrl?: string;
}

export const api = new ApiClient(API_BASE_URL);
export default api;
