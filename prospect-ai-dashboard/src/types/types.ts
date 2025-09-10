export interface Prospect {
  id: string;
  name: string;
  company: string;
  title: string;
  email: string;
  phone?: string;
  location: string;
  industry: string;
  companySize: string;
  leadScore: number;
  status: ProspectStatus;
  lastActivity: string;
  profileUrl: string;
  connectionLevel: string;
  mutualConnections: number;
  tags: string[];
  createdAt: string;
  updatedAt: string;
}

export type ProspectStatus = 'new' | 'contacted' | 'responded' | 'qualified' | 'converted' | 'rejected';

export interface Campaign {
  id: string;
  name: string;
  status: CampaignStatus;
  totalProspects: number;
  contacted: number;
  responded: number;
  converted: number;
  responseRate: number;
  conversionRate: number;
  createdAt: string;
}

export type CampaignStatus = 'active' | 'paused' | 'completed';

export interface FilterOptions {
  search: string;
  industry: string[];
  companySize: string[];
  leadScore: [number, number];
  status: ProspectStatus[];
  location: string[];
  tags: string[];
}

export interface DashboardMetrics {
  total: number;
  contacted: number;
  responded: number;
  converted: number;
  responseRate: number;
  conversionRate: number;
}

export interface ThemeContextType {
  isDark: boolean;
  toggleTheme: () => void;
}