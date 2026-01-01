import { create } from 'zustand';
import { api } from '@/lib/api';
import {
  PeppiChatMode,
  PeppiConversation,
  PeppiConversationListItem,
  PeppiChatMessage,
  StartConversationRequest,
} from '@/types';

interface PeppiChatState {
  // Chat panel state
  isOpen: boolean;
  isLoading: boolean;
  error: string | null;

  // Current conversation
  activeConversation: PeppiConversation | null;
  messages: PeppiChatMessage[];
  mode: PeppiChatMode;

  // Streaming state (for future use)
  isStreaming: boolean;
  streamingContent: string;

  // Conversation list
  conversations: PeppiConversationListItem[];

  // Service status
  isAvailable: boolean;
  statusMessage: string;

  // Escalation state
  showEscalationPrompt: boolean;
  lastEscalationMessageId: string | null;
  escalationSubmitting: boolean;
  escalationSuccess: boolean;
}

interface PeppiChatActions {
  // Panel actions
  openChat: (mode?: PeppiChatMode) => void;
  closeChat: () => void;
  setMode: (mode: PeppiChatMode) => void;

  // Conversation actions
  startConversation: (
    childId: string,
    request: StartConversationRequest
  ) => Promise<PeppiConversation | null>;
  sendMessage: (childId: string, content: string) => Promise<void>;
  loadConversationHistory: (
    childId: string,
    conversationId: string
  ) => Promise<void>;
  endConversation: (childId: string) => Promise<void>;
  listConversations: (childId: string, activeOnly?: boolean) => Promise<void>;
  resumeConversation: (
    childId: string,
    conversationId: string
  ) => Promise<void>;

  // Festival story helpers
  startFestivalChat: (
    childId: string,
    festivalId: string,
    storyId: string,
    language?: string
  ) => Promise<void>;

  // Curriculum chat helpers
  startCurriculumChat: (
    childId: string,
    lessonId?: string,
    language?: string
  ) => Promise<void>;

  // Status
  checkStatus: (childId: string) => Promise<void>;
  clearError: () => void;
  reset: () => void;

  // Escalation actions
  submitEscalation: (
    childId: string,
    description: string
  ) => Promise<void>;
  dismissEscalationPrompt: () => void;
}

type PeppiChatStore = PeppiChatState & PeppiChatActions;

const initialState: PeppiChatState = {
  isOpen: false,
  isLoading: false,
  error: null,
  activeConversation: null,
  messages: [],
  mode: 'GENERAL',
  isStreaming: false,
  streamingContent: '',
  conversations: [],
  isAvailable: false,
  statusMessage: 'Checking Peppi status...',
  showEscalationPrompt: false,
  lastEscalationMessageId: null,
  escalationSubmitting: false,
  escalationSuccess: false,
};

