'use client'

import { useMemo, useState } from 'react'
import { Run, useRuns } from '@/lib/hooks'

function duration(run: Run) {
  if (!run.duration_ms) return '—'
  return `${Math.floor(run.duration_ms / 60000).toString().padStart(2, '0')}:${Math.floor((run.duration_ms % 60000) / 1000).toString().padStart(2, '0')}`
}

export default function RunsPage() {
  const { runs, loading, error, refetch } = useRuns()
  const [filter, setFilter] = useState('all')
  const [selected, setSelected] = useState<Run | null>(null)
  const filtered = useMemo(() => filter === 'all' ? runs : runs.filter((run) => run.status === filter), [filter, runs])
  const completed = runs.filter((run) => run.status === 'completed').length
  const running = runs.filter((run) => run.status === 'running').length

  return <div className="page legacy-page">
    <div className="legacy-header"><div><p className="eyebrow">Execution ledger</p><h1 className="page-title">See the work as it runs.</h1><p className="page-subtitle">Follow execution state, cost and evidence without losing the mission context.</p></div><span className="live-badge"><i></i>Persisted API</span></div>
    <div className="run-overview"><div><span>Running now</span><strong>{running}</strong></div><div><span>Completed records</span><strong>{completed}</strong></div><div><span>Total runs</span><strong>{runs.length}</strong></div><div><span>Tokens recorded</span><strong>{runs.reduce((sum, run) => sum + (run.tokens_used || 0), 0).toLocaleString()}</strong></div></div>
    <div className="filter-row run-filters">{['all', 'running', 'completed', 'pending', 'failed', 'cancelled'].map((item) => <button key={item} className={filter === item ? 'filter-active' : ''} onClick={() => setFilter(item)}>{item}</button>)}<span className="filter-result">{filtered.length} runs · <button className="inline-action" onClick={refetch}>Refresh</button></span></div>
    {error && <p className="form-error" role="alert">Runs unavailable: {error}</p>}
    {loading && <div className="empty-message">Loading persisted runs…</div>}
    {!loading && !error && !filtered.length && <div className="empty-message">No persisted run matches this filter.</div>}
    <section className="run-list">{filtered.map((run) => <button className="run-row" key={run.id} onClick={() => setSelected(run)}><span className={`run-status-icon ${run.status}`}>{run.status === 'running' ? '↻' : run.status === 'completed' ? '✓' : run.status === 'failed' ? '!' : '·'}</span><span className="run-copy"><strong>{run.prompt}</strong><small>{run.agent_id} · {run.id}</small>{run.status === 'running' && <span className="run-progress"><i style={{ width: `${run.progress}%` }}></i></span>}</span><span className={`run-state ${run.status}`}>{run.status}</span><span className="run-meta"><small>{duration(run)}</small><small>{run.cost ? `$${run.cost.toFixed(2)}` : '—'}</small></span><span className="motion-arrow">→</span></button>)}</section>
    {selected && <div className="detail-backdrop" role="presentation" onClick={() => setSelected(null)}><section className="detail-drawer" role="dialog" aria-modal="true" aria-label={selected.prompt} onClick={(event) => event.stopPropagation()}><button className="drawer-close" onClick={() => setSelected(null)} aria-label="Close">×</button><p className="eyebrow">Run detail · Persisted record</p><span className={`run-state ${selected.status}`}>{selected.status}</span><h2>{selected.prompt}</h2><p className="drawer-lede">Run identifier {selected.id}, owned by agent {selected.agent_id}.</p><div className="drawer-list"><div><span>Progress</span><strong>{selected.progress}%</strong></div><div><span>Tokens used</span><strong>{selected.tokens_used.toLocaleString()}</strong></div><div><span>Estimated cost</span><strong>${selected.cost.toFixed(2)}</strong></div></div>{selected.error && <p className="form-error">{selected.error}</p>}</section></div>}
  </div>
}
