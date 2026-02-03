'use client';

import { motion } from 'framer-motion';
import { ChallengeResultResponse } from '@/lib/api';
import { ShareButton } from './ShareButton';

interface ChallengeResultProps {
  result: ChallengeResultResponse;
  onViewLeaderboard: () => void;
  onPlayAgain: () => void;
}

export function ChallengeResult({ result, onViewLeaderboard, onPlayAgain }: ChallengeResultProps) {
  const isPerfect = result.percentage === 100;
  const isGood = result.percentage >= 80;
  const isMedium = result.percentage >= 50;

  const emoji = isPerfect ? '🏆' : isGood ? '🌟' : isMedium ? '👍' : '💪';
  const message = isPerfect
    ? 'Perfect Score!'
    : isGood
    ? 'Great Job!'
    : isMedium
    ? 'Good Try!'
    : 'Keep Practicing!';

  const bgGradient = isPerfect
    ? 'from-yellow-400 to-orange-500'
    : isGood
    ? 'from-green-400 to-emerald-500'
    : isMedium
    ? 'from-blue-400 to-indigo-500'
    : 'from-purple-400 to-pink-500';

  return (
    <div className={`min-h-screen bg-gradient-to-b ${bgGradient} p-4`}>
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="max-w-lg mx-auto"
      >
        {/* Result Card */}
        <div className="bg-white rounded-3xl shadow-2xl p-8 text-center mb-6">
          {/* Trophy/Badge animation */}
          <motion.div
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ type: 'spring', duration: 0.8, delay: 0.2 }}
            className="text-8xl mb-4"
          >
            {emoji}
          </motion.div>

          <h1 className="text-3xl font-bold text-gray-900 mb-2">{message}</h1>
          <p className="text-gray-500 mb-6">{result.challenge_title}</p>

          {/* Score */}
          <div className="bg-gray-50 rounded-2xl p-6 mb-6">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.4 }}
              className="text-5xl font-bold text-gray-900 mb-2"
            >
              {result.score}/{result.max_score}
            </motion.div>
            <div className="text-2xl font-semibold text-purple-600">
              {result.percentage}%
            </div>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="bg-purple-50 rounded-xl p-4">
              <div className="text-3xl font-bold text-purple-600">#{result.rank}</div>
              <div className="text-sm text-gray-500">Your Rank</div>
            </div>
            <div className="bg-pink-50 rounded-xl p-4">
              <div className="text-3xl font-bold text-pink-600">
                {Math.floor(result.time_taken_seconds / 60)}:{(result.time_taken_seconds % 60).toString().padStart(2, '0')}
              </div>
              <div className="text-sm text-gray-500">Time</div>
            </div>
          </div>

          {/* Total participants */}
          <p className="text-gray-500 mb-6">
            You beat <span className="font-semibold text-purple-600">{result.total_participants - result.rank}</span> of {result.total_participants} players!
          </p>

          {/* Actions */}
          <div className="space-y-3">
            <ShareButton
              url={result.share_url}
              title={`I scored ${result.percentage}% on ${result.challenge_title}!`}
              className="w-full"
            />

            <button
              onClick={onViewLeaderboard}
              className="w-full py-3 px-4 bg-purple-100 hover:bg-purple-200 text-purple-700 rounded-full font-semibold transition-colors"
            >
              View Leaderboard
            </button>

            <button
              onClick={onPlayAgain}
              className="w-full py-3 px-4 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full font-semibold transition-colors"
            >
              Play Again
            </button>
          </div>
        </div>

        {/* Question breakdown */}
        <div className="bg-white/80 backdrop-blur rounded-2xl p-4">
          <h3 className="font-semibold text-gray-700 mb-3">Question Breakdown</h3>
          <div className="flex flex-wrap gap-2">
            {result.detailed_results.map((r, i) => (
              <div
                key={i}
                className={`w-10 h-10 rounded-full flex items-center justify-center text-lg font-bold ${
                  r.correct
                    ? 'bg-green-500 text-white'
                    : 'bg-red-500 text-white'
                }`}
              >
                {r.correct ? '✓' : '✗'}
              </div>
            ))}
          </div>
        </div>
      </motion.div>
    </div>
  );
}
