/**
 * LA FICHE D'UNE PAROLE (lot 3a, SPEC-ECRANS §4) — ce qu'elle DIT, sans rien peindre : la phrase complète (C-069, Q412 ; `lot-V136-PHRASE`),
 * le mot d'état et sa date passée (C-210 D2, D5 ; `_datePassee`, `_chicheARelever`, `_ficheCotes`), la consigne du geste (C-108, Q463, Q465 ;
 * `ecran()` de `lot-S1B-geo`), les parts à plusieurs (C-115, Q486 ; `lot-V145-PARTS`), et le mode du trait avec sa base (C-210, Q608).
 * Les formes sont celles du prototype, au caractère près ; les tests les portent en dur (tests/unitaires/fiche.test.ts).
 */
import type { Mot, Parole } from '../donnees/schema.ts';
import { elision } from './elision.ts';

/** la phrase de la célébration (v148, C-144 ; `TEXTES_ENGAGEMENT.tenir`) — exceptions nommées au « ! », espace insécable */
export function phraseTenue(p: Parole): string {
  return p.chiche ? 'Défi relevé\u00a0!' : 'Parole tenue\u00a0!';
}

/** la ligne d'état de « juste après » (cadre 101) : « À DEUX » seulement si la parole est faite avec quelqu'un */
export function ligneJusteApres(p: Parole): string {
  const aDeux = (!!p.from && p.from !== 'moi') || (!!p.who && p.who !== 'moi' && p.who !== 'le groupe');
  return (aDeux ? 'TENUE À DEUX' : 'TENUE') + ' · À L\u2019INSTANT';
}

/** au-delà de trois personnes, la phrase dit « … + x personnes » (v136, C-069) */
export const QUELQUES = 3;

/** les personnes d'un champ (« Rachel, Marion et Nico ») — jamais « moi » ; « tout le monde » d'une parole d'un Cercle : ses membres */
export function gens(v: unknown, membres?: readonly string[]): string[] {
  const w = (typeof v === 'string' ? v : '').trim();
  if (!w || /^moi$/i.test(w)) return [];
  if (/groupe|nu[ée]e|tout le monde/i.test(w) && membres && membres.length) return membres.slice();
  return w
    .split(/\s*[,·]\s*|\s+et\s+/)
    .map((x) => x.trim())
    .filter((x) => x && !/^moi$/i.test(x));
}

/** un morceau de la phrase : du texte, un nom (qui se touche : la fiche de la personne), ou « + x personnes » (qui déroule la liste) */
export type Morceau = { t: string } | { nom: string } | { plus: number };

export interface Phrase {
  morceaux: Morceau[];
  /** le texte entier, tel qu'on le lit */
  txt: string;
}

export const champ = (p: Parole, k: string): unknown => (p as unknown as Record<string, unknown>)[k] ?? p.suite?.[k];

/** reçue : `from` n'est pas moi */
export function recue(p: Parole): boolean {
  const f = String(p.from || 'moi').trim();
  return !!f && !/^moi$/i.test(f);
}

function liste(L: string[], deplie: boolean): Morceau[] {
  const n = L.length;
  const N = (x: string): Morceau => ({ nom: x });
  if (n <= QUELQUES || deplie) {
    if (n === 1) return [N(L[0]!)];
    const out: Morceau[] = [];
    L.slice(0, n - 1).forEach((x, i) => {
      if (i) out.push({ t: ', ' });
      out.push(N(x));
    });
    out.push({ t: ' et ' }, N(L[n - 1]!));
    return out;
  }
  return [N(L[0]!), { t: ', ' }, N(L[1]!), { t: ' ' }, { plus: n - 2 }];
}

function texte(m: Morceau[]): string {
  return m.map((x) => ('t' in x ? x.t : 'nom' in x ? x.nom : '+ ' + String(x.plus) + ' personnes')).join('');
}

/**
 * la phrase complète d'une fiche Promi ou Chiche (jamais d'un Cercle, ni d'un gardé de côté) ; le titre n'y est PAS (il reste seul, le plus
 * grand texte de la fiche). « de » s'élide devant la parole.
 */
