/**
 * LE STOCKAGE SUR L'APPAREIL. Une écriture atomique, au moment du geste (C-226 : une parole plantée est écrite AVANT toute animation).
 * Une seule clé, un seul écrivain : le magasin (src/etat/magasin.ts).
 */
export interface Stockage {
  lire(): string | null;
  ecrire(texte: string): void;
  effacer(): void;
}

export const CLE_ETAT = 'promi.etat.v1';

export function stockageLocal(cle: string = CLE_ETAT, ls: Storage = localStorage): Stockage {
  return {
    lire: () => ls.getItem(cle),
    ecrire: (t) => {
      ls.setItem(cle, t);
    },
    effacer: () => {
      ls.removeItem(cle);
    },
  };
}

/** Pour les tests : un stockage en mémoire. */
export function stockageMemoire(initial: string | null = null): Stockage & { contenu(): string | null } {
  let c = initial;
  return {
    lire: () => c,
    ecrire: (t) => {
      c = t;
    },
    effacer: () => {
      c = null;
    },
    contenu: () => c,
  };
}
