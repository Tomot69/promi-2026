/**
 * C-239 (v181a) — « un toucher ouvre la dalle de parole la plus proche si elle est à 22 pt ou moins du doigt ; deux à égale distance :
 * aucune ; seulement une dalle de moins de 44 pt ; rien ne change à l'écran ; le moteur n'est pas touché ». Porté de `_toucheTolerant`
 * (app.html ≈ l. 7228) : des cercles de 1 en 1 pt (40 points), lus par le toucher du moteur (lecture seule) ; une seconde dalle à 3 pt
 * près : égale distance ; la taille d'une dalle : le plus grand carré qu'elle contient, par pas de 2 pt.
 */
import type { DalleTouchee } from '../moteur/facade.ts';

export function toucheTolerant(
  hit: (x: number, y: number) => DalleTouchee | null,
  sx: number,
  sy: number,
  R = 22,
): DalleTouchee | null {
  const cle = (h: DalleTouchee | null): string | null =>
    !h ? null : h.kind === 'nuee' && h.nuee ? 'n:' + h.nuee : h.pid != null ? 'p:' + String(h.pid) : null;
  const N = 40;
  let prem: { k: string; h: DalleTouchee; x: number; y: number } | null = null;
  let r1 = 0;
  for (let r = 1; r <= R + 3; r++) {
    if (prem && r > r1 + 3) break;
    const vu = new Map<string, { k: string; h: DalleTouchee; x: number; y: number }>();
    for (let a = 0; a < N; a++) {
      const x = sx + r * Math.cos((a * 2 * Math.PI) / N);
      const y = sy + r * Math.sin((a * 2 * Math.PI) / N);
      const h = hit(x, y);
      const k = cle(h);
      if (k && h && !vu.has(k)) vu.set(k, { k, h, x, y });
    }
    if (!vu.size) continue;
    if (!prem) {
      if (r > R) break;
      if (vu.size > 1) return null;
      prem = [...vu.values()][0]!;
      r1 = r;
      continue;
    }
    for (const k of vu.keys()) if (k !== prem.k) return null;
  }
  if (!prem) return null;
  // sa taille : le plus grand carré qu'elle contient, lu par pas de 2 pt autour du point trouvé ; 44 pt et plus : rien
  const P = 2;
  const M = 60;
  const S2 = new Set<string>();
  const L: Array<[number, number]> = [];
  for (let y2 = -M; y2 <= M; y2 += P)
    for (let x2 = -M; x2 <= M; x2 += P)
      if (cle(hit(prem.x + x2, prem.y + y2)) === prem.k) {
        S2.add(String(x2) + ',' + String(y2));
        L.push([x2, y2]);
      }
  let best = 0;
  for (const [lx, ly] of L) {
    let a2 = best + P;
    while (a2 < 44) {
      let ok = true;
      for (let yy = ly; yy <= ly + a2 && ok; yy += P)
        for (let xx = lx; xx <= lx + a2; xx += P)
          if (!S2.has(String(xx) + ',' + String(yy))) {
            ok = false;
            break;
          }
      if (!ok) break;
      best = a2;
      a2 += P;
    }
    if (best >= 44) return null;
  }
  return prem.h;
}
