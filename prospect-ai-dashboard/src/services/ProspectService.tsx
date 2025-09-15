//ospect-ai-dashboard/src/services/ProspectService.tsx
import { http } from '@/services/api';
import type { Prospect, Campaign } from '@/types';

export type FilterOptions = {
  search?: string
  industry?: string[]
  status?: string[]
  companySize?: string[]
  location?: string[]
  tags?: string[]
  leadScore?: [number, number]
}

class ProspectService {
  async getProspects(filters?: FilterOptions): Promise<Prospect[]> {
    const q: Record<string, string> = {}
    if (filters?.search) q.search = filters.search
    if (filters?.industry?.length) q.industry = filters.industry.join(',')
    if (filters?.status?.length) q.status = filters.status.join(',')
    if (filters?.companySize?.length) q.companySize = filters.companySize.join(',')
    if (filters?.location?.length) q.location = filters.location.join(',')
    if (filters?.tags?.length) q.tags = filters.tags.join(',')
    if (Array.isArray(filters?.leadScore) && filters!.leadScore!.length === 2) {
      q.leadScoreMin = String(filters!.leadScore![0])
      q.leadScoreMax = String(filters!.leadScore![1])
    }
    return http<Prospect[]>('/prospects', { query: q })
  }

  async getCampaigns(): Promise<Campaign[]> {
    return http<Campaign[]>('/campaigns')
  }

  async updateProspectStatus(prospectId: string, status: string): Promise<void> {
    await http<void>(`/prospects/${prospectId}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    })
  }
}

export const prospectService = new ProspectService()
export type { Prospect, Campaign} 