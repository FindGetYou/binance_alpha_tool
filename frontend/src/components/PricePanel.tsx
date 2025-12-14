import React from 'react'
import { PriceResponse, formatTs, roundHalfUpToFixed } from '../api/client'

interface Props {
  data?: PriceResponse
  list?: PriceResponse[]
  loading: boolean
  error?: string
  onClear?: () => void
  historySize?: number
}

export default function PricePanel({ data, list = [], loading, error, onClear, historySize = 15 }: Props) {
  const rows = list.slice(0, historySize)
  const needPlaceholders = Math.max(0, historySize - rows.length)
  const rowH = 44 // px
  const height = rowH * historySize
  return (
    <div className="card pad">
      <div className="row" style={{ justifyContent: 'space-between', alignItems: 'center' }}>
        <div className="section-title">Realtime Price</div>
        <div className="row">
          {error && <span className="help" style={{ color: 'var(--danger)', marginRight: 8 }}>{error}</span>}
          {onClear && <button className="btn" onClick={onClear}>Clear</button>}
        </div>
      </div>
      <div className="help" style={{ margin: '4px 0 8px 2px' }}>Symbol: {rows[0]?.symbol || data?.symbol || '—'}</div>
      <div className="price-table">
        <div className="price-header">
          <div className="cell time">Time</div>
          <div className="cell num col-last">Last</div>
          <div className="cell num col-avg">Average</div>
          <div className="cell num col-vwap">VWAP</div>
        </div>
        <div className="price-scroll" style={{ maxHeight: height, height }}>
          {rows.map((it, idx) => {
            const prev = idx + 1 < rows.length ? rows[idx + 1] : undefined
            let trend = ''
            if (prev) {
              const now = Number(it.price_now)
              const last = Number(prev.price_now)
              if (Number.isFinite(now) && Number.isFinite(last)) {
                if (now > last) trend = 'up'
                else if (now < last) trend = 'down'
              }
            }
            return (
              <div key={idx} className="price-row">
                <div className="cell time">{formatTs(it.timestamp)}</div>
                <div className={`cell num col-last ${trend}`}>{roundHalfUpToFixed(it.price_now)}</div>
                <div className="cell num col-avg">{roundHalfUpToFixed(it.price_avg)}</div>
                <div className="cell num col-vwap">{roundHalfUpToFixed(it.price_vwap)}</div>
              </div>
            )
          })}
          {Array.from({ length: needPlaceholders }).map((_, i) => (
            <div key={`ph-${i}`} className="price-row placeholder">
              <div className="cell time">—</div>
              <div className="cell num col-last">—</div>
              <div className="cell num col-avg">—</div>
              <div className="cell num col-vwap">—</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
