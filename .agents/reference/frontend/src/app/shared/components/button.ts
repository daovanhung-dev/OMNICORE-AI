export function button(label: string, action?: () => void): HTMLButtonElement {
  const el = document.createElement('button'); el.type='button'; el.textContent=label;
  if(action) el.addEventListener('click',action); return el;
}
