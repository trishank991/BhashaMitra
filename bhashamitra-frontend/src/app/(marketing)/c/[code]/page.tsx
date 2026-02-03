'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { motion } from 'framer-motion';
import api, { PublicChallengeResponse, ChallengeResultResponse, ChallengeLeaderboardResponse } from '@/lib/api';
import { ChallengeQuiz } from '@/components/challenges/ChallengeQuiz';
import { ChallengeResult } from '@/components/challenges/ChallengeResult';
import { ChallengeLeaderboard } from '@/components/challenges/ChallengeLeaderboard';
import { Loading } from '@/components/ui';

type GameState = 'loading' | 'intro' | 'playing' | 'result' | 'leaderboard' | 'expired' | 'error';

export default function ChallengePlayPage() {
  const params = useParams();
  const code = (params.code as string).toUpperCase();

  const [gameState, setGameState] = useState<GameState>('loading');
  const [challenge, setChallenge] = useState<PublicChallengeResponse | null>(null);
  const [attemptId, setAttemptId] = useState<string | null>(null);
  const [result, setResult] = useState<ChallengeResultResponse | null>(null);
  const [leaderboard, setLeaderboard] = useState<ChallengeLeaderboardResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Participant info
  const [participantName, setParticipantName] = useState('');
  const [participantLocation, setParticipantLocation] = useState('');

  // Fetch challenge on mount
  useEffect(() => {
    const fetchChallenge = async () => {
      const response = await api.getPublicChallenge(code);
      if (response.success && response.data) {
        // Access nested data structure: response.data.data contains the challenge
        const challengeData = (response.data as any).data;
        if (challengeData?.is_expired) {
          setGameState('expired');
        } else if (challengeData) {
          setChallenge(challengeData);
          setGameState('intro');
        } else {
          setError('Challenge not found');
          setGameState('error');
        }
      } else {
        setError(response.error || 'Challenge not found');
        setGameState('error');
      }
    };
    fetchChallenge();
  }, [code]);

  const handleStart = async () => {
    if (!participantName.trim()) return;

    const response = await api.startChallengeAttempt(code, {
      participant_name: participantName.trim(),
      participant_location: participantLocation.trim(),
    });

    if (response.success && response.data) {
      // Access nested data structure: response.data.data contains { attempt_id, challenge, started_at }
      const data = (response.data as any).data;
      if (data) {
        setAttemptId(data.attempt_id);
        setChallenge(data.challenge);
        setGameState('playing');
      } else {
        setError('Failed to start challenge');
      }
    } else {
      setError(response.error || 'Failed to start challenge');
    }
  };

  const handleComplete = async (answers: number[], timeTaken: number) => {
    if (!attemptId) return;

    const response = await api.submitChallengeAnswers({
      attempt_id: attemptId,
      answers,
      time_taken_seconds: timeTaken,
    });

    if (response.success && response.data) {
      // Access nested data structure: response.data.data contains the result
      const resultData = (response.data as any).data;
      if (resultData) {
        setResult(resultData);
        setGameState('result');
      } else {
        setError('Failed to submit answers');
        setGameState('error');
      }
    } else {
      setError(response.error || 'Failed to submit answers');
      setGameState('error');
    }
  };

  const handleViewLeaderboard = async () => {
    const response = await api.getChallengeLeaderboard(code);
    if (response.success && response.data) {
      // Access nested data structure: response.data.data contains the leaderboard
      const leaderboardData = (response.data as any).data;
      if (leaderboardData) {
        setLeaderboard(leaderboardData);
        setGameState('leaderboard');
      }
    }
  };

  const handlePlayAgain = () => {
    setAttemptId(null);
    setResult(null);
    setGameState('intro');
  };

  // Loading state
  if (gameState === 'loading') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-purple-100 to-pink-100">
        <Loading size="lg" text="Loading challenge..." />
      </div>
    );
  }

  // Error state
  if (gameState === 'error') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-purple-100 to-pink-100 p-4">
        <div className="bg-white rounded-3xl shadow-xl p-8 text-center max-w-sm">
          <div className="text-6xl mb-4">😔</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Oops!</h1>
          <p className="text-gray-500 mb-6">{error || 'Something went wrong'}</p>
          <a
            href="/"
            className="inline-block px-6 py-3 bg-purple-500 hover:bg-purple-600 text-white rounded-full font-semibold"
          >
            Go Home
          </a>
        </div>
      </div>
    );
  }

  // Expired state
  if (gameState === 'expired') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-gray-100 to-gray-200 p-4">
        <div className="bg-white rounded-3xl shadow-xl p-8 text-center max-w-sm">
          <div className="text-6xl mb-4">⏰</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Challenge Expired</h1>
          <p className="text-gray-500 mb-6">This challenge is no longer available.</p>
          <a
            href="/"
            className="inline-block px-6 py-3 bg-purple-500 hover:bg-purple-600 text-white rounded-full font-semibold"
          >
            Explore PeppiAcademy
          </a>
        </div>
      </div>
    );
  }

  // Intro/Registration state
  if (gameState === 'intro' && challenge) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-purple-100 to-pink-100 p-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-lg mx-auto pt-8"
        >
          {/* Challenge Header */}
          <div className="bg-white rounded-3xl shadow-xl p-6 mb-6 text-center">
            <div className="text-5xl mb-4">🎯</div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">{challenge.title}</h1>
            {challenge.title_native && (
              <p className="text-lg text-purple-600 mb-4">{challenge.title_native}</p>
            )}

            <div className="flex items-center justify-center gap-4 text-sm text-gray-500 mb-4">
              <span>{challenge.question_count} Questions</span>
              <span>•</span>
              <span>{challenge.time_limit_seconds}s each</span>
              <span>•</span>
              <span className="capitalize">{challenge.difficulty}</span>
            </div>

            <div className="bg-gray-50 rounded-xl p-4">
              <p className="text-sm text-gray-600">
                Challenge by <span className="font-semibold text-purple-600">{challenge.creator_name}</span>
              </p>
              <p className="text-sm text-gray-500">
                {challenge.language_name} • {challenge.category}
              </p>
            </div>
          </div>

          {/* Registration Form */}
          <div className="bg-white rounded-3xl shadow-xl p-6">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Enter Your Name</h2>

            <input
              type="text"
              value={participantName}
              onChange={(e) => setParticipantName(e.target.value)}
              placeholder="Your name"
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 mb-3"
              maxLength={50}
              autoFocus
            />

            <input
              type="text"
              value={participantLocation}
              onChange={(e) => setParticipantLocation(e.target.value)}
              placeholder="Your city (optional)"
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 mb-6"
              maxLength={50}
            />

            <button
              onClick={handleStart}
              disabled={!participantName.trim()}
              className="w-full py-4 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 disabled:from-gray-300 disabled:to-gray-400 text-white rounded-xl font-bold text-lg transition-all shadow-lg"
            >
              Start Challenge
            </button>

            <p className="text-center text-xs text-gray-400 mt-4">
              No signup required - just enter your name and play!
            </p>
          </div>
        </motion.div>
      </div>
    );
  }

  // Playing state
  if (gameState === 'playing' && challenge) {
    return <ChallengeQuiz challenge={challenge} onComplete={handleComplete} />;
  }

  // Result state
  if (gameState === 'result' && result) {
    return (
      <ChallengeResult
        result={result}
        onViewLeaderboard={handleViewLeaderboard}
        onPlayAgain={handlePlayAgain}
      />
    );
  }

  // Leaderboard state
  if (gameState === 'leaderboard' && leaderboard) {
    return (
      <ChallengeLeaderboard
        leaderboard={leaderboard}
        myAttemptId={attemptId || undefined}
        onBack={() => setGameState('result')}
      />
    );
  }

  return null;
}
