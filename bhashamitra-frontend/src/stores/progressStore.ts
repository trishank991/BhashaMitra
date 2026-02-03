import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { Badge, GameSession } from '@/types';
import { XP_PER_LEVEL, STREAK_BONUS_XP, API_BASE_URL } from '@/lib/constants';
import api from '@/lib/api';

// Helper function to make authenticated requests
async function fetchWithAuth<T>(endpoint: string): Promise<T | null> {
  const token = api.getAccessToken();
  if (!token) return null;

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) return null;
    const data = await response.json();
    return data;
  } catch {
    return null;
  }
}

interface ProgressState {
  xp: number;
  level: number;
  streak: number;
  lastPracticeDate: string | null;
  badges: Badge[];
  gameSessions: GameSession[];
  storiesRead: string[];
  wordsLearned: string[];

  // Actions
  addXp: (amount: number) => void;
  updateStreak: () => void;
  syncWithBackend: (childId: string) => Promise<void>;
  addBadge: (badge: Omit<Badge, 'earnedAt'>) => void;
  addGameSession: (session: GameSession) => void;
  markStoryRead: (storyId: string) => void;
  addLearnedWord: (wordId: string) => void;
  resetProgress: () => void;

  // Computed
  getXpForNextLevel: () => number;
  getXpProgress: () => number;
}

export const useProgressStore = create<ProgressState>()(
  persist(
    (set, get) => ({
      xp: 0,
      level: 1,
      streak: 0,
      lastPracticeDate: null,
      badges: [],
      gameSessions: [],
      storiesRead: [],
      wordsLearned: [],

      addXp: (amount: number) => {
        const { xp, level } = get();
        let newXp = xp + amount;
        let newLevel = level;

        // Check for level up
        while (newXp >= XP_PER_LEVEL * newLevel) {
          newXp -= XP_PER_LEVEL * newLevel;
          newLevel += 1;
        }

        set({ xp: newXp, level: newLevel });
      },

      updateStreak: () => {
        const { lastPracticeDate, streak } = get();
        const today = new Date().toISOString().split('T')[0];

        if (lastPracticeDate === today) {
          // Already practiced today
          return;
        }

        const yesterday = new Date(Date.now() - 86400000)
          .toISOString()
          .split('T')[0];

        if (lastPracticeDate === yesterday) {
          // Continuing streak
          const newStreak = streak + 1;
          set({
            streak: newStreak,
            lastPracticeDate: today,
          });

          // Add streak bonus XP
          get().addXp(STREAK_BONUS_XP);

          // Check for streak badges
          if (newStreak === 7) {
            get().addBadge({
              id: 'streak-7',
              name: 'Week Warrior',
              description: 'Practiced for 7 days in a row!',
              icon: '🔥',
              type: 'streak',
            });
          } else if (newStreak === 30) {
            get().addBadge({
              id: 'streak-30',
              name: 'Monthly Master',
              description: 'Practiced for 30 days in a row!',
              icon: '⭐',
              type: 'streak',
            });
          }
        } else {
          // Streak broken, start fresh
          set({
            streak: 1,
            lastPracticeDate: today,
          });
        }
      },

      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      syncWithBackend: async (childId: string) => {
        try {
          // Fetch streak from backend
          const streakData = await fetchWithAuth<{ data: { current_streak: number; longest_streak: number; last_activity_date: string | null; is_active: boolean } }>('/gamification/streak/');
          if (streakData?.data) {
            set({ streak: streakData.data.current_streak || 0 });
          }

          // Fetch badges from backend
          const badgesData = await fetchWithAuth<{ data: { earned: Array<{ id: string; name: string; description: string; icon: string; earned_at: string }>; available: Array<{ id: string; name: string; description: string; icon: string }> } }>('/gamification/badges/');
          if (badgesData?.data?.earned) {
            set({
              badges: badgesData.data.earned.map((b) => ({
                id: b.id,
                name: b.name,
                description: b.description,
                icon: b.icon,
                type: 'achievement' as const,
                earnedAt: b.earned_at,
              })),
            });
          }
        } catch (error) {
          console.error('Failed to sync gamification data with backend:', error);
        }
      },

      addBadge: (badge) => {
        const { badges } = get();

        // Check if badge already earned
        if (badges.some((b) => b.id === badge.id)) {
          return;
        }

        const newBadge: Badge = {
          ...badge,
          earnedAt: new Date().toISOString(),
        };

        set({ badges: [...badges, newBadge] });
      },

      addGameSession: (session) => {
        set((state) => ({
          gameSessions: [...state.gameSessions, session],
        }));

        // Add XP from game
        get().addXp(session.xpEarned);
        get().updateStreak();
      },

      markStoryRead: (storyId: string) => {
        const { storiesRead } = get();

        if (storiesRead.includes(storyId)) {
          return;
        }

        set({ storiesRead: [...storiesRead, storyId] });
        get().updateStreak();

        // Add story completion XP
        get().addXp(50); // STORY_COMPLETE_XP

        // Check for story badges
        const totalStories = storiesRead.length + 1;
        if (totalStories === 1) {
          get().addBadge({
            id: 'first-story',
            name: 'Story Starter',
            description: 'Read your first story!',
            icon: '📖',
            type: 'achievement',
          });
        } else if (totalStories === 10) {
          get().addBadge({
            id: 'story-10',
            name: 'Bookworm',
            description: 'Read 10 stories!',
            icon: '📚',
            type: 'milestone',
          });
        }
      },

      addLearnedWord: (wordId: string) => {
        const { wordsLearned } = get();

        if (wordsLearned.includes(wordId)) {
          return;
        }

        set({ wordsLearned: [...wordsLearned, wordId] });

        // Check for vocabulary badges
        const totalWords = wordsLearned.length + 1;
        if (totalWords === 10) {
          get().addBadge({
            id: 'words-10',
            name: 'Word Collector',
            description: 'Learned 10 new words!',
            icon: '📝',
            type: 'achievement',
          });
        } else if (totalWords === 50) {
          get().addBadge({
            id: 'words-50',
            name: 'Vocabulary Victor',
            description: 'Learned 50 new words!',
            icon: '🏆',
            type: 'milestone',
          });
        }
      },

      resetProgress: () => {
        set({
          xp: 0,
          level: 1,
          streak: 0,
          lastPracticeDate: null,
          badges: [],
          gameSessions: [],
          storiesRead: [],
          wordsLearned: [],
        });
      },

      getXpForNextLevel: () => {
        const { level } = get();
        return XP_PER_LEVEL * level;
      },

      getXpProgress: () => {
        const { xp, level } = get();
        return (xp / (XP_PER_LEVEL * level)) * 100;
      },
    }),
    {
      name: 'bhashamitra-progress',
    }
  )
);
