'use client';

import React, { useState, useEffect } from 'react';
import api from '@/lib/api';

interface Props {
  onSuccess: (code: string) => void;
  onCancel: () => void;
  canCreate: boolean;
  isQuotaLoading: boolean;
}

const LANGUAGES = [
  { value: 'HINDI', label: 'Hindi' },
  { value: 'TAMIL', label: 'Tamil' },
  { value: 'GUJARATI', label: 'Gujarati' },
  { value: 'PUNJABI', label: 'Punjabi' },
  { value: 'TELUGU', label: 'Telugu' },
  { value: 'MALAYALAM', label: 'Malayalam' },
  { value: 'FIJI_HINDI', label: 'Fiji Hindi' },
];

interface Category {
  id: string;
  name: string;
  label?: string;
  slug?: string;
  value?: string;
  display_name?: string;
}

interface ChallengeFormData {
  title: string;
  description: string;
  language: string;
  category: string;
  difficulty: string;
  question_count: number;
  time_limit_seconds: number;
}

interface ApiResponse<T> {
  success: boolean;
  data?: T | { data: T };
  error?: string;
}

export default function CreateChallengeForm({ onSuccess, onCancel, canCreate, isQuotaLoading }: Props) {
  const [categories, setCategories] = useState<Category[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState<ChallengeFormData>({
    title: '',
    description: '',
    language: 'HINDI',
    category: '',
    difficulty: 'medium',
    question_count: 5,
    time_limit_seconds: 30
  });

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const res = await api.getChallengeCategories() as ApiResponse<Category[]>;
        if (res?.success && res?.data) {
          // Normalizes data structure for safety
          const data = res.data as Category[] | { data: Category[] };
          setCategories(Array.isArray(data) ? data : (data.data || []));
        }
      } catch (err) {
        console.error("Failed to fetch categories", err);
      }
    };
    fetchCategories();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!canCreate || isSubmitting) return;

    setIsSubmitting(true);
    setError(null);
    try {
      const res = await api.createChallenge(formData) as ApiResponse<{ code: string }>;
      if (res?.success && res?.data) {
        const data = res.data as { code: string } | { data: { code: string } };
        const code = 'code' in data ? data.code : data.data?.code;
        if (code) {
          onSuccess(code);
        } else {
          setError('Failed to create challenge');
        }
      } else if (res?.error) {
        setError(res.error);
      }
    } catch (err) {
      setError('An unexpected error occurred. Please try again.');
      console.error("Submission failed", err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 bg-white p-6 rounded-lg shadow">
      {/* Title Field */}
      <div>
        <label className="block text-sm font-medium text-gray-700">Challenge Title</label>
        <input
          type="text"
          required
          placeholder="e.g., Daily Hindi Vocabulary"
          className="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          disabled={!canCreate || isSubmitting}
        />
      </div>

      {/* Description Field */}
      <div>
        <label className="block text-sm font-medium text-gray-700">Description</label>
        <textarea
          rows={3}
          placeholder="Describe what this challenge is about..."
          className="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          disabled={!canCreate || isSubmitting}
        />
      </div>

      {/* Category Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700">Category</label>
        <select
          required
          className="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          value={formData.category}
          onChange={(e) => setFormData({ ...formData, category: e.target.value })}
          disabled={!canCreate || isSubmitting}
        >
          <option value="">Select a category</option>
          {/* eslint-disable-next-line @typescript-eslint/no-explicit-any */}
          {categories.map((cat: Category) => (
            <option key={cat.id || cat.slug || cat.value} value={cat.id || cat.slug || cat.value}>
              {cat.name || cat.display_name || cat.label || 'Unnamed Category'}
            </option>
          ))}
        </select>
      </div>

      {/* Language Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700">Language</label>
        <select
          required
          className="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          value={formData.language}
          onChange={(e) => setFormData({ ...formData, language: e.target.value })}
          disabled={!canCreate || isSubmitting}
        >
          {LANGUAGES.map((lang) => (
            <option key={lang.value} value={lang.value}>
              {lang.label}
            </option>
          ))}
        </select>
      </div>

      {/* Difficulty Row */}
      <div>
        <label className="block text-sm font-medium text-gray-700">Difficulty</label>
        <select
          className="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500"
          value={formData.difficulty}
          onChange={(e) => setFormData({ ...formData, difficulty: e.target.value })}
          disabled={!canCreate || isSubmitting}
        >
          <option value="easy">Easy (Ages 4-6)</option>
          <option value="medium">Medium (Ages 7-10)</option>
          <option value="hard">Hard (Ages 11-14)</option>
        </select>
      </div>

      {/* Question Count and Time Limit Row */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Number of Questions</label>
          <select
            className="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500"
            value={formData.question_count}
            onChange={(e) => setFormData({ ...formData, question_count: parseInt(e.target.value) })}
            disabled={!canCreate || isSubmitting}
          >
            <option value={3}>3 Questions</option>
            <option value={5}>5 Questions</option>
            <option value={7}>7 Questions</option>
            <option value={10}>10 Questions</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Time per Question (Secs)</label>
          <select
            className="mt-1 block w-full border border-gray-300 rounded-md p-2 shadow-sm focus:ring-blue-500 focus:border-blue-500"
            value={formData.time_limit_seconds}
            onChange={(e) => setFormData({ ...formData, time_limit_seconds: parseInt(e.target.value) })}
            disabled={!canCreate || isSubmitting}
          >
            <option value={15}>15 seconds</option>
            <option value={30}>30 seconds</option>
            <option value={45}>45 seconds</option>
            <option value={60}>60 seconds</option>
          </select>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-4 pt-4 border-t">
        <button
          type="submit"
          disabled={!canCreate || isSubmitting || isQuotaLoading}
          className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-gray-400 transition-colors"
        >
          {isSubmitting ? 'Creating...' : 'Create Challenge'}
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="flex-1 bg-gray-100 text-gray-700 py-2 px-4 rounded-md font-medium hover:bg-gray-200 transition-colors"
        >
          Cancel
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-md">
          <p className="text-red-600 text-sm text-center font-medium">
            {error}
          </p>
        </div>
      )}

      {/* Quota Restriction Message */}
      {!canCreate && !isQuotaLoading && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-md">
          <p className="text-red-600 text-sm text-center font-medium">
            Daily creation limit reached. Please upgrade your plan or try again tomorrow.
          </p>
        </div>
      )}
    </form>
  );
}