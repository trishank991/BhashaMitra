'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { Loader2, Users, BookOpen, Globe } from 'lucide-react';
import { api } from '@/lib/api';

// Types
interface FamilyInfo {
  name: string;
  member_count: number;
}

// Animation variants
const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.5 }
};

const stagger = {
  animate: {
    transition: {
      staggerChildren: 0.1
    }
  }
};

// Language benefits
const LANGUAGE_BENEFITS = [
  'Communicate with your family in your native language',
  'Pass down cultural traditions and stories',
  'Build stronger connections across generations'
];

export default function JoinFamilyPage({ params }: { params: { code: string } }) {
  const router = useRouter();
  const [familyInfo, setFamilyInfo] = useState<FamilyInfo | null>(null);
  const [isLoading, setIsLoading] = useState({ fetching: true, joining: false });
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchFamilyInfo();
  }, [params.code]);

  const fetchFamilyInfo = async () => {
    try {
      setIsLoading(prev => ({ ...prev, fetching: true }));
      const response = await api.validateFamilyCode(params.code);
      
      if (!response.success || !response.data) {
        throw new Error(response.error || 'Invalid invitation code');
      }
      
      setFamilyInfo(response.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load family information');
    } finally {
      setIsLoading(prev => ({ ...prev, fetching: false }));
    }
  };

  const handleJoinFamily = async () => {
    try {
      setIsLoading(prev => ({ ...prev, joining: true }));
      const response = await api.joinFamilyViaCode(params.code);

      if (!response.success) {
        throw new Error(response.error || 'Failed to join family');
      }

      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to join family');
    } finally {
      setIsLoading(prev => ({ ...prev, joining: false }));
    }
  };

  if (isLoading.fetching) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 text-center"
        >
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-3xl">❌</span>
          </div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Oops!</h1>
          <p className="text-gray-600 mb-6">{error}</p>
          <Link
            href="/"
            className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            ← Back to Home
          </Link>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 py-12 px-4">
      <motion.div
        initial="initial"
        animate="animate"
        variants={stagger}
        className="max-w-4xl mx-auto"
      >
        {/* Header */}
        <motion.div variants={fadeInUp} className="text-center mb-12">
          <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-6">
            <span className="text-4xl">👨‍👩‍👧‍👦</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            You have been invited!
          </h1>
          <p className="text-xl text-gray-600">
            Someone wants you to join their family group on PeppiAcademy
          </p>
        </motion.div>

        {/* Family Info Card */}
        {familyInfo && (
          <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-xl p-8 mb-8">
            <div className="flex items-center gap-4 mb-6">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                <Users className="w-8 h-8 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-900">
                  {familyInfo.name}
                </h2>
                <p className="text-gray-600">
                  {familyInfo.member_count} {familyInfo.member_count === 1 ? 'member' : 'members'} · Ready to learn together
                </p>
              </div>
            </div>

            <div className="border-t pt-6">
              <p className="text-gray-700 mb-4">
                <strong>Family Challenge:</strong> There is an active challenge waiting for you!
              </p>
            </div>
          </motion.div>
        )}

        {/* Benefits Section */}
        <motion.div variants={fadeInUp} className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Globe className="w-6 h-6 text-blue-600" />
            What you will do:
          </h3>
          <ul className="space-y-3">
            {LANGUAGE_BENEFITS.map((benefit, i) => (
              <li key={i} className="flex items-start gap-3">
                <span className="text-green-600 text-xl mt-0.5">✓</span>
                <span className="text-gray-700">{benefit}</span>
              </li>
            ))}
          </ul>
        </motion.div>

        {/* Action Buttons */}
        <motion.div variants={fadeInUp} className="flex flex-col sm:flex-row gap-4">
          <button
            onClick={handleJoinFamily}
            disabled={isLoading.joining}
            className="flex-1 flex items-center justify-center gap-2 px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold text-lg hover:shadow-lg transition-all disabled:opacity-50"
          >
            {isLoading.joining ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Joining...
              </>
            ) : (
              <>
                <BookOpen className="w-5 h-5" />
                Join {familyInfo?.name}
              </>
            )}
          </button>
        </motion.div>

        {/* Footer */}
        <motion.div variants={fadeInUp} className="text-center mt-8">
          <p className="text-gray-600">
            Already have an account?{' '}
            <Link href="/login" className="text-blue-600 hover:underline font-medium">
              Log In
            </Link>
          </p>
        </motion.div>

        {/* Back Link */}
        <motion.div variants={fadeInUp} className="text-center mt-6">
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-900"
          >
            ← Back to PeppiAcademy
          </Link>
        </motion.div>
      </motion.div>
    </div>
  );
}


  