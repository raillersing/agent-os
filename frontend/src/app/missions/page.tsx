'use client'

import { useEffect, useMemo, useState } from 'react'
import api from '@/lib/api'

type Mission = { id: string; workspace_id: string; title: string; objective: string; status: string; progress: number; plan: Array<{ name?: string; status?: string }> }
type Approval = { id: string; mission_id: string; action: string; scope: Record<string, unknown>; status: string }
type AuditEvent = { id: string; event_type: string; details: Record<string, unknown>; created_at: string }

const statusClass = (status: string) => status === 'running' ? 'running' : status === 'waiting_approval' ? 'review' : 'complete'

export default function Missions() {
  const [missions, setMissions] = useState<Mission[]>([])
  const [approvals, setApprovals] = useState<Approval[]>([])
  const [auditEvents, setAuditEvents] = useState<AuditEvent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [deciding, setDeciding] = useState(false)

  const refresh = async () => {
    setLoading(true)
    try {
      const [missionData, approvalData] = await Promise.all([api.listMissions(), api.listApprovals('pending')])
      setMissions(missionData)
      setApprovals(approvalData)
      if (missionData[0]?.workspace_id) setAuditEvents(await api.listAuditEvents(missionData[0].workspace_id))
      else setAuditEvents([])
      setError('')
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Mission Control could not be loaded.')
    } finally { setLoading(false) }
  }

  useEffect(() => { refresh() }, [])
  const active = useMemo(() => missions.find((mission) => !['completed', 'cancelled', 'failed'].includes(mission.status)) || missions[0], [missions])
  const relevantApproval = approvals.find((approval) => approval.mission_id === active?.id)

  const decide = async (status: 'approved' | 'rejected') => {
    if (!relevantApproval) return
    setDeciding(true)
    try { await api.decideApproval(relevantApproval.id, status, `Decision recorded in Mission Control: ${status}.`); await refresh() }
    catch (cause) { setError(cause instanceof Error ? cause.message : 'Decision could not be saved.') }
    finally { setDeciding(false) }
  }

  const steps = active?.plan?.length ? active.plan : [{ name: 'Mission captured', status: active?.status || 'planned' }]
  const activeCount = missions.filter((mission) => ['planned', 'running', 'waiting_approval'].includes(mission.status)).length

  return <div className="page">
    <div className="page-heading"><div><p className="eyebrow">Mission Control</p><h1 className="page-title">Every outcome, clearly in motion.</h1><p className="page-subtitle">Follow persisted progress, inspect the requested scope, and step in only when judgment is needed.</p></div></div>
    <div className="metric-strip"><div className="metric"><span>Active missions</span><strong>{loading ? '…' : activeCount}</strong><small>Persisted</small></div><div className="metric"><span>Waiting on you</span><strong>{loading ? '…' : approvals.length}</strong><small>Approvals</small></div><div className="metric"><span>Completed</span><strong>{loading ? '…' : missions.filter((mission) => mission.status === 'completed').length}</strong><small>Recorded</small></div><div className="metric"><span>System state</span><strong>{error ? '!' : 'OK'}</strong><small>{error ? 'Needs attention' : 'Connected'}</small></div></div>
    {error && <p className="form-error" role="alert">Mission Control unavailable: {error}</p>}
    {!loading && !active && <div className="empty-message">No mission yet. Start from Home and describe the outcome you want to achieve.</div>}
    {active && <section className="section mission-layout"><div className="panel"><div className="panel-title"><h2>{active.title}</h2><span className={`status ${statusClass(active.status)}`}>{active.status.replace('_', ' ')} · {active.progress}%</span></div><p className="mission-objective">{active.objective}</p><div className="timeline">{steps.map((step, index) => { const complete = ['completed', 'done'].includes(step.status || '') || index < active.progress / 100 * steps.length; const current = !complete && index === Math.floor(active.progress / 100 * steps.length); return <div className={`step ${complete ? 'done' : current ? 'active' : ''}`} key={`${step.name}-${index}`}><span className="step-mark">{complete ? '✓' : index + 1}</span><div><h3>{step.name || `Step ${index + 1}`}</h3><p>{complete ? 'Recorded as complete.' : current ? 'Current persisted stage.' : 'Waiting for prior work.'}</p></div></div> })}</div></div><aside>{relevantApproval ? <div className="approval-card"><span>Approval required</span><h3>{relevantApproval.action}</h3><p>Scope: {Object.entries(relevantApproval.scope || {}).map(([key, value]) => `${key}: ${String(value)}`).join(' · ') || 'No additional scope metadata.'}</p><div className="approval-actions"><button className="approve" disabled={deciding} onClick={() => decide('approved')}>{deciding ? 'Saving…' : 'Approve once'}</button><button className="review-button" disabled={deciding} onClick={() => decide('rejected')}>Reject</button></div></div> : <div className="panel approval-complete" role="status"><span className="status complete">No pending approval</span><p>There is no action awaiting a decision for this mission.</p></div>}<div className="panel agents-panel"><div className="panel-title"><h2>Recent evidence</h2><span>Audit log</span></div>{auditEvents.length ? auditEvents.slice(0, 4).map((event) => <div className="agent-row" key={event.id}><span className="agent-badge">EV</span><div><strong>{event.event_type}</strong><small>{new Date(event.created_at).toLocaleString()}</small></div></div>) : <p className="panel-empty">No audit event for this workspace yet.</p>}</div><div className="panel agents-panel"><div className="panel-title"><h2>Mission record</h2><span>Persistent</span></div><div className="agent-row"><span className="agent-badge">ID</span><div><strong>Mission ID</strong><small>{active.id}</small></div></div><div className="agent-row"><span className="agent-badge">ST</span><div><strong>State</strong><small>Progress and plan are stored in the control plane.</small></div><span className="agent-state">{active.status}</span></div></div></aside></section>}
  </div>
}
