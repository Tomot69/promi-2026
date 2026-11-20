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
import type { EtatV1, Parole } from '../donnees/schema.ts';
import type { Magasin } from '../etat/magasin.ts';
import { ajusterAppareil } from '../design/appareil.ts';
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
  choisirMonde(monde: string): void;
  choisirPalette(palette: string, teinte: number): void;
  appliquerTheme(theme: 'clair' | 'sombre'): void;
  mondes(): string[];
  mondeCourant(): MondeDalle;
  /** la Toile entière, rendue à l'échelle `ech` (banc de rendu, partage) */
  rendre(cv: HTMLCanvasElement, ech: number, clair: boolean, vue?: boolean): boolean;
  lecture(): ReturnType<MoteurFonctions['Toile_lecture']>;
  redessiner(): void;
}

export function creerFacade(magasin: Magasin): Facade {
  let paroles: ParoleMoteur[] = [];
  let device: HTMLElement | null = null;

  function toile(): MoteurToile {
    if (!w.Toile) throw new Error("façade : le moteur n'est pas chargé");
    return w.Toile;
  }

  function poserGlobaux(e: Readonly<EtatV1>): void {
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

  /** le moteur a noté des places (`_placeNote` → `saveState()`) : le magasin les garde */
  function rendrePlaces(): void {
    magasin.noterPlaces(paroles.map((p) => ({ id: p.id, place: p['place'] as Parole['place'] })));
  }

  function charger(): void {
    if (w.Toile) return;
    w['saveState'] = rendrePlaces;
    w['_grainePropre'] = () => magasin.etat().utilisateur.graine ?? 0;
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
        ajusterAppareil(device);
      }
      const e = magasin.etat();
      this.appliquerTheme(e.reglages.theme);
      poserGlobaux(e);
      charger();
      // le moteur se mesure sur le parent du canevas (`size()`) : il ne le fait qu'au redimensionnement de la fenêtre, ou quand on le lui demande
      w.Toile_resize?.();
    },
    planterTout() {
      const e = magasin.etat();
      poserGlobaux(e);
      const T = toile();
      if (T.getPalette() !== e.studio.palette) T.setPalette(e.studio.palette);
      if (T.getHue() !== e.studio.teinte) T.setHue(e.studio.teinte);
      if (T.getTheme() !== e.studio.monde) T.setTheme(e.studio.monde);
      T.sync(paroles.filter((p) => !p.draft).map((p) => p.id));
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
    rendre: (cv, ech, clair, vue) => toile().renderTo(cv, ech, clair, vue ? { vue: true } : undefined),
    lecture() {
      if (!w.Toile_lecture) throw new Error("façade : le moteur n'est pas chargé");
      return w.Toile_lecture();
    },
    redessiner: () => {
      toile().redraw();
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
