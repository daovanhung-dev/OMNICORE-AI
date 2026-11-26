import {getJson} from '../../../../core/http/api-client.js';
export async function fetchItems(page: number, signal: AbortSignal): Promise<unknown> {
  const query = new URLSearchParams({page: String(page), page_size: '1'});
  return getJson(`/api/v1/items?${query}`, signal);
}
