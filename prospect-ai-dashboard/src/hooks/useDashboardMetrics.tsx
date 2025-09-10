import { useState, useEffect } from 'react';
import { Prospect, DashboardMetrics } from '../types/types';

export const useDashboardMetrics = (prospects: Prospect[]) => {
  const [metrics, setMetrics] = useState<DashboardMetrics>({
    total: 0,
    contacted: 0,
    responded: 0,
    converted: 0,
    responseRate: 0,
    conversionRate: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (prospects.length > 0) {
      setLoading(true);
      const total = prospects.length;
      const contacted = prospects.filter(p => p.status !== 'new').length;
      const responded = prospects.filter(p => ['responded', 'qualified', 'converted'].includes(p.status)).length;
      const converted = prospects.filter(p => p.status === 'converted').length;
      
      const responseRate = contacted > 0 ? (responded / contacted) * 100 : 0;
      const conversionRate = contacted > 0 ? (converted / contacted) * 100 : 0;

      setMetrics({
        total,
        contacted,
        responded,
        converted,
        responseRate,
        conversionRate,
      });
      setLoading(false);
    }
  }, [prospects]);

  return { metrics, loading };
};