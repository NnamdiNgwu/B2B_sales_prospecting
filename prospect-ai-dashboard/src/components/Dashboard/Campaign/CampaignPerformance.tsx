import React from 'react';
import { useCampaigns } from '@/hooks/useCampaigns';
import { Card } from '@/components/UI/Card/Card';
import { LoadingSpinner } from '@/components/UI/LoadingSpinner/LoadingSpinner';
import { ErrorMessage } from '@/components/UI/ErrorMessage/ErrorMessage';
import { formatDate } from '@/utils/utils';

export const CampaignPerformance: React.FC = () => {
  const { campaigns, loading, error } = useCampaigns();

  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  return (
    <Card>
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        Campaign Performance
      </h3>
      <div className="space-y-4">
        {campaigns.map((campaign) => (
          <div key={campaign.id} className="p-4 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800">
            <div className="flex justify-between items-start">
              <div>
                <p className="font-semibold text-gray-800 dark:text-gray-200">{campaign.name}</p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Started: {formatDate(campaign.startDate)}
                </p>
              </div>
              <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                campaign.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-200 text-gray-800'
              }`}>
                {campaign.status}
              </span>
            </div>
            <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">Sent</p>
                <p className="text-xl font-bold text-gray-900 dark:text-white">{campaign.sent}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">Opened</p>
                <p className="text-xl font-bold text-gray-900 dark:text-white">{campaign.opened}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">Clicked</p>
                <p className="text-xl font-bold text-gray-900 dark:text-white">{campaign.clicked}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">Replies</p>
                <p className="text-xl font-bold text-gray-900 dark:text-white">{campaign.replies}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};