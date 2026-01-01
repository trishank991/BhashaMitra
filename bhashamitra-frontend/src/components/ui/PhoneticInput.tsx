'use client';

import { useState, useEffect, useRef, ChangeEvent, KeyboardEvent, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Volume2, ArrowRightLeft, Sparkles, Keyboard, X } from 'lucide-react';
import { cn } from '@/lib/utils';
import { LanguageCode } from '@/types';
import {
  getRandomExample,
  detectScriptType,
  normalizeForTransliteration,
  simpleTransliterate,
} from '@/lib/transliteration';
import { IndianLanguageKeyboard } from './IndianLanguageKeyboard';

// Subset of languages supported by the keyboard
type KeyboardLanguageCode = 'HINDI' | 'TAMIL' | 'TELUGU' | 'GUJARATI' | 'PUNJABI' | 'BENGALI' | 'MALAYALAM';

export type PhoneticInputMode = 'roman-to-native' | 'native-to-roman';

export interface PhoneticInputProps {
  language: LanguageCode;
  value?: string;
  onChange: (nativeText: string, romanText: string) => void;
  placeholder?: string;
  onSpeak?: (text: string) => void;
  onSubmit?: (text: string) => void;
  mode?: PhoneticInputMode;
  showPreview?: boolean;
  disabled?: boolean;
  className?: string;
  autoTransliterate?: boolean;
  showHints?: boolean;
  maxLength?: number;
  rows?: number;
}

