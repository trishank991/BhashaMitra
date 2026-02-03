'use client';

import { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { usePeppiChatStore, useAuthStore } from '@/stores';
import { PeppiChatHeader } from './PeppiChatHeader';
import { PeppiChatMessage } from './PeppiChatMessage';
import { PeppiChatInput } from './PeppiChatInput';
import { PeppiTypingIndicator } from './PeppiTypingIndicator';
import { PeppiMascot } from '@/components/peppi/PeppiMascot';
import { PeppiChatMode } from '@/types';
import { AlertCircle, Send, X, CheckCircle } from 'lucide-react';

// Chat suggestion chips for different modes
const chatSuggestions = {
  GENERAL: [
    'Teach me a new word',
    'Let\'s play a word game',
    'How do I say "hello"?',
    'Practice sentences',
  ],
  FESTIVAL_STORY: [
    'Tell me about this story',
    'Why did the hero do that?',
    'What\'s the moral?',
    'Explain the festival',
  ],
  CURRICULUM_HELP: [
    'Help with grammar',
    'Explain this word',
    'Practice the lesson',
    'Quiz me!',
  ],
};

interface PeppiChatPanelProps {
  childId: string;
}

// Helper to extract language code from child profile
const getChildLanguage = (language: unknown): string => {
  if (!language) return 'HINDI';
  if (typeof language === 'string') return language;
  if (typeof language === 'object' && language !== null && 'code' in language) {
    return (language as { code: string }).code;
  }
  return 'HINDI';
};

export function PeppiChatPanel({ childId }: PeppiChatPanelProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [escalationText, setEscalationText] = useState('');

  // Get child's language from auth store
  const activeChild = useAuthStore((state) => state.activeChild);
  const childLanguage = getChildLanguage(activeChild?.language);

  const {
    isOpen,
    isLoading,
    error,
    activeConversation,
    messages,
    mode,
    isAvailable,
    statusMessage,
    showEscalationPrompt,
    escalationSubmitting,
    escalationSuccess,
    closeChat,
    setMode,
    startConversation,
    sendMessage,
    endConversation,
    checkStatus,
    clearError,
    submitEscalation,
    dismissEscalationPrompt,
  } = usePeppiChatStore();

  // Check status on mount
  useEffect(() => {
    if (isOpen && childId) {
      checkStatus(childId);
    }
  }, [isOpen, childId, checkStatus]);

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle mode change
  const handleModeChange = async (newMode: PeppiChatMode) => {
    if (activeConversation && mode !== newMode) {
      // End current conversation and start new one with different mode
      await endConversation(childId);
    }
    setMode(newMode);
  };

  // Handle send message
  const handleSendMessage = async (content: string) => {
    if (!activeConversation) {
      // Start a new conversation first and wait for it to complete
      // startConversation now returns the conversation directly,
      // avoiding the race condition with state updates
      const newConversation = await startConversation(childId, { mode, language: childLanguage });
      if (newConversation) {
        // Send message using the returned conversation directly
        sendMessage(childId, content);
      }
    } else {
      sendMessage(childId, content);
    }
  };

  // Handle end conversation
  const handleEndConversation = async () => {
    await endConversation(childId);
  };

  // Handle starting a conversation
  const handleStartChat = async () => {
    clearError();
    await startConversation(childId, { mode, language: childLanguage });
  };

  // Handle escalation submission
  const handleSubmitEscalation = async () => {
    if (!escalationText.trim()) return;
    await submitEscalation(childId, escalationText.trim());
    setEscalationText('');
  };

  if (!isOpen) return null;

  return (
    <div className="fixed bottom-20 right-4 z-50 w-[350px] sm:w-[380px] max-h-[70vh] bg-gray-50 rounded-2xl shadow-2xl border border-gray-200 flex flex-col">
      {/* Header */}
      <PeppiChatHeader
        mode={mode}
        onModeChange={handleModeChange}
        onClose={closeChat}
        onEndConversation={activeConversation ? handleEndConversation : undefined}
        hasActiveConversation={!!activeConversation}
      />

      {/* Error display */}
      {error && (
        <div className="bg-red-50 text-red-600 px-4 py-2 text-sm flex items-center justify-between">
          <span>{error}</span>
          <button
            onClick={clearError}
            className="text-red-400 hover:text-red-600"
          >
            ✕
          </button>
        </div>
      )}

      {/* Chat area */}
      <div className="flex-1 overflow-y-auto p-4 min-h-[200px] max-h-[350px]">
        {!activeConversation ? (
          // No active conversation - show start button with suggestions
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="mb-2">
              <PeppiMascot size="sm" />
            </div>
            <h4 className="font-semibold text-gray-800 mb-1">
              Hey! I&apos;m Peppi!
            </h4>
            <p className="text-sm text-gray-500 mb-3 px-4">
              {mode === 'FESTIVAL_STORY'
                ? "Let&apos;s explore festival stories together yaar!"
                : mode === 'CURRICULUM_HELP'
                ? "I&apos;m here to help you learn dost!"
                : "Let&apos;s chat and practice together!"}
            </p>

            {/* Chat suggestions */}
            <div className="flex flex-wrap justify-center gap-2 mb-4 px-2">
              {chatSuggestions[mode].map((suggestion, idx) => (
                <button
                  key={idx}
                  onClick={async () => {
                    clearError();
                    // Start conversation and wait for it to complete
                    await startConversation(childId, { mode, language: childLanguage });
                    // Now send the suggestion message
                    sendMessage(childId, suggestion);
                  }}
                  disabled={isLoading || !isAvailable}
                  className="text-xs bg-orange-100 hover:bg-orange-200 text-orange-700 px-3 py-1.5 rounded-full transition-colors disabled:opacity-50"
                >
                  {suggestion}
                </button>
              ))}
            </div>

            {!isAvailable ? (
              <div className="text-sm text-amber-600 bg-amber-50 px-4 py-2 rounded-lg">
                {statusMessage}
              </div>
            ) : (
              <button
                onClick={handleStartChat}
                disabled={isLoading}
                className="bg-orange-500 hover:bg-orange-600 text-white px-6 py-2.5 rounded-xl font-medium text-sm transition-colors disabled:bg-gray-300"
              >
                {isLoading ? 'Starting...' : 'Start Chatting'}
              </button>
            )}
          </div>
        ) : (
          // Active conversation - show messages
          <>
            {messages.map((msg) => (
              <PeppiChatMessage key={msg.id} message={msg} />
            ))}

            {isLoading && <PeppiTypingIndicator />}

            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Escalation Prompt */}
      <AnimatePresence>
        {showEscalationPrompt && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="mx-4 mb-3 bg-amber-50 border border-amber-200 rounded-xl p-3"
          >
            <div className="flex items-start gap-2 mb-2">
              <AlertCircle className="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm font-medium text-amber-800">
                  Need more help?
                </p>
                <p className="text-xs text-amber-600 mt-0.5">
                  Tell us about your issue and our team will look into it.
                </p>
              </div>
              <button
                onClick={dismissEscalationPrompt}
                className="text-amber-400 hover:text-amber-600"
              >
                <X size={16} />
              </button>
            </div>
            <div className="flex gap-2">
              <input
                type="text"
                value={escalationText}
                onChange={(e) => setEscalationText(e.target.value)}
                placeholder="Describe your issue..."
                className="flex-1 px-3 py-2 text-sm border border-amber-200 rounded-lg
                           focus:outline-none focus:ring-2 focus:ring-amber-300"
                disabled={escalationSubmitting}
              />
              <button
                onClick={handleSubmitEscalation}
                disabled={!escalationText.trim() || escalationSubmitting}
                className="px-3 py-2 bg-amber-500 hover:bg-amber-600 disabled:bg-gray-300
                           text-white rounded-lg transition-colors"
              >
                {escalationSubmitting ? (
                  <span className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin block" />
                ) : (
                  <Send size={16} />
                )}
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Escalation Success Message */}
      <AnimatePresence>
        {escalationSuccess && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="mx-4 mb-3 bg-green-50 border border-green-200 rounded-xl p-3 flex items-center gap-2"
          >
            <CheckCircle className="w-5 h-5 text-green-500" />
            <p className="text-sm text-green-700">
              Thanks! Our team will review your report.
            </p>
            <button
              onClick={dismissEscalationPrompt}
              className="ml-auto text-green-400 hover:text-green-600"
            >
              <X size={16} />
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Input area */}
      {activeConversation && (
        <PeppiChatInput
          onSend={handleSendMessage}
          disabled={isLoading || !isAvailable}
          placeholder={
            mode === 'FESTIVAL_STORY'
              ? 'Ask about the story...'
              : mode === 'CURRICULUM_HELP'
              ? 'Ask me anything about your lesson...'
              : 'Type your message...'
          }
        />
      )}
    </div>
  );
}
