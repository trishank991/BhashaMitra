'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import confetti from 'canvas-confetti';
import { Card, Button } from '@/components/ui';
import { useSounds } from '@/hooks';
import { useAudio } from '@/hooks/useAudio';

interface SpellingBeeGameProps {
  onComplete?: (score: number, passed: boolean) => void;
  onBack?: () => void;
}

// Sample spelling words for Hindi learning
const SPELLING_WORDS = [
  {
    id: '1',
    word: 'हाथी',
    meaning: 'elephant',
    hint: 'एक बड़ा जानवर जिसकी सोंग होती है',
    audioHint: 'हाथी - एक बड़ा जानवर',
  },
  {
    id: '2',
    word: 'किताब',
    meaning: 'book',
    hint: 'जिसमें कहानियाँ और कविताएँ होती हैं',
    audioHint: 'किताब - पढ़ने की चीज़',
  },
  {
    id: '3',
    word: 'आम',
    meaning: 'mango',
    hint: 'एक मीठा पीला फल',
    audioHint: 'आम - एक मीठा फल',
  },
  {
    id: '4',
    word: 'चाँद',
    meaning: 'moon',
    hint: 'रात में आसमान में चमकता है',
    audioHint: 'चाँद - रात का सितारा',
  },
  {
    id: '5',
    word: 'पानी',
    meaning: 'water',
    hint: 'पीने की चीज़, बिना जीवन नहीं जी सकते',
    audioHint: 'पानी - जीवन की ज़रूरत',
  },
  {
    id: '6',
    word: 'पतंग',
    meaning: 'kite',
    hint: 'हवा में उड़ती है, धागे से बाँधी जाती है',
    audioHint: 'पतंग - हवा में उड़ने वाली',
  },
  {
    id: '7',
    word: 'सूरज',
    meaning: 'sun',
    hint: 'दिन में आसमान में चमकता है, गर्मी देता है',
    audioHint: 'सूरज - दिन का तारा',
  },
  {
    id: '8',
    word: 'मछली',
    meaning: 'fish',
    hint: 'पानी में रहती है, तैरती है',
    audioHint: 'मछली - पानी का जानवर',
  },
  {
    id: '9',
    word: 'पहाड़',
    meaning: 'mountain',
    hint: 'बहुत ऊँची ज़मीन',
    audioHint: 'पहाड़ - ऊँची भूमि',
  },
  {
    id: '10',
    word: 'तारा',
    meaning: 'star',
    hint: 'रात में आसमान में चमकते हैं',
    audioHint: 'तारा - रात का सव्र्व्य',
  },
];

