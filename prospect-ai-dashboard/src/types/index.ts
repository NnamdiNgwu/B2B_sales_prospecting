// THEME TYPES
export type Theme = 'light' | 'dark';

export interface ThemeContextType {
  theme: Theme;
  isDark: boolean;
  toggleTheme: () => void;
}

// PROSPECT & CAMPAIGN TYPES
// export interface Prospect {
//   id: string;
//   name: string;
//   company: string;
//   status: 'Lead' | 'Contacted' | 'Qualified' | 'Proposal' | 'Closed';
//   lastContactDate: string;
//   email: string;
//   potentialValue: number;
// }
export type Prospect = {
  id: string
  name: string
  company: string
  status: string
  industry?: string | null
  lastContactDate?: string | null
}

// export interface Campaign {
//   id: string;
//   name:string;
//   performance: number;
//   startDate: string;
//   endDate: string;
//   status: 'Active' | 'Paused' | 'Completed';
// }

export type Campaign = {
  id: string
  name: string
  channel: string
  sent: number
  opens: number
  clicks: number
  responses: number
}

// METRICS & FILTER TYPES
export interface DashboardMetrics {
  totalProspects: number;
  contactedLastWeek: number;
  conversionRate: number;
  pipelineValue: number;
}

export interface FilterOptions {
  searchTerm: string;
  status: string[];
  industries: string[];
  companySize: [number, number];
}

