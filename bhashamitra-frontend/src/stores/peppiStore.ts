import { create } from 'zustand';
import { PeppiState, PeppiMessage } from '@/types';
import { PEPPI_GREETINGS, PEPPI_ENCOURAGEMENTS, PEPPI_CELEBRATIONS } from '@/lib/constants';

interface PeppiStore extends PeppiState {
  messages: PeppiMessage[];

  // Narration state
  isNarrating: boolean;
  currentStoryId: string | null;
  currentPage: number;
  audioUrl: string | null;
  audioProgress: number;

  // Actions
  setMood: (mood: PeppiState['mood']) => void;
  setTyping: (isTyping: boolean) => void;
  setCurrentMessage: (message: string | null) => void;
  addMessage: (message: Omit<PeppiMessage, 'id' | 'timestamp'>) => void;
  clearMessages: () => void;

  // Narration actions
  startNarration: (storyId: string, page: number) => void;
  stopNarration: () => void;
  setAudioProgress: (progress: number) => void;

  // Convenience methods
  greet: () => void;
  encourage: () => void;
  celebrate: () => void;
  think: () => void;
  speakWithAnimation: (text: string, type: PeppiMessage['type']) => Promise<void>;
}

const getRandomItem = <T>(array: T[]): T => {
  return array[Math.floor(Math.random() * array.length)];
};

export const usePeppiStore = create<PeppiStore>((set, get) => ({
  mood: 'happy',
  isTyping: false,
  currentMessage: null,
  messages: [],

  // Narration state
  isNarrating: false,
  currentStoryId: null,
  currentPage: 0,
  audioUrl: null,
  audioProgress: 0,

  setMood: (mood) => set({ mood }),

  setTyping: (isTyping) => set({ isTyping }),

  setCurrentMessage: (message) => set({ currentMessage: message }),

  addMessage: (message) => {
    const newMessage: PeppiMessage = {
      ...message,
      id: Date.now().toString(),
      timestamp: new Date(),
    };

    set((state) => ({
      messages: [...state.messages, newMessage],
    }));
  },

  clearMessages: () => set({ messages: [] }),

  // Narration actions
  startNarration: (storyId: string, page: number) => {
    set({
      isNarrating: true,
      currentStoryId: storyId,
      currentPage: page,
      mood: 'excited',
    });
  },

  stopNarration: () => {
    set({
      isNarrating: false,
      audioProgress: 0,
      mood: 'happy',
    });
  },

  setAudioProgress: (progress: number) => {
    set({ audioProgress: progress });
  },

  greet: () => {
    const message = getRandomItem(PEPPI_GREETINGS);
    set({ mood: 'happy', currentMessage: message });
    get().addMessage({ type: 'greeting', text: message });
  },

  encourage: () => {
    const message = getRandomItem(PEPPI_ENCOURAGEMENTS);
    set({ mood: 'encouraging', currentMessage: message });
    get().addMessage({ type: 'encouragement', text: message });
  },

  celebrate: () => {
    const message = getRandomItem(PEPPI_CELEBRATIONS);
    set({ mood: 'celebrating', currentMessage: message });
    get().addMessage({ type: 'celebration', text: message });
  },

  think: () => {
    set({ mood: 'thinking', isTyping: true, currentMessage: null });
  },

  speakWithAnimation: async (text: string, type: PeppiMessage['type']) => {
    // Show typing animation
    set({ isTyping: true, mood: 'thinking' });

    // Simulate typing delay based on message length
    const typingDelay = Math.min(text.length * 30, 2000);
    await new Promise((resolve) => setTimeout(resolve, typingDelay));

    // Show the message
    set({
      isTyping: false,
      currentMessage: text,
      mood: type === 'celebration' ? 'celebrating' :
            type === 'encouragement' ? 'encouraging' :
            type === 'hint' ? 'thinking' : 'happy',
    });

    get().addMessage({ type, text });

    // Clear message after display time
    const displayTime = Math.max(text.length * 50, 3000);
    await new Promise((resolve) => setTimeout(resolve, displayTime));

    set({ currentMessage: null, mood: 'happy' });
  },
}));
