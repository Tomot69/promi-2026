/**
 * LE TRAIT DE LA PAGE + (§2.1 à §2.6 ; le prototype : `trait()` de `lot-S3-page-plus`, `ruban` et `chevron` de `window._onde`, `fleche`) —
 * peint sur l'onde, la parole prête (C-209, C-213, C-229) : l'amorce orange qui s'effile (le départ, C-133, C-169), le chevron, les points à
 * tracer (Ø 12 × 1,15, tous les 18 pt, C-184), la flèche d'invite courbe (§2.4). Pendant le geste : le plein du départ au doigt, jamais au-delà
 * de la moitié (C-237 ; le trait entier pour un Cercle). Les cotes et les couleurs sont celles du prototype, en dur.
 */
import { cheminOnde, type Onde } from './onde.ts';
import { palette } from '../../design/jetons.ts';
import { matiereTrait } from '../../animation/trace/pinceau.ts';

export const TRAIT_K = 1.3;
export const TRAIT_PTS = 1.15;
/** le trait posé sur un champ : la teinte sombre de sa nature (`NATTRAIT`, §2.1 bis corrigé, C-140) */
export const NATTRAIT = { promi: palette.bleu08, chiche: palette.framboise02, nuee: palette.mauve02 } as const;
/** le départ d'une action (C-133, D6) */
export const ORANGE_DEPART = palette.orangeDepart;

/** l'amorce effilée : la courbe décalée perpendiculairement de ± épaisseur / 2, de e0 à e1 */
export function ruban(g: CanvasRenderingContext2D, y: Onde, x0: number, x1: number, e0: number, e1: number): void {
  const n = 44;
  const haut: [number, number][] = [];
  const bas: [number, number][] = [];
  const d = (x: number): number => y(x + 0.5) - y(x - 0.5);
  for (let i = 0; i <= n; i++) {
    const x = x0 + ((x1 - x0) * i) / n;
    const e = (e0 + (e1 - e0) * (i / n)) / 2;
    const dd = d(x);
    const L = Math.sqrt(1 + dd * dd);
    haut.push([x - (dd / L) * e, y(x) + e / L]);
    bas.push([x + (dd / L) * e, y(x) - e / L]);
  }
  g.beginPath();
  g.moveTo(haut[0]![0], haut[0]![1]);
  for (let i = 1; i < haut.length; i++) g.lineTo(haut[i]![0], haut[i]![1]);
  for (let i = bas.length - 1; i >= 0; i--) g.lineTo(bas[i]![0], bas[i]![1]);
  g.closePath();
}

/** le chevron du départ, orange, couché sur la pente de l'onde en cx — `col` : la couleur du trait (une carte d'Index : on n'y trace rien, v146) */
export function chevron(
  g: CanvasRenderingContext2D,
  y: Onde,
  cx: number,
  ep: number,
  col: string = ORANGE_DEPART,
): void {
  const ang = Math.atan2(y(cx + 8) - y(cx - 8), 16);
  const k = ep / 10;
  g.save();
  g.translate(cx, y(cx));
  g.rotate(ang);
  g.beginPath();
  g.moveTo(-7 * k, -10 * k);
  g.lineTo(6 * k, 0);
  g.lineTo(-7 * k, 10 * k);
  g.lineWidth = 6 * k;
  g.lineCap = 'round';
  g.lineJoin = 'round';
  g.strokeStyle = col;
  g.stroke();
  g.restore();
}

/** §2.4 — la flèche d'invite : A = (chevron + 32, base + 46), B = (chevron + 10, base + 14), tête sur la tangente réelle en B (± 32°, 13) */
export function fleche(g: CanvasRenderingContext2D, base: number, chev: number, col: string): void {
  const ax = chev + 32;
  const ay = base + 46;
  const bx = chev + 10;
  const by = base + 14;
  const c1x = ax - 10;
  const c1y = ay - 4;
  const c2x = bx + 3;
  const c2y = by + 12;
  const K = TRAIT_K;
  g.save();
  g.strokeStyle = col;
  g.lineWidth = 4.5 * K;
  g.lineCap = 'round';
  g.lineJoin = 'round';
  let vx = bx - c2x;
  let vy = by - c2y;
  const L = Math.hypot(vx, vy) || 1;
  vx /= L;
  vy /= L;
  // le bout rond (4,5 de large) dépasse de 2,25 : la courbe s'arrête en deçà, son bout tombe là où les ailes se rejoignent
  g.beginPath();
  g.moveTo(ax, ay);
  g.bezierCurveTo(c1x, c1y, c2x, c2y, bx - vx * 2.25 * K, by - vy * 2.25 * K);
  g.stroke();
  const aile = (deg: number): [number, number] => {
    const r = (deg * Math.PI) / 180;
    return [bx - (vx * Math.cos(r) - vy * Math.sin(r)) * 13 * K, by - (vx * Math.sin(r) + vy * Math.cos(r)) * 13 * K];
  };
  const g1 = aile(-32);
  const g2 = aile(32);
  g.beginPath();
  g.moveTo(g1[0], g1[1]);
  g.lineTo(bx, by);
  g.lineTo(g2[0], g2[1]);
  g.stroke();
  g.restore();
}

