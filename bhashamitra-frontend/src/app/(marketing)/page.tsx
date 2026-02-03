'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { useAuthStore } from '@/stores';
import { Button } from '@/components/ui';
import { PeppiAvatar } from '@/components/peppi';
import { fadeInUp, staggerContainer } from '@/lib/constants';

// Service cards for Peppi Academy
const services = [
  {
    id: 'languages',
    name: 'Peppi Languages',
    tagline: 'Your Heritage Language Friend',
    description: 'Learn Hindi, Tamil, Telugu, Gujarati, Punjabi, Malayalam and more through stories and games.',
    icon: '🗣️',
    color: 'from-orange-400 to-amber-500',
    href: '/languages',
    available: true,
  },
  {
    id: 'maths',
    name: 'Peppi Maths',
    tagline: 'Ancient Wisdom, Modern Learning',
    description: 'Master Vedic mathematics, mental calculations, and logical reasoning techniques.',
    icon: '🧮',
    color: 'from-blue-400 to-indigo-500',
    href: '/maths',
    available: false,
  },
  {
    id: 'history',
    name: 'Peppi History',
    tagline: '5000 Years of Amazing Stories',
    description: 'Explore ancient civilizations, empires, freedom fighters, and modern India.',
    icon: '📜',
    color: 'from-amber-500 to-orange-600',
    href: '/history',
    available: false,
  },
  {
    id: 'culture',
    name: 'Peppi Culture',
    tagline: 'Celebrate Living Traditions',
    description: 'Discover festivals, arts, cuisine, and traditions from ALL of India.',
    icon: '🎭',
    color: 'from-purple-400 to-pink-500',
    href: '/culture',
    available: false,
  },
];

// Diversity showcase - representing ALL of India
const diversityShowcase = [
  { label: 'Religions', items: ['Hindu', 'Muslim', 'Sikh', 'Christian', 'Jain', 'Buddhist', 'Parsi'] },
  { label: 'Regions', items: ['North', 'South', 'East', 'West', 'Central', 'Northeast'] },
  { label: 'Languages', items: ['22+ Official', '200+ Dialects', '13+ Scripts'] },
];

// Festival highlights - inclusive of all religions
const festivals = [
  { name: 'Diwali', emoji: '🪔', religion: 'Hindu' },
  { name: 'Eid', emoji: '🌙', religion: 'Muslim' },
  { name: 'Christmas', emoji: '🎄', religion: 'Christian' },
  { name: 'Gurpurab', emoji: '🙏', religion: 'Sikh' },
  { name: 'Buddha Purnima', emoji: '☸️', religion: 'Buddhist' },
  { name: 'Mahavir Jayanti', emoji: '🕉️', religion: 'Jain' },
  { name: 'Navroze', emoji: '🔥', religion: 'Parsi' },
  { name: 'Holi', emoji: '🎨', religion: 'Hindu' },
];

