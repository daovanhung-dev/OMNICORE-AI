import {getAccessToken,clearSession} from '../auth/session.js';
export class HttpError extends Error { constructor(readonly status: number, readonly traceId: string | null) { super(`HTTP ${status}`); } }
export async function getJson(path: string, signal: AbortSignal, timeoutMs = 10000): Promise<unknown> {
  if (!path.startsWith('/api/') || path.startsWith('//')) throw new Error('Đường dẫn không hợp lệ');
  const headers: Record<string,string> = {Accept: 'application/json'};
  const token = getAccessToken(); if (token) headers.Authorization = `Bearer ${token}`;
  const controller = new AbortController();
  const abort = () => controller.abort();
  if(signal.aborted) abort(); else signal.addEventListener('abort',abort,{once:true});
  const timer = setTimeout(abort,timeoutMs);
  try {
    const response = await fetch(path, {signal: controller.signal, headers});
    if (response.status === 401) clearSession();
    if (!response.ok) throw new HttpError(response.status,response.headers.get('X-Request-ID'));
    return await response.json();
  } finally { clearTimeout(timer);signal.removeEventListener('abort',abort); }
}
