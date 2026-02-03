'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { MainLayout } from '@/components/layout';
import { Card, Button, Avatar, Badge, Loading } from '@/components/ui';
import { useAuthStore } from '@/stores';
import { fadeInUp, staggerContainer, SUPPORTED_LANGUAGES } from '@/lib/constants';

export default function ProfilePage() {
  const router = useRouter();
  const [isHydrated, setIsHydrated] = useState(false);
  const { user, activeChild, children, logout, setActiveChild, isAuthenticated } = useAuthStore();

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    if (isHydrated && !isAuthenticated) {
      router.push('/login');
    }
  }, [isHydrated, isAuthenticated, router]);

  if (!isHydrated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading size="lg" text="Loading..." />
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loading size="lg" text="Redirecting..." />
      </div>
    );
  }

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  const languageInfo = activeChild?.language
    ? SUPPORTED_LANGUAGES[activeChild.language.code]
    : null;

  return (
    <MainLayout headerTitle="Profile" showProgress={false}>
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-6"
      >
        {/* Current Child Profile */}
        {activeChild && (
          <motion.div variants={fadeInUp}>
            <Card className="text-center">
              <Avatar
                emoji={activeChild.avatar || '🐯'}
                size="xl"
                className="mx-auto mb-4"
              />
              <h2 className="text-2xl font-bold text-gray-900">{activeChild.name}</h2>
              {languageInfo && (
                <p className="text-gray-500 mt-1">
                  Learning {languageInfo.flag} {languageInfo.name}
                </p>
              )}
              <div className="flex justify-center gap-2 mt-4">
                <Badge variant="primary" icon="⭐">
                  Level {activeChild.level || 1}
                </Badge>
                <Badge variant="secondary" icon="🔥">
                  {activeChild.streak || 0} Day Streak
                </Badge>
              </div>
            </Card>
          </motion.div>
        )}

        {/* Switch Child (if parent has multiple children) */}
        {children.length > 1 && (
          <motion.div variants={fadeInUp}>
            <h2 className="text-lg font-bold text-gray-900 mb-3">Switch Profile</h2>
            <div className="flex gap-3 overflow-x-auto pb-2">
              {children.map((child) => (
                <button
                  key={child.id}
                  onClick={() => setActiveChild(child)}
                  className={`flex-shrink-0 flex flex-col items-center p-3 rounded-2xl transition-all ${
                    activeChild?.id === child.id
                      ? 'bg-primary-100 ring-2 ring-primary-500'
                      : 'bg-gray-100 hover:bg-gray-200'
                  }`}
                >
                  <Avatar emoji={child.avatar || '🐯'} size="lg" />
                  <span className="text-sm font-medium mt-2">{child.name}</span>
                </button>
              ))}
            </div>
          </motion.div>
        )}

        {/* Settings */}
        <motion.div variants={fadeInUp}>
          <h2 className="text-lg font-bold text-gray-900 mb-3">Settings</h2>
          <div className="space-y-2">
            <Card interactive className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-2xl">🌐</span>
                <span className="font-medium">Language Settings</span>
              </div>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
                className="w-5 h-5 text-gray-400"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="m8.25 4.5 7.5 7.5-7.5 7.5"
                />
              </svg>
            </Card>

            <Card interactive className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-2xl">🔔</span>
                <span className="font-medium">Notifications</span>
              </div>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
                className="w-5 h-5 text-gray-400"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="m8.25 4.5 7.5 7.5-7.5 7.5"
                />
              </svg>
            </Card>

            <Card interactive className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-2xl">👨‍👩‍👧</span>
                <span className="font-medium">Parent Dashboard</span>
              </div>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
                className="w-5 h-5 text-gray-400"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="m8.25 4.5 7.5 7.5-7.5 7.5"
                />
              </svg>
            </Card>

            <Card interactive className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-2xl">❓</span>
                <span className="font-medium">Help & Support</span>
              </div>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
                className="w-5 h-5 text-gray-400"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="m8.25 4.5 7.5 7.5-7.5 7.5"
                />
              </svg>
            </Card>
          </div>
        </motion.div>

        {/* Account Info */}
        {user && (
          <motion.div variants={fadeInUp}>
            <h2 className="text-lg font-bold text-gray-900 mb-3">Account</h2>
            <Card>
              <div className="flex items-center gap-4 mb-4">
                <Avatar name={user.name} size="lg" />
                <div>
                  <p className="font-bold text-gray-900">{user.name}</p>
                  <p className="text-sm text-gray-500">{user.email}</p>
                </div>
              </div>
              <Badge variant="accent">Parent Account</Badge>
            </Card>
          </motion.div>
        )}

        {/* Logout */}
        <motion.div variants={fadeInUp}>
          <Button
            variant="outline"
            size="lg"
            className="w-full text-error-500 border-error-200 hover:bg-error-50"
            onClick={handleLogout}
          >
            Log Out
          </Button>
        </motion.div>

        {/* App Info */}
        <motion.div variants={fadeInUp} className="text-center pt-4 pb-8">
          <p className="text-sm text-gray-400">BhashaMitra v1.0.0</p>
          <p className="text-xs text-gray-300 mt-1">Made with love for diaspora families</p>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
}
