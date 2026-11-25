/**
 * LA CARTE D'INDEX (SPEC-ECRANS §8, PROMI-SPECIFICATIONS §3.9 ; le prototype : `geo`, `peintCarte`, `_s4Index` de lot-S4, `_s4TitresAjuste`
 * (C-151, v203) ; la construction de la fiche, C-147). Elle se réutilise : la fiche d'une personne porte les mêmes cartes (trois par ligne).
 *
 *     échelle   = hauteur / 600 ;  base = la hauteur de trait de la fiche (bornée à [196, 344]) × échelle
 *     amplitude = 13 × largeur / 173 ;  boîte = ⌊ base + amplitude + 20 ⌋
 *     trait     = 5,5 × largeur / 173 · points r = 3,2 × l/173 tous les 11 × l/173 ; UNE période d'onde sur la largeur de la carte
 *
 * Le champ porte la nature (et cède à la dalle quand elles se confondent, Q93) ; la dalle porte le monde, jamais la nature — sauf sous Ingénu
 * (Q297 : la rampe de sa nature) ; le corps est celui de la fiche (C-147 : `#0E78F2` · `#7C3F58` · `#5D4978`, la terre d'une parole tenue),
 * dans les deux thèmes ; le texte crème, l'état comme sur la fiche (« TENU » en amande).
 */
import type { Facade } from '../../moteur/facade.ts';
import type { Parole } from '../../donnees/schema.ts';
import { palette } from '../../design/jetons.ts';
import { el } from '../commun.ts';
import { cheminOnde, onde } from '../page-plus/onde.ts';
import { chevron, NATTRAIT, ruban } from '../page-plus/trait.ts';
import { CRETE } from '../fiche/ligne.ts';
import { traitFiche, type ModeTrait } from '../../metier/fiche.ts';
import { photoDe } from '../fiche/photo.ts';
import { imagePhoto } from '../photo/peinture.ts';
import { esc } from '../commun.ts';

export type NatureCarte = 'promi' | 'chiche' | 'nuee';

/** le champ de la nature (`NATCOL`) */
export const NATCOL: Record<NatureCarte, string> = {
  promi: palette.bleu45,
  chiche: palette.framboise54,
  nuee: palette.mauve77,
};
/** le texte du libellé de nature, posé sur la crème (`_NATTXT`) */
export const NATTXT: Record<NatureCarte, string> = {
  promi: palette.bleu08,
  chiche: palette.framboise11,
  nuee: palette.brun193,
};
/** le corps de la fiche (C-147) */
export const CORPS: Record<NatureCarte, string> = {
  promi: palette.cobalt50,
  chiche: palette.framboise35,
  nuee: palette.mauve35,
};
export const MOT_NAT: Record<NatureCarte, string> = { promi: 'Promi', chiche: 'Chiche', nuee: 'Cercle' };
/**
 * la largeur du libellé de nature, une COTE (PromiLate 13 px, relevée police chargée, 20 sept.) — jamais une mesure au moment de peindre : la
 * police n'y est pas encore (§8)
 */
export const LARGEUR_LIB: Record<NatureCarte, number> = { promi: 73, chiche: 81, nuee: 76 };
/** Q297 — sous Ingénu, la rampe de la nature (`RAMPE` de `_ingenuRampe`, v18–v19) */
const hex = (v: string): number[] => [1, 3, 5].map((i) => parseInt(v.slice(i, i + 2), 16));
export const RAMPE_INGENU: Record<NatureCarte, number[][]> = {
  promi: [palette.ingenuPromi1, palette.ingenuPromi2, palette.ingenuPromi3].map(hex),
  chiche: [palette.ingenuChiche1, palette.ingenuChiche2, palette.ingenuChiche3, palette.ingenuChiche4].map(hex),
  nuee: [palette.ingenuCercle1, palette.ingenuCercle2, palette.ingenuCercle3].map(hex),
};

export interface GeoCarte {
  w: number;
  h: number;
  base: number;
  amp: number;
  boite: number;
  ep: number;
  r: number;
  esp: number;
  dalle: { x: number; y: number; w: number; h: number };
}

