/**
 * LA FAÇADE DU MOTEUR DE LA PELOTE (lot 6 ; Tom, 28 nov. 2026 : « Oui, le reprendre » — la CINQUIÈME pièce reprise).
 *
 * Le moteur (`src/moteur/repris/pelote-moteur.js`) est le bloc `lot-AURA-PELOTE-MOTEUR` du prototype, copié OCTET POUR OCTET par
 * `outils/reprendre.py` (vérifié par tests/unitaires/repris.test.ts) : le velours, ses îles, son semis, son peintre (WebGL 2, et son secours au
 * processeur). On ne le corrige jamais ici. Il se pose sur `window.PeloteMoteur` et lit quelques réglages sur `window` (`_peloteGL`,
 * `_peloteReglage`, `_peloteBord`, `_pelotePoints`, `_peloteGLTout`, `_peloteEmpCPU`) : CETTE FAÇADE EST LA SEULE à les toucher — le lint
 * interdit `PeloteMoteur` et `window.PeloteMoteur` partout ailleurs (eslint.config.js).
 *
 * Ses options sont celles du prototype (`opts()` de lot-AURA-PELOTE), passées telles quelles : le moteur les lit sans schéma.
 */
import source from './repris/pelote-moteur.js?raw';

/** un objet d'options ou d'état du moteur, lu et écrit par lui seul */
export type OptionsPelote = Record<string, unknown>;
/** l'état du semis d'une Pelote (le pavage, ses cellules), gardé par l'écran et rendu au moteur */
export type SemisPelote = Record<string, unknown>;
/** les îles (une par parole tenue) */
export type IlesPelote = Record<string, unknown>;

export interface MoteurPelote {
  /** la Pelote par la carte graphique (WebGL 2) ; faux : elle n'a pas pu (le secours `peint` prend la main) */
  peintGL(cv: HTMLCanvasElement, o: OptionsPelote): boolean;
  /** la Pelote au processeur (le secours ; il calcule aussi le creux du doigt, `seulementEtat`) */
  peint(cv: HTMLCanvasElement, o: OptionsPelote): void;
  glDispo(): boolean;
  /** la rampe du velours d'un ton (de l'ombre à la lumière) */
  rampeVelours(base: number[]): number[][];
  atlasAlpha(
    dessin: unknown,
    tailles: unknown,
    ori: unknown,
    niv: unknown,
    a0: number,
    a1: number,
    tour: boolean,
    nv: unknown,
  ): unknown;
  GRAIN_POIL: unknown;
  ORI: unknown;
  NIVA: unknown;
  NVAR: unknown;
  semisPavage(
    nc: number,
    m: number,
    joint: number,
    k: number,
    nbCoul: number,
    tourne: boolean,
    gril: number,
  ): SemisPelote;
  batIles(n: number, pal: unknown, opt: OptionsPelote): IlesPelote;
  m_gestes(n: number, graine: number): unknown;
  retoucheTraces(st: unknown, anciennes: unknown[], nouvelles: unknown[]): number;
}

/** les réglages que le moteur lit sur `window` (ceux que l'écran du prototype pose) */
export interface ReglagesPelote {
  /** faux : jamais la carte graphique (le secours au processeur) */
  gl?: boolean;
  /** la densité du poil : facteur (×1), épaisseur (×1), reflet adouci */
  reglage?: { facteur: number; epaisseur: number; doux: boolean };
  /** vrai : le creux du doigt calculé au processeur (le témoin du juge, v126) */
  empCPU?: boolean;
  /** le contexte de la carte graphique perdu (le Studio en a ouvert d'autres) : l'écran refait ses préparations */
  perdu?: () => void;
}

interface FenetrePelote {
  PeloteMoteur?: MoteurPelote;
  _peloteGL?: boolean;
  _peloteReglage?: ReglagesPelote['reglage'];
  _peloteEmpCPU?: boolean;
  _auraPreInvalide?: () => void;
  _peloteGLEtat?: () => unknown;
}

let charge: MoteurPelote | null = null;

/** le moteur, chargé une fois (son bloc posé tel quel dans la page, comme le prototype le porte) */
export function chargerPelote(): MoteurPelote {
  if (charge) return charge;
  const w = window as unknown as FenetrePelote;
  if (!w.PeloteMoteur) {
    const s = document.createElement('script');
    s.text = source + '\n//# sourceURL=pelote-moteur.js';
    document.head.appendChild(s);
  }
  if (!w.PeloteMoteur) throw new Error("la Pelote : le moteur n'a pas été posé");
  charge = w.PeloteMoteur;
  return charge;
}

/** pose les réglages que le moteur lit (ce qui n'est pas donné reste tel quel) */
export function reglerPelote(r: ReglagesPelote): void {
  const w = window as unknown as FenetrePelote;
  if (r.gl !== undefined) w._peloteGL = r.gl;
  if (r.reglage) w._peloteReglage = r.reglage;
  if (r.empCPU !== undefined) w._peloteEmpCPU = r.empCPU;
  if (r.perdu) w._auraPreInvalide = r.perdu;
}

/** ce que le peintre WebGL dit de lui (le relevé, `?mesure=1`) */
export function etatGLPelote(): unknown {
  const f = (window as unknown as FenetrePelote)._peloteGLEtat;
  return f ? f() : null;
}
