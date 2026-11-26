import type {Item} from '../models/item.model.js';
export function renderItems(container: HTMLElement, items: Item[]): void {
  const list = document.createElement('ul');
  for (const item of items) {
    const row = document.createElement('li');
    row.textContent = item.name;
    list.append(row);
  }
  container.replaceChildren(list);
}
