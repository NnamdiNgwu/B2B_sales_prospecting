// export const PROSPECT_STATUSES: Record<ProspectStatus, { label: string; color: string }> = {
//   new: { label: 'New Leads', color: 'bg-gray-500' },
//   contacted: { label: 'Contacted', color: 'bg-blue-500' },
//   'In Conversation': { label: 'In Conversation', color: 'bg-yellow-100 text-yellow-800' },
//   'Demo Scheduled': { label: 'Demo Scheduled', color: 'bg-purple-100 text-purple-800' },
//   responded: { label: 'Responded', color: 'bg-yellow-500' },
//   qualified: { label: 'Qualified', color: 'bg-purple-500' },
//   converted: { label: 'Converted', color: 'bg-green-500' },
//   rejected: { label: 'Rejected', color: 'bg-red-500' }
// };

export const INDUSTRIES = [
  'Technology', 'Healthcare', 'Finance', 'Retail', 'Manufacturing', 'Education'
];

export const COMPANY_SIZES = [
  '1-10', '11-50', '51-200', '201-500', '501-1000', '1001+'
];

export const STAGES = ['Lead', 'Contacted', 'Qualified', 'Proposal', 'Closed'];

export const STAGE_COLORS: { [key: string]: string } = {
  Lead: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
  Contacted: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
  Qualified: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  Proposal: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
  Closed: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
};

// export const DASHBOARD_REFRESH_INTERVAL = 30000; // 30 seconds
// export const MAX_PROSPECTS_PER_PAGE = 50;