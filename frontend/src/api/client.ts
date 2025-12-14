export type PriceResponse = {
  symbol: string
  price_now: string | number
  price_avg: string | number
  price_vwap: string | number
  timestamp: number
}

export type TokenItem = { symbol: string; alphaId: string }

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'

async function http<T>(path: string, opts?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path}`
  const resp = await fetch(url, {
    ...opts,
    headers: { 'Content-Type': 'application/json', ...(opts?.headers || {}) }
  })
  if (!resp.ok) {
    const text = await resp.text().catch(() => '')
    throw new Error(text || `HTTP ${resp.status}`)
  }
  return resp.json() as Promise<T>
}

export const api = {
  async tokens(): Promise<TokenItem[]> {
    return http<TokenItem[]>(`/api/alpha/tokens`)
  },
  async price(alphaId: string): Promise<PriceResponse> {
    const q = encodeURIComponent(alphaId)
    return http<PriceResponse>(`/api/alpha/price?alphaId=${q}`)
  },
  async calc(body: {
    price_now: string | number
    per_volume: string | number
    waste_lower: string | number
    waste_upper: string | number
    fee_amount_token: string | number
  }): Promise<{ diff_lower: string; diff_upper: string }> {
    return http(`/api/calc/price-range`, { method: 'POST', body: JSON.stringify(body) })
  }
}

export function roundHalfUpToFixed(val: string | number, decimals = 8): string {
  // We only deal with non-negative values in this UI; JS toFixed is fine for HALF_UP equivalence
  const n = typeof val === 'string' ? Number(val) : val
  if (!Number.isFinite(n)) return '0.00000000'
  return n.toFixed(decimals)
}

export function formatTs(ts: number): string {
  const d = new Date(ts)
  return d.toLocaleString()
}
