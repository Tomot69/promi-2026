/**
 * L'INDEX — CE QU'IL LISTE, DANS QUEL ORDRE, ET LES MOTS D'UNE CARTE (le prototype : `buildIndex`, l. 3892 ; `motQui`, `motEtat` de lot-S4 ;
 * « Récents » de lot-V181B-RECENTS, C-245).
 *  · une entrée par Cercle (nommé, ou porté par une parole), puis une par parole — une parole plantée dans un Cercle listé n'a pas d'entrée à elle :
 *    le Cercle tient sa place (cadres 72 et 74) ;
 *  · les gardés de côté (et les demandes) ferment la liste ; « Récents » (le défaut) : la dernière action d'abord (`derAct`), sans action connue la
 *    plus récemment plantée (l'id : toujours sous une heure en ms) ; un Cercle : la plus récente de ses paroles.
 */
import type { Etat, Parole } from '../donnees/schema.ts';
import { champ, datePassee } from './fiche.ts';

export type Filtre = 'tous' | 'suspens' | 'promi' | 'nuees' | 'brouillons' | 'demandes';
export type Tri = 'recent' | 'personne' | 'nuee';
export type Entree = { kind: 'promi'; p: Parole } | { kind: 'nuee'; k: string };

const moiQ = (w: string): boolean => !w || w.toLowerCase() === 'moi';

/** « à Rachel », « au groupe », « aux voisins » (`_aQui`) */
export function aQui(w: string): string {
  return /^le\s/i.test(w) ? 'au ' + w.slice(3) : /^les\s/i.test(w) ? 'aux ' + w.slice(4) : 'à ' + w;
}

/** le sur-titre d'une carte (`motQui`) */
export function motQui(p: Parole): string {
  if (p.draft) return 'gardé de côté';
  const w = (p.who || '').trim();
  if (moiQ(w) && p.from && p.from !== 'moi') return 'de ' + p.from;
  if (moiQ(w)) return 'à moi';
  return aQui(w);
}

/** le mot d'état d'une carte (`motEtat`), et sa date passée (C-210, D5 : « EN COURS · 12 OCT. ») */
export function motEtat(p: Parole, aujourdhui: Date): string {
  let m: string;
  if (p.draft) m = 'GARDÉ DE CÔTÉ';
  else if (p.status === 'tenu') m = p.chiche && champ(p, 'avec') ? 'TENU À DEUX' : 'TENUE';
  else m = p.chiche ? 'LANCÉ' : 'EN COURS';
  const d = datePassee(p, aujourdhui);
  return d ? m + ' · ' + d.toUpperCase() : m;
}

/** la parole est une demande (« promets-moi ») */
const demande = (p: Parole): boolean => !!champ(p, 'req');

/** la dernière action d'une parole (`actP`) : `derAct`, sinon son id */
const actP = (p: Parole): number => (p.derAct != null ? +p.derAct : +p.id || 0);

/** `due` comme le prototype le soustrait : null compte 0, absent n'est pas un nombre (la comparaison ne tranche pas) */
const due = (p: Parole): number => (p.due === null ? 0 : p.due === undefined ? NaN : +p.due);
/** la personne d'une parole (`_personKey`) : celui qui me la promet, sinon à qui je la promets */
const cleP = (p: Parole): string => (p.from && p.from !== 'moi' ? p.from : p.who || '');
const estMoi = (k: string, moi: string): boolean => {
  const x = k.trim().toLowerCase();
  return x === '' || x === 'moi' || x === moi.trim().toLowerCase();
};

/**
 * « Par personne », « Par Cercle » (`ixSortBy`, `_computePersonOrder`) : les personnes dans l'ordre alphabétique (« moi » en dernier), puis le
 * nom, puis l'échéance ; un Cercle par son nom, puis l'échéance — 0 : la comparaison ne tranche pas
 */
function trierPar(tri: Tri, e: Readonly<Etat>, moi: string): (a: Parole, b: Parole) => number {
  if (tri === 'personne') {
    const vus: string[] = [];
    for (const p of e.paroles) {
      if (p.draft) continue;
      const k = estMoi(cleP(p), moi) ? '__moi' : cleP(p);
      if (!vus.includes(k)) vus.push(k);
    }
    const rang = new Map(
      [...vus.filter((k) => k !== '__moi').sort((a, b) => a.localeCompare(b)), '__moi'].map((k, i) => [k, i]),
    );
    return (a, b) => {
      const ka = cleP(a);
      const kb = cleP(b);
      const ra = rang.get(estMoi(ka, moi) ? '__moi' : ka) ?? 999;
      const rb = rang.get(estMoi(kb, moi) ? '__moi' : kb) ?? 999;
      if (ra !== rb) return ra - rb;
      const c = ka.localeCompare(kb);
      return c || due(a) - due(b);
    };
  }
  const nom = (p: Parole): string => (p.nuee ? e.cercles[p.nuee] || p.nuee : '~~');
  return (a, b) => nom(a).localeCompare(nom(b)) || due(a) - due(b);
}

export function entreesIndex(
  e: Readonly<Etat>,
  q = '',
  filtre: Filtre = 'tous',
  tri: Tri = 'recent',
  moi = 'Moi',
): Entree[] {
  const Q = q.trim().toLowerCase();
  const P = e.paroles;
  const nomC = (k: string): string => e.cercles[k] || k;
  const mt = (p: Parole): boolean =>
    !Q || [p.title || '', p.who || '', p.from || '', p.nuee ? nomC(p.nuee) : ''].join(' ').toLowerCase().includes(Q);
  const ent: Entree[] = [];
  if (filtre === 'tous' || filtre === 'nuees') {
    const ks = [...new Set([...P.map((p) => p.nuee).filter((k): k is string => !!k), ...Object.keys(e.cercles)])];
    for (const k of ks)
      if (!Q || nomC(k).toLowerCase().includes(Q) || P.some((p) => p.nuee === k && mt(p)))
        ent.push({ kind: 'nuee', k });
  }
  const listes = new Set(ent.map((x) => (x.kind === 'nuee' ? x.k : '')));
  for (const p of P) {
    if (!mt(p)) continue;
    if (p.nuee && listes.has(p.nuee) && !p.draft) continue;
    if (p.draft) {
      if (filtre !== 'tous' && filtre !== 'brouillons') continue;
    } else if (demande(p)) {
      if (filtre !== 'tous' && filtre !== 'demandes') continue;
    } else {
      if (filtre === 'brouillons' || filtre === 'demandes' || filtre === 'nuees') continue;
      if (filtre === 'suspens' && p.status !== 'encours') continue;
    }
    ent.push({ kind: 'promi', p });
  }
  const plantees = (k: string): Parole[] => P.filter((q) => q.nuee === k && !q.draft);
  const garde = (x: Entree): number =>
    x.kind === 'nuee' ? (plantees(x.k).length ? 0 : 1) : x.p.draft || demande(x.p) ? 1 : 0;
  const cle = (x: Entree): number => (x.kind === 'nuee' ? Math.max(0, ...plantees(x.k).map(actP)) : actP(x.p));
  const ordre = (x: Entree): number => {
    if (x.kind !== 'nuee') return x.p.id;
    const l = P.filter((q) => q.nuee === x.k);
    return l.length ? Math.min(...l.map((q) => q.id)) - 0.5 : 1e9;
  };
  const par = trierPar(tri, e, moi);
  ent.sort((a, b) => {
    const ga = garde(a);
    const gb = garde(b);
    if (ga !== gb) return ga - gb;
    if (tri === 'recent') return cle(b) - cle(a);
    if (a.kind === 'promi' && b.kind === 'promi') {
      const c = par(a.p, b.p);
      if (c) return c;
    } else if (a.kind !== b.kind) return a.kind === 'nuee' ? -1 : 1;
    return ordre(a) - ordre(b);
  });
  return ent;
}
