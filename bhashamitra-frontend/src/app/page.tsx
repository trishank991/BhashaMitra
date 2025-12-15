'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { useAuthStore } from '@/stores';
import { Button } from '@/components/ui';
import { fadeInUp, staggerContainer } from '@/lib/constants';

// Peppi SVG Component
function PeppiSVG({ size = 'md' }: { size?: 'sm' | 'md' | 'lg' | 'xl' }) {
  const sizes = {
    sm: 'w-12 h-12',
    md: 'w-24 h-24',
    lg: 'w-32 h-32',
    xl: 'w-40 h-40',
  };

  return (
    <svg className={sizes[size]} viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      {/* Ears */}
      <path fill="#F5E6D3" d="M20 40 L10 10 L35 30 Z"/>
      <path fill="#F5E6D3" d="M80 40 L90 10 L65 30 Z"/>
      <path fill="#E8D4C4" d="M18 32 L12 14 L30 28 Z"/>
      <path fill="#E8D4C4" d="M82 32 L88 14 L70 28 Z"/>
      <path fill="#FFCDB8" d="M22 30 L16 18 L32 28 Z"/>
      <path fill="#FFCDB8" d="M78 30 L84 18 L68 28 Z"/>
      {/* Head */}
      <ellipse fill="#F5E6D3" cx="50" cy="50" rx="38" ry="35"/>
      {/* Eyes */}
      <ellipse fill="white" cx="35" cy="48" rx="12" ry="14"/>
      <ellipse fill="white" cx="65" cy="48" rx="12" ry="14"/>
      <ellipse fill="#4A90D9" cx="35" cy="50" rx="9" ry="11"/>
      <ellipse fill="#4A90D9" cx="65" cy="50" rx="9" ry="11"/>
      <ellipse fill="#1a1a1a" cx="35" cy="51" rx="4" ry="5"/>
      <ellipse fill="#1a1a1a" cx="65" cy="51" rx="4" ry="5"/>
      <circle fill="white" cx="38" cy="45" r="3"/>
      <circle fill="white" cx="68" cy="45" r="3"/>
      {/* Nose */}
      <path fill="#FF7F50" d="M50 58 L46 65 L54 65 Z"/>
      {/* Whiskers */}
      <line stroke="#999" strokeWidth="1" x1="8" y1="52" x2="28" y2="56"/>
      <line stroke="#999" strokeWidth="1" x1="8" y1="60" x2="28" y2="60"/>
      <line stroke="#999" strokeWidth="1" x1="92" y1="52" x2="72" y2="56"/>
      <line stroke="#999" strokeWidth="1" x1="92" y1="60" x2="72" y2="60"/>
      {/* Collar */}
      <ellipse fill="#FF6B35" cx="50" cy="78" rx="22" ry="5"/>
      {/* Bell */}
      <circle fill="#FFD700" cx="50" cy="83" r="5"/>
      <circle fill="#FFF8DC" cx="48" cy="81" r="1.5"/>
    </svg>
  );
}

// Language badges data
const LANGUAGES = [
  { name: 'Hindi', native: 'हिंदी', color: 'border-l-orange-500 text-orange-700' },
  { name: 'Tamil', native: 'தமிழ்', color: 'border-l-pink-500 text-pink-700' },
  { name: 'Gujarati', native: 'ગુજરાતી', color: 'border-l-yellow-500 text-yellow-700' },
  { name: 'Punjabi', native: 'ਪੰਜਾਬੀ', color: 'border-l-teal-500 text-teal-700' },
];

