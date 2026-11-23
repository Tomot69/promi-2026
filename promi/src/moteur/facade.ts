/**
 * LA FAÇADE DU MOTEUR — le SEUL endroit de l'app qui parle au moteur repris (src/moteur/repris/promi-moteur.js, copie octet pour octet
 * du prototype). Un écran ne touche jamais `window.Toile` : il appelle la façade. (Règle de la vraie app ; lint et dependency-cruiser.)
 *
 * Le contrat du moteur, relevé sur le prototype (eslint no-undef sur le moteur, 20 nov. 2026) — ce qu'il lit de la page :
 *  · un canevas `#toileCv` dans `#stage`, dans `#device` (sa taille est celle de son parent ; `#device.light` = le thème clair) ;
 *  · `promises` (les paroles, au format du prototype), `NUE` (les Cercles), `NUEDALLE`, `USER.seed` (la graine, `promi_graine`),
 *    `saveState()` (il l'appelle quand il a noté la place d'une dalle), et la clé `promi_nueplace` du stockage ;
 *  · deux questions à l'app : `Toile.labelsOn()` (le texte sur les dalles ?) et `Toile.labelOf(graine)` (quel texte ?).
 * La façade pose tout cela depuis le magasin, charge le moteur, et rend les places qu'il a notées au magasin (`noterPlaces`).
 */
import moteurSource from './repris/promi-moteur.js?raw';
import type { Etat, Parole } from '../donnees/schema.ts';
import type { Magasin } from '../etat/magasin.ts';
import type { EtiquetteDalle, GraineMoteur, MondeDalle, MoteurFonctions, MoteurToile } from './types.ts';

type Fenetre = Window & Record<string, unknown> & Partial<MoteurFonctions> & { Toile?: MoteurToile };

const w = window as unknown as Fenetre;

/** Une parole telle que le moteur la lit : les champs du prototype, à plat. Objet vivant : le moteur y note `place`. */
type ParoleMoteur = Record<string, unknown> & { id: number; draft?: boolean };

function versMoteur(p: Parole): ParoleMoteur {
  const { suite, ...connus } = p;
  return { ...connus, ...(suite ?? {}) };
}

