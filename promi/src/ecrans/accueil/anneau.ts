/**
 * L'ANNEAU DU + DE L'ACCUEIL (v18, C-210 v173) — deux arcs nets au plus, tenu `#00341A` puis en cours `#291547`, dans la proportion des
 * paroles (ni gardées de côté, ni demandées), partant de midi dans le sens des aiguilles, un jour de 3 px d'arc entre eux ; sans filet
 * (v135, C-059). Le calcul de `plusAnneau` (lot-V16 du prototype), au caractère près : la même image SVG pour les mêmes nombres.
 */
import { palette } from '../../design/jetons.ts';

export interface CompteAnneau {
  tenues: number;
  enCours: number;
}

/** D : le diamètre du + (72) ; w : l'épaisseur de l'anneau (l'écart entre le bord et le disque, 13,5) */
export function anneauSvg(n: CompteAnneau, D = 72, w = 13.5): string {
  const tot = n.tenues + n.enCours;
  const parts = (
    [
      [n.tenues, palette.menthe11],
      [n.enCours, palette.mauve12],
    ] as Array<[number, string]>
  ).filter((x) => x[0] > 0);
  const c = D / 2;
  const rm = c - w / 2;
  const GJ = parts.length > 1 ? 3 / rm : 0.002;
  let a = -Math.PI / 2 + GJ / 2;
  const P = (R: number, q: number): string => (c + R * Math.cos(q)).toFixed(2) + ' ' + (c + R * Math.sin(q)).toFixed(2);
  const arc = (R: number, a0: number, a1: number): string =>
    'M' + P(R, a0) + ' A' + R.toFixed(2) + ' ' + R.toFixed(2) + ' 0 ' + (a1 - a0 > Math.PI ? 1 : 0) + ' 1 ' + P(R, a1);
  let out = '';
  for (const [k, col] of parts) {
    const L = (k / tot) * 2 * Math.PI;
    const a1 = a + L - GJ;
    out += '<path d="' + arc(rm, a, a1) + '" fill="none" stroke="' + col + '" stroke-width="' + String(w) + '"/>';
    a += L;
  }
  return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + String(D) + ' ' + String(D) + '">' + out + '</svg>';
}

/** la valeur CSS de `--anneau` : l'image, comme le prototype la pose (`url("data:image/svg+xml;utf8,…")`) */
export function anneauCss(n: CompteAnneau): string {
  return 'url("data:image/svg+xml;utf8,' + encodeURIComponent(anneauSvg(n)) + '")';
}
