import React, { HTMLAttributes, forwardRef } from 'react';
import { cn } from "@/utils/classNames";

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'elevated' | 'outline';
  padding?: 'none' | 'sm' | 'md' | 'lg';
}

const Card = forwardRef<HTMLDivElement, CardProps>(({
  className,
  variant = 'default',
  padding = 'md',
  children,
  ...props
}, ref) => {
  const baseClasses = 'bg-white dark:bg-gray-800 rounded-lg transition-colors duration-200';
  
  const variants = {
    default: 'border border-gray-200 dark:border-gray-700',
    elevated: 'shadow-lg border border-gray-200 dark:border-gray-700',
    outline: 'border-2 border-gray-300 dark:border-gray-600'
  };

  const paddings = {
    none: '',
    sm: 'p-3',
    md: 'p-6',
    lg: 'p-8'
  };

  return (
    <div
      ref={ref}
      className={cn(
        baseClasses,
        variants[variant],
        paddings[padding],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
});

Card.displayName = 'Card';

export { Card };