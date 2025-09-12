import React, { useState } from 'react';
import { Header } from './Header/Header';
import { MetricsCards } from './Metrics/MetricsCards';
import { ProspectPipeline } from './Pipeline/ProspectPipeline';
import { ProspectTable } from './Table/ProspectTable';
import { FilterPanel } from './Filters/FilterPanel';
import { CampaignPerformance } from './Campaign/CampaignPerformance';
import { useProspects } from '@/hooks/useProspects';
import { useCampaigns } from '@/hooks/useCampaigns';
import { useDashboardMetrics } from '@/hooks/useDashboardMetrics';
import { Button } from '@/components/UI/Button/Button';
import { Card } from '@/components/UI/Card/Card';
import { LoadingSpinner } from '@/components/UI/LoadingSpinner/LoadingSpinner';
import { ErrorMessage } from '@/components/UI/ErrorMessage/ErrorMessage';

export const Dashboard: React.FC = () => {
  const [showFilters, setShowFilters] = useState(false);
  const [selectedView, setSelectedView] = useState<'table' | 'pipeline'>('table');

  const { 
    prospects, 
    loading: prospectsLoading, 
    error: prospectsError,
    filters,
    updateFilters 
  } = useProspects();
  
  const { campaigns, loading: campaignsLoading } = useCampaigns();
  const { metrics, loading: metricsLoading } = useDashboardMetrics(prospects);

  const isLoading = prospectsLoading || campaignsLoading || metricsLoading;

  if (isLoading && !prospectsError) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <Header />
        <div className="flex items-center justify-center min-h-[calc(100vh-4rem)]">
          <LoadingSpinner size="lg" />
        </div>
      </div>
    );
  }

  if (prospectsError) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <Header />
        <div className="flex items-center justify-center min-h-[calc(100vh-4rem)]">
          <ErrorMessage 
            title="Error Loading Dashboard"
            message={prospectsError}
          />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <MetricsCards metrics={metrics} />
        
        <div className="mb-8">
          <CampaignPerformance campaigns={campaigns || []} />
        </div>

        <Card padding="none">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div className="flex items-center gap-4">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Prospects ({prospects.length})
                </h2>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setShowFilters(!showFilters)}
                  leftIcon={
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
                    </svg>
                  }
                >
                  Filters
                </Button>
              </div>
              
              <div className="flex items-center gap-2">
                <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
                  <Button
                    variant={selectedView === 'table' ? 'primary' : 'ghost'}
                    size="sm"
                    onClick={() => setSelectedView('table')}
                  >
                    Table View
                  </Button>
                  <Button
                    variant={selectedView === 'pipeline' ? 'primary' : 'ghost'}
                    size="sm"
                    onClick={() => setSelectedView('pipeline')}
                  >
                    Pipeline View
                  </Button>
                </div>
              </div>
            </div>
          </div>

          {showFilters && (
            <FilterPanel 
              filters={filters}
              onFiltersChange={updateFilters}
              prospects={prospects}
            />
          )}
        </Card>

        <div className="mt-6">
          {selectedView === 'table' ? (
            <ProspectTable prospects={prospects} />
          ) : (
            <ProspectPipeline prospects={prospects} />
          )}
        </div>
      </div>
    </div>
  );
};