import { describe, expect, it } from 'vitest';
import { creerHorloge } from '../../src/animation/horloge.ts';

const natifs = { raf: () => 0, st: () => 0, ct: () => undefined, now: () => 0 };

describe("l'horloge unique, en mode piloté (l'algorithme de banc_rendu.py, PILOTE)", () => {
  it('avance de 1000/60 ms par image, passe les minuteurs échus PUIS les images', () => {
    const h = creerHorloge('pilote', natifs, 1000);
    const vu: string[] = [];
    h.minuteur(() => vu.push('m10'), 10);
    h.image((t) => vu.push('i' + t.toFixed(3)));
    h.images(1);
    expect(vu).toEqual(['m10', 'i1016.667']);
    expect(h.maintenant()).toBeCloseTo(1016.667, 3);
  });
  it('ordonne les minuteurs par échéance, puis par ordre de pose ; un intervalle repart à son pas (16 ms au moins)', () => {
    const h = creerHorloge('pilote', natifs, 0);
    const vu: string[] = [];
    h.minuteur(() => vu.push('b'), 5);
    h.minuteur(() => vu.push('a'), 2);
    h.minuteur(() => vu.push('c'), 5);
    const id = h.intervalle(() => vu.push('i'), 1);
    h.images(2);
    h.annuleMinuteur(id);
    h.images(2);
    expect(vu).toEqual(['a', 'b', 'c', 'i', 'i']); // l'intervalle à 16 puis 32 ms ; annulé, plus rien
  });
  it("une image demandée pendant une image passe à l'image suivante ; une image annulée ne passe pas", () => {
    const h = creerHorloge('pilote', natifs, 0);
    let n = 0;
    const boucle = (): void => {
      n++;
      if (n < 3) h.image(boucle);
    };
    h.image(boucle);
    const x = h.image(() => (n = 100));
    h.annuleImage(x);
    h.images(5);
    expect(n).toBe(3);
  });
  it('« quand le fil est libre » = un minuteur de 1 ms (comme le banc)', () => {
    const h = creerHorloge('pilote', natifs, 0);
    let ok = false;
    h.quandLibre((d) => (ok = d.timeRemaining() === 50 && !d.didTimeout));
    h.images(1);
    expect(ok).toBe(true);
  });
  it("en mode réel, images() n'existe pas", () => {
    expect(() => creerHorloge('reel', natifs).images(1)).toThrow();
  });
});
