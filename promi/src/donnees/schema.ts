/**
 * LE SCHÉMA DE DONNÉES, VERSION 2 (v1 en L0 ; v2 au lot 2a : le gardé de côté porte l'état de la page + qui l'a gardé, `brouillon`) (règle de la vraie app : « un schéma versionné avec ses migrations, dès la version 1 »).
 *
 * Source : portage/SPEC-DONNEES.md et SPEC-DONNEES.schema.json (le modèle du prototype). Les noms des champs d'une parole sont ceux du
 * prototype : ils sont la spécification, le moteur les lit tels quels, et l'import de l'export de Tom ne perd rien.
 * Tout champ que le prototype porte et que ce schéma ne nomme pas encore est gardé, intact, dans `suite` (aucune perte : test
 * tests/unitaires/import.test.ts, aller-retour au caractère près).
 *
 * Vocabulaire (CLAUDE.md §2) : le code du prototype dit `nuee`, l'écran dit Cercle ; `draft` = gardé de côté.
 */

export const VERSION_SCHEMA = 3 as const;

/** v173 (C-210) : deux états. `rate` n'existe plus (la migration le rend « en cours »). */
export type EtatParole = 'encours' | 'tenu';

/** [x/W, y/H] et, pour un monde « fait de ses seules paroles », un 1 (C-101, v142). */
export type Place = [number, number] | [number, number, 0 | 1];

export interface MondeDalle {
  m: string;
  p: string;
  h: number;
}

export interface CouleurDalle {
  ci: number;
  lit: number;
  rgb?: number[];
  choisi?: number;
}

export interface Mot {
  t: string;
  d: string;
  by: string;
  vu?: boolean;
  essai?: boolean;
}

export interface Echeance {
  iso: string;
  due: number;
}

/**
 * L'état de la page + gardé avec un gardé de côté (le `p.brouillon` du prototype, v162) : sa nature, la phrase, les personnes, le nom et les
 * membres d'un Cercle. Les champs que le prototype y porte et que la vraie app n'écrit pas encore (l'échéance, la note : Peaufiner, lot 2b)
 * sont gardés tels quels (`suite`).
 */
export interface Brouillon {
  v: 1;
  nat: 'promi' | 'chiche' | 'nuee';
  phrase: { sens?: string; titre?: string; qui?: string; avec?: string; [cle: string]: unknown };
  who: string[];
  sens: string | null;
  nom: string;
  membres: string[];
  [cle: string]: unknown;
}

/** Ce qu'un Cercle porte en propre (v3) : sa DESCRIPTION, ses PIÈCES JOINTES (leurs noms), son TRAIT (un pinceau) — Peaufiner ; SES MOTS (« Un mot… »). */
export interface InfosCercle {
  note?: string;
  fichiers?: string[];
  trait?: string;
  mots?: Mot[];
}

/** Une parole (Promi ou Chiche ; un gardé de côté porte `draft: true`). */
export interface Parole {
  id: number;
  title: string;
  who: string;
  due: number | null;
  intensity: number;
  status: EtatParole;
  from: string;
  recur: unknown;
  remind: unknown;
  x: number;
  y: number;
  tx: number;
  ty: number;
  nuee?: string | null;
  monde?: MondeDalle;
  dalle?: CouleurDalle;
  place?: Place;
  cle?: string;
  derAct?: number;
  ech?: Echeance;
  draft?: boolean;
  chiche?: boolean;
  comments?: Mot[];
  parts?: Record<string, string>;
  vuTenue?: Record<string, string>;
  /** un gardé de côté (`draft`) : l'état ENTIER de la page + qui l'a gardé (C-149, v162 — `lot-V162-GARDER` du prototype) ; v2 */
  brouillon?: Brouillon;
  /** tout autre champ du prototype, gardé tel quel (aucune perte) */
  suite?: Record<string, unknown>;
}

export interface EvenementFil {
  id: number;
  type: string;
  text: string;
  pid?: number;
  t?: string;
  unread?: boolean;
  ts?: number;
  suite?: Record<string, unknown>;
}

export interface Studio {
  monde: string;
  palette: string;
  teinte: number;
  /** le monde était-il gratuit quand il a été choisi (v71) */
  libre?: boolean;
  /** mondes acquis */
  acquis: Record<string, 1>;
}

export interface Reglages {
  theme: 'clair' | 'sombre';
  /** « avec texte » : les titres sur les dalles */
  labels: boolean;
  tri: string;
  humeur: string;
  notifOn: boolean;
}

export interface Etat {
  schema: typeof VERSION_SCHEMA;
  paroles: Parole[];
  /** pierres tombales `id|titre` (v187) */
  effacees: string[];
  /** les Cercles : clé → nom (`NUE`) */
  cercles: Record<string, string>;
  /** les membres de chaque Cercle (`NUEEMEM`) */
  membres: Record<string, string[]>;
  /** la couleur figée de la dalle de chaque Cercle (`NUEDALLE`) */
  dallesCercles: Record<string, CouleurDalle>;
  /** la place gardée de chaque Cercle (`promi_nueplace`) */
  placesCercles: Record<string, Place>;
  /** v3 (lot 5) : ce qu'un Cercle porte en propre — sa description, ses pièces jointes, son trait (le prototype ne les gardait pas), ses mots */
  infosCercles: Record<string, InfosCercle>;
  personnes: unknown[];
  fil: EvenementFil[];
  filReactions: Record<string, unknown>;
  partageMasque: Record<string, unknown>;
  reglages: Reglages;
  studio: Studio;
  utilisateur: { prenom: string | null; graine: number | null };
  compteurs: { nid: number; fid: number };
  /**
   * Les autres clés de l'appareil du prototype (onboarding, guide, Pelote, notifications, murs, phrases suggérées…), gardées telles
   * quelles, sous leur nom. Chaque lot qui porte un écran en reprend les siennes dans le schéma (une migration v1 → v2…).
   */
  autres: Record<string, string>;
}

export function etatVide(): Etat {
  return {
    schema: VERSION_SCHEMA,
    paroles: [],
    effacees: [],
    cercles: {},
    membres: {},
    dallesCercles: {},
    placesCercles: {},
    infosCercles: {},
    personnes: [],
    fil: [],
    filReactions: {},
    partageMasque: {},
    reglages: { theme: 'sombre', labels: true, tri: 'inspi', humeur: 'cobalt', notifOn: false },
    studio: { monde: 'encre', palette: 'signal', teinte: 0, acquis: {} },
    utilisateur: { prenom: null, graine: null },
    compteurs: { nid: 1, fid: 1 },
    autres: {},
  };
}
