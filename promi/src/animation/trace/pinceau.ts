/**
 * LA MATIÈRE DU TRAIT — LES DOUZE PINCEAUX (le prototype : `_matiereTrait` et `_PINCEAU_TRACES` de lot-PINCEAU, Q128, C-196).
 *
 * Les douze tracés viennent de la planche (PLANCHE-DOUZE-TRAITS), relevés tels quels du prototype dans un JSON engendré
 * (`outils/reprendre.py`, `src/animation/repris/pinceaux-traces.json` : jamais retouché). Ils sont posés sur l'onde du §2.1 (base 560,
 * amplitude 36) : on reporte leur LIGNE MOYENNE sur l'onde de l'écran, jamais leur boîte —
 *     Y(x) = y_planche(x) − onde(560, 36)(x) + onde(base, amp)(x)
 * la matière garde son épaisseur et son grain ; seule la vague sous elle change. La coupe à [x0, x1] est franche (le chevron marque la frontière).
 */
import DONNEES from '../repris/pinceaux-traces.json';

type Trace = number[];
const TRACES = DONNEES.traces as Record<string, Trace[]>;
/** [nom, libre (1) ou de Ma Parole ! (0), ce que fait la matière] */
export const PINCEAUX_META = DONNEES.meta as Array<[string, number, string]>;

const W = 390;
const BASE_P = 560;
const AMP_P = 36;
function ondeP(x: number): number {
  const t = Math.max(0, Math.min(1, x / W));
  return BASE_P - AMP_P * 0.34 * t - AMP_P * 0.62 * Math.sin(2 * Math.PI * 1.5 * t);
}

/** un nom de pinceau connu, sinon « Plein » (jamais du vide : `promiPinceau` du prototype) */
export function nomPinceau(n: unknown): string {
  return typeof n === 'string' && n in TRACES ? n : 'Plein';
}

/**
 * la matière du pinceau `nom`, peinte dans `g` (en pt 390) sur l'onde `yc`, coupée à [x0, x1], à la couleur `col` ;
 * rend faux si le pinceau n'a pas de tracé (rien n'est peint)
 */
export function matiereTrait(
  g: CanvasRenderingContext2D,
  nom: string,
  yc: (x: number) => number,
  x0: number,
  x1: number,
  col: string,
): boolean {
  const T = TRACES[nom];
  if (!T || !T.length) return false;
  const Y = (x: number, y: number): number => y - ondeP(x) + yc(x);
  g.save();
  g.beginPath();
  g.rect(x0, 0, x1 - x0, 900);
  g.clip();
  g.fillStyle = col;
  g.strokeStyle = col;
  g.lineCap = 'round';
  g.lineJoin = 'round';
  for (const p of T) {
    if (p[0] === 0) {
      // un contour plein : M/L/Z
      g.beginPath();
      for (let k = 1; k < p.length; k += 2) {
        const x = p[k]!;
        const y = Y(x, p[k + 1]!);
        if (k === 1) g.moveTo(x, y);
        else g.lineTo(x, y);
      }
      g.closePath();
      g.fill();
    } else if (p[0] === 1) {
      // une barre : x1 y1 x2 y2 épaisseur
      g.lineWidth = p[5]!;
      g.beginPath();
      g.moveTo(p[1]!, Y(p[1]!, p[2]!));
      g.lineTo(p[3]!, Y(p[3]!, p[4]!));
      g.stroke();
    } else if (p[0] === 2) {
      // un grain, une perle, une goutte
      g.beginPath();
      g.arc(p[1]!, Y(p[1]!, p[2]!), p[3]!, 0, 6.2832);
      g.fill();
    }
  }
  g.restore();
  return true;
}
