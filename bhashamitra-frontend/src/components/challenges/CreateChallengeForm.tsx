'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import api, { ChallengeCategoryOption, CreateChallengeRequest } from '@/lib/api';

interface CreateChallengeFormProps {
  onSuccess: (code: string) => void;
  onCancel: () => void;
  defaultLanguage?: string;
}

const LANGUAGES = [
  { value: 'HINDI', label: 'Hindi', native: 'हिंदी' },
  { value: 'TAMIL', label: 'Tamil', native: 'தமிழ்' },
  { value: 'GUJARATI', label: 'Gujarati', native: 'ગુજરાતી' },
  { value: 'PUNJABI', label: 'Punjabi', native: 'ਪੰਜਾਬੀ' },
  { value: 'TELUGU', label: 'Telugu', native: 'తెలుగు' },
  { value: 'MALAYALAM', label: 'Malayalam', native: 'മലയാളം' },
];

const DIFFICULTIES = [
  { value: 'easy', label: 'Easy', description: 'Ages 4-6', emoji: '🌱' },
  { value: 'medium', label: 'Medium', description: 'Ages 7-10', emoji: '🌿' },
  { value: 'hard', label: 'Hard', description: 'Ages 11-14', emoji: '🌳' },
];

export function CreateChallengeForm({ onSuccess, onCancel, defaultLanguage = 'HINDI' }: CreateChallengeFormProps) {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [categories, setCategories] = useState<ChallengeCategoryOption[]>([]);
  const [categoriesLoading, setCategoriesLoading] = useState(true);

  const [formData, setFormData] = useState({
    title: '',
    title_native: '',
    language: defaultLanguage,
    category: '',
    difficulty: 'easy',
    question_count: 5,
    time_limit_seconds: 30,
  });

  // Fetch categories when language changes
  useEffect(() => {
    const fetchCategories = async () => {
      setCategoriesLoading(true);
      setFormData(prev => ({ ...prev, category: '' })); 

      try {
        const response = await api.getChallengeCategories(formData.language);
        if (response.success && response.data) {
          const fetchedCategories = response.data.data || [];
          setCategories(fetchedCategories);
          if (fetchedCategories.length > 0) {
            setFormData(prev => ({ ...prev, category: fetchedCategories[0].value }));
          }
        }
      } catch (error) {
        console.error("Failed to fetch categories", error);
        setCategories([]);
      } finally {
        setCategoriesLoading(false);
      }
    };

    if (formData.language) {
      fetchCategories();
    }
  }, [formData.language]);

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await api.createChallenge(formData as CreateChallengeRequest);
      if (response.success && response.data) {
        onSuccess(response.data.data.code);
      } else {
        setError(response.error || 'Failed to create challenge');
      }
    } catch (err) {
      setError('An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-3xl shadow-xl p-6 max-w-lg mx-auto">
      {/* Progress */}
      <div className="flex items-center gap-2 mb-6">
        {[1, 2, 3].map((s) => (
          <div
            key={s}
            className={`flex-1 h-2 rounded-full ${
              s <= step ? 'bg-purple-500' : 'bg-gray-200'
            }`}
          />
        ))}
      </div>

      {/* Step 1: Basic Info */}
      {step === 1 && (
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
        >
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Create Challenge</h2>

          {/* Language */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Language
            </label>
            <div className="grid grid-cols-3 gap-2">
              {LANGUAGES.map((lang) => (
                <button
                  key={lang.value}
                  onClick={() => setFormData({ ...formData, language: lang.value })}
                  className={`p-3 rounded-xl border-2 transition-all ${
                    formData.language === lang.value
                      ? 'border-purple-500 bg-purple-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="font-medium text-gray-900">{lang.label}</div>
                  <div className="text-sm text-gray-500">{lang.native}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Title */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Challenge Title
            </label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              placeholder="e.g., Learn Hindi Alphabet"
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
              maxLength={100}
            />
          </div>

          <button
            onClick={() => setStep(2)}
            disabled={!formData.title || !formData.language}
            className="w-full py-3 bg-purple-500 hover:bg-purple-600 disabled:bg-gray-300 text-white rounded-xl font-semibold transition-colors"
          >
            Next
          </button>
        </motion.div>
      )}

      {/* Step 2: Category & Difficulty */}
      {step === 2 && (
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
        >
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Choose Category</h2>

          {/* Category */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Topic
            </label>
            {categoriesLoading ? (
              <div className="text-center p-4">Loading topics...</div>
            ) : (
              <div className="grid grid-cols-2 gap-2">
                {categories.map((cat) => (
                  <button
                    key={cat.value}
                    onClick={() => setFormData({ ...formData, category: cat.value })}
                    className={`p-4 rounded-xl border-2 text-left transition-all ${
                      formData.category === cat.value
                        ? 'border-purple-500 bg-purple-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="font-medium text-gray-900">{cat.label}</div>
                    <div className="text-sm text-gray-500">{cat.item_count} items</div>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Difficulty */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Difficulty
            </label>
            <div className="flex gap-2">
              {DIFFICULTIES.map((diff) => (
                <button
                  key={diff.value}
                  onClick={() => setFormData({ ...formData, difficulty: diff.value })}
                  className={`flex-1 p-4 rounded-xl border-2 text-center transition-all ${
                    formData.difficulty === diff.value
                      ? 'border-purple-500 bg-purple-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="text-2xl mb-1">{diff.emoji}</div>
                  <div className="font-medium text-gray-900">{diff.label}</div>
                  <div className="text-xs text-gray-500">{diff.description}</div>
                </button>
              ))}
            </div>
          </div>

          <div className="flex gap-3">
            <button
              onClick={() => setStep(1)}
              className="flex-1 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl font-semibold transition-colors"
            >
              Back
            </button>
            <button
              onClick={() => setStep(3)}
              disabled={!formData.category || categoriesLoading}
              className="flex-1 py-3 bg-purple-500 hover:bg-purple-600 disabled:bg-gray-300 text-white rounded-xl font-semibold transition-colors"
            >
              Next
            </button>
          </div>
        </motion.div>
      )}

      {/* Step 3: Settings */}
      {step === 3 && (
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
        >
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Quiz Settings</h2>

          {/* Question Count */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Number of Questions: {formData.question_count}
            </label>
            <input
              type="range"
              min={3}
              max={10}
              value={formData.question_count}
              onChange={(e) => setFormData({ ...formData, question_count: parseInt(e.target.value) })}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-400">
              <span>3</span>
              <span>10</span>
            </div>
          </div>

          {/* Time Limit */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Time per Question: {formData.time_limit_seconds}s
            </label>
            <input
              type="range"
              min={10}
              max={60}
              step={5}
              value={formData.time_limit_seconds}
              onChange={(e) => setFormData({ ...formData, time_limit_seconds: parseInt(e.target.value) })}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-400">
              <span>10s</span>
              <span>60s</span>
            </div>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg text-sm">
              {error}
            </div>
          )}

          <div className="flex gap-3">
            <button
              onClick={() => setStep(2)}
              className="flex-1 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl font-semibold transition-colors"
            >
              Back
            </button>
            <button
              onClick={handleSubmit}
              disabled={loading}
              className="flex-1 py-3 bg-green-500 hover:bg-green-600 disabled:bg-gray-300 text-white rounded-xl font-semibold transition-colors"
            >
              {loading ? 'Creating...' : 'Create Challenge'}
            </button>
          </div>

          <button
            onClick={onCancel}
            className="w-full mt-3 py-2 text-gray-500 hover:text-gray-700 text-sm"
          >
            Cancel
          </button>
        </motion.div>
      )}
    </div>
  );
}