/** la géométrie d'une carte (`geo`) : `fige` — une hauteur de trait figée à la plantation n'est pas bornée */
export function geoCarte(w: number, h: number, baseFiche: number, fige = false): GeoCarte {
  let bf = baseFiche;
  if (!fige) bf = Math.max(196, Math.min(344, bf));
  const s = h / 600;
  const k = w / 173;
  const base = bf * s;
  const amp = 13 * k;
  const boite = Math.floor(base + amp + 20);
  let dh = Math.round(base - amp - 13.7 * (h / 198));
  if (dh < 10) dh = 10;
  let dw = Math.floor(1.2 * dh);
  if (dw > w - 8) {
    dw = w - 8;
    dh = Math.round(dw / 1.2);
  }
  return {
    w,
    h,
    base,
    amp,
    boite,
    ep: 5.5 * k,
    r: 3.2 * k,
    esp: 11 * k,
    dalle: { x: Math.floor((w - dw) / 2), y: Math.round(0.0455 * h), w: dw, h: dh },
  };
}

// ── Q93 · QUAND LA DALLE ET LE CHAMP SE RENCONTRENT, C'EST LE CHAMP QUI CÈDE (sa clarté seule, en HSL, jusqu'à 42 d'écart) ──
const lum = (r: number, v: number, b: number): number => 0.2126 * r + 0.7152 * v + 0.0722 * b;
function rgbHsl(r0: number, v0: number, b0: number): [number, number, number] {
  const r = r0 / 255;
  const v = v0 / 255;
  const b = b0 / 255;
  const mx = Math.max(r, v, b);
  const mn = Math.min(r, v, b);
  let h = 0;
  let s = 0;
  const l = (mx + mn) / 2;
  const d = mx - mn;
  if (d) {
    s = l > 0.5 ? d / (2 - mx - mn) : d / (mx + mn);
    h = mx === r ? (v - b) / d + (v < b ? 6 : 0) : mx === v ? (b - r) / d + 2 : (r - v) / d + 4;
    h /= 6;
  }
  return [h, s, l];
}
function hslRgb(h: number, s: number, l: number): [number, number, number] {
  if (!s) {
    const g = Math.round(l * 255);
    return [g, g, g];
  }
  const f = (p: number, q: number, t0: number): number => {
    let t = t0;
    if (t < 0) t += 1;
    if (t > 1) t -= 1;
    if (t < 1 / 6) return p + (q - p) * 6 * t;
    if (t < 1 / 2) return q;
    if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
    return p;
  };
  const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
  const p = 2 * l - q;
  return [Math.round(f(p, q, h + 1 / 3) * 255), Math.round(f(p, q, h) * 255), Math.round(f(p, q, h - 1 / 3) * 255)];
}
/** la couleur du champ face à une dalle de clarté `Ld` (`champCede`) ; `cv` porte la décision (`data-cede` : clarté du champ, de la dalle, écart) */
export function champCede(natCol: string, Ld: number | null, cv: HTMLCanvasElement): string {
  if (Ld === null) {
    cv.removeAttribute('data-cede');
    return natCol;
  }
  const c = hex(natCol) as [number, number, number];
  const Lc = lum(c[0], c[1], c[2]);
  const note = (a: number): void => {
    cv.setAttribute('data-cede', [Math.round(a), Math.round(Ld), Math.round(Math.abs(a - Ld))].join(','));
  };
  if (Math.abs(Lc - Ld) >= 42) {
    note(Lc);
    return natCol;
  }
  const hsl = rgbHsl(c[0], c[1], c[2]);
  const pousse = (sens: number): { c: [number, number, number]; d: number; ok: boolean } => {
    let l = hsl[2];
    let best: [number, number, number] = c;
    let bd = -1;
    for (let k = 0; k < 90; k++) {
      l = Math.max(0.06, Math.min(0.94, l + sens * 0.01));
      const q = hslRgb(hsl[0], hsl[1], l);
      const d = Math.abs(lum(q[0], q[1], q[2]) - Ld);
      if (d > bd) {
        bd = d;
        best = q;
      }
      if (d >= 42) return { c: q, d, ok: true };
      if (l <= 0.06 || l >= 0.94) break;
    }
    return { c: best, d: bd, ok: false };
  };
  const haut = pousse(1);
  const bas = pousse(-1);
  const pris =
    haut.ok && bas.ok ? (Lc >= Ld ? haut : bas) : haut.ok ? haut : bas.ok ? bas : haut.d >= bas.d ? haut : bas;
  const f = pris.c;
  note(lum(f[0], f[1], f[2]));
  return `rgb(${String(f[0])},${String(f[1])},${String(f[2])})`;
}

