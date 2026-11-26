import {button} from '../../../../shared/components/button.js';
import {fetchItems} from '../data-access/item.service.js';
import {decodePage} from '../models/item.model.js';
import {renderItems} from '../ui/item-list.js';
export class ItemPageController {
  private page = 1;
  private request?: AbortController;
  private readonly status = document.createElement('p');
  private readonly list = document.createElement('section');
  private readonly next = button('Tiếp');
  private readonly previous = button('Trước');
  private readonly retry = button('Tải lại');
  constructor(private readonly root: HTMLElement) {
    const title = document.createElement('h1'); title.textContent = 'Danh mục';
    this.status.setAttribute('role','status');
    this.next.textContent = 'Tiếp'; this.previous.textContent = 'Trước'; this.retry.textContent = 'Tải lại';
    this.next.onclick = () => void this.load(this.page + 1);
    this.previous.onclick = () => void this.load(this.page - 1);
    this.retry.onclick = () => void this.load(this.page);
    this.root.replaceChildren(title,this.status,this.list,this.previous,this.next,this.retry);
  }
  async load(page: number = 1): Promise<void> {
    this.request?.abort(); const controller = new AbortController(); this.request = controller;
    this.previous.disabled = this.next.disabled = true;
    this.status.textContent = 'Đang tải…'; this.list.replaceChildren();
    try {
      const raw = await fetchItems(page, controller.signal);
      if (this.request !== controller) return;
      const data = decodePage(raw);
      this.page = data.page;
      this.status.textContent = data.items.length ? `Trang ${data.page} · ${data.total} mục` : 'Không có dữ liệu';
      renderItems(this.list, data.items);
      this.previous.disabled = data.page <= 1;
      this.next.disabled = data.page * data.page_size >= data.total;
    } catch {
      if (this.request === controller && !controller.signal.aborted) this.status.textContent = 'Không tải được dữ liệu. Hãy thử lại.';
    }
  }
  destroy(): void { this.request?.abort(); this.root.replaceChildren(); }
}
