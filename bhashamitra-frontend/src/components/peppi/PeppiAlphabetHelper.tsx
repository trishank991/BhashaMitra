'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuthStore, usePeppiChatStore } from '@/stores';
import { cn } from '@/lib/utils';

interface PeppiAlphabetHelperProps {
  language?: string;
  className?: string;
}

// Chat suggestion chips - same as PeppiChatPanel's CURRICULUM_HELP mode
// Restricted to these pre-defined prompts only (no free-form chat)
const chatSuggestions = [
  'Help with grammar',
  'Explain this word',
  'Practice the lesson',
  'Quiz me!',
];

// Peppi Head SVG for the chat button (matches PeppiChatButton)
function PeppiHead() {
  return (
    <svg viewBox="0 0 100 100" className="w-10 h-10">
      {/* Ears */}
      <path fill="#F5E6D3" d="M20 40 L10 10 L35 30 Z"/>
      <path fill="#F5E6D3" d="M80 40 L90 10 L65 30 Z"/>
      <path fill="#FFCDB8" d="M22 30 L16 18 L32 28 Z"/>
      <path fill="#FFCDB8" d="M78 30 L84 18 L68 28 Z"/>
      {/* Head */}
      <ellipse fill="#F5E6D3" cx="50" cy="50" rx="38" ry="35"/>
      {/* Eyes */}
      <ellipse fill="white" cx="35" cy="48" rx="12" ry="14"/>
      <ellipse fill="white" cx="65" cy="48" rx="12" ry="14"/>
      <ellipse fill="#4A90D9" cx="35" cy="50" rx="9" ry="11"/>
      <ellipse fill="#4A90D9" cx="65" cy="50" rx="9" ry="11"/>
      <ellipse fill="#1a1a1a" cx="35" cy="51" rx="4" ry="5"/>
      <ellipse fill="#1a1a1a" cx="65" cy="51" rx="4" ry="5"/>
      <circle fill="white" cx="38" cy="45" r="3"/>
      <circle fill="white" cx="68" cy="45" r="3"/>
      {/* Nose */}
      <path fill="#FF7F50" d="M50 58 L46 65 L54 65 Z"/>
      {/* Whiskers */}
      <line stroke="#999" strokeWidth="1" x1="8" y1="52" x2="28" y2="56"/>
      <line stroke="#999" strokeWidth="1" x1="8" y1="60" x2="28" y2="60"/>
      <line stroke="#999" strokeWidth="1" x1="92" y1="52" x2="72" y2="56"/>
      <line stroke="#999" strokeWidth="1" x1="92" y1="60" x2="72" y2="60"/>
      {/* Collar */}
      <ellipse fill="#FF6B35" cx="50" cy="78" rx="22" ry="5"/>
      {/* Bell */}
      <circle fill="#FFD700" cx="50" cy="83" r="5"/>
      <circle fill="#FFF8DC" cx="48" cy="81" r="1.5"/>
    </svg>
  );
}

// Mini Peppi head for header
function PeppiMiniHead() {
  return (
    <svg viewBox="0 0 100 100" className="w-8 h-8">
      {/* Ears */}
      <path fill="#F5E6D3" d="M20 40 L10 10 L35 30 Z"/>
      <path fill="#F5E6D3" d="M80 40 L90 10 L65 30 Z"/>
      <path fill="#FFCDB8" d="M22 30 L16 18 L32 28 Z"/>
      <path fill="#FFCDB8" d="M78 30 L84 18 L68 28 Z"/>
      {/* Head */}
      <ellipse fill="#F5E6D3" cx="50" cy="50" rx="38" ry="35"/>
      {/* Eyes */}
      <ellipse fill="white" cx="35" cy="48" rx="12" ry="14"/>
      <ellipse fill="white" cx="65" cy="48" rx="12" ry="14"/>
      <ellipse fill="#4A90D9" cx="35" cy="50" rx="9" ry="11"/>
      <ellipse fill="#4A90D9" cx="65" cy="50" rx="9" ry="11"/>
      <ellipse fill="#1a1a1a" cx="35" cy="51" rx="4" ry="5"/>
      <ellipse fill="#1a1a1a" cx="65" cy="51" rx="4" ry="5"/>
      <circle fill="white" cx="38" cy="45" r="3"/>
      <circle fill="white" cx="68" cy="45" r="3"/>
      {/* Nose */}
      <path fill="#FF7F50" d="M50 58 L46 65 L54 65 Z"/>
      {/* Whiskers */}
      <line stroke="#999" strokeWidth="1" x1="8" y1="52" x2="28" y2="56"/>
      <line stroke="#999" strokeWidth="1" x1="8" y1="60" x2="28" y2="60"/>
      <line stroke="#999" strokeWidth="1" x1="92" y1="52" x2="72" y2="56"/>
      <line stroke="#999" strokeWidth="1" x1="92" y1="60" x2="72" y2="60"/>
      {/* Collar */}
      <ellipse fill="#FF6B35" cx="50" cy="78" rx="22" ry="5"/>
      {/* Bell */}
      <circle fill="#FFD700" cx="50" cy="83" r="5"/>
      <circle fill="#FFF8DC" cx="48" cy="81" r="1.5"/>
    </svg>
  );
}

