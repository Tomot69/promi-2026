/**
 * LE TRACÉ DES LETTRES (C-125, C-279 : le seul langage pour tracer et détracer) — le module repris du prototype, derrière une interface
 * typée. Le module (src/animation/repris/trace-lettres.js et ses trois tables de chemins) est une copie octet pour octet ; il prend son
 * temps de l'horloge unique (installée à sa place, src/animation/horloge.ts).
 * L0 : le chargement et l'interface. Le premier écran qui trace (lot 2, la page +) s'en sert.
 */
import traceSource from '../repris/trace-lettres.js?raw';
import cheminsGilbert from '../repris/trace-chemins-gilbert.js?raw';
import cheminsAtkinson from '../repris/trace-chemins-atkinson.js?raw';
import cheminsPromiLate from '../repris/trace-chemins-promilate.js?raw';

export interface Segment {
  t: string;
  couleur?: string;
  police?: string;
  classe?: string;
  style?: string;
}

export interface OptionsTrace {
  cps?: number;
  vitesse?: number;
  inverse?: boolean;
  preparer?: boolean;
  arme?: boolean;
  /** rappel de fin (le module : `surFin`) ; interrompu si `stop()` l'a coupé */
  surFin?: (r: { interrompu: boolean }) => void;
}

export interface ControleTrace {
  stop(): void;
  lance?(): void;
  accelere?(k: number): void;
  /** la lettre en cours, la part du texte réel déjà montrée, le total, les lettres en cours, le temps de plume */
  etat(): { glyphe: number; texteReel: number; total: number; actives: number[]; t: number };
}

export interface TraceLettres {
  trace(cible: HTMLElement, contenu: null | string | Segment[], options?: OptionsTrace): ControleTrace;
  actif(): boolean;
}

let charge: TraceLettres | null = null;

function injecter(src: string, nom: string): void {
  const s = document.createElement('script');
  s.text = src + '\n//# sourceURL=' + nom;
  document.head.appendChild(s);
}

export function chargerTrace(): TraceLettres {
  if (charge) return charge;
  injecter(cheminsGilbert, 'trace-chemins-gilbert.js');
  injecter(cheminsAtkinson, 'trace-chemins-atkinson.js');
  injecter(cheminsPromiLate, 'trace-chemins-promilate.js');
  injecter(traceSource, 'trace-lettres.js');
  const t = (window as unknown as { TraceLettres?: TraceLettres }).TraceLettres;
  if (!t) throw new Error("tracé : le module n'a pas été posé");
  charge = t;
  return t;
}
