'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { ArrowLeft, Video, Calendar, Clock, Users, Star, Lock } from 'lucide-react';
import { MainLayout } from '@/components/layout';
import { Card, Loading } from '@/components/ui';
import { useAuthStore } from '@/stores';
import { useSubscription } from '@/hooks/useSubscription';
import { fadeInUp, staggerContainer } from '@/lib/constants';

interface LiveClass {
  id: string;
  title: string;
  description: string;
  instructor: string;
  date: string;
  time: string;
  duration: string;
  spots: number;
  maxSpots: number;
  level: 'Beginner' | 'Intermediate' | 'Advanced';
  language: string;
}

// Mock data for live classes
const UPCOMING_CLASSES: LiveClass[] = [
  {
    id: '1',
    title: 'Hindi Conversation Practice',
    description: 'Practice everyday Hindi conversations with native speakers',
    instructor: 'Priya Sharma',
    date: 'Tomorrow',
    time: '4:00 PM',
    duration: '45 min',
    spots: 3,
    maxSpots: 8,
    level: 'Beginner',
    language: 'Hindi',
  },
  {
    id: '2',
    title: 'Tamil Story Reading',
    description: 'Read and discuss traditional Tamil folk stories',
    instructor: 'Karthik Rajan',
    date: 'Saturday',
    time: '10:00 AM',
    duration: '60 min',
    spots: 5,
    maxSpots: 10,
    level: 'Intermediate',
    language: 'Tamil',
  },
  {
    id: '3',
    title: 'Telugu Alphabet Fun',
    description: 'Learn Telugu letters through songs and games',
    instructor: 'Lakshmi Devi',
    date: 'Sunday',
    time: '11:00 AM',
    duration: '30 min',
    spots: 2,
    maxSpots: 6,
    level: 'Beginner',
    language: 'Telugu',
  },
];

export default function LiveClassesPage() {
  const router = useRouter();
  const [isHydrated, setIsHydrated] = useState(false);
  const { isAuthenticated } = useAuthStore();
  const subscription = useSubscription();

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (isHydrated && !isAuthenticated) {
      router.push('/login?redirect=/live-classes');
    }
  }, [isHydrated, isAuthenticated, router]);

  if (!isHydrated || !isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading size="lg" text="Loading..." />
      </div>
    );
  }

  const isPremium = subscription.tier === 'PREMIUM';

  const handleBookClass = (classId: string) => {
    if (!isPremium) {
      router.push('/pricing');
      return;
    }
    // TODO: Implement booking logic
    alert('Booking feature coming soon!');
  };

  return (
    <MainLayout>
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-6"
      >
        {/* Header */}
        <motion.div variants={fadeInUp} className="flex items-center gap-4">
          <button
            onClick={() => router.back()}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <ArrowLeft size={24} />
          </button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Live Classes</h1>
            <p className="text-gray-500">Learn with expert instructors</p>
          </div>
        </motion.div>

        {/* Premium Banner (for non-premium users) */}
        {!isPremium && (
          <motion.div variants={fadeInUp}>
            <Card className="bg-gradient-to-r from-purple-500 to-pink-500 text-white">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
                  <Lock size={24} />
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-lg">Premium Feature</h3>
                  <p className="text-white/90 text-sm">
                    Upgrade to Premium to book live classes with expert instructors
                  </p>
                </div>
                <button
                  onClick={() => router.push('/pricing')}
                  className="bg-white text-purple-600 px-4 py-2 rounded-full font-bold hover:shadow-lg transition-all"
                >
                  Upgrade
                </button>
              </div>
            </Card>
          </motion.div>
        )}

        {/* Stats for Premium users */}
        {isPremium && (
          <motion.div variants={fadeInUp}>
            <Card className="bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                    <Video className="w-5 h-5 text-green-600" />
                  </div>
                  <div>
                    <p className="font-medium text-green-700">Your Classes</p>
                    <p className="text-sm text-gray-500">3 free classes this month</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-green-600">3</p>
                  <p className="text-xs text-gray-500">remaining</p>
                </div>
              </div>
            </Card>
          </motion.div>
        )}

        {/* Upcoming Classes */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-4">Upcoming Classes</h2>
          <div className="space-y-4">
            {UPCOMING_CLASSES.map((liveClass, index) => (
              <motion.div
                key={liveClass.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="hover:shadow-md transition-shadow">
                  <div className="flex flex-col sm:flex-row sm:items-center gap-4">
                    {/* Class Info */}
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className={`px-2 py-0.5 text-xs font-medium rounded-full ${
                          liveClass.level === 'Beginner' ? 'bg-green-100 text-green-700' :
                          liveClass.level === 'Intermediate' ? 'bg-yellow-100 text-yellow-700' :
                          'bg-red-100 text-red-700'
                        }`}>
                          {liveClass.level}
                        </span>
                        <span className="text-xs text-gray-500">{liveClass.language}</span>
                      </div>
                      <h3 className="font-bold text-gray-900">{liveClass.title}</h3>
                      <p className="text-sm text-gray-500 mt-1">{liveClass.description}</p>
                      <div className="flex items-center gap-4 mt-3 text-sm text-gray-600">
                        <span className="flex items-center gap-1">
                          <Calendar size={14} />
                          {liveClass.date}
                        </span>
                        <span className="flex items-center gap-1">
                          <Clock size={14} />
                          {liveClass.time} ({liveClass.duration})
                        </span>
                        <span className="flex items-center gap-1">
                          <Users size={14} />
                          {liveClass.spots}/{liveClass.maxSpots} spots
                        </span>
                      </div>
                      <div className="flex items-center gap-2 mt-2">
                        <Star size={14} className="text-yellow-500 fill-yellow-500" />
                        <span className="text-sm text-gray-600">with {liveClass.instructor}</span>
                      </div>
                    </div>

                    {/* Book Button */}
                    <div className="sm:text-right">
                      <button
                        onClick={() => handleBookClass(liveClass.id)}
                        className={`w-full sm:w-auto px-6 py-2 rounded-xl font-semibold transition-all ${
                          isPremium
                            ? 'bg-purple-500 hover:bg-purple-600 text-white'
                            : 'bg-gray-100 text-gray-400 cursor-not-allowed'
                        }`}
                        disabled={!isPremium}
                      >
                        {isPremium ? 'Book Now' : 'Premium Only'}
                      </button>
                      {liveClass.spots <= 3 && (
                        <p className="text-xs text-orange-500 mt-1">Only {liveClass.spots} spots left!</p>
                      )}
                    </div>
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Coming Soon Section */}
        <motion.div variants={fadeInUp}>
          <Card className="bg-gray-50 text-center py-8">
            <div className="text-4xl mb-3">🎬</div>
            <h3 className="font-bold text-gray-900 mb-2">More Classes Coming Soon!</h3>
            <p className="text-gray-500 text-sm max-w-md mx-auto">
              We&apos;re adding more live classes in various languages including Gujarati, Marathi, Bengali, and more.
            </p>
          </Card>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
}