/** ce qu'une carte porte : sa nature, son trait (mode, couleur), son champ et sa matière */
export interface EtatCarte {
  nat: NatureCarte;
  mode: ModeTrait;
  col: string;
  /** la hauteur de trait de la fiche (`_ficheEcran(…).base`) */
  base: number;
  /** pas de matière (un Cercle sans parole) : le champ reste, la dalle manque */
  sansMatiere?: boolean;
  /** les paroles d'un Cercle (Q213) : à partir de deux, toutes ses dalles, en petite Toile */
  mosa?: number[];
}

export function etatParole(p: Parole): EtatCarte {
  const t = traitFiche(p);
  const nat: NatureCarte = p.chiche ? 'chiche' : 'promi';
  return { nat, mode: t.mode, base: t.base, col: p.status === 'tenu' ? CRETE : NATTRAIT[nat] };
}

export type Rect4 = [number, number, number, number];
/**
 * LA PETITE TOILE D'UN CERCLE (Q213, `_petiteToile` de lot-REPERAGE) — ses dalles « occupent l'espace de la carte, réparties, comme une petite
 * Toile » : une case par dalle, tirée d'une suite déterministe (les ids), jamais devant le libellé ; chaque dalle rendue par le moteur à la taille de
 * sa case et posée 1:1. Rend les boîtes peintes (en pt de la carte), ou null.
 */
export function petiteToile(
  g: CanvasRenderingContext2D,
  facade: Facade,
  A: { x: number; y: number; w: number; h: number },
  Lr: { x: number; y: number; w: number; h: number },
  ids: number[],
): Rect4[] | null {
  const n = ids.length;
  if (n < 2) return null;
  const ratio = A.w / A.h;
  const cols = Math.max(1, Math.round(Math.sqrt(n * ratio * 1.25)));
  let rows = Math.ceil((n + 2) / cols);
  while (cols * rows < n + 3) rows++;
  const cw = A.w / cols;
  const ch = A.h / rows;
  const cells: Array<[number, number]> = [];
  for (let r = 0; r < rows; r++)
    for (let c = 0; c < cols; c++) {
      const cx = A.x + c * cw;
      const cy = A.y + r * ch;
      if (cx < Lr.x + Lr.w && cy < Lr.y + Lr.h) continue;
      cells.push([cx, cy]);
    }
  const h = (v: number, s: number): number => {
    let x = ((v * 2654435761) ^ (s * 40503)) >>> 0;
    x ^= x >>> 15;
    x = Math.imul(x, 2246822519) >>> 0;
    x ^= x >>> 13;
    return (x % 1000) / 1000;
  };
  const cle = ids.reduce((a, b) => a + b, 0);
  cells.sort((a, b) => h(Math.round(a[0] * 7 + a[1] * 13), cle) - h(Math.round(b[0] * 7 + b[1] * 13), cle));
  const pick = cells.slice(0, n).sort((a, b) => a[1] - b[1] || a[0] - b[0]);
  const T = g.getTransform();
  const sx = Math.hypot(T.a, T.b) || 1;
  const rects: Rect4[] = [];
  ids.forEach((pid, k) => {
    const cel = pick[k];
    if (!cel) return;
    const sz = Math.min(cw, ch) * (0.92 + 0.22 * h(pid, 3));
    const t = facade.rendreDalle(pid, sz * sx, sz * sx)?.cv;
    if (!t) return;
    const w = t.width / sx;
    const hh = t.height / sx;
    const jx = (h(pid, 1) - 0.5) * Math.max(0, cw - w) * 0.9;
    const jy = (h(pid, 2) - 0.5) * Math.max(0, ch - hh) * 0.9;
    const rx = cel[0] + (cw - w) / 2 + jx;
    let ry = cel[1] + (ch - hh) / 2 + jy;
    // rien devant le libellé : la BOÎTE peinte, bornée
    if (rx < Lr.x + Lr.w && rx + w > Lr.x && ry < Lr.y + Lr.h && ry + hh > Lr.y) ry = Lr.y + Lr.h;
    facade.poserUn(g, t, rx + w / 2, ry + hh / 2);
    rects.push([Math.round(rx), Math.round(ry), Math.round(w), Math.round(hh)]);
  });
  return rects.length ? rects : null;
}

