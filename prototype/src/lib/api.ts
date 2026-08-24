export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

export interface ApiError extends Error {
  status?: number;
}

export async function apiFetch<T = unknown>(path: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${path}`;
  const response = await fetch(url, {
    ...options,
    credentials: 'include',
    headers: {
      ...(options?.body ? { 'Content-Type': 'application/json' } : {}),
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const err = new Error(`API error ${response.status}: ${response.statusText}`) as ApiError;
    err.status = response.status;
    throw err;
  }

  // Handle 204 No Content
  const contentLength = response.headers.get('content-length');
  if (response.status === 204 || contentLength === '0') {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export interface HealthResponse {
  status: string;
}

export function getHealth(): Promise<HealthResponse> {
  return apiFetch<HealthResponse>('/health');
}

export interface Workspace {
  id: string;
  name: string;
}

export function listWorkspaces(): Promise<Workspace[]> {
  return apiFetch<Workspace[]>('/api/v1/workspaces');
}
