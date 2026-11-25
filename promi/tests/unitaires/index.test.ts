/**
 * LOT 4 — L'INDEX : ce qu'il liste et dans quel ordre (`buildIndex`, C-245 « Récents »), les mots d'une carte (`motQui`, `motEtat`).
 */
import { describe, expect, it } from 'vitest';
import { etatVide, type Parole } from '../../src/donnees/schema.ts';
import { aQui, entreesIndex, motEtat, motQui } from '../../src/metier/index.ts';

const P = (id: number, o: Partial<Parole> = {}): Parole => ({
  id,
  title: `parole ${String(id)}`,
  who: 'moi',
  due: null,
  intensity: 2,
  status: 'encours',
  from: 'moi',
  recur: null,
  remind: null,
  x: 0,
  y: 0,
  tx: 0,
  ty: 0,
  ...o,
});
const ids = (L: ReturnType<typeof entreesIndex>): Array<number | string> =>
  L.map((x) => (x.kind === 'nuee' ? x.k : x.p.id));

describe("l'Index", () => {
  it('« Récents » : la dernière action d’abord, puis la plus récemment plantée ; les gardés de côté ferment la liste', () => {
    const e = etatVide();
    e.paroles = [P(1), P(2, { derAct: 1_800_000_000_000 }), P(3, { draft: true, derAct: 1_900_000_000_000 }), P(4)];
    expect(ids(entreesIndex(e))).toEqual([2, 4, 1, 3]);
  });
  it('un Cercle tient la place de ses paroles, et prend la dernière action de la plus récente', () => {
    const e = etatVide();
    e.cercles = { n1: 'Marseille', vide: 'Atelier' };
    e.paroles = [P(1, { nuee: 'n1' }), P(2), P(3, { nuee: 'n1', derAct: 1_800_000_000_000 })];
    // un Cercle sans parole est « gardé de côté » : il ferme la liste
    expect(ids(entreesIndex(e))).toEqual(['n1', 2, 'vide']);
  });
  it('la recherche lit le titre, la personne, celui qui promet et le nom du Cercle ; les filtres', () => {
    const e = etatVide();
    e.cercles = { n1: 'Marseille' };
    e.paroles = [
      P(1, { title: 'nager', who: 'Rachel' }),
      P(2, { status: 'tenu' }),
      P(3, { draft: true }),
      P(4, { nuee: 'n1' }),
    ];
    expect(ids(entreesIndex(e, 'rach'))).toEqual([1]);
    expect(ids(entreesIndex(e, 'marseille'))).toEqual(['n1']);
    // « En suspens » ne liste pas les Cercles : la parole d'un Cercle y paraît à son nom (comme `buildIndex`)
    expect(ids(entreesIndex(e, '', 'suspens'))).toEqual([4, 1]);
    expect(ids(entreesIndex(e, '', 'brouillons'))).toEqual([3]);
    expect(ids(entreesIndex(e, '', 'nuees'))).toEqual(['n1']);
  });
  it('les mots d’une carte', () => {
    const d = new Date(2026, 10, 25);
    expect(motQui(P(1))).toBe('à moi');
    expect(motQui(P(1, { from: 'Nico' }))).toBe('de Nico');
    expect(motQui(P(1, { who: 'Rachel, Marion' }))).toBe('à Rachel, Marion');
    expect(motQui(P(1, { draft: true }))).toBe('gardé de côté');
    expect(aQui('le groupe')).toBe('au groupe');
    expect(aQui('les voisins')).toBe('aux voisins');
    expect(motEtat(P(1), d)).toBe('EN COURS');
    expect(motEtat(P(1, { chiche: true }), d)).toBe('LANCÉ');
    expect(motEtat(P(1, { status: 'tenu' }), d)).toBe('TENUE');
    expect(motEtat(P(1, { status: 'tenu', chiche: true, suite: { avec: 'Rachel' } }), d)).toBe('TENU À DEUX');
    expect(motEtat(P(1, { due: -3, ech: { iso: '2026-10-12', due: -3 } }), d)).toBe('EN COURS · 12 OCT.');
  });
});