/** un Cercle (`etatNuee`) : sa fiche a ses cotes (base 232 avec des paroles, 282 vide), son trait est entier (mode complet) */
export function etatCercle(ids: number[]): EtatCarte {
  const e: EtatCarte = { nat: 'nuee', mode: 'complet', base: ids.length ? 232 : 282, col: NATTRAIT.nuee, mosa: ids };
  if (!ids.length) e.sansMatiere = true;
  return e;
}

/** le texte et l'état d'une carte */
export interface TextesCarte {
  eb: string;
  titre: string;
  et: string;
}

export interface CfgCarte {
  facade: Facade;
  /** la parole dont on peint la dalle (sa photo la remplace, Q53) — null : aucune */
  p: Parole | null;
  /** la palette du Studio est Ingénu (Q297) */
  ingenu: boolean;
  /** se repeindre quand une photo a fini de charger */
  repeindre: () => void;
}

/** le trait, la matière et le champ d'une carte, dans son canevas (`peintCarte`) */
export function peindreCarte(cv: HTMLCanvasElement, g2: GeoCarte, e: EtatCarte, c: CfgCarte): void {
  const W = g2.w;
  const H = g2.h;
  const dpr = Math.max(2, Math.min(3, window.devicePixelRatio || 2));
  cv.width = Math.round(W * dpr);
  cv.height = Math.round(H * dpr);
  cv.style.width = `${String(W)}px`;
  cv.style.height = `${String(H)}px`;
  const g = cv.getContext('2d');
  if (!g) return;
  g.setTransform(dpr, 0, 0, dpr, 0, 0);
  g.clearRect(0, 0, W, H);
  g.imageSmoothingEnabled = true;
  g.imageSmoothingQuality = 'high';
  const y = onde(g2.base, g2.amp, W, 1);
  const id = c.p?.id ?? null;
  // la rampe de la PAROLE (`_ingenuRampe(id)` : sa nature — sur la carte d'un Cercle, celle de sa dernière parole)
  const rampe = c.ingenu && c.p ? { cols: RAMPE_INGENU[c.p.chiche ? 'chiche' : 'promi'], haut: 0.9 } : undefined;
  const o = rampe ? { rampe } : {};
  // 1 · le champ, borné en bas par l'onde — TOUJOURS (« un champ blanc n'existe jamais ») ; la dalle rendue d'abord, pour qu'il sache à quoi il se compare
  const Ld =
    !e.sansMatiere && id !== null ? c.facade.clarteDalle(id, g2.dalle.w * dpr, g2.dalle.h * dpr, o, true) : null;
  const champ = Ld !== null ? champCede(NATCOL[e.nat], Ld, cv) : NATCOL[e.nat];
  if (Ld === null) cv.removeAttribute('data-cede');
  g.beginPath();
  cheminOnde(g, y, 0, W, W, 1);
  g.lineTo(W, 0);
  g.lineTo(0, 0);
  g.closePath();
  g.fillStyle = champ;
  g.fill();
  cv.setAttribute('data-champ', champ);
  // 2 · la matière : la photo (dans la boîte de la dalle, couvrante), sinon la vraie dalle du moteur, à droite du libellé de nature (ou sous lui)
  cv.removeAttribute('data-matiere');
  cv.removeAttribute('data-matieres');
  let decl: { x: number; y: number; w: number; h: number } | null = null;
  const src = c.p ? photoDe(c.p) : null;
  const im = src ? imagePhoto(src, c.repeindre) : null;
  let ym = 1e9;
  for (let x = 0; x <= W; x += 4) ym = Math.min(ym, y(x));
  const mosa =
    e.mosa && e.mosa.length > 1
      ? petiteToile(
          g,
          c.facade,
          { x: 8, y: 8, w: W - 16, h: ym - 14 },
          { x: 0, y: 0, w: 10 + LARGEUR_LIB[e.nat] + 4, h: 36 },
          e.mosa,
        )
      : null;
  if (mosa) {
    cv.setAttribute('data-matieres', JSON.stringify(mosa));
    const x0 = Math.min(...mosa.map((r) => r[0]));
    const y0 = Math.min(...mosa.map((r) => r[1]));
    decl = {
      x: x0,
      y: y0,
      w: Math.max(...mosa.map((r) => r[0] + r[2])) - x0,
      h: Math.max(...mosa.map((r) => r[1] + r[3])) - y0,
    };
  } else if (im && im.width && im.height) {
    const b = g2.dalle;
    const r = im.width / im.height;
    const br = b.w / b.h;
    const [sw, sh, sx, sy] =
      r > br
        ? [im.height * br, im.height, (im.width - im.height * br) / 2, 0]
        : [im.width, im.width / br, 0, (im.height - im.width / br) / 2];
    g.drawImage(im, sx, sy, sw, sh, b.x, b.y, b.w, b.h);
    decl = b;
  } else if (!e.sansMatiere && id !== null && Ld !== null) {
    const b0 = g2.dalle;
    const dx = Math.max(0, 10 + LARGEUR_LIB[e.nat] + 8 - b0.x);
    const dy = Math.max(0, 38 - b0.y);
    // carte étroite (trois par ligne) : le libellé mangerait la largeur — la dalle descend sous lui
    const b =
      b0.w - dx >= b0.w * 0.5
        ? { x: b0.x + dx, y: b0.y, w: b0.w - dx, h: b0.h }
        : { x: b0.x, y: b0.y + dy, w: b0.w, h: Math.max(12, b0.h - dy) };
    const r = c.facade.poserDalle(g, id, b.x, b.y, b.w, b.h, o, true);
    if (r)
      decl = {
        x: Math.round(b.x + (b.w - r.w) / 2),
        y: Math.round(b.y + (b.h - r.h) / 2),
        w: Math.round(r.w),
        h: Math.round(r.h),
      };
  }
  if (decl) cv.setAttribute('data-matiere', [decl.x, decl.y, decl.w, decl.h].join(','));
  // 3 · la ligne (§2.6) : la couleur d'état, jamais celle de la nature
  const col = e.col;
  const ep = g2.ep;
  const rr = g2.r;
  const esp = g2.esp;
  const mid = W / 2;
  g.strokeStyle = col;
  g.fillStyle = col;
  g.lineWidth = ep;
  g.lineCap = 'round';
  g.lineJoin = 'round';
  const plein = (a: number, b: number): void => {
    g.beginPath();
    cheminOnde(g, y, a, b, W, 1);
    g.stroke();
  };
  const points = (x0: number): void => {
    for (let x = x0; x < W - rr; x += esp) {
      g.beginPath();
      g.arc(x, y(x), rr, 0, 6.2832);
      g.fill();
    }
  };
  if (e.mode === 'complet') plein(0, W);
  else if (e.mode === 'duo') {
    const gp = 4 * (W / 173);
    plein(0, mid - gp);
    plein(mid + gp, W);
  } else if (e.mode === 'points') {
    const cx = W * 0.11;
    ruban(g, y, -W * 0.03, cx + ep * 0.6, ep * 2.2, ep * 0.15);
    g.fill();
    chevron(g, y, cx, ep, col);
    points(cx + esp * 1.3);
  } else {
    plein(0, mid);
    chevron(g, y, mid, ep, col);
    points(mid + esp);
  }
  cv.setAttribute('data-trait', [g2.base, g2.amp, col, e.mode, 'carte', W, ep, rr, esp].join(','));
}

