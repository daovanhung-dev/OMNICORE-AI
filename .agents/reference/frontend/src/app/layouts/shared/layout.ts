export function mountLayout(root: HTMLElement): HTMLElement {
  const outlet = document.createElement('div'); root.replaceChildren(outlet); return outlet;
}
