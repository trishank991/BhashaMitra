'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { SUPPORTED_LANGUAGES } from '@/lib/constants';
import { LanguageCode } from '@/types';

interface LanguageSelectorProps {
  currentLanguage: LanguageCode;
  onLanguageChange: (language: LanguageCode) => void;
  isLoading?: boolean;
}

export function LanguageSelector({
  currentLanguage,
  onLanguageChange,
  isLoading = false,
}: LanguageSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);

  const currentLang = SUPPORTED_LANGUAGES[currentLanguage] || SUPPORTED_LANGUAGES.HINDI;

  // Hindi, Tamil, Punjabi, Fiji Hindi, and Gujarati have curriculum content
  const availableLanguages: LanguageCode[] = ['HINDI', 'PUNJABI', 'TAMIL', 'FIJI_HINDI', 'GUJARATI'];

  return (
    <div className="relative">
      {/* Current Language Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        disabled={isLoading}
        className="flex items-center gap-2 px-4 py-2 bg-white rounded-2xl shadow-sm border-2 border-gray-100 hover:border-primary-300 transition-all disabled:opacity-50"
      >
        <span className="text-2xl">{currentLang.flag}</span>
        <div className="text-left">
          <p className="text-sm font-bold text-gray-900">{currentLang.name}</p>
          <p className="text-xs text-gray-500">{currentLang.nativeName}</p>
        </div>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className={`h-4 w-4 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
        {isLoading && (
          <div className="absolute right-2 top-1/2 -translate-y-1/2">
            <div className="w-4 h-4 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
          </div>
        )}
      </button>

      {/* Dropdown */}
      <AnimatePresence>
        {isOpen && (
          <>
            {/* Backdrop */}
            <div
              className="fixed inset-0 z-40"
              onClick={() => setIsOpen(false)}
            />

            {/* Options */}
            <motion.div
              initial={{ opacity: 0, y: -10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -10, scale: 0.95 }}
              transition={{ duration: 0.15 }}
              className="absolute top-full left-0 right-0 mt-2 bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden z-50 min-w-[200px]"
            >
              <div className="p-2">
                <p className="px-3 py-2 text-xs font-medium text-gray-400 uppercase">
                  Select Language
                </p>
                {availableLanguages.map((langCode) => {
                  const lang = SUPPORTED_LANGUAGES[langCode];
                  const isSelected = langCode === currentLanguage;

                  return (
                    <button
                      key={langCode}
                      onClick={() => {
                        if (!isSelected) {
                          onLanguageChange(langCode);
                        }
                        setIsOpen(false);
                      }}
                      className={`w-full flex items-center gap-3 px-3 py-3 rounded-xl transition-colors ${
                        isSelected
                          ? 'bg-primary-50 border-2 border-primary-300'
                          : 'hover:bg-gray-50 border-2 border-transparent'
                      }`}
                    >
                      <span className="text-2xl">{lang.flag}</span>
                      <div className="text-left flex-1">
                        <p className={`font-medium ${isSelected ? 'text-primary-700' : 'text-gray-900'}`}>
                          {lang.name}
                        </p>
                        <p className="text-sm text-gray-500">{lang.nativeName}</p>
                      </div>
                      {isSelected && (
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          className="h-5 w-5 text-primary-500"
                          viewBox="0 0 20 20"
                          fill="currentColor"
                        >
                          <path
                            fillRule="evenodd"
                            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                            clipRule="evenodd"
                          />
                        </svg>
                      )}
                    </button>
                  );
                })}
              </div>

              {/* Coming Soon Languages */}
              <div className="border-t border-gray-100 p-2 bg-gray-50">
                <p className="px-3 py-2 text-xs font-medium text-gray-400">
                  Coming Soon
                </p>
                <div className="flex flex-wrap gap-2 px-3 py-1">
                  {(['TELUGU', 'MALAYALAM', 'BENGALI'] as LanguageCode[]).map((langCode) => {
                    const lang = SUPPORTED_LANGUAGES[langCode];
                    return (
                      <span
                        key={langCode}
                        className="inline-flex items-center gap-1 px-2 py-1 bg-gray-200 rounded-full text-xs text-gray-500"
                      >
                        {lang.flag} {lang.name}
                      </span>
                    );
                  })}
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
}

export default LanguageSelector;
