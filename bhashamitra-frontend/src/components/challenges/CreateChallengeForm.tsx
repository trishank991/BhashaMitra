'use client';

import React, { useState, useEffect } from 'react';
import api from '@/lib/api';
import type { CreateChallengeRequest, ChallengeCategoryOption } from '@/lib/api';
import { AlertCircle, Loader2 } from 'lucide-react';

interface Props {
  onSuccess: (code: string) => void;
  onCancel: () => void;
  canCreate: boolean;
  isQuotaLoading: boolean;
}

export default function CreateChallengeForm({ onSuccess, onCancel, canCreate, isQuotaLoading }: Props) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [categories, setCategories] = useState<ChallengeCategoryOption[]>([]);
  const [form, setForm] = useState<CreateChallengeRequest>({
    title: '',
    language: 'HINDI',
    category: '',
    difficulty: 'easy',
    question_count: 5,
    time_limit_seconds: 30,
  });

  useEffect(() => {
    async function loadCategories() {
      if (!form.language) return;
      try {
        const res = await api.getChallengeCategories(form.language);
        if (res.success && res.data?.data) {
          setCategories(res.data.data);
          // Set default category if not already set
          if (!form.category && res.data.data.length > 0) {
            setForm(f => ({ ...f, category: res.data.data[0].value }));
          }
        } else {
          setCategories([]);
        }
      } catch (error) {
        console.error("Failed to load categories", error);
        setCategories([]);
      }
    }
    loadCategories();
  }, [form.language]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!canCreate || isQuotaLoading) return;

    setIsSubmitting(true);
    try {
      const res = await api.createChallenge(form);
      if (res.success && res.data?.data?.code) {
        onSuccess(res.data.data.code);
      } else {
        alert(res.error || "Failed to create the challenge. Please try again.");
      }
    } catch (error) {
      alert("An unexpected error occurred. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const isSubmitDisabled = isSubmitting || isQuotaLoading || !canCreate;

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {!isQuotaLoading && !canCreate && (
        <div className="p-4 text-sm text-yellow-800 rounded-lg bg-yellow-50 flex items-center" role="alert">
          <AlertCircle className="w-5 h-5 mr-3 flex-shrink-0" />
          <span className="font-medium">Daily limit reached.</span> You can create more challenges tomorrow or upgrade your plan for unlimited access.
        </div>
      )}

      <fieldset disabled={isSubmitDisabled} className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700">
            Challenge Title
          </label>
          <input
            id="title"
            className="w-full p-2 border rounded-md mt-1 shadow-sm focus:ring-blue-500 focus:border-blue-500"
            placeholder="e.g., Fun Family Words Quiz"
            value={form.title}
            onChange={e => setForm({ ...form, title: e.target.value })}
            required
          />
        </div>

        <div>
          <label htmlFor="category" className="block text-sm font-medium text-gray-700">
            Category
          </label>
          <select
            id="category"
            className="w-full p-2 border rounded-md mt-1 shadow-sm focus:ring-blue-500 focus:border-blue-500"
            value={form.category}
            onChange={e => setForm({ ...form, category: e.target.value })}
            required
          >
            <option value="" disabled>
              Select a category
            </option>
            {categories.map(c => (
              <option key={c.value} value={c.value}>
                {c.label} ({c.item_count} questions available)
              </option>
            ))}
          </select>
        </div>
      </fieldset>

      <div className="flex justify-between items-center pt-4">
        <button type="button" onClick={onCancel} className="text-sm font-medium text-gray-600 hover:text-gray-900 disabled:opacity-50" disabled={isSubmitting}>
          Cancel
        </button>
        <button
          type="submit"
          disabled={isSubmitDisabled}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg font-semibold flex items-center justify-center disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {isSubmitting ? (
            <>
              <Loader2 className="w-5 h-5 mr-2 animate-spin" />
              Creating...
            </>
          ) : (
            'Create Challenge'
          )}
        </button>
      </div>
    </form>
  );
}
