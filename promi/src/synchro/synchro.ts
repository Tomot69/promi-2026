/**
 * LA SYNCHRO — l'interface du stockage distant. Firebase s'y branchera en 1.1 (comptes, Cercles partagés, parts à plusieurs, vraies
 * invitations — C-023). En version 1, l'implémentation est LOCALE : tout reste sur l'appareil, rien ne part.
 */
import type { Etat } from '../donnees/schema.ts';

export interface Invitation {
  cercle: string;
  de: string;
  pour: string;
}

export interface Synchro {
  readonly nom: 'locale' | 'firebase';
  /** l'identité de l'appareil ou du compte */
  qui(): Promise<string>;
  /** envoie l'état local (rien en version 1) */
  pousser(e: Readonly<Etat>): Promise<void>;
  /** ce qui a changé ailleurs (rien en version 1) */
  tirer(): Promise<Partial<Etat> | null>;
  /** les invitations reçues (1.1) */
  invitations(): Promise<Invitation[]>;
}

export function synchroLocale(): Synchro {
  return {
    nom: 'locale',
    qui: () => Promise.resolve('appareil'),
    pousser: () => Promise.resolve(),
    tirer: () => Promise.resolve(null),
    invitations: () => Promise.resolve([]),
  };
}
