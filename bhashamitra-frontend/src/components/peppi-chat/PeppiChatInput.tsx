'use client';

import { useState, KeyboardEvent, useRef } from 'react';
import { Keyboard, X } from 'lucide-react';
import { IndianLanguageKeyboard } from '@/components/ui';
import { AnimatePresence } from 'framer-motion';

type LanguageCode = 'HINDI' | 'TAMIL' | 'TELUGU' | 'GUJARATI' | 'PUNJABI' | 'BENGALI' | 'MALAYALAM';

interface PeppiChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
  language?: LanguageCode;
}

export function PeppiChatInput({
  onSend,
  disabled = false,
  placeholder = 'Type a message...',
  language = 'HINDI',
}: PeppiChatInputProps) {
  const [input, setInput] = useState('');
  const [showKeyboard, setShowKeyboard] = useState(false);
  const [keyboardLanguage, setKeyboardLanguage] = useState<LanguageCode>(language);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    const trimmedInput = input.trim();
    if (trimmedInput && !disabled) {
      onSend(trimmedInput);
      setInput('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleKeyboardInput = (char: string) => {
    setInput((prev) => prev + char);
    textareaRef.current?.focus();
  };

  const handleKeyboardDelete = () => {
    setInput((prev) => prev.slice(0, -1));
    textareaRef.current?.focus();
  };

  return (
    <div className="border-t border-gray-100 bg-white">
      {/* Main input area */}
      <div className="p-3">
        <div className="flex items-end gap-2">
          {/* Keyboard toggle button */}
          <button
            onClick={() => setShowKeyboard(!showKeyboard)}
            className={`w-10 h-10 rounded-xl flex items-center justify-center transition-colors duration-200 ${
              showKeyboard
                ? 'bg-indigo-500 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
            title={showKeyboard ? 'Hide keyboard' : 'Show Indian language keyboard'}
          >
            {showKeyboard ? <X size={20} /> : <Keyboard size={20} />}
          </button>

          {/* Text input */}
          <div className="flex-1 relative">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={placeholder}
              disabled={disabled}
              rows={1}
              className="w-full px-4 py-2.5 pr-12 border border-gray-200 rounded-xl
                         resize-none focus:outline-none focus:ring-2 focus:ring-orange-300
                         focus:border-orange-300 disabled:bg-gray-50 disabled:text-gray-400
                         text-sm"
              style={{ minHeight: '42px', maxHeight: '120px' }}
            />
          </div>

          {/* Send button */}
          <button
            onClick={handleSend}
            disabled={disabled || !input.trim()}
            className="w-10 h-10 bg-orange-500 hover:bg-orange-600 disabled:bg-gray-300
                       rounded-xl flex items-center justify-center text-white
                       transition-colors duration-200"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
            </svg>
          </button>
        </div>

        {/* Character count */}
        <div className="flex justify-between items-center mt-1">
          <span className="text-xs text-gray-400">
            {showKeyboard && `Typing in ${keyboardLanguage}`}
          </span>
          <span className={`text-xs ${input.length > 900 ? 'text-red-500' : 'text-gray-400'}`}>
            {input.length}/1000
          </span>
        </div>
      </div>

      {/* Indian Language Keyboard - Fixed above bottom nav when open */}
      <AnimatePresence>
        {showKeyboard && (
          <div className="fixed bottom-16 left-0 right-0 z-[60]">
            <IndianLanguageKeyboard
              language={keyboardLanguage}
              onInput={handleKeyboardInput}
              onDelete={handleKeyboardDelete}
              onClose={() => setShowKeyboard(false)}
              onLanguageChange={(lang) => setKeyboardLanguage(lang)}
              isOpen={showKeyboard}
            />
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
