// import React from 'react';
// import { Prospect } from '@/types';
// import { ProspectCard } from './ProspectCard';
// import { STAGE_COLORS } from '@/constants/dashboard';

// interface PipelineStageProps {
//   stage: {
//     key: string;
//     label: string;
//     color: string;
//     prospects: Prospect[];
//     count: number;
//   };
//   isLast: boolean;
// }

// export const PipelineStage: React.FC<PipelineStageProps> = ({ stage, isLast }) => {
//   return (
//     <div className="relative">
//       <div className="flex items-center justify-between mb-4">
//         <h4 className="text-sm font-medium text-gray-900 dark:text-white">
//           {stage.label}
//         </h4>
//         <span className="text-sm text-gray-500 dark:text-gray-400">
//           {stage.count}
//         </span>
//       </div>
      
//       <div className="space-y-3">
//         {stage.prospects.slice(0, 5).map((prospect) => (
//           <ProspectCard key={prospect.id} prospect={prospect} stageColor={stage.color} />
//         ))}
        
//         {stage.count > 5 && (
//           <div className="text-center">
//             <button className="text-sm text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300">
//               +{stage.count - 5} more
//             </button>
//           </div>
//         )}
//       </div>
      
//       {/* Pipeline connector */}
//       {!isLast && (
//         <div className="hidden lg:block absolute top-8 -right-3 w-6 h-0.5 bg-gray-300 dark:bg-gray-600">
//           <div className="absolute right-0 top-1/2 transform -translate-y-1/2 w-2 h-2 bg-gray-300 dark:bg-gray-600 rotate-45"></div>
//         </div>
//       )}
//     </div>
//   );
// };

// export const ProspectPipeline: React.FC<{ prospects: Prospect[] }> = ({ prospects }) => {
//   const stages = Object.keys(STAGE_COLORS);

//   const prospectsByStage = stages.reduce((acc, stage) => {
//     acc[stage] = prospects.filter(p => p.status === stage);
//     return acc;
//   }, {} as Record<string, Prospect[]>);

//   return (
//     <div className="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg">
//       <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Prospect Pipeline</h2>
//       <div className="flex overflow-x-auto space-x-4 pb-4">
//         {stages.map((stage, index) => (
//           <PipelineStage 
//             key={stage} 
//             stage={{ name: stage, prospects: prospectsByStage[stage] || [] }} 
//             isLast={index === stages.length - 1} 
//           />
//         ))}
//       </div>
//     </div>
//   );
// };


import React from 'react';
import type { Prospect } from '@/types';
import { STAGES, STAGE_COLORS } from '@/constants/dashboard';
import { ProspectCard } from './ProspectCard';

interface PipelineStageProps {
  stage: string;
  prospects: Prospect[];
}

const PipelineStage: React.FC<PipelineStageProps> = ({ stage, prospects }) => {
  return (
    <div className="flex-1 min-w-[280px] bg-gray-50 dark:bg-gray-800/50 rounded-lg p-3">
      <h3 className="font-semibold text-gray-800 dark:text-gray-200 mb-3 px-1">
        {stage} <span className="text-sm text-gray-500">{prospects.length}</span>
      </h3>
      <div className="space-y-3 h-full overflow-y-auto">
        {prospects.map(prospect => (
          <ProspectCard key={prospect.id} prospect={prospect} stageColor={STAGE_COLORS[stage]} />
        ))}
      </div>
    </div>
  );
};

export const ProspectPipeline: React.FC<{ prospects: Prospect[] }> = ({ prospects }) => {
  const prospectsByStage = STAGES.reduce((acc, stage) => {
    acc[stage] = prospects.filter(p => p.status === stage);
    return acc;
  }, {} as { [key: string]: Prospect[] });

  return (
    <div className="flex space-x-4 overflow-x-auto pb-4">
      {STAGES.map(stage => (
        <PipelineStage key={stage} stage={stage} prospects={prospectsByStage[stage] || []} />
      ))}
    </div>
  );
};