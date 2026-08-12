'use client'

import { useMemo, useState } from 'react'

const tools = [
  { name: 'Web Search', category: 'research', description: 'Search external sources for grounded mission context.', approval: false, uses: 234, success: 99, latency: '2.3s' },
  { name: 'Execute Code', category: 'development', description: 'Run bounded code in a sandboxed environment.', approval: true, uses: 89, success: 95, latency: '1.8s' },
  { name: 'Read File', category: 'filesystem', description: 'Read approved workspace files for analysis.', approval: false, uses: 456, success: 100, latency: '0.1s' },
  { name: 'Write File', category: 'filesystem', description: 'Write to an approved path with a recoverable backup.', approval: true, uses: 123, success: 100, latency: '0.2s' },
  { name: 'Send Email', category: 'communication', description: 'Send a message after recipient and scope approval.', approval: true, uses: 45, success: 98, latency: '2.5s' },
  { name: 'Data Analysis', category: 'analytics', description: 'Analyze structured data with bounded libraries.', approval: false, uses: 67, success: 97, latency: '3.2s' },
]

export default function ToolsPage() {
  const [category, setCategory] = useState('all'); const [selected, setSelected] = useState<typeof tools[number] | null>(null)
  const filtered = useMemo(() => category === 'all' ? tools : tools.filter((tool) => tool.category === category), [category])
  const categories = ['all', 'research', 'development', 'filesystem', 'communication', 'analytics']
  return <div className="page legacy-page">
    <div className="legacy-header"><div><p className="eyebrow">Capability registry</p><h1 className="page-title">Tools with boundaries.</h1><p className="page-subtitle">Understand what an agent can do, which actions require approval, and how reliably each capability performs.</p></div><span className="preview-badge">Preview data</span></div>
    <div className="run-overview tool-overview"><div><span>Available tools</span><strong>{tools.length}</strong></div><div><span>Approval gated</span><strong>{tools.filter((tool) => tool.approval).length}</strong></div><div><span>Average success</span><strong>98%</strong></div><div><span>Policy state</span><strong>Ready</strong></div></div>
    <div className="filter-row">{categories.map((item) => <button key={item} className={category === item ? 'filter-active' : ''} onClick={() => setCategory(item)}>{item}</button>)}<span className="filter-result">{filtered.length} tools</span></div>
    <section className="tool-grid">{filtered.map((tool) => <button className="tool-card" key={tool.name} onClick={() => setSelected(tool)}><div className="tool-card-head"><span className="tool-glyph">⌘</span><span className={`memory-type ${tool.category}`}>{tool.category}</span></div><h2>{tool.name}</h2><p>{tool.description}</p><div className="tool-stats"><div><strong>{tool.uses}</strong><span>uses</span></div><div><strong>{tool.success}%</strong><span>success</span></div><div><strong>{tool.latency}</strong><span>latency</span></div></div><div className="tool-card-foot"><span className={tool.approval ? 'approval-flag' : 'safe-flag'}>{tool.approval ? '◆ approval required' : '● bounded access'}</span><span>Inspect →</span></div></button>)}</section>
    {selected && <div className="detail-backdrop" role="presentation" onClick={() => setSelected(null)}><section className="detail-drawer" role="dialog" aria-modal="true" aria-label={selected.name} onClick={(event) => event.stopPropagation()}><button className="drawer-close" onClick={() => setSelected(null)} aria-label="Close">×</button><p className="eyebrow">Tool detail · Preview</p><span className="memory-type research">{selected.category}</span><h2>{selected.name}</h2><p className="drawer-lede">{selected.description}</p><div className="drawer-list"><div><span>Policy</span><strong>{selected.approval ? 'Approval required' : 'Bounded access'}</strong></div><div><span>Success rate</span><strong>{selected.success}%</strong></div><div><span>Average latency</span><strong>{selected.latency}</strong></div></div><button className="secondary-button" onClick={() => setSelected(null)}>Close preview</button></section></div>}
  </div>
}
