'use client';

import { useEffect, useState, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import {
  ArrowLeft,
  Calendar,
  Download,
  Share2,
  Loader2,
  AlertCircle,
  RefreshCw,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuthStore } from '@/stores';
import { Loading } from '@/components/ui';
import parentApi, { ReportCard } from '@/services/parentApi';
import {
  StatsOverview,
  SkillMasteryCard,
  AchievementsCard,
  InsightsCard,
  StreakCard,
  PronunciationCard,
  ContentProgressCard,
} from '@/components/report-card';

type ReportPeriod = 'weekly' | 'monthly' | 'all_time';

export default function ReportCardPage() {
  const params = useParams();
  const router = useRouter();
  const childId = params.childId as string;

  const [isHydrated, setIsHydrated] = useState(false);
  const { isAuthenticated } = useAuthStore();

  const [reportCard, setReportCard] = useState<ReportCard | null>(null);
  const [period, setPeriod] = useState<ReportPeriod>('monthly');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  const fetchReportCard = useCallback(async () => {
    if (!childId) return;

    setIsLoading(true);
    setError(null);

    try {
      const data = await parentApi.getReportCard(childId, period);
      setReportCard(data);
    } catch (err) {
      console.error('Failed to fetch report card:', err);
      setError('Failed to load report card. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }, [childId, period]);

  useEffect(() => {
    if (isHydrated && isAuthenticated && childId) {
      fetchReportCard();
    }
  }, [isHydrated, isAuthenticated, childId, fetchReportCard]);

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

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const periodLabels: Record<ReportPeriod, string> = {
    weekly: 'This Week',
    monthly: 'This Month',
    all_time: 'All Time',
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <button
                onClick={() => router.back()}
                className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-full transition-colors"
              >
                <ArrowLeft size={20} />
              </button>
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  {reportCard?.child_name ? `${reportCard.child_name}'s Report Card` : 'Report Card'}
                </h1>
                {reportCard?.report_period && (
                  <p className="text-sm text-gray-500">
                    {formatDate(reportCard.report_period.start_date)} - {formatDate(reportCard.report_period.end_date)}
                  </p>
                )}
              </div>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={fetchReportCard}
                className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-full transition-colors"
                title="Refresh"
              >
                <RefreshCw size={18} />
              </button>
              <button
                className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-full transition-colors"
                title="Download PDF"
              >
                <Download size={18} />
              </button>
              <button
                className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-full transition-colors"
                title="Share"
              >
                <Share2 size={18} />
              </button>
            </div>
          </div>

          {/* Period Selector */}
          <div className="flex gap-2 mt-4">
            {(['weekly', 'monthly', 'all_time'] as ReportPeriod[]).map((p) => (
              <button
                key={p}
                onClick={() => setPeriod(p)}
                className={cn(
                  'px-4 py-2 rounded-full text-sm font-medium transition-colors',
                  period === p
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                )}
              >
                {periodLabels[p]}
              </button>
            ))}
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-6">
        {isLoading ? (
          <div className="flex items-center justify-center py-20">
            <div className="text-center">
              <Loader2 className="w-8 h-8 animate-spin text-primary-600 mx-auto mb-4" />
              <p className="text-gray-500">Loading report card...</p>
            </div>
          </div>
        ) : error ? (
          <div className="flex items-center justify-center py-20">
            <div className="text-center">
              <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
              <p className="text-gray-700 mb-4">{error}</p>
              <button
                onClick={fetchReportCard}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                Try Again
              </button>
            </div>
          </div>
        ) : reportCard ? (
          <div className="space-y-6">
            {/* Stats Overview */}
            <motion.section
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Calendar className="w-5 h-5 text-primary-600" />
                Overview
              </h2>
              <StatsOverview stats={reportCard.overall_stats} />
            </motion.section>

            {/* Two Column Layout */}
            <div className="grid md:grid-cols-2 gap-6">
              {/* Left Column */}
              <div className="space-y-6">
                {/* Streak Card */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                >
                  <StreakCard streak={reportCard.streak} />
                </motion.div>

                {/* Skill Mastery */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                >
                  <SkillMasteryCard skills={reportCard.skill_mastery} />
                </motion.div>

                {/* Pronunciation Stats */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 }}
                >
                  <PronunciationCard pronunciation={reportCard.pronunciation} />
                </motion.div>
              </div>

              {/* Right Column */}
              <div className="space-y-6">
                {/* Content Progress */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.15 }}
                >
                  <ContentProgressCard content={reportCard.content_completion} />
                </motion.div>

                {/* Insights */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.25 }}
                >
                  <InsightsCard insights={reportCard.insights} />
                </motion.div>

                {/* Achievements */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.35 }}
                >
                  <AchievementsCard achievements={reportCard.achievements} />
                </motion.div>
              </div>
            </div>

            {/* Footer */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="text-center py-6 text-sm text-gray-500"
            >
              Report generated on {formatDate(reportCard.generated_at)}
            </motion.div>
          </div>
        ) : (
          <div className="text-center py-20">
            <AlertCircle className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">No report data available</p>
          </div>
        )}
      </main>
    </div>
  );
}
