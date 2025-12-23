'use client';

import { ReactNode } from 'react';
import { BottomNav } from './BottomNav';
import { Header } from './Header';
import { PeppiAssistant } from '@/components/peppi';
import { PeppiChatButton, PeppiChatPanel } from '@/components/peppi-chat';
import { useAuthStore } from '@/stores';
import { useSubscription } from '@/hooks/useSubscription';
import { cn } from '@/lib/utils';

interface MainLayoutProps {
  children: ReactNode;
  showHeader?: boolean;
  showProgress?: boolean;
  showNav?: boolean;
  showPeppi?: boolean;
  showPeppiChat?: boolean;
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
  showPeppiChat = true,
  headerTitle,
  showBack = false,
  onBack,
  className,
}: MainLayoutProps) {
  const { activeChild } = useAuthStore();
  const subscription = useSubscription();

  // Show Peppi chat for paid tier users
  const shouldShowPeppiChat = showPeppiChat && subscription.isPaidTier && subscription.isActive && activeChild?.id;

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

      {/* Peppi Assistant (basic) - for free users */}
      {showPeppi && !shouldShowPeppiChat && <PeppiAssistant />}

      {/* Peppi Chat (full) - for paid tier users */}
      {shouldShowPeppiChat && activeChild?.id && (
        <>
          <PeppiChatButton childId={activeChild.id} />
          <PeppiChatPanel childId={activeChild.id} />
        </>
      )}
    </div>
  );
}

export default MainLayout;
