import { useState, useEffect } from 'react';
import { Campaign } from '../types/types';
import { prospectService } from '../services/ProspectService';
import { getErrorMessage } from './useErrorHandler';

export const useCampaigns = () => {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCampaigns = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await prospectService.getCampaigns();
        setCampaigns(data);
      } catch (err) {
        setError(getErrorMessage(err));
      } finally {
        setLoading(false);
      }
    };

    fetchCampaigns();
  }, []);

  return { campaigns, loading, error };
};