export default function SpellingBeeGame({ onComplete, onBack }: SpellingBeeGameProps) {
  const [words, setWords] = useState(SPELLING_WORDS);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userInput, setUserInput] = useState('');
  const [score, setScore] = useState(0);
  const [showHint, setShowHint] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [attempts, setAttempts] = useState(0);
  const [hasRevealed, setHasRevealed] = useState(false);
  
  const { onCorrect, onWrong, onLevelUp, onClick } = useSounds();
  const { isLoading, playAudio } = useAudio({ language: 'HINDI' });
  
  const inputRef = useRef<HTMLInputElement>(null);
  const currentWord = words[currentIndex];

  // Shuffle words on mount
  useEffect(() => {
    const shuffled = [...SPELLING_WORDS].sort(() => Math.random() - 0.5);
    setWords(shuffled);
  }, []);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, [currentIndex]);

  const playHintAudio = useCallback(() => {
    if (currentWord) {
      playAudio(currentWord.audioHint);
    }
  }, [currentWord, playAudio]);

  const playWordAudio = useCallback(() => {
    if (currentWord) {
      playAudio(currentWord.word);
    }
  }, [currentWord, playAudio]);

  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    if (!userInput.trim()) return;
    
    onClick();
    setAttempts(prev => prev + 1);
    
    // Normalize input (remove spaces, lowercase comparison)
    const normalizedInput = userInput.trim().replace(/\s+/g, '');
    const normalizedWord = currentWord.word.replace(/\s+/g, '');
    
    if (normalizedInput === normalizedWord) {
      // Correct!
      setScore(s => s + (attempts === 0 ? 40 : attempts === 1 ? 25 : 10));
      onCorrect();
      
      // Confetti for first try
      if (attempts === 0) {
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 },
          colors: ['#f59e0b', '#22c55e', '#3b82f6'],
        });
      }
      
      // Move to next word after short delay
      setTimeout(() => {
        if (currentIndex < words.length - 1) {
          setCurrentIndex(i => i + 1);
          setUserInput('');
          setAttempts(0);
          setHasRevealed(false);
          setShowHint(false);
        } else {
          // Game complete
          setIsComplete(true);
          const finalScore = score + (attempts === 0 ? 40 : attempts === 1 ? 25 : 10);
          const passed = finalScore >= 250;
          
          if (passed) {
            onLevelUp();
            confetti({
              particleCount: 150,
              spread: 100,
              origin: { y: 0.5 },
            });
          }
          
          onComplete?.(finalScore, passed);
        }
      }, 1500);
    } else {
      // Wrong - shake animation
      onWrong();
      setUserInput('');
      inputRef.current?.focus();
    }
  }, [userInput, currentWord, attempts, currentIndex, words.length, score, onCorrect, onWrong, onLevelUp, onComplete, onClick]);

  const handleReveal = useCallback(() => {
    setHasRevealed(true);
    setShowHint(true);
    playWordAudio();
  }, [playWordAudio]);

  if (isComplete) {
    const totalScore = score;
    const passed = totalScore >= 250;
    
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-100 flex items-center justify-center p-4">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="max-w-md w-full"
        >
          <Card className="text-center p-8 bg-white shadow-xl">
            <div className="text-6xl mb-4">🅱️️</div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              {passed ? 'शाबाश!' : 'अच्छा प्रयास!'}
            </h2>
            <p className="text-gray-600 mb-6">
              {passed 
                ? 'आपने स्पेलिंग बी पूरी कर ली!' 
                : 'फिर से कोशिश करें!'}
            </p>
            
            <div className="text-5xl font-bold text-primary-600 mb-2">
              {totalScore}
            </div>
            <p className="text-sm text-gray-500 mb-6">अंक (40 अंक प्रति शब्द)</p>

            {/* Stars earned */}
            <div className="flex justify-center gap-2 mb-6">
              {[1, 2, 3].map((star) => (
                <span 
                  key={star}
                  className={`text-4xl ${star <= Math.floor(totalScore / 150) ? 'opacity-100' : 'opacity-30'}`}
                >
                  ⭐
                </span>
              ))}
            </div>

            <div className="flex gap-3 justify-center">
              <Button variant="outline" onClick={onBack}>
                वापस जाएं
              </Button>
              <Button 
                variant="primary" 
                onClick={() => {
                  const shuffled = [...SPELLING_WORDS].sort(() => Math.random() - 0.5);
                  setWords(shuffled);
                  setCurrentIndex(0);
                  setScore(0);
                  setUserInput('');
                  setAttempts(0);
                  setIsComplete(false);
                  setHasRevealed(false);
                  setShowHint(false);
                }}
              >
                फिर से खेलें
              </Button>
            </div>
          </Card>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-100">
      {/* Header */}
      <div className="bg-white shadow-sm p-4">
        <div className="max-w-2xl mx-auto flex items-center justify-between">
          <Button variant="ghost" size="sm" onClick={onBack}>
            ← वापस
          </Button>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600">
              {currentIndex + 1} / {words.length}
            </span>
            <div className="w-32 h-3 bg-gray-200 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-purple-500"
                initial={{ width: 0 }}
                animate={{ width: `${((currentIndex + 1) / words.length) * 100}%` }}
              />
            </div>
          </div>
          <span className="text-lg font-bold text-primary-600">
            {score} XP
          </span>
        </div>
      </div>

      {/* Game Content */}
      <div className="max-w-2xl mx-auto p-6">
        <motion.div
          key={currentIndex}
          initial={{ x: 50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: -50, opacity: 0 }}
        >
          {/* Meaning Card */}
          <Card className="p-6 mb-6 bg-white shadow-lg">
            <p className="text-lg text-gray-500 mb-2">इसका क्या अर्थ है?</p>
            <p className="text-3xl font-bold text-gray-900 mb-4">
              {currentWord?.meaning}
            </p>
            
            {/* Hint Toggle */}
            {!hasRevealed && (
              <Button
                variant="outline"
                size="sm"
                onClick={handleReveal}
                className="mb-2"
              >
                💡 सही शब्द देखें
              </Button>
            )}

            {/* Revealed Word */}
            <AnimatePresence>
              {hasRevealed && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="bg-yellow-50 border border-yellow-200 rounded-lg p-4"
                >
                  <p className="text-4xl font-bold text-yellow-700 text-center mb-2">
                    {currentWord?.word}
                  </p>
                  <p className="text-sm text-yellow-600 text-center">
                    सही वर्तनी लिखें
                  </p>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Hint */}
            {showHint && !hasRevealed && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4"
              >
                <p className="text-sm text-yellow-700">
                  <strong>सुराग:</strong> {currentWord?.hint}
                </p>
              </motion.div>
            )}
          </Card>

          {/* Audio Buttons */}
          <div className="flex justify-center gap-3 mb-6">
            <Button
              variant="secondary"
              onClick={playWordAudio}
              disabled={isLoading}
            >
              🔊 सुनें
            </Button>
            <Button
              variant="secondary"
              onClick={playHintAudio}
              disabled={isLoading}
            >
              💡 सुराग सुनें
            </Button>
          </div>

          {/* Input Form */}
          <form onSubmit={handleSubmit}>
            <Card className="p-6 mb-4 bg-white shadow-lg">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                सही वर्तनी लिखें:
              </label>
              <input
                ref={inputRef}
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                placeholder="यहाँ लिखें..."
                className="w-full p-4 text-3xl text-center border-2 border-purple-200 rounded-xl focus:border-purple-500 focus:outline-none"
                autoFocus
              />
            </Card>

            <Button
              type="submit"
              variant="primary"
              size="lg"
              className="w-full"
              disabled={!userInput.trim()}
            >
              जाँच करें ✓
            </Button>
          </form>

          {/* Progress hint */}
          <p className="text-center text-sm text-gray-500 mt-4">
            {attempts === 0 
              ? 'पूरे 40 अंक आपके! 🏆' 
              : attempts === 1 
                ? '25 अंक बचे! 🎯' 
                : '10 अंक बचे! 💪'}
          </p>
        </motion.div>
      </div>
    </div>
  );
}