// Pricing tiers - NZD pricing
const PRICING_TIERS = [
  {
    name: 'Free',
    price: '$0',
    period: '',
    icon: '🌱',
    voiceType: 'Browse Mode',
    voiceBadgeClass: 'bg-green-100 text-green-700',
    features: [
      { text: 'Basic alphabets for all languages', enabled: true },
      { text: 'Vocabulary & pronunciation', enabled: true },
      { text: '5 stories from all traditions', enabled: true },
      { text: '2 games per day', enabled: true },
      { text: '1 child profile', enabled: true },
      { text: 'L1-L10 Curriculum Journey', enabled: false },
      { text: 'Peppi AI Chat', enabled: false },
      { text: 'Live classes', enabled: false },
    ],
    ctaClass: 'bg-white text-green-600 border-2 border-green-500 hover:bg-green-500 hover:text-white',
    featured: false,
  },
  {
    name: 'Standard',
    price: 'NZD $20',
    period: '/month',
    icon: '⭐',
    voiceType: 'Full Curriculum',
    voiceBadgeClass: 'bg-yellow-100/50 text-yellow-100',
    features: [
      { text: 'L1-L10 Curriculum (CBSE/ICSE)', enabled: true },
      { text: 'Guided learning journey', enabled: true },
      { text: 'Peppi AI Chat system', enabled: true },
      { text: 'Peppi story narration', enabled: true },
      { text: 'Unlimited stories & games', enabled: true },
      { text: '3 child profiles', enabled: true },
      { text: 'Progress reports', enabled: true },
    ],
    ctaClass: 'bg-yellow-400 text-gray-900 hover:bg-yellow-300',
    featured: true,
  },
  {
    name: 'Premium',
    price: 'Coming Soon',
    period: '',
    icon: '👑',
    voiceType: 'Live Teachers',
    voiceBadgeClass: 'bg-purple-100 text-purple-700',
    comingSoon: true,
    features: [
      { text: 'Everything in Standard', enabled: true },
      { text: '1 live class per month with real teachers', enabled: true, comingSoon: true },
      { text: 'Premium human-quality voices', enabled: true, comingSoon: true },
      { text: '5 child profiles', enabled: true },
      { text: 'Priority support', enabled: true },
      { text: 'Early access to new content', enabled: true },
      { text: 'Offline downloads', enabled: true, comingSoon: true },
      { text: 'Family group sessions', enabled: true, comingSoon: true },
    ],
    ctaClass: 'bg-gray-400 text-white cursor-not-allowed',
    featured: false,
    note: 'Launching Q2 2025 - Join waitlist!',
  },
];

