// filepath: /Users/Nnamdi2/data_science_projects/B2B_sales_prospecting/prospect-ai-dashboard/src/components/Dashboard/Campaign/CampaignPerformance.tsx
import React from 'react'
import { useCampaigns } from '@/hooks/useCampaigns'
import { Card } from '@/components/UI/Card/Card'
import { LoadingSpinner } from '@/components/UI/LoadingSpinner/LoadingSpinner'
import { ErrorMessage } from '@/components/UI/ErrorMessage/ErrorMessage'
import { PerformanceChart, type ChartPoint } from '@/components/Charts/PerformanceChart'

function buildChartData(campaigns: any[]): ChartPoint[] {
  const hasSeries = campaigns.some(c => Array.isArray(c?.timeseries) && c.timeseries.length > 0)
  if (hasSeries) {
    const map = new Map<string, ChartPoint>()
    for (const c of campaigns) {
      for (const p of (c.timeseries || [])) {
        const date = typeof p.date === 'string' ? p.date : new Date(p.date).toISOString().slice(0, 10)
        const curr = map.get(date) || { date, sent: 0, opens: 0, clicks: 0, responses: 0 }
        curr.sent = (curr.sent || 0) + (p.sent ?? 0)
        curr.opens = (curr.opens || 0) + (p.opens ?? 0)
        curr.clicks = (curr.clicks || 0) + (p.clicks ?? 0)
        curr.responses = (curr.responses || 0) + (p.responses ?? 0)
        map.set(date, curr)
      }
    }
    return Array.from(map.values()).sort((a, b) => a.date.localeCompare(b.date))
  }
  const totals = campaigns.reduce(
    (acc, c) => ({
      sent: acc.sent + (c.sent ?? 0),
      opens: acc.opens + (c.opens ?? 0),
      clicks: acc.clicks + (c.clicks ?? 0),
      responses: acc.responses + (c.responses ?? 0),
    }),
    { sent: 0, opens: 0, clicks: 0, responses: 0 }
  )
  const today = new Date().toISOString().slice(0, 10)
  return [{ date: today, ...totals }]
}

