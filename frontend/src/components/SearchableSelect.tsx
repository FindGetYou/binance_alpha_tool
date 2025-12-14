import React, { useEffect, useMemo, useRef, useState } from 'react'

export type Option = { value: string; label: string }

interface Props {
  options: Option[]
  value: string
  placeholder?: string
  disabled?: boolean
  onChange: (value: string) => void
  width?: number
}

export default function SearchableSelect({ options, value, placeholder = 'Select...', disabled, onChange, width = 260 }: Props) {
  const [open, setOpen] = useState(false)
  const [input, setInput] = useState('')
  const [active, setActive] = useState(0)
  const wrapRef = useRef<HTMLDivElement>(null)

  const map = useMemo(() => new Map(options.map(o => [o.value, o.label])), [options])
  const label = map.get(value)

  useEffect(() => {
    // sync input with external value when closed
    if (!open) {
      setInput(label ?? value ?? '')
    }
  }, [value, label, open])

  const filtered = useMemo(() => {
    const q = input.trim().toLowerCase()
    const list = q ? options.filter(o => o.label.toLowerCase().includes(q)) : options
    return list.slice(0, 200) // cap list to 200
  }, [options, input])

  useEffect(() => {
    function onDocClick(e: MouseEvent) {
      if (!wrapRef.current) return
      if (!wrapRef.current.contains(e.target as Node)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', onDocClick)
    return () => document.removeEventListener('mousedown', onDocClick)
  }, [])

  function pick(opt: Option) {
    onChange(opt.value)
    setOpen(false)
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (!open && (e.key === 'ArrowDown' || e.key === 'Enter')) {
      setOpen(true)
      e.preventDefault()
      return
    }
    if (!open) return
    if (e.key === 'ArrowDown') {
      setActive(i => Math.min(filtered.length - 1, i + 1))
      e.preventDefault()
    } else if (e.key === 'ArrowUp') {
      setActive(i => Math.max(0, i - 1))
      e.preventDefault()
    } else if (e.key === 'Enter') {
      const opt = filtered[active]
      if (opt) pick(opt)
      e.preventDefault()
    } else if (e.key === 'Escape') {
      setOpen(false)
    }
  }

  return (
    <div className="combo" ref={wrapRef} style={{ position: 'relative', width }}>
      <input
        className="input"
        placeholder={placeholder}
        disabled={disabled}
        value={open ? input : (label ?? value ?? '')}
        onChange={e => { setInput(e.target.value); setOpen(true); setActive(0) }}
        onFocus={() => setOpen(true)}
        onKeyDown={onKeyDown}
      />
      {open && (
        <div className="combo-menu card" style={{ position: 'absolute', top: 44, left: 0, right: 0, zIndex: 20, maxHeight: 280, overflow: 'auto', padding: 6 }}>
          {filtered.length === 0 ? (
            <div className="combo-item" style={{ padding: '8px 10px', color: 'var(--muted)' }}>No results</div>
          ) : (
            filtered.map((o, idx) => (
              <div
                key={o.value}
                className={`combo-item ${idx === active ? 'active' : ''}`}
                style={{ padding: '8px 10px', borderRadius: 6, cursor: 'pointer' }}
                onMouseEnter={() => setActive(idx)}
                onMouseDown={(e) => { e.preventDefault(); pick(o) }}
              >
                {o.label}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  )
}

