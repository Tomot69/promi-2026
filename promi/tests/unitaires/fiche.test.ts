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
import { etatVide, type Parole } from '../../src/donnees/schema.ts';
import { noyauxDe } from '../../src/ecrans/fiche/noyaux.ts';
import { creerMagasin, type Magasin } from '../../src/etat/magasin.ts';
import { stockageMemoire } from '../../src/donnees/stockage.ts';

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

describe('tenir (lot 3a-2) : ce que le magasin écrit — le prototype, `#segStatus` « tenue », lot-V145-PARTS, lot-V149-VALIDATION', () => {
  const magasinAvec = (paroles: Parole[]): Magasin => {
    const m = creerMagasin(stockageMemoire(), () => AUJ);
    const e = etatVide();
    m.importer({ ...e, paroles, compteurs: { nid: 50, fid: 9 } });
    return m;
  };
  const trace = [
    { x: 150, y: 60 },
    { x: 200, y: 58 },
  ];
  test('seul : la parole tenue, son trait, « vue tenue », la ligne du Fil (les guillemets insécables)', () => {
    const m = magasinAvec([P({ id: 7 })]);
    expect(m.tenir(7, trace, 1_800_000_000_000)).toBe('tenue');
    const p = m.etat().paroles[0]!;
    expect(p.status).toBe('tenu');
    expect(p.suite?.['trace']).toEqual(trace);
    expect(Object.keys(p.vuTenue ?? {})).toEqual(['moi']);
    expect(m.etat().fil[0]).toMatchObject({
      type: 'kept',
      text: 'Tu as tenu « rendre le livre »',
      pid: 7,
      t: "à l'instant",
      unread: false,
    });
    // déjà tenue : rien
    expect(m.tenir(7, trace, 1_800_000_000_001)).toBe('rien');
  });
  test('ma part, sans être la dernière : `parts.moi` seul, la parole reste en cours, rien au Fil', () => {
    const m = magasinAvec([P({ id: 7, chiche: true, from: 'Marion', suite: { avec: 'Lou' } })]);
    const fil = m.etat().fil.length;
    expect(m.tenir(7, trace, 1_800_000_000_000)).toBe('part');
    const p = m.etat().paroles[0]!;
    expect(p.status).toBe('encours');
    expect(Object.keys(p.parts ?? {})).toEqual(['moi']);
    expect(m.etat().fil.length).toBe(fil);
  });
  test('la dernière part : tenue, « Chacun a tracé sa part »', () => {
    const m = magasinAvec([P({ id: 7, chiche: true, from: 'Marion', suite: { avec: 'Lou' }, parts: { Lou: 'x' } })]);
    expect(m.tenir(7, trace, 1_800_000_000_000)).toBe('tenue');
    expect(m.etat().fil[0]!.text).toBe('Chacun a tracé sa part : « rendre le livre »');
  });
  test('je ne suis pas de ceux qui tiennent : rien', () => {
    const m = magasinAvec([P({ id: 7, chiche: true, who: 'Rachel, Marion' })]);
    expect(m.tenir(7, trace, 1_800_000_000_000)).toBe('rien');
    expect(m.etat().paroles[0]!.status).toBe('encours');
  });
  test('une parole récurrente renaît en cours (`regenRecur`)', () => {
    const m = magasinAvec([P({ id: 7, recur: 'weekly' })]);
    m.tenir(7, trace, 1_800_000_000_000);
    const n = m.etat().paroles.find((q) => q.id === 50)!;
    expect(n).toMatchObject({ title: 'rendre le livre', status: 'encours', due: 7, recur: 'weekly' });
    expect(
      m
        .etat()
        .fil.slice(0, 2)
        .map((f) => f.text),
    ).toEqual(['Tu as tenu « rendre le livre »', '↻ « rendre le livre » régénérée']);
  });
});

describe('renommer (lot 3a-4, C-280, Q621) : ce que le magasin écrit — le prototype, `sort()` de lot-V203-TITRE', () => {
  const magasinAvec = (paroles: Parole[]): Magasin => {
    const m = creerMagasin(stockageMemoire(), () => AUJ);
    m.importer({ ...etatVide(), paroles, compteurs: { nid: 50, fid: 9 } });
    return m;
  };
  test('le titre neuf, la clé de plantation gardée, la dernière action', () => {
    const m = magasinAvec([P({ id: 7 })]);
    expect(m.etat().paroles[0]!.cle, 'la clé posée à la relecture (Q621)').toBe('rendre le livre');
    m.renommer(7, 'rendre le livre demain', 1_800_000_000_000);
    const p = m.etat().paroles[0]!;
    expect(p.title).toBe('rendre le livre demain');
    expect(p.cle).toBe('rendre le livre');
    expect(p.derAct).toBe(1_800_000_000_000);
  });
  test('une parole plantée porte sa clé dès sa plantation', () => {
    const m = magasinAvec([]);
    const id = m.planter(
      {
        titre: 'courir',
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
      1_800_000_000_000,
    );
    expect(m.etat().paroles.find((q) => q.id === id)!.cle).toBe('courir');
  });
  test('les lignes du Fil qui la citent sont réécrites (les guillemets insécables), les autres non', () => {
    const m = magasinAvec([P({ id: 7 }), P({ id: 8, title: 'rendre le livre' })]);
    m.tenir(7, [{ x: 150, y: 60 }], 1_800_000_000_000);
    m.tenir(8, [{ x: 150, y: 60 }], 1_800_000_000_001);
    m.renommer(7, 'rendre le livre demain', 1_800_000_000_002);
    const L = m.etat().fil.map((f) => [f.pid, f.text]);
    expect(L).toContainEqual([7, 'Tu as tenu « rendre le livre demain »']);
    expect(L).toContainEqual([8, 'Tu as tenu « rendre le livre »']);
  });
});

describe('les Noyaux d’une parole d’un Cercle (lot 3a ; le prototype : `openDetail`, `auraDisques`)', () => {
  test('« Toi », puis UN disque : le Cercle, son nom entier, l’agrégat de toutes ses paroles', () => {
    const toutes = [
      P({ id: 1, nuee: 'n1', who: 'tout le monde' }),
      P({ id: 2, nuee: 'n1', who: 'tout le monde', status: 'tenu' }),
      P({ id: 3, nuee: 'n1', who: 'tout le monde', from: 'Rachel' }),
      P({ id: 4, who: 'Marion' }),
    ];
    const N = noyauxDe(toutes[0]!, toutes, { n1: 'l’atelier du samedi' });
    expect(N.map((n) => n.nom)).toEqual(['Toi', 'l’atelier du samedi']);
    expect(N[1]).toMatchObject({ moi: false, cercle: 'n1', tenues: 1, enCours: 2 });
  });
  test('sans nom connu, la clé ; une parole à soi n’a que « Toi »', () => {
    const p = P({ nuee: 'n9' });
    expect(noyauxDe(p, [p]).map((n) => n.nom)).toEqual(['Toi', 'n9']);
    expect(noyauxDe(P({}), [P({})]).map((n) => n.nom)).toEqual(['Toi']);
  });
});
