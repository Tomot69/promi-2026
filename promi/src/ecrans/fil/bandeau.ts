/**
 * LE BANDEAU DU FIL (PROMI-SPECIFICATIONS §3.10, cadre 76 ; le prototype : `_s4Fil` et `peintBandeau` de lot-S4) — 358 × 128, rayon 22 : à
 * gauche la matière (143 pt) bordée d'un trait VERTICAL (la même onde, tournée d'un quart de tour, ses coefficients relevés sur le cadre 76 :
 * base 121, montée 4,3, sinus 8,425, une période), à droite l'événement, le titre, l'état. Construit comme la fiche (C-147), dans les deux thèmes.
 */
import type { Facade } from '../../moteur/facade.ts';
import type { Parole } from '../../donnees/schema.ts';
import { palette } from '../../design/jetons.ts';
import { esc } from '../commun.ts';
import { photoDe } from '../fiche/photo.ts';
import { imagePhoto } from '../photo/peinture.ts';
import {
  champCede,
  CORPS,
  LARGEUR_LIB,
  MOT_NAT,
  NATCOL,
  NATTXT,
  petiteToile,
  RAMPE_INGENU,
  type EtatCarte,
} from '../index/carte.ts';

export const BANDEAU = { X: 16, W: 358, H: 128, PAS: 140, CX: 143 } as const;

/** le visage d'un événement qui vient de quelqu'un (`_visSvg`) : une silhouette crème sur le champ de la nature */
function visage(d: number): string {
  const f = (v: number): string => v.toFixed(2);
  const x0 = d / 2 - 0.3 * d;
  const x1 = d / 2 + 0.3 * d;
  const ye = 0.98 * d;
  return (
    `<svg viewBox="0 0 ${String(d)} ${String(d)}" xmlns="http://www.w3.org/2000/svg">` +
    `<circle cx="${String(d / 2)}" cy="${f((0.78 * d) / 2)}" r="${f(0.19 * d)}" fill="${palette.creme95}"/>` +
    `<path d="M${f(x0)} ${f(ye)} A${f(0.3 * d)} ${f(0.27 * d)} 0 0 1 ${f(x1)} ${f(ye)} Z" fill="${palette.creme95}"/></svg>`
  );
}

export interface TextesBandeau {
  ev: string;
  titre: string;
  et: string;
  /** l'événement vient de quelqu'un d'autre : son visage */
  vis: boolean;
}

/** la matière et le trait du bandeau, dans son canevas (`peintBandeau`) */
function peindre(
  cv: HTMLCanvasElement,
  e: EtatCarte,
  facade: Facade,
  p: Parole | null,
  ingenu: boolean,
  repeindre: () => void,
): void {
  const W = BANDEAU.CX;
  const H = BANDEAU.H;
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
  const bx = 121.0;
  const mont = 4.3;
  const a = 8.425;
  const x = (t: number): number => {
    const u = Math.max(0, Math.min(1, t / H));
    return bx - mont * u - a * Math.sin(2 * Math.PI * u);
  };
  const trace = (y0: number, y1: number): void => {
    g.beginPath();
    g.moveTo(x(y0), y0);
    for (let yy = y0; yy <= y1; yy += 2) g.lineTo(x(yy), yy);
    g.lineTo(x(y1), y1);
  };
  // la dalle d'abord, le champ cède ensuite (Q93) ; rendue par le moteur à la taille de sa boîte (110 × 80), la rampe de sa nature sous Ingénu
  const id = p?.id ?? null;
  const o = ingenu && p ? { rampe: { cols: RAMPE_INGENU[p.chiche ? 'chiche' : 'promi'], haut: 0.9 } } : undefined;
  const src = !e.sansMatiere && id !== null ? facade.rendreDalle(id, 110 * dpr, 80 * dpr, o) : null;
  const champ = src && src.lum !== null ? champCede(NATCOL[e.nat], src.lum, cv) : NATCOL[e.nat];
  trace(0, H);
  g.lineTo(0, H);
  g.lineTo(0, 0);
  g.closePath();
  g.fillStyle = champ;
  g.fill();
  cv.setAttribute('data-champ', champ);
  cv.setAttribute('data-matiere', '5,40,110,80');
  const ph = p ? photoDe(p) : null;
  const im = ph ? imagePhoto(ph, repeindre) : null;
  if (e.mosa && e.mosa.length > 1) {
    let xm = 1e9;
    for (let yy = 0; yy <= H; yy += 4) xm = Math.min(xm, x(yy));
    petiteToile(
      g,
      facade,
      { x: 6, y: 6, w: xm - 12, h: H - 12 },
      { x: 0, y: 0, w: 10 + LARGEUR_LIB[e.nat] + 4, h: 36 },
      e.mosa,
    );
  } else if (im && im.width && im.height) {
    const b = { x: 5, y: 19, w: 110, h: 89 };
    const r = im.width / im.height;
    const br = b.w / b.h;
    const [sw, sh, sx, sy] =
      r > br
        ? [im.height * br, im.height, (im.width - im.height * br) / 2, 0]
        : [im.width, im.width / br, 0, (im.height - im.width / br) / 2];
    g.drawImage(im, sx, sy, sw, sh, b.x, b.y, b.w, b.h);
  } else if (src) facade.poserUn(g, src.cv, 5 + 110 / 2, 40 + 80 / 2);
  // le trait vertical : entier pour une parole tenue (ou tenue à deux), sinon la moitié pleine puis des points (r 3,4 tous les 13)
  g.strokeStyle = e.col;
  g.fillStyle = e.col;
  g.lineWidth = 7;
  g.lineCap = 'round';
  g.lineJoin = 'round';
  if (e.mode === 'complet' || e.mode === 'duo') {
    trace(0, H);
    g.stroke();
  } else {
    trace(0, H / 2);
    g.stroke();
    for (let yy = 77; yy < H; yy += 13) {
      g.beginPath();
      g.arc(x(yy), yy, 3.4, 0, 6.2832);
      g.fill();
    }
  }
  cv.setAttribute('data-trait-v', [bx, mont, a, H, e.col, e.mode, 7, 3.4, W].join(','));
}

