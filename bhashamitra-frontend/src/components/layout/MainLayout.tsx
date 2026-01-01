'use client';

import { ReactNode, useState, useEffect } from 'react';
import { BottomNav } from './BottomNav';
import { Header } from './Header';
import { PeppiAlphabetHelper } from '@/components/peppi';
import { PeppiChatButton, PeppiChatPanel } from '@/components/peppi-chat';
import { useAuthStore, useSubscriptionStore } from '@/stores';
import { useSubscription } from '@/hooks/useSubscription';
import { cn } from '@/lib/utils';

interface MainLayoutProps {
  children: ReactNode;
  showHeader?: boolean;
  showProgress?: boolean;
  showNav?: boolean;
  showPeppi?: boolean;
  headerTitle?: string;
  showBack?: boolean;
  onBack?: () => void;
  className?: string;
}

export function MainLayout({
  children,
  showHeader = true,
  showProgress = true,
  showNav = true,
  showPeppi = true,
  headerTitle,
  showBack = false,
  onBack,
  className,
}: MainLayoutProps) {
  const { activeChild } = useAuthStore();
  const subscription = useSubscription();
  const subscriptionStore = useSubscriptionStore();
  const [hasRefreshedSubscription, setHasRefreshedSubscription] = useState(false);

  // Get current language from active child
  const currentLanguage = activeChild?.language
    ? (typeof activeChild.language === 'string' ? activeChild.language : activeChild.language.code)
    : 'HINDI';

  // Premium users get full Peppi chat with 3 modes (Chat, Story, Learn)
  // Free users get restricted chat with preset prompts only
  const isPaidUser = subscription.isPaidTier && subscription.isActive;

  // Auto-refresh subscription on first mount to ensure tier is detected correctly
  useEffect(() => {
    if (!hasRefreshedSubscription && subscription.loading) {
      const timer = setTimeout(() => {
        console.log('[MainLayout] Auto-refreshing subscription...');
        localStorage.removeItem('subscription-storage');
        subscriptionStore.fetchSubscription();
        setHasRefreshedSubscription(true);
      }, 1000);
      return () => clearTimeout(timer);
    }
  }, [subscription.loading, hasRefreshedSubscription, subscriptionStore]);

  return (
    <div className="min-h-screen bg-background">
      {showHeader && (
        <Header
          showProgress={showProgress}
          title={headerTitle}
          showBack={showBack}
          onBack={onBack}
        />
      )}

      <main
        className={cn(
          'px-4 py-4',
          showNav && 'pb-20', // Extra padding for bottom nav
          className
        )}
      >
        {children}
      </main>

      {showNav && <BottomNav />}

      {/* Peppi Chat - different experience based on subscription */}
      {showPeppi && (
        <>
          {/* PAID users: Full Peppi chat with 3 modes (Chat, Story, Learn) */}
          {isPaidUser && activeChild?.id && (
            <>
              <PeppiChatButton childId={activeChild.id} />
              <PeppiChatPanel childId={activeChild.id} />
            </>
          )}

          {/* FREE users: Restricted chat with preset prompts only */}
          {!isPaidUser && <PeppiAlphabetHelper language={currentLanguage} />}
        </>
      )}
    </div>
  );
}

export default MainLayout;
