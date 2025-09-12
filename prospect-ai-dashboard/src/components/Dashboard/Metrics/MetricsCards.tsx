import React from 'react';
import type { DashboardMetrics } from '@/types';
import { Card } from '@/components/UI/Card/Card';
import { MetricCard } from './MetricCard';

interface MetricsCardsProps {
  metrics: DashboardMetrics;
  loading?: boolean;
}

export const MetricsCards: React.FC<MetricsCardsProps> = ({ metrics, loading = false }) => {
  const metricCards = [
    {
      title: 'Total Prospects',
      value: metrics.total.toLocaleString(),
      change: '+12%',
      changeType: 'positive' as const,
      icon: 'users'
    },
    {
      title: 'Contacted',
      value: metrics.contacted.toLocaleString(),
      change: '+8%',
      changeType: 'positive' as const,
      icon: 'message'
    },
    {
      title: 'Response Rate',
      value: `${metrics.responseRate.toFixed(1)}%`,
      change: '+3.2%',
      changeType: 'positive' as const,
      icon: 'chart'
    },
    {
      title: 'Conversion Rate',
      value: `${metrics.conversionRate.toFixed(1)}%`,
      change: '+1.8%',
      changeType: 'positive' as const,
      icon: 'trending'
    }
  ];

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {Array.from({ length: 4 }).map((_, index) => (
          <Card key={index} className="animate-pulse">
            <div className="h-20 bg-gray-200 dark:bg-gray-700 rounded"></div>
          </Card>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {metricCards.map((metric, index) => (
        <MetricCard key={index} {...metric} />
      ))}
    </div>
  );
};