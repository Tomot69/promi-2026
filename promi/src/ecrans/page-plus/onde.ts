/**
 * L'ONDE (SPEC-ECRANS §0, CLAUDE.md §2.1) — une seule formule, partout : y(t) = base − amp·0,34·t − amp·0,62·sin(2π·1,5·t), t = x / largeur.
 * Le chemin est fait de cubiques, un segment par quart de période, aux tangentes exactes (la pente lue à ± 0,5 pt) : c'est ainsi que le
 * prototype la peint, et le bord du champ en dépend au pixel.
 */
export type Onde = (x: number) => number;

export function onde(base: number, amp: number, largeur = 390, periode = 1.5): Onde {
  const mont = amp * 0.34;
  const a = amp * 0.62;
  return (x) => {
    const t = Math.max(0, Math.min(1, x / largeur));
    return base - mont * t - a * Math.sin(2 * Math.PI * periode * t);
  };
}

/** le tracé de l'onde de x0 à x1 (moveTo puis cubiques), dans le contexte donné */
export function cheminOnde(g: CanvasRenderingContext2D, y: Onde, x0: number, x1: number, largeur = 390): void {
  const seg = largeur / 6;
  const d = (x: number): number => y(x + 0.5) - y(x - 0.5);
  const xs = [x0];
  let k = Math.ceil(x0 / seg) * seg;
  while (k < x1 - 0.5) {
    xs.push(k);
    k += seg;
  }
  xs.push(x1);
  g.moveTo(xs[0]!, y(xs[0]!));
  for (let i = 0; i < xs.length - 1; i++) {
    const a = xs[i]!;
    const b = xs[i + 1]!;
    const h = (b - a) / 3;
    g.bezierCurveTo(a + h, y(a) + d(a) * h, b - h, y(b) - d(b) * h, b, y(b));
  }
}

/** le point le plus bas de l'onde (sa plus grande ordonnée), lu tous les 3 pt comme le prototype (`hzCible`) */
export function basOnde(y: Onde, largeur = 390): number {
  let b = -1e9;
  for (let x = 0; x <= largeur; x += 3) b = Math.max(b, y(x));
  return b;
}
