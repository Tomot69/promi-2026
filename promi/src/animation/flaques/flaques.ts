/**
 * LES FLAQUES (C-130, C-271 : la matière de toutes les transitions) — le module repris du prototype, derrière une interface typée.
 * Copie octet pour octet (src/animation/repris/flaques.js) ; son temps vient de l'horloge unique.
 * L0 : le chargement et l'interface. Le premier écran qui passe en flaques (lot 1, l'accueil) s'en sert.
 */
import flaquesSource from '../repris/flaques.js?raw';

export interface Scene {
  [membre: string]: unknown;
}

export interface Flaques {
  alea(graine: number): () => number;
  Scene: new (...a: unknown[]) => Scene;
  Nappe: new (...a: unknown[]) => unknown;
  floute(...a: unknown[]): unknown;
  [membre: string]: unknown;
}

let charge: Flaques | null = null;

export function chargerFlaques(): Flaques {
  if (charge) return charge;
  const s = document.createElement('script');
  s.text = flaquesSource + '\n//# sourceURL=flaques.js';
  document.head.appendChild(s);
  const f = (window as unknown as { Flaques?: Flaques }).Flaques;
  if (!f) throw new Error("flaques : le module n'a pas été posé");
  charge = f;
  return f;
}
