import {mountRoute} from './app/app.routes.js';
const root = document.getElementById('app');
if (!root) throw new Error('Thiếu vùng hiển thị');
mountRoute(root, location.pathname);