/** le bandeau : son nœud (`.s4-carte.fil-b`), son canevas peint, ses textes ; le titre est posé une fois le bandeau dans le document (`poserTitre`) */
export function bandeau(
  e: EtatCarte,
  t: TextesBandeau,
  c: { facade: Facade; p: Parole | null; ingenu: boolean; repeindre: () => void; largeur?: number },
): HTMLElement {
  const tenue = /^TENU/.test(t.et);
  const d = document.createElement('div');
  d.className = 's4-carte fil-b';
  // A3 : large de l'écran moins 16 de chaque côté (358 à 390)
  d.style.width = `${String(c.largeur ?? BANDEAU.W)}px`;
  d.style.height = `${String(BANDEAU.H)}px`;
  d.style.background = tenue ? palette.prune09 : CORPS[e.nat];
  d.setAttribute('data-nat', e.nat);
  const etCol = tenue ? palette.menthe82 : e.nat === 'nuee' ? palette.mauve77 : palette.creme95;
  d.innerHTML =
    '<canvas></canvas>' +
    `<div class="s4-natlab" style="color:${NATTXT[e.nat]}">${MOT_NAT[e.nat]}</div>` +
    '<div class="s4-ev">' +
    (t.vis ? `<span class="s4-vis" style="background:${NATCOL[e.nat]}">${visage(26)}</span>` : '') +
    `<span class="s4-nom">${esc(t.ev)}</span></div>` +
    `<div class="s4-ti">${esc(t.titre)}</div>` +
    `<div class="s4-et" style="color:${etCol}">${esc(t.et)}</div>`;
  peindre(d.querySelector('canvas')!, e, c.facade, c.p, c.ingenu, c.repeindre);
  return d;
}

/**
 * LE TITRE D'UN BANDEAU (Tom, 23 sept. : « rends-lui sa taille d'origine, remonte-le, et au-delà de deux lignes coupe avec des points de suite.
 * Jamais de réduction de taille ») : sa taille ne bouge pas ; il finit à 92, l'état à 98 ; à deux lignes il grandit VERS LE HAUT (42 → 50) et
 * l'événement monte avec lui, jusqu'à 8 pt du bord ; au-delà de deux lignes, « … ». Un titre d'une ligne ne bouge pas d'un pixel.
 */
export function poserTitre(d: HTMLElement): void {
  const t = d.querySelector<HTMLElement>('.s4-ti');
  const ve = d.querySelector<HTMLElement>('.s4-ev');
  if (!t) return;
  const BAS = 92;
  const GAP = 6;
  const HEV = 28;
  const HAUT_MIN = 8;
  const H0 = 42;
  const LH = 1.04;
  const MAXL = 2;
  const fs = parseFloat(getComputedStyle(t).fontSize) || 24;
  t.style.display = 'block';
  t.style.height = 'auto';
  t.style.removeProperty('-webkit-line-clamp');
  const voulu = Math.ceil(t.scrollHeight) || 0;
  const ligne = fs * LH;
  const n = Math.max(1, Math.round(voulu / ligne));
  let h = Math.max(H0, Math.ceil(Math.min(n, MAXL) * ligne));
  h = Math.min(h, BAS - HAUT_MIN - GAP - HEV);
  t.style.height = `${String(h)}px`;
  t.style.top = `${String(BAS - h)}px`;
  if (ve) ve.style.top = `${String(Math.max(HAUT_MIN, BAS - h - GAP - HEV))}px`;
  t.style.display = '-webkit-box';
  t.style.setProperty('-webkit-box-orient', 'vertical');
  t.style.setProperty('-webkit-line-clamp', String(MAXL));
}
