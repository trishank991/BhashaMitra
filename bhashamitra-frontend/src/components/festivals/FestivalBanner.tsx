'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Calendar, Sparkles, ChevronRight, Star } from 'lucide-react';
import { Festival } from '@/types';
import api from '@/lib/api';

interface FestivalBannerProps {
  language?: string;
  onFestivalClick?: (festival: Festival) => void;
  className?: string;
}

const RELIGION_COLORS: Record<string, { bg: string; text: string; accent: string }> = {
  HINDU: { bg: 'from-orange-500 to-red-500', text: 'text-white', accent: 'bg-yellow-400' },
  MUSLIM: { bg: 'from-green-500 to-emerald-600', text: 'text-white', accent: 'bg-white' },
  SIKH: { bg: 'from-amber-500 to-orange-500', text: 'text-white', accent: 'bg-blue-500' },
  CHRISTIAN: { bg: 'from-blue-500 to-indigo-600', text: 'text-white', accent: 'bg-yellow-400' },
  JAIN: { bg: 'from-purple-500 to-pink-500', text: 'text-white', accent: 'bg-white' },
  BUDDHIST: { bg: 'from-yellow-500 to-amber-600', text: 'text-gray-900', accent: 'bg-red-500' },
};

const RELIGION_ICONS: Record<string, string> = {
  HINDU: '/icons/festivals/diya.png',
  MUSLIM: '/icons/festivals/moon.png',
  SIKH: '/icons/festivals/khanda.png',
  CHRISTIAN: '/icons/festivals/star.png',
  JAIN: '/icons/festivals/ahimsa.png',
  BUDDHIST: '/icons/festivals/wheel.png',
};

export function FestivalBanner({ language, onFestivalClick, className = '' }: FestivalBannerProps) {
  const [upcomingFestivals, setUpcomingFestivals] = useState<Festival[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUpcoming = async () => {
      setLoading(true);
      const response = await api.getUpcomingFestivals();
      if (response.success && response.data) {
        setUpcomingFestivals(response.data.slice(0, 5));
      }
      setLoading(false);
    };
    fetchUpcoming();
  }, []);

  useEffect(() => {
    if (upcomingFestivals.length <= 1) return;

    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % upcomingFestivals.length);
    }, 5000);

    return () => clearInterval(interval);
  }, [upcomingFestivals.length]);

  if (loading) {
    return (
      <div className={`animate-pulse bg-gradient-to-r from-gray-200 to-gray-300 rounded-2xl h-32 ${className}`} />
    );
  }

  if (upcomingFestivals.length === 0) {
    return null;
  }

  const currentFestival = upcomingFestivals[currentIndex];
  const colors = RELIGION_COLORS[currentFestival.religion] || RELIGION_COLORS.HINDU;
  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  return (
    <div className={`relative overflow-hidden rounded-2xl ${className}`}>
      <AnimatePresence mode="wait">
        <motion.div
          key={currentFestival.id}
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -50 }}
          transition={{ duration: 0.5 }}
          className={`bg-gradient-to-r ${colors.bg} p-6 cursor-pointer`}
          onClick={() => onFestivalClick?.(currentFestival)}
        >
          {/* Decorative elements */}
          <div className="absolute top-2 right-2 opacity-20">
            <Sparkles className="w-16 h-16 text-white" />
          </div>
          <div className="absolute bottom-2 left-2 opacity-20">
            <Star className="w-12 h-12 text-white" />
          </div>

          <div className="relative z-10 flex items-center justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <Calendar className={`w-5 h-5 ${colors.text}`} />
                <span className={`text-sm font-medium ${colors.text} opacity-90`}>
                  Upcoming Festival - {monthNames[currentFestival.typical_month - 1]}
                </span>
              </div>

              <h3 className={`text-2xl font-bold ${colors.text} mb-1`}>
                {currentFestival.localized_name || currentFestival.name}
              </h3>

              {currentFestival.name_native && (
                <p className={`text-lg ${colors.text} opacity-90 mb-2`}>
                  {currentFestival.name_native}
                </p>
              )}

              <p className={`text-sm ${colors.text} opacity-80 line-clamp-2 max-w-md`}>
                {currentFestival.description}
              </p>

              <div className="flex items-center gap-4 mt-3">
                {currentFestival.activity_count !== undefined && currentFestival.activity_count > 0 && (
                  <span className={`text-xs ${colors.text} opacity-80 bg-white/20 px-2 py-1 rounded-full`}>
                    {currentFestival.activity_count} Activities
                  </span>
                )}
                {currentFestival.story_count !== undefined && currentFestival.story_count > 0 && (
                  <span className={`text-xs ${colors.text} opacity-80 bg-white/20 px-2 py-1 rounded-full`}>
                    {currentFestival.story_count} Stories
                  </span>
                )}
              </div>
            </div>

            <div className="flex flex-col items-center gap-2">
              <motion.div
                whileHover={{ scale: 1.1 }}
                className={`${colors.accent} p-3 rounded-full`}
              >
                <ChevronRight className="w-6 h-6 text-gray-800" />
              </motion.div>
              <span className={`text-xs ${colors.text} opacity-70`}>Explore</span>
            </div>
          </div>
        </motion.div>
      </AnimatePresence>

      {/* Pagination dots */}
      {upcomingFestivals.length > 1 && (
        <div className="absolute bottom-2 left-1/2 -translate-x-1/2 flex gap-2">
          {upcomingFestivals.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentIndex(index)}
              className={`w-2 h-2 rounded-full transition-all ${
                index === currentIndex
                  ? 'bg-white w-4'
                  : 'bg-white/50'
              }`}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default FestivalBanner;
