'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Volume2, ChevronLeft, ChevronRight, BookOpen, Music, Sparkles, Play } from 'lucide-react';
import { cn } from '@/lib/utils';
import { api } from '@/lib/api';
import type { LessonContent } from '@/types/curriculum';

interface ContentData {
  // Common fields
  id?: string;
  // Vocabulary word fields
  word?: string;
  romanization?: string;
  translation?: string;
  example_sentence?: string;
  example_translation?: string;
  pronunciation_audio_url?: string;
  image_url?: string;
  part_of_speech?: string;
  gender?: string;
  // Letter fields
  character?: string;
  ipa?: string;
  example_word?: string;
  example_word_translation?: string;
  pronunciation_guide?: string;
  audio_url?: string;
  category?: string;
  // Matra fields
  symbol?: string;
  name?: string;
  sound?: string;
  usage_examples?: string[];
  // Story fields
  title?: string;
  title_hindi?: string;
  content_text?: string;
  pages?: { text: string; image_url?: string }[];
  // Song fields
  lyrics?: string[];
  lyrics_romanized?: string[];
  video_url?: string;
}

interface LessonContentRendererProps {
  content: LessonContent & { data?: ContentData };
  language?: string;
  showTranslations?: boolean;
  onComplete?: () => void;
  className?: string;
}