export interface Facade {
  /** pose l'hôte du moteur dans `conteneur`, puis charge le moteur (une seule fois) */
  monter(conteneur: HTMLElement): void;
  /** donne au moteur les paroles du magasin et les plante (`Toile.sync`) */
  planterTout(): void;
  /**
   * redonne au moteur l'état du magasin (ses globales : `promises`, `NUE`…) sans rien planter : le moteur lit les paroles à chaque image (le titre
   * écrit sur une dalle, sa clé de plantation, son état) — après chaque écriture, il lit celles du magasin
   */
  rafraichir(): void;
  choisirMonde(monde: string): void;
  choisirPalette(palette: string, teinte: number): void;
  appliquerTheme(theme: 'clair' | 'sombre'): void;
  mondes(): string[];
  mondeCourant(): MondeDalle;
  /** les tons de la palette du Studio (le monde courant), en hexadécimal majuscule — l'outil de dessin (le prototype : `palette()` de lot-V132-DESSIN) */
  tonsStudio(): string[];
  /** la Toile entière, rendue à l'échelle `ech` (banc de rendu, partage) */
  rendre(cv: HTMLCanvasElement, ech: number, clair: boolean, vue?: boolean): boolean;
  lecture(): ReturnType<MoteurFonctions['Toile_lecture']>;
  redessiner(): void;
  /** le recadrage du moteur (le symbole « recadrer » de l'accueil, le double toucher) */
  recadrer(): void;
  /** le frémissement de toute la Toile (`liven`) : 1,5 s après le chargement et à chaque retour sur l'accueil (le prototype, app.html
   * ≈ l. 7271, 3402, 7408, 10109) — il fait aussi finir aux graines leur chemin vers leur place (le relâchement s'arrête à 0,6 pt) */
  fremir(): void;
  /** l'hôte du moteur (`#device`) : l'accueil y pose son plateau et sa barre */
  appareil(): HTMLElement;
  /** la dalle sous un point de la Toile (en pt de l'écran) : une parole, un Cercle, ou rien (`Toile.hit`, lecture seule) */
  toucher(x: number, y: number): DalleTouchee | null;
  /** la vue de la Toile (zoom, décalage) ; et si elle appartient à la main (pincée ou glissée) plutôt qu'au cadrage automatique */
  vue(): { s: number; ox: number; oy: number };
  vueALaMain(): boolean;
  /**
   * LA DALLE QUE LA PAROLE QU'ON ÉCRIT AURA (C-241, v182a : `Toile.dalleAvenir`, lecture seule) — rendue pour tenir dans `tw × th` px,
   * gardée tant que les paroles, le monde et la palette ne changent pas ; sur une Toile faite de ses paroles, le titre et la personne
   * comptent (C-062). La page + la pose en haut, 1:1 (`poserUn`). Rien, si le moteur ne peut pas la calculer.
   */
  dalleAvenir(
    id: number,
    tw: number,
    th: number,
    a: { chiche: boolean; title: string; who: string },
  ): HTMLCanvasElement | null;
  /**
   * rend la dalle de la parole `id` et la pose dans la boîte (x, y, w, h) des coordonnées courantes, 1:1, centrée (`_poseDalle` du moteur ;
   * `rampe` : la teinte de la nature, Q30, peinte par le moteur). Rend ce qui a VRAIMENT été peint.
   */
  poserDalle(
    g: CanvasRenderingContext2D,
    id: number,
    x: number,
    y: number,
    w: number,
    h: number,
    o: { rampe?: { cols: number[][]; haut: number }; courant?: number },
  ): { x: number; y: number; w: number; h: number } | null;
  /** la cellule de la dalle `id` ne touche pas le bord de la Toile (sa dalle est entière) — `Toile.dalleAbs`, `Toile.taille` */
  dalleEntiere(id: number): boolean;
  /** pose un canevas 1:1, centré sur (cx, cy) des coordonnées courantes du contexte (`_poseUn` du moteur) */
  poserUn(g: CanvasRenderingContext2D, cv: HTMLCanvasElement, cx: number, cy: number): void;
  /** C-237 : la parole plantée donnée au moteur (`Toile.addPromi`) — sa cellule grandit sous la page qui s'en va */
  planterUne(id: number): void;
  /** C-306 : le Cercle créé donné au moteur (`Toile.addNuee`, puis `sync` : le prototype, `#addNuee`) */
  planterCercle(cle: string): void;
  /**
   * OÙ LA TOILE VIVANTE POSE LA DALLE `id`, en pt de l'appareil (le prototype : `_dalleSurToile` sur un rendu frais, v183b) — la dalle rendue
   * seule par le moteur (`dalleTrame`, à l'échelle 1, sa place déclarée `__dalleInfo.org`), dans la vue du moment. Avec ce rendu (sa forme).
   */
  placeDalle(id: number): { x: number; y: number; w: number; h: number; cv: HTMLCanvasElement } | null;
  /** le canevas de la Toile vivante (le fond de la naissance la recopie à chaque image) */
  toileCanevas(): HTMLCanvasElement | null;
}

export interface DalleTouchee {
  pid: number | null;
  kind: string;
  nuee?: string;
}

