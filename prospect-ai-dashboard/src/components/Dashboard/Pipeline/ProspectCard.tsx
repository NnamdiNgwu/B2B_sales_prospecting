import React from 'react';
import type { Prospect } from '@/types';
import { cn } from '@/utils/classNames';

interface ProspectCardProps {
  prospect: Prospect;
  stageColor: string;
}

export const ProspectCard: React.FC<ProspectCardProps> = ({ prospect, stageColor }) => {
  return (
    <div className="p-3 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-semibold text-gray-900 dark:text-white">{prospect.name}</p>
          <p className="text-xs text-gray-500 dark:text-gray-400">{prospect.company}</p>
        </div>
        <span
          className={cn('px-2 py-0.5 text-xs font-medium rounded-full', stageColor)}
        >
          {prospect.status}
        </span>
      </div>
      <p className="mt-2 text-xs text-gray-600 dark:text-gray-300 truncate">
        Last contact: {prospect.lastContactDate}
      </p>
    </div>
  );
};