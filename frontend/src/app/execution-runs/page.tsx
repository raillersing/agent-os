'use client'

import { useCallback, useEffect, useState } from 'react'
import api from '@/lib/api'

const states = ['accepted', 'queued', 'running', 'retrying', 'completed', 'failed', 'cancelled', 'unknown']

export default function ExecutionRunsPage() {
  const [workspaceId, setWorkspaceId] = useState('')
  const [runs, setRuns] = useState<any[]>([])
  const [tasks, setTasks] = useState<any[]>([])
  const [evidence, setEvidence] = useState<any | null>(null)
  const [error, setError] = useState('')
  const refresh = useCallback(async () => {
    if (!workspaceId) return
    try { setRuns(await api.listExecutionRuns(workspaceId)); setTasks(await api.listTasks(workspaceId)); setError('') }
    catch (cause) { setError(cause instanceof Error ? cause.message : 'D1 execution unavailable') }
  }, [workspaceId])
  const inspectEvidence = async (runId: string) => {
    try { setEvidence(await api.getExecutionEvidence(runId, workspaceId)); setError('') }
    catch (cause) { setError(cause instanceof Error ? cause.message : 'Evidence unavailable') }
  }
  useEffect(() => { void refresh() }, [refresh])
  return <main className="page">
    <p className="eyebrow">D1 durable execution</p><h1 className="page-title">Tasks, runs and evidence</h1>
    <p className="page-subtitle">Lifecycle is read from the persisted control plane; Temporal history is not the UI authority.</p>
    <label>Workspace ID <input value={workspaceId} onChange={event => setWorkspaceId(event.target.value)} placeholder="workspace UUID" /></label>
    {error && <p className="form-error" role="alert">{error}</p>}
    <section className="panel"><h2>Tasks</h2>{tasks.map(task => <p key={task.id}><strong>{task.title}</strong> · {task.state} · {task.id}</p>)}{!tasks.length && <p className="panel-empty">Enter a workspace UUID to inspect persisted tasks.</p>}</section>
    <section className="panel"><h2>Runs</h2>{runs.map(run => <article key={run.id} className="agent-row"><div><strong>{run.state}</strong><small>{run.execution_mode === 'openai' ? 'LIVE / EXTERNAL OPENAI' : 'SIMULATOR'}</small><small>{run.id} · {run.workflow_id}</small><small>{run.attempts.length} attempts · {run.receipt ? `receipt ${run.receipt.id}` : 'no receipt yet'}</small>{run.artifacts.map((artifact: any) => <small key={artifact.id}>artifact {artifact.content_hash}</small>)}<button type="button" onClick={() => void inspectEvidence(run.id)}>Inspect AI evidence</button></div></article>)}{!runs.length && <p className="panel-empty">No persisted D1 runs.</p>}</section>
    {evidence && <section className="panel"><h2>AI evidence</h2><p>Disclosure: {evidence.context_manifests?.[0]?.disclosure_state ?? 'unknown'} · manifest {evidence.context_manifests?.[0]?.manifest_hash ?? 'unknown'}</p><p>Adapter: {evidence.invocations?.[0]?.adapter_id ?? 'simulator'} · actual model: {evidence.invocations?.[0]?.actual_model ?? 'unknown'}</p><p>Usage: {evidence.usage?.[0]?.source ?? 'unknown'} · cost: {evidence.usage?.[0]?.cost_state ?? 'unknown'} · latency: {evidence.invocations?.[0]?.latency_ms ?? 'unknown'} ms</p><p>Tools enabled: {evidence.invocations?.[0]?.tools_enabled ? 'yes' : 'no/unknown'}</p></section>}
    <div className="filter-row">{states.map(state => <span key={state} className="status">{state}</span>)}</div>
  </main>
}