// Features data
const FEATURES = [
  {
    icon: '📖',
    title: 'Interactive Stories',
    description: 'Explore festival stories, folktales, and cultural narratives narrated by Peppi. Stories from Diwali to Eid, Baisakhi to Christmas!',
    tag: '100+ Stories',
    gradient: 'from-orange-50 to-orange-100',
  },
  {
    icon: '🎮',
    title: 'Fun Learning Games',
    description: 'Memory games, word matching, pronunciation challenges, and vocabulary builders that make learning feel like play.',
    tag: '20+ Game Types',
    gradient: 'from-pink-50 to-pink-100',
  },
  {
    icon: '🗣️',
    title: 'Pronunciation Practice',
    description: 'Hear correct pronunciation with our AI-powered TTS. Premium members get human-quality voices for authentic learning.',
    tag: 'Native Accents',
    gradient: 'from-teal-50 to-teal-100',
  },
  {
    icon: '🎯',
    title: 'Structured Curriculum',
    description: 'Age-appropriate lessons from alphabet basics to conversational fluency. Perfect for ages 4-14.',
    tag: '5 Levels',
    gradient: 'from-indigo-50 to-indigo-100',
  },
  {
    icon: '👨‍👩‍👧',
    title: 'Family Features',
    description: 'Multiple child profiles, progress tracking for parents, and family challenges to learn together.',
    tag: 'COPPA Compliant',
    gradient: 'from-amber-50 to-amber-100',
  },
  {
    icon: '🏆',
    title: 'Rewards & Streaks',
    description: 'Earn badges, maintain streaks, and unlock achievements. Gamification that keeps kids coming back!',
    tag: '50+ Badges',
    gradient: 'from-purple-50 to-purple-100',
  },
];

// Pricing tiers
const PRICING_TIERS = [
  {
    name: 'Free',
    price: '$0',
    icon: '🌱',
    voiceType: 'Basic AI Voice',
    voiceBadgeClass: 'bg-green-100 text-green-700',
    features: [
      { text: '10 stories per month', enabled: true },
      { text: '5 vocabulary lessons', enabled: true },
      { text: '3 games per day', enabled: true },
      { text: 'Basic progress tracking', enabled: true },
      { text: '1 child profile', enabled: true },
      { text: 'Peppi story narration', enabled: false },
      { text: 'Full curriculum access', enabled: false },
      { text: 'Human-quality voices', enabled: false },
    ],
    ctaClass: 'bg-white text-green-600 border-2 border-green-500 hover:bg-green-500 hover:text-white',
    featured: false,
  },
  {
    name: 'Standard',
    price: '$12',
    icon: '⭐',
    voiceType: 'AI Generated Voice',
    voiceBadgeClass: 'bg-yellow-100/50 text-yellow-100',
    features: [
      { text: 'Unlimited stories', enabled: true },
      { text: 'Full vocabulary curriculum', enabled: true },
      { text: 'Unlimited games', enabled: true },
      { text: 'Peppi story narration', enabled: true },
      { text: '3 child profiles', enabled: true },
      { text: 'Detailed progress reports', enabled: true },
      { text: 'All festival stories', enabled: true },
      { text: 'Human-quality voices', enabled: false },
    ],
    ctaClass: 'bg-yellow-400 text-gray-900 hover:bg-yellow-300',
    featured: true,
  },
  {
    name: 'Premium',
    price: '$20',
    icon: '👑',
    voiceType: 'Real Human Voices',
    voiceBadgeClass: 'bg-purple-100 text-purple-700',
    features: [
      { text: 'Everything in Standard', enabled: true },
      { text: 'Human-quality voice narration', enabled: true },
      { text: 'Unlimited child profiles', enabled: true },
      { text: 'Priority new content', enabled: true },
      { text: 'Offline downloads', enabled: true },
      { text: 'Family challenges', enabled: true },
      { text: 'Exclusive premium stories', enabled: true },
      { text: 'Early access to AI coaching', enabled: true },
    ],
    ctaClass: 'bg-gradient-to-r from-purple-600 to-purple-700 text-white hover:from-purple-500 hover:to-purple-600',
    featured: false,
  },
];

// Festival stories
const FESTIVALS = [
  { name: 'Diwali', religion: 'Hindu Festival', stories: 5, icon: '🪔', gradient: 'from-orange-200 to-orange-300' },
  { name: 'Holi', religion: 'Hindu Festival', stories: 4, icon: '🎨', gradient: 'from-pink-200 to-pink-300' },
  { name: 'Eid', religion: 'Islamic Festival', stories: 4, icon: '🌙', gradient: 'from-green-200 to-green-300' },
  { name: 'Guru Nanak Jayanti', religion: 'Sikh Festival', stories: 3, icon: '🙏', gradient: 'from-blue-200 to-blue-300' },
  { name: 'Christmas', religion: 'Christian Festival', stories: 3, icon: '🎄', gradient: 'from-red-200 to-red-300' },
  { name: 'Baisakhi', religion: 'Sikh Festival', stories: 2, icon: '🌾', gradient: 'from-amber-200 to-amber-300' },
];

