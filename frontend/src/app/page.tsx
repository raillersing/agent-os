'use client'

import Link from 'next/link'
import { useState } from 'react'
import api from '@/lib/api'

const templates = ['Research a market', 'Prepare a brief', 'Review a codebase']
const missions = [
  { title: 'Customer research synthesis', detail: '18 interviews → themes and opportunities', status: 'RUNNING', progress: 68, accent: 'green', code: 'CR', updated: '12 min ago' },
  { title: 'Website launch checklist', detail: 'Content, accessibility and release readiness', status: 'REVIEW', progress: 84, accent: 'gold', code: 'WL', updated: '1 decision' },
]
const activity = [
  ['08:42', 'Research agent completed synthesis', 'Customer research synthesis', 'green'],
  ['08:29', 'Approval requested', 'Website launch checklist', 'gold'],
  ['08:00', 'Mission created', 'Monday operations brief', 'blue'],
]

export default function Home() {
  const [intent, setIntent] = useState('')
  const [prepared, setPrepared] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  const createMission = async () => {
    if (!intent.trim()) return
    setSaving(true); setError('')
    try {
      let workspaces = await api.listWorkspaces()
      if (!workspaces.length) workspaces = [await api.createWorkspace({ name: 'My workspace', description: 'Default local AgentOS workspace' })]
      await api.createMission({ workspace_id: workspaces[0].id, title: intent.trim().slice(0, 80), objective: intent.trim(), plan: [{ name: 'Clarify scope', status: 'planned' }, { name: 'Execute bounded work', status: 'planned' }, { name: 'Review evidence', status: 'planned' }] })
      setPrepared(true)
    } catch (cause) { setError(cause instanceof Error ? cause.message : 'The mission could not be saved.') }
    finally { setSaving(false) }
  }

  return <div className="page control-room">
    <section className="control-hero">
      <div className="control-hero-copy">
        <p className="eyebrow hero-eyebrow"><span className="eyebrow-rule"></span>Wednesday · 12 August 2026</p>
        <h1>Make progress<br /><em>visible.</em></h1>
        <p className="control-lede">One calm place to direct your agents, follow the work, and decide what happens next.</p>
        <div className="hero-actions"><Link className="primary-button" href="/missions">Open mission control <span>↗</span></Link><Link className="hero-secondary" href="/agents">View your agents <span>→</span></Link></div>
      </div>
      <div className="hero-orb" aria-hidden="true"><div className="orb-ring ring-one"></div><div className="orb-ring ring-two"></div><div className="orb-core"><span>✦</span><small>AGENT<br />OS</small></div><div className="orb-node node-one">PLAN</div><div className="orb-node node-two">RUN</div><div className="orb-node node-three">PROVE</div></div>
      <div className="hero-stats"><div><strong>03</strong><span>active missions</span></div><div><strong>01</strong><span>decision waiting</span></div><div><strong>99.8%</strong><span>system uptime</span></div></div>
    </section>

    <section className="mission-launch">
      <div className="launch-head"><div><p className="eyebrow">Start something new</p><h2>What should move forward?</h2></div><span className="launch-status"><i></i> Ready for input</span></div>
      <div className="launch-input"><span className="launch-symbol">✦</span><textarea value={intent} onChange={(event) => { setIntent(event.target.value); setPrepared(false) }} placeholder="Describe an outcome in plain language…" aria-label="Describe your goal" /><button className="primary-button" disabled={!intent.trim() || saving} onClick={createMission}>{saving ? 'Creating…' : 'Create mission'} <span>↗</span></button></div>
      <div className="launch-footer"><span>Try a starting point</span>{templates.map((template) => <button key={template} onClick={() => setIntent(template)}>{template}</button>)}</div>
    </section>
    {error && <p className="form-error" role="alert"><strong>Mission not saved.</strong> {error}</p>}
    {prepared && <div className="prepared-message" role="status"><div><strong>Mission draft ready</strong><span>Your outcome is persisted and ready for review.</span></div><Link href="/missions" className="primary-button">Review plan ↗</Link></div>}

    <section className="control-grid">
      <div className="motion-panel"><div className="panel-heading"><div><p className="eyebrow">Live workspace</p><h2>In motion</h2></div><Link href="/missions">View all ↗</Link></div><div className="motion-list">{missions.map((mission) => <Link href="/missions" className="motion-row" key={mission.title}><span className={`mission-code ${mission.accent}`}>{mission.code}</span><span className="motion-copy"><strong>{mission.title}</strong><small>{mission.detail}</small><span className="motion-progress"><i style={{ width: `${mission.progress}%` }}></i></span></span><span className={`mission-tag ${mission.accent}`}>{mission.status}</span><span className="motion-arrow">→</span></Link>)}</div></div>
      <aside className="decision-panel"><div className="panel-heading"><div><p className="eyebrow">Human in the loop</p><h2>One decision</h2></div><span className="decision-count">01</span></div><div className="decision-body"><div className="decision-icon">!</div><div><strong>Website launch checklist</strong><p>The release plan is ready for your approval.</p><Link href="/missions">Review decision <span>↗</span></Link></div></div><div className="decision-foot"><span>Waiting since</span><strong>21 min</strong></div></aside>
    </section>

    <section className="activity-panel"><div className="panel-heading"><div><p className="eyebrow">Traceable by design</p><h2>Recent activity</h2></div><Link href="/runs">Open run log ↗</Link></div><div className="activity-list">{activity.map(([time, title, detail, tone]) => <div className="activity-row" key={title}><time>{time}</time><span className={`activity-dot ${tone}`}></span><div><strong>{title}</strong><small>{detail}</small></div><span className="activity-check">✓</span></div>)}</div></section>
  </div>
}
