// import React from 'react'
// import { Routes, Route, Navigate } from 'react-router-dom'
// import { Layout } from '@/components/UI/Layout/Base'
// import { ThemeProvider } from '@/contexts/ThemeContext'
// import { Dashboard } from '@/components/Dashboard/Dashboard'
// import CampaignPerformance from '@/components/Dashboard/Campaign/CampaignPerformance'

// const Analytics: React.FC = () => (
//   <div className="p-4 text-sm text-gray-600">Analytics coming soon.</div>
// )
// const Settings: React.FC = () => (
//   <div className="p-4 text-sm text-gray-600">Settings coming soon.</div>
// )

// export default function App() {
//   return (
//     <ThemeProvider>
//       <Layout title="Prospect AI Dashboard">
//         <Routes>
//           <Route path="/" element={<Navigate to="/dashboard" replace />} />
//           <Route path="/dashboard" element={<Dashboard />} />
//           <Route path="/campaigns" element={<CampaignPerformance />} />
//           <Route path="/analytics" element={<Analytics />} />
//           <Route path="/settings" element={<Settings />} />
//           <Route path="*" element={<Navigate to="/dashboard" replace />} />
//         </Routes>
//       </Layout>
//     </ThemeProvider>
//   )
// }


import React, { useEffect, useState } from 'react'
import { Card } from '@/components/UI/Card/Card'
import { Button } from '@/components/UI/Button/Button'
import { ErrorMessage } from '@/components/UI/ErrorMessage/ErrorMessage'
import { http } from '@/services/api'

type OrgSettings = {
  from_name: string
  from_email: string
  company_name: string
  website?: string
  brand_voice?: string
}

const SettingsPage: React.FC = () => {
  const [org, setOrg] = useState<OrgSettings>({ from_name: '', from_email: '', company_name: '' })
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    let active = true
    const load = async () => {
      try {
        setError(null); setLoading(true)
        const data = await http<any>('/settings/org').catch(() => ({}))
        if (active && data && Object.keys(data).length) setOrg(data as OrgSettings)
      } catch (e: any) {
        if (active) setError(e?.message || 'Failed to load settings')
      } finally {
        if (active) setLoading(false)
      }
    }
    load()
    return () => { active = false }
  }, [])

  const save = async () => {
    try {
      setSaved(false); setError(null); setSaving(true)
      await http('/settings/org', { method: 'POST', body: JSON.stringify(org) })
      setSaved(true)
    } catch (e: any) {
      setError(e?.message || 'Save failed')
    } finally {
      setSaving(false)
    }
  }

  return (
    <Card>
      <div className="p-4 space-y-4">
        <h2 className="text-lg font-semibold">Settings</h2>
        <p className="text-sm text-gray-600">
          Configure organization details, campaign defaults, and integrations.
        </p>

        {error && <ErrorMessage message={error} />}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <input className="input" placeholder="From name" value={org.from_name}
                 onChange={e => setOrg({ ...org, from_name: e.target.value })} />
          <input className="input" placeholder="From email" value={org.from_email}
                 onChange={e => setOrg({ ...org, from_email: e.target.value })} />
          <input className="input" placeholder="Company name" value={org.company_name}
                 onChange={e => setOrg({ ...org, company_name: e.target.value })} />
          <input className="input" placeholder="Website" value={org.website || ''}
                 onChange={e => setOrg({ ...org, website: e.target.value })} />
        </div>

        <textarea className="w-full rounded border p-2" rows={3} placeholder="Brand voice"
                  value={org.brand_voice || ''} onChange={e => setOrg({ ...org, brand_voice: e.target.value })} />

        <div className="flex items-center gap-3">
          <Button onClick={save} disabled={loading || saving}>{saving ? 'Saving…' : 'Save'}</Button>
          {saved && <span className="text-sm text-green-600">Saved</span>}
        </div>
      </div>
    </Card>
  )
}

export default SettingsPage