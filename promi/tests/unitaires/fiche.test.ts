/**
 * LOT 3a — ce que la fiche DIT, contre le prototype (relevé le 23 nov. 2026, `banc-etats/etat-fiches.json`, `openDetail(pid)`), en dur.
 */
import { describe, expect, test } from 'vitest';
import {
  consigne,
  datePassee,
  etatParts,
  initiales,
  ligneEtat,
  phraseFiche,
  tenants,
  traitFiche,
} from '../../src/metier/fiche.ts';
import type { Parole } from '../../src/donnees/schema.ts';

const P = (x: Partial<Parole> & Record<string, unknown>): Parole =>
  ({
    id: 1,
    title: 'rendre le livre',
    who: 'moi',
    due: null,
    intensity: 1,
    status: 'encours',
    from: 'moi',
    recur: null,
    remind: null,
    x: 0,
    y: 0,
    tx: 0,
    ty: 0,
    ...x,
  }) as Parole;
const AUJ = new Date(2026, 10, 23);

describe('la phrase complète (C-069, Q412)', () => {
  const cas: Array<[Partial<Parole> & Record<string, unknown>, string]> = [
    [{}, 'Je me promets de'],
    [{ who: 'Marion', title: 'appeler mamie' }, 'Je promets à Marion d’'],
    [{ who: 'Rachel, Marion', title: 'passer voir Nico' }, 'Je promets à Rachel et Marion de'],
    [
      { who: 'Rachel, Marion, Nico, Lou, Adrien', title: 'répondre à Marion' },
      'Je promets à Rachel, Marion + 3 personnes de',
    ],
    [{ from: 'Nico', title: 'lire le roman' }, 'Nico me promet de'],
    [{ chiche: true, title: 'courir dimanche' }, 'T’es pas chiche de'],
    [{ chiche: true, who: 'Adrien', title: 'peindre la porte' }, 'Adrien, t’es pas chiche de'],
    [{ chiche: true, from: 'Marion', title: 'envoyer la carte' }, 'Marion me dit : t’es pas chiche d’'],
    [{ chiche: true, avec: 'Lou', status: 'tenu', title: 'payer Adrien' }, 'Lou, t’es pas chiche de'],
    [{ chiche: true, who: 'Rachel, Marion', title: 'passer voir Nico' }, 'Rachel et Marion, vous êtes pas chiches de'],
    [{ req: true, who: 'Rachel' }, 'Rachel, promets-moi de'],
  ];
  for (const [p, t] of cas) test(t, () => expect(phraseFiche(P(p))!.txt).toBe(t));
  test('dépliée, la liste entière', () =>
    expect(phraseFiche(P({ who: 'Rachel, Marion, Nico, Lou, Adrien' }), true)!.txt).toBe(
      'Je promets à Rachel, Marion, Nico, Lou et Adrien de',
    ));
  test('un gardé de côté : pas de phrase', () => expect(phraseFiche(P({ draft: true }))).toBeNull());
});

describe("la ligne d'état (C-210)", () => {
  test('en cours, date passée : « EN COURS · 12 OCT. »', () =>
    expect(ligneEtat(P({ due: -42, ech: { iso: '2026-10-12', due: -42 } }), AUJ).texte).toBe('EN COURS · 12 OCT.'));
  test('les mots', () => {
    expect(ligneEtat(P({}), AUJ).texte).toBe('EN COURS');
    expect(ligneEtat(P({ status: 'tenu' }), AUJ)).toEqual({ texte: 'TENUE', tenu: true });
    expect(ligneEtat(P({ chiche: true }), AUJ).texte).toBe('LANCÉ');
    expect(ligneEtat(P({ chiche: true, from: 'Marion' }), AUJ).texte).toBe('À RELEVER');
    expect(ligneEtat(P({ chiche: true, status: 'tenu', avec: 'Lou' }), AUJ).texte).toBe('TENU À DEUX');
  });
  test('une date future ne s’écrit pas', () => expect(datePassee(P({ due: 99 }), AUJ)).toBeNull());
});

describe('la consigne et les parts (C-108, Q465, C-115)', () => {
  test('les consignes', () => {
    expect(consigne(P({}))).toBe('trace pour tenir');
    expect(consigne(P({ chiche: true }))).toBe('trace pour lancer');
    expect(consigne(P({ chiche: true, who: 'Adrien' }))).toBe('à Adrien de tracer sa part');
    expect(consigne(P({ status: 'tenu' }))).toBeNull();
    expect(consigne(P({ draft: true }))).toBe('trace pour planter');
  });
  test('à plusieurs : une part tracée, il reste Marion', () => {
    const p = P({ chiche: true, who: 'Rachel, Marion', parts: { Rachel: '2026-11-10T10:00:00Z' } });
    expect(tenants(p)).toEqual(['Rachel', 'Marion']);
    expect(etatParts(p).reste).toEqual(['Marion']);
    expect(consigne(p)).toBe('à Marion de tracer sa part');
  });
  test('une promesse que je fais à plusieurs : ma part seule', () =>
    expect(tenants(P({ who: 'Rachel, Marion' }))).toEqual(['moi']));
  test('les initiales', () => expect(initiales(['Marion', 'Mathieu', 'Lou'], 'Tom')).toEqual(['MA', 'MA', 'L']));
  test('le trait', () => {
    expect(traitFiche(P({}))).toEqual({ mode: 'moitie', base: 286, amp: 36, carte: false });
    expect(traitFiche(P({ status: 'tenu' })).base).toBe(362);
    expect(traitFiche(P({ status: 'tenu', comments: [{ t: 'x', d: '', by: 'Rachel' }] })).base).toBe(286);
    expect(traitFiche(P({ status: 'tenu', chiche: true, avec: 'Lou' })).mode).toBe('duo');
  });
});
