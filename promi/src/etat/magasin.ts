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
import { dessinsCercles } from '../metier/cercle.ts';
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
  /**
   * ce que la Pelote garde d'une ouverture à l'autre (lot 6) — l'ordre de ses îles (`promi_pelote_ordre`), la couleur vue (`promi_pelote_vue`), le
   * palier de densité appliqué (`promi_pelote_palier`), le nombre de tenues déjà vues (`promi_pelote_vus`) : dans les clés du prototype (`autres`),
   * sous leur nom ; seules les clés `promi_pelote_*` s'écrivent ici
   */
  noterPelote(cle: string, valeur: string): void;
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
   * PEAUFINER UN CERCLE (lot 5 ; le prototype : le Peaufiner d'une Nuée, `_nueePeaufiner`) — sa DESCRIPTION, ses PIÈCES JOINTES, son TRAIT
   * (`infosCercles`, v3 : le prototype ne les gardait pas). Écrit tout de suite.
   */
  peaufinerCercle(cle: string, champs: { note?: string; fichiers?: string[]; trait?: string }): void;
  /** C-042 : le dessin d'un Cercle (posé, en cours, masqué) ou null (retiré) — dans la clé du prototype, `promi_dessins_cercle` */
  dessinCercle(cle: string, d: unknown): void;
  /**
   * UN MOT sur la fiche d'un Cercle (lot 5 ; `_cercleMots` de lot-V146-CERCLE-MOT, `envoie` de lot-V145-COMM) — signé de mon prénom, vu ; une
   * ligne du Fil (« Tu as commenté « Marseille » · Marseille » : le Cercle est son propre titre et son propre destinataire, comme le prototype).
   */
  motCercle(cle: string, texte: string, moi: string, maintenant: number): void;
  /** C-253 : les mots d'un Cercle que la fiche a montrés sont vus */
  motsVusCercle(cle: string, cles: readonly string[]): void;
  /** les MEMBRES d'un Cercle (`_nqMembers`, l'ajout et la croix) : la liste neuve */
  membresCercle(cle: string, membres: string[]): void;
  /**
   * DISSOUDRE un Cercle (C-192 ; `_nqDissolve(cle, false)`) : ses paroles restent, hors du Cercle ; le Cercle, ses membres et ses réglages
   * partent. Rend ce qu'il faut pour l'annuler (« Annuler », 5 s), ou null.
   */
  dissoudre(cle: string): { cle: string; avant: Etat } | null;
  /** « Annuler » après une dissolution : le Cercle revient tel qu'il était (ce qui a changé depuis reste) */
  rendreCercle(x: { cle: string; avant: Etat }): void;
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
  /**
   * REPORTER depuis le Fil (le prototype : `_fpost`, enveloppé par lot-V151-ECHEANCE, C-160) : l'échéance recomptée contre aujourd'hui ; passée, on
   * compte depuis aujourd'hui ; plus 1, 7 ou 30 jours ; la parole n'attend plus de réponse ; la LIGNE du Fil devient « Tu as reporté : « … » (+1 j) »
   * (elle garde son heure).
   */
  reporter(fid: number, jours: number, maintenant: number): void;
  /** une ligne du Fil touchée est vue (`_filVu`, Q347) — rien d'autre ne change */
  filVu(fid: number): void;
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
  /** À QUI / QUI OSE ? (lot 3b ; le prototype : `_gensFiche('who')`) : les personnes, « moi » si personne */
  qui?: string[];
  /** AVEC (un Chiche : `_gensFiche('avec')`) : ses compagnons, aucun si vide */
  avec?: string[];
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
    // Q621 : chaque parole plantée porte sa clé de plantation, posée à chaque écriture (le prototype : `saveState` enveloppé par lot-V203-CLE) ;
    // C-160 : et sa DATE d'échéance, posée le jour où ses jours sont choisis (le prototype : `saveState` enveloppé par `noteTout`, lot-V151-ECHEANCE)
    // — sans elle, la date n'était posée qu'à la relecture suivante, comptée depuis ce jour-là : une échéance ne passait jamais
    e = { ...suivant, paroles: poserCles(recompterEcheances(suivant.paroles, aujourdhui())) };
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
    noterPelote(cle, valeur) {
      if (!cle.startsWith('promi_pelote_') || e.autres[cle] === valeur) return;
      valider('noterPelote', { ...e, autres: { ...e.autres, [cle]: valeur } });
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
    reporter(fid, jours, maintenant) {
      const f = e.fil.find((x) => x.id === fid);
      if (!f) return;
      const p0 = f.pid != null ? e.paroles.find((x) => x.id === f.pid) : undefined;
      let paroles = e.paroles;
      if (p0) {
        const r = recompterEcheances([p0], aujourdhui())[0]!;
        const due = (r.due != null && +r.due < 0 ? 0 : (r.due ?? 0)) + jours;
        const suite: Record<string, unknown> = { ...(r.suite ?? {}), pending: false, accepted: true };
        const p = recompterEcheances([{ ...r, due, suite, derAct: maintenant }], aujourdhui())[0]!;
        paroles = e.paroles.map((x) => (x.id === p.id ? p : x));
      }
      const lab = jours === 1 ? '+1 j' : jours === 7 ? '+1 sem' : `+${String(jours)} j`;
      const ligne = { ...f, type: 'added', text: `Tu as reporté : « ${p0 ? p0.title : 'un Promi'} » (${lab})` };
      valider('reporter', { ...e, paroles, fil: e.fil.map((x) => (x.id === fid ? ligne : x)) });
    },
    filVu(fid) {
      if (!e.fil.some((f) => f.id === fid && f.unread)) return;
      valider('filVu', { ...e, fil: e.fil.map((f) => (f.id === fid ? { ...f, unread: false } : f)) });
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
      if (champs.qui) neuve.who = champs.qui.length ? champs.qui.join(', ') : 'moi';
      if (champs.avec) pose('avec', champs.avec.join(', '));
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
    peaufinerCercle(cle, champs) {
      if (!(cle in e.cercles)) return;
      const avant = e.infosCercles[cle] ?? {};
      const neuf = { ...avant, ...champs };
      if (JSON.stringify(neuf) === JSON.stringify(avant)) return;
      valider('peaufinerCercle', { ...e, infosCercles: { ...e.infosCercles, [cle]: neuf } });
    },
    dessinCercle(cle, d) {
      if (!(cle in e.cercles)) return;
      const L = dessinsCercles(e.autres);
      if (JSON.stringify(L[cle] ?? null) === JSON.stringify(d ?? null)) return;
      if (d) L[cle] = d;
      else Reflect.deleteProperty(L, cle);
      valider('dessinCercle', { ...e, autres: { ...e.autres, promi_dessins_cercle: JSON.stringify(L) } });
    },
    motCercle(cle, texte, moi, maintenant) {
      const t = texte.trim();
      if (!(cle in e.cercles) || !t) return;
      const nom = e.cercles[cle]!;
      const info = e.infosCercles[cle] ?? {};
      const mot: Mot = { t, d: new Date(maintenant).toISOString(), by: moi, vu: true };
      const fid = e.compteurs.fid;
      const ligne = ligneFil(fid, 'comment', `Tu as commenté « ${nom} » · ${nom}`, maintenant);
      valider('motCercle', {
        ...e,
        infosCercles: { ...e.infosCercles, [cle]: { ...info, mots: [...(info.mots ?? []), mot] } },
        fil: [ligne, ...e.fil],
        compteurs: { ...e.compteurs, fid: fid + 1 },
      });
    },
    motsVusCercle(cle, cles) {
      const info = e.infosCercles[cle];
      if (!info?.mots?.length || !cles.length) return;
      const C = new Set(cles);
      let n = 0;
      const mots = info.mots.map((m) => {
        if (m.vu || !C.has(cleMot(m))) return m;
        n++;
        return { ...m, vu: true };
      });
      if (n) valider('motsVusCercle', { ...e, infosCercles: { ...e.infosCercles, [cle]: { ...info, mots } } });
    },
    membresCercle(cle, membres) {
      if (!(cle in e.cercles)) return;
      const l = membres.map((x) => x.trim()).filter((x, i, a) => x && a.indexOf(x) === i);
      if (JSON.stringify(l) === JSON.stringify(e.membres[cle] ?? [])) return;
      valider('membresCercle', { ...e, membres: { ...e.membres, [cle]: l } });
    },
    dissoudre(cle) {
      if (!(cle in e.cercles)) return null;
      const avant = e;
      const sans = <T>(o: Record<string, T>): Record<string, T> =>
        Object.fromEntries(Object.entries(o).filter(([c]) => c !== cle));
      valider('dissoudre', {
        ...e,
        paroles: e.paroles.map((q) => (q.nuee === cle ? { ...q, nuee: null } : q)),
        cercles: sans(e.cercles),
        membres: sans(e.membres),
        infosCercles: sans(e.infosCercles),
      });
      return { cle, avant };
    },
    rendreCercle(x) {
      const a = x.avant;
      const k = x.cle;
      if (k in e.cercles || !(k in a.cercles)) return;
      const ids = new Set(a.paroles.filter((q) => q.nuee === k).map((q) => q.id));
      valider('rendreCercle', {
        ...e,
        paroles: e.paroles.map((q) => (ids.has(q.id) && q.nuee == null ? { ...q, nuee: k } : q)),
        cercles: { ...e.cercles, [k]: a.cercles[k]! },
        membres: { ...e.membres, [k]: a.membres[k] ?? [] },
        infosCercles: a.infosCercles[k] ? { ...e.infosCercles, [k]: a.infosCercles[k] } : e.infosCercles,
      });
    },
    creerCercle(nom, membres, maintenant, dessin) {
      const cle = `n${String(maintenant)}`;
      const autres = { ...e.autres };
      if (dessin) autres['promi_dessins_cercle'] = JSON.stringify({ ...dessinsCercles(e.autres), [cle]: dessin });
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
