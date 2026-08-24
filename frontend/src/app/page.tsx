'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'
import api from '@/lib/api'

const templates = ['Research a market', 'Prepare a brief', 'Review a codebase']

export default function Home() {
  const [intent, setIntent] = useState('')
  const [prepared, setPrepared] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  const [workspaceId, setWorkspaceId] = useState<string | null>(null)
  const [missions, setMissions] = useState<any[]>([])
  const [pendingApprovals, setPendingApprovals] = useState<any[]>([])
  const [activity, setActivity] = useState<any[]>([])

  useEffect(() => {
    async function bootstrap() {
      try {
        const workspaces = await api.listWorkspaces()
        if (!workspaces.length) return
        const firstId = workspaces[0].id
        setWorkspaceId(firstId)
        const [missionData, approvalData, auditData] = await Promise.all([
          api.listMissions(firstId),
          api.listApprovals(firstId, 'pending'),
          api.listAuditEvents(firstId, 5),
        ])
        setMissions(missionData.slice(0, 4))
        setPendingApprovals(approvalData)
        setActivity(auditData)
      } catch (cause) {
        setError(cause instanceof Error ? cause.message : 'Workspace unavailable')
      } finally {
        setLoading(false)
      }
    }
    bootstrap()
  }, [])

  const createMission = async () => {
    if (!intent.trim() || !workspaceId) return
    setSaving(true); setError('')
    try {
      let projects = await api.listProjects(workspaceId)
      if (!projects.length) projects = [await api.createProject({ workspace_id: workspaceId, name: intent.trim().slice(0, 80), purpose: intent.trim() })]
      await api.createMission({
        workspace_id: workspaceId,
        project_id: projects[0].project_id,
        title: intent.trim().slice(0, 80),
        objective: intent.trim(),
        plan: [{ name: 'Clarify scope', status: 'planned' }, { name: 'Execute bounded work', status: 'planned' }, { name: 'Review evidence', status: 'planned' }],
      })
      const refreshed = await api.listMissions(workspaceId)
      setMissions(refreshed.slice(0, 4))
      setPrepared(true)
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'The mission could not be saved.')
    } finally {
      setSaving(false)
    }
  }

  const runningMissions = missions.filter((m) => m.state === 'running' || m.state === 'queued')
  const firstApproval = pendingApprovals[0]

  return <div className="page control-room">
    <section className="control-hero">
      <div className="control-hero-copy">
        <p className="eyebrow hero-eyebrow"><span className="eyebrow-rule"></span>Control room</p>
        <h1>Make progress<br /><em>visible.</em></h1>
        <p className="control-lede">One calm place to direct your agents, follow the work, and decide what happens next.</p>
        <div className="hero-actions"><Link className="primary-button" href="/missions">Open mission control <span>↗</span></Link><Link className="hero-secondary" href="/agents">View your agents <span>→</span></Link></div>
      </div>
      <div className="hero-orb" aria-hidden="true"><div className="orb-ring ring-one"></div><div className="orb-ring ring-two"></div><div className="orb-core"><span>✦</span><small>AGENT<br />OS</small></div><div className="orb-node node-one">PLAN</div><div className="orb-node node-two">RUN</div><div className="orb-node node-three">PROVE</div></div>
      <div className="hero-stats"><div><strong>{String(runningMissions.length).padStart(2, '0')}</strong><span>active missions</span></div><div><strong>{String(pendingApprovals.length).padStart(2, '0')}</strong><span>decision{pendingApprovals.length === 1 ? '' : 's'} waiting</span></div><div><strong>99.8%</strong><span>system uptime</span></div></div>
    </section>

    <section className="mission-launch">
      <div className="launch-head"><div><p className="eyebrow">Start something new</p><h2>What should move forward?</h2></div><span className="launch-status"><i></i> Ready for input</span></div>
      <div className="launch-input"><span className="launch-symbol">✦</span><textarea value={intent} onChange={(event) => { setIntent(event.target.value); setPrepared(false) }} placeholder="Describe an outcome in plain language…" aria-label="Describe your goal" /><button className="primary-button" disabled={!intent.trim() || saving || !workspaceId} onClick={createMission}>{saving ? 'Creating…' : 'Create mission'} <span>↗</span></button></div>
      <div className="launch-footer"><span>Try a starting point</span>{templates.map((template) => <button key={template} onClick={() => setIntent(template)}>{template}</button>)}</div>
    </section>
    {error && <p className="form-error" role="alert"><strong>Mission not saved.</strong> {error}</p>}
    {prepared && <div className="prepared-message" role="status"><div><strong>Mission draft ready</strong><span>Your outcome is persisted and ready for review.</span></div><Link href="/missions" className="primary-button">Review plan ↗</Link></div>}

    <section className="control-grid">
      <div className="motion-panel"><div className="panel-heading"><div><p className="eyebrow">Live workspace</p><h2>In motion</h2></div><Link href="/missions">View all ↗</Link></div>
        {loading && <p className="panel-empty">Loading missions…</p>}
        {!loading && !missions.length && <p className="panel-empty">No missions yet. Create one above.</p>}
        <div className="motion-list">{missions.map((mission) => <Link href="/missions" className="motion-row" key={mission.id}><span className={`mission-code ${mission.state === 'running' ? 'green' : mission.state === 'completed' ? 'blue' : 'gold'}`}>{mission.title.slice(0, 2).toUpperCase()}</span><span className="motion-copy"><strong>{mission.title}</strong><small>{mission.objective || 'No objective provided'}</small></span><span className={`mission-tag ${mission.state === 'running' ? 'green' : mission.state === 'completed' ? 'blue' : 'gold'}`}>{mission.state.toUpperCase()}</span><span className="motion-arrow">→</span></Link>)}</div>
      </div>
      <aside className="decision-panel"><div className="panel-heading"><div><p className="eyebrow">Human in the loop</p><h2>{pendingApprovals.length > 1 ? `${pendingApprovals.length} decisions` : 'One decision'}</h2></div><span className="decision-count">{String(pendingApprovals.length).padStart(2, '0')}</span></div>
        {firstApproval ? <div className="decision-body"><div className="decision-icon">!</div><div><strong>{firstApproval.action}</strong><p>A decision is waiting for mission {firstApproval.mission_id.slice(0, 8)}.</p><Link href="/missions">Review decision <span>↗</span></Link></div></div> : <div className="decision-body"><div className="decision-icon">✓</div><div><strong>No pending decision</strong><p>Everything is running smoothly.</p></div></div>}
      </aside>
    </section>

    <section className="activity-panel"><div className="panel-heading"><div><p className="eyebrow">Traceable by design</p><h2>Recent activity</h2></div><Link href="/runs">Open run log ↗</Link></div>
      {loading && <p className="panel-empty">Loading audit events…</p>}
      {!loading && !activity.length && <p className="panel-empty">No recent activity.</p>}
      <div className="activity-list">{activity.map((event: any) => <div className="activity-row" key={event.id}><time>{new Date(event.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</time><span className={`activity-dot ${event.severity === 'error' ? 'red' : event.severity === 'warning' ? 'gold' : 'green'}`}></span><div><strong>{event.event_type}</strong><small>{event.description || event.entity_type}</small></div><span className="activity-check">✓</span></div>)}</div>
    </section>
  </div>
}
