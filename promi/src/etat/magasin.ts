/**
 * LE MAGASIN — l'état unique de l'app (règle : « un état unique, un seul propriétaire par information »).
 *
 * Toute modification passe par une ACTION nommée ; aucun écran n'écrit l'état. L'action écrit le stockage tout de suite, dans la tâche du
 * geste (C-226), puis prévient les abonnés. Les abonnés reçoivent l'état et le nom de l'action ; ils comparent avant d'agir.
 */
import type { Brouillon, CouleurDalle, Etat, MondeDalle, Mot, Parole, Place } from '../donnees/schema.ts';
import { tirer } from '../metier/exemples.ts';
import { etatVide } from '../donnees/schema.ts';
import { migrer } from '../donnees/migrations/index.ts';
import { minuit, poserCles, recompterEcheances, tombe } from '../metier/relecture.ts';
import { aPlusieurs, etatParts } from '../metier/fiche.ts';
import { ligneFil } from '../metier/fil.ts';
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
  /**
   * C-237, C-226 : PLANTER une parole (Promi, Chiche) — écrite dans la tâche du trait, avant toute animation ; son monde figé (v30) ; une ligne
   * du Fil (le prototype : `#addPromi`, `P()`). Rend son id.
   */
  planter(
    p: {
      titre: string;
      who: string;
      chiche: boolean;
      sens: 'soi' | 'faire' | 'demander';
      avec: string;
      note: string;
      monde: MondeDalle;
      due: number | null;
      dueISO: string | null;
      cercle: string | null;
      fichiers: string[];
      /** le dessin de la page + (C-042) : il suit la parole */
      dessin?: unknown;
      /** la photo importée sur la page + (lot-PHOTO, une adresse `data:`) : elle suit la parole (« sur la page +, la photo se pose sur le brouillon
       * de phrase, et suivra la promesse à la plantation ») */
      photo?: string | null;
      /** son cadrage au doigt (C-085 : « il suit la photo à la plantation ») */
      photoCadre?: unknown;
    },
    maintenant: number,
  ): number;
  /** C-306 : créer un Cercle (son nom, ses membres) — rien d'autre ; une ligne du Fil (le prototype : `#addNuee`). Rend sa clé. */
  /** un Cercle créé ; son dessin (C-042), gardé par Cercle dans la clé du prototype `promi_dessins_cercle` */
  creerCercle(nom: string, membres: string[], maintenant: number, dessin?: unknown): string;
  /**
   * TENIR (lot 3a-2 ; le prototype : le clic « tenue » de `#segStatus`, `lot-S5`, `lot-V145-PARTS`, `lot-V149-VALIDATION`) — le trait tracé
   * jusqu'au bout sur une fiche. Seul (ou la dernière part) : la parole passe tenue (`trace`, `vuTenue.moi`, une ligne du Fil, une parole
   * récurrente renaît) → « tenue ». À plusieurs, ma part n'étant pas la dernière : `parts.moi` seul → « part ». Je ne suis pas de ceux qui
   * tiennent, ou déjà tenue : rien → « rien ».
   */
  tenir(id: number, trace: Array<{ x: number; y: number }>, maintenant: number): 'tenue' | 'part' | 'rien';
  /**
   * C-280 : RENOMMER une parole (son titre modifié sur sa fiche ; le prototype : `sort()` de lot-V203-TITRE) — le titre neuf partout ; la clé
   * de plantation gardée (Q621 : le moteur la lit, la dalle garde sa forme) ; les lignes du Fil qui la citent, réécrites ; sa dernière action.
   */
  renommer(id: number, titre: string, maintenant: number): void;
  /**
   * PEAUFINER une parole plantée (lot 3b ; le prototype : les réglages de `lot-S2` sur une fiche) — l'échéance (AVANT : des jours, une date du
   * calendrier, ou « en l’air »), le Cercle, la note, les pièces jointes, le trait. Rien d'autre : une parole tenue le reste (R-005 — le
   * prototype la repassait « en cours » quand on changeait son échéance : un vestige d'avant les deux états, v173).
   */
  peaufiner(id: number, champs: ChampsPeaufiner, maintenant: number): void;
  /**
   * EFFACER une parole (lot 3b-1b ; le prototype : `_v16SupprimerPromi`, v187) — elle quitte la Toile et toutes les listes ; sa pierre tombale
   * (`id|titre`) est posée : une parole effacée ne revient jamais (`sansTombes`, à chaque relecture). Écrit tout de suite (C-226). Rend ce
   * qu'il faut pour l'annuler (la parole et sa place dans la liste), ou null.
   */
  effacer(id: number): { parole: Parole; rang: number } | null;
  /** « Annuler » après un effacement : la parole revient à sa place, sa pierre tombale est retirée (`_deterrer`) */
  deterrer(x: { parole: Parole; rang: number }): void;
  /**
   * UN MOT envoyé sur une fiche (lot 3b-2 ; le prototype : `envoie` de lot-V145-COMM, C-260) — signé de mon prénom, vu (mon mot n'est jamais
   * « neuf » pour moi) ; une ligne du Fil (« Tu as commenté « … » · à qui »). Écrit tout de suite (C-226).
   */
  ajouterMot(id: number, texte: string, moi: string, maintenant: number): void;
  /** C-253 : les mots que la fiche a montrés (clés `date|auteur|texte`) sont vus — rien d'autre ne change (voir n'est pas agir : ni `derAct`, ni le Fil) */
  motsVus(id: number, cles: readonly string[]): void;
  /**
   * LE BOUTON PHOTO D'UNE FICHE (v117, v118, v140 ; `_photoMenu` du prototype) : `photo` une adresse `data:` (elle REMPLACE le dessin — il n'en
   * reste rien, C-085 —, son cadrage repart de zéro) ou null (retirée) ; `origine` : la dalle d'origine (vrai) ou du Studio (faux) — elle retire
   * la photo. Rien d'autre ne change (ni `derAct` : le prototype ne la comptait pas).
   */
  photo(id: number, o: { photo?: string | null; origine?: boolean }): void;
  /** C-085, C-098 : le cadrage de la photo (z, dx, dy, a ; `n` la longueur de son adresse), écrit à la fin du geste — rien d'autre ne change */
  cadrer(id: number, c: { z: number; dx: number; dy: number; a?: number; n: number }): void;
  /**
   * C-042 : le dessin de la parole (posé, en cours, masqué) ou null (retiré) ; `retirerPhoto` : il vient d'être POSÉ — il remplace la photo
   * de la bande (v140, C-086), il n'en reste rien. Rien d'autre ne change.
   */
  dessin(id: number, d: unknown, retirerPhoto?: boolean): void;
}

