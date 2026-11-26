/**
 * LOT 5 — LA FICHE D'UN CERCLE (src/metier/cercle.ts) : ce qu'elle dit, au caractère près (les formes du prototype, `renderDetail`, `_ficheNuee`).
 */
import { describe, expect, it } from 'vitest';
import type { Parole } from '../../src/donnees/schema.ts';
import { migrer, MIGRATIONS } from '../../src/donnees/migrations/index.ts';
import { baseCercle, ligneAvec, ligneEtatCercle, motDuFil, parolesDuCercle } from '../../src/metier/cercle.ts';

const P = (o: Partial<Parole>): Parole => ({ id: 1, title: 't', who: 'moi', status: 'encours', ...o }) as Parole;

describe('la fiche d’un Cercle', () => {
  it('ses paroles : celles du Cercle, jamais un gardé de côté, dans l’ordre', () => {
    const L = [
      P({ id: 1, nuee: 'n1' }),
      P({ id: 2, nuee: 'n2' }),
      P({ id: 3, nuee: 'n1', draft: true }),
      P({ id: 4, nuee: 'n1' }),
    ];
    expect(parolesDuCercle(L, 'n1').map((q) => q.id)).toEqual([1, 4]);
  });
  it('§9 : la base du trait, max(176, 460 − 86 n), « Planter » compris', () => {
    expect([0, 1, 2, 3, 9].map(baseCercle)).toEqual([374, 288, 202, 176, 176]);
  });
  it('« Avec … » : deux nommés, puis le reste, moi compris ; « Avec toi seulement »', () => {
    expect(ligneAvec([])).toBe('Avec toi seulement');
    expect(ligneAvec(['Rachel'])).toBe('Avec Rachel');
    expect(ligneAvec(['Rachel', 'Marion'])).toBe('Avec Rachel, Marion, +1');
    expect(ligneAvec(['Rachel', 'Adrien', 'Léa', 'Nico'])).toBe('Avec Rachel, Adrien, +3');
  });
  it('la ligne d’état : « 5 Promi · 2 tenus », « 1 Promi », « encore aucune parole » (Q213)', () => {
    expect(ligneEtatCercle([])).toBe('encore aucune parole');
    expect(ligneEtatCercle([P({})])).toBe('1 Promi');
    expect(ligneEtatCercle([P({}), P({ status: 'tenu' })])).toBe('2 Promi · 1 tenu');
    expect(ligneEtatCercle([P({ status: 'tenu' }), P({ status: 'tenu' }), P({})])).toBe('3 Promi · 2 tenus');
  });
  it('le mot d’une ligne du fil : l’état d’un Promi, la nature d’un Chiche', () => {
    expect(motDuFil(P({}))).toBe('en cours');
    expect(motDuFil(P({ status: 'tenu' }))).toBe('TENU');
    expect(motDuFil(P({ chiche: true }))).toBe('CHICHE LANCÉ');
    expect(motDuFil(P({ chiche: true, status: 'tenu' }))).toBe('CHICHE RELEVÉ');
    expect(motDuFil(P({ chiche: true, suite: { chicheEtat: 'releve' } }))).toBe('CHICHE RELEVÉ');
  });
  it('le schéma v3 : un état v2 reçoit sa table des réglages des Cercles, vide ; rien d’autre ne change', () => {
    const v2 = { schema: 2, paroles: [{ id: 1, title: 'a' }], cercles: { n1: 'Marseille' } };
    const e = migrer(v2, MIGRATIONS, 3) as unknown as Record<string, unknown>;
    expect(e).toEqual({ ...v2, schema: 3, infosCercles: {} });
  });
});
