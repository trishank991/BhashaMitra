'use client';

import React, { useState, useEffect } from 'react';
import api from '@/lib/api';
import { CreateChallengeRequest } from '@/lib/api';

interface Category { value: string; label: string; }
interface Props { onSuccess: (code: string) => void; onCancel: () => void; }

export default function CreateChallengeForm({ onSuccess, onCancel }: Props) {
  const [loading, setLoading] = useState(false);
  const [categories, setCategories] = useState<Category[]>([]);
  const [form, setForm] = useState<CreateChallengeRequest>({
    title: '', language: 'HINDI', category: '', difficulty: 'BEGINNER', question_count: 5,
  });

  useEffect(() => {
    async function load() {
      const res = await api.getChallengeCategories(form.language);
      if (res.success && res.data) setCategories(res.data);
    }
    load();
  }, [form.language]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    const res = await api.createChallenge(form);
    if (res.success && res.data) onSuccess(res.data.code);
    else alert(res.error || "Failed to create");
    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input className="w-full p-2 border rounded" placeholder="Title" value={form.title} onChange={e => setForm({...form, title: e.target.value})} required />
      <select className="w-full p-2 border rounded" value={form.category} onChange={e => setForm({...form, category: e.target.value})} required>
        <option value="">Select Category</option>
        {categories.map(c => <option key={c.value} value={c.value}>{c.label}</option>)}
      </select>
      <div className="flex justify-between mt-4">
        <button type="button" onClick={onCancel}>Cancel</button>
        <button type="submit" disabled={loading} className="bg-blue-600 text-white px-4 py-2 rounded">{loading ? 'Saving...' : 'Create'}</button>
      </div>
    </form>
  );
}
