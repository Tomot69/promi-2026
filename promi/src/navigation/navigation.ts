/**
 * LA NAVIGATION — la seule porte d'un écran à un autre. Un écran ne s'ouvre jamais lui-même : il le demande ici, et l'écran destinataire
 * s'y inscrit (`poser`) quand il est porté. Au lot 1, aucun écran destinataire n'existe encore (la fiche : lot 3a ; la page + : lot 2 ;
 * le Studio : lot 7 ; l'Aura : lot 5 ; l'Index, le Fil : lot 4 ; Partager, les Réglages, l'offre : lot 8 ; le compte : lot 9) : la demande est notée et
 * rien ne s'ouvre. Le journal des demandes sert les tests (toucher une dalle demande SA fiche).
 */
export type Destination =
  'fiche' | 'cercle' | 'pagePlus' | 'studio' | 'aura' | 'index' | 'fil' | 'partager' | 'reglages' | 'offre' | 'compte';

export interface Demande {
  vers: Destination;
  arg?: string | number;
  t: number;
}

export interface Navigation {
  ouvrir(vers: Destination, arg?: string | number): void;
  poser(vers: Destination, ouvrir: (arg?: string | number) => void): void;
  journal(): readonly Demande[];
}

export function creerNavigation(maintenant: () => number): Navigation {
  const portes = new Map<Destination, (arg?: string | number) => void>();
  const notes: Demande[] = [];
  return {
    ouvrir(vers, arg) {
      notes.push(arg === undefined ? { vers, t: maintenant() } : { vers, arg, t: maintenant() });
      if (notes.length > 100) notes.shift();
      portes.get(vers)?.(arg);
    },
    poser(vers, ouvrir) {
      portes.set(vers, ouvrir);
    },
    journal: () => notes,
  };
}
