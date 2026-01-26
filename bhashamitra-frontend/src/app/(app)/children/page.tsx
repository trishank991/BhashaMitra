'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { useAuthStore } from '@/stores';
import { MainLayout } from '@/components/layout';
import { Loading } from '@/components/ui';
import { fadeInUp, staggerContainer } from '@/lib/constants';
import { ChildProfile } from '@/types';

export default function ChildrenPage() {
  const router = useRouter();
  const [isHydrated, setIsHydrated] = useState(false);
  const { isAuthenticated, children, activeChild, setActiveChild, fetchChildren } = useAuthStore();

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (!isHydrated) return;
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    fetchChildren();
  }, [isHydrated, isAuthenticated, router, fetchChildren]);

  if (!isHydrated || !isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading size="lg" text="Loading..." />
      </div>
    );
  }

  const handleSelectChild = (child: ChildProfile) => {
    setActiveChild(child);
    router.push('/home');
  };

  return (
    <MainLayout headerTitle="My Children" showBack onBack={() => router.back()}>
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-4"
      >
        <motion.div variants={fadeInUp}>
          <h1 className="text-2xl font-bold text-gray-900">My Children</h1>
          <p className="text-sm text-gray-500 mt-1">Manage your children&apos;s profiles and learning</p>
        </motion.div>

        {children.length === 0 ? (
          <motion.div variants={fadeInUp} className="text-center py-12">
            <span className="text-5xl block mb-4">👶</span>
            <h2 className="text-lg font-semibold text-gray-800 mb-2">No children added yet</h2>
            <p className="text-gray-500 mb-6">Add your first child to start their language learning journey!</p>
            <Link
              href="/children/add"
              className="inline-block px-6 py-3 bg-primary-500 text-white rounded-xl font-medium hover:bg-primary-600 transition-colors"
            >
              Add Child
            </Link>
          </motion.div>
        ) : (
          <div className="space-y-3">
            {children.map((child) => (
              <motion.div key={child.id} variants={fadeInUp}>
                <button
                  onClick={() => handleSelectChild(child)}
                  className={`w-full text-left p-4 rounded-xl border-2 transition-all ${
                    activeChild?.id === child.id
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 bg-white hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div className="text-3xl">{child.avatar || '👤'}</div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <h3 className="font-semibold text-gray-900">{child.name}</h3>
                        {activeChild?.id === child.id && (
                          <span className="text-xs bg-primary-500 text-white px-2 py-0.5 rounded-full">Active</span>
                        )}
                      </div>
                      <p className="text-sm text-gray-500">Age {child.age} &middot; Level {child.level}</p>
                    </div>
                    <Link
                      href={`/children/${child.id}`}
                      onClick={(e) => e.stopPropagation()}
                      className="p-2 text-gray-400 hover:text-gray-600"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                        <path strokeLinecap="round" strokeLinejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
                      </svg>
                    </Link>
                  </div>
                </button>
              </motion.div>
            ))}

            <motion.div variants={fadeInUp}>
              <Link
                href="/children/add"
                className="flex items-center justify-center gap-2 w-full p-4 rounded-xl border-2 border-dashed border-gray-300 text-gray-500 hover:border-primary-300 hover:text-primary-500 transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                </svg>
                Add Another Child
              </Link>
            </motion.div>
          </div>
        )}
      </motion.div>
    </MainLayout>
  );
}
