import { useEffect, useState } from 'react'
import type { Prospect } from '@/types'
import { prospectService, type FilterOptions } from '@/services/ProspectService'

const initialFilters: FilterOptions = {
  search: '',
  industry: [],
  companySize: [],
  leadScore: [0, 100],
  status: [],
  location: [],
  tags: [],
}

export const useProspects = () => {
  const [prospects, setProspects] = useState<Prospect[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filters, setFilters] = useState<FilterOptions>(initialFilters)

  useEffect(() => {
    let active = true
    const load = async () => {
      try {
        setLoading(true)
        setError(null)
        const data = await prospectService.getProspects(filters)
        if (active) setProspects(data || [])
      } catch (e: any) {
        if (active) setError(e?.message || 'Failed to load prospects')
      } finally {
        if (active) setLoading(false)
      }
    }
    load()
    return () => {
      active = false
    }
  }, [
    filters.search,
    filters.leadScore?.[0],
    filters.leadScore?.[1],
    JSON.stringify(filters.industry),
    JSON.stringify(filters.status),
    JSON.stringify(filters.companySize),
    JSON.stringify(filters.location),
    JSON.stringify(filters.tags),
  ])

  const updateFilters = (next: Partial<FilterOptions>) =>
    setFilters((prev) => ({ ...prev, ...next }))

  return { prospects, loading, error, filters, updateFilters }
}