export function LessonContentRenderer({
  content,
  language = 'HINDI',
  showTranslations = true,
  onComplete,
  className,
}: LessonContentRendererProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentPage, setCurrentPage] = useState(0);
  const [showDetails, setShowDetails] = useState(false);
  const [highlightedWord, setHighlightedWord] = useState(-1);

  const data = content.data || {};

  // Reset state when content changes
  useEffect(() => {
    setCurrentPage(0);
    setShowDetails(false);
    setHighlightedWord(-1);
  }, [content.id]);

  // TTS playback handler
  const playAudio = async (text: string, audioUrl?: string) => {
    setIsPlaying(true);
    try {
      if (audioUrl) {
        const audio = new Audio(audioUrl);
        audio.onended = () => setIsPlaying(false);
        audio.onerror = () => setIsPlaying(false);
        await audio.play();
      } else {
        const response = await api.getAudio(text, language, 'kid_friendly');
        if (response.success && response.audioUrl) {
          const audio = new Audio(response.audioUrl);
          audio.onended = () => setIsPlaying(false);
          audio.onerror = () => setIsPlaying(false);
          await audio.play();
        } else {
          setIsPlaying(false);
        }
      }
    } catch (error) {
      console.error('Audio playback error:', error);
      setIsPlaying(false);
    }
  };

  // Audio button component
  const AudioButton = ({ text, audioUrl, size = 'md' }: { text: string; audioUrl?: string; size?: 'sm' | 'md' | 'lg' }) => {
    const sizeClasses = {
      sm: 'w-10 h-10',
      md: 'w-14 h-14',
      lg: 'w-16 h-16',
    };

    return (
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={(e) => {
          e.stopPropagation();
          playAudio(text, audioUrl);
        }}
        disabled={isPlaying}
        className={cn(
          'rounded-full flex items-center justify-center shadow-lg transition-all',
          sizeClasses[size],
          isPlaying
            ? 'bg-primary-300 animate-pulse'
            : 'bg-primary-500 hover:bg-primary-600'
        )}
      >
        <Volume2 className="text-white" size={size === 'lg' ? 28 : size === 'md' ? 24 : 20} />
      </motion.button>
    );
  };

  // Render vocabulary word content
  const renderVocabularyWord = () => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-3xl p-8 border-2 border-purple-200 shadow-xl"
    >
      <div className="flex flex-col items-center text-center">
        {/* Image */}
        {data.image_url && (
          <motion.img
            initial={{ scale: 0.8 }}
            animate={{ scale: 1 }}
            src={data.image_url}
            alt={data.translation}
            className="w-40 h-40 object-cover rounded-2xl mb-6 shadow-lg border-4 border-white"
          />
        )}

        {/* Word */}
        <div className="relative mb-4">
          <h2 className="text-6xl md:text-7xl font-bold text-gray-900 mb-2">
            {data.word}
          </h2>
          <div className="absolute -right-16 top-1/2 -translate-y-1/2">
            <AudioButton
              text={data.word || ''}
              audioUrl={data.pronunciation_audio_url}
              size="lg"
            />
          </div>
        </div>

        {/* Romanization */}
        <p className="text-2xl text-purple-600 font-semibold mb-2">
          {data.romanization}
        </p>

        {/* Part of speech & gender */}
        {(data.part_of_speech || data.gender) && (
          <div className="flex gap-2 mb-4">
            {data.part_of_speech && (
              <span className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm font-medium">
                {data.part_of_speech}
              </span>
            )}
            {data.gender && (
              <span className="bg-pink-100 text-pink-700 px-3 py-1 rounded-full text-sm font-medium">
                {data.gender}
              </span>
            )}
          </div>
        )}

        {/* Translation */}
        {showTranslations && data.translation && (
          <p className="text-xl text-gray-700 font-medium mb-6">
            {data.translation}
          </p>
        )}

        {/* Example sentence */}
        {data.example_sentence && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: showDetails ? 1 : 0, height: showDetails ? 'auto' : 0 }}
            className="w-full max-w-md overflow-hidden"
          >
            <div className="bg-white/80 rounded-2xl p-4 border border-purple-200">
              <p className="text-lg text-gray-800 mb-1">{data.example_sentence}</p>
              {showTranslations && data.example_translation && (
                <p className="text-gray-500 text-sm">{data.example_translation}</p>
              )}
            </div>
          </motion.div>
        )}

        {/* Show example button */}
        {data.example_sentence && (
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="mt-4 text-purple-600 font-medium flex items-center gap-1"
          >
            <Sparkles size={16} />
            {showDetails ? 'Hide example' : 'Show example sentence'}
          </button>
        )}
      </div>
    </motion.div>
  );

  // Render letter content
  const renderLetter = () => (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-3xl p-8 border-2 border-yellow-200 shadow-xl"
    >
      <div className="flex flex-col items-center text-center">
        {/* Giant letter */}
        <motion.div
          initial={{ scale: 0.5, rotate: -10 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{ type: 'spring', duration: 0.5 }}
          className="relative mb-6"
        >
          <div className="text-9xl md:text-[12rem] font-bold text-orange-600 leading-none">
            {data.character}
          </div>
          <div className="absolute -right-12 top-4">
            <AudioButton
              text={data.character || ''}
              audioUrl={data.audio_url}
              size="lg"
            />
          </div>
        </motion.div>

        {/* Romanization & IPA */}
        <div className="flex items-center gap-4 mb-4">
          <span className="text-3xl font-bold text-orange-500">
            {data.romanization}
          </span>
          {data.ipa && (
            <span className="text-xl text-gray-500 font-mono">
              [{data.ipa}]
            </span>
          )}
        </div>

        {/* Category badge */}
        {data.category && (
          <span className="bg-orange-100 text-orange-700 px-4 py-2 rounded-full text-sm font-semibold mb-6">
            {data.category}
          </span>
        )}

        {/* Pronunciation guide */}
        {data.pronunciation_guide && (
          <div className="bg-white/80 rounded-2xl p-4 border border-orange-200 max-w-md mb-4">
            <p className="text-gray-700">{data.pronunciation_guide}</p>
          </div>
        )}

        {/* Example word */}
        {data.example_word && (
          <div className="bg-orange-100/50 rounded-2xl p-4 border border-orange-200">
            <p className="text-2xl font-bold text-gray-800 mb-1">
              {data.example_word}
            </p>
            {showTranslations && data.example_word_translation && (
              <p className="text-gray-600">{data.example_word_translation}</p>
            )}
          </div>
        )}
      </div>
    </motion.div>
  );

  // Render matra content
  const renderMatra = () => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-gradient-to-br from-teal-50 to-cyan-50 rounded-3xl p-8 border-2 border-teal-200 shadow-xl"
    >
      <div className="flex flex-col items-center text-center">
        {/* Matra symbol */}
        <motion.div
          animate={{ scale: [1, 1.05, 1] }}
          transition={{ repeat: Infinity, duration: 2 }}
          className="text-8xl md:text-9xl font-bold text-teal-600 mb-4"
        >
          {data.symbol || data.character}
        </motion.div>

        {/* Name and sound */}
        <h3 className="text-2xl font-bold text-gray-800 mb-2">
          {data.name || data.romanization}
        </h3>
        {data.sound && (
          <p className="text-xl text-teal-600 mb-4">
            Sound: &ldquo;{data.sound}&rdquo;
          </p>
        )}

        {/* Audio button */}
        <AudioButton
          text={data.symbol || data.character || ''}
          audioUrl={data.audio_url}
          size="lg"
        />

        {/* Usage examples */}
        {data.usage_examples && data.usage_examples.length > 0 && (
          <div className="mt-6 w-full max-w-md">
            <h4 className="text-lg font-semibold text-gray-700 mb-3">Examples:</h4>
            <div className="space-y-2">
              {data.usage_examples.map((example, idx) => (
                <div
                  key={idx}
                  className="bg-white/80 rounded-xl p-3 border border-teal-200"
                >
                  <p className="text-lg">{example}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );

  // Render story content
  const renderStory = () => {
    const pages = data.pages || [{ text: data.content_text || '' }];
    const currentPageData = pages[currentPage];

    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-3xl p-8 border-2 border-indigo-200 shadow-xl"
      >
        {/* Title */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <BookOpen className="text-indigo-500" size={28} />
            <div>
              <h2 className="text-2xl font-bold text-gray-900">
                {data.title_hindi || data.title}
              </h2>
              {showTranslations && data.title && data.title_hindi && (
                <p className="text-gray-500">{data.title}</p>
              )}
            </div>
          </div>
          <AudioButton
            text={currentPageData?.text || ''}
            size="md"
          />
        </div>

        {/* Story page */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentPage}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            className="bg-white rounded-2xl p-6 border border-indigo-200 min-h-[200px]"
          >
            {currentPageData?.image_url && (
              <img
                src={currentPageData.image_url}
                alt=""
                className="w-full h-48 object-cover rounded-xl mb-4"
              />
            )}
            <p className="text-xl leading-relaxed text-gray-800">
              {currentPageData?.text}
            </p>
          </motion.div>
        </AnimatePresence>

        {/* Navigation */}
        {pages.length > 1 && (
          <div className="flex items-center justify-between mt-6">
            <button
              onClick={() => setCurrentPage(Math.max(0, currentPage - 1))}
              disabled={currentPage === 0}
              className={cn(
                'flex items-center gap-2 px-4 py-2 rounded-xl font-medium transition-all',
                currentPage === 0
                  ? 'text-gray-400 cursor-not-allowed'
                  : 'text-indigo-600 hover:bg-indigo-100'
              )}
            >
              <ChevronLeft size={20} />
              Previous
            </button>

            <span className="text-gray-500">
              {currentPage + 1} / {pages.length}
            </span>

            <button
              onClick={() => {
                if (currentPage === pages.length - 1) {
                  onComplete?.();
                } else {
                  setCurrentPage(currentPage + 1);
                }
              }}
              className="flex items-center gap-2 px-4 py-2 rounded-xl font-medium text-indigo-600 hover:bg-indigo-100 transition-all"
            >
              {currentPage === pages.length - 1 ? 'Complete' : 'Next'}
              <ChevronRight size={20} />
            </button>
          </div>
        )}
      </motion.div>
    );
  };

  // Render song content
  const renderSong = () => {
    const lyrics = data.lyrics || [];
    const romanized = data.lyrics_romanized || [];

    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-br from-pink-50 to-rose-50 rounded-3xl p-8 border-2 border-pink-200 shadow-xl"
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <Music className="text-pink-500" size={28} />
            <h2 className="text-2xl font-bold text-gray-900">
              {data.title_hindi || data.title || 'Song'}
            </h2>
          </div>
          {data.video_url && (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex items-center gap-2 bg-pink-500 text-white px-4 py-2 rounded-xl font-medium"
            >
              <Play size={18} />
              Play Video
            </motion.button>
          )}
        </div>

        {/* Lyrics */}
        <div className="bg-white rounded-2xl p-6 border border-pink-200">
          <div className="space-y-4">
            {lyrics.map((line, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0.5 }}
                animate={{
                  opacity: highlightedWord === idx ? 1 : 0.7,
                  scale: highlightedWord === idx ? 1.02 : 1,
                }}
                onClick={() => playAudio(line)}
                className={cn(
                  'p-3 rounded-xl cursor-pointer transition-all',
                  highlightedWord === idx
                    ? 'bg-pink-100 border-2 border-pink-300'
                    : 'hover:bg-pink-50'
                )}
              >
                <p className="text-xl font-medium text-gray-800">{line}</p>
                {romanized[idx] && (
                  <p className="text-pink-600 text-sm mt-1">{romanized[idx]}</p>
                )}
              </motion.div>
            ))}
          </div>
        </div>

        {/* Play all button */}
        <div className="flex justify-center mt-6">
          <AudioButton
            text={lyrics.join('. ')}
            size="lg"
          />
        </div>
      </motion.div>
    );
  };

  // Render based on content type
  const renderContent = () => {
    switch (content.content_type) {
      case 'VOCABULARY_WORD':
        return renderVocabularyWord();
      case 'LETTER':
        return renderLetter();
      case 'MATRA':
        return renderMatra();
      case 'STORY':
        return renderStory();
      case 'SONG':
        return renderSong();
      default:
        return (
          <div className="bg-gray-100 rounded-2xl p-8 text-center">
            <p className="text-gray-500">
              Content type &ldquo;{content.content_type}&rdquo; not yet supported
            </p>
          </div>
        );
    }
  };

  return (
    <div className={cn('max-w-2xl mx-auto', className)}>
      {renderContent()}
    </div>
  );
}

export default LessonContentRenderer;
