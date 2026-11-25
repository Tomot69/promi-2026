/**
 * LOT 4 — LE FIL : REPORTER (`_fpost` du prototype, enveloppé par lot-V151-ECHEANCE, C-160).
 */
import { describe, expect, it } from 'vitest';
import { creerMagasin } from '../../src/etat/magasin.ts';
import { stockageMemoire } from '../../src/donnees/stockage.ts';
import { entreesFil } from '../../src/metier/fil.ts';

describe('reporter', () => {
  it('une échéance passée se compte depuis aujourd’hui ; la ligne du Fil devient « Tu as reporté », la parole remonte en tête', () => {
    let auj = new Date(2026, 10, 24);
    const m = creerMagasin(stockageMemoire(), () => auj);
    for (const titre of ['lire', 'nager'])
      m.planter(
        {
          titre,
          who: 'moi',
          chiche: false,
          sens: 'soi',
          avec: '',
          note: '',
          monde: { m: 'encre', p: 'signal', h: 0 },
          due: 2,
          dueISO: null,
          cercle: null,
          fichiers: [],
        },
        titre === 'lire' ? 1000 : 2000,
      );
    auj = new Date(2026, 11, 1);
    m.recompter();
    const lire = m.etat().paroles.find((p) => p.title === 'lire')!;
    expect(lire.due).toBe(-5);
    const f = m.etat().fil.find((x) => x.pid === lire.id)!;
    expect(entreesFil(m.etat()).find((x) => x.f.id === f.id)!.gestes).toEqual(['tracer', 'post']);
    m.reporter(f.id, 7, Date.UTC(2026, 11, 1, 10));
    const p = m.etat().paroles.find((q) => q.id === lire.id)!;
    expect([p.due, p.ech?.iso, p.status]).toEqual([7, '2026-12-08', 'encours']);
    const g = m.etat().fil.find((x) => x.id === f.id)!;
    expect([g.type, g.text, g.t]).toEqual(['added', 'Tu as reporté : « lire » (+1 sem)', f.t]);
    expect(entreesFil(m.etat())[0]!.f.id, 'la dernière action d’abord (C-245)').toBe(f.id);
    expect(entreesFil(m.etat()).find((x) => x.f.id === f.id)!.gestes).toEqual([]);
  });
});
