'use client';

import { useState, useEffect, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Search,
  Filter,
  Grid3X3,
  List,
  Calendar,
  X,
} from 'lucide-react';
import { Festival, FestivalReligion } from '@/types';
import api from '@/lib/api';
import { FestivalCard } from './FestivalCard';

type ViewMode = 'grid' | 'list' | 'calendar';

interface FestivalListProps {
  language?: string;
  onFestivalSelect?: (festival: Festival) => void;
}

const RELIGIONS: { value: FestivalReligion | 'ALL'; label: string }[] = [
  { value: 'ALL', label: 'All Religions' },
  { value: 'HINDU', label: 'Hindu' },
  { value: 'MUSLIM', label: 'Muslim' },
  { value: 'SIKH', label: 'Sikh' },
  { value: 'CHRISTIAN', label: 'Christian' },
  { value: 'JAIN', label: 'Jain' },
  { value: 'BUDDHIST', label: 'Buddhist' },
];

const MONTHS = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
];

export function FestivalList({ language, onFestivalSelect }: FestivalListProps) {
  const [festivals, setFestivals] = useState<Festival[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedReligion, setSelectedReligion] = useState<FestivalReligion | 'ALL'>('ALL');
  const [selectedMonth, setSelectedMonth] = useState<number | null>(null);
  const [viewMode, setViewMode] = useState<ViewMode>('grid');
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    const fetchFestivals = async () => {
      setLoading(true);
      const response = await api.getFestivals({
        religion: selectedReligion !== 'ALL' ? selectedReligion : undefined,
        month: selectedMonth ?? undefined,
      });
      if (response.success && response.data) {
        setFestivals(response.data);
      }
      setLoading(false);
    };
    fetchFestivals();
  }, [selectedReligion, selectedMonth]);

  const filteredFestivals = useMemo(() => {
    if (!searchQuery) return festivals;
    const query = searchQuery.toLowerCase();
    return festivals.filter(
      (f) =>
        f.name.toLowerCase().includes(query) ||
        f.name_native?.toLowerCase().includes(query) ||
        f.description?.toLowerCase().includes(query)
    );
  }, [festivals, searchQuery]);

  const festivalsByMonth = useMemo(() => {
    const grouped: Record<number, Festival[]> = {};
    filteredFestivals.forEach((f) => {
      const month = f.typical_month;
      if (!grouped[month]) grouped[month] = [];
      grouped[month].push(f);
    });
    return grouped;
  }, [filteredFestivals]);

  const clearFilters = () => {
    setSelectedReligion('ALL');
    setSelectedMonth(null);
    setSearchQuery('');
  };

  const hasActiveFilters = selectedReligion !== 'ALL' || selectedMonth !== null || searchQuery;

  return (
    <div className="space-y-4">
      {/* Search and View Controls */}
      <div className="flex flex-col sm:flex-row gap-3">
        {/* Search */}
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search festivals..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition-all"
          />
        </div>

        {/* Controls */}
        <div className="flex gap-2">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-xl border transition-all ${
              showFilters || hasActiveFilters
                ? 'bg-indigo-50 border-indigo-200 text-indigo-700'
                : 'border-gray-200 text-gray-600 hover:bg-gray-50'
            }`}
          >
            <Filter className="w-5 h-5" />
            <span className="hidden sm:inline">Filters</span>
            {hasActiveFilters && (
              <span className="bg-indigo-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                !
              </span>
            )}
          </button>

          {/* View Mode Toggle */}
          <div className="flex rounded-xl border border-gray-200 overflow-hidden">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2.5 ${viewMode === 'grid' ? 'bg-indigo-50 text-indigo-600' : 'text-gray-500 hover:bg-gray-50'}`}
            >
              <Grid3X3 className="w-5 h-5" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2.5 border-l border-gray-200 ${viewMode === 'list' ? 'bg-indigo-50 text-indigo-600' : 'text-gray-500 hover:bg-gray-50'}`}
            >
              <List className="w-5 h-5" />
            </button>
            <button
              onClick={() => setViewMode('calendar')}
              className={`p-2.5 border-l border-gray-200 ${viewMode === 'calendar' ? 'bg-indigo-50 text-indigo-600' : 'text-gray-500 hover:bg-gray-50'}`}
            >
              <Calendar className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Filters Panel */}
      <AnimatePresence>
        {showFilters && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div className="bg-gray-50 rounded-xl p-4 space-y-4">
              {/* Religion Filter */}
              <div>
                <label className="text-sm font-medium text-gray-700 mb-2 block">Religion</label>
                <div className="flex flex-wrap gap-2">
                  {RELIGIONS.map((r) => (
                    <button
                      key={r.value}
                      onClick={() => setSelectedReligion(r.value)}
                      className={`px-3 py-1.5 rounded-full text-sm transition-all ${
                        selectedReligion === r.value
                          ? 'bg-indigo-500 text-white'
                          : 'bg-white text-gray-600 border border-gray-200 hover:border-indigo-300'
                      }`}
                    >
                      {r.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Month Filter */}
              <div>
                <label className="text-sm font-medium text-gray-700 mb-2 block">Month</label>
                <div className="flex flex-wrap gap-2">
                  <button
                    onClick={() => setSelectedMonth(null)}
                    className={`px-3 py-1.5 rounded-full text-sm transition-all ${
                      selectedMonth === null
                        ? 'bg-indigo-500 text-white'
                        : 'bg-white text-gray-600 border border-gray-200 hover:border-indigo-300'
                    }`}
                  >
                    All
                  </button>
                  {MONTHS.map((m, idx) => (
                    <button
                      key={m}
                      onClick={() => setSelectedMonth(idx + 1)}
                      className={`px-3 py-1.5 rounded-full text-sm transition-all ${
                        selectedMonth === idx + 1
                          ? 'bg-indigo-500 text-white'
                          : 'bg-white text-gray-600 border border-gray-200 hover:border-indigo-300'
                      }`}
                    >
                      {m.slice(0, 3)}
                    </button>
                  ))}
                </div>
              </div>

              {/* Clear Filters */}
              {hasActiveFilters && (
                <button
                  onClick={clearFilters}
                  className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700"
                >
                  <X className="w-4 h-4" />
                  Clear all filters
                </button>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Results Count */}
      <div className="text-sm text-gray-500">
        {loading ? 'Loading...' : `${filteredFestivals.length} festivals found`}
      </div>

      {/* Festival Display */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="animate-pulse bg-gray-100 rounded-2xl h-48" />
          ))}
        </div>
      ) : viewMode === 'calendar' ? (
        /* Calendar View */
        <div className="space-y-6">
          {Object.entries(festivalsByMonth)
            .sort(([a], [b]) => parseInt(a) - parseInt(b))
            .map(([month, monthFestivals]) => (
              <div key={month}>
                <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2">
                  <Calendar className="w-5 h-5 text-indigo-500" />
                  {MONTHS[parseInt(month) - 1]}
                  <span className="text-sm font-normal text-gray-400">
                    ({monthFestivals.length})
                  </span>
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  {monthFestivals.map((festival) => (
                    <FestivalCard
                      key={festival.id}
                      festival={festival}
                      onClick={() => onFestivalSelect?.(festival)}
                    />
                  ))}
                </div>
              </div>
            ))}
        </div>
      ) : viewMode === 'list' ? (
        /* List View */
        <div className="space-y-3">
          {filteredFestivals.map((festival) => (
            <FestivalCard
              key={festival.id}
              festival={festival}
              compact
              onClick={() => onFestivalSelect?.(festival)}
            />
          ))}
        </div>
      ) : (
        /* Grid View */
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredFestivals.map((festival) => (
            <FestivalCard
              key={festival.id}
              festival={festival}
              onClick={() => onFestivalSelect?.(festival)}
            />
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && filteredFestivals.length === 0 && (
        <div className="text-center py-12">
          <Calendar className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-700 mb-2">No festivals found</h3>
          <p className="text-gray-500 mb-4">
            Try adjusting your filters or search query
          </p>
          <button
            onClick={clearFilters}
            className="text-indigo-600 hover:text-indigo-700 font-medium"
          >
            Clear all filters
          </button>
        </div>
      )}
    </div>
  );
}

export default FestivalList;