export function PhoneticInput({
  language,
  value: externalValue = '',
  onChange,
  placeholder,
  onSpeak,
  onSubmit,
  mode: initialMode = 'roman-to-native',
  showPreview = true,
  disabled = false,
  className,
  autoTransliterate = true,
  showHints = true,
  maxLength = 1000,
  rows = 3,
}: PhoneticInputProps) {
  const [romanText, setRomanText] = useState('');
  const [nativeText, setNativeText] = useState('');
  const [mode, setMode] = useState<PhoneticInputMode>(initialMode);
  const [isTransliterating, setIsTransliterating] = useState(false);
  const [hint, setHint] = useState<{ roman: string; native: string } | null>(null);
  const [showKeyboard, setShowKeyboard] = useState(false);
  const [keyboardLanguage, setKeyboardLanguage] = useState<LanguageCode>(language);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const transliterateTimeoutRef = useRef<NodeJS.Timeout>();

  // Update hint when language changes
  useEffect(() => {
    if (showHints) {
      setHint(getRandomExample(language));
    }
  }, [language, showHints]);

  // Sync with external value
  useEffect(() => {
    if (externalValue !== nativeText && externalValue !== romanText) {
      const scriptType = detectScriptType(externalValue);
      if (scriptType === 'native') {
        setNativeText(externalValue);
      } else {
        setRomanText(externalValue);
        handleTransliterate(externalValue);
      }
    }
  }, [externalValue]);

  // Transliterate function
  const handleTransliterate = async (text: string) => {
    if (!autoTransliterate || !text.trim()) {
      setNativeText('');
      return;
    }

    setIsTransliterating(true);

    // Clear previous timeout
    if (transliterateTimeoutRef.current) {
      clearTimeout(transliterateTimeoutRef.current);
    }

    // Debounce transliteration
    transliterateTimeoutRef.current = setTimeout(() => {
      try {
        const normalized = normalizeForTransliteration(text);
        const result = simpleTransliterate(normalized, language);
        setNativeText(result);
        onChange(result, text);
      } catch (error) {
        console.error('Transliteration error:', error);
        setNativeText(text);
        onChange(text, text);
      } finally {
        setIsTransliterating(false);
      }
    }, 150);
  };

  // Handle roman input change
  const handleRomanChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    const text = e.target.value;
    if (text.length > maxLength) return;

    setRomanText(text);
    if (mode === 'roman-to-native') {
      handleTransliterate(text);
    } else {
      onChange(text, text);
    }
  };

  // Handle native input change
  const handleNativeChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    const text = e.target.value;
    if (text.length > maxLength) return;

    setNativeText(text);
    onChange(text, romanText);
  };

  // Toggle mode
  const toggleMode = () => {
    setMode(prevMode => prevMode === 'roman-to-native' ? 'native-to-roman' : 'roman-to-native');
  };

  // Handle keyboard input
  const handleKeyboardInput = (char: string) => {
    const newText = nativeText + char;
    if (newText.length > maxLength) return;

    setNativeText(newText);
    onChange(newText, romanText);
    inputRef.current?.focus();
  };

  // Handle keyboard delete
  const handleKeyboardDelete = () => {
    const newText = nativeText.slice(0, -1);
    setNativeText(newText);
    onChange(newText, romanText);
    inputRef.current?.focus();
  };

  // Handle key down (Enter to submit)
  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey && onSubmit) {
      e.preventDefault();
      const textToSubmit = mode === 'roman-to-native' ? nativeText : romanText;
      if (textToSubmit.trim()) {
        onSubmit(textToSubmit);
        setRomanText('');
        setNativeText('');
      }
    }
  };

  // Handle speak
  const handleSpeak = () => {
    const textToSpeak = mode === 'roman-to-native' ? nativeText : romanText;
    if (onSpeak && textToSpeak.trim()) {
      onSpeak(textToSpeak);
    }
  };

  // Memoized keyboard language type guard - maps to supported keyboard languages
  const getKeyboardLangCode = useMemo((): KeyboardLanguageCode => {
    const validKeyboardLangs: KeyboardLanguageCode[] = ['HINDI', 'TAMIL', 'TELUGU', 'GUJARATI', 'PUNJABI', 'BENGALI', 'MALAYALAM'];
    if (validKeyboardLangs.includes(keyboardLanguage as KeyboardLanguageCode)) {
      return keyboardLanguage as KeyboardLanguageCode;
    }
    // Map unsupported languages to closest supported one
    if (keyboardLanguage === 'MARATHI' || keyboardLanguage === 'FIJI_HINDI') return 'HINDI';
    if (keyboardLanguage === 'KANNADA') return 'TELUGU'; // Similar Dravidian script
    if (keyboardLanguage === 'ODIA') return 'BENGALI'; // Similar script family
    if (keyboardLanguage === 'ASSAMESE') return 'BENGALI'; // Uses Bengali script
    if (keyboardLanguage === 'URDU') return 'HINDI'; // Can use Devanagari
    return 'HINDI';
  }, [keyboardLanguage]);

  return (
    <div className={cn('w-full', className)}>
      {/* Header with mode toggle and actions */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          {/* Mode indicator */}
          <button
            onClick={toggleMode}
            disabled={disabled}
            className={cn(
              'flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
              disabled
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-indigo-100 text-indigo-700 hover:bg-indigo-200'
            )}
            title="Toggle input mode"
          >
            <span>{mode === 'roman-to-native' ? 'Roman → Native' : 'Native → Roman'}</span>
            <ArrowRightLeft size={14} />
          </button>

          {/* Transliterating indicator */}
          <AnimatePresence>
            {isTransliterating && (
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.8 }}
                className="flex items-center gap-1 text-indigo-500"
              >
                <Sparkles size={14} className="animate-pulse" />
                <span className="text-xs">Converting...</span>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Action buttons */}
        <div className="flex items-center gap-2">
          {/* Keyboard toggle */}
          <button
            onClick={() => setShowKeyboard(!showKeyboard)}
            disabled={disabled}
            className={cn(
              'p-2 rounded-lg transition-colors',
              showKeyboard
                ? 'bg-indigo-500 text-white'
                : disabled
                  ? 'bg-gray-100 text-gray-400'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            )}
            title={showKeyboard ? 'Hide keyboard' : 'Show native keyboard'}
          >
            {showKeyboard ? <X size={16} /> : <Keyboard size={16} />}
          </button>

          {/* Speak button */}
          {onSpeak && (
            <button
              onClick={handleSpeak}
              disabled={disabled || (!nativeText.trim() && !romanText.trim())}
              className={cn(
                'p-2 rounded-lg transition-colors',
                disabled || (!nativeText.trim() && !romanText.trim())
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-green-100 text-green-700 hover:bg-green-200'
              )}
              title="Speak text"
            >
              <Volume2 size={16} />
            </button>
          )}
        </div>
      </div>

      {/* Hint */}
      {showHints && hint && !romanText && !nativeText && (
        <motion.div
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-2 p-2 bg-amber-50 border border-amber-200 rounded-lg"
        >
          <p className="text-xs text-amber-700">
            <span className="font-medium">Try: </span>
            <span className="font-mono">{hint.roman}</span>
            <span className="mx-1">→</span>
            <span className="font-bold text-lg">{hint.native}</span>
          </p>
        </motion.div>
      )}

      {/* Input area */}
      <div className="relative">
        {mode === 'roman-to-native' ? (
          // Roman to Native mode
          <textarea
            ref={inputRef}
            value={romanText}
            onChange={handleRomanChange}
            onKeyDown={handleKeyDown}
            placeholder={placeholder || 'Type in English/Roman script...'}
            disabled={disabled}
            rows={rows}
            maxLength={maxLength}
            className={cn(
              'w-full px-4 py-3 rounded-xl border-2 transition-colors resize-none',
              'text-gray-900 placeholder:text-gray-400',
              'focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100',
              disabled && 'bg-gray-100 cursor-not-allowed opacity-60',
              'font-mono'
            )}
          />
        ) : (
          // Native to Roman mode
          <textarea
            ref={inputRef}
            value={nativeText}
            onChange={handleNativeChange}
            onKeyDown={handleKeyDown}
            placeholder={placeholder || 'Type in native script...'}
            disabled={disabled}
            rows={rows}
            maxLength={maxLength}
            className={cn(
              'w-full px-4 py-3 rounded-xl border-2 transition-colors resize-none',
              'text-gray-900 placeholder:text-gray-400 text-xl',
              'focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100',
              disabled && 'bg-gray-100 cursor-not-allowed opacity-60'
            )}
          />
        )}

        {/* Character counter */}
        <div className="absolute bottom-2 right-3 text-xs text-gray-400">
          {mode === 'roman-to-native' ? romanText.length : nativeText.length}/{maxLength}
        </div>
      </div>

      {/* Preview of transliterated text */}
      {showPreview && mode === 'roman-to-native' && nativeText && (
        <motion.div
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-2 p-3 bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200 rounded-xl"
        >
          <div className="flex items-center gap-2 mb-1">
            <Sparkles size={14} className="text-indigo-500" />
            <span className="text-xs font-medium text-indigo-700">Transliterated:</span>
          </div>
          <p className="text-2xl font-bold text-gray-900">{nativeText}</p>
        </motion.div>
      )}

      {/* Native keyboard */}
      <AnimatePresence>
        {showKeyboard && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-3"
          >
            <IndianLanguageKeyboard
              language={getKeyboardLangCode}
              onInput={handleKeyboardInput}
              onDelete={handleKeyboardDelete}
              onClose={() => setShowKeyboard(false)}
              onLanguageChange={(lang) => setKeyboardLanguage(lang)}
              isOpen={showKeyboard}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default PhoneticInput;