export default function LandingPage() {
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
    <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-pink-50">
      {/* Navigation */}
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled ? 'bg-white/95 backdrop-blur-md shadow-md py-3' : 'bg-transparent py-4'
      }`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-gradient-to-br from-orange-50 to-orange-100 rounded-xl flex items-center justify-center shadow-lg">
              <PeppiSVG size="sm" />
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-orange-600 to-pink-600 bg-clip-text text-transparent">
              BhashaMitra
            </span>
          </div>

          <div className="hidden md:flex items-center gap-8">
            <a href="#features" className="text-teal-800 font-medium hover:text-orange-600 transition-colors">Features</a>
            <a href="#peppi" className="text-teal-800 font-medium hover:text-orange-600 transition-colors">Meet Peppi</a>
            <a href="#pricing" className="text-teal-800 font-medium hover:text-orange-600 transition-colors">Pricing</a>
            <a href="#festivals" className="text-teal-800 font-medium hover:text-orange-600 transition-colors">Stories</a>
            <Link href="/login">
              <Button variant="primary" size="sm" className="rounded-full px-6">
                Start Free Trial
              </Button>
            </Link>
          </div>

          <Link href="/login" className="md:hidden">
            <Button variant="ghost" size="sm">Log In</Button>
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="min-h-screen flex items-center pt-20 pb-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
        {/* Floating decorations */}
        <div className="absolute inset-0 pointer-events-none">
          <motion.div
            className="absolute top-[15%] left-[8%] text-4xl opacity-60"
            animate={{ y: [0, -20, 0], rotate: [0, 5, 0] }}
            transition={{ duration: 6, repeat: Infinity }}
          >🪔</motion.div>
          <motion.div
            className="absolute top-[25%] right-[12%] text-3xl opacity-60"
            animate={{ y: [0, -15, 0], rotate: [0, -5, 0] }}
            transition={{ duration: 5, repeat: Infinity, delay: 1 }}
          >🎨</motion.div>
          <motion.div
            className="absolute bottom-[25%] left-[15%] text-2xl opacity-60"
            animate={{ y: [0, -18, 0], rotate: [0, 3, 0] }}
            transition={{ duration: 7, repeat: Infinity, delay: 2 }}
          >📚</motion.div>
          <motion.div
            className="absolute bottom-[15%] right-[8%] text-3xl opacity-60"
            animate={{ y: [0, -22, 0], rotate: [0, -3, 0] }}
            transition={{ duration: 6, repeat: Infinity, delay: 0.5 }}
          >🌸</motion.div>
        </div>

        <div className="max-w-7xl mx-auto w-full">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Text Content */}
            <motion.div
              variants={staggerContainer}
              initial="initial"
              animate="animate"
              className="text-center lg:text-left"
            >
              <motion.h1
                variants={fadeInUp}
                className="text-4xl sm:text-5xl lg:text-6xl font-bold text-teal-800 leading-tight mb-6"
              >
                Keep Your{' '}
                <span className="bg-gradient-to-r from-orange-500 to-pink-500 bg-clip-text text-transparent">
                  Heritage
                </span>{' '}
                Alive Through Language
              </motion.h1>

              <motion.p
                variants={fadeInUp}
                className="text-lg sm:text-xl text-gray-600 mb-8"
              >
                Fun, interactive language learning designed for Indian diaspora children in New Zealand & Australia. Learn with stories, games, and your AI friend Peppi!
              </motion.p>

              {/* Language badges */}
              <motion.div variants={fadeInUp} className="flex flex-wrap justify-center lg:justify-start gap-3 mb-8">
                {LANGUAGES.map((lang) => (
                  <div
                    key={lang.name}
                    className={`bg-white px-4 py-2 rounded-full shadow-md border-l-4 ${lang.color} flex items-center gap-2 font-medium hover:shadow-lg transition-shadow`}
                  >
                    <span>{lang.native}</span>
                    <span className="text-gray-400">{lang.name}</span>
                  </div>
                ))}
              </motion.div>

              {/* CTA Buttons */}
              <motion.div variants={fadeInUp} className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                <Link href="/register">
                  <Button size="lg" className="rounded-full px-8 shadow-lg hover:shadow-xl transition-shadow">
                    Start Learning Free →
                  </Button>
                </Link>
                <a href="#features">
                  <Button variant="outline" size="lg" className="rounded-full px-8">
                    See How It Works
                  </Button>
                </a>
              </motion.div>
            </motion.div>

            {/* Peppi Mascot */}
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="flex justify-center relative"
            >
              <div className="relative">
                {/* Glow effect */}
                <motion.div
                  className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-orange-300/30 rounded-full blur-3xl"
                  animate={{ scale: [1, 1.1, 1], opacity: [0.6, 0.8, 0.6] }}
                  transition={{ duration: 3, repeat: Infinity }}
                />

                {/* Peppi character */}
                <motion.div
                  animate={{ y: [0, -15, 0] }}
                  transition={{ duration: 4, repeat: Infinity }}
                  className="relative z-10"
                >
                  <div className="w-64 h-64 sm:w-80 sm:h-80">
                    <svg viewBox="0 0 220 250" xmlns="http://www.w3.org/2000/svg" className="w-full h-full drop-shadow-2xl">
                      {/* Tail */}
                      <ellipse fill="#F5E6D3" cx="195" cy="160" rx="25" ry="18" transform="rotate(-20 195 160)"/>
                      <ellipse fill="#F5E6D3" cx="205" cy="145" rx="18" ry="14" transform="rotate(-40 205 145)"/>
                      <ellipse fill="#F5E6D3" cx="208" cy="125" rx="12" ry="10" transform="rotate(-60 208 125)"/>

                      {/* Back Paws */}
                      <ellipse fill="#F5E6D3" cx="65" cy="215" rx="28" ry="18"/>
                      <ellipse fill="#F5E6D3" cx="155" cy="215" rx="28" ry="18"/>
                      <ellipse fill="#FFB6C1" cx="55" cy="218" rx="6" ry="5"/>
                      <ellipse fill="#FFB6C1" cx="65" cy="222" rx="5" ry="4"/>
                      <ellipse fill="#FFB6C1" cx="75" cy="218" rx="6" ry="5"/>
                      <ellipse fill="#FFB6C1" cx="65" cy="212" rx="8" ry="6"/>
                      <ellipse fill="#FFB6C1" cx="145" cy="218" rx="6" ry="5"/>
                      <ellipse fill="#FFB6C1" cx="155" cy="222" rx="5" ry="4"/>
                      <ellipse fill="#FFB6C1" cx="165" cy="218" rx="6" ry="5"/>
                      <ellipse fill="#FFB6C1" cx="155" cy="212" rx="8" ry="6"/>

                      {/* Body */}
                      <ellipse fill="#F5E6D3" cx="110" cy="175" rx="65" ry="55"/>

                      {/* Head */}
                      <ellipse fill="#F5E6D3" cx="110" cy="95" rx="75" ry="70"/>

                      {/* Ears */}
                      <path fill="#F5E6D3" d="M45 75 L25 15 L75 55 Z"/>
                      <path fill="#F5E6D3" d="M175 75 L195 15 L145 55 Z"/>
                      <path fill="#E8D4C4" d="M40 55 L28 22 L58 48 Z"/>
                      <path fill="#E8D4C4" d="M180 55 L192 22 L162 48 Z"/>
                      <path fill="#FFCDB8" d="M48 60 L35 30 L65 52 Z"/>
                      <path fill="#FFCDB8" d="M172 60 L185 30 L155 52 Z"/>

                      {/* Eyes */}
                      <ellipse fill="white" cx="75" cy="95" rx="24" ry="28"/>
                      <ellipse fill="white" cx="145" cy="95" rx="24" ry="28"/>
                      <ellipse fill="#4A90D9" cx="75" cy="98" rx="18" ry="22"/>
                      <ellipse fill="#4A90D9" cx="145" cy="98" rx="18" ry="22"/>
                      <ellipse fill="#1a1a1a" cx="75" cy="100" rx="8" ry="10"/>
                      <ellipse fill="#1a1a1a" cx="145" cy="100" rx="8" ry="10"/>
                      <circle fill="white" cx="82" cy="88" r="7"/>
                      <circle fill="white" cx="152" cy="88" r="7"/>
                      <circle fill="white" cx="70" cy="102" r="4"/>
                      <circle fill="white" cx="140" cy="102" r="4"/>

                      {/* Nose */}
                      <path fill="#FF7F50" d="M110 115 L103 128 L117 128 Z"/>

                      {/* Whiskers */}
                      <line stroke="#999" strokeWidth="1.5" strokeLinecap="round" x1="20" y1="105" x2="55" y2="112"/>
                      <line stroke="#999" strokeWidth="1.5" strokeLinecap="round" x1="18" y1="118" x2="55" y2="120"/>
                      <line stroke="#999" strokeWidth="1.5" strokeLinecap="round" x1="20" y1="131" x2="55" y2="128"/>
                      <line stroke="#999" strokeWidth="1.5" strokeLinecap="round" x1="200" y1="105" x2="165" y2="112"/>
                      <line stroke="#999" strokeWidth="1.5" strokeLinecap="round" x1="202" y1="118" x2="165" y2="120"/>
                      <line stroke="#999" strokeWidth="1.5" strokeLinecap="round" x1="200" y1="131" x2="165" y2="128"/>

                      {/* Collar */}
                      <ellipse fill="#FF6B35" cx="110" cy="148" rx="45" ry="8"/>
                      <rect fill="#FF6B35" x="65" y="144" width="90" height="8" rx="4"/>

                      {/* Bell */}
                      <circle fill="#FFD700" cx="110" cy="158" r="10"/>
                      <circle fill="#FFF8DC" cx="107" cy="155" r="3"/>
                      <line stroke="#B8860B" strokeWidth="2" x1="110" y1="165" x2="110" y2="168"/>
                      <rect fill="#B8860B" x="105" y="148" width="10" height="6" rx="2"/>
                    </svg>
                  </div>
                </motion.div>

                {/* Speech bubble */}
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.8 }}
                  className="absolute top-0 right-0 sm:-right-8"
                >
                  <motion.div
                    animate={{ y: [0, -8, 0], rotate: [-2, 2, -2] }}
                    transition={{ duration: 3, repeat: Infinity }}
                    className="bg-white px-4 py-3 rounded-2xl shadow-lg font-bold text-teal-800"
                  >
                    Namaste! I am Peppi! 🔔
                    <div className="absolute bottom-0 left-8 w-0 h-0 border-l-[12px] border-l-transparent border-r-[12px] border-r-transparent border-t-[12px] border-t-white -mb-3" />
                  </motion.div>
                </motion.div>

                {/* AI Badge */}
                <motion.div
                  initial={{ opacity: 0, scale: 0 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 1 }}
                  className="absolute bottom-4 left-4"
                >
                  <motion.div
                    animate={{ scale: [1, 1.05, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                    className="bg-gradient-to-r from-pink-500 to-orange-500 text-white px-4 py-2 rounded-full text-sm font-bold shadow-lg"
                  >
                    AI Powered 🤖
                  </motion.div>
                </motion.div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-white to-orange-50/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <p className="text-pink-600 font-semibold uppercase tracking-wider mb-2">Why BhashaMitra?</p>
            <h2 className="text-3xl sm:text-4xl font-bold text-teal-800 mb-4">
              Learning Your Heritage Language Should Be Fun!
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Designed specifically for diaspora children who want to connect with their roots
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {FEATURES.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="bg-white rounded-3xl p-8 shadow-md hover:shadow-xl transition-all duration-300 hover:-translate-y-2 relative overflow-hidden group"
              >
                <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-orange-500 to-pink-500 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300" />
                <div className={`w-16 h-16 bg-gradient-to-br ${feature.gradient} rounded-2xl flex items-center justify-center text-3xl mb-6`}>
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold text-teal-800 mb-3">{feature.title}</h3>
                <p className="text-gray-600 mb-4">{feature.description}</p>
                <span className="inline-block bg-gray-100 text-teal-700 text-sm font-semibold px-4 py-1 rounded-full">
                  {feature.tag}
                </span>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Peppi Section */}
      <section id="peppi" className="py-24 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-teal-700 to-teal-600 relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-[10%] left-[10%] w-64 h-64 bg-white rounded-full blur-3xl" />
          <div className="absolute bottom-[10%] right-[10%] w-64 h-64 bg-white rounded-full blur-3xl" />
        </div>

        <div className="max-w-7xl mx-auto relative z-10">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
                Meet <span className="text-yellow-400">Peppi</span> - Your Learning Companion
              </h2>
              <p className="text-lg text-white/90 mb-8 leading-relaxed">
                Peppi is your child&apos;s friendly AI tutor, available as Peppi Bhaiya (brother) or Peppi Didi (sister).
                Peppi narrates stories with excitement, guides through lessons, and celebrates every achievement!
              </p>

              <div className="space-y-4">
                {[
                  { icon: '📚', title: 'Story Narrator', desc: 'Peppi reads stories aloud with emotion and excitement. Available in Standard & Premium tiers.' },
                  { icon: '🎓', title: 'Language Coach', desc: 'Practice conversations with Peppi. Get real-time feedback on pronunciation.', comingSoon: true },
                  { icon: '💬', title: 'AI Conversation Partner', desc: 'Chat with Peppi in your heritage language. Powered by advanced AI.', comingSoon: true },
                ].map((item) => (
                  <div
                    key={item.title}
                    className="flex items-start gap-4 bg-white/10 backdrop-blur-sm rounded-2xl p-5 hover:bg-white/15 transition-colors"
                  >
                    <div className="w-12 h-12 bg-yellow-400 rounded-xl flex items-center justify-center text-2xl flex-shrink-0">
                      {item.icon}
                    </div>
                    <div>
                      <h4 className="font-bold text-white mb-1">{item.title}</h4>
                      <p className="text-sm text-white/80">{item.desc}</p>
                      {item.comingSoon && (
                        <span className="inline-block mt-2 text-xs font-semibold bg-yellow-400/20 text-yellow-300 px-2 py-1 rounded-lg uppercase">
                          Coming Soon
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="flex justify-center"
            >
              <div className="bg-white rounded-3xl p-8 shadow-2xl text-center max-w-sm">
                <div className="w-36 h-36 mx-auto mb-6 bg-gradient-to-br from-orange-50 to-orange-100 rounded-full flex items-center justify-center shadow-lg">
                  <PeppiSVG size="lg" />
                </div>
                <h3 className="text-2xl font-bold text-teal-800 mb-2">Peppi</h3>
                <p className="text-gray-500 mb-6">Your AI Learning Friend</p>
                <div className="flex justify-center gap-3">
                  <span className="bg-blue-100 text-blue-700 px-4 py-2 rounded-full text-sm font-semibold">
                    Peppi Bhaiya
                  </span>
                  <span className="bg-pink-100 text-pink-700 px-4 py-2 rounded-full text-sm font-semibold">
                    Peppi Didi
                  </span>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-24 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <p className="text-pink-600 font-semibold uppercase tracking-wider mb-2">Simple Pricing</p>
            <h2 className="text-3xl sm:text-4xl font-bold text-teal-800 mb-4">
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
                    : 'bg-orange-50 hover:shadow-xl'
                } transition-all duration-300 hover:-translate-y-2`}
              >
                {tier.featured && (
                  <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-gradient-to-r from-pink-500 to-orange-500 text-white text-xs font-bold px-4 py-1.5 rounded-full uppercase tracking-wider">
                    Most Popular
                  </div>
                )}

                <div className="text-center pb-6 border-b border-current/10 mb-6">
                  <div className={`w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center text-3xl ${
                    tier.featured ? 'bg-white/20' : index === 0 ? 'bg-green-100' : 'bg-purple-100'
                  }`}>
                    {tier.icon}
                  </div>
                  <h3 className={`text-2xl font-bold mb-2 ${tier.featured ? 'text-white' : 'text-teal-800'}`}>
                    {tier.name}
                  </h3>
                  <div className={`text-4xl font-bold ${tier.featured ? 'text-white' : 'text-teal-800'}`}>
                    {tier.price}
                    <span className="text-lg font-normal opacity-70">/month</span>
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
                      </span>
                    </li>
                  ))}
                </ul>

                <Link href="/register" className="block">
                  <button className={`w-full py-3 rounded-full font-bold transition-all duration-300 ${tier.ctaClass}`}>
                    {tier.name === 'Free' ? 'Start Free' : `Get ${tier.name}`}
                  </button>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Festival Stories Section */}
      <section id="festivals" className="py-24 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-white to-orange-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <p className="text-pink-600 font-semibold uppercase tracking-wider mb-2">Cultural Stories</p>
            <h2 className="text-3xl sm:text-4xl font-bold text-teal-800 mb-4">
              Festival Stories From Every Tradition
            </h2>
            <p className="text-lg text-gray-600">Celebrating the beautiful diversity of Indian heritage</p>
          </div>

          <div className="flex gap-6 overflow-x-auto pb-6 snap-x snap-mandatory scrollbar-thin scrollbar-thumb-orange-400 scrollbar-track-gray-100">
            {FESTIVALS.map((festival, index) => (
              <motion.div
                key={festival.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
                className="min-w-[280px] bg-white rounded-3xl overflow-hidden shadow-md hover:shadow-xl transition-all duration-300 hover:-translate-y-2 snap-start"
              >
                <div className={`h-40 bg-gradient-to-br ${festival.gradient} flex items-center justify-center text-6xl`}>
                  {festival.icon}
                </div>
                <div className="p-6">
                  <h4 className="text-xl font-bold text-teal-800 mb-1">{festival.name}</h4>
                  <p className="text-sm text-gray-500 mb-2">{festival.religion}</p>
                  <p className="text-orange-600 font-semibold">{festival.stories} stories available</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-orange-500 to-pink-500 relative overflow-hidden">
        <div className="absolute inset-0 opacity-20">
          <div className="absolute top-[20%] left-[20%] w-64 h-64 bg-white rounded-full blur-3xl" />
          <div className="absolute bottom-[20%] right-[20%] w-64 h-64 bg-white rounded-full blur-3xl" />
        </div>

        <div className="max-w-3xl mx-auto text-center relative z-10">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-6"
          >
            Ready to Keep Your Heritage Alive?
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="text-xl text-white/90 mb-10"
          >
            Join families helping their children connect with their roots. Start your free trial today!
          </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="flex flex-col sm:flex-row gap-4 justify-center"
          >
            <Link href="/register">
              <button className="bg-white text-orange-600 px-8 py-4 rounded-full font-bold text-lg shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all duration-300">
                Start Free Trial
              </button>
            </Link>
            <a href="#features">
              <button className="border-2 border-white text-white px-8 py-4 rounded-full font-bold text-lg hover:bg-white hover:text-orange-600 transition-all duration-300">
                Learn More
              </button>
            </a>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-teal-800 text-white py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-12 mb-12">
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center">
                  <PeppiSVG size="sm" />
                </div>
                <span className="text-2xl font-bold">BhashaMitra</span>
              </div>
              <p className="text-white/70 text-sm leading-relaxed">
                Helping Indian diaspora children in New Zealand & Australia connect with their heritage through fun, interactive language learning.
              </p>
            </div>

            <div>
              <h4 className="font-bold mb-4">Product</h4>
              <ul className="space-y-3 text-white/70">
                <li><a href="#features" className="hover:text-yellow-400 transition-colors">Features</a></li>
                <li><a href="#pricing" className="hover:text-yellow-400 transition-colors">Pricing</a></li>
                <li><a href="#festivals" className="hover:text-yellow-400 transition-colors">Stories</a></li>
                <li><a href="#" className="hover:text-yellow-400 transition-colors">Games</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-bold mb-4">Company</h4>
              <ul className="space-y-3 text-white/70">
                <li><a href="#" className="hover:text-yellow-400 transition-colors">About Us</a></li>
                <li><a href="#" className="hover:text-yellow-400 transition-colors">Contact</a></li>
                <li><a href="#" className="hover:text-yellow-400 transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-yellow-400 transition-colors">Careers</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-bold mb-4">Legal</h4>
              <ul className="space-y-3 text-white/70">
                <li><Link href="/privacy" className="hover:text-yellow-400 transition-colors">Privacy Policy</Link></li>
                <li><Link href="/terms" className="hover:text-yellow-400 transition-colors">Terms of Service</Link></li>
                <li><Link href="/childrens-privacy" className="hover:text-yellow-400 transition-colors">Children&apos;s Privacy</Link></li>
                <li><Link href="/privacy#cookies" className="hover:text-yellow-400 transition-colors">Cookie Policy</Link></li>
              </ul>
            </div>
          </div>

          <div className="pt-8 border-t border-white/10 flex flex-col sm:flex-row justify-between items-center gap-4">
            <p className="text-white/60 text-sm">
              © 2025 BhashaMitra. Made with ❤️ in Auckland, New Zealand
            </p>
            <div className="flex gap-4">
              {['📘', '📸', '🐦', '📺'].map((icon, i) => (
                <a
                  key={i}
                  href="#"
                  className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center hover:bg-yellow-400 hover:-translate-y-1 transition-all duration-300"
                >
                  {icon}
                </a>
              ))}
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
