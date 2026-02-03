'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';

export interface BreadcrumbItem {
  label: string;
  href?: string;
  emoji?: string;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
  className?: string;
}

export function Breadcrumb({ items, className = '' }: BreadcrumbProps) {
  return (
    <motion.nav
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex items-center flex-wrap gap-1 text-sm ${className}`}
      aria-label="Breadcrumb"
    >
      {/* Home link */}
      <Link
        href="/home"
        className="flex items-center text-gray-500 hover:text-gray-700 transition-colors"
      >
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
      </Link>

      {items.map((item, index) => {
        const isLast = index === items.length - 1;

        return (
          <span key={index} className="flex items-center">
            {/* Separator */}
            <svg className="w-4 h-4 text-gray-400 mx-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>

            {/* Item */}
            {isLast || !item.href ? (
              <span className={`flex items-center gap-1 ${isLast ? 'text-gray-900 font-medium' : 'text-gray-500'}`}>
                {item.emoji && <span className="text-base">{item.emoji}</span>}
                <span className="truncate max-w-[150px]">{item.label}</span>
              </span>
            ) : (
              <Link
                href={item.href}
                className="flex items-center gap-1 text-gray-500 hover:text-indigo-600 transition-colors"
              >
                {item.emoji && <span className="text-base">{item.emoji}</span>}
                <span className="truncate max-w-[150px]">{item.label}</span>
              </Link>
            )}
          </span>
        );
      })}
    </motion.nav>
  );
}