export default function PeppiAcademyLanding() {
  const router = useRouter();
  const { isAuthenticated, activeChild } = useAuthStore();
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    // Redirect authenticated users to home
    if (isAuthenticated && activeChild) {
      router.push('/home');
    }
  }, [isAuthenticated, activeChild, router]);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-teal-50">
      {/* Header */}
      <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled ? 'bg-white/95 backdrop-blur-md shadow-md py-3' : 'bg-transparent py-4'
      }`}>
        <div className="max-w-6xl mx-auto px-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <PeppiAvatar size="sm" showBubble={false} />
            <span className="font-bold text-xl text-gray-800">Peppi Academy</span>
          </div>
          <div className="hidden md:flex items-center gap-6">
            <a href="#services" className="text-gray-600 hover:text-orange-600 transition-colors">Services</a>
            <a href="#festivals" className="text-gray-600 hover:text-orange-600 transition-colors">Festivals</a>
            <a href="#pricing" className="text-gray-600 hover:text-orange-600 transition-colors">Pricing</a>
          </div>
          <div className="flex gap-2">
            <Link href="/login">
              <Button variant="ghost" size="sm">Log In</Button>
            </Link>
            <Link href="/register">
              <Button size="sm">Sign Up Free</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="pt-20">
        <motion.section
          variants={staggerContainer}
          initial="initial"
          animate="animate"
          className="max-w-6xl mx-auto px-4 py-16 text-center"
        >
          {/* Main Peppi */}
          <motion.div variants={fadeInUp} className="mb-6 flex justify-center">
            <PeppiAvatar size="xl" showBubble={false} />
          </motion.div>

          {/* Title */}
          <motion.h1 variants={fadeInUp} className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Peppi Academy
          </motion.h1>

          <motion.p variants={fadeInUp} className="text-xl md:text-2xl text-primary-600 font-medium mb-4">
            Celebrating India&apos;s Incredible Diversity
          </motion.p>

          <motion.p variants={fadeInUp} className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
            A comprehensive learning platform for diaspora children and young adults worldwide.
            Languages, Mathematics, History, and Culture - honoring ALL of India&apos;s religions, regions, and traditions.
          </motion.p>

          {/* Diversity Stats */}
          <motion.div variants={fadeInUp} className="flex flex-wrap justify-center gap-6 mb-10">
            {diversityShowcase.map((item) => (
              <div key={item.label} className="bg-white rounded-xl shadow-sm px-6 py-4 border border-gray-100">
                <p className="text-sm text-gray-500 mb-1">{item.label}</p>
                <p className="text-sm font-medium text-gray-700">{item.items.join(' • ')}</p>
              </div>
            ))}
          </motion.div>
        </motion.section>

        {/* Services Grid */}
        <motion.section
          id="services"
          variants={staggerContainer}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true }}
          className="max-w-6xl mx-auto px-4 py-12"
        >
          <motion.h2 variants={fadeInUp} className="text-2xl font-bold text-center text-gray-800 mb-8">
            Learning Modules
          </motion.h2>

          <div className="grid md:grid-cols-2 gap-6">
            {services.map((service) => (
              <motion.div
                key={service.id}
                variants={fadeInUp}
                className={`relative rounded-2xl overflow-hidden ${
                  service.available ? 'cursor-pointer hover:shadow-xl transition-shadow' : 'opacity-75'
                }`}
              >
                {service.available ? (
                  <Link href={service.href}>
                    <ServiceCard service={service} />
                  </Link>
                ) : (
                  <ServiceCard service={service} />
                )}
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* Festival Showcase - Inclusive */}
        <motion.section
          id="festivals"
          variants={staggerContainer}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true }}
          className="max-w-6xl mx-auto px-4 py-12"
        >
          <motion.h2 variants={fadeInUp} className="text-2xl font-bold text-center text-gray-800 mb-3">
            Celebrating All Festivals
          </motion.h2>
          <motion.p variants={fadeInUp} className="text-center text-gray-600 mb-8">
            We honor and teach about celebrations from every community
          </motion.p>

          <motion.div variants={fadeInUp} className="flex flex-wrap justify-center gap-3">
            {festivals.map((festival) => (
              <div
                key={festival.name}
                className="flex items-center gap-2 bg-white rounded-full px-4 py-2 shadow-sm border border-gray-100"
              >
                <span className="text-xl">{festival.emoji}</span>
                <span className="text-sm font-medium text-gray-700">{festival.name}</span>
              </div>
            ))}
          </motion.div>
        </motion.section>

        {/* Why Peppi Academy */}
        <motion.section
          variants={staggerContainer}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true }}
          className="max-w-6xl mx-auto px-4 py-12"
        >
          <motion.h2 variants={fadeInUp} className="text-2xl font-bold text-center text-gray-800 mb-8">
            Why Peppi Academy?
          </motion.h2>

          <div className="grid md:grid-cols-3 gap-6">
            {[
              {
                icon: '🌏',
                title: 'Built for Diaspora',
                description: 'Designed specifically for Indian families in NZ, Australia, UK, USA, Canada, and worldwide.',
              },
              {
                icon: '🤝',
                title: 'Truly Inclusive',
                description: 'Representing ALL Indian religions, regions, languages, and traditions. Not just one community.',
              },
              {
                icon: '🎮',
                title: 'Fun & Engaging',
                description: 'Gamified learning with stories, games, rewards, and Peppi the AI tutor cat.',
              },
              {
                icon: '👨‍👩‍👧‍👦',
                title: 'Family-Focused',
                description: 'Parent dashboards, progress tracking, and grandparent voice message contributions.',
              },
              {
                icon: '📱',
                title: 'Learn Anywhere',
                description: 'Web-based platform works on any device. Mobile apps coming soon.',
              },
              {
                icon: '🆓',
                title: 'Free to Start',
                description: 'Generous free tier with optional premium features. Quality education for all.',
              },
            ].map((feature) => (
              <motion.div
                key={feature.title}
                variants={fadeInUp}
                className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 text-center"
              >
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="font-semibold text-gray-800 mb-2">{feature.title}</h3>
                <p className="text-sm text-gray-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* Language Scripts Showcase */}
        <motion.section
          variants={staggerContainer}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true }}
          className="max-w-6xl mx-auto px-4 py-12"
        >
          <motion.h2 variants={fadeInUp} className="text-2xl font-bold text-center text-gray-800 mb-8">
            Learn Beautiful Scripts
          </motion.h2>

          <motion.div variants={fadeInUp} className="flex flex-wrap justify-center gap-4">
            {[
              { script: 'हिन्दी', name: 'Hindi' },
              { script: 'தமிழ்', name: 'Tamil' },
              { script: 'తెలుగు', name: 'Telugu' },
              { script: 'ગુજરાતી', name: 'Gujarati' },
              { script: 'ਪੰਜਾਬੀ', name: 'Punjabi' },
              { script: 'മലയാളം', name: 'Malayalam' },
              { script: 'বাংলা', name: 'Bengali' },
              { script: 'मराठी', name: 'Marathi' },
              { script: 'ಕನ್ನಡ', name: 'Kannada' },
              { script: 'ଓଡ଼ିଆ', name: 'Odia' },
              { script: 'اردو', name: 'Urdu' },
            ].map((lang) => (
              <div
                key={lang.name}
                className="bg-gradient-to-br from-orange-50 to-amber-50 rounded-xl px-5 py-3 border border-orange-100"
              >
                <p className="text-2xl font-medium text-gray-800 mb-1">{lang.script}</p>
                <p className="text-xs text-gray-500 text-center">{lang.name}</p>
              </div>
            ))}
          </motion.div>
        </motion.section>

        {/* Pricing Section */}
        <section id="pricing" className="py-16 px-4 bg-gradient-to-b from-white to-orange-50">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-12">
              <p className="text-pink-600 font-semibold uppercase tracking-wider mb-2">Simple Pricing</p>
              <h2 className="text-3xl font-bold text-gray-800 mb-4">
                Choose Your Learning Journey
              </h2>
              <p className="text-lg text-gray-600">Start free, upgrade when you&apos;re ready for more</p>
            </div>

            <div className="grid lg:grid-cols-3 gap-8 max-w-5xl mx-auto">
              {PRICING_TIERS.map((tier, index) => (
                <motion.div
                  key={tier.name}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className={`rounded-3xl p-8 relative ${
                    tier.featured
                      ? 'bg-gradient-to-br from-teal-700 to-teal-600 text-white scale-105 shadow-2xl'
                      : 'bg-white hover:shadow-xl'
                  } transition-all duration-300 hover:-translate-y-2`}
                >
                  {tier.featured && (
                    <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-gradient-to-r from-pink-500 to-orange-500 text-white text-xs font-bold px-4 py-1.5 rounded-full uppercase tracking-wider">
                      Most Popular
                    </div>
                  )}
                  {tier.comingSoon && (
                    <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-gradient-to-r from-purple-500 to-indigo-500 text-white text-xs font-bold px-4 py-1.5 rounded-full uppercase tracking-wider">
                      Coming Soon
                    </div>
                  )}

                  <div className="text-center pb-6 border-b border-current/10 mb-6">
                    <div className={`w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center text-3xl ${
                      tier.featured ? 'bg-white/20' : index === 0 ? 'bg-green-100' : 'bg-purple-100'
                    }`}>
                      {tier.icon}
                    </div>
                    <h3 className={`text-2xl font-bold mb-2 ${tier.featured ? 'text-white' : 'text-gray-800'}`}>
                      {tier.name}
                    </h3>
                    <div className={`text-4xl font-bold ${tier.featured ? 'text-white' : 'text-gray-800'}`}>
                      {tier.price}
                      {tier.period && <span className="text-lg font-normal opacity-70">{tier.period}</span>}
                    </div>
                    <div className={`inline-block mt-3 px-3 py-1 rounded-full text-sm font-semibold ${tier.voiceBadgeClass}`}>
                      {tier.voiceType}
                    </div>
                  </div>

                  <ul className="space-y-4 mb-8">
                    {tier.features.map((feature) => (
                      <li
                        key={feature.text}
                        className={`flex items-start gap-3 ${feature.enabled ? '' : 'opacity-50'}`}
                      >
                        <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs flex-shrink-0 ${
                          feature.enabled
                            ? tier.featured ? 'bg-yellow-400 text-gray-900' : 'bg-green-500 text-white'
                            : 'bg-gray-300 text-gray-500'
                        }`}>
                          {feature.enabled ? '✓' : '✗'}
                        </span>
                        <span className={tier.featured ? 'text-white/90' : 'text-gray-700'}>
                          {feature.text}
                          {(feature as { comingSoon?: boolean }).comingSoon && (
                            <span className="ml-2 text-xs bg-purple-100 text-purple-600 px-2 py-0.5 rounded-full">
                              Soon
                            </span>
                          )}
                        </span>
                      </li>
                    ))}
                  </ul>

                  {tier.comingSoon ? (
                    <button
                      className={`w-full py-3 rounded-full font-bold transition-all duration-300 ${tier.ctaClass}`}
                      disabled
                    >
                      Join Waitlist
                    </button>
                  ) : (
                    <Link href="/register" className="block">
                      <button className={`w-full py-3 rounded-full font-bold transition-all duration-300 ${tier.ctaClass}`}>
                        {tier.name === 'Free' ? 'Start Free' : `Get ${tier.name}`}
                      </button>
                    </Link>
                  )}

                  {tier.note && (
                    <p className={`mt-4 text-xs text-center ${tier.featured ? 'text-white/60' : 'text-gray-500'}`}>
                      {tier.note}
                    </p>
                  )}
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <motion.section
          variants={staggerContainer}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true }}
          className="max-w-6xl mx-auto px-4 py-16 text-center"
        >
          <motion.div variants={fadeInUp} className="bg-gradient-to-r from-primary-500 to-secondary-500 rounded-3xl p-8 md:p-12">
            <h2 className="text-2xl md:text-3xl font-bold text-white mb-4">
              Start Your Heritage Journey Today
            </h2>
            <p className="text-white/90 mb-6 max-w-xl mx-auto">
              Join thousands of diaspora families connecting their children with India&apos;s incredible heritage.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/register">
                <Button size="lg" className="w-full sm:w-auto bg-white text-primary-600 hover:bg-gray-50">
                  Get Started Free
                </Button>
              </Link>
              <Link href="/languages">
                <Button size="lg" variant="outline" className="w-full sm:w-auto border-white text-white hover:bg-white/10">
                  Explore Languages
                </Button>
              </Link>
            </div>
          </motion.div>
        </motion.section>
      </main>

      {/* Footer */}
      <footer className="bg-gray-50 border-t border-gray-100 py-8">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-2">
              <PeppiAvatar size="sm" showBubble={false} />
              <span className="font-semibold text-gray-700">Peppi Academy</span>
            </div>
            <p className="text-sm text-gray-500 text-center">
              Made with love for Indian diaspora families worldwide
            </p>
            <div className="flex gap-4 text-sm text-gray-500">
              <Link href="/help" className="hover:text-gray-700">About</Link>
              <Link href="/help" className="hover:text-gray-700">Contact</Link>
              <Link href="/privacy" className="hover:text-gray-700">Privacy</Link>
              <Link href="/terms" className="hover:text-gray-700">Terms</Link>
            </div>
          </div>
          <div className="mt-6 pt-6 border-t border-gray-200 text-center">
            <p className="text-xs text-gray-400">
              Celebrating India&apos;s unity in diversity - all religions, all regions, all traditions
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

// Service Card Component
function ServiceCard({ service }: { service: typeof services[0] }) {
  return (
    <div className={`bg-gradient-to-br ${service.color} p-6 h-full`}>
      <div className="flex items-start justify-between mb-4">
        <div className="text-4xl">{service.icon}</div>
        {!service.available && (
          <span className="bg-white/20 text-white text-xs px-2 py-1 rounded-full">
            Coming Soon
          </span>
        )}
      </div>
      <h3 className="text-xl font-bold text-white mb-1">{service.name}</h3>
      <p className="text-white/80 text-sm mb-2">{service.tagline}</p>
      <p className="text-white/70 text-sm">{service.description}</p>
      {service.available && (
        <div className="mt-4 flex items-center text-white font-medium text-sm">
          Start Learning <span className="ml-2">→</span>
        </div>
      )}
    </div>
  );
}
