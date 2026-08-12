'use client'

import { useMemo, useState } from 'react'

const memories = [
  { key: 'project-context', type: 'knowledge', source: 'documentation', content: 'Agent OS is a provider-neutral control plane for AI agents. MVP focuses on durable workflows.', accessed: '2 min ago', count: 45 },
  { key: 'seo-keywords', type: 'data', source: 'keyword-researcher', content: 'Target keywords: agent os, ai agent orchestration, agent control plane, workflow automation.', accessed: '15 min ago', count: 12 },
  { key: 'competitor-analysis', type: 'analysis', source: 'seo-analyzer', content: 'Key differentiator: vendor-neutral architecture with approvals and provenance.', accessed: '30 min ago', count: 8 },
  { key: 'client-context-acme', type: 'client', source: 'manual', content: 'Acme Corp: SaaS company, target AI startups, goal to increase organic traffic.', accessed: '1 hour ago', count: 23 },
  { key: 'blog-outline-ai-agents', type: 'content', source: 'content-writer', content: 'Outline: orchestration, control planes, components, implementation patterns, best practices.', accessed: '45 min ago', count: 5 },
  { key: 'outreach-templates', type: 'template', source: 'outreach-bot', content: 'Partnership, follow-up and re-engagement templates.', accessed: '2 hours ago', count: 34 },
]

export default function MemoryPage() {
  const [query, setQuery] = useState(''); const [type, setType] = useState('all'); const [selected, setSelected] = useState<typeof memories[number] | null>(null)
  const filtered = useMemo(() => memories.filter((item) => (type === 'all' || item.type === type) && `${item.key} ${item.content}`.toLowerCase().includes(query.toLowerCase())), [query, type])
  const types = ['all', 'knowledge', 'data', 'analysis', 'client', 'content', 'template']
  return <div className="page legacy-page">
    <div className="legacy-header"><div><p className="eyebrow">Knowledge layer</p><h1 className="page-title">Memory with provenance.</h1><p className="page-subtitle">Inspect what agents know, where it came from, and when it was last used.</p></div><span className="preview-badge">Preview data</span></div>
    <div className="memory-command"><span className="search-glyph">⌕</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search keys, content or sources…" aria-label="Search memory" /><kbd>⌘ K</kbd></div>
    <div className="filter-row">{types.map((item) => <button key={item} className={type === item ? 'filter-active' : ''} onClick={() => setType(item)}>{item}</button>)}<span className="filter-result">{filtered.length} entries</span></div>
    <div className="memory-summary"><div><span>Total entries</span><strong>{memories.length}</strong></div><div><span>Accesses recorded</span><strong>{memories.reduce((sum, item) => sum + item.count, 0)}</strong></div><div><span>Types</span><strong>{new Set(memories.map((item) => item.type)).size}</strong></div><div><span>Data source</span><strong>Preview</strong></div></div>
    <section className="memory-grid">{filtered.map((item) => <button className="memory-card" key={item.key} onClick={() => setSelected(item)}><div className="memory-card-head"><span className={`memory-type ${item.type}`}>{item.type}</span><span>{item.count} accesses</span></div><h2>{item.key}</h2><p>{item.content}</p><div className="memory-card-foot"><span>{item.source}</span><span>{item.accessed}</span></div></button>)}</section>
    {!filtered.length && <div className="empty-message">No memory entry matches this search.</div>}
    {selected && <div className="detail-backdrop" role="presentation" onClick={() => setSelected(null)}><section className="detail-drawer" role="dialog" aria-modal="true" aria-label={selected.key} onClick={(event) => event.stopPropagation()}><button className="drawer-close" onClick={() => setSelected(null)} aria-label="Close">×</button><span className={`memory-type ${selected.type}`}>{selected.type}</span><h2>{selected.key}</h2><p className="drawer-lede">{selected.content}</p><div className="drawer-list"><div><span>Source</span><strong>{selected.source}</strong></div><div><span>Last accessed</span><strong>{selected.accessed}</strong></div><div><span>Access count</span><strong>{selected.count}</strong></div></div><p className="preview-note">This surface currently uses preview data. API-backed memory management is a separate implementation step.</p></section></div>}
  </div>
}