export function creerFacade(magasin: Magasin): Facade {
  let paroles: ParoleMoteur[] = [];
  const avenirs = new Map<string, HTMLCanvasElement>();
  let device: HTMLElement | null = null;

  function toile(): MoteurToile {
    if (!w.Toile) throw new Error("façade : le moteur n'est pas chargé");
    return w.Toile;
  }

  function poserGlobaux(e: Readonly<Etat>): void {
    paroles = e.paroles.map(versMoteur);
    w['promises'] = paroles;
    w['NUE'] = { ...e.cercles };
    w['NUEEMEM'] = { ...e.membres };
    w['NUEDALLE'] = { ...e.dallesCercles };
    w['USER'] = { name: e.utilisateur.prenom ?? 'moi', photo: null, seed: e.utilisateur.graine ?? 0 };
    // la clé privée du moteur : il la lit et l'écrit lui-même (les places des Cercles)
    if (Object.keys(e.placesCercles).length) localStorage.setItem('promi_nueplace', JSON.stringify(e.placesCercles));
    else localStorage.removeItem('promi_nueplace');
    if (e.utilisateur.graine != null) localStorage.setItem('promi_graine', String(e.utilisateur.graine));
  }

  /** le moteur a noté des places (`_placeNote` → `saveState()`) et figé des couleurs (`_dalleFigee`, Q213 ; `NUEDALLE`) : le magasin les
   * garde — sans quoi une parole plantée changeait de couleur au rechargement */
  function rendrePlaces(): void {
    magasin.noterPlaces(
      paroles.map((p) => ({ id: p.id, place: p['place'] as Parole['place'], dalle: p['dalle'] as Parole['dalle'] })),
      { ...((w['NUEDALLE'] as Record<string, NonNullable<Parole['dalle']>> | undefined) ?? {}) },
    );
  }

  function charger(): void {
    if (w.Toile) return;
    w['saveState'] = rendrePlaces;
    w['_grainePropre'] = () => magasin.etat().utilisateur.graine ?? 0;
    // la couleur d'une parole qui n'en a pas encore : tirée de son titre et de sa personne, jamais du hasard ni de son id (Q213, la règle
    // du prototype, app.html ≈ l. 3308 : FNV-1a de « titre|personne », 4 tons) — le moteur l'appelle (`_dalleFigee`)
    w['_dalleDeCle'] = (p: { title?: string | number | null; who?: string | number | null } | null) => {
      const s = `${String(p?.title ?? '')}|${String(p?.who ?? '')}`;
      let h = 2166136261;
      for (let i = 0; i < s.length; i++) {
        h ^= s.charCodeAt(i);
        h = Math.imul(h, 16777619) >>> 0;
      }
      return { ci: h % 4, lit: 0 };
    };
    const s = document.createElement('script');
    s.text = moteurSource + '\n//# sourceURL=promi-moteur.js';
    document.head.appendChild(s);
    const T = toile();
    T.labelsOn = () => !!magasin.etat().reglages.labels;
    T.labelOf = (g: GraineMoteur): EtiquetteDalle | null => {
      if (!g) return null;
      const e = magasin.etat();
      if (g.kind === 'nuee' && g.nuee) return { who: null, title: e.cercles[g.nuee] ?? g.nuee };
      if (g.pid == null) return null;
      const p = paroles.find((x) => x.id === g.pid);
      if (!p || p.draft) return null;
      const who = typeof p['who'] === 'string' && p['who'] !== 'moi' ? p['who'] : null;
      return { who, title: typeof p['title'] === 'string' ? p['title'] : '' };
    };
  }

  return {
    monter(conteneur) {
      if (!device) {
        device = document.createElement('div');
        device.id = 'device';
        device.className = 'device';
        const stage = document.createElement('div');
        stage.id = 'stage';
        stage.className = 'stage';
        const cv = document.createElement('canvas');
        cv.id = 'toileCv';
        cv.className = 'toilecv';
        stage.appendChild(cv);
        device.appendChild(stage);
        conteneur.appendChild(device);
      }
      const e = magasin.etat();
      this.appliquerTheme(e.reglages.theme);
      poserGlobaux(e);
      charger();
      // le moteur se mesure sur le parent du canevas (`size()`) : il ne le fait qu'au redimensionnement de la fenêtre, ou quand on le lui demande
      w.Toile_resize?.();
    },
    rafraichir() {
      poserGlobaux(magasin.etat());
    },
    planterTout() {
      const e = magasin.etat();
      poserGlobaux(e);
      const T = toile();
      if (T.getPalette() !== e.studio.palette) T.setPalette(e.studio.palette);
      if (T.getHue() !== e.studio.teinte) T.setHue(e.studio.teinte);
      if (T.getTheme() !== e.studio.monde) T.setTheme(e.studio.monde);
      T.sync(paroles.filter((p) => !p.draft).map((p) => p.id));
      rendrePlaces();
    },
    choisirMonde(monde) {
      toile().setTheme(monde);
    },
    choisirPalette(palette, teinte) {
      const T = toile();
      T.setPalette(palette);
      if (teinte) T.setHue(teinte);
    },
    appliquerTheme(theme) {
      device?.classList.toggle('light', theme === 'clair');
      w.Toile?.redraw();
    },
    mondes() {
      return Object.keys(MONDES_ORDRE);
    },
    mondeCourant: () => toile().mondeCourant(),
    tonsStudio() {
      const m = toile().mondeCourant();
      return toile()
        .tonsDe(m.p, m.h)
        .map(
          (c) =>
            '#' +
            c
              .slice(0, 3)
              .map((v) =>
                Math.max(0, Math.min(255, Math.round(v)))
                  .toString(16)
                  .padStart(2, '0'),
              )
              .join('')
              .toUpperCase(),
        );
    },
    rendre: (cv, ech, clair, vue) => toile().renderTo(cv, ech, clair, vue ? { vue: true } : undefined),
    lecture() {
      if (!w.Toile_lecture) throw new Error("façade : le moteur n'est pas chargé");
      return w.Toile_lecture();
    },
    redessiner: () => {
      toile().redraw();
    },
    fremir: () => {
      w.Toile_liven?.();
    },
    recadrer: () => {
      w.Toile_recadre?.();
    },
    appareil() {
      if (!device) throw new Error("façade : l'hôte du moteur n'est pas monté");
      return device;
    },
    toucher(x, y) {
      const h = toile().hit(x, y) as { pid?: number | null; kind?: string; nuee?: string } | null;
      if (!h) return null;
      const d: DalleTouchee = { pid: h.pid ?? null, kind: h.kind ?? 'gray' };
      if (h.nuee) d.nuee = h.nuee;
      return d;
    },
    vue() {
      const v = (w.Toile_vueLue as (() => { s: number; ox: number; oy: number }) | undefined)?.();
      return v ? { s: v.s, ox: v.ox, oy: v.oy } : { s: 1, ox: 0, oy: 0 };
    },
    vueALaMain: () => !!w['_vueMain'],
    planterUne(id) {
      const e = magasin.etat();
      poserGlobaux(e);
      const T = toile() as MoteurToile & {
        addPromi(id: number): void;
        addNuee(k: string): void;
        addMember(k: string, id: number): void;
      };
      // plantée dans un Cercle : elle le rejoint (le prototype : `Toile.addNuee`, `addMember`)
      const k = e.paroles.find((p) => p.id === id)?.nuee;
      if (k) {
        T.addNuee(k);
        T.addMember(k, id);
      } else T.addPromi(id);
    },
    planterCercle(cle) {
      poserGlobaux(magasin.etat());
      const T = toile() as MoteurToile & { addNuee(k: string): void };
      T.addNuee(cle);
      T.sync(paroles.filter((p) => !p.draft).map((p) => p.id));
    },
    placeDalle(id) {
      try {
        const T = toile() as MoteurToile & { dalleTrame(cv: HTMLCanvasElement, id: number, k: number): boolean };
        const lc = document.createElement('canvas') as HTMLCanvasElement & { __dalleInfo?: { org?: number[] } };
        if (!T.dalleTrame(lc, id, 1)) return null;
        const o = lc.__dalleInfo?.org;
        if (!o || !o[2] || !device) return null;
        const D = device.getBoundingClientRect();
        const s = D.width / (device.offsetWidth || 390) || 1;
        const tcv = device.querySelector<HTMLCanvasElement>('#toileCv');
        const L = w.Toile_lecture?.();
        if (!tcv || !L) return null;
        const R = tcv.getBoundingClientRect();
        const v = L.vue;
        const sx = R.width / (L.W || tcv.clientWidth || 390);
        return {
          x: (R.left - D.left + (v.ox + v.s * o[0]!) * sx) / s,
          y: (R.top - D.top + (v.oy + v.s * o[1]!) * sx) / s,
          w: ((lc.width / o[2]) * v.s * sx) / s,
          h: ((lc.height / o[2]) * v.s * sx) / s,
          cv: lc,
        };
      } catch {
        return null;
      }
    },
    toileCanevas() {
      return device?.querySelector<HTMLCanvasElement>('#toileCv') ?? null;
    },
    dalleAvenir(id, tw, th, a) {
      const T = toile() as MoteurToile & {
        dalleAvenir(cv: HTMLCanvasElement, k: number, o: Record<string, unknown>): boolean;
      };
      try {
        const L = w.Toile_lecture?.();
        const sig = L
          ? `${String(L.graines.length)}:${L.graines.map((q) => (q.pid == null ? '' : String(q.pid))).join(';')}`
          : '';
        const neuf = !!T.semisNeuf();
        const A = { id, chiche: a.chiche, title: neuf ? a.title : '', who: neuf ? a.who || 'moi' : 'moi' };
        const cle = [
          id,
          Math.round(tw),
          Math.round(th),
          A.chiche ? 1 : 0,
          A.title,
          A.who,
          JSON.stringify(T.mondeCourant()),
          sig,
        ].join('|');
        const deja = avenirs.get(cle);
        if (deja) return deja;
        const c1 = document.createElement('canvas');
        if (!T.dalleAvenir(c1, 1, A) || !c1.width) return null;
        const k = Math.min(tw / c1.width, th / c1.height);
        const c2 = document.createElement('canvas');
        if (!T.dalleAvenir(c2, k, A) || !c2.width) return null;
        if (avenirs.size > 8) avenirs.delete(avenirs.keys().next().value!);
        avenirs.set(cle, c2);
        return c2;
      } catch {
        return null;
      }
    },
    poserDalle(g, id, x, y, l, h, o) {
      const f = w['_poseDalle'] as
        ((...a: unknown[]) => { x: number; y: number; w: number; h: number } | null) | undefined;
      const r = f ? f(g, id, x, y, l, h, o) : null;
      return r ? { x: r.x, y: r.y, w: r.w, h: r.h } : null;
    },
    dalleEntiere(id) {
      const T = toile();
      const a = T.dalleAbs(id) as { minx: number; miny: number; w: number; h: number } | null;
      const t = (T.taille as (() => { w: number; h: number }) | undefined)?.() ?? { w: 1e9, h: 1e9 };
      return !!a && a.minx > 1 && a.miny > 1 && a.minx + a.w < t.w - 1 && a.miny + a.h < t.h - 1;
    },
    poserUn(g, cv, cx, cy) {
      (w['_poseUn'] as (g: CanvasRenderingContext2D, cv: HTMLCanvasElement, x: number, y: number) => void)(
        g,
        cv,
        cx,
        cy,
      );
    },
  };
}

/**
 * L'ordre des vingt mondes au Studio (le `order` du prototype) et ceux de Ma Parole ! (`_mondesCercle`), relevés le 20 nov. 2026.
 * vrai = un monde de Ma Parole ! (payant). Le Studio (lot 7) les lira d'ici ; leurs prix : src/metier/achats.ts.
 */
export const MONDES_ORDRE: Readonly<Record<string, boolean>> = {
  encre: false,
  touffe: false,
  brouillamini: false,
  halin: false,
  esquille: false,
  mosaique: false,
  braille: false,
  pixel: false,
  ramage: true,
  guingois: true,
  chantourne: true,
  volubilis: true,
  madrure: true,
  chamade: true,
  ritournelle: true,
  bobinette: true,
  mascaret: true,
  terrazzo: true,
  gravure: true,
  sillons: true,
};
