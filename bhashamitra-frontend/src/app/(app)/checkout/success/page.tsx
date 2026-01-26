'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { useSubscriptionStore } from '@/stores/subscriptionStore';
import { useAuthStore } from '@/stores/authStore';

export default function CheckoutSuccessPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const sessionId = searchParams.get('session_id');
  const { fetchSubscription } = useSubscriptionStore();
  const { isAuthenticated, loadUserProfile } = useAuthStore();
  const [countdown, setCountdown] = useState(10);

  useEffect(() => {
    // Refresh subscription data
    const refreshData = async () => {
      if (isAuthenticated) {
        await loadUserProfile();
        await fetchSubscription();
      }
    };
    refreshData();
  }, [isAuthenticated, loadUserProfile, fetchSubscription]);

  useEffect(() => {
    // Auto-redirect countdown
    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          router.push('/home');
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [router]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-emerald-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 text-center">
        {/* Success Icon */}
        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg
            className="w-10 h-10 text-green-500"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 13l4 4L19 7"
            />
          </svg>
        </div>

        {/* Title */}
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Welcome to the Family!
        </h1>
        <p className="text-gray-600 mb-8">
          Your subscription has been activated successfully. Your child&apos;s Hindi learning journey begins now!
        </p>

        {/* Peppi Character */}
        <div className="bg-gradient-to-r from-orange-100 to-amber-100 rounded-xl p-6 mb-8">
          <div className="text-6xl mb-3">🐱</div>
          <p className="text-lg font-medium text-orange-800">
            &ldquo;Namaste! I&apos;m Peppi, and I can&apos;t wait to help your child learn Hindi!&rdquo;
          </p>
        </div>

        {/* What's Next */}
        <div className="text-left bg-gray-50 rounded-xl p-6 mb-8">
          <h2 className="font-bold text-gray-900 mb-4">What&apos;s Next?</h2>
          <ul className="space-y-3">
            <li className="flex items-start gap-3">
              <span className="flex-shrink-0 w-6 h-6 bg-orange-500 text-white rounded-full flex items-center justify-center text-sm font-medium">
                1
              </span>
              <span className="text-gray-700">Add your child&apos;s profile</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="flex-shrink-0 w-6 h-6 bg-orange-500 text-white rounded-full flex items-center justify-center text-sm font-medium">
                2
              </span>
              <span className="text-gray-700">Start with Level 1 basics</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="flex-shrink-0 w-6 h-6 bg-orange-500 text-white rounded-full flex items-center justify-center text-sm font-medium">
                3
              </span>
              <span className="text-gray-700">Have fun learning with Peppi!</span>
            </li>
          </ul>
        </div>

        {/* CTA Buttons */}
        <div className="space-y-3">
          <Link
            href="/home"
            className="block w-full bg-orange-500 text-white py-3 px-6 rounded-lg font-medium hover:bg-orange-600 transition-colors"
          >
            Start Learning
          </Link>
          <Link
            href="/profile"
            className="block w-full bg-gray-100 text-gray-700 py-3 px-6 rounded-lg font-medium hover:bg-gray-200 transition-colors"
          >
            Manage Subscription
          </Link>
        </div>

        {/* Auto-redirect notice */}
        <p className="text-sm text-gray-500 mt-6">
          Redirecting to home in {countdown} seconds...
        </p>

        {sessionId && (
          <p className="text-xs text-gray-400 mt-4">
            Session: {sessionId.slice(0, 20)}...
          </p>
        )}
      </div>
    </div>
  );
}
