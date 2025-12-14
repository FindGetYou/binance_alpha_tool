import React, { useEffect, useRef, useState } from 'react'
import HeaderBar from './components/HeaderBar'
import PricePanel from './components/PricePanel'
import Calculator from './components/Calculator'
import { PriceResponse, api } from './api/client'

export default function App() {
  const [alphaId, setAlphaId] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | undefined>()
  const [price, setPrice] = useState<PriceResponse | undefined>()
  const [priceHistory, setPriceHistory] = useState<PriceResponse[]>([])

  const [polling, setPolling] = useState(false)
  const [freqSec, setFreqSec] = useState(5)
  const timer = useRef<number | undefined>(undefined)
  const VISIBLE_ROWS = 15 // fixed visible rows; change here if needed

  async function fetchPrice() {
    if (!alphaId) return
    setLoading(true); setError(undefined)
    try {
      const res = await api.price(alphaId)
      setPrice(res)
      setPriceHistory(prev => [res, ...prev].slice(0, VISIBLE_ROWS))
    } catch (e: any) {
      setError(e?.message || 'Fetch failed')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { // clear timer on unmount
    return () => { if (timer.current) window.clearInterval(timer.current) }
  }, [])

  useEffect(() => {
    if (!polling) {
      if (timer.current) window.clearInterval(timer.current)
      timer.current = undefined
      return
    }
    if (!alphaId) return
    fetchPrice()
    timer.current = window.setInterval(fetchPrice, freqSec * 1000) as any
    return () => { if (timer.current) window.clearInterval(timer.current) }
  }, [polling, freqSec, alphaId])

  function handleSelect(id: string) {
    setAlphaId(id)
    // reset history when switching token
    setPrice(undefined)
    setPriceHistory([])
    setTimeout(fetchPrice, 0)
  }

  return (
    <div className="container">
      <HeaderBar
        selected={alphaId}
        onSelect={handleSelect}
        onQuery={() => { fetchPrice() }}
        polling={polling}
        onTogglePolling={setPolling}
        freqSec={freqSec}
        onChangeFreq={setFreqSec}
      />
      <div className="column-stack">
        <Calculator priceNow={price?.price_now} />
        <PricePanel
          data={price}
          list={priceHistory}
          loading={loading}
          error={error}
          onClear={() => setPriceHistory([])}
          historySize={VISIBLE_ROWS}
        />
      </div>
      <div className="footer">Binance Alpha Tool • Built with FastAPI + React</div>
    </div>
  )
}
