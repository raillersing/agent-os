'use client'

import { useEffect, useState } from 'react'
import api from '@/lib/api'

type Automation = { id: string; name: string; description: string; trigger_type: string; trigger_config: Record<string, unknown>; steps: Array<{ name?: string }>; enabled: number }

export default function Automations() {
  const [automations, setAutomations] = useState<Automation[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const refresh = () => api.listAutomations().then(setAutomations).catch((cause) => setError(cause.message)).finally(() => setLoading(false))
  useEffect(() => { refresh() }, [])
  const create = async () => { try { const workspaces = await api.listWorkspaces(); if (!workspaces.length) { setError('Create a workspace before creating an automation.'); return } const automation = await api.createAutomation({ workspace_id: workspaces[0].id, name: 'New scheduled brief', description: 'A bounded, reviewable scheduled workflow.', trigger_type: 'schedule', trigger_config: { cron: '0 8 * * 1' }, steps: [{ name: 'Collect' }, { name: 'Prepare' }, { name: 'Review' }] }); setAutomations((current) => [automation, ...current]); setError('') } catch (cause) { setError(cause instanceof Error ? cause.message : 'Automation could not be saved.') } }
  return <div className="page"><div className="page-heading"><div><p className="eyebrow">Automations</p><h1 className="page-title">Repeat the work, not the setup.</h1><p className="page-subtitle">Each workflow has a persisted trigger, bounded steps, and an inspectable state.</p></div><button className="primary-button" onClick={create}>＋ New automation</button></div>{error && <p className="form-error" role="alert">{error}</p>}{loading && <div className="empty-message">Loading persisted automations…</div>}{!loading && !error && !automations.length && <div className="empty-message">No automation yet. Create a workspace, then add a bounded recurring workflow.</div>}<section className="section collection-grid">{automations.map((automation) => <article className="card collection-card" key={automation.id}><div className="card-top"><span className={`status ${automation.enabled ? 'running' : 'complete'}`}>{automation.enabled ? 'On' : 'Paused'}</span><span className="trigger">{automation.trigger_type}</span></div><h2>{automation.name}</h2><p>{automation.description || 'No description yet.'}</p><div className="automation-flow">{automation.steps.map((step, index) => <span key={`${step.name}-${index}`}>{index > 0 && <b>→ </b>}{step.name || `Step ${index + 1}`}</span>)}</div></article>)}</section></div>
}
