import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}


export const formatNumber = (num: number): string => {
  return new Intl.NumberFormat().format(num);
};

export const formatPercentage = (num: number, decimals: number = 1): string => {
  return `${num.toFixed(decimals)}%`;
};

export function formatDate(
  input?: string | number | Date | null,
  options?: Intl.DateTimeFormatOptions
): string {
  if (!input) return '—'
  const date = input instanceof Date ? input : new Date(input)
  if (isNaN(date.getTime())) return '—'
  const fmt = new Intl.DateTimeFormat(undefined, {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    ...options,
  })
  return fmt.format(date)
}

export const formatRelativeTime = (date: string | Date): string => {
  const now = new Date();
  const targetDate = new Date(date);
  const diffInMs = now.getTime() - targetDate.getTime();
  const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24));
  
  if (diffInDays === 0) return 'Today';
  if (diffInDays === 1) return 'Yesterday';
  if (diffInDays < 7) return `${diffInDays} days ago`;
  if (diffInDays < 30) return `${Math.floor(diffInDays / 7)} weeks ago`;
  
  return formatDate(date);
};