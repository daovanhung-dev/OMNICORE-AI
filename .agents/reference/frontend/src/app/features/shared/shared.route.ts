import {ItemPageController} from './SH01/pages/item-page.js';
export function mountShared(root: HTMLElement): ItemPageController { return new ItemPageController(root); }
