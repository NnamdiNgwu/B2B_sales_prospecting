import type { Prospect, Campaign, FilterOptions } from "@/types";

class ProspectService {
  private baseUrl = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api';

  async getProspects(filters?: FilterOptions): Promise<Prospect[]> {
    try {
      const queryParams = new URLSearchParams();
      
      if (filters) {
        if (filters.search) queryParams.append('search', filters.search);
        if (filters.industry.length) queryParams.append('industry', filters.industry.join(','));
        if (filters.status.length) queryParams.append('status', filters.status.join(','));
        // Add other filters...
      }

      const response = await fetch(`${this.baseUrl}/prospects?${queryParams}`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch prospects: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching prospects:', error);
      throw error;
    }
  }

  async getCampaigns(): Promise<Campaign[]> {
    try {
      const response = await fetch(`${this.baseUrl}/campaigns`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch campaigns: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching campaigns:', error);
      throw error;
    }
  }

  async updateProspectStatus(prospectId: string, status: string): Promise<void> {
    try {
      const response = await fetch(`${this.baseUrl}/prospects/${prospectId}/status`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status }),
      });

      if (!response.ok) {
        throw new Error(`Failed to update prospect status: ${response.statusText}`);
      }
    } catch (error) {
      console.error('Error updating prospect status:', error);
      throw error;
    }
  }
}

export const prospectService = new ProspectService();