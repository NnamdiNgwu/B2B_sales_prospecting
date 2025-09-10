import React from 'react';
import { Prospect } from '../../../types';
import { ProspectCard } from './ProspectCard';

interface PipelineStageProps {
  stage: {
    key: string;
    label: string;
    color: string;
    prospects: Prospect[];
    count: number;
  };
  isLast: boolean;
}

export const PipelineStage: React.FC<PipelineStageProps> = ({ stage, isLast }) => {
  return (
    <div className="relative">
      <div className="flex items-center justify-between mb-4">
        <h4 className="text-sm font-medium text-gray-900 dark:text-white">
          {stage.label}
        </h4>
        <span className="text-sm text-gray-500 dark:text-gray-400">
          {stage.count}
        </span>
      </div>
      
      <div className="space-y-3">
        {stage.prospects.slice(0, 5).map((prospect) => (
          <ProspectCard key={prospect.id} prospect={prospect} stageColor={stage.color} />
        ))}
        
        {stage.count > 5 && (
          <div className="text-center">
            <button className="text-sm text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300">
              +{stage.count - 5} more
            </button>
          </div>
        )}
      </div>
      
      {/* Pipeline connector */}
      {!isLast && (
        <div className="hidden lg:block absolute top-8 -right-3 w-6 h-0.5 bg-gray-300 dark:bg-gray-600">
          <div className="absolute right-0 top-1/2 transform -translate-y-1/2 w-2 h-2 bg-gray-300 dark:bg-gray-600 rotate-45"></div>
        </div>
      )}
    </div>
  );
};