/**
 * Agent OS API Client
 *
 * Authentication is handled through an httpOnly cookie returned by the server.
 * All requests include credentials so the cookie is sent cross-origin in local
 * development (same host, different port).
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

interface RequestOptions {
  method?: string;
  headers?: Record<string, string>;
  body?: any;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
    const { method = 'GET', headers = {}, body } = options;

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...headers,
      },
      credentials: 'include',
      body: body ? JSON.stringify(body) : undefined,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));
      throw new Error(error.detail || `HTTP error ${response.status}`);
    }

    if (response.status === 204) {
      return null as T;
    }

    return response.json();
  }

  // Auth
  async login(email: string, password: string) {
    return this.request<{ access_token: string }>('/api/v1/auth/token', {
      method: 'POST',
      body: { email, password },
    });
  }

  async logout() {
    return this.request<null>('/api/v1/auth/logout', { method: 'POST' });
  }

  // Agents
  async listAgents(params?: { limit?: number; offset?: number; status?: string }) {
    const query = new URLSearchParams();
    if (params?.limit) query.set('limit', params.limit.toString());
    if (params?.offset) query.set('offset', params.offset.toString());
    if (params?.status) query.set('status', params.status);
    return this.request<any[]>(`/api/v1/agents?${query.toString()}`);
  }

  async getAgent(id: string) {
    return this.request<any>(`/api/v1/agents/${id}`);
  }

  async createAgent(data: any) {
    return this.request<any>('/api/v1/agents', {
      method: 'POST',
      body: data,
    });
  }

  async updateAgent(id: string, data: any) {
    return this.request<any>(`/api/v1/agents/${id}`, {
      method: 'PATCH',
      body: data,
    });
  }

  async deleteAgent(id: string) {
    return this.request<null>(`/api/v1/agents/${id}`, {
      method: 'DELETE',
    });
  }

  // Runs
  async listRuns(params?: { limit?: number; offset?: number; agent_id?: string; status?: string }) {
    const query = new URLSearchParams();
    if (params?.limit) query.set('limit', params.limit.toString());
    if (params?.offset) query.set('offset', params.offset.toString());
    if (params?.agent_id) query.set('agent_id', params.agent_id);
    if (params?.status) query.set('status', params.status);
    return this.request<any[]>(`/api/v1/runs?${query.toString()}`);
  }

  async getRun(id: string) {
    return this.request<any>(`/api/v1/runs/${id}`);
  }

  async createRun(agentId: string, data: any) {
    return this.request<any>(`/api/v1/runs/${agentId}/run`, {
      method: 'POST',
      body: data,
    });
  }

  async cancelRun(id: string) {
    return this.request<any>(`/api/v1/runs/${id}/cancel`, {
      method: 'POST',
    });
  }

  // Memory
  async searchMemory(query: string, limit?: number) {
    const params = new URLSearchParams({ q: query });
    if (limit) params.set('limit', limit.toString());
    return this.request<any>(`/api/v1/memory/search?${params.toString()}`);
  }

  async getMemory(key: string) {
    return this.request<any>(`/api/v1/memory/${key}`);
  }

  async createMemory(data: any) {
    return this.request<any>('/api/v1/memory', {
      method: 'POST',
      body: data,
    });
  }

  async deleteMemory(key: string) {
    return this.request<null>(`/api/v1/memory/${key}`, {
      method: 'DELETE',
    });
  }

  // Tools
  async listTools() {
    return this.request<any[]>('/api/v1/tools');
  }

  async executeTool(toolId: string, data: any) {
    return this.request<any>(`/api/v1/tools/${toolId}/execute`, {
      method: 'POST',
      body: data,
    });
  }

  // Health
  async healthCheck() {
    return this.request<any>('/health');
  }

  async listArtifacts(workspaceId: string) {
    return this.request<any[]>(`/api/v1/artifacts?workspace_id=${encodeURIComponent(workspaceId)}`);
  }

  async listWorkspaces() {
    return this.request<any[]>('/api/v1/workspaces');
  }

  async createWorkspace(data: { name: string; description?: string; budget?: number }) {
    return this.request<any>('/api/v1/workspaces', { method: 'POST', body: data });
  }

  async listProjects(workspaceId?: string) {
    if (!workspaceId) throw new Error('workspaceId is required to list projects');
    const query = `?workspace_id=${encodeURIComponent(workspaceId)}`;
    return this.request<Array<{ project_id: string; workspace_id: string; name: string; purpose: string; state: 'active' | 'paused' | 'archived'; created_by: string; version: number }>>(`/api/v1/projects${query}`);
  }

  async createProject(data: { workspace_id: string; name: string; purpose: string }) {
    return this.request<{ project_id: string; workspace_id: string; name: string; purpose: string; state: 'active' | 'paused' | 'archived'; created_by: string; version: number }>('/api/v1/projects', { method: 'POST', body: data });
  }

  async listMissions(workspaceId: string) {
    return this.request<any[]>(`/api/v1/missions?workspace_id=${encodeURIComponent(workspaceId)}`);
  }

  async createMission(data: { workspace_id: string; project_id: string; title: string; objective: string; plan?: Array<Record<string, unknown>> }) {
    return this.request<{ id: string; workspace_id: string; project_id: string; title: string; objective: string }>('/api/v1/missions', { method: 'POST', body: data });
  }

  async listAutomations(workspaceId: string) {
    return this.request<any[]>(`/api/v1/automations?workspace_id=${encodeURIComponent(workspaceId)}`);
  }

  async createAutomation(data: { workspace_id: string; name: string; description?: string; trigger_type: string; trigger_config?: Record<string, unknown>; steps?: Array<Record<string, unknown>> }) {
    return this.request<any>('/api/v1/automations', { method: 'POST', body: data });
  }

  async listApprovals(workspaceId: string, status?: string) {
    const params = new URLSearchParams({ workspace_id: workspaceId });
    if (status) params.set('status', status);
    return this.request<any[]>(`/api/v1/approvals?${params.toString()}`);
  }

  async createApproval(workspaceId: string, data: { mission_id: string; action: string; scope?: Record<string, unknown> }) {
    return this.request<any>(`/api/v1/approvals?workspace_id=${encodeURIComponent(workspaceId)}`, { method: 'POST', body: data });
  }

  async listAuditEvents(workspaceId: string, limit = 8) {
    return this.request<any[]>(`/api/v1/audit-events?workspace_id=${encodeURIComponent(workspaceId)}&limit=${limit}`);
  }

  async decideApproval(workspaceId: string, id: string, status: 'approved' | 'rejected', decisionNote?: string) {
    return this.request<any>(`/api/v1/approvals/${id}/decision?workspace_id=${encodeURIComponent(workspaceId)}`, {
      method: 'POST',
      body: { status, decision_note: decisionNote },
    });
  }

  async listTasks(workspaceId: string) {
    return this.request<any[]>(`/api/v1/tasks?workspace_id=${encodeURIComponent(workspaceId)}`);
  }

  async listExecutionRuns(workspaceId: string) {
    return this.request<any[]>(`/api/v1/execution-runs?workspace_id=${encodeURIComponent(workspaceId)}`);
  }

  async getExecutionRun(id: string, workspaceId: string) {
    return this.request<any>(`/api/v1/execution-runs/${id}?workspace_id=${encodeURIComponent(workspaceId)}`);
  }

  async cancelExecutionRun(id: string, workspaceId: string) {
    return this.request<any>(`/api/v1/execution-runs/${id}/cancel?workspace_id=${encodeURIComponent(workspaceId)}`, { method: 'POST' });
  }

  async getExecutionEvidence(id: string, workspaceId: string) {
    return this.request<any>(`/api/v1/execution-runs/${id}/evidence?workspace_id=${encodeURIComponent(workspaceId)}`);
  }
}

export const api = new ApiClient();
export default api;
