export const PROSPECT_STATUSES: Record<ProspectStatus, { label: string; color: string }> = {
  new: { label: 'New Leads', color: 'bg-gray-500' },
  contacted: { label: 'Contacted', color: 'bg-blue-500' },
  responded: { label: 'Responded', color: 'bg-yellow-500' },
  qualified: { label: 'Qualified', color: 'bg-purple-500' },
  converted: { label: 'Converted', color: 'bg-green-500' },
  rejected: { label: 'Rejected', color: 'bg-red-500' }
};

export const COMPANY_SIZES = [
  '1-10',
  '11-50',
  '51-200',
  '201-1000',
  '1001-5000',
  '5000+'
];

export const INDUSTRIES = [
  'Technology',
  'Healthcare',
  'Finance',
  'Manufacturing',
  'Retail',
  'Education',
  'Real Estate',
  'Marketing'
];

export const DASHBOARD_REFRESH_INTERVAL = 30000; // 30 seconds
export const MAX_PROSPECTS_PER_PAGE = 50;