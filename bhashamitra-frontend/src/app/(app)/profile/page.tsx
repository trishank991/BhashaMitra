'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { MainLayout } from '@/components/layout';
import { Card, Button, Avatar, Badge, Loading, SubscriptionBadge } from '@/components/ui';
import { SubscriptionTier } from '@/types';
import { useAuthStore } from '@/stores';
import { fadeInUp, staggerContainer, SUPPORTED_LANGUAGES } from '@/lib/constants';
import api from '@/lib/api';

export default function ProfilePage() {
  const router = useRouter();
  const [isHydrated, setIsHydrated] = useState(false);
  const [portalLoading, setPortalLoading] = useState(false);
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

  const handleManageSubscription = async () => {
    setPortalLoading(true);
    try {
      const response = await api.createCustomerPortal(window.location.href);
      if (response.success && response.data) {
        window.location.href = response.data.url;
      }
    } catch (error) {
      console.error('Failed to open subscription portal:', error);
    } finally {
      setPortalLoading(false);
    }
  };

  // Handle both string and object formats from API
  const languageCode = activeChild?.language
    ? (typeof activeChild.language === 'string' ? activeChild.language : activeChild.language.code)
    : null;
  const languageInfo = languageCode
    ? SUPPORTED_LANGUAGES[languageCode as keyof typeof SUPPORTED_LANGUAGES]
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

            <Card interactive onClick={() => router.push('/help')} className="flex items-center justify-between">
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
              <div className="flex gap-2">
                <Badge variant="accent">Parent Account</Badge>
                <SubscriptionBadge tier={user.subscription_tier as SubscriptionTier || 'FREE'} />
              </div>
            </Card>
          </motion.div>
        )}

        {/* Subscription */}
        {user && (
          <motion.div variants={fadeInUp}>
            <h2 className="text-lg font-bold text-gray-900 mb-3">Subscription</h2>
            <Card className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">Current Plan</p>
                  <p className="text-sm text-gray-500">
                    {user.subscription_info?.description || 'Pre-cached content only'}
                  </p>
                </div>
                <SubscriptionBadge
                  tier={user.subscription_tier as SubscriptionTier || 'FREE'}
                  size="lg"
                />
              </div>

              {user.subscription_tier === 'FREE' && (
                <div className="bg-gradient-to-r from-primary-50 to-secondary-50 rounded-xl p-4">
                  <p className="font-medium text-gray-900 mb-2">Upgrade for more features</p>
                  <div className="space-y-2 text-sm text-gray-600">
                    <p>Standard (NZD $20/month): Unlimited games, L1-L10 curriculum, Peppi AI</p>
                    <p>Premium (NZD $30/month): Live classes, premium voices, priority support</p>
                  </div>
                  <Button
                    variant="primary"
                    size="sm"
                    className="mt-3"
                    onClick={() => router.push('/pricing')}
                  >
                    Upgrade Now
                  </Button>
                </div>
              )}

              {user.subscription_tier !== 'FREE' && (
                <div className="space-y-3">
                  {user.subscription_info?.expires_at && (
                    <div className="text-sm text-gray-500">
                      <p>
                        Renews: {new Date(user.subscription_info.expires_at).toLocaleDateString()}
                      </p>
                    </div>
                  )}
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleManageSubscription}
                    disabled={portalLoading}
                  >
                    {portalLoading ? 'Loading...' : 'Manage Subscription'}
                  </Button>
                </div>
              )}
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
          <p className="text-sm text-gray-400">PeppiAcademy v1.0.0</p>
          <p className="text-xs text-gray-300 mt-1">Made with love for diaspora families</p>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
}
