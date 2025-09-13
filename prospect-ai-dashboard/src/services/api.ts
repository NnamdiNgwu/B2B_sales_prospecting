const API_BASE =
  (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_URL) ||
  (typeof window !== 'undefined' ? '/api' : '/api')

type Query = Record<string, string | number | boolean | undefined>
type HttpOptions = RequestInit & { query?: Query }

function toQuery(query?: Query) {
  if (!query) return ''
  const p = new URLSearchParams()
  Object.entries(query).forEach(([k, v]) => {
    if (v !== undefined && v !== null) p.set(k, String(v))
  })
  const s = p.toString()
  return s ? `?${s}` : ''
}

export async function http<T>(path: string, opts: HttpOptions = {}): Promise<T> {
  const { query, headers, ...rest } = opts
  const res = await fetch(`${API_BASE}${path}${toQuery(query)}`, {
    ...rest,
    headers: { 'content-type': 'application/json', ...(headers || {}) },
  })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`HTTP ${res.status} ${res.statusText}: ${text}`)
  }
  // Handle empty body
  const text = await res.text()
  return (text ? JSON.parse(text) : null) as T
}