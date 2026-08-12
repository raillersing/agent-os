'use client'

import { useState } from 'react'

const goals = [
  { name: 'SEO campaign Q1', description: 'Rank for 50 target keywords in the AI agent space.', progress: 78, tasks: '18 / 24', deadline: '31 Mar 2026', owner: 'Hermes', tone: 'gold' },
  { name: 'Content pipeline', description: 'Produce a reliable, reviewable publishing workflow.', progress: 92, tasks: '92 / 100', deadline: '30 Jun 2026', owner: 'OpenClaw', tone: 'green' },
  { name: 'Lead generation', description: 'Generate qualified leads with traceable provenance.', progress: 45, tasks: '22 / 50', deadline: '30 Sep 2026', owner: 'Hermes', tone: 'blue' },
  { name: 'Video content', description: 'Create a reusable library of product education assets.', progress: 30, tasks: '15 / 50', deadline: '31 Dec 2026', owner: 'OpenClaw', tone: 'violet' },
]

export default function GoalsPage() {
  const [selected, setSelected] = useState<typeof goals[number] | null>(null)
  return <div className="page legacy-page">
    <div className="legacy-header"><div><p className="eyebrow">Direction</p><h1 className="page-title">Goals with a clear horizon.</h1><p className="page-subtitle">Keep long-term outcomes visible without losing the next concrete step.</p></div><span className="preview-badge">Preview data</span></div>
    <div className="legacy-toolbar"><div className="toolbar-copy"><span className="eyebrow">Portfolio view</span><strong>{goals.length} active outcomes</strong></div><button className="primary-button" onClick={() => setSelected(goals[0])}>＋ Inspect a goal</button></div>
    <section className="goal-grid">{goals.map((goal) => <button className="goal-card" key={goal.name} onClick={() => setSelected(goal)}><div className="goal-card-head"><span className={`goal-glyph ${goal.tone}`}>◎</span><span className="mission-tag gold">ACTIVE</span></div><h2>{goal.name}</h2><p>{goal.description}</p><div className="goal-progress-head"><span>Progress</span><strong>{goal.progress}%</strong></div><div className="goal-progress"><i style={{ width: `${goal.progress}%` }}></i></div><div className="goal-meta"><span>{goal.tasks} tasks</span><span>{goal.owner}</span><span>{goal.deadline}</span></div></button>)}</section>
    {selected && <div className="detail-backdrop" role="presentation" onClick={() => setSelected(null)}><section className="detail-drawer" role="dialog" aria-modal="true" aria-label={selected.name} onClick={(event) => event.stopPropagation()}><button className="drawer-close" onClick={() => setSelected(null)} aria-label="Close">×</button><p className="eyebrow">Goal detail · Preview</p><h2>{selected.name}</h2><p className="drawer-lede">{selected.description}</p><div className="drawer-stat"><span>Current progress</span><strong>{selected.progress}%</strong></div><div className="goal-progress"><i style={{ width: `${selected.progress}%` }}></i></div><div className="drawer-list"><div><span>Tasks complete</span><strong>{selected.tasks}</strong></div><div><span>Responsible agent</span><strong>{selected.owner}</strong></div><div><span>Deadline</span><strong>{selected.deadline}</strong></div></div><button className="secondary-button" onClick={() => setSelected(null)}>Close preview</button></section></div>}
  </div>
}
