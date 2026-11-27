/**
 * LOT 6 — L'AURA (src/metier/aura.ts) : ce qu'elle dit, au caractère près (le prototype : `donnees`, `remplit`, `comptes` de lot-AURA-PELOTE).
 * Les valeurs sont écrites en dur : un juge ne lit jamais la valeur qu'il vérifie (CLAUDE.md §7).
 */
import { describe, expect, it } from 'vitest';
import type { Parole } from '../../src/donnees/schema.ts';
import { donneesAura, envers, mesParoles, natureMaj, ordreTenus, parts, personnes } from '../../src/metier/aura.ts';

const P = (o: Partial<Parole> & { suite?: Record<string, unknown> }): Parole =>
  ({ id: 1, title: 't', who: 'moi', status: 'encours', from: 'moi', ...o }) as Parole;

describe('l’Aura', () => {
  it('mes paroles : ni un gardé de côté, ni une demande, ni la parole d’un autre', () => {
    const L = [
      P({ id: 1 }),
      P({ id: 2, draft: true }),
      P({ id: 3, suite: { req: true } }),
      P({ id: 4, from: 'Rachel' }),
      P({ id: 5, from: '' }),
    ];
    expect(mesParoles(L).map((q) => q.id)).toEqual([1, 5]);
  });
  it('l’ordre des tenues est celui où elles sont apparues : l’ordre gardé, puis les nouvelles par id', () => {
    const L = [P({ id: 9, status: 'tenu' }), P({ id: 3, status: 'tenu' }), P({ id: 5, status: 'tenu' }), P({ id: 7 })];
    const r = ordreTenus(L, [5, 7, 2]);
    expect(r.ordre).toEqual([5, 3, 9]);
    expect(r.tenus.map((q) => q.id)).toEqual([5, 3, 9]);
  });
  it('la nature la plus tenue ; égalité : Promi, puis Chiche, puis Cercle ; zéro : Promi', () => {
    expect(natureMaj([])).toBe('promi');
    expect(natureMaj([P({ chiche: true }), P({})])).toBe('promi');
    expect(natureMaj([P({ chiche: true }), P({ chiche: true }), P({})])).toBe('chiche');
    expect(natureMaj([P({ nuee: 'n1' }), P({ chiche: true })])).toBe('chiche');
  });
  it('les parts d’un anneau : deux états (C-210)', () => {
    expect(parts([])).toEqual([0, 0]);
    expect(parts([P({ status: 'tenu' }), P({}), P({}), P({ status: 'tenu' })])).toEqual([0.5, 0.5]);
  });
  it('les personnes : ordre alphabétique, ni moi ni « le groupe » ; ce qu’on me tient les rejoint (Q215)', () => {
    const L = [
      P({ id: 1, who: 'Rachel, Marion' }),
      P({ id: 2, who: 'Élodie', status: 'tenu' }),
      P({ id: 3, who: 'Tom' }),
      P({ id: 4, who: 'le groupe' }),
    ];
    const E = envers([...L, P({ id: 8, from: 'Nico', who: 'moi', status: 'tenu' })], 'Tom', {});
    const g = personnes(L, E, 'Tom');
    expect(g.map((x) => x.nom)).toEqual(['Élodie', 'Marion', 'Nico', 'Rachel']);
    expect(g.find((x) => x.nom === 'Nico')).toEqual({ nom: 'Nico', parts: [1, 0], recu: [1, 0], nRecu: 1 });
    expect(g.find((x) => x.nom === 'Élodie')?.parts).toEqual([1, 0]);
  });
  it('ce qu’on te tient : ce qu’on te promet, ce qu’on promet à un de tes Cercles, la moitié d’un Chiche relevé', () => {
    const L = [
      P({ id: 1, from: 'Rachel', who: 'moi' }),
      P({ id: 2, from: 'Marion', who: 'Adrien' }),
      P({ id: 3, from: 'Nico', who: 'Adrien', nuee: 'n1' }),
      P({ id: 4, chiche: true, suite: { chicheEtat: 'releve', avec: 'Léa' } }),
    ];
    expect(envers(L, 'Tom', { n1: 'Marseille' }).map((x) => `${x.nom}:${String(x.p.id)}`)).toEqual([
      'Rachel:1',
      'Nico:3',
      'Léa:4',
    ]);
  });
  it('la phrase : aucune parole (→ la page +) ; rien de tenu (→ l’Index) ; sinon le mot du nombre de tenues', () => {
    const o = { moi: 'Tom', cercles: {}, ordre: [] };
    expect(donneesAura([], o).phrase).toEqual({
      l1: 'La première parole laissera sa trace ici.',
      l2: 'Tout commence par une parole donnée.',
      mene: 'plus',
    });
    expect(donneesAura([P({})], o).phrase).toEqual({
      l1: 'Rien de tenu pour l’instant.',
      l2: 'Une parole tenue prendra place ici.',
      mene: 'index',
    });
    const t = (n: number): Parole[] => Array.from({ length: n }, (_, i) => P({ id: i + 1, status: 'tenu' }));
    expect(donneesAura(t(1), o).phrase.l1).toBe('Tout ça, tu l’as dit. Et tu l’as fait.');
    expect(donneesAura(t(5), o).phrase.l1).toBe('Rien de ce qui est ici n’a été dit à la légère.');
    expect(donneesAura(t(4), o).phrase.l1).toBe('Et dire que tout ça, c’est toi.');
  });
  it('« Ce que tu as tenu » : toutes, la plus récente (la dernière apparue) en premier ; les deux chiffres', () => {
    const L = [P({ id: 1, status: 'tenu' }), P({ id: 2 }), P({ id: 3, status: 'tenu' }), P({ id: 4 }), P({ id: 5 })];
    const d = donneesAura(L, { moi: 'Tom', cercles: {}, ordre: [3] });
    expect(d.moisson.map((q) => q.id)).toEqual([1, 3]);
    expect(d.chiffres).toEqual([2, 3]);
  });
});
