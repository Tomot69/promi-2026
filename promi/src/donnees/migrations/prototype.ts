/**
 * L'IMPORT DE L'EXPORT DU PROTOTYPE (`app.html?export=1` → etats/tom-*.json) — la « migration 0 → 1 ».
 *
 * Un export porte `ls`, tout le stockage de l'appareil du prototype (clé → chaîne). Rien ne se perd : ce que le schéma v1 nomme est
 * rangé à sa place ; le reste d'une parole va dans `suite` ; les autres clés de l'appareil vont dans `autres`, telles quelles.
 * La preuve : `versPrototype(importer(x))` redonne le stockage d'origine (tests/unitaires/import.test.ts, sur les exports de Tom).
 *
 * Deux transformations, et seulement deux, viennent de décisions de Tom que le prototype applique lui-même à la relecture :
 *  · C-210 (v173) : `status: 'rate'` redevient `'encours'` (`_migreEtats`) ;
 *  · la clé `setItem` d'un export n'est pas une donnée : c'est le texte d'une fonction (le `localStorage.setItem` enveloppé par la
 *    boîte noire, énuméré par l'export). Elle est écartée.
 */
import type { CouleurDalle, Etat, EvenementFil, Mot, Parole, Place, Reglages, Studio } from '../schema.ts';
import { VERSION_SCHEMA, etatVide } from '../schema.ts';
import { figerDalles, poserCles, reparerPlaces, sansTombes } from '../../metier/relecture.ts';

export type StockagePrototype = Record<string, string>;

/** Un export du prototype, ou directement son stockage (les états de banc-etats/). */
export interface ExportPrototype {
  ls?: StockagePrototype;
  quand?: string;
  version?: unknown;
  [cle: string]: unknown;
}

const CLES_RANGEES = [
  'promi_state',
  'promi_studio',
  'promi_nueplace',
  'promi_prenom',
  'promi_graine',
  'promi_theme',
] as const;
const CLES_ECARTEES = ['setItem'] as const;

const CHAMPS_PAROLE = [
  'id',
  'title',
  'who',
  'due',
  'intensity',
  'status',
  'from',
  'recur',
  'remind',
  'x',
  'y',
  'tx',
  'ty',
  'nuee',
  'monde',
  'dalle',
  'place',
  'cle',
  'derAct',
  'ech',
  'draft',
  'chiche',
  'comments',
  'parts',
  'vuTenue',
  'brouillon',
] as const;
const CHAMPS_FIL = ['id', 'type', 'text', 'pid', 't', 'unread', 'ts'] as const;

type Brut = Record<string, unknown>;

function estObjet(v: unknown): v is Brut {
  return typeof v === 'object' && v !== null && !Array.isArray(v);
}

function separer(o: Brut, champs: readonly string[]): { connus: Brut; suite?: Brut } {
  const connus: Brut = {};
  const suite: Brut = {};
  let n = 0;
  for (const [k, v] of Object.entries(o)) {
    if (champs.includes(k)) connus[k] = v;
    else {
      suite[k] = v;
      n++;
    }
  }
  return n ? { connus, suite } : { connus };
}

function parole(o: Brut): Parole {
  const { connus, suite } = separer(o, CHAMPS_PAROLE);
  const p = connus as unknown as Parole;
  if ((p.status as string) === 'rate') p.status = 'encours';
  if (suite) p.suite = suite;
  return p;
}

function evenement(o: Brut): EvenementFil {
  const { connus, suite } = separer(o, CHAMPS_FIL);
  const e = connus as unknown as EvenementFil;
  if (suite) e.suite = suite;
  return e;
}

export function stockageDe(x: ExportPrototype | StockagePrototype): StockagePrototype {
  const ls = x.ls;
  if (estObjet(ls)) return ls;
  return x as StockagePrototype;
}

