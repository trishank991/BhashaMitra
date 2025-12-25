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
  MimicChallengeFilters,
  // Curriculum types
  CurriculumLevel,
  CurriculumModule,
  Lesson,
  LevelProgress,
  ModuleProgress,
  LessonProgress,
  CurriculumLevelWithProgress,
  CurriculumModuleWithProgress,
  LessonWithProgress,
  ChildCurriculumProgress,
  // Song types
  Song,
  // Peppi AI types
  PeppiContext,
  PeppiGreeting,
  PeppiTeaching,
  PeppiFeedback,
  // Peppi Chat types
  PeppiChatMode,
  PeppiConversation,
  PeppiConversationListItem,
  PeppiChatMessage,
  StartConversationRequest,
  StartConversationResponse,
  SendMessageRequest,
  SendMessageResponse,
  ConversationHistoryResponse,
  PeppiChatStatusResponse,
  SubmitEscalationRequest,
  SubmitEscalationResponse,
  // Teacher & Classroom types
  CurriculumTeacher,
  TeacherCharacterType,
  Classroom,
  ClassroomWithLevel,
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
    // Clear any existing token before login to avoid JWT validation errors
    const previousToken = this.accessToken;
    this.accessToken = null;

    const result = await this.request<LoginResponse>('/auth/login/', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });

    // Restore token only if login failed (in case user wants to retry)
    if (!result.success) {
      this.accessToken = previousToken;
    }

    return result;
  }

  async register(data: RegisterData): Promise<ApiResponse<RegisterResponse>> {
    // Clear any existing token before register to avoid JWT validation errors
    const previousToken = this.accessToken;
    this.accessToken = null;

    const result = await this.request<RegisterResponse>('/auth/register/', {
      method: 'POST',
      body: JSON.stringify({
        email: data.email,
        password: data.password,
        name: data.name,
      }),
    });

    // Restore token only if register failed
    if (!result.success) {
      this.accessToken = previousToken;
    }

    return result;
  }

  async refreshToken(refreshToken: string): Promise<ApiResponse<{ access: string }>> {
    return this.request<{ access: string }>('/auth/refresh/', {
      method: 'POST',
      body: JSON.stringify({ refresh: refreshToken }),
    });
  }

  // Email verification endpoints
  async verifyEmail(token: string): Promise<ApiResponse<{ meta: { message: string }; data: { email: string } }>> {
    return this.request('/auth/verify-email/', {
      method: 'POST',
      body: JSON.stringify({ token }),
    });
  }

  async resendVerification(email: string): Promise<ApiResponse<{ meta: { message: string } }>> {
    return this.request('/auth/resend-verification/', {
      method: 'POST',
      body: JSON.stringify({ email }),
    });
  }

  // Password reset endpoints
  async requestPasswordReset(email: string): Promise<ApiResponse<{ meta: { message: string } }>> {
    return this.request('/auth/password-reset/', {
      method: 'POST',
      body: JSON.stringify({ email }),
    });
  }

  async resetPassword(token: string, password: string, passwordConfirm: string): Promise<ApiResponse<{ meta: { message: string } }>> {
    return this.request('/auth/password-reset/confirm/', {
      method: 'POST',
      body: JSON.stringify({ token, password, password_confirm: passwordConfirm }),
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
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const response = await this.request<{ data: any[]; meta: { total: number } }>(`/stories/${queryString ? `?${queryString}` : ''}`);
    if (response.success && response.data) {
      // Transform backend story format to frontend Story type
      // Use arrow function to preserve 'this' binding
      const transformedStories = (response.data.data || []).map((story) => this.transformStory(story));
      return {
        success: true,
        data: {
          results: transformedStories,
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
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const response = await this.request<{ data: any }>(`/stories/${id}/`);
    if (response.success && response.data && response.data.data) {
      return {
        success: true,
        data: this.transformStory(response.data.data),
      };
    }
    return {
      success: false,
      error: response.error,
    };
  }

  // Transform backend story format to frontend Story type
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  private transformStory(backendStory: any): Story {
    // Map backend fields to frontend Story interface
    // Backend: title (English), title_hindi (Hindi), title_romanized
    // Frontend: title (main display), titleNative (native script)
    return {
      id: backendStory.id,
      // Use title_hindi as main title for Hindi stories, fallback to title
      title: backendStory.title_hindi || backendStory.title || '',
      // titleNative should show the Hindi script version
      titleNative: backendStory.title_hindi || backendStory.title || '',
      description: backendStory.synopsis || backendStory.moral_english || '',
      language: backendStory.language as LanguageCode,
      difficulty: this.mapLevelToDifficulty(backendStory.level),
      duration: backendStory.estimated_minutes || 3,
      thumbnail: backendStory.cover_image_url || '',
      pages: (backendStory.pages || []).map((page) => this.transformStoryPage(page)),
      vocabulary: (backendStory.vocabulary || []).map((vocab) => this.transformVocabularyWord(vocab)),
      isLocked: false,
      requiredLevel: backendStory.level || 1,
      xpReward: backendStory.xp_reward || 10,
    };
  }

  // Transform backend story page to frontend StoryPage
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  private transformStoryPage(page: any): import('@/types').StoryPage {
    return {
      id: page.id || `page-${page.page_number}`,
      pageNumber: page.page_number,
      text: page.text_hindi || page.text_content || '',
      transliteration: page.text_romanized || '',
      translation: page.text_content || '',
      audioUrl: page.audio_url || undefined,
      imageUrl: page.image_url || undefined,
      highlightWords: page.highlight_words || [],
    };
  }

  // Transform backend vocabulary to frontend VocabularyWord
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  private transformVocabularyWord(vocab: any): import('@/types').VocabularyWord {
    return {
      id: vocab.id || vocab.word_hindi,
      word: vocab.word_hindi || '',
      transliteration: vocab.word_transliteration || '',
      meaning: vocab.word_english || '',
      audioUrl: vocab.audio_url || undefined,
      exampleSentence: vocab.example_hindi || '',
      exampleTranslation: vocab.example_english || '',
    };
  }

  // Map story level (1-5) to difficulty
  private mapLevelToDifficulty(level: number): 'beginner' | 'intermediate' | 'advanced' {
    if (level <= 2) return 'beginner';
    if (level <= 4) return 'intermediate';
    return 'advanced';
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
  async getVocabularyThemes(childId: string, language?: string): Promise<ApiResponse<VocabularyTheme[]>> {
    // API returns { data: [...] } format
    const params = language ? `?language=${language}` : '';
    const response = await this.request<{ data: VocabularyTheme[] }>(`/children/${childId}/curriculum/vocabulary/themes/${params}`);
    if (response.success && response.data) {
      return { success: true, data: response.data.data || [] };
    }
    return { success: false, error: response.error, data: [] };
  }

  async getThemeWords(childId: string, themeId: string, language?: string): Promise<ApiResponse<VocabularyWord[]>> {
    const params = language ? `?language=${language}` : '';
    const response = await this.request<{ data: VocabularyWord[] }>(`/children/${childId}/curriculum/vocabulary/themes/${themeId}/words/${params}`);
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
    // API returns { data: [...] } format
    const response = await this.request<{ data: Script[] }>(`/children/${childId}/curriculum/alphabet/scripts/`);
    if (response.success && response.data) {
      return { success: true, data: response.data.data || [] };
    }
    return { success: false, error: response.error, data: [] };
  }

  async getScriptLetters(childId: string, scriptId: string): Promise<ApiResponse<Letter[]>> {
    return this.request<Letter[]>(`/children/${childId}/curriculum/alphabet/scripts/${scriptId}/letters/`);
  }

  async getAlphabetProgress(childId: string): Promise<ApiResponse<AlphabetProgress>> {
    return this.request<AlphabetProgress>(`/children/${childId}/curriculum/alphabet/progress/`);
  }

  // Grammar endpoints
  async getGrammarTopics(childId: string, language?: string): Promise<ApiResponse<GrammarTopic[]>> {
    // API returns { data: [...] } format
    const params = language ? `?language=${language}` : '';
    const response = await this.request<{ data: GrammarTopic[] }>(`/children/${childId}/curriculum/grammar/topics/${params}`);
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
    const response = await this.request<{ results: Festival[] } | Festival[]>(`/festivals/festivals/${queryString ? `?${queryString}` : ''}`);
    if (response.success && response.data) {
      // Handle both paginated and non-paginated responses
      const festivals = Array.isArray(response.data) ? response.data : (response.data.results || []);
      return { success: true, data: festivals };
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

  /**
   * Get Peppi narration for a song (full lyrics narration)
   * NOTE: During testing, only 1 song can be cached at a time.
   */
  async getPeppiSongNarration(songId: number | string, language: string, gender: PeppiGender): Promise<ApiResponse<{
    audio_url: string;
    cached: boolean;
    song_title?: string;
    song_title_hindi?: string;
  }>> {
    return this.request<{ audio_url: string; cached: boolean; song_title?: string; song_title_hindi?: string }>(
      `/peppi/narrate/song/${songId}/?language=${language}&gender=${gender}`
    );
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

  // ========================================
  // CURRICULUM HIERARCHY ENDPOINTS
  // ========================================

  /**
   * Get all curriculum levels (L1-L10)
   * @param childId Optional child ID to include progress info
   */
  async getCurriculumLevels(childId?: string): Promise<ApiResponse<CurriculumLevelWithProgress[]>> {
    const params = childId ? `?child_id=${childId}` : '';
    const response = await this.request<CurriculumLevelWithProgress[]>(`/curriculum/levels/${params}`);
    if (response.success && response.data) {
      return { success: true, data: response.data || [] };
    }
    return { success: false, error: response.error, data: [] };
  }

  /**
   * Get a single curriculum level with details
   * @param levelId Level UUID
   * @param childId Optional child ID to include progress info
   */
  async getCurriculumLevel(levelId: string, childId?: string): Promise<ApiResponse<CurriculumLevelWithProgress>> {
    const params = childId ? `?child_id=${childId}` : '';
    return this.request<CurriculumLevelWithProgress>(`/curriculum/levels/${levelId}/${params}`);
  }

  /**
   * Get modules within a curriculum level
   * @param levelId Level UUID
   * @param childId Optional child ID to include progress info
   */
  async getLevelModules(levelId: string, childId?: string): Promise<ApiResponse<CurriculumModuleWithProgress[]>> {
    const params = childId ? `?child_id=${childId}` : '';
    const response = await this.request<CurriculumModuleWithProgress[]>(`/curriculum/levels/${levelId}/modules/${params}`);
    if (response.success && response.data) {
      return { success: true, data: response.data || [] };
    }
    return { success: false, error: response.error, data: [] };
  }

  /**
   * Get a single module with details
   * @param moduleId Module UUID
   * @param childId Optional child ID to include progress info
   */
  async getCurriculumModule(moduleId: string, childId?: string): Promise<ApiResponse<CurriculumModuleWithProgress>> {
    const params = childId ? `?child_id=${childId}` : '';
    return this.request<CurriculumModuleWithProgress>(`/curriculum/modules/${moduleId}/${params}`);
  }

  /**
   * Get lessons within a module
   * @param moduleId Module UUID
   * @param childId Optional child ID to include progress info
   */
  async getModuleLessons(moduleId: string, childId?: string): Promise<ApiResponse<LessonWithProgress[]>> {
    const params = childId ? `?child_id=${childId}` : '';
    const response = await this.request<LessonWithProgress[]>(`/curriculum/modules/${moduleId}/lessons/${params}`);
    if (response.success && response.data) {
      return { success: true, data: response.data || [] };
    }
    return { success: false, error: response.error, data: [] };
  }

  /**
   * Get a single lesson with contents
   * @param lessonId Lesson UUID
   * @param childId Optional child ID to include progress info
   */
  async getLesson(lessonId: string, childId?: string): Promise<ApiResponse<LessonWithProgress>> {
    const params = childId ? `?child_id=${childId}` : '';
    return this.request<LessonWithProgress>(`/curriculum/lessons/${lessonId}/${params}`);
  }

  /**
   * Update lesson progress for a child
   * @param lessonId Lesson UUID
   * @param childId Child UUID
   * @param score Score percentage (0-100)
   */
  async updateLessonProgress(
    lessonId: string,
    childId: string,
    score: number
  ): Promise<ApiResponse<LessonProgress>> {
    return this.request<LessonProgress>(`/curriculum/lessons/${lessonId}/progress/`, {
      method: 'POST',
      body: JSON.stringify({ child_id: childId, score }),
    });
  }

  /**
   * Get child's overall curriculum progress across all levels
   * @param childId Child UUID
   */
  async getChildCurriculumProgress(childId: string): Promise<ApiResponse<ChildCurriculumProgress>> {
    return this.request<ChildCurriculumProgress>(`/curriculum/progress/levels/?child_id=${childId}`);
  }

  // ========================================
  // SONGS ENDPOINTS (L1 Curriculum)
  // ========================================

  /**
   * Get list of songs, optionally filtered by level
   * @param levelId Optional level UUID to filter songs
   */
  async getSongs(levelId?: string): Promise<ApiResponse<Song[]>> {
    const params = levelId ? `?level=${levelId}` : '';
    const response = await this.request<Song[]>(`/curriculum/songs/${params}`);
    if (response.success && response.data) {
      return { success: true, data: response.data || [] };
    }
    return { success: false, error: response.error, data: [] };
  }

  /**
   * Get a single song with details
   * @param songId Song UUID
   */
  async getSong(songId: string): Promise<ApiResponse<Song>> {
    return this.request<Song>(`/curriculum/songs/${songId}/`);
  }

  /**
   * Get songs by level code and optionally language
   * @param levelCode Level code (e.g., 'L1')
   * @param language Optional language filter (e.g., 'HINDI')
   */
  async getSongsByLevel(levelCode: string, language?: string): Promise<ApiResponse<Song[]>> {
    const params = language ? `?language=${language}` : '';
    const response = await this.request<Song[]>(`/curriculum/songs/level/${levelCode}/${params}`);
    if (response.success && response.data) {
      return { success: true, data: response.data || [] };
    }
    return { success: false, error: response.error, data: [] };
  }

  // ========================================
  // PEPPI AI ENDPOINTS
  // ========================================

  /**
   * Get Peppi's greeting for a child
   * @param childId Child UUID
   * @param timeOfDay Optional time of day
   */
  async getPeppiGreeting(childId: string, timeOfDay?: string): Promise<ApiResponse<PeppiGreeting>> {
    const params = timeOfDay ? `?time_of_day=${timeOfDay}` : '';
    return this.request<PeppiGreeting>(`/curriculum/peppi/${childId}/greeting/${params}`);
  }

  /**
   * Get Peppi's teaching script for a word
   * @param childId Child UUID
   * @param wordId Word UUID
   */
  async getPeppiTeaching(childId: string, wordId: string): Promise<ApiResponse<PeppiTeaching>> {
    return this.request<PeppiTeaching>(`/curriculum/peppi/${childId}/teach-word/`, {
      method: 'POST',
      body: JSON.stringify({ word_id: wordId }),
    });
  }

  /**
   * Send feedback to Peppi and get response
   * @param childId Child UUID
   * @param isCorrect Whether the answer was correct
   * @param activityType Type of activity
   */
  async sendPeppiFeedback(
    childId: string,
    isCorrect: boolean,
    activityType: string
  ): Promise<ApiResponse<PeppiFeedback>> {
    return this.request<PeppiFeedback>(`/curriculum/peppi/${childId}/feedback/`, {
      method: 'POST',
      body: JSON.stringify({ is_correct: isCorrect, activity_type: activityType }),
    });
  }

  /**
   * Get current Peppi context for a child
   * @param childId Child UUID
   */
  async getPeppiContext(childId: string): Promise<ApiResponse<PeppiContext>> {
    return this.request<PeppiContext>(`/curriculum/peppi/${childId}/context/`);
  }

  // ========================================
  // PEPPI CHAT ENDPOINTS (AI Chatbot)
  // ========================================

  /**
   * Check Peppi chat service status
   */
  async getPeppiChatStatus(childId: string): Promise<ApiResponse<PeppiChatStatusResponse>> {
    return this.request<PeppiChatStatusResponse>(`/children/${childId}/peppi-chat/status/`);
  }

  /**
   * Start a new Peppi chat conversation
   * @param childId Child UUID
   * @param data Conversation start parameters
   */
  async startPeppiConversation(
    childId: string,
    data: StartConversationRequest
  ): Promise<ApiResponse<StartConversationResponse>> {
    return this.request<StartConversationResponse>(`/children/${childId}/peppi-chat/`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * Send a message in a Peppi chat conversation
   * @param childId Child UUID
   * @param conversationId Conversation UUID
   * @param data Message data
   */
  async sendPeppiMessage(
    childId: string,
    conversationId: string,
    data: SendMessageRequest
  ): Promise<ApiResponse<SendMessageResponse>> {
    return this.request<SendMessageResponse>(
      `/children/${childId}/peppi-chat/${conversationId}/messages/`,
      {
        method: 'POST',
        body: JSON.stringify(data),
      }
    );
  }

  /**
   * Get conversation history
   * @param childId Child UUID
   * @param conversationId Conversation UUID
   * @param limit Number of messages to fetch
   * @param offset Offset for pagination
   */
  async getPeppiConversationHistory(
    childId: string,
    conversationId: string,
    limit: number = 50,
    offset: number = 0
  ): Promise<ApiResponse<ConversationHistoryResponse>> {
    return this.request<ConversationHistoryResponse>(
      `/children/${childId}/peppi-chat/${conversationId}/?limit=${limit}&offset=${offset}`
    );
  }

  /**
   * List all conversations for a child
   * @param childId Child UUID
   * @param activeOnly Only return active conversations
   * @param mode Filter by conversation mode
   */
  async listPeppiConversations(
    childId: string,
    activeOnly: boolean = false,
    mode?: PeppiChatMode
  ): Promise<ApiResponse<{ conversations: PeppiConversationListItem[] }>> {
    let params = `?active=${activeOnly}`;
    if (mode) {
      params += `&mode=${mode}`;
    }
    return this.request<{ conversations: PeppiConversationListItem[] }>(
      `/children/${childId}/peppi-chat/${params}`
    );
  }

  /**
   * End a Peppi chat conversation
   * @param childId Child UUID
   * @param conversationId Conversation UUID
   */
  async endPeppiConversation(
    childId: string,
    conversationId: string
  ): Promise<ApiResponse<{ message: string; conversation: PeppiConversationListItem }>> {
    return this.request<{ message: string; conversation: PeppiConversationListItem }>(
      `/children/${childId}/peppi-chat/${conversationId}/end/`,
      {
        method: 'POST',
      }
    );
  }

  /**
   * Submit an escalation report when Peppi cannot help
   */
  async submitPeppiEscalation(
    childId: string,
    conversationId: string,
    data: SubmitEscalationRequest
  ): Promise<ApiResponse<SubmitEscalationResponse>> {
    return this.request<SubmitEscalationResponse>(
      `/children/${childId}/peppi-chat/${conversationId}/escalate/`,
      {
        method: 'POST',
        body: JSON.stringify(data),
      }
    );
  }

  // ========================================
  // TEACHER ENDPOINTS
  // ========================================

  /**
   * Get all active teachers
   * @param characterType Optional filter by character type (CAT/OWL)
   */
  async getTeachers(characterType?: TeacherCharacterType): Promise<ApiResponse<CurriculumTeacher[]>> {
    const params = characterType ? `?character_type=${characterType}` : '';
    const response = await this.request<CurriculumTeacher[]>(`/curriculum/teachers/${params}`);
    if (response.success && response.data) {
      return { success: true, data: response.data || [] };
    }
    return { success: false, error: response.error, data: [] };
  }

  /**
   * Get a single teacher by ID
   * @param teacherId Teacher UUID
   */
  async getTeacher(teacherId: string): Promise<ApiResponse<CurriculumTeacher>> {
    return this.request<CurriculumTeacher>(`/curriculum/teachers/${teacherId}/`);
  }

  /**
   * Get teacher by character type (CAT for Peppi, OWL for Gyan)
   * @param characterType Character type
   */
  async getTeacherByCharacter(characterType: TeacherCharacterType): Promise<ApiResponse<CurriculumTeacher>> {
    return this.request<CurriculumTeacher>(`/curriculum/teachers/character/${characterType}/`);
  }

  // ========================================
  // CLASSROOM ENDPOINTS
  // ========================================

  /**
   * Get all active classrooms
   */
  async getClassrooms(): Promise<ApiResponse<Classroom[]>> {
    const response = await this.request<Classroom[]>('/curriculum/classrooms/');
    if (response.success && response.data) {
      return { success: true, data: response.data || [] };
    }
    return { success: false, error: response.error, data: [] };
  }

  /**
   * Get a single classroom by ID
   * @param classroomId Classroom UUID
   */
  async getClassroom(classroomId: string): Promise<ApiResponse<ClassroomWithLevel>> {
    return this.request<ClassroomWithLevel>(`/curriculum/classrooms/${classroomId}/`);
  }

  /**
   * Get classroom by level code
   * @param levelCode Level code (e.g., 'L1')
   */
  async getClassroomByLevel(levelCode: string): Promise<ApiResponse<ClassroomWithLevel>> {
    return this.request<ClassroomWithLevel>(`/curriculum/classrooms/level/${levelCode}/`);
  }

  // ========================================
  // SUBSCRIPTION ENDPOINTS
  // ========================================

  /**
   * Get all available subscription tiers (public endpoint)
   */
  async getSubscriptionTiers(): Promise<ApiResponse<SubscriptionTiersResponse>> {
    return this.request<SubscriptionTiersResponse>('/auth/subscription-tiers/');
  }

  /**
   * Get current user's subscription details with homepage configuration
   */
  async getCurrentSubscription(): Promise<ApiResponse<CurrentSubscriptionResponse>> {
    return this.request<CurrentSubscriptionResponse>('/auth/subscription/');
  }

  /**
   * Get homepage progress summary for a child
   * @param childId Child UUID
   */
  async getChildHomepageProgress(childId: string): Promise<ApiResponse<ChildHomepageProgressResponse>> {
    return this.request<ChildHomepageProgressResponse>(`/curriculum/children/${childId}/homepage-progress/`);
  }
}

// Subscription Types
export interface TierFeatureItem {
  text: string;
  enabled: boolean;
  note?: string;
}

export interface TierInfo {
  name: string;
  price: string;
  price_yearly: string;
  currency: string;
  icon: string;
  color: string;
  features: TierFeatureItem[];
  cta: string;
  featured: boolean;
}

export interface SubscriptionTiersResponse {
  data: {
    tiers: {
      FREE: TierInfo;
      STANDARD: TierInfo;
      PREMIUM: TierInfo;
    };
    currency: string;
    billing_cycles: string[];
    contact_for_custom: {
      email: string;
      note: string;
    };
  };
}

export interface SubscriptionFeatures {
  has_curriculum_progression: boolean;
  has_peppi_ai_chat: boolean;
  has_peppi_narration: boolean;
  has_live_classes: boolean;
  has_progress_reports: boolean;
  content_access_mode: string;
  tts_provider: string;
}

export interface SubscriptionLimits {
  story_limit: number;
  games_per_day: number;
  child_profiles: number;
  free_live_classes: number;
}

export interface UpgradeCTA {
  message: string;
  button_text: string;
  price: string;
}

export interface CurrentSubscriptionResponse {
  data: {
    user_id: string;
    tier: 'FREE' | 'STANDARD' | 'PREMIUM';
    is_paid_tier: boolean;
    is_subscription_active: boolean;
    expires_at: string | null;
    homepage_mode: 'playground' | 'classroom';
    homepage_title: string;
    features: SubscriptionFeatures;
    limits: SubscriptionLimits;
    upgrade_cta: UpgradeCTA | null;
  };
}

export interface ChildHomepageProgressResponse {
  data: {
    child: {
      id: string;
      name: string;
      avatar: string;
      level: number;
    };
    summary: {
      levels_completed: number;
      total_points: number;
      current_streak: number;
    };
    current_progress: {
      level: {
        id: string;
        name: string;
        hindi_name: string;
        order: number;
      };
      module: {
        id: string;
        name: string;
        hindi_name: string;
        order: number;
      } | null;
      lesson: {
        id: string;
        title: string;
        hindi_title: string;
        order: number;
      } | null;
      continue_url: string;
    } | null;
    upgrade_prompt?: {
      message: string;
      cta: string;
      price: string;
    };
  };
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
  rule_count?: number;  // Backend sends rule_count (singular)
  progress?: {
    exercises_attempted: number;
    exercises_correct: number;
    accuracy: number;
    mastered: boolean;
  };
}

export interface GrammarExample {
  hindi?: string;
  romanized?: string;
  english?: string;
}

export interface GrammarRule {
  id: string;
  title: string;
  explanation: string;
  formula?: string;
  examples: (string | GrammarExample)[];
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