export interface ChampsPeaufiner {
  echeance?: { due: number | null; dueISO: string | null; enLair: boolean };
  cercle?: string | null;
  note?: string;
  fichiers?: string[];
  trait?: string;
}

export interface Magasin extends Actions {
  etat(): Readonly<Etat>;
  /** aujourd'hui, à minuit (`?jour=+N` l'avance pour la page, jamais mémorisé — C-160) */
  aujourdhui(): Date;
  /** C-160 : les échéances recomptées contre aujourd'hui (au retour au premier plan) ; rien ne s'écrit si rien ne change */
  recompter(): void;
  abonner(f: Abonne): () => void;
}

/** la clé d'un mot : sa date, son auteur, son texte (un mot n'a pas d'identifiant) */
export function cleMot(m: { d: string; by: string; t: string }): string {
  return `${m.d}|${m.by}|${m.t}`;
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
    // Q621 : chaque parole plantée porte sa clé de plantation, posée à chaque écriture (le prototype : `saveState` enveloppé par lot-V203-CLE)
    e = { ...suivant, paroles: poserCles(suivant.paroles) };
    stockage.ecrire(JSON.stringify(e));
    for (const f of abonnes) f(e, action);
  }

  return {
    etat: () => e,
    aujourdhui,
    recompter() {
      const r = relire(e);
      if (JSON.stringify(r.paroles) !== JSON.stringify(e.paroles)) valider('recompter', r);
    },
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
      const fil = [ligneFil(fid, 'added', `Tu as gardé « ${titre} » de côté`, maintenant, { pid: id }), ...e.fil];
      valider('garderDeCote', { ...e, paroles, fil, compteurs });
      return id;
    },
    planter(p, maintenant) {
      const id = e.compteurs.nid;
      const fid = e.compteurs.fid;
      const suite: Record<string, unknown> = { phraseSens: p.chiche ? 'chiche' : p.sens === 'soi' ? 'faire' : p.sens };
      if (p.chiche) {
        suite['chicheEtat'] = 'lance';
        if (p.avec) suite['avec'] = p.avec;
      } else if (p.sens === 'demander') {
        suite['req'] = true;
        suite['reqEtat'] = 'attente';
        suite['reqLe'] = maintenant;
      }
      if (p.note) suite['note'] = p.note;
      if (p.dueISO) suite['dueISO'] = p.dueISO;
      if (p.fichiers.length) suite['files'] = p.fichiers.slice();
      if (p.dessin) suite['dessin'] = p.dessin;
      if (p.photo) suite['photo'] = p.photo;
      if (p.photo && p.photoCadre) suite['photoCadre'] = p.photoCadre;
      const neuve: Parole = {
        id,
        title: p.titre,
        who: p.who,
        due: p.due,
        intensity: 2,
        status: 'encours',
        from: 'moi',
        recur: null,
        remind: null,
        x: 0,
        y: 0,
        tx: 0,
        ty: 0,
        nuee: p.cercle,
        monde: p.monde,
        derAct: maintenant,
        suite,
      };
      if (p.chiche) neuve.chiche = true;
      const texte = `Tu as planté « ${p.titre} »${p.who && p.who !== 'moi' ? ` pour ${p.who}` : ''}`;
      valider('planter', {
        ...e,
        paroles: [...e.paroles, neuve],
        fil: [ligneFil(fid, 'added', texte, maintenant, { pid: id }), ...e.fil],
        compteurs: { nid: id + 1, fid: fid + 1 },
      });
      return id;
    },
    renommer(id, titre, maintenant) {
      const p = e.paroles.find((q) => q.id === id);
      if (!p || p.title === titre) return;
      const avant = p.title;
      const neuve: Parole = { ...p, title: titre, derAct: maintenant };
      if (neuve.cle == null && !p.draft) neuve.cle = avant;
      // les lignes du Fil citent le titre entre guillemets — insécables depuis v21 (`insecable`) : les deux formes sont réécrites (le
      // prototype ne cherchait que la forme à espaces ordinaires, et ne réécrivait donc plus rien : écart nommé, JUGES-TESTS 3a-4)
      const NB = '\u00a0';
      const fil = e.fil.map((f) =>
        f.pid === id && typeof f.text === 'string'
          ? {
              ...f,
              text: f.text
                .split(`«${NB}${avant}${NB}»`)
                .join(`«${NB}${titre}${NB}»`)
                .split(`« ${avant} »`)
                .join(`«${NB}${titre}${NB}»`),
            }
          : f,
      );
      valider('renommer', { ...e, paroles: e.paroles.map((q) => (q.id === id ? neuve : q)), fil });
    },
    effacer(id) {
      const rang = e.paroles.findIndex((q) => q.id === id);
      const p = e.paroles[rang];
      if (!p) return null;
      const k = tombe(p);
      const effacees = e.effacees.includes(k) ? e.effacees : [...e.effacees, k].slice(-300);
      valider('effacer', { ...e, paroles: e.paroles.filter((q) => q.id !== id), effacees });
      return { parole: p, rang };
    },
    deterrer(x) {
      if (e.paroles.some((q) => q.id === x.parole.id)) return;
      const k = tombe(x.parole);
      const paroles = [...e.paroles];
      paroles.splice(Math.min(x.rang, paroles.length), 0, x.parole);
      valider('deterrer', { ...e, paroles, effacees: e.effacees.filter((t) => t !== k) });
    },
    ajouterMot(id, texte, moi, maintenant) {
      const p = e.paroles.find((q) => q.id === id);
      const t = texte.trim();
      if (!p || !t) return;
      const mot: Mot = { t, d: new Date(maintenant).toISOString(), by: moi, vu: true };
      const neuve: Parole = { ...p, comments: [...(p.comments ?? []), mot], derAct: maintenant };
      const recu = !!p.from && !/^moi$/i.test(p.from);
      const au = p.nuee ? (e.cercles[p.nuee] ?? p.nuee) : recu ? p.from : p.who;
      const fid = e.compteurs.fid;
      const ligne = ligneFil(
        fid,
        'comment',
        `Tu as commenté « ${p.title} »${au && !/^moi$/i.test(au) ? ` · ${au}` : ''}`,
        maintenant,
        { pid: id },
      );
      valider('ajouterMot', {
        ...e,
        paroles: e.paroles.map((q) => (q.id === id ? neuve : q)),
        fil: [ligne, ...e.fil],
        compteurs: { ...e.compteurs, fid: fid + 1 },
      });
    },
    photo(id, o) {
      const p = e.paroles.find((q) => q.id === id);
      if (!p) return;
      const suite: Record<string, unknown> = { ...(p.suite ?? {}) };
      if (o.photo !== undefined) {
        if (o.photo) {
          suite['photo'] = o.photo;
          Reflect.deleteProperty(suite, 'dessin');
        } else Reflect.deleteProperty(suite, 'photo');
        Reflect.deleteProperty(suite, 'photoCadre');
      }
      if (o.origine !== undefined) {
        if (o.origine) suite['dalleOrigine'] = true;
        else Reflect.deleteProperty(suite, 'dalleOrigine');
        Reflect.deleteProperty(suite, 'photo');
        Reflect.deleteProperty(suite, 'photoCadre');
      }
      valider('photo', { ...e, paroles: e.paroles.map((q) => (q.id === id ? { ...p, suite } : q)) });
    },
    cadrer(id, c) {
      const p = e.paroles.find((q) => q.id === id);
      if (!p || typeof p.suite?.['photo'] !== 'string') return;
      const suite: Record<string, unknown> = { ...p.suite, photoCadre: { ...c } };
      valider('cadrer', { ...e, paroles: e.paroles.map((q) => (q.id === id ? { ...p, suite } : q)) });
    },
    dessin(id, d, retirerPhoto = false) {
      const p = e.paroles.find((q) => q.id === id);
      if (!p) return;
      const suite: Record<string, unknown> = { ...(p.suite ?? {}) };
      if (d) suite['dessin'] = d;
      else Reflect.deleteProperty(suite, 'dessin');
      if (retirerPhoto) {
        Reflect.deleteProperty(suite, 'photo');
        Reflect.deleteProperty(suite, 'photoCadre');
      }
      valider('dessin', { ...e, paroles: e.paroles.map((q) => (q.id === id ? { ...p, suite } : q)) });
    },
    motsVus(id, cles) {
      const p = e.paroles.find((q) => q.id === id);
      if (!p?.comments?.length || !cles.length) return;
      const C = new Set(cles);
      let n = 0;
      const comments = p.comments.map((m) => {
        if (m.vu || !C.has(cleMot(m))) return m;
        n++;
        return { ...m, vu: true };
      });
      if (!n) return;
      valider('motsVus', { ...e, paroles: e.paroles.map((q) => (q.id === id ? { ...p, comments } : q)) });
    },
    peaufiner(id, champs, maintenant) {
      const p = e.paroles.find((q) => q.id === id);
      if (!p || p.draft) return;
      const suite: Record<string, unknown> = { ...(p.suite ?? {}) };
      let neuve: Parole = { ...p, derAct: maintenant, suite };
      const pose = (k: string, v: unknown): void => {
        if (v == null || v === '' || v === false || (Array.isArray(v) && !v.length)) Reflect.deleteProperty(suite, k);
        else suite[k] = v;
      };
      const ech = champs.echeance;
      if (ech) {
        neuve.due = ech.enLair ? null : ech.due;
        delete neuve.ech;
        pose('dueISO', ech.enLair ? null : ech.dueISO);
        pose('enLair', ech.enLair);
        suite['dueChoisi'] = true;
        neuve = recompterEcheances([neuve], aujourdhui())[0]!;
      }
      if (champs.cercle !== undefined) neuve.nuee = champs.cercle;
      if (champs.note !== undefined) pose('note', champs.note);
      if (champs.fichiers) pose('files', champs.fichiers.slice());
      if (champs.trait) suite['trait'] = champs.trait;
      valider('peaufiner', { ...e, paroles: e.paroles.map((q) => (q.id === id ? neuve : q)) });
    },
    tenir(id, trace, maintenant) {
      const p = e.paroles.find((q) => q.id === id);
      if (!p || p.draft || p.status === 'tenu') return 'rien';
      const iso = new Date(maintenant).toISOString();
      let parts = p.parts;
      if (aPlusieurs(p)) {
        const S = etatParts(p);
        if (!S.moi) return 'rien';
        if (!S.moiFait) parts = { ...(p.parts ?? {}), moi: iso };
        if (S.reste.some((x) => x !== 'moi')) {
          const avecPart: Parole = { ...p, derAct: maintenant };
          if (parts) avecPart.parts = parts;
          valider('tenir', { ...e, paroles: e.paroles.map((q) => (q.id === id ? avecPart : q)) });
          return 'part';
        }
      }
      const tenue: Parole = {
        ...p,
        status: 'tenu',
        draft: false,
        vuTenue: { ...(p.vuTenue ?? {}), moi: iso },
        derAct: maintenant,
        suite: { ...(p.suite ?? {}), trace: trace.map((t) => ({ x: t.x, y: t.y })) },
      };
      if (parts) tenue.parts = parts;
      let { nid, fid } = e.compteurs;
      const fil = [...e.fil];
      const texte = aPlusieurs(p) ? `Chacun a tracé sa part : « ${p.title} »` : `Tu as tenu « ${p.title} »`;
      const paroles = e.paroles.map((q) => (q.id === id ? tenue : q));
      // une parole récurrente renaît en cours (`regenRecur` : chaque jour, semaine, mois)
      const rec = typeof p.recur === 'string' ? p.recur : null;
      if (rec) {
        const due = ({ daily: 1, weekly: 7, monthly: 30 } as Record<string, number>)[rec] ?? 7;
        const np: Parole = {
          id: nid,
          title: p.title,
          who: p.who,
          due,
          intensity: p.intensity || 2,
          status: 'encours',
          from: p.from,
          recur: rec,
          remind: null,
          x: 0,
          y: 0,
          tx: 0,
          ty: 0,
          nuee: p.nuee ?? null,
          derAct: maintenant,
        };
        if (p.monde) np.monde = p.monde;
        paroles.push(np);
        nid++;
        fil.unshift(ligneFil(fid++, 'added', `↻ « ${p.title} » régénérée`, maintenant, { pid: p.id }));
      }
      fil.unshift(ligneFil(fid++, 'kept', texte, maintenant, { pid: id }));
      valider('tenir', { ...e, paroles, fil, compteurs: { ...e.compteurs, nid, fid } });
      return 'tenue';
    },
    creerCercle(nom, membres, maintenant, dessin) {
      const cle = `n${String(maintenant)}`;
      const autres = { ...e.autres };
      if (dessin) {
        let L: Record<string, unknown> = {};
        try {
          L = (JSON.parse(e.autres['promi_dessins_cercle'] ?? '{}') as Record<string, unknown> | null) ?? {};
        } catch {
          L = {};
        }
        autres['promi_dessins_cercle'] = JSON.stringify({ ...L, [cle]: dessin });
      }
      const fid = e.compteurs.fid;
      const texte = `Tu as créé le Cercle ${nom}${membres.length ? ` · invité ${membres.join(', ')}` : ''}`;
      valider('creerCercle', {
        ...e,
        cercles: { ...e.cercles, [cle]: nom },
        membres: { ...e.membres, [cle]: membres.slice() },
        autres,
        fil: [ligneFil(fid, 'nuee', texte, maintenant), ...e.fil],
        compteurs: { ...e.compteurs, fid: fid + 1 },
      });
      return cle;
    },
  };
}