export function phraseFiche(p: Parole, deplie = false, membres?: readonly string[]): Phrase | null {
  if (p.draft || champ(p, 'nuee') === true) return null;
  const D = elision(p.title);
  const W = gens(p.who, membres);
  const A = gens(champ(p, 'avec'));
  const from = String(p.from || 'moi').trim();
  const r = recue(p);
  let m: Morceau[];
  if (p.chiche) {
    const TU = 't’es pas chiche';
    const VOUS = 'vous êtes pas chiches';
    if (r) m = [{ nom: from }, { t: ' me dit : ' + TU }];
    else {
      const C = W.slice();
      for (const x of A) if (!C.includes(x)) C.push(x);
      m = C.length ? [...liste(C, deplie), { t: ', ' + (C.length > 1 ? VOUS : TU) }] : [{ t: 'T’es pas chiche' }];
    }
  } else if (r) m = [{ nom: from }, { t: ' me promet' }];
  else if (champ(p, 'req')) {
    const L = W.length ? W : [String(p.who || '')];
    m = [...liste(L, deplie), { t: ', ' + (W.length > 1 ? 'promettez-moi' : 'promets-moi') }];
  } else if (!W.length) m = [{ t: 'Je me promets' }];
  else m = [{ t: 'Je promets à ' }, ...liste(W, deplie)];
  m.push({ t: ' ' + D });
  // les morceaux de texte voisins se fondent (la page + rend une suite de textes comme un seul nœud)
  const out: Morceau[] = [];
  for (const x of m) {
    const der = out[out.length - 1];
    if ('t' in x && der && 't' in der) der.t += x.t;
    else out.push({ ...x });
  }
  return { morceaux: out, txt: texte(out) };
}

/** un Chiche reçu et pas encore relevé (D2) */
export function chicheARelever(p: Parole): boolean {
  return !!(p.chiche && p.status !== 'tenu' && champ(p, 'chicheEtat') !== 'releve' && recue(p));
}

const MOIS = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.'];

/** une échéance passée, écrite comme une date (D5) : « 12 oct. » — `null` si la parole n'en a pas */
export function datePassee(p: Parole, aujourdhui: Date): string | null {
  if (p.draft || p.status === 'tenu' || p.due == null || Number.isNaN(+p.due) || +p.due >= 0) return null;
  let d: Date;
  if (p.ech?.iso && /^\d{4}-\d{2}-\d{2}$/.test(p.ech.iso)) {
    const [a, mo, j] = p.ech.iso.split('-').map(Number) as [number, number, number];
    d = new Date(a, mo - 1, j);
  } else {
    d = new Date(aujourdhui);
    d.setDate(d.getDate() + Math.round(+p.due));
  }
  return String(d.getDate()) + ' ' + MOIS[d.getMonth()]!;
}

/** la ligne d'état : le mot, puis « · » et la date passée s'il y en a une ; `tenu` : la mention se marque en amande (v18) */
export function ligneEtat(p: Parole, aujourdhui: Date): { texte: string; tenu: boolean } {
  const tenu = p.status === 'tenu';
  let mot: string;
  if (p.chiche) mot = tenu ? (champ(p, 'avec') ? 'TENU À DEUX' : 'TENUE') : chicheARelever(p) ? 'À RELEVER' : 'LANCÉ';
  else mot = tenu ? 'TENUE' : 'EN COURS';
  const d = datePassee(p, aujourdhui);
  return { texte: mot + (d ? ' · ' + d.toUpperCase() : ''), tenu };
}

// ── les parts (C-115) ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────

/** qui doit tenir (`tenants` de lot-V145-PARTS) : 'moi' ou des prénoms */
export function tenants(p: Parole): string[] {
  const T: string[] = [];
  const aj = (x: string): void => {
    const v = x.trim();
    if (v && !T.includes(v)) T.push(v);
  };
  if (p.draft || champ(p, 'nuee') === true) return ['moi'];
  const W = gens(p.who);
  const A = gens(champ(p, 'avec'));
  const r = recue(p);
  if (p.chiche) {
    if (r) {
      aj('moi');
      A.forEach(aj);
    } else {
      W.forEach(aj);
      A.forEach(aj);
      if (!T.length) aj('moi');
    }
  } else if (r) aj(String(p.from));
  else if (champ(p, 'req')) {
    W.forEach(aj);
    if (!T.length) aj('moi');
  } else if (p.nuee && A.length) {
    aj('moi');
    A.forEach(aj);
  } else aj('moi');
  return T;
}