/** les cotes d'une densité : deux cartes par ligne (165 × 198), ou trois (106 × 133) */
export interface Densite {
  CW: number;
  CH: number;
  RAD: number;
  GX: number[];
  PAS: number;
  FEB: number;
  FTI: number;
  FET: number;
  PADX: number;
  TXW: number;
  DY_EB: number;
  DY_TI: number;
  BAS_TI: number;
}
export const DEUX: Densite = {
  CW: 165,
  CH: 198,
  RAD: 17,
  GX: [24, 201],
  PAS: 210,
  FEB: 16,
  FTI: 24,
  FET: 13,
  PADX: 12,
  TXW: 140,
  DY_EB: 10.5,
  DY_TI: 17,
  BAS_TI: 24,
};

/**
 * A3, L0 §2 : la vraie app s'adapte à l'écran — deux cartes par rangée, 24 pt des bords, 12 pt entre elles ; à 390 de large, exactement `DEUX`
 * (165 de large, colonnes à 24 et 201, le texte sur 140).
 */
export function deux(largeur: number): Densite {
  const CW = (largeur - 60) / 2;
  return { ...DEUX, CW, GX: [24, 36 + CW], TXW: CW - 25 };
}

/** la carte : son nœud (`.s4-carte`), son canevas peint, ses textes ; le titre est ajusté une fois posé (`ajusterTitre`) */
export function carte(
  D: Densite,
  e: EtatCarte,
  t: TextesCarte,
  c: CfgCarte,
  o: { tenue: boolean; garde: boolean; clair: boolean },
): HTMLElement {
  const tenue = o.tenue;
  const g2 = geoCarte(D.CW, D.CH, e.base);
  const d = document.createElement('div');
  d.className = 's4-carte';
  d.style.width = `${String(D.CW)}px`;
  d.style.height = `${String(D.CH)}px`;
  d.style.borderRadius = `${String(D.RAD)}px`;
  d.style.background = tenue ? palette.prune09 : CORPS[e.nat];
  d.setAttribute('data-nat', e.nat);
  // C-149 suite (v163) : un gardé de côté se reconnaît au premier coup d'œil — un pointillé de 3 pt DEDANS, le violet « en cours » en clair, son
  // clair en sombre (la couleur de la nature s'y confondait avec le champ)
  if (o.garde) {
    const gc = o.clair ? palette.mauve12 : palette.gardeSombre;
    d.style.outline = `3px dashed ${gc}`;
    d.style.outlineOffset = '-3px';
    d.setAttribute('data-garde-trait', gc);
  }
  const yEb = Math.round(g2.boite - D.DY_EB);
  const yTi = yEb + D.DY_TI;
  const etCol = tenue ? palette.menthe82 : e.nat === 'nuee' ? palette.mauve77 : palette.creme95;
  d.innerHTML =
    '<canvas></canvas>' +
    `<div class="s4-natlab" style="color:${NATTXT[e.nat]}">${MOT_NAT[e.nat]}</div>` +
    `<div class="s4-eb" style="left:${String(D.PADX)}px;top:${String(yEb)}px;width:${String(D.TXW)}px">${esc(t.eb)}</div>` +
    `<div class="s4-ti" style="left:${String(D.PADX)}px;top:${String(yTi)}px;width:${String(D.TXW)}px;height:${String(Math.max(0, D.CH - D.BAS_TI - yTi))}px">${esc(t.titre)}</div>` +
    `<div class="s4-et" style="left:${String(D.PADX)}px;width:${String(D.TXW)}px;color:${etCol}">${esc(t.et)}</div>`;
  const cv = d.querySelector('canvas')!;
  peindreCarte(cv, g2, e, c);
  return d;
}

