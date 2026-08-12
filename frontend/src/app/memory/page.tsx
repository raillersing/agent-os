'use client'

import { useMemo, useState } from 'react'
import { Memory, useMemory } from '@/lib/hooks'

export default function MemoryPage() {
  const [query, setQuery] = useState('')
  const [type, setType] = useState('all')
  const [selected, setSelected] = useState<Memory | null>(null)
  const { memories, loading, error, search } = useMemory(query)
  const types = ['all', ...Array.from(new Set(memories.map((item) => item.type)))]
  const filtered = useMemo(() => type === 'all' ? memories : memories.filter((item) => item.type === type), [memories, type])
  const accesses = memories.reduce((sum, item) => sum + item.access_count, 0)

  return <div className="page legacy-page">
    <div className="legacy-header"><div><p className="eyebrow">Knowledge layer</p><h1 className="page-title">Memory with provenance.</h1><p className="page-subtitle">Inspect what agents know, where it came from, and when it was last used.</p></div><span className="live-badge"><i></i>Persisted API</span></div>
    <div className="memory-command"><span className="search-glyph">⌕</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search keys, content or sources…" aria-label="Search memory" /><kbd>⌘ K</kbd></div>
    <div className="filter-row">{types.map((item) => <button key={item} className={type === item ? 'filter-active' : ''} onClick={() => setType(item)}>{item}</button>)}<span className="filter-result">{filtered.length} entries</span></div>
    <div className="memory-summary"><div><span>Total entries</span><strong>{memories.length}</strong></div><div><span>Accesses recorded</span><strong>{accesses}</strong></div><div><span>Types</span><strong>{new Set(memories.map((item) => item.type)).size}</strong></div><div><span>Data source</span><strong>API</strong></div></div>
    {error && <p className="form-error" role="alert">Memory unavailable: {error}</p>}
    {loading && <div className="empty-message">Loading persisted memory…</div>}
    {!loading && !error && !filtered.length && <div className="empty-message">No memory entry matches this search.</div>}
    <section className="memory-grid">{filtered.map((item) => <button className="memory-card" key={item.key} onClick={() => setSelected(item)}><div className="memory-card-head"><span className={`memory-type ${item.type}`}>{item.type}</span><span>{item.access_count} accesses</span></div><h2>{item.key}</h2><p>{item.content}</p><div className="memory-card-foot"><span>{item.source || 'Unknown source'}</span><span>{item.last_accessed_at ? new Date(item.last_accessed_at).toLocaleString() : 'Not accessed'}</span></div></button>)}</section>
    {selected && <div className="detail-backdrop" role="presentation" onClick={() => setSelected(null)}><section className="detail-drawer" role="dialog" aria-modal="true" aria-label={selected.key} onClick={(event) => event.stopPropagation()}><button className="drawer-close" onClick={() => setSelected(null)} aria-label="Close">×</button><span className={`memory-type ${selected.type}`}>{selected.type}</span><h2>{selected.key}</h2><p className="drawer-lede">{selected.content}</p><div className="drawer-list"><div><span>Source</span><strong>{selected.source || 'Unknown'}</strong></div><div><span>Last accessed</span><strong>{selected.last_accessed_at ? new Date(selected.last_accessed_at).toLocaleString() : 'Not accessed'}</strong></div><div><span>Access count</span><strong>{selected.access_count}</strong></div></div><button className="secondary-button" onClick={() => { setSelected(null); search(query) }}>Refresh record</button></section></div>}
  </div>
}
