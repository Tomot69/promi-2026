/**
 * LOT 2a — les règles pures de la page + : le tirage des exemples (redteam_suggestions, v115, v179b — E4 point 4), « de » / « d’ » (C-312,
 * la règle de liaison_regle.py en dur), la migration 1 → 2 (le gardé de côté et son `brouillon`), et l'action « garder de côté » du magasin.
 */
import { describe, expect, it } from 'vitest';
import { tirer, variante } from '../../src/metier/exemples.ts';
import { elision } from '../../src/metier/elision.ts';
import { migrer, MIGRATIONS } from '../../src/donnees/migrations/index.ts';
import { creerMagasin } from '../../src/etat/magasin.ts';
import { stockageMemoire } from '../../src/donnees/stockage.ts';
import { EXEMPLES } from '../../src/textes/page-plus.ts';

/** un hasard écrit d'avance */
const alea = (graine: number): (() => number) => {
  let s = graine;
  return () => ((s = (s * 16807) % 2147483647) - 1) / 2147483646;
};

describe('les exemples des pastilles vides', () => {
  it('les phrases fixes d’abord, puis le sac sans remise, jamais la même deux fois de suite', () => {
    for (const [t, fixes] of [
      ['soi', 2],
      ['chiche', 1],
    ] as const) {
      const L = EXEMPLES[t].length;
      let e = { n: 0, sac: null as number[] | null, der: null as number | null };
      const vus: number[] = [];
      const r = alea(7);
      for (let i = 0; i < 3 * L; i++) {
        const x = tirer(L, fixes, e, r);
        vus.push(x.rang);
        e = x.suivant;
      }
      expect(vus.slice(0, fixes), `${t} : les phrases fixes`).toEqual([...Array(fixes).keys()]);
      // un sac entier passe avant qu'une phrase revienne
      const sac1 = vus.slice(fixes, L);
      expect(new Set(sac1).size, `${t} : le premier sac, sans remise`).toBe(L - fixes);
      for (let i = 1; i < vus.length; i++)
        expect(vus[i], `${t} : jamais deux fois de suite (${String(i)})`).not.toBe(vus[i - 1]);
    }
  });
  it('« A / B » : la variante plurielle', () => {
    expect(variante('t’emmener voir la mer / vous emmener voir la mer', true)).toBe('vous emmener voir la mer');
    expect(variante('t’emmener voir la mer / vous emmener voir la mer', false)).toBe('t’emmener voir la mer');
    expect(variante('m’y mettre', true)).toBe('m’y mettre');
  });
});

describe('« de » ou « d’ » (C-312, liaison_regle.py)', () => {
  const CAS: Array<[string, string]> = [
    ['me coucher le jour même', 'de'],
    ['apprendre à repriser', 'd’'],
    ['arroser mes plantes', 'd’'],
    ['écrire une lettre', 'd’'],
    ['habiter ici', 'd’'],
    ['haïr la pluie', 'de'],
    ['hurler', 'de'],
    ['y aller', 'd’'],
    ['en finir', 'd’'],
    ['yoga', 'de'],
    ['oui', 'de'],
    ['onze heures', 'de'],
    ['3 kilos', 'de'],
    ['', 'de'],
  ];
  for (const [t, d] of CAS) it(`« ${t} » → ${d}`, () => expect(elision(t)).toBe(d));
});

describe('le schéma v2 : le gardé de côté porte son brouillon', () => {
  it('migrer un état v1 : `suite.brouillon` passe à sa place, rien ne se perd', () => {
    const v1 = {
      schema: 1,
      paroles: [
        { id: 1, title: 'a', draft: true, suite: { brouillon: { v: 1, nat: 'chiche' }, dk: 'solo' } },
        { id: 2, title: 'b', suite: { brouillon: { v: 1, nat: 'promi' } } },
        { id: 3, title: 'c' },
      ],
    };
    // la migration 1 → 2 seule (la cible : la version 2)
    const e = migrer(v1, MIGRATIONS, 2) as unknown as { schema: number; paroles: Array<Record<string, unknown>> };
    expect(e.schema).toBe(2);
    expect(e.paroles[0]).toEqual({
      id: 1,
      title: 'a',
      draft: true,
      brouillon: { v: 1, nat: 'chiche' },
      suite: { dk: 'solo' },
    });
    expect(e.paroles[1]).toEqual({ id: 2, title: 'b', brouillon: { v: 1, nat: 'promi' } });
    expect(e.paroles[2]).toEqual({ id: 3, title: 'c' });
  });
  it('garder de côté : un gardé de côté écrit tout de suite, mis à jour à la reprise, dit au Fil', () => {
    const st = stockageMemoire();
    const m = creerMagasin(st);
    const b = {
      v: 1 as const,
      nat: 'chiche' as const,
      phrase: { titre: 'x' },
      who: [],
      sens: 'soi',
      nom: '',
      membres: [],
    };
    const id = m.garderDeCote(b, 'x', 'moi', null, 1000);
    expect(m.etat().paroles.find((p) => p.id === id)).toMatchObject({
      draft: true,
      chiche: true,
      title: 'x',
      brouillon: b,
    });
    expect(JSON.parse(st.contenu()!).paroles).toHaveLength(1);
    expect(m.etat().fil[0]!.text).toBe('Tu as gardé «\u00a0x\u00a0» de côté');
    const id2 = m.garderDeCote({ ...b, nat: 'promi' }, 'y', 'Rachel', id, 2000);
    expect(id2).toBe(id);
    expect(m.etat().paroles).toHaveLength(1);
    expect(m.etat().paroles[0]).toMatchObject({ title: 'y', who: 'Rachel' });
    expect(m.etat().paroles[0]!.chiche).toBeUndefined();
  });
});

describe('C-129 — pas d’emoji', () => {
  it('les pictogrammes, les teintes, la jonction, les drapeaux et la touche numérotée entière partent ; le texte reste', async () => {
    const { sansEmoji } = await import('../../src/metier/emoji.ts');
    expect(sansEmoji('marcher 🏃 une 👍🏽 heure 1️⃣ 👨‍👩‍👧 🇫🇷 ❤️ ✨')).toBe('marcher  une  heure     ');
    expect(sansEmoji('appeler Lou')).toBe('appeler Lou');
  });
});
