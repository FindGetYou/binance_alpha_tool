import React, { useEffect, useMemo, useState } from 'react'
import { api, TokenItem } from '../api/client'
import SearchableSelect from './SearchableSelect'

interface Props {
  onSelect: (alphaId: string) => void
  onQuery?: () => void
  selected: string
  polling: boolean
  onTogglePolling: (v: boolean) => void
  freqSec: number
  onChangeFreq: (n: number) => void
}

export default function HeaderBar({ onSelect, onQuery, selected, polling, onTogglePolling, freqSec, onChangeFreq }: Props) {
  const [tokens, setTokens] = useState<TokenItem[]>([])
  const [loading, setLoading] = useState(false)
  const [custom, setCustom] = useState('')
  const [useCustom, setUseCustom] = useState(false)

  useEffect(() => {
    let mounted = true
    setLoading(true)
    api.tokens().then((list) => {
      if (!mounted) return
      setTokens(list)
    }).catch(() => {}).finally(() => setLoading(false))
    return () => { mounted = false }
  }, [])

  useEffect(() => {
    if (useCustom && custom) onSelect(custom)
  }, [useCustom, custom])

  const options = useMemo(() => tokens.map(t => ({ value: t.alphaId, label: `${t.symbol} (${t.alphaId})` })), [tokens])

  return (
    <div className="card headerbar">
      <div className="header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
          <div>
            <div className="label">Token</div>
            <div className="row">
              <SearchableSelect
                options={options}
                value={selected}
                disabled={loading || useCustom}
                onChange={(v) => onSelect(v)}
                width={260}
              />
              <button className={`btn ${useCustom ? 'on' : ''}`} onClick={() => setUseCustom(v => !v)}>{useCustom ? 'Custom On' : 'Custom Off'}</button>
              <input className="input" style={{ width: 240 }} placeholder="e.g. KOGE or BTCUSDT or ALPHA_118" disabled={!useCustom} value={custom} onChange={e => setCustom(e.target.value.trim())} />
              <button className="btn primary" onClick={() => onQuery ? onQuery() : onSelect(useCustom ? custom : selected)} disabled={!(useCustom ? custom : selected)}>Query</button>
            </div>
            <div className="help">You can pick from list or type base/symbol (e.g. KOGE / BTCUSDT / ALPHA_118)</div>
          </div>
        </div>
        <div className="stack">
          <div>
            <div className="label">Realtime Update</div>
            <div className={`switch ${polling ? 'on' : ''}`} onClick={() => onTogglePolling(!polling)}>
              <div className="dot" />
            </div>
          </div>
          <div>
            <div className="label">Refresh (sec)</div>
            <input className="input" style={{ width: 100 }} type="number" min={1} max={60} value={freqSec} onChange={e => onChangeFreq(Math.max(1, Math.min(60, Number(e.target.value) || 1)))} />
          </div>
        </div>
      </div>
    </div>
  )
}
