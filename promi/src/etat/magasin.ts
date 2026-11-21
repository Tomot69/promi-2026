/**
 * LE MAGASIN — l'état unique de l'app (règle : « un état unique, un seul propriétaire par information »).
 *
 * Toute modification passe par une ACTION nommée ; aucun écran n'écrit l'état. L'action écrit le stockage tout de suite, dans la tâche du
 * geste (C-226), puis prévient les abonnés. Les abonnés reçoivent l'état et le nom de l'action ; ils comparent avant d'agir.
 */
import type { CouleurDalle, EtatV1, Place } from '../donnees/schema.ts';
import { etatVide } from '../donnees/schema.ts';
import { migrer } from '../donnees/migrations/index.ts';
import { minuit, recompterEcheances } from '../metier/relecture.ts';
import type { Stockage } from '../donnees/stockage.ts';

export type Abonne = (e: Readonly<EtatV1>, action: string) => void;

export interface Actions {
  /** remplace tout l'état par un état importé (l'export du prototype, ou une sauvegarde) */
  importer(x: unknown): void;
  choisirMonde(monde: string): void;
  choisirPalette(palette: string, teinte?: number): void;
  choisirTheme(theme: 'clair' | 'sombre'): void;
  /** le moteur a choisi la place d'une dalle (il la note lui-même, _placeNote) : elle est gardée */
  noterPlaces(
    places: Array<{ id: number; place: Place | undefined; dalle?: CouleurDalle | undefined }>,
    dallesCercles?: Record<string, CouleurDalle>,
  ): void;
  /** le bandeau « Garder ta Toile » de l'accueil a reçu une réponse (v52, C-200 ①) — gardée dans les clés du prototype (`autres`) */
  repondreRappel(reponse: 'oui' | 'non', nParoles: number, maintenant: number): void;
}

export interface Magasin extends Actions {
  etat(): Readonly<EtatV1>;
  abonner(f: Abonne): () => void;
}

export function creerMagasin(stockage: Stockage, aujourdhui: () => Date = () => minuit()): Magasin {
  let e: EtatV1 = relire(lire());

  /** à l'ouverture (et à chaque import) : les échéances recomptées contre aujourd'hui (C-160) */
  function relire(x: EtatV1): EtatV1 {
    return { ...x, paroles: recompterEcheances(x.paroles, aujourdhui()) };
  }
  const abonnes = new Set<Abonne>();

  function lire(): EtatV1 {
    const t = stockage.lire();
    if (!t) return etatVide();
    return migrer(JSON.parse(t));
  }
  function valider(action: string, suivant: EtatV1): void {
    e = suivant;
    stockage.ecrire(JSON.stringify(e));
    for (const f of abonnes) f(e, action);
  }

  return {
    etat: () => e,
    abonner(f) {
      abonnes.add(f);
      return () => abonnes.delete(f);
    },
    importer(x) {
      valider('importer', relire(migrer(x)));
    },
    choisirMonde(monde) {
      if (e.studio.monde === monde) return;
      valider('choisirMonde', { ...e, studio: { ...e.studio, monde } });
    },
    choisirPalette(palette, teinte = 0) {
      valider('choisirPalette', { ...e, studio: { ...e.studio, palette, teinte } });
    },
    choisirTheme(theme) {
      if (e.reglages.theme === theme) return;
      valider('choisirTheme', { ...e, reglages: { ...e.reglages, theme } });
    },
    noterPlaces(places, dallesCercles) {
      // la place (`_placeNote`) et la couleur figée (`_dalleFigee`, Q213) que le moteur a notées sur chaque parole ; et la couleur de
      // chaque Cercle (`NUEDALLE`) — une couleur figée ne se perd jamais : rien ne l'efface ici
      const parId = new Map(places.map((p) => [p.id, p]));
      let change = false;
      const paroles = e.paroles.map((p) => {
        const n = parId.get(p.id);
        if (!n) return p;
        const memePlace = JSON.stringify(n.place) === JSON.stringify(p.place);
        const memeDalle = !n.dalle || JSON.stringify(n.dalle) === JSON.stringify(p.dalle);
        if (memePlace && memeDalle) return p;
        change = true;
        const q = { ...p };
        if (n.place) q.place = n.place;
        else delete q.place;
        if (n.dalle) q.dalle = { ...n.dalle };
        return q;
      });
      let cercles = e.dallesCercles;
      if (dallesCercles && JSON.stringify(dallesCercles) !== JSON.stringify(e.dallesCercles)) {
        cercles = { ...e.dallesCercles, ...dallesCercles };
        change = true;
      }
      if (change) valider('noterPlaces', { ...e, paroles, dallesCercles: cercles });
    },
    repondreRappel(reponse, nParoles, maintenant) {
      const a = { ...e.autres };
      const n = (+(a['promi_rappel_n'] ?? 0) || 0) + 1;
      a['promi_rappel_n'] = String(n);
      a['promi_rappel_p'] = String(nParoles);
      a['promi_rappel_t'] = String(maintenant);
      if (reponse === 'non') {
        const brut = a['promi_rappel_non'];
        // les refus d'avant v164b comptent : sans compteur, le nombre de réponses d'avant
        const non = (brut == null || brut === '' ? Math.max(0, n - 1) : +brut) + 1;
        a['promi_rappel_non'] = String(non);
        if (non >= 2) a['promi_rappel_fin'] = '1';
      }
      valider('repondreRappel', { ...e, autres: a });
    },
  };
}
