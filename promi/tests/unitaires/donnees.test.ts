import { describe, expect, it } from 'vitest';
import { migrer } from '../../src/donnees/migrations/index.ts';
import { etatVide } from '../../src/donnees/schema.ts';
import { creerMagasin } from '../../src/etat/magasin.ts';
import { stockageMemoire } from '../../src/donnees/stockage.ts';
import {
  dalleDeCle,
  placeValide,
  poserCles,
  recompterEcheances,
  reparerPlaces,
  sansTombes,
} from '../../src/metier/relecture.ts';
import type { Parole } from '../../src/donnees/schema.ts';

const p = (o: Partial<Parole>): Parole =>
  ({
    id: 1,
    title: 't',
    who: 'moi',
    due: 0,
    intensity: 1,
    status: 'encours',
    from: 'moi',
    recur: null,
    remind: null,
    x: 0,
    y: 0,
    tx: 0,
    ty: 0,
    ...o,
  }) as Parole;

describe('le schéma versionné et ses migrations', () => {
  it('un état de la version courante passe tel quel', () => {
    const e = etatVide();
    expect(migrer(e)).toBe(e);
  });
  it("une version plus ancienne passe par chaque migration, dans l'ordre", () => {
    const m = { 0: (e: { schema: number } & Record<string, unknown>) => ({ ...e, schema: 1, vu: true }) };
    expect(migrer({ schema: 0 }, m, 1)).toMatchObject({ schema: 1, vu: true });
  });
  it("une migration manquante, ou un état plus récent que l'app : une erreur, jamais une perte silencieuse", () => {
    expect(() => migrer({ schema: 0 }, {}, 1)).toThrow(/aucune migration/);
    expect(() => migrer({ schema: 9 })).toThrow(/version 9/);
  });
});

describe('le magasin : un état unique, écrit au geste', () => {
  it('chaque action écrit le stockage tout de suite (C-226) et prévient les abonnés', () => {
    const s = stockageMemoire();
    const m = creerMagasin(s);
    const vu: string[] = [];
    m.abonner((_, a) => vu.push(a));
    m.choisirMonde('touffe');
    expect(JSON.parse(s.contenu()!).studio.monde).toBe('touffe');
    expect(vu).toEqual(['choisirMonde']);
    m.choisirMonde('touffe');
    expect(vu).toEqual(['choisirMonde']);
  });
  it("relit ce qu'il a écrit", () => {
    const s = stockageMemoire();
    creerMagasin(s).choisirPalette('beat', 12);
    expect(creerMagasin(s).etat().studio).toMatchObject({ palette: 'beat', teinte: 12 });
  });
});

describe('les passes de relecture du prototype', () => {
  it('une parole effacée ne revient pas (v187)', () => {
    expect(sansTombes([p({ id: 1, title: 'a' }), p({ id: 2, title: 'b' })], ['2|b']).map((x) => x.id)).toEqual([1]);
  });
  it('places : invalides effacées, la plus ancienne garde une place doublée (C-177)', () => {
    expect(placeValide([0.5, 0.5])).toBe(true);
    expect(placeValide([0, 0])).toBe(false);
    expect(placeValide([0.5, 0.5, 2])).toBe(false);
    const r = reparerPlaces(
      [p({ id: 2, place: [0.42, 0.74] }), p({ id: 1, place: [0.42, 0.74] }), p({ id: 3, place: [0.42, 0.74, 1] })],
      {},
    );
    expect(r.paroles.map((x) => x.place ?? null)).toEqual([null, [0.42, 0.74], [0.42, 0.74, 1]]);
  });
  it("une couleur figée vient du titre et de la personne, jamais de l'id (Q213)", () => {
    expect(dalleDeCle({ title: 'planter un arbre', who: 'moi' })).toEqual(
      dalleDeCle({ title: 'planter un arbre', who: 'moi' }),
    );
    expect(dalleDeCle({ title: 'a', who: 'moi' }).ci).toBeLessThan(4);
  });
  it('la clé de plantation : le titre, jamais pour un gardé de côté (Q621)', () => {
    expect(
      poserCles([p({ title: 'x' }), p({ title: 'y', draft: true }), p({ title: 'z', cle: 'z0' })]).map(
        (x) => x.cle ?? null,
      ),
    ).toEqual(['x', null, 'z0']);
  });
  it("l'échéance est une date, recomptée contre aujourd'hui (C-160)", () => {
    const auj = new Date(2026, 10, 20);
    const [a, b] = recompterEcheances([p({ due: 7, ech: { iso: '2026-11-24', due: 7 } }), p({ due: 3 })], auj);
    expect(a!.due).toBe(4);
    expect(b!.ech).toEqual({ iso: '2026-11-23', due: 3 });
  });
});
