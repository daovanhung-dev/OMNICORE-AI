import {mountShared} from './features/shared/shared.route.js';
import {mountLayout} from './layouts/shared/layout.js';
export function mountRoute(root: HTMLElement, path: string): void {
  if (path === '/' || path === '/items') { const page = mountShared(mountLayout(root)); void page.load(); }
  else root.textContent = 'Không tìm thấy trang';
}
