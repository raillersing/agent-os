/**
 * React Hooks for Agent OS API
 */

'use client'

import { useState, useEffect, useCallback } from 'react';
import api from './api';

// Types
interface Agent {
  id: string;
  name: string;
  model: string;
  status: string;
  description?: string;
  capabilities: string[];
  config: Record<string, any>;
  policies: Record<string, any>;
  total_runs: number;
  successful_runs: number;
  failed_runs: number;
  total_tokens: number;
  total_cost: number;
  created_at: string;
  updated_at: string;
  last_run_at?: string;
}

export interface Run {
  id: string;
  agent_id: string;
  status: string;
  prompt: string;
  context?: Record<string, any>;
  result?: Record<string, any>;
  error?: string;
  progress: number;
  current_step?: string;
  steps: any[];
  tokens_used: number;
  cost: number;
  duration_ms?: number;
  started_at: string;
  completed_at?: string;
  created_at: string;
}

export interface Memory {
  key: string;
  content: string;
  type: string;
  source?: string;
  agent_id?: string;
  metadata_: Record<string, any>;
  access_count: number;
  last_accessed_at?: string;
  created_at: string;
  updated_at: string;
  expires_at?: string;
}

// Hooks
export function useAgents() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAgents = useCallback(async () => {
    try {
      setLoading(true);
      const data = await api.listAgents();
      setAgents(data);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAgents();
  }, [fetchAgents]);

  return { agents, loading, error, refetch: fetchAgents };
}

export function useAgent(id: string) {
  const [agent, setAgent] = useState<Agent | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchAgent() {
      try {
        setLoading(true);
        const data = await api.getAgent(id);
        setAgent(data);
        setError(null);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchAgent();
  }, [id]);

  return { agent, loading, error };
}

export function useRuns(agentId?: string) {
  const [runs, setRuns] = useState<Run[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchRuns = useCallback(async () => {
    try {
      setLoading(true);
      const data = await api.listRuns(agentId ? { agent_id: agentId } : undefined);
      setRuns(data);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [agentId]);

  useEffect(() => {
    fetchRuns();
  }, [fetchRuns]);

  return { runs, loading, error, refetch: fetchRuns };
}

export function useMemory(query?: string) {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const searchMemory = useCallback(async (q: string) => {
    try {
      setLoading(true);
      const data = await api.searchMemory(q);
      setMemories(data.results);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    searchMemory(query || '');
  }, [query, searchMemory]);

  return { memories, loading, error, search: searchMemory };
}

export function useTools() {
  const [tools, setTools] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchTools() {
      try {
        setLoading(true);
        const data = await api.listTools();
        setTools(data);
        setError(null);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchTools();
  }, []);

  return { tools, loading, error };
}