/**
 * Q158, 16 sept. — L'ÉTAT TIENT DANS SA CARTE (`etatsDeCarte`) : s'il déborde, sa taille descend par pas de 0,5 jusqu'à 12 (le plancher du §6) ;
 * s'il faut encore gagner, c'est l'interlettre qui cède, par pas de 0,01 em, jusqu'à 0,12 em (« 9 PROMI · 3 TENUS »). La carte doit être posée.
 */
export function ajusterEtat(d: HTMLElement): void {
  const n = d.querySelector<HTMLElement>('.s4-et');
  if (!n || !n.clientWidth) return;
  n.style.removeProperty('font-size');
  n.style.removeProperty('letter-spacing');
  let t = parseFloat(getComputedStyle(n).fontSize);
  if (!t || n.scrollWidth <= n.clientWidth + 1) return;
  for (let g = 0; n.scrollWidth > n.clientWidth + 1 && t > 12 && g < 16; g++) {
    t -= 0.5;
    n.style.fontSize = `${String(t)}px`;
  }
  if (n.scrollWidth > n.clientWidth + 1) {
    let em = parseFloat(getComputedStyle(n).letterSpacing) / t;
    if (!isFinite(em)) em = 0.18;
    for (let h = 0; n.scrollWidth > n.clientWidth + 1 && em > 0.12 && h < 12; h++) {
      em -= 0.01;
      n.style.letterSpacing = `${em.toFixed(3)}em`;
    }
  }
}

