/**
 * LOT 6 — LA ROTATION DE LA PELOTE (src/metier/derive.ts, C-302) : la dérive de l'axe est celle du prototype, tirage pour tirage. Les valeurs sont
 * celles que rend `_peloteDerive.simule` du prototype (relevées le 28 nov. 2026, WebKit), écrites en dur (CLAUDE.md §7).
 */
import { describe, expect, it } from 'vitest';
import { AUTO, TOUR_S, borne, creerDerive, hasardGraine, simuleDerive } from '../../src/metier/derive.ts';

describe('la dérive de la Pelote', () => {
  it('un tour en 66,7 s (C-298) ; la vue s’incline au plus de ±1,15', () => {
    expect(TOUR_S).toBeCloseTo(66.6667, 3);
    expect(AUTO).toBeCloseTo(0.0942478, 6);
    expect(borne(2)).toBe(1.15);
    expect(borne(-3)).toBe(-1.15);
  });
  it('30 s au pas de 1/60, graine 7 : les pas du prototype', () => {
    const a = simuleDerive(30, 1 / 60, 7);
    expect(a.length).toBe(1801);
    expect(a[0]).toEqual([-1e-7, 0.0773874, 0.0537944, 0.32]);
    expect(a[600]).toEqual([-0.0163771, -0.0092482, 0.0900264, 0.24312]);
    expect(a[1200]).toEqual([-0.0161145, -0.0767216, 0.0367392, 0.06626]);
    expect(a[1800]).toEqual([-0.0462978, -0.0460044, 0.0599241, -0.15417]);
  });
  it('5 min au pas de 1/30, graine 3 ; 20 s par défaut', () => {
    const b = simuleDerive(300, 1 / 30, 3);
    expect(b.length).toBe(9000);
    expect(b[0]).toEqual([9e-7, 0.077387, 0.0537945, 0.32]);
    expect(b[4500]).toEqual([0.0032644, 0.0835246, 0.0594379, -0.51719]);
    expect(b[8999]).toEqual([-0.0196972, 0.019524, -0.0846725, 0.71208]);
    const c = simuleDerive(20);
    expect(c.length).toBe(1200);
    expect(c[0]).toEqual([-1e-7, 0.0773876, 0.0537942, 0.32]);
    expect(c[1199]).toEqual([-0.0404891, 0.0926123, 0.0129842, -0.03968]);
  });
  it('la vitesse reste entre 0,85 et 1,15 × celle de C-298, jamais un saut d’un pas à l’autre', () => {
    const D = creerDerive(hasardGraine(11));
    let tan = 0.32;
    let w0 = -1;
    for (let i = 0; i < 60 * 120; i++) {
      const W = D.pas(1 / 60, tan);
      tan = borne(tan + W.tan / 60);
      expect(W.w).toBeGreaterThanOrEqual(AUTO * 0.85 - 1e-9);
      expect(W.w).toBeLessThanOrEqual(AUTO * 1.15 + 1e-9);
      if (w0 >= 0) expect(Math.abs(W.w - w0)).toBeLessThan(AUTO * 0.002);
      w0 = W.w;
    }
  });
});
