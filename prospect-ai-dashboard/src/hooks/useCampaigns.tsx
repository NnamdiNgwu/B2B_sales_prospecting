import { useEffect, useState } from 'react'
import type { Campaign } from '@/types'
import { http } from '@/services/api'

export function useCampaigns() {
  const [data, setData] = useState<Campaign[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let active = true
    const load = async () => {
      try {
        setLoading(true)
        setError(null)
        const rows = await http<Campaign[]>('/campaigns')
        if (active) setData(rows || [])
      } catch (e: any) {
        if (active) setError(e?.message || 'Failed to load campaigns')
      } finally {
        if (active) setLoading(false)
      }
    }
    load()
    return () => {
      active = false
    }
  }, [])

  return { data, loading, error }
}