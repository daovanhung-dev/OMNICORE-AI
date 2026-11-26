export interface Item { id: number; name: string }
export interface ItemPage { items: Item[]; total: number; page: number; page_size: number }
export function decodePage(raw: unknown): ItemPage {
  if (typeof raw !== 'object' || raw === null || !('data' in raw)) throw new Error('Phản hồi sai cấu trúc');
  const d = raw.data as Partial<ItemPage> | null;
  if (!d || !Array.isArray(d.items) || !d.items.every(x => x && Number.isSafeInteger(x.id) && typeof x.name === 'string') || !Number.isSafeInteger(d.total) || !Number.isSafeInteger(d.page) || !Number.isSafeInteger(d.page_size) || d.total! < 0 || d.page! < 1 || d.page_size! < 1) throw new Error('Phản hồi sai kiểu');
  return d as ItemPage;
}