/**
 * C-151, v203 — LE TITRE NE TOUCHE JAMAIS L'ÉTAT (`_s4TitresAjuste`) : il part de 24 et rétrécit d'un point à la fois tant qu'il déborde de sa boîte
 * ou que le bas de ses lignes passe à moins de 2 pt du mot d'état ; plancher 13 (12 sur une carte étroite) ; au plancher, s'il déborde encore, il
 * s'arrête par « … » à la dernière ligne qui tient au-dessus de l'état. La carte doit être posée (dans le document, visible).
 */
export function ajusterTitre(d: HTMLElement, depart: number): void {
  const t = d.querySelector<HTMLElement>('.s4-ti');
  const et = d.querySelector<HTMLElement>('.s4-et');
  if (!t || !t.clientHeight) return;
  for (const p of ['display', '-webkit-box-orient', '-webkit-line-clamp', 'overflow', 'line-height'])
    t.style.removeProperty(p);
  const hBoite = t.dataset['h'] ?? t.style.height;
  t.dataset['h'] = hBoite;
  t.style.height = hBoite;
  const R = document.createRange();
  const k = t.getBoundingClientRect().width / (t.offsetWidth || 1) || 1;
  const deborde = (): boolean => {
    if (t.scrollHeight > t.clientHeight + 1) return true;
    if (!et) return false;
    R.selectNodeContents(t);
    return R.getBoundingClientRect().bottom > et.getBoundingClientRect().top - 2 * k;
  };
  let fs = depart;
  t.style.fontSize = `${String(fs)}px`;
  if (!deborde()) return;
  const sol = d.getBoundingClientRect().width / k < 120 ? 12 : 13;
  for (let n = 0; n < 14 && fs > sol && deborde(); n++) {
    fs -= 1;
    t.style.fontSize = `${String(fs)}px`;
  }
  if (deborde() && et) {
    const lim = et.getBoundingClientRect().top - 2 * k;
    const lh = 1.2 * fs;
    const N = Math.max(1, Math.floor((lim - t.getBoundingClientRect().top) / (lh * k) + 0.001));
    t.style.lineHeight = '1.2';
    t.style.height = `${String(N * lh)}px`;
    t.style.display = '-webkit-box';
    t.style.setProperty('-webkit-box-orient', 'vertical');
    t.style.setProperty('-webkit-line-clamp', String(N));
    t.style.overflow = 'hidden';
  }
}

/**
 * LA PASTILLE « PAS ENCORE VU » d'une carte (v89, Q347 ; C-253 : un mot neuf l'allume aussi) : un disque de 9 pt, #FB4C0D, cerné d'un filet
 * crème de 1,4 pt, à 10 pt du coin haut droit ; elle s'ouvre sur son centre (`v201pop`, 0,26 s).
 */
export function poserPastille(d: HTMLElement): void {
  if (d.querySelector(':scope > .s4-att')) return;
  d.appendChild(el('i', { class: 's4-att', 'aria-hidden': 'true' }));
}
