import { describe, it, expect } from 'vitest';
import { labDe, origineGardee, SEUIL_ORIGINE } from '../../src/metier/origine.ts';

describe('la dalle d’origine dans la bande haute (Q365)', () => {
  it('le seuil est celui de redteam_tonsurton : ΔE 15', () => {
    expect(SEUIL_ORIGINE).toBe(15);
  });
  it('le Lab du prototype (D65) : le blanc, le noir, le bleu de la nature', () => {
    expect(labDe('#FFFFFF')!.map((v) => Math.round(v) + 0)).toEqual([100, 0, 0]);
    expect(labDe('#000000')!.map((v) => Math.round(v) + 0)).toEqual([0, 0, 0]);
    expect(labDe('#82AEF8')!.map((v) => Math.round(v) + 0)).toEqual([71, 5, -41]);
  });
  it('une dalle proche du champ prend la rampe ; une dalle loin du champ garde sa couleur', () => {
    const champ = labDe('#82AEF8')!;
    expect(origineGardee([champ[0] + 3, champ[1], champ[2]], '#82AEF8')!.origine).toBe(false);
    expect(origineGardee([30, 40, 20], '#82AEF8')!.origine).toBe(true);
    expect(origineGardee(null, '#82AEF8')).toBeNull();
  });
});
