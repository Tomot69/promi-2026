/**
 * LE TRAIT D'UNE FICHE (SPEC-GESTE §2.6 ; le prototype : `ligne()` de `_ficheTrait`, lot-S1B-geo, et `_partsPeint`, lot-V145-PARTS) — sur l'onde
 * de la fiche, selon son mode : `moitie` (ma moitié plantée, orange jusqu'au chevron du milieu, puis les points à tracer), `complet` (la parole
 * tenue : la crête pleine), `duo` (tenu à deux : deux moitiés séparées de 8 pt), et, à plusieurs (C-115), la seconde moitié en parts. Aucun
 * filet (C-059, v135). Le trait est une FONCTION de (base, amp) : la jonction (lot 3a-3) le retrace aplati par ce même code.
 */
import { cheminOnde, onde, type Onde } from '../page-plus/onde.ts';
import { chevron, ORANGE_DEPART, TRAIT_K, TRAIT_PTS } from '../page-plus/trait.ts';
import type { EtatParts, ModeTrait } from '../../metier/fiche.ts';
import { palette } from '../../design/jetons.ts';

export const W = 390;
/** la crête : le trait d'une parole tenue (`CRETE`) */
export const CRETE = palette.crete27;
const ECART_PARTS = 14;
const FIN = 2.5;
const MAX_INITIALES = 4;

export interface LigneFiche {
  mode: ModeTrait;
  /** la teinte du trait : sombre de la nature (`NATTRAIT`), ou la crête */
  col: string;
  /** les points à tracer d'une fiche qui attend un geste (Ø 12 × 1,15) — sinon Ø 9 × 1,15 */
  attend: boolean;
  /** à plusieurs (C-115) : l'état des parts, et leurs initiales (ou le compte) ; `encre` : la couleur du compte */
  parts?: { S: EtatParts; initiales: string[]; encre: string } | undefined;
  /** pendant le geste (lot 3a-2) : l'abscisse du doigt */
  doigt?: number | undefined;
}

/** la ligne de la fiche, peinte dans `g` (en pt 390), sur l'onde (base, amp) */
export function peindreLigne(g: CanvasRenderingContext2D, base: number, amp: number, l: LigneFiche): void {
  const y = onde(base, amp);
  const ep = 10 * TRAIT_K;
  const rr = 4.5 * TRAIT_PTS;
  const esp = 18;
  const mid = W / 2;
  g.save();
  g.strokeStyle = l.col;
  g.fillStyle = l.col;
  g.lineWidth = ep;
  g.lineCap = 'round';
  g.lineJoin = 'round';
  const plein = (a: number, b: number, c = l.col): void => {
    g.strokeStyle = c;
    g.beginPath();
    cheminOnde(g, y, a, b, W);
    g.stroke();
    g.strokeStyle = l.col;
  };
  const points = (x0: number): void => {
    g.fillStyle = l.col;
    const rp = l.attend ? 6 * TRAIT_PTS : rr;
    for (let x = x0; x < W - rr; x += esp) {
      g.beginPath();
      g.arc(x, y(x), rp, 0, 6.2832);
      g.fill();
    }
  };
  if (l.mode === 'complet') plein(0, W);
  else if (l.mode === 'duo') {
    plein(0, mid - 4);
    plein(mid + 4, W);
  } else if (l.parts) peindreParts(g, y, l, ep, plein);
  else {
    plein(0, mid - ep * 0.15, ORANGE_DEPART);
    const dg = l.doigt != null ? Math.max(mid, Math.min(l.doigt, W - ep)) : mid;
    if (dg > mid + 0.5) plein(mid - ep * 0.15, dg - ep * 0.15);
    chevron(g, y, dg, ep);
    points(dg + esp);
  }
  g.restore();
}

function peindreParts(
  g: CanvasRenderingContext2D,
  y: Onde,
  l: LigneFiche,
  ep: number,
  plein: (a: number, b: number, c?: string) => void,
): void {
  const { S, initiales, encre } = l.parts!;
  const mid = W / 2;
  plein(0, mid);
  const x0 = mid + ECART_PARTS;
  const L = (W - x0 - (S.n - 1) * ECART_PARTS) / S.n;
  const X: Array<[number, number]> = [];
  for (let i = 0; i < S.n; i++) {
    const a = x0 + i * (L + ECART_PARTS);
    const b = i === S.n - 1 ? W + ep : a + L;
    X.push([a, Math.min(b, W)]);
    if (S.faites.includes(S.T[i]!)) plein(a + ep / 2, i === S.n - 1 ? b : b - ep / 2, CRETE);
    else {
      g.save();
      g.lineWidth = FIN;
      g.lineCap = 'round';
      g.beginPath();
      cheminOnde(g, y, a + FIN / 2, i === S.n - 1 ? W : b - FIN / 2, W);
      g.stroke();
      g.restore();
    }
  }
  if (S.moi && !S.moiFait) {
    plein(0, mid - ep * 0.15, ORANGE_DEPART);
    chevron(g, y, mid, ep);
  }
  g.save();
  g.font = '700 12px Gilbert, system-ui, sans-serif';
  g.textAlign = 'center';
  g.textBaseline = 'alphabetic';
  const pose = (txt: string, xc: number, col: string): void => {
    const an = Math.atan2(y(xc + 6) - y(xc - 6), 12);
    g.save();
    g.translate(xc, y(xc));
    g.rotate(an);
    g.fillStyle = col;
    (g as unknown as { letterSpacing: string }).letterSpacing = '0.6px';
    g.fillText(txt, 0, ep / 2 + 17.5);
    g.restore();
  };
  if (S.n <= MAX_INITIALES) {
    for (let i = 0; i < S.n; i++)
      if (S.faites.includes(S.T[i]!)) pose(initiales[i]!, (X[i]![0] + X[i]![1]) / 2, palette.menthe82);
  } else pose(String(S.faites.length) + ' SUR ' + String(S.n), (x0 + W) / 2, encre);
  g.restore();
}
