import React, { useEffect, useMemo, useState } from 'react'
import { api, roundHalfUpToFixed } from '../api/client'

interface Props {
  priceNow?: string | number
}

export default function Calculator({ priceNow }: Props) {
  const [perVolume, setPerVolume] = useState('1030')
  const [wasteLower, setWasteLower] = useState('0.15')
  const [wasteUpper, setWasteUpper] = useState('0.25')
  const [feeAmountToken, setFeeAmountToken] = useState('0')
  const [targetVolume, setTargetVolume] = useState('65536')

  const [auto, setAuto] = useState(true)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | undefined>()
  const [result, setResult] = useState<{ diff_lower: string; diff_upper: string } | undefined>()

  const disabled = useMemo(() => !priceNow || Number(priceNow) <= 0 || loading, [priceNow, loading])

  async function compute() {
    if (!priceNow) return
    setLoading(true); setError(undefined)
    try {
      const body = {
        price_now: String(priceNow),
        per_volume: perVolume,
        waste_lower: wasteLower,
        waste_upper: wasteUpper,
        fee_amount_token: feeAmountToken,
      }
      const res = await api.calc(body)
      setResult(res)
    } catch (e: any) {
      setError(e?.message || 'Compute failed')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (!auto) return
    compute()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [auto, priceNow, perVolume, wasteLower, wasteUpper, feeAmountToken])

  return (
    <div className="card pad">
      <div className="section-title">Calculator</div>
      <div className="grid cols-4">
        <div>
          <div className="label">Per Trade Volume (USDT)</div>
          <input className="input" value={perVolume} onChange={e => setPerVolume(e.target.value)} />
        </div>
        <div>
          <div className="label">Waste Lower (USDT)</div>
          <input className="input" value={wasteLower} onChange={e => setWasteLower(e.target.value)} />
        </div>
        <div>
          <div className="label">Waste Upper (USDT)</div>
          <input className="input" value={wasteUpper} onChange={e => setWasteUpper(e.target.value)} />
        </div>
        <div>
          <div className="label">Fee Amount (Token)</div>
          <input className="input" value={feeAmountToken} onChange={e => setFeeAmountToken(e.target.value)} />
        </div>
      </div>
      <div className="grid cols-4" style={{ marginTop: 12 }}>
        <div>
          <div className="label">Target Volume (USDT)</div>
          <input className="input" value={targetVolume} onChange={e => setTargetVolume(e.target.value)} />
        </div>
        <div>
          <div className="label">Realtime Calc</div>
          <div className={`switch ${auto ? 'on' : ''}`} onClick={() => setAuto(!auto)}>
            <div className="dot" />
          </div>
        </div>
        <div className="row" style={{ alignItems: 'flex-end' }}>
          <button className="btn primary" disabled={disabled} onClick={compute}>Calculate</button>
          {loading && <span className="help">Calculating...</span>}
          {error && <span className="help" style={{ color: 'var(--danger)' }}>{error}</span>}
        </div>
      </div>
      <div className="hr" />
      <div className="grid cols-2">
        <div>
          <div className="label">Diff Lower</div>
          <div className="kpi">{result ? roundHalfUpToFixed(result.diff_lower) : '—'}<span className="unit">USDT</span></div>
        </div>
        <div>
          <div className="label">Diff Upper</div>
          <div className="kpi">{result ? roundHalfUpToFixed(result.diff_upper) : '—'}<span className="unit">USDT</span></div>
        </div>
      </div>
    </div>
  )
}