export const usePeppiChatStore = create<PeppiChatStore>((set, get) => ({
  ...initialState,

  // Panel actions
  openChat: (mode = 'GENERAL') => {
    set({ isOpen: true, mode, error: null });
  },

  closeChat: () => {
    set({ isOpen: false });
  },

  setMode: (mode) => {
    set({ mode });
  },

  // Start a new conversation
  startConversation: async (childId, request) => {
    set({ isLoading: true, error: null });

    try {
      const response = await api.startPeppiConversation(childId, request);

      if (response.success && response.data) {
        const { conversation, greeting } = response.data;
        set({
          activeConversation: conversation,
          messages: [greeting],
          mode: request.mode,
          isLoading: false,
        });
        return conversation;
      } else {
        set({
          error: response.error || 'Failed to start conversation',
          isLoading: false,
        });
        return null;
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Network error',
        isLoading: false,
      });
      return null;
    }
  },

  // Send a message
  sendMessage: async (childId, content) => {
    const { activeConversation } = get();

    if (!activeConversation) {
      set({ error: 'No active conversation' });
      return;
    }

    set({ isLoading: true, error: null });

    // Optimistically add user message
    const tempUserMessage: PeppiChatMessage = {
      id: `temp-${Date.now()}`,
      role: 'user',
      content_primary: content,
      input_type: 'text',
      created_at: new Date().toISOString(),
    };

    set((state) => ({
      messages: [...state.messages, tempUserMessage],
    }));

    try {
      const response = await api.sendPeppiMessage(
        childId,
        activeConversation.id,
        { content, input_type: 'text' }
      );

      if (response.success && response.data) {
        const { user_message, assistant_message, needs_escalation } = response.data;

        // Replace temp message with actual and add assistant response
        set((state) => ({
          messages: [
            ...state.messages.filter((m) => m.id !== tempUserMessage.id),
            user_message,
            assistant_message,
          ],
          isLoading: false,
          // Show escalation prompt if Peppi couldn't help
          showEscalationPrompt: needs_escalation,
          lastEscalationMessageId: needs_escalation ? assistant_message.id : null,
          escalationSuccess: false,
        }));
      } else {
        // Remove temp message on error
        set((state) => ({
          messages: state.messages.filter((m) => m.id !== tempUserMessage.id),
          error: response.error || 'Failed to send message',
          isLoading: false,
        }));
      }
    } catch (error) {
      set((state) => ({
        messages: state.messages.filter((m) => m.id !== tempUserMessage.id),
        error: error instanceof Error ? error.message : 'Network error',
        isLoading: false,
      }));
    }
  },

  // Load conversation history
  loadConversationHistory: async (childId, conversationId) => {
    set({ isLoading: true, error: null });

    try {
      const response = await api.getPeppiConversationHistory(
        childId,
        conversationId
      );

      if (response.success && response.data) {
        set({
          messages: response.data.messages,
          isLoading: false,
        });
      } else {
        set({
          error: response.error || 'Failed to load history',
          isLoading: false,
        });
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Network error',
        isLoading: false,
      });
    }
  },

  // End conversation
  endConversation: async (childId) => {
    const { activeConversation } = get();

    if (!activeConversation) return;

    try {
      await api.endPeppiConversation(childId, activeConversation.id);
      set({
        activeConversation: null,
        messages: [],
      });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to end conversation',
      });
    }
  },

  // List conversations
  listConversations: async (childId, activeOnly = false) => {
    try {
      const response = await api.listPeppiConversations(childId, activeOnly);

      if (response.success && response.data) {
        set({ conversations: response.data.conversations });
      }
    } catch (error) {
      console.error('Failed to list conversations:', error);
    }
  },

  // Resume an existing conversation
  resumeConversation: async (childId, conversationId) => {
    set({ isLoading: true, error: null });

    try {
      const response = await api.getPeppiConversationHistory(
        childId,
        conversationId
      );

      if (response.success && response.data) {
        const { conversation, messages } = response.data;
        set({
          activeConversation: {
            id: conversation.id,
            child_name: conversation.child_name,
            mode: conversation.mode,
            language: conversation.language,
            is_active: conversation.is_active,
            messages_count: conversation.messages_count,
            created_at: conversation.created_at,
            last_message_at: conversation.last_message_at,
          },
          messages,
          mode: conversation.mode,
          isOpen: true,
          isLoading: false,
        });
      } else {
        set({
          error: response.error || 'Failed to load conversation',
          isLoading: false,
        });
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Network error',
        isLoading: false,
      });
    }
  },

  // Start festival story chat
  startFestivalChat: async (childId, festivalId, storyId, language = 'HINDI') => {
    await get().startConversation(childId, {
      mode: 'FESTIVAL_STORY',
      language,
      festival_id: festivalId,
      story_id: storyId,
    });
    set({ isOpen: true });
  },

  // Start curriculum help chat
  startCurriculumChat: async (childId, lessonId, language = 'HINDI') => {
    await get().startConversation(childId, {
      mode: 'CURRICULUM_HELP',
      language,
      lesson_id: lessonId,
    });
    set({ isOpen: true });
  },

  // Check service status
  checkStatus: async (childId) => {
    if (!childId) {
      set({
        isAvailable: false,
        statusMessage: 'No child profile selected',
      });
      return;
    }

    try {
      const response = await api.getPeppiChatStatus(childId);

      if (response.success && response.data) {
        set({
          isAvailable: response.data.available,
          statusMessage: response.data.message,
        });
      } else {
        set({
          isAvailable: false,
          statusMessage: response.error || 'Service unavailable',
        });
      }
    } catch {
      set({
        isAvailable: false,
        statusMessage: 'Unable to check status',
      });
    }
  },

  // Clear error
  clearError: () => set({ error: null }),

  // Reset store
  reset: () => set(initialState),

  // Submit escalation report
  submitEscalation: async (childId, description) => {
    const { activeConversation, lastEscalationMessageId } = get();

    if (!activeConversation) {
      set({ error: 'No active conversation' });
      return;
    }

    set({ escalationSubmitting: true, error: null });

    try {
      const response = await api.submitPeppiEscalation(
        childId,
        activeConversation.id,
        {
          message_id: lastEscalationMessageId || undefined,
          description,
        }
      );

      if (response.success) {
        set({
          escalationSubmitting: false,
          escalationSuccess: true,
          showEscalationPrompt: false,
        });
      } else {
        set({
          escalationSubmitting: false,
          error: response.error || 'Failed to submit report',
        });
      }
    } catch (error) {
      set({
        escalationSubmitting: false,
        error: error instanceof Error ? error.message : 'Network error',
      });
    }
  },

  // Dismiss escalation prompt
  dismissEscalationPrompt: () => set({
    showEscalationPrompt: false,
    lastEscalationMessageId: null,
    escalationSuccess: false,
  }),
}));
