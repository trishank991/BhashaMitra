'use client';

import { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { useAuthStore } from '@/stores';
import { ChildProfile } from '@/types';

export function ChildSwitcher() {
  const { children, activeChild, setActiveChild } = useAuthStore();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  if (!activeChild || children.length === 0) return null;

  const handleSelect = (child: ChildProfile) => {
    setActiveChild(child);
    setIsOpen(false);
  };

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/80 border border-gray-200 hover:bg-white transition-colors"
      >
        <span className="text-lg">{activeChild.avatar || '👤'}</span>
        <span className="text-sm font-medium text-gray-700 max-w-[80px] truncate">
          {activeChild.name}
        </span>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-3.5 h-3.5 text-gray-400">
          <path strokeLinecap="round" strokeLinejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute right-0 top-full mt-1 w-56 bg-white rounded-xl shadow-lg border border-gray-200 py-1 z-50">
          {children.map((child) => (
            <button
              key={child.id}
              onClick={() => handleSelect(child)}
              className={`w-full flex items-center gap-3 px-4 py-2.5 text-left hover:bg-gray-50 transition-colors ${
                activeChild.id === child.id ? 'bg-primary-50' : ''
              }`}
            >
              <span className="text-xl">{child.avatar || '👤'}</span>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">{child.name}</p>
                <p className="text-xs text-gray-500">Age {child.age}</p>
              </div>
              {activeChild.id === child.id && (
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-primary-500">
                  <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 0 1 .143 1.052l-8 10.5a.75.75 0 0 1-1.127.075l-4.5-4.5a.75.75 0 0 1 1.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 0 1 1.05-.143Z" clipRule="evenodd" />
                </svg>
              )}
            </button>
          ))}
          <div className="border-t border-gray-100 mt-1 pt-1">
            <Link
              href="/children"
              onClick={() => setIsOpen(false)}
              className="flex items-center gap-3 px-4 py-2.5 text-left hover:bg-gray-50 transition-colors"
            >
              <span className="text-xl">⚙️</span>
              <span className="text-sm text-gray-600">Manage Children</span>
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}

export default ChildSwitcher;