export interface EtatParts {
  T: string[];
  n: number;
  faites: string[];
  reste: string[];
  moi: boolean;
  moiFait: boolean;
}

export function etatParts(p: Parole): EtatParts {
  const T = tenants(p);
  const fait = (x: string): boolean => !!p.parts?.[x];
  return {
    T,
    n: T.length,
    faites: T.filter(fait),
    reste: T.filter((x) => !fait(x)),
    moi: T.includes('moi'),
    moiFait: fait('moi'),
  };
}

export function aPlusieurs(p: Parole): boolean {
  return !p.draft && tenants(p).length >= 2;
}

/** les initiales sous les parts (deux lettres si deux prénoms commencent pareil) ; `moi` : le prénom de l'utilisateur */
export function initiales(T: readonly string[], moiNom: string): string[] {
  const N = T.map((x) => (/^moi$/i.test(x) ? moiNom : x));
  const I = N.map((n) => n.charAt(0).toUpperCase());
  return I.map((c, i) => (I.some((d, j) => j !== i && d === c) ? N[i]!.slice(0, 2).toUpperCase() : c));
}

// ── la consigne et le trait ─────────────────────────────────────────────────────────────────────────────────────────────────────────────

/** le mot du geste sous le trait (ou `null` : rien à tracer) */
export function consigne(p: Parole, moiNom = 'Moi'): string | null {
  if (p.draft) return p.chiche ? 'trace pour lancer' : 'trace pour planter';
  if (p.status === 'tenu') return null;
  if (aPlusieurs(p)) {
    const S = etatParts(p);
    if (S.moi && !S.moiFait) return 'trace pour tenir';
    const nom = (x: string): string => (/^moi$/i.test(x) ? moiNom : x);
    if (S.reste.length === 1) return 'à ' + nom(S.reste[0]!) + ' de tracer sa part';
    return 'à chacun de tracer sa part';
  }
  if (p.chiche && !champ(p, 'avec')) {
    const q = String(p.who || '').trim();
    if (!q || /^(moi|soi|toi)$/i.test(q)) return 'trace pour lancer';
    return /,|\+|\bet\b/.test(q) ? 'à chacun de tracer sa part' : 'à ' + q + ' de tracer sa part';
  }
  return 'trace pour tenir';
}

export type ModeTrait = 'moitie' | 'complet' | 'duo' | 'points';

export interface Trait {
  mode: ModeTrait;
  base: number;
  amp: number;
  /** une parole tenue qui porte un mot ou une note : sa base reste 286 (la carte du mot) */
  carte: boolean;
}

/** le mode du trait et sa base (`ecran()` : 286 · tenue 362, 286 avec un mot · tenu à deux 334 ; amplitude 36) */
export function traitFiche(p: Parole): Trait {
  const tenu = p.status === 'tenu';
  const duo = !!(p.chiche && champ(p, 'avec'));
  const note = champ(p, 'note');
  const aMot = (typeof note === 'string' && !!note.trim()) || !!p.comments?.length;
  if (p.draft) return { mode: 'points', base: 286, amp: 36, carte: false };
  if (duo && tenu) return { mode: 'duo', base: 334, amp: 36, carte: false };
  if (tenu)
    return aMot
      ? { mode: 'complet', base: 286, amp: 36, carte: true }
      : { mode: 'complet', base: 362, amp: 36, carte: false };
  return { mode: 'moitie', base: 286, amp: 36, carte: false };
}

/** UN MOT NEUF (C-253, `_motNeuf` de lot-V184B-MOTS) : écrit par un autre — ni « moi », ni mon prénom — et pas encore vu */
export function motNeuf(m: Mot, moi: string): boolean {
  const b = String(m.by || 'moi').trim();
  return !m.vu && !(/^moi$/i.test(b) || (!!moi && b === moi));
}
/** le nombre de mots neufs d'une parole (`_motsNeufs`) */
export const motsNeufs = (p: Parole, moi: string): number => (p.comments ?? []).filter((m) => motNeuf(m, moi)).length;