const CampaignPerformance: React.FC = () => {
  const { data, loading, error } = useCampaigns()

  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <LoadingSpinner />
      </div>
    )
  }
  if (error) return <ErrorMessage message={error} />

  const campaigns = Array.isArray(data) ? data : []
  if (campaigns.length === 0) {
    return <Card><div className="p-4 text-sm text-gray-600">No campaign data available.</div></Card>
  }

  const chartData = buildChartData(campaigns)

  return (
    <Card>
      <div className="p-4 space-y-6">
        <div>
          <h3 className="text-base font-semibold mb-3">Campaign Performance</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {campaigns.map((c: any) => (
              <div key={c.id} className="rounded border border-gray-200 dark:border-gray-700 p-3 bg-white dark:bg-gray-800">
                <div className="flex items-start justify-between">
                  <div>
                    <div className="font-medium text-gray-900 dark:text-white">{c.name}</div>
                    <div className="text-xs text-gray-600 dark:text-gray-400">Channel: {c.channel || '—'}</div>
                  </div>
                  <span className="text-xs px-2 py-1 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                    {c.status || 'unknown'}
                  </span>
                </div>
                <div className="mt-2 text-sm">
                  <span>Sent: {c.sent ?? 0}</span>{' · '}
                  <span>Opens: {c.opens ?? 0}</span>{' · '}
                  <span>Clicks: {c.clicks ?? 0}</span>{' · '}
                  <span>Responses: {c.responses ?? 0}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div>
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-sm font-semibold text-gray-900 dark:text-white">Timeseries</h4>
            <span className="text-xs text-gray-500">Auto-aggregated</span>
          </div>
          <PerformanceChart data={chartData} />
        </div>
      </div>
    </Card>
  )
}

export default CampaignPerformance
export { CampaignPerformance }



// import React from 'react';
// import { useCampaigns } from '@/hooks/useCampaigns';
// import { Card } from '@/components/UI/Card/Card';
// import { LoadingSpinner } from '@/components/UI/LoadingSpinner/LoadingSpinner';
// import { ErrorMessage } from '@/components/UI/ErrorMessage/ErrorMessage';
// // import { formatDate } from '@/utils/utils';

// export const CampaignPerformance: React.FC = () => {
//   const { data, loading, error } = useCampaigns();

//   if (loading) {
//     return (
//       <div className="flex justify-center items-center p-8">
//         <LoadingSpinner />
//       </div>
//     );
//   }

//   if (error) {
//     return <ErrorMessage message={error} />;
//   }

//   return (
//     <Card>
//       <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
//         Campaign Performance
//       </h3>
//       <div className="space-y-4">
//         {campaigns.map((campaign) => (
//           <div key={campaign.id} className="p-4 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800">
//             <div className="flex justify-between items-start">
//               <div>
//                 <p className="font-semibold text-gray-800 dark:text-gray-200">{campaign.name}</p>
//                 <p className="text-sm text-gray-500 dark:text-gray-400">
//                   Started: {formatDate(campaign.startDate)}
//                 </p>
//               </div>
//               <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
//                 campaign.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-200 text-gray-800'
//               }`}>
//                 {campaign.status}
//               </span>
//             </div>
//             <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
//               <div>
//                 <p className="text-sm text-gray-500 dark:text-gray-400">Sent</p>
//                 <p className="text-xl font-bold text-gray-900 dark:text-white">{campaign.sent}</p>
//               </div>
//               <div>
//                 <p className="text-sm text-gray-500 dark:text-gray-400">Opened</p>
//                 <p className="text-xl font-bold text-gray-900 dark:text-white">{campaign.opened}</p>
//               </div>
//               <div>
//                 <p className="text-sm text-gray-500 dark:text-gray-400">Clicked</p>
//                 <p className="text-xl font-bold text-gray-900 dark:text-white">{campaign.clicked}</p>
//               </div>
//               <div>
//                 <p className="text-sm text-gray-500 dark:text-gray-400">Replies</p>
//                 <p className="text-xl font-bold text-gray-900 dark:text-white">{campaign.replies}</p>
//               </div>
//             </div>
//           </div>
//         ))}
//       </div>
//     </Card>
//   );
// };

// import React from 'react'
// import { useCampaigns } from '@/hooks/useCampaigns'
// import { Card } from '@/components/UI/Card/Card'
// import { LoadingSpinner } from '@/components/UI/LoadingSpinner/LoadingSpinner'
// import { ErrorMessage } from '@/components/UI/ErrorMessage/ErrorMessage'

// const CampaignPerformance: React.FC = () => {
//   const { data, loading, error } = useCampaigns()

//   if (loading) return <LoadingSpinner />
//   if (error) return <ErrorMessage message={error} />

//   const campaigns = Array.isArray(data) ? data : []
//   if (campaigns.length === 0) {
//     return <Card><div className="p-4 text-sm text-gray-600">No campaign data available.</div></Card>
//   }

//   return (
//     <Card>
//       <div className="p-4">
//         <h3 className="text-base font-semibold mb-3">Campaign Performance</h3>
//         <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
//           {campaigns.map((c) => (
//             <div key={c.id} className="rounded border p-3">
//               <div className="font-medium">{c.name}</div>
//               <div className="text-sm text-gray-600">Channel: {c.channel}</div>
//               <div className="mt-2 text-sm">
//                 <span>Sent: {c.sent}</span>{' · '}
//                 <span>Opens: {c.opens}</span>{' · '}
//                 <span>Clicks: {c.clicks}</span>{' · '}
//                 <span>Responses: {c.responses}</span>
//               </div>
//             </div>
//           ))}
//         </div>
//       </div>
//     </Card>
//   )
// }

// export default CampaignPerformance
// export { CampaignPerformance }

// // ...existing code...
// import React from 'react'
// import { useCampaigns } from '@/hooks/useCampaigns'
// import { Card } from '@/components/UI/Card/Card'
// import { LoadingSpinner } from '@/components/UI/LoadingSpinner/LoadingSpinner'
// import { ErrorMessage } from '@/components/UI/ErrorMessage/ErrorMessage'
// import { PerformanceChart, type ChartPoint } from '@/components/Charts/PerformanceChart'

// // Aggregate timeseries from campaigns returned by useCampaigns.
// // Supports either campaign.timeseries[] or falls back to a single aggregated point.
// function buildChartData(campaigns: any[]): ChartPoint[] {
//   // Prefer merging per-day timeseries if present
//   const hasSeries = campaigns.some(c => Array.isArray(c?.timeseries) && c.timeseries.length > 0)
//   if (hasSeries) {
//     const map = new Map<string, ChartPoint>()
//     for (const c of campaigns) {
//       for (const p of (c.timeseries || [])) {
//         const date = typeof p.date === 'string' ? p.date : new Date(p.date).toISOString().slice(0, 10)
//         const curr = map.get(date) || { date, sent: 0, opens: 0, clicks: 0, responses: 0 }
//         curr.sent = (curr.sent || 0) + (p.sent ?? 0)
//         curr.opens = (curr.opens || 0) + (p.opens ?? 0)
//         curr.clicks = (curr.clicks || 0) + (p.clicks ?? 0)
//         curr.responses = (curr.responses || 0) + (p.responses ?? 0)
//         map.set(date, curr)
//       }
//     }
//     return Array.from(map.values()).sort((a, b) => a.date.localeCompare(b.date))
//   }

//   // Fallback: one point with totals across campaigns (uses today)
//   const totals = campaigns.reduce(
//     (acc, c) => ({
//       sent: acc.sent + (c.sent ?? 0),
//       opens: acc.opens + (c.opens ?? 0),
//       clicks: acc.clicks + (c.clicks ?? 0),
//       responses: acc.responses + (c.responses ?? 0),
//     }),
//     { sent: 0, opens: 0, clicks: 0, responses: 0 }
//   )
//   const today = new Date().toISOString().slice(0, 10)
//   return [{ date: today, ...totals }]
// }

// const CampaignPerformance: React.FC = () => {
//   const { data, loading, error } = useCampaigns()

//   if (loading) {
//     return (
//       <div className="flex justify-center items-center p-8">
//         <LoadingSpinner />
//       </div>
//     )
//   }
//   if (error) return <ErrorMessage message={error} />

//   const campaigns = Array.isArray(data) ? data : []
//   if (campaigns.length === 0) {
//     return <Card><div className="p-4 text-sm text-gray-600">No campaign data available.</div></Card>
//   }

//   const chartData = buildChartData(campaigns)

//   return (
//     <Card>
//       <div className="p-4 space-y-6">
//         <div>
//           <h3 className="text-base font-semibold mb-3">Campaign Performance</h3>
//           <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
//             {campaigns.map((c: any) => (
//               <div key={c.id} className="rounded border border-gray-200 dark:border-gray-700 p-3 bg-white dark:bg-gray-800">
//                 <div className="flex items-start justify-between">
//                   <div>
//                     <div className="font-medium text-gray-900 dark:text-white">{c.name}</div>
//                     <div className="text-xs text-gray-600 dark:text-gray-400">Channel: {c.channel || '—'}</div>
//                   </div>
//                   <span className="text-xs px-2 py-1 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
//                     {c.status || 'unknown'}
//                   </span>
//                 </div>
//                 <div className="mt-2 text-sm">
//                   <span>Sent: {c.sent ?? 0}</span>{' · '}
//                   <span>Opens: {c.opens ?? 0}</span>{' · '}
//                   <span>Clicks: {c.clicks ?? 0}</span>{' · '}
//                   <span>Responses: {c.responses ?? 0}</span>
//                 </div>
//               </div>
//             ))}
//           </div>
//         </div>

//         <div>
//           <div className="flex items-center justify-between mb-3">
//             <h4 className="text-sm font-semibold text-gray-900 dark:text-white">Timeseries</h4>
//             <span className="text-xs text-gray-500">Auto-aggregated</span>
//           </div>
//           <PerformanceChart data={chartData} />
//         </div>
//       </div>
//     </Card>
//   )
// }

// export default CampaignPerformance
// export { CampaignPerformance }