/** L'export (ou le stockage) du prototype → l'état v1. */
export function importer(x: ExportPrototype | StockagePrototype): Etat {
  const ls = stockageDe(x);
  const e = etatVide();
  const brut = ls['promi_state'];
  const st: Brut = brut ? (JSON.parse(brut) as Brut) : {};
  if (brut && st['v'] !== 1) throw new Error('import : promi_state.v = ' + String(st['v']) + ' (attendu : 1)');

  e.paroles = Array.isArray(st['promises']) ? (st['promises'] as Brut[]).map(parole) : [];
  e.effacees = Array.isArray(st['effacees']) ? (st['effacees'] as string[]) : [];
  e.cercles = estObjet(st['NUE']) ? (st['NUE'] as Record<string, string>) : {};
  e.membres = estObjet(st['NUEEMEM']) ? (st['NUEEMEM'] as Record<string, string[]>) : {};
  e.dallesCercles = estObjet(st['NUEDALLE']) ? (st['NUEDALLE'] as Record<string, CouleurDalle>) : {};
  e.personnes = Array.isArray(st['PEOPLE']) ? (st['PEOPLE'] as unknown[]) : [];
  e.fil = Array.isArray(st['FEED']) ? (st['FEED'] as Brut[]).map(evenement) : [];
  e.filReactions = estObjet(st['feedReacted']) ? st['feedReacted'] : {};
  e.partageMasque = estObjet(st['shareHidden']) ? st['shareHidden'] : {};
  const s = estObjet(st['state']) ? st['state'] : {};
  const reglages: Reglages = {
    theme: ls['promi_theme'] === 'light' ? 'clair' : 'sombre',
    labels: !!s['labels'],
    tri: typeof s['sort'] === 'string' ? s['sort'] : 'inspi',
    humeur: typeof s['mood'] === 'string' ? s['mood'] : 'cobalt',
    notifOn: !!st['notifOn'],
  };
  e.reglages = reglages;
  const studioBrut = ls['promi_studio'] ? (JSON.parse(ls['promi_studio']) as Brut) : null;
  const monde =
    (studioBrut && typeof studioBrut['m'] === 'string' && studioBrut['m']) ||
    (typeof s['structure'] === 'string' ? s['structure'] : 'encre');
  const studio: Studio = {
    monde,
    palette: studioBrut && typeof studioBrut['p'] === 'string' ? studioBrut['p'] : 'signal',
    teinte: studioBrut && typeof studioBrut['h'] === 'number' ? studioBrut['h'] : 0,
    acquis: studioBrut && estObjet(studioBrut['acquis']) ? (studioBrut['acquis'] as Record<string, 1>) : {},
  };
  if (studioBrut && typeof studioBrut['libre'] === 'boolean') studio.libre = studioBrut['libre'];
  e.studio = studio;
  e.placesCercles = ls['promi_nueplace'] ? (JSON.parse(ls['promi_nueplace']) as Record<string, Place>) : {};
  e.utilisateur = {
    prenom: ls['promi_prenom'] ?? null,
    graine: ls['promi_graine'] != null && ls['promi_graine'] !== '' ? +ls['promi_graine'] | 0 : null,
  };
  e.compteurs = {
    nid: typeof st['nid'] === 'number' ? st['nid'] : 1 + Math.max(0, ...e.paroles.map((p) => p.id)),
    fid: typeof st['fid'] === 'number' ? st['fid'] : 1,
  };
  for (const [k, v] of Object.entries(ls)) {
    if ((CLES_RANGEES as readonly string[]).includes(k) || (CLES_ECARTEES as readonly string[]).includes(k)) continue;
    e.autres[k] = v;
  }
  // ce qui permet à versPrototype de rendre le stockage tel qu'il était (une clé absente reste absente)
  const presentes: string[] = CLES_RANGEES.filter((k) => k in ls);
  if ('effacees' in st) presentes.push('promi_state:effacees');
  e.autres['__presentes'] = JSON.stringify(presentes);
  if (studioBrut) e.autres['__studio_m'] = JSON.stringify(studioBrut['m'] ?? null);
  e.autres['__state_structure'] = JSON.stringify(s['structure'] ?? null);
  e.autres['__theme_brut'] = JSON.stringify(ls['promi_theme'] ?? null);
  return e;
}

function remettre(o: { suite?: Record<string, unknown> }): Brut {
  const { suite, ...connus } = o;
  return { ...connus, ...(suite ?? {}) };
}

/**
 * L'import, puis les passes que le prototype applique à chaque relecture (`loadState` : `_sansTombes`, `_reparePlaces`,
 * `_figeDallesManquantes`, `_clePlantation`) — l'état que la vraie app montre est celui que le prototype montrerait.
 */
export function importerEtRelire(x: ExportPrototype | StockagePrototype): Etat {
  const e = importer(x);
  const r = reparerPlaces(sansTombes(e.paroles, e.effacees), e.placesCercles);
  return { ...e, paroles: poserCles(figerDalles(r.paroles)), placesCercles: r.cercles };
}

/**
 * L'état v1 → le stockage du prototype. Il sert la preuve « sans perte » et, au portage, la comparaison au prototype (les tests de
 * rendu chargent le MÊME état des deux côtés).
 */
export function versPrototype(e: Etat): StockagePrototype {
  const ls: StockagePrototype = {};
  const presentes = new Set<string>(JSON.parse(e.autres['__presentes'] ?? '[]') as string[]);
  for (const [k, v] of Object.entries(e.autres)) if (!k.startsWith('__')) ls[k] = v;
  const structure = JSON.parse(e.autres['__state_structure'] ?? 'null') as string | null;
  const state: Brut = {
    mood: e.reglages.humeur,
    structure: structure ?? e.studio.monde,
    sort: e.reglages.tri,
    labels: e.reglages.labels,
  };
  const st: Brut = {
    v: 1,
    promises: e.paroles.map((p) => remettre(p)),
    NUE: e.cercles,
    NUEEMEM: e.membres,
    NUEDALLE: e.dallesCercles,
    PEOPLE: e.personnes,
    FEED: e.fil.map((f) => remettre(f)),
    feedReacted: e.filReactions,
    shareHidden: e.partageMasque,
    state,
    nid: e.compteurs.nid,
    fid: e.compteurs.fid,
    notifOn: e.reglages.notifOn,
  };
  if (presentes.has('promi_state:effacees')) st['effacees'] = e.effacees;
  ls['promi_state'] = JSON.stringify(st);
  if (presentes.has('promi_studio')) {
    const s: Brut = {
      m: JSON.parse(e.autres['__studio_m'] ?? 'null') ?? e.studio.monde,
      p: e.studio.palette,
      h: e.studio.teinte,
    };
    if (e.studio.libre !== undefined) s['libre'] = e.studio.libre;
    s['acquis'] = e.studio.acquis;
    ls['promi_studio'] = JSON.stringify(s);
  }
  if (presentes.has('promi_nueplace')) ls['promi_nueplace'] = JSON.stringify(e.placesCercles);
  if (presentes.has('promi_prenom') && e.utilisateur.prenom != null) ls['promi_prenom'] = e.utilisateur.prenom;
  if (presentes.has('promi_graine') && e.utilisateur.graine != null) ls['promi_graine'] = String(e.utilisateur.graine);
  const themeBrut = JSON.parse(e.autres['__theme_brut'] ?? 'null') as string | null;
  if (presentes.has('promi_theme')) ls['promi_theme'] = themeBrut ?? (e.reglages.theme === 'clair' ? 'light' : 'dark');
  return ls;
}

export const VERSION_IMPORTEE = VERSION_SCHEMA;
export type { Mot };
