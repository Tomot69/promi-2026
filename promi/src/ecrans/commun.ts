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

// ── LA CROIX D'UN PLATEAU (le prototype : `lot-V157-CROIX`, C-173, v158) ──────────────────────────────────────────────────────────────────
interface Metriques {
  cap: number;
  xh: number;
  xa: number;
  fa: number;
  fd: number;
}
const METRIQUES = new Map<string, Metriques>();
let cvMetr: CanvasRenderingContext2D | null = null;
/** les métriques d'une police (pour 1 px), lues sur la police RENDUE (`metr`) : la capitale H, le X, et la boîte de la police */
function metr(fam: string, wt: string, st: string): Metriques {
  const cle = st + '|' + wt + '|' + fam;
  const deja = METRIQUES.get(cle);
  if (deja) return deja;
  cvMetr ??= document.createElement('canvas').getContext('2d')!;
  const g = cvMetr;
  g.font = `${st} ${wt} 100px ${fam}`;
  const h = g.measureText('H');
  const x = g.measureText('X');
  const r: Metriques = {
    cap: (h.actualBoundingBoxAscent || 70) / 100,
    xh: ((x.actualBoundingBoxAscent || 70) + (x.actualBoundingBoxDescent || 0)) / 100,
    xa: (x.actualBoundingBoxAscent || 70) / 100,
    fa: (h.fontBoundingBoxAscent || 0) / 100,
    fd: (h.fontBoundingBoxDescent || 0) / 100,
  };
  // une police pas encore chargée : on ne garde pas sa mesure
  if (document.fonts.check(`${st} ${wt} 100px ${fam}`)) METRIQUES.set(cle, r);
  return r;
}

/**
 * LA CROIX « X » D'UN PLATEAU, posée comme le prototype la pose (`pose()` de lot-V157-CROIX) : le « X » de PromiLate à la taille du X de
 * « INDEX » (35 px, `_tailleX`), centré sur les CAPITALES du titre de la barre (sa ligne de base lue sur les métriques de sa police rendue), son
 * bord droit à la distance du bord de la barre où le titre commence à gauche ; une boîte de 44 × 44 centrée sur lui. Tout se lit sur la police
 * rendue : sur un autre moteur de polices (WebKit de Linux) la croix suit le titre comme dans le prototype, jamais une cote relevée sur le Mac.
 */
export function poserCroix(croix: HTMLElement, glyphe: HTMLElement, titre: HTMLElement): void {
  const op = (croix.offsetParent as HTMLElement | null) ?? croix.parentElement!;
  const ro = op.getBoundingClientRect();
  const kk = ro.width / (op.offsetWidth || 1) || 1;
  if (!ro.width || !titre.getClientRects().length) return;
  const c = getComputedStyle(titre);
  const m = metr(c.fontFamily, c.fontWeight, c.fontStyle);
  const fsT = parseFloat(c.fontSize) || 16;
  const rg = document.createRange();
  rg.selectNodeContents(titre);
  const R = rg.getClientRects();
  const r = R.length ? R[0]! : titre.getBoundingClientRect();
  const tot = m.fa + m.fd || 1.2;
  const base = m.fa ? r.top + r.height * (m.fa / tot) : r.top + r.height * 0.78;
  const cap = m.cap * fsT * kk;
  const fam = getComputedStyle(document.documentElement).getPropertyValue('--f-marque').trim() || 'PromiLate';
  const mX = metr(fam, '400', 'normal');
  const fs = 35;
  cvMetr ??= document.createElement('canvas').getContext('2d')!;
  cvMetr.font = `400 100px ${fam}`;
  const lx = (fs * kk * cvMetr.measureText('X').width) / 100;
  const ins = r.left - ro.left;
  const cx = ro.right - ins - lx / 2;
  const cy = base - cap / 2;
  const left = (cx - ro.left) / kk - op.clientLeft + op.scrollLeft - 22;
  const top = (cy - ro.top) / kk - op.clientTop + op.scrollTop - 22;
  const fa = mX.fa || 0.93;
  const fd = mX.fd || 0.27;
  const gt = 22 - fa * fs + ((mX.xa - (mX.xh - mX.xa)) * fs) / 2;
  croix.style.left = `${left.toFixed(2)}px`;
  croix.style.top = `${top.toFixed(2)}px`;
  croix.style.right = 'auto';
  glyphe.style.top = `${gt.toFixed(2)}px`;
  glyphe.style.lineHeight = `${((fa + fd) * fs).toFixed(2)}px`;
  glyphe.style.fontSize = `${fs.toFixed(2)}px`;
}
