/**
 * LOT 3b-1 — Peaufiner sur la fiche et SUPPRIMER : les actions du magasin (`peaufiner`, `effacer`, `deterrer`) et le mot d'AVANT (`motAvant`).
 */
import { describe, expect, it } from 'vitest';
import { creerMagasin } from '../../src/etat/magasin.ts';
import { stockageMemoire } from '../../src/donnees/stockage.ts';
import { motAvant } from '../../src/metier/echeance.ts';
import type { Parole } from '../../src/donnees/schema.ts';

const AUJ = new Date(2026, 10, 24);
function magasin(): ReturnType<typeof creerMagasin> {
  const m = creerMagasin(stockageMemoire(), () => AUJ);
  m.planter(
    {
      titre: 'lire',
      who: 'moi',
      chiche: false,
      sens: 'soi',
      avec: '',
      note: '',
      monde: { m: 'encre', p: 'signal', h: 0 },
      due: null,
      dueISO: null,
      cercle: null,
      fichiers: [],
    },
    1000,
  );
  return m;
}

describe('peaufiner', () => {
  it('AVANT : des jours, puis une date du calendrier, puis « en l’air » ; la date est posée et recomptée', () => {
    const m = magasin();
    const id = m.etat().paroles[0]!.id;
    m.peaufiner(id, { echeance: { due: 7, dueISO: null, enLair: false } }, 2000);
    let p = m.etat().paroles[0]!;
    expect([p.due, p.ech?.iso, p.suite?.['dueChoisi']]).toEqual([7, '2026-12-01', true]);
    expect(motAvant(p, AUJ)).toBe('mardi 1');
    m.peaufiner(id, { echeance: { due: 3, dueISO: '2026-11-27', enLair: false } }, 3000);
    p = m.etat().paroles[0]!;
    expect([p.due, p.suite?.['dueISO'], motAvant(p, AUJ)]).toEqual([3, '2026-11-27', 'vendredi 27']);
    m.peaufiner(id, { echeance: { due: null, dueISO: null, enLair: true } }, 4000);
    p = m.etat().paroles[0]!;
    expect([p.due, p.ech, p.suite?.['dueISO'], motAvant(p, AUJ)]).toEqual([null, undefined, undefined, 'en l’air']);
  });
  it('le Cercle, la note, les fichiers, le trait ; une parole tenue le reste (R-005)', () => {
    const m = magasin();
    const id = m.etat().paroles[0]!.id;
    m.peaufiner(id, { cercle: 'n1', note: 'une note', fichiers: ['a.pdf'], trait: 'Coulé' }, 2000);
    const p = m.etat().paroles[0]!;
    expect([p.nuee, p.suite?.['note'], p.suite?.['files'], p.suite?.['trait'], p.derAct]).toEqual([
      'n1',
      'une note',
      ['a.pdf'],
      'Coulé',
      2000,
    ]);
    m.tenir(id, [], 3000);
    m.peaufiner(id, { echeance: { due: 1, dueISO: null, enLair: false } }, 4000);
    expect(m.etat().paroles[0]!.status).toBe('tenu');
  });
  it('motAvant : « un jour » sans échéance', () => {
    expect(motAvant({ id: 1, title: 't', due: null } as Parole, AUJ)).toBe('un jour');
  });
});

describe('effacer, deterrer', () => {
  it('effacer pose la pierre tombale ; deterrer rend la parole à sa place et retire la pierre', () => {
    const m = magasin();
    const id = m.etat().paroles[0]!.id;
    const x = m.effacer(id);
    expect(m.etat().paroles.length).toBe(0);
    expect(m.etat().effacees).toEqual([`${String(id)}|lire`]);
    m.deterrer(x!);
    expect(m.etat().paroles.map((p) => p.id)).toEqual([id]);
    expect(m.etat().effacees).toEqual([]);
    expect(m.effacer(9999)).toBeNull();
  });
});
