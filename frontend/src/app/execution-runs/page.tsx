'use client'

import { useCallback, useEffect, useState } from 'react'
import api from '@/lib/api'

const states = ['accepted', 'queued', 'running', 'retrying', 'completed', 'failed', 'cancelled', 'unknown']

export default function ExecutionRunsPage() {
  const [workspaceId, setWorkspaceId] = useState('')
  const [runs, setRuns] = useState<any[]>([])
  const [tasks, setTasks] = useState<any[]>([])
  const [error, setError] = useState('')
  const refresh = useCallback(async () => {
    if (!workspaceId) return
    try { setRuns(await api.listExecutionRuns(workspaceId)); setTasks(await api.listTasks(workspaceId)); setError('') }
    catch (cause) { setError(cause instanceof Error ? cause.message : 'D1 execution unavailable') }
  }, [workspaceId])
  useEffect(() => { void refresh() }, [refresh])
  return <main className="page">
    <p className="eyebrow">D1 durable execution</p><h1 className="page-title">Tasks, runs and evidence</h1>
    <p className="page-subtitle">Lifecycle is read from the persisted control plane; Temporal history is not the UI authority.</p>
    <label>Workspace ID <input value={workspaceId} onChange={event => setWorkspaceId(event.target.value)} placeholder="workspace UUID" /></label>
    {error && <p className="form-error" role="alert">{error}</p>}
    <section className="panel"><h2>Tasks</h2>{tasks.map(task => <p key={task.id}><strong>{task.title}</strong> · {task.state} · {task.id}</p>)}{!tasks.length && <p className="panel-empty">Enter a workspace UUID to inspect persisted tasks.</p>}</section>
    <section className="panel"><h2>Runs</h2>{runs.map(run => <article key={run.id} className="agent-row"><div><strong>{run.state}</strong><small>{run.id} · {run.workflow_id}</small><small>{run.attempts.length} attempts · {run.receipt ? `receipt ${run.receipt.id}` : 'no receipt yet'}</small>{run.artifacts.map((artifact: any) => <small key={artifact.id}>artifact {artifact.content_hash}</small>)}</div></article>)}{!runs.length && <p className="panel-empty">No persisted D1 runs.</p>}</section>
    <div className="filter-row">{states.map(state => <span key={state} className="status">{state}</span>)}</div>
  </main>
}
