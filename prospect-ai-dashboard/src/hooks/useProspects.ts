data_science_projects/B2B_sales_prospecting/ai_job_hunt/src/hooks/useProspects.ts
import { useState, useEffect } from 'react';
import { Prospect, FilterOptions } from '../types/types';
import { prospectService } from '../services/ProspectService';
import { getErrorMessage } from './useErrorHandler';

const initialFilters: FilterOptions = {
  search: '',
  industry: [],
  companySize: [],
  leadScore: [0, 100],
  status: [],
  location: [],
  tags: [],
};

export const useProspects = () => {
  const [prospects, setProspects] = useState<Prospect[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<FilterOptions>(initialFilters);

  useEffect(() => {
    const fetchProspects = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await prospectService.getProspects(filters);
        setProspects(data);
      } catch (err) {
        setError(getErrorMessage(err));
      } finally {
        setLoading(false);
      }
    };

    fetchProspects();
  }, [filters]);

  const updateFilters = (newFilters: Partial<FilterOptions>) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  return { prospects, loading, error, filters, updateFilters };
};



// import { useState, useEffect, useCallback } from 'react';
// import { Prospect, FilterOptions } from '../types';
// import { prospectService } from '../services/prospectService';
// import { getErrorMessage } from './useErrorHandler';

// interface UseProspectsReturn {
//   prospects: Prospect[];
//   loading: boolean;
//   error: string | null;
//   filters: FilterOptions;
//   updateFilters: (newFilters: Partial<FilterOptions>) => void;
//   refetch: () => Promise<void>;
// }

// const initialFilters: FilterOptions = {
//   search: '',
//   industry: [],
//   companySize: [],
//   leadScore: [0, 100],
//   status: [],
//   location: [],
//   tags: []
// };

// export const useProspects = (): UseProspectsReturn => {
//   const [prospects, setProspects] = useState<Prospect[]>([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState<string | null>(null);
//   const [filters, setFilters] = useState<FilterOptions>(initialFilters);

//   const fetchProspects = useCallback(async (currentFilters: FilterOptions) => {
//     try {
//       setLoading(true);
//       setError(null);
//       const data = await prospectService.getProspects(currentFilters);
//       setProspects(data);
//     } catch (err) {
//       setError(getErrorMessage(err));
//     } finally {
//       setLoading(false);
//     }
//   }, []);

//   useEffect(() => {
//     fetchProspects(filters);
//   }, [filters, fetchProspects]);

//   const updateFilters = useCallback((newFilters: Partial<FilterOptions>) => {
//     setFilters(prevFilters => ({ ...prevFilters, ...newFilters }));
//   }, []);

//   const refetch = useCallback(() => fetchProspects(filters), [filters, fetchProspects]);

//   return {
//     prospects,
//     loading,
//     error,
//     filters,
//     updateFilters,
//     refetch
//   };
// };


