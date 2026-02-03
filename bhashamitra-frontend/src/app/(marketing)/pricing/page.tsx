'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import { useAuthStore } from '@/stores/authStore';

interface TierFeature {
  text: string;
  enabled: boolean;
  note?: string;
}

interface TierInfo {
  name: string;
  price: string;
  price_yearly: string;
  currency: string;
  icon: string;
  color: string;
  features: TierFeature[];
  cta: string;
  featured: boolean;
}

type BillingCycle = 'monthly' | 'yearly';

export default function PricingPage() {
  const router = useRouter();
  const { user, isAuthenticated } = useAuthStore();
  const [tiers, setTiers] = useState<Record<string, TierInfo> | null>(null);
  const [billingCycle, setBillingCycle] = useState<BillingCycle>('monthly');
  const [loading, setLoading] = useState(true);
  const [checkoutLoading, setCheckoutLoading] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadPricing();
  }, []);

  const loadPricing = async () => {
    try {
      const response = await api.getSubscriptionTiers();
      if (response.success && response.data) {
        setTiers(response.data.data.tiers);
      } else {
        setError('Failed to load pricing information');
      }
    } catch {
      setError('Failed to load pricing information');
    } finally {
      setLoading(false);
    }
  };

  const handleSubscribe = async (tier: 'STANDARD' | 'PREMIUM') => {
    if (!isAuthenticated) {
      router.push(`/login?redirect=/pricing&tier=${tier}`);
      return;
    }

    if (user?.subscription_tier === tier) {
      return;
    }

    setCheckoutLoading(tier);
    setError(null);

    try {
      const response = await api.createCheckoutSession({
        tier,
        billing_cycle: billingCycle,
      });

      if (response.success && response.data) {
        window.location.href = response.data.url;
      } else {
        setError(response.error || 'Failed to create checkout session');
      }
    } catch {
      setError('Failed to start checkout. Please try again.');
    } finally {
      setCheckoutLoading(null);
    }
  };

  const getButtonText = (tierKey: string, tier: TierInfo) => {
    if (!isAuthenticated) {
      return tier.cta;
    }

    if (user?.subscription_tier === tierKey) {
      return 'Current Plan';
    }

    if (tierKey === 'FREE') {
      return user?.subscription_tier !== 'FREE' ? 'Downgrade' : tier.cta;
    }

    return tier.cta;
  };

  const isCurrentPlan = (tierKey: string) => {
    return isAuthenticated && user?.subscription_tier === tierKey;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-amber-50 to-orange-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading pricing...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-amber-50 to-orange-50 py-12 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Choose Your Learning Journey
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Start your child&apos;s Hindi learning adventure with PeppiAcademy
          </p>
        </div>

        {/* Billing Toggle */}
        <div className="flex justify-center mb-10">
          <div className="bg-white rounded-full p-1 shadow-md inline-flex">
            <button
              onClick={() => setBillingCycle('monthly')}
              className={`px-6 py-2 rounded-full text-sm font-medium transition-colors ${
                billingCycle === 'monthly'
                  ? 'bg-orange-500 text-white'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Monthly
            </button>
            <button
              onClick={() => setBillingCycle('yearly')}
              className={`px-6 py-2 rounded-full text-sm font-medium transition-colors ${
                billingCycle === 'yearly'
                  ? 'bg-orange-500 text-white'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Yearly
              <span className="ml-2 text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full">
                Save 17%
              </span>
            </button>
          </div>
        </div>

        {error && (
          <div className="max-w-md mx-auto mb-8 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-center">
            {error}
          </div>
        )}

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {tiers && ['FREE', 'STANDARD', 'PREMIUM'].map((tierKey) => {
            const tier = tiers[tierKey];
            if (!tier) return null;

            const isFeatured = tier.featured;
            const isCurrent = isCurrentPlan(tierKey);
            const price = billingCycle === 'monthly' ? tier.price : tier.price_yearly;

            return (
              <div
                key={tierKey}
                className={`relative bg-white rounded-2xl shadow-lg overflow-hidden transition-transform hover:scale-105 ${
                  isFeatured ? 'ring-2 ring-orange-500 md:scale-105' : ''
                } ${isCurrent ? 'ring-2 ring-green-500' : ''}`}
              >
                {isFeatured && (
                  <div className="absolute top-0 left-0 right-0 bg-orange-500 text-white text-center py-1 text-sm font-medium">
                    Most Popular
                  </div>
                )}
                {isCurrent && (
                  <div className="absolute top-0 left-0 right-0 bg-green-500 text-white text-center py-1 text-sm font-medium">
                    Current Plan
                  </div>
                )}

                <div className={`p-8 ${isFeatured || isCurrent ? 'pt-12' : ''}`}>
                  {/* Header */}
                  <div className="text-center mb-6">
                    <span className="text-4xl mb-2 block">{tier.icon}</span>
                    <h2 className="text-2xl font-bold text-gray-900">{tier.name}</h2>
                    <div className="mt-4">
                      <span className="text-4xl font-bold" style={{ color: tier.color }}>
                        {price}
                      </span>
                      {tierKey !== 'FREE' && (
                        <span className="text-gray-500 ml-1">
                          /{billingCycle === 'monthly' ? 'month' : 'year'}
                        </span>
                      )}
                    </div>
                    {billingCycle === 'yearly' && tierKey !== 'FREE' && (
                      <p className="text-sm text-green-600 mt-1">2 months free!</p>
                    )}
                  </div>

                  {/* Features */}
                  <ul className="space-y-3 mb-8">
                    {tier.features.map((feature, idx) => (
                      <li key={idx} className="flex items-start gap-3">
                        {feature.enabled ? (
                          <svg className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                          </svg>
                        ) : (
                          <svg className="w-5 h-5 text-gray-300 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        )}
                        <span className={feature.enabled ? 'text-gray-700' : 'text-gray-400'}>
                          {feature.text}
                          {feature.note && (
                            <span className="block text-xs text-gray-400">{feature.note}</span>
                          )}
                        </span>
                      </li>
                    ))}
                  </ul>

                  {/* CTA Button */}
                  <button
                    onClick={() => {
                      if (tierKey === 'FREE') {
                        if (!isAuthenticated) {
                          router.push('/register');
                        }
                      } else {
                        handleSubscribe(tierKey as 'STANDARD' | 'PREMIUM');
                      }
                    }}
                    disabled={isCurrent || checkoutLoading === tierKey}
                    className={`w-full py-3 px-6 rounded-lg font-medium transition-colors ${
                      isCurrent
                        ? 'bg-gray-100 text-gray-500 cursor-not-allowed'
                        : tierKey === 'FREE'
                        ? 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                        : isFeatured
                        ? 'bg-orange-500 text-white hover:bg-orange-600'
                        : 'bg-gray-900 text-white hover:bg-gray-800'
                    }`}
                  >
                    {checkoutLoading === tierKey ? (
                      <span className="flex items-center justify-center gap-2">
                        <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                        </svg>
                        Processing...
                      </span>
                    ) : (
                      getButtonText(tierKey, tier)
                    )}
                  </button>
                </div>
              </div>
            );
          })}
        </div>

        {/* 7-Day Trial Notice */}
        <div className="text-center mt-12">
          <div className="inline-flex items-center gap-2 bg-blue-50 text-blue-700 px-6 py-3 rounded-full">
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="font-medium">7-day free trial on all paid plans</span>
          </div>
        </div>

        {/* FAQ Section */}
        <div className="mt-16 max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold text-center text-gray-900 mb-8">
            Frequently Asked Questions
          </h2>
          <div className="space-y-4">
            <details className="bg-white rounded-lg p-4 shadow-sm">
              <summary className="font-medium cursor-pointer">Can I cancel anytime?</summary>
              <p className="mt-2 text-gray-600">
                Yes! You can cancel your subscription at any time. You&apos;ll continue to have access until the end of your billing period.
              </p>
            </details>
            <details className="bg-white rounded-lg p-4 shadow-sm">
              <summary className="font-medium cursor-pointer">What payment methods do you accept?</summary>
              <p className="mt-2 text-gray-600">
                We accept all major credit and debit cards through Stripe, our secure payment processor.
              </p>
            </details>
            <details className="bg-white rounded-lg p-4 shadow-sm">
              <summary className="font-medium cursor-pointer">Can I switch plans later?</summary>
              <p className="mt-2 text-gray-600">
                Absolutely! You can upgrade or downgrade your plan at any time through your account settings.
              </p>
            </details>
            <details className="bg-white rounded-lg p-4 shadow-sm">
              <summary className="font-medium cursor-pointer">Is there a family discount?</summary>
              <p className="mt-2 text-gray-600">
                Our Standard and Premium plans include multiple child profiles (3 and 5 respectively), so the whole family can learn together!
              </p>
            </details>
          </div>
        </div>

        {/* Back to Home */}
        <div className="text-center mt-12">
          <button
            onClick={() => router.push('/')}
            className="text-gray-600 hover:text-gray-900 underline"
          >
            Back to Home
          </button>
        </div>
      </div>
    </div>
  );
}
