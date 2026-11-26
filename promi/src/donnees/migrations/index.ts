/**
 * LES MIGRATIONS DU SCHÉMA. Chaque version a sa migration vers la suivante, testée sur l'état réel de Tom (etats/) avant d'être livrée.
 * Aucune perte : une migration qui ne sait pas ranger un champ le garde (`suite`, `autres`).
 *
 * Version 1 (L0) ; version 2 (lot 2a : `brouillon`, 002-brouillon.ts) ; version 3 (lot 5 : `infosCercles`, 003-infos-cercles.ts) — le schéma de src/donnees/schema.ts. La « version 0 » est le stockage du prototype : on y entre par `importer`.
 * Pour ajouter la version 2 : écrire `002-….ts` (une fonction pure, de la version n à n + 1), l'ajouter à MIGRATIONS, monter VERSION_SCHEMA.
 */
import type { Etat } from '../schema.ts';
import { VERSION_SCHEMA } from '../schema.ts';
import { importerEtRelire, type ExportPrototype } from './prototype.ts';
import { migrer1vers2 } from './002-brouillon.ts';
import { migrer2vers3 } from './003-infos-cercles.ts';

type EtatBrut = { schema: number } & Record<string, unknown>;

/** MIGRATIONS[n] mène de la version n à la version n + 1. */
export const MIGRATIONS: Record<number, (e: EtatBrut) => EtatBrut> = { 1: migrer1vers2, 2: migrer2vers3 };

export function estPrototype(x: unknown): x is ExportPrototype {
  if (typeof x !== 'object' || x === null) return false;
  const o = x as Record<string, unknown>;
  return typeof o['promi_state'] === 'string' || (typeof o['ls'] === 'object' && o['ls'] !== null);
}

/** Ce qu'on a lu (un état sauvegardé, ou un export du prototype) → l'état de la version courante. */
export function migrer(
  x: unknown,
  migrations: Record<number, (e: EtatBrut) => EtatBrut> = MIGRATIONS,
  cible: number = VERSION_SCHEMA,
): Etat {
  let e: EtatBrut;
  if (estPrototype(x)) e = importerEtRelire(x) as unknown as EtatBrut;
  else if (typeof x === 'object' && x !== null && typeof (x as EtatBrut).schema === 'number') e = x as EtatBrut;
  else throw new Error('migrer : ni un état versionné, ni un export du prototype');
  if (e.schema > cible) throw new Error(`migrer : l'état est en version ${e.schema}, l'app ne connaît que ${cible}`);
  while (e.schema < cible) {
    const m = migrations[e.schema];
    if (!m) throw new Error(`migrer : aucune migration depuis la version ${e.schema}`);
    const suivant = m(e);
    if (suivant.schema !== e.schema + 1)
      throw new Error(`migrer : la migration ${e.schema} ne mène pas à ${e.schema + 1}`);
    e = suivant;
  }
  return e as unknown as Etat;
}
