/**
 * LE MAGASIN — l'état unique de l'app (règle : « un état unique, un seul propriétaire par information »).
 *
 * Toute modification passe par une ACTION nommée ; aucun écran n'écrit l'état. L'action écrit le stockage tout de suite, dans la tâche du
 * geste (C-226), puis prévient les abonnés. Les abonnés reçoivent l'état et le nom de l'action ; ils comparent avant d'agir.
 */
import type { Brouillon, CouleurDalle, Etat, Parole, Place } from '../donnees/schema.ts';
import { tirer } from '../metier/exemples.ts';
import { etatVide } from '../donnees/schema.ts';
import { migrer } from '../donnees/migrations/index.ts';
import { minuit, recompterEcheances } from '../metier/relecture.ts';
import type { Stockage } from '../donnees/stockage.ts';

export type Abonne = (e: Readonly<Etat>, action: string) => void;

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
  /**
   * l'exemple d'une pastille vide, à l'ouverture de la page + (`lot-EXEMPLES-V20`) : le tirage (src/metier/exemples.ts) et ses traces, gardées
   * dans les clés du prototype (`promi_ex_<type>`, `promi_ex_sac_<type>`, `promi_ex_der_<type>`) — rend le rang de la phrase
   */
  tirerExemple(type: string, longueur: number, fixes: number, alea: () => number): number;
  /** l'exemple « promets-moi » : le rang du prénom (v211, C-309, `promi_ex_prenom`) — il avance d'un cran et rend le nouveau rang */
  avancerPrenom(): number;
  /**
   * « garder de côté » (C-149, v162) : l'état entier de la page + devient un gardé de côté (`draft`, `brouillon`), écrit tout de suite ;
   * un gardé de côté REPRIS (`repris`) est mis à jour, jamais doublé. Le Fil le dit (« Tu as gardé « … » de côté »). Rend son id.
   */
  garderDeCote(b: Brouillon, titre: string, qui: string, repris: number | null, maintenant: number): number;
}

export interface Magasin extends Actions {
  etat(): Readonly<Etat>;
  abonner(f: Abonne): () => void;
}

export function creerMagasin(stockage: Stockage, aujourdhui: () => Date = () => minuit()): Magasin {
  let e: Etat = relire(lire());

  /** à l'ouverture (et à chaque import) : les échéances recomptées contre aujourd'hui (C-160) */
  function relire(x: Etat): Etat {
    return { ...x, paroles: recompterEcheances(x.paroles, aujourdhui()) };
  }
  const abonnes = new Set<Abonne>();

  function lire(): Etat {
    const t = stockage.lire();
    if (!t) return etatVide();
    return migrer(JSON.parse(t));
  }
  function valider(action: string, suivant: Etat): void {
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
    tirerExemple(type, longueur, fixes, alea) {
      const a = e.autres;
      const sacBrut = a['promi_ex_sac_' + type];
      let sac: number[] | null = null;
      try {
        const v = sacBrut ? (JSON.parse(sacBrut) as unknown) : null;
        sac = Array.isArray(v) ? v.map(Number) : null;
      } catch {
        sac = null;
      }
      const derBrut = a['promi_ex_der_' + type];
      const t = tirer(
        longueur,
        fixes,
        {
          n: +(a['promi_ex_' + type] ?? 0) || 0,
          sac,
          der: derBrut == null || derBrut === '' ? null : +derBrut,
        },
        alea,
      );
      const b = { ...a, ['promi_ex_' + type]: String(t.suivant.n), ['promi_ex_der_' + type]: String(t.suivant.der) };
      if (t.suivant.sac !== sac) b['promi_ex_sac_' + type] = JSON.stringify(t.suivant.sac);
      valider('tirerExemple', { ...e, autres: b });
      return t.rang;
    },
    avancerPrenom() {
      const v = e.autres['promi_ex_prenom'];
      const r = v != null && v !== '' && +v >= 0 ? +v : -1;
      const n = (r + 1) % 2;
      valider('avancerPrenom', { ...e, autres: { ...e.autres, promi_ex_prenom: String(n) } });
      return n;
    },
    garderDeCote(b, titre, qui, repris, maintenant) {
      const ancien = repris == null ? undefined : e.paroles.find((p) => p.id === repris && p.draft);
      const nuee = b.nat === 'nuee';
      const champs = (p: Parole): Parole => {
        const q: Parole = { ...p, title: titre, who: nuee ? 'le groupe' : qui, draft: true, brouillon: b };
        if (b.nat === 'chiche') q.chiche = true;
        else delete q.chiche;
        const suite = { ...(p.suite ?? {}) };
        suite['dk'] = nuee ? 'nuee' : 'solo';
        suite['phraseSens'] = b.phrase.sens ?? 'faire';
        if (nuee) suite['nueeMembers'] = b.membres.slice();
        q.suite = suite;
        return q;
      };
      let id: number;
      let paroles: Parole[];
      let compteurs = e.compteurs;
      if (ancien) {
        id = ancien.id;
        paroles = e.paroles.map((p) => (p.id === id ? champs(p) : p));
      } else {
        id = e.compteurs.nid;
        compteurs = { ...compteurs, nid: id + 1 };
        const neuve: Parole = {
          id,
          title: titre,
          who: qui,
          due: 30,
          intensity: 2,
          status: 'encours',
          from: 'moi',
          recur: null,
          remind: null,
          x: 0,
          y: 0,
          tx: 0,
          ty: 0,
          nuee: null,
          derAct: maintenant,
        };
        paroles = [...e.paroles, champs(neuve)];
      }
      const fid = compteurs.fid;
      compteurs = { ...compteurs, fid: fid + 1 };
      const fil = [
        { id: fid, type: 'added', text: `Tu as gardé « ${titre} » de côté`, pid: id, t: 'à l’instant', ts: maintenant },
        ...e.fil,
      ];
      valider('garderDeCote', { ...e, paroles, fil, compteurs });
      return id;
    },
  };
}
