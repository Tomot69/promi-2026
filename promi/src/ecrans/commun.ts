/**
 * CE QUE LES ÉCRANS PARTAGENT (la page +, la fiche) : fabriquer un nœud, échapper un texte, lire un toucher net, une couleur avec son alpha,
 * l'icône du bouton photo.
 */
/** le bouton photo d'une fiche et de la page + : le cadre traversé d'un trait (C-060, choix C) */
export const SVG_PHOTO =
  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3.5" y="5" width="17" height="14" rx="2.5"/><path d="M1.5 14.5c2.6-5 5.2-5 7.2-1.6s4.400 3.4 6.4 0 4-4.4 7.400-3.4"/></svg>';

export const esc = (s: string): string =>
  s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]!);

export function el<K extends keyof HTMLElementTagNameMap>(
  tag: K,
  attrs: Record<string, string> = {},
): HTMLElementTagNameMap[K] {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  return e;
}

/** un toucher net : appui puis lever à moins de 10 pt et 600 ms (SPEC-ECRANS §0) — au doigt, WebKit ne fabrique pas toujours de `click` */
export function surToucher(cible: HTMLElement, f: (ev: PointerEvent) => void): void {
  let d: { x: number; y: number; t: number; id: number } | null = null;
  cible.addEventListener('pointerdown', (ev) => {
    d = { x: ev.clientX, y: ev.clientY, t: ev.timeStamp, id: ev.pointerId };
  });
  cible.addEventListener('pointerup', (ev) => {
    const g = d;
    d = null;
    if (!g || g.id !== ev.pointerId) return;
    if (Math.hypot(ev.clientX - g.x, ev.clientY - g.y) > 10 || ev.timeStamp - g.t > 600) return;
    f(ev);
  });
  cible.addEventListener('pointercancel', () => {
    d = null;
  });
}

export function avecAlpha(h: string, a: number): string {
  const [r, g, b] = [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  return `rgba(${String(r)}, ${String(g)}, ${String(b)}, ${String(a)})`;
}