export interface TraitPeint {
  /** le départ (le ruban ou le plein tiré, le chevron) : sur sa couche quand il clignote, sinon sur le champ */
  depart: CanvasRenderingContext2D;
  /** les points et la flèche */
  champ: CanvasRenderingContext2D;
  y: Onde;
  base: number;
  W: number;
  col: string;
  /** 'plate' : au repos ; 'cours' : le doigt trace, `doigt` l'abscisse ; 'signe' : la moitié (ou le trait entier) donnée */
  etat: 'plate' | 'cours' | 'signe';
  doigt: number;
  entier: boolean;
  /** le pinceau choisi (Q128, lot-PINCEAU) : sa matière remplace l'amorce, la part tirée et la moitié signée ; « Plein » : le trait plein */
  pinceau?: string | undefined;
}

/** le trait de la page + (le prototype, `trait()` § 3 et 4) ; rend l'abscisse du chevron */
export function peindreTrait(t: TraitPeint): number {
  const { y, W, col } = t;
  const ep = 10 * TRAIT_K;
  const rr = 4.5 * TRAIT_PTS;
  const esp = 18;
  const MI = t.entier ? W : W / 2;
  const cx = t.etat === 'signe' ? MI : t.etat === 'cours' ? Math.max(W * 0.11, Math.min(t.doigt, MI)) : W * 0.11;
  const bout = cx - ep * 0.15;
  const gD = t.depart;
  gD.save();
  gD.strokeStyle = ORANGE_DEPART;
  gD.fillStyle = ORANGE_DEPART;
  gD.lineWidth = ep;
  gD.lineCap = 'round';
  gD.lineJoin = 'round';
  // le pinceau : sa matière, de −3 % à la pointe (au repos : jusqu'au bout de l'amorce) — à l'orange du départ, à la couleur du trait une fois signé
  const pin = t.pinceau && t.pinceau !== 'Plein' ? t.pinceau : null;
  const fait =
    !!pin &&
    matiereTrait(
      t.etat === 'signe' ? t.champ : gD,
      pin,
      y,
      -W * 0.03,
      t.etat === 'plate' ? bout : cx,
      t.etat === 'signe' ? col : ORANGE_DEPART,
    );
  if (fait) {
    // la matière est posée
  } else if (t.etat === 'cours') {
    gD.beginPath();
    cheminOnde(gD, y, 0, cx, W);
    gD.stroke();
  } else if (t.etat === 'plate') {
    ruban(gD, y, -W * 0.03, bout, ep * 2.2, ep * 0.15);
    gD.fill();
  }
  gD.restore();
  if (t.etat === 'signe' && !fait) {
    // signée, la moitié reprend la couleur du trait
    const g = t.champ;
    g.save();
    g.strokeStyle = col;
    g.lineWidth = ep;
    g.lineCap = 'round';
    g.lineJoin = 'round';
    g.beginPath();
    cheminOnde(g, y, 0, cx, W);
    g.stroke();
    g.restore();
  }
  // le trait entier d'un Cercle donné : plus rien ne manque, ni chevron ni points
  if (!(t.entier && t.etat === 'signe')) {
    chevron(gD, y, cx, ep);
    const g = t.champ;
    g.save();
    g.fillStyle = col;
    const rp = 6 * TRAIT_PTS;
    for (let x = cx + esp * 1.3; x < W - rr; x += esp) {
      g.beginPath();
      g.arc(x, y(x), rp, 0, 6.2832);
      g.fill();
    }
    g.restore();
  }
  if (t.etat === 'plate') fleche(t.champ, t.base, W * 0.11, col);
  return cx;
}
