'use client';

import { ReactNode } from 'react';
import { BottomNav } from './BottomNav';
import { Header } from './Header';
import { PeppiAssistant } from '@/components/peppi';
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

      {showPeppi && <PeppiAssistant />}
    </div>
  );
}

export default MainLayout;
