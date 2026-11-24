/**
 * « LA DALLE D'ORIGINE » DANS LA BANDE HAUTE D'UNE FICHE (v118, Q365 tranchée ; le prototype : `_origineBande` de lot-V118-ORIGINE).
 *
 * « Avec La dalle d'origine, la bande haute de la fiche prend la couleur d'origine, sauf si elle passe sous le seuil de redteam_tonsurton face au
 * champ. Dans ce cas seulement, la rampe de Q30 s'applique. » Le seuil : ΔE 15 (CIELAB), entre le Lab MOYEN de la dalle rendue dans son monde de
 * plantation (déclaré par le moteur) et la couleur du champ (la nature).
 */
export const SEUIL_ORIGINE = 15;

function lin(c: number): number {
  const v = c / 255;
  return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
}
function f(t: number): number {
  return t > 0.008856 ? Math.cbrt(t) : 7.787 * t + 16 / 116;
}

/** le Lab (D65) d'une couleur `#rrggbb` — la formule du prototype, telle quelle */
export function labDe(hex: string): [number, number, number] | null {
  const m = /^#?([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i.exec(hex.trim());
  if (!m) return null;
  const r = lin(parseInt(m[1]!, 16));
  const g = lin(parseInt(m[2]!, 16));
  const b = lin(parseInt(m[3]!, 16));
  const x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047;
  const y = 0.2126729 * r + 0.7151522 * g + 0.072175 * b;
  const z = (0.0193339 * r + 0.119192 * g + 0.9503041 * b) / 1.08883;
  return [116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))];
}

/** la dalle d'origine garde sa couleur (vrai) ou prend la rampe de sa nature (faux : elle se confondrait avec le champ) ; null sans mesure */
export function origineGardee(
  labDalle: readonly number[] | null,
  champ: string,
): { dE: number; origine: boolean } | null {
  const F = labDe(champ);
  if (!labDalle || labDalle.length < 3 || !F) return null;
  const d = Math.hypot(labDalle[0]! - F[0], labDalle[1]! - F[1], labDalle[2]! - F[2]);
  return { dE: d, origine: d >= SEUIL_ORIGINE };
}
