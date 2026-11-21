/**
 * LOT 1 — ce que l'accueil calcule, contre les valeurs du prototype écrites EN DUR (§7 : un juge porte la décision, l'app la respecte).
 */
import { describe, expect, test } from 'vitest';
import { anneauCss, anneauSvg } from '../../src/ecrans/accueil/anneau.ts';
import { compteAnneau, filAttente } from '../../src/metier/fil.ts';
import { rappelDu } from '../../src/metier/rappel.ts';
import { toucheTolerant } from '../../src/ecrans/toucher-tolerant.ts';
import { etatVide, type Etat, type Parole } from '../../src/donnees/schema.ts';
import type { DalleTouchee } from '../../src/moteur/facade.ts';

/** l'anneau du + relevé sur le prototype (jeu de démonstration : 7 tenues, 11 en cours), `--kr-svg` de #createBtn, 20 nov. 2026 */
const ANNEAU_PROTOTYPE =
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72"><path d="M37.50 6.79 A29.25 29.25 0 0 1 55.93 57.41" fill="none" stroke="#00341A" stroke-width="13.5"/><path d="M53.63 59.34 A29.25 29.25 0 1 1 34.50 6.79" fill="none" stroke="#291547" stroke-width="13.5"/></svg>';

describe("l'anneau du +", () => {
  test('les mêmes nombres donnent la même image que le prototype, au caractère près', () => {
    expect(anneauSvg({ tenues: 7, enCours: 11 })).toBe(ANNEAU_PROTOTYPE);
    expect(anneauCss({ tenues: 7, enCours: 11 })).toBe(
      'url("data:image/svg+xml;utf8,' + encodeURIComponent(ANNEAU_PROTOTYPE) + '")',
    );
  });
  test('un seul état : un arc presque entier (le jour de 0,002 rad) ; aucune parole : aucun arc', () => {
    expect((anneauSvg({ tenues: 2, enCours: 0 }).match(/<path/g) ?? []).length).toBe(1);
    expect(anneauSvg({ tenues: 0, enCours: 0 })).toBe(
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72"></svg>',
    );
  });
});

function etat(
  paroles: Array<Partial<Parole> & Record<string, unknown>>,
  fil: unknown[] = [],
  autres: Record<string, string> = {},
): Etat {
  const e = etatVide();
  e.paroles = paroles.map((p, i) => {
    const { suite, ...connus } = p as Parole;
    const extra = Object.fromEntries(
      Object.entries(p).filter(([k]) => !['id', 'title', 'status', 'draft'].includes(k)),
    );
    return {
      ...connus,
      id: p.id ?? i + 1,
      ...(Object.keys(extra).length ? { suite: { ...(suite ?? {}), ...extra } } : {}),
    } as Parole;
  });
  e.fil = fil as Etat['fil'];
  e.autres = autres;
  return e;
}

describe('la pastille du Fil et le compte de l’anneau (v89, Q347 ; v173)', () => {
  test('ce qui attend un geste : un Chiche reçu, un Promi reçu non accepté, une invitation, une moitié, une demande', () => {
    const e = etat(
      [
        { id: 1, status: 'encours', pending: true },
        { id: 2, status: 'tenu' },
        { id: 3, status: 'encours', req: true },
        { id: 4, status: 'encours', req: true, reqEtat: 'expiree' },
      ],
      [
        { id: 1, type: 'chiche_recu', pid: 9 },
        { id: 2, type: 'received', pid: 1 },
        { id: 3, type: 'received', pid: 2 },
        { id: 4, type: 'invitation', fait: true },
        { id: 5, type: 'moitie', pid: 2 },
        { id: 6, type: 'added', pid: 1 },
      ],
    );
    // chiche_recu + received(pending) + la demande en attente = 3 ; la moitié d'une parole tenue, l'invitation faite, l'ajout : rien
    expect(filAttente(e)).toBe(3);
  });
  test("l'anneau ne compte ni les gardées de côté ni les demandes", () => {
    const e = etat([
      { status: 'tenu' },
      { status: 'encours' },
      { status: 'encours', draft: true },
      { status: 'encours', req: true },
    ]);
    expect(compteAnneau(e)).toEqual({ tenues: 1, enCours: 1 });
  });
});

describe('le bandeau « Garder ta Toile » (v52, C-200 ①) — les écarts en dur : 5 · 10 · 20 paroles, 3 · 7 · 14 jours', () => {
  const J = 864e5;
  const t = 1_800_000_000_000;
  const trois = [{}, {}, {}];
  test('jamais avant la fin de l’onboarding, ni une fois le compte fait', () => {
    expect(rappelDu(etat(trois, [], {}), t)).toBe(false);
    expect(rappelDu(etat(trois, [], { promi_onb: '1', promi_compte: 'fait:1' }), t)).toBe(false);
  });
  test('la première fois : après le troisième Promi, ou deux jours', () => {
    expect(rappelDu(etat([{}, {}], [], { promi_onb: '1' }), t)).toBe(false);
    expect(rappelDu(etat(trois, [], { promi_onb: '1' }), t)).toBe(true);
    expect(rappelDu(etat([{}], [], { promi_onb: '1', promi_debut: String(t - 2 * J) }), t)).toBe(true);
  });
  test('après une réponse : 5 nouvelles paroles ou 3 jours ; après deux « Plus tard », plus jamais', () => {
    const a = { promi_onb: '1', promi_rappel_n: '1', promi_rappel_p: '3', promi_rappel_t: String(t) };
    expect(rappelDu(etat(Array(7).fill({}), [], a), t + J)).toBe(false);
    expect(rappelDu(etat(Array(8).fill({}), [], a), t + J)).toBe(true);
    expect(rappelDu(etat(trois, [], a), t + 3 * J)).toBe(true);
    expect(rappelDu(etat(Array(50).fill({}), [], { ...a, promi_rappel_fin: '1' }), t + 99 * J)).toBe(false);
  });
});

describe('le toucher tolérant (C-239) : à 22 pt au plus, une seule dalle, de moins de 44 pt', () => {
  // une dalle carrée de 30 pt centrée en (100, 100) ; une grande de 80 pt centrée en (300, 300)
  const hit = (x: number, y: number): DalleTouchee | null =>
    Math.abs(x - 100) <= 15 && Math.abs(y - 100) <= 15
      ? { pid: 1, kind: 'promi' }
      : Math.abs(x - 300) <= 40 && Math.abs(y - 300) <= 40
        ? { pid: 2, kind: 'promi' }
        : null;
  test('une petite dalle à 15 pt du doigt est prise ; à 40 pt, non', () => {
    expect(toucheTolerant(hit, 130, 100)?.pid).toBe(1);
    expect(toucheTolerant(hit, 160, 100)).toBeNull();
  });
  // ⚠ LE PROTOTYPE N'APPLIQUE PAS la limite de 44 pt que C-239 décide : sa boucle mesure des carrés jusqu'à 42 pt (`while(a2<44)`), et son
  // refus (`best>=44`) ne peut jamais être vrai — une grande dalle profite aussi de la tolérance. La vraie app est identique au prototype ;
  // l'écart à la décision est signalé à Tom (rapport du lot 1). Ce test écrit le comportement du prototype.
  test('une grande dalle (80 pt) profite aussi de la tolérance, comme dans le prototype', () => {
    expect(toucheTolerant(hit, 350, 300)?.pid).toBe(2);
  });
});
