'use client'

import { useMemo, useState } from 'react'

const artifacts = [
  { name: 'AI agent infographic', type: 'image', agent: 'OpenClaw', date: '2 min ago', mark: '◈', tone: 'gold' },
  { name: 'Product demo video', type: 'video', agent: 'OpenClaw', date: '15 min ago', mark: '▶', tone: 'blue' },
  { name: 'Podcast episode 12', type: 'voice', agent: 'Hermes', date: '1 hour ago', mark: '◉', tone: 'green' },
  { name: 'Social media banner', type: 'image', agent: 'OpenClaw', date: '2 hours ago', mark: '▧', tone: 'violet' },
  { name: 'Tutorial walkthrough', type: 'video', agent: 'OpenClaw', date: '3 hours ago', mark: '▷', tone: 'amber' },
  { name: 'Voice note — ideas', type: 'voice', agent: 'Hermes', date: '5 hours ago', mark: '◌', tone: 'rose' },
]

export default function StudioPage() {
  const [category, setCategory] = useState('all'); const filtered = useMemo(() => category === 'all' ? artifacts : artifacts.filter((item) => item.type === category), [category])
  return <div className="page legacy-page">
    <div className="legacy-header"><div><p className="eyebrow">Artifact workspace</p><h1 className="page-title">A studio for finished work.</h1><p className="page-subtitle">Collect the outputs that matter, inspect their provenance, and keep delivery separate from execution.</p></div><span className="preview-badge">Preview data</span></div>
    <section className="studio-hero"><div><p className="eyebrow">Create an artifact</p><h2>Turn a run into something ready to share.</h2><p>Generation actions are not connected yet. This prototype shows the intended artifact library and delivery flow.</p></div><button className="primary-button" onClick={() => setCategory('all')}>＋ Explore library</button></section>
    <div className="filter-row">{['all', 'image', 'video', 'voice'].map((item) => <button key={item} className={category === item ? 'filter-active' : ''} onClick={() => setCategory(item)}>{item}</button>)}<span className="filter-result">{filtered.length} artifacts</span></div>
    <section className="artifact-grid">{filtered.map((item) => <article className="artifact-card" key={item.name}><div className={`artifact-preview ${item.tone}`}><span>{item.mark}</span><small>{item.type}</small></div><div className="artifact-copy"><div><h2>{item.name}</h2><p>by {item.agent}</p></div><span className="artifact-arrow">↗</span></div><div className="artifact-foot"><span>Generated artifact</span><span>{item.date}</span></div></article>)}</section>
  </div>
}
