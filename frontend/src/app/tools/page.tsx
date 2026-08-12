'use client'

import { useMemo, useState } from 'react'
import { useTools } from '@/lib/hooks'

type Tool = { id: string; name: string; description: string; category: string; requires_approval: boolean }

export default function ToolsPage() {
  const { tools, loading, error } = useTools()
  const [category, setCategory] = useState('all')
  const [selected, setSelected] = useState<Tool | null>(null)
  const categories = ['all', ...Array.from(new Set(tools.map((tool) => tool.category)))]
  const filtered = useMemo(() => category === 'all' ? tools : tools.filter((tool) => tool.category === category), [category, tools])
  const approvalGated = tools.filter((tool) => tool.requires_approval).length

  return <div className="page legacy-page">
    <div className="legacy-header"><div><p className="eyebrow">Capability registry</p><h1 className="page-title">Tools with boundaries.</h1><p className="page-subtitle">Understand what an agent can do and which actions require approval.</p></div><span className="live-badge"><i></i>Persisted registry</span></div>
    <div className="run-overview tool-overview"><div><span>Available tools</span><strong>{tools.length}</strong></div><div><span>Approval gated</span><strong>{approvalGated}</strong></div><div><span>Categories</span><strong>{new Set(tools.map((tool) => tool.category)).size}</strong></div><div><span>Policy state</span><strong>{loading ? '…' : 'Ready'}</strong></div></div>
    <div className="filter-row">{categories.map((item) => <button key={item} className={category === item ? 'filter-active' : ''} onClick={() => setCategory(item)}>{item}</button>)}<span className="filter-result">{filtered.length} tools</span></div>
    {error && <p className="form-error" role="alert">Tools unavailable: {error}</p>}
    {loading && <div className="empty-message">Loading persisted tool registry…</div>}
    {!loading && !error && !filtered.length && <div className="empty-message">No tool matches this category.</div>}
    <section className="tool-grid">{filtered.map((tool: Tool) => <button className="tool-card" key={tool.id} onClick={() => setSelected(tool)}><div className="tool-card-head"><span className="tool-glyph">⌘</span><span className="memory-type research">{tool.category}</span></div><h2>{tool.name}</h2><p>{tool.description}</p><div className="tool-card-foot"><span className={tool.requires_approval ? 'approval-flag' : 'safe-flag'}>{tool.requires_approval ? '◆ approval required' : '● bounded access'}</span><span>Inspect →</span></div></button>)}</section>
    {selected && <div className="detail-backdrop" role="presentation" onClick={() => setSelected(null)}><section className="detail-drawer" role="dialog" aria-modal="true" aria-label={selected.name} onClick={(event) => event.stopPropagation()}><button className="drawer-close" onClick={() => setSelected(null)} aria-label="Close">×</button><p className="eyebrow">Tool detail · Persisted registry</p><span className="memory-type research">{selected.category}</span><h2>{selected.name}</h2><p className="drawer-lede">{selected.description}</p><div className="drawer-list"><div><span>Tool ID</span><strong>{selected.id}</strong></div><div><span>Policy</span><strong>{selected.requires_approval ? 'Approval required' : 'Bounded access'}</strong></div></div></section></div>}
  </div>
}