// Typing indicator (matches PeppiTypingIndicator)
function TypingIndicator() {
  return (
    <div className="flex justify-start mb-3">
      <div className="bg-white border border-orange-100 rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-6 h-6 bg-orange-100 rounded-full flex items-center justify-center text-sm animate-bounce">
            🐱
          </div>
          <span className="text-xs font-medium text-orange-600">Peppi</span>
        </div>
        <div className="flex gap-1">
          <span className="w-2 h-2 bg-orange-400 rounded-full animate-bounce [animation-delay:-0.3s]" />
          <span className="w-2 h-2 bg-orange-400 rounded-full animate-bounce [animation-delay:-0.15s]" />
          <span className="w-2 h-2 bg-orange-400 rounded-full animate-bounce" />
        </div>
      </div>
    </div>
  );
}

// Message component (matches PeppiChatMessage)
function ChatMessage({ message }: { message: { role: string; content_primary?: string; content?: string; created_at?: string } }) {
  const isUser = message.role === 'user';
  const content = message.content_primary || message.content || '';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-3`}>
      <div
        className={`max-w-[85%] px-4 py-3 rounded-2xl ${
          isUser
            ? 'bg-orange-500 text-white rounded-br-md'
            : 'bg-white border border-orange-100 text-gray-800 rounded-bl-md shadow-sm'
        }`}
      >
        {/* Avatar for Peppi */}
        {!isUser && (
          <div className="flex items-center gap-2 mb-2">
            <div className="w-6 h-6 bg-orange-100 rounded-full flex items-center justify-center text-sm">
              🐱
            </div>
            <span className="text-xs font-medium text-orange-600">Peppi</span>
          </div>
        )}

        {/* Main content */}
        <p className="text-sm leading-relaxed whitespace-pre-wrap">
          {content}
        </p>

        {/* Timestamp */}
        {message.created_at && (
          <p className={`text-[10px] mt-1.5 ${isUser ? 'text-orange-100' : 'text-gray-400'}`}>
            {new Date(message.created_at).toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </p>
        )}
      </div>
    </div>
  );
}

export function PeppiAlphabetHelper({ language = 'HINDI', className }: PeppiAlphabetHelperProps) {
  const [isOpen, setIsOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const activeChild = useAuthStore((state) => state.activeChild);
  const {
    isAvailable,
    statusMessage,
    checkStatus,
    startConversation,
    sendMessage,
    activeConversation,
    messages,
    isLoading: chatLoading,
    error,
    clearError,
    endConversation,
  } = usePeppiChatStore();

  const childId = activeChild?.id;

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle opening the helper
  const handleOpen = async () => {
    setIsOpen(true);
    if (childId) {
      await checkStatus(childId);
    }
  };

  // Handle closing the helper
  const handleClose = async () => {
    if (activeConversation && childId) {
      await endConversation(childId);
    }
    setIsOpen(false);
    clearError();
  };

  // Handle ending conversation
  const handleEndConversation = async () => {
    if (childId) {
      await endConversation(childId);
    }
  };

  // Handle suggestion chip click
  const handleSuggestionClick = async (suggestion: string) => {
    if (!childId || !isAvailable) return;
    clearError();

    try {
      // Start conversation if not already active
      if (!activeConversation) {
        await startConversation(childId, {
          mode: 'CURRICULUM_HELP',
          language,
        });
        // Wait a moment for state to update
        await new Promise(resolve => setTimeout(resolve, 100));
      }

      // Send the pre-defined message
      await sendMessage(childId, suggestion);
    } catch (err) {
      console.error('[PeppiAlphabetHelper] Error:', err);
    }
  };

  return (
    <div className={cn('fixed bottom-20 right-4 z-50', className)}>
      {/* Chat Panel */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            className="absolute bottom-20 right-0 w-[350px] sm:w-[380px] max-h-[70vh] bg-gray-50 rounded-2xl shadow-2xl border border-gray-200 flex flex-col overflow-hidden"
          >
            {/* Header - matches PeppiChatHeader design */}
            <div className="bg-gradient-to-r from-orange-500 to-amber-500 text-white px-4 py-3 rounded-t-2xl">
              {/* Top row: Title and close */}
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center p-0.5">
                    <PeppiMiniHead />
                  </div>
                  <div>
                    <h3 className="font-semibold text-sm">Chat with Peppi</h3>
                    <p className="text-[10px] text-orange-100">
                      📚 Learn Mode
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  {activeConversation && (
                    <button
                      onClick={handleEndConversation}
                      className="text-xs bg-white/20 hover:bg-white/30 px-2 py-1 rounded transition-colors"
                      title="End conversation"
                    >
                      End Chat
                    </button>
                  )}
                  <button
                    onClick={handleClose}
                    className="w-8 h-8 hover:bg-white/20 rounded-full flex items-center justify-center transition-colors"
                    title="Close"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-5 w-5"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fillRule="evenodd"
                        d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            {/* Error display */}
            {error && (
              <div className="bg-red-50 text-red-600 px-4 py-2 text-sm flex items-center justify-between">
                <span>{error}</span>
                <button onClick={clearError} className="text-red-400 hover:text-red-600">
                  ✕
                </button>
              </div>
            )}

            {/* Chat area */}
            <div className="flex-1 overflow-y-auto p-4 min-h-[200px] max-h-[350px]">
              {!activeConversation ? (
                // No active conversation - show welcome with suggestions
                <div className="flex flex-col items-center justify-center h-full text-center">
                  <div className="mb-2">
                    <PeppiMiniHead />
                  </div>
                  <h4 className="font-semibold text-gray-800 mb-1">
                    Hey! I'm Peppi!
                  </h4>
                  <p className="text-sm text-gray-500 mb-3 px-4">
                    I'm here to help you learn dost!
                  </p>

                  {!isAvailable && childId && (
                    <div className="text-sm text-amber-600 bg-amber-50 px-4 py-2 rounded-lg mb-3">
                      {statusMessage || 'Peppi is currently unavailable'}
                    </div>
                  )}

                  {!childId && (
                    <div className="text-sm text-gray-600 bg-gray-100 px-4 py-2 rounded-lg mb-3">
                      Please select a child profile to use Peppi
                    </div>
                  )}

                  {/* Chat suggestions - pill chips */}
                  <div className="flex flex-wrap justify-center gap-2 mb-4 px-2">
                    {chatSuggestions.map((suggestion, idx) => (
                      <button
                        key={idx}
                        onClick={() => handleSuggestionClick(suggestion)}
                        disabled={chatLoading || !isAvailable || !childId}
                        className="text-xs bg-orange-100 hover:bg-orange-200 text-orange-700 px-3 py-1.5 rounded-full transition-colors disabled:opacity-50"
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                // Active conversation - show messages
                <>
                  {messages.map((msg, idx) => (
                    <ChatMessage key={msg.id || idx} message={msg} />
                  ))}

                  {chatLoading && <TypingIndicator />}

                  {/* Quick suggestion chips for follow-up */}
                  {!chatLoading && (
                    <div className="flex flex-wrap gap-2 mt-4 pt-3 border-t border-gray-200">
                      {chatSuggestions.map((suggestion, idx) => (
                        <button
                          key={idx}
                          onClick={() => handleSuggestionClick(suggestion)}
                          disabled={chatLoading || !isAvailable}
                          className="text-xs bg-orange-100 hover:bg-orange-200 text-orange-700 px-3 py-1.5 rounded-full transition-colors disabled:opacity-50"
                        >
                          {suggestion}
                        </button>
                      ))}
                    </div>
                  )}

                  <div ref={messagesEndRef} />
                </>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Floating Button - matches PeppiChatButton design */}
      <motion.button
        onClick={isOpen ? handleClose : handleOpen}
        className={cn(
          'w-16 h-16 rounded-full shadow-xl flex items-center justify-center transition-all',
          isOpen
            ? 'bg-gray-100 hover:bg-gray-200 border-2 border-gray-300'
            : 'bg-gradient-to-br from-orange-100 to-amber-100 hover:from-orange-200 hover:to-amber-200 border-2 border-orange-300'
        )}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        animate={{
          y: isOpen ? 0 : [0, -5, 0],
        }}
        transition={{
          y: {
            duration: 2,
            repeat: isOpen ? 0 : Infinity,
            ease: 'easeInOut',
          },
        }}
      >
        {isOpen ? (
          // Close icon
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6 text-gray-600"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        ) : (
          // Peppi head
          <PeppiHead />
        )}

        {/* AI badge when closed */}
        {!isOpen && (
          <motion.span
            className="absolute -top-1 -right-1 bg-gradient-to-r from-pink-500 to-orange-500 text-white px-2 py-0.5 rounded-full text-[10px] font-bold shadow-lg"
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            AI
          </motion.span>
        )}

        {/* Chat text hint */}
        {!isOpen && (
          <motion.div
            initial={{ opacity: 0, x: 10 }}
            animate={{ opacity: 1, x: 0 }}
            className="absolute right-full mr-2 bg-white px-3 py-1.5 rounded-lg shadow-lg whitespace-nowrap"
          >
            <span className="text-sm font-medium text-gray-700">Chat with Peppi!</span>
            <div className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-1 w-0 h-0 border-t-[6px] border-t-transparent border-b-[6px] border-b-transparent border-l-[6px] border-l-white" />
          </motion.div>
        )}
      </motion.button>
    </div>
  );
}

export default PeppiAlphabetHelper;
