import React from 'react';
import { Card } from '../Card/Card';

interface ErrorMessageProps {
  title: string;
  message: string;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({ title, message }) => {
  return (
    <Card variant="outline" className="max-w-lg w-full border-red-500/50 bg-red-50 dark:bg-red-900/20">
      <div className="flex items-center">
        <div className="flex-shrink-0">
          <svg className="h-6 w-6 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div className="ml-4">
          <h3 className="text-lg font-medium text-red-800 dark:text-red-200">{title}</h3>
          <div className="mt-2 text-sm text-red-700 dark:text-red-300">
            <p>{message}</p>
          </div>
        </div>
      </div>
    </Card>
  );
};