'use client'

import { useMemo, useState } from 'react'

const runs = [
  { id: 'run_8f24', agent: 'Researcher', task: 'Synthesize customer interviews', status: 'running', duration: '02:14', progress: 68, tokens: '12.4k', cost: '$0.42' },
  { id: 'run_8f1d', agent: 'Planner', task: 'Prepare launch readiness plan', status: 'completed', duration: '04:08', progress: 100, tokens: '18.7k', cost: '$0.61' },
  { id: 'run_8e92', agent: 'Analyst', task: 'Compare competitor positioning', status: 'pending', duration: '—', progress: 0, tokens: '—', cost: '—' },
  { id: 'run_8d40', agent: 'Writer', task: 'Generate weekly operations brief', status: 'failed', duration: '01:32', progress: 32, tokens: '5.1k', cost: '$0.18' },
]

export default function RunsPage() {
  const [filter, setFilter] = useState('all'); const [selected, setSelected] = useState<typeof runs[number] | null>(null)
  const filtered = useMemo(() => filter === 'all' ? runs : runs.filter((run) => run.status === filter), [filter])
  return <div className="page legacy-page">
    <div className="legacy-header"><div><p className="eyebrow">Execution ledger</p><h1 className="page-title">See the work as it runs.</h1><p className="page-subtitle">Follow execution state, cost and evidence without losing the mission context.</p></div><span className="preview-badge">Preview data</span></div>
    <div className="run-overview"><div><span>Running now</span><strong>01</strong></div><div><span>Completed today</span><strong>12</strong></div><div><span>Success rate</span><strong>96.4%</strong></div><div><span>Tokens today</span><strong>84.2k</strong></div></div>
    <div className="filter-row run-filters">{['all', 'running', 'completed', 'pending', 'failed'].map((item) => <button key={item} className={filter === item ? 'filter-active' : ''} onClick={() => setFilter(item)}>{item}</button>)}<span className="filter-result">{filtered.length} runs</span></div>
    <section className="run-list">{filtered.map((run) => <button className="run-row" key={run.id} onClick={() => setSelected(run)}><span className={`run-status-icon ${run.status}`}>{run.status === 'running' ? '↻' : run.status === 'completed' ? '✓' : run.status === 'failed' ? '!' : '·'}</span><span className="run-copy"><strong>{run.task}</strong><small>{run.agent} · {run.id}</small>{run.status === 'running' && <span className="run-progress"><i style={{ width: `${run.progress}%` }}></i></span>}</span><span className={`run-state ${run.status}`}>{run.status}</span><span className="run-meta"><small>{run.duration}</small><small>{run.cost}</small></span><span className="motion-arrow">→</span></button>)}</section>
    {selected && <div className="detail-backdrop" role="presentation" onClick={() => setSelected(null)}><section className="detail-drawer" role="dialog" aria-modal="true" aria-label={selected.task} onClick={(event) => event.stopPropagation()}><button className="drawer-close" onClick={() => setSelected(null)} aria-label="Close">×</button><p className="eyebrow">Run detail · Preview</p><span className={`run-state ${selected.status}`}>{selected.status}</span><h2>{selected.task}</h2><p className="drawer-lede">Executed by {selected.agent} under run identifier {selected.id}.</p><div className="drawer-list"><div><span>Duration</span><strong>{selected.duration}</strong></div><div><span>Tokens used</span><strong>{selected.tokens}</strong></div><div><span>Estimated cost</span><strong>{selected.cost}</strong></div></div><p className="preview-note">This screen currently displays a representative execution ledger. Live run history will use the persisted API records.</p></section></div>}
  </div>
}
