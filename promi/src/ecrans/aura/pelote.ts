/**
 * LA PELOTE DE L'AURA (lot 6 ; le prototype : la sphère de lot-AURA-PELOTE) — ce qui la PEINT et la fait VIVRE ; le moteur (le velours, ses îles,
 * son semis, son peintre) est la cinquième pièce reprise, derrière sa façade (`src/moteur/pelote.ts`) ; ses couleurs se DÉCIDENT dans
 * `src/metier/pelote-couleurs.ts`, sa rotation dans `src/metier/derive.ts`. Ce module tient :
 *  · les préparations (l'atlas des poils, le semis du palier, les îles — une par parole tenue, dans l'ordre où elles sont apparues — et la cession
 *    de teinte du chantier 59 en sombre, le recalage de clarté d'Ingénu), gardées tant que rien ne change ;
 *  · la boucle (l'horloge unique) : la dérive de l'axe (C-302), l'élan qui s'ajoute à la rotation lente, la respiration (Q364 → A : la lumière du
 *    velours, 10 s, 0,6 s après l'affichage, au temps réel ; immobile au milieu du cycle sous « Réduire les animations »), le roulis du calque ;
 *  · le régulateur de densité (110 000 → 90 000 → 75 000 poils : il VISE pendant qu'on regarde, et n'applique qu'en quittant l'écran — Q186, Q237).
 * Les gestes (prise, élan, creux, traces) vivent dans `gestes.ts` et écrivent dans l'état publié ici (`etat`).
 */
import type { Facade } from '../../moteur/facade.ts';
import type { MondeDalle, Parole } from '../../donnees/schema.ts';
import { chargerPelote, type MoteurPelote, type OptionsPelote, type SemisPelote } from '../../moteur/pelote.ts';
import { horloge } from '../../animation/horloge.ts';
import { AUTO, borne, creerDerive, type Derive, type PasDerive } from '../../metier/derive.ts';
import type { AccesPelote, Empreinte, Trace } from './gestes.ts';
// Ingénu : la rampe de chaque nature (Q297, v18–v19 : `RAMPE` de lot-V18), tirée des jetons — la même que les cartes de l'Index
import { RAMPE_INGENU as RAMPE } from '../index/carte.ts';
import {
  CREME,
  cederIles,
  cessionIle,
  corps,
  etatCouleursInitial,
  fondIleIngenu,
  fondSphere,
  hauteurIngenu,
  lisibiliteIle,
  nouvelleOuverture,
  solEffectif,
  texteBouton,
  type ContexteCouleurs,
  type EtatCouleurs,
  type Lab,
  type RGB,
  type StockageCouleurs,
} from '../../metier/pelote-couleurs.ts';

/** la boule : sa boîte (296 × 296), la part du rayon (116 pt) */
export const BO = { x: 47, y: 105.532, d: 296 } as const;
export const R_BOULE = 0.392;
/** les réglages du peintre, repris de la planche (`page`, `ecranAura`) */
const FROISSE = (() => {
  const D = [
    [0.62, 0.31, 0.72],
    [-0.47, 0.83, -0.3],
    [0.18, -0.55, 0.81],
    [-0.79, -0.37, 0.49],
    [0.34, 0.88, 0.33],
    [0.71, -0.62, -0.33],
  ];
  const Kk = [9.7, 13.1, 17.9, 23.3, 29.1, 37.7];
  const A = [0.0059, 0.0041, 0.0029, 0.0019, 0.0012, 0.0007];
  const PH = [0.4, 1.9, 2.7, 0.9, 1.4, 2.2];
  return D.map((d, i) => [A[i]!, d[0]! * Kk[i]!, d[1]! * Kk[i]!, d[2]! * Kk[i]!, PH[i]!]);
})();
const ENV = [1.0, 0.0, 1.31, 0.77, -1.05, 0.4, -0.83, 1.49, 0.61, 1.9];
const KN = 0.55;
const KDENS = [4.7, 5.3, 4.1, 0.6, 1.9, 1.1, 6.7, 5.9, 7.3, 2.4, 0.7, 1.5];
/** les paliers du régulateur (densité ×1 : v123 et v124 — la densité 3 n'est pas portée, Q378) */
export const PALIERS = [110000, 90000, 75000] as const;
/** l'échelle des îles, celle de la planche */
const PXR = 620 * 0.438;
const MAG = 2.2;
/** la peau, en clair : la crème du corps, à 0,78 (Q210, 23 sept.) */
const PEAU_T = 0.78;
/** l'élan s'éteint en τ ; le budget d'une image (le régulateur) ; le creux du doigt (v139) : il revient en τ 0,60, ce qui file par-dessus le comble
 *  (amorti, jamais retranché), il se retire quand il est invisible ; 160 traces au plus */
const G = {
  TANG: 0.32,
  TAU: 0.55,
  BUDGET: 16.7,
  ENF_TAU: 0.6,
  RETOUR_TAU: 0.6,
  COMBLE: 0.42,
  COMBLE_K: 0.08,
  EMP_FIN: 0.0004,
  TRACES: 160,
} as const;
/** la respiration (v117, Q364 → A) : 0 → 0,55, 4 s qui monte, 6 s qui redescend, 0,6 s après l'affichage */
export const SOUFFLE = { MAX: 0.55, MONTE: 4, DESCEND: 6, DEPART: 0.6 } as const;

export interface HotePelote {
  facade: Facade;
  cv: HTMLCanvasElement;
  rot: HTMLElement;
  /** l'écran (sa couleur de fond se lit sur lui) */
  ecran: HTMLElement;
  clair(): boolean;
  /** l'Aura est à l'écran (ouverte, rien par-dessus la Pelote) */
  visible(): boolean;
  /** le stockage de l'appareil (les clés de la Pelote : `promi_pelote_*`) */
  stockage: StockageCouleurs;
  /** le hasard (Math.random : le prototype tire au hasard à chaque ouverture) */
  hasard: () => number;
  /** après une image peinte, toutes les trente : l'écran repose sa colonne */
  apresImage?: () => void;
  /** un autre écran PAR-DESSUS la Pelote (une fiche, une personne) : on ne peint pas dessous */
  couvert?: () => boolean;
  /** les tenues dans l'ordre des îles, lues dans l'état (la préparation au repos les lit avant l'ouverture) */
  tenues(): Parole[];
}

/** l'état vivant de la vue, que les gestes lisent et écrivent */
export interface VuePelote {
  lac: number;
  tan: number;
  vlac: number;
  vtan: number;
  om: number;
  lacAv: number;
  tau: number;
  rampe: { vl: number; vt: number; t: number; d: number } | null;
}

export interface Pelote {
  /** les tenues dans l'ordre des îles, et leur nombre */
  donner(T: readonly Parole[]): void;
  /** un ton neuf (sauf s'il a été tiré au repos), les préparations, la première image peinte dans le geste, la boucle */
  ouvrir(): void;
  /** la boucle s'arrête ; la vise du régulateur s'applique (jamais sous les yeux) ; la prochaine ouverture se prépare au repos (un ton neuf) */
  fermer(): void;
  /** quelque chose a changé hors de l'écran (une parole, la palette, le thème) : la préparation au repos se refait ; `ton` : un ton neuf */
  invalider(ton: boolean): void;
  /** les couleurs décidées pour cette ouverture */
  couleurs(): { sol: RGB; corps: RGB | null; bouton: { rgb: RGB; idx: number } };
  vue: VuePelote;
  /** l'état vivant que les gestes lisent et écrivent (gestes.ts) */
  acces: AccesPelote;
  /** le juge : figer la rotation, poser une vue, forcer le souffle, poser les tirages de couleur du prototype, peindre maintenant */
  fige(b: boolean): void;
  poserTirages(e: Partial<EtatCouleurs>): void;
  /** le juge : la Pelote sans ses îles (une trame vide — leur matière respire, M1), et les îles bâties (leur nombre, la dernière) */
  sansIles(b: boolean): void;
  iles(): { n: number; peintes: number; derniere: number[] | null };
  /** le juge : les traces (posées et en attente), chacune avec sa largeur, son intensité et ses deux bouts dans l'objet */
  traces(): Array<{ a: number[]; b: number[]; L: number; w: number; f: number }>;
  poserVue(lac: number, tan: number): void;
  souffleU(u: number | null): void;
  peindre(): boolean;
  etat(): {
    pret: boolean;
    peints: number;
    palier: number;
    vise: number;
    gl: boolean;
    roll: number;
    erreur: string | null;
    souffle: number;
    ouverture: unknown;
  };
}

type Ile = { m?: ArrayLike<number> };
type Iles = { iles: Ile[]; col?: (number[] | null)[]; derniere?: number[]; cle?: string };

export function monterPelote(h: HotePelote): Pelote {
  const M: MoteurPelote = chargerPelote();
  const { facade, cv, rot } = h;
  let T: Parole[] = [];
  const etatC: EtatCouleurs = etatCouleursInitial();
  let ouverture: unknown = null;
  let solTireAvance = false;
  const PEL = {
    palier: lireEntier('promi_pelote_palier', 0, 0, PALIERS.length - 1),
    vise: 0,
    ms: [] as number[],
    skip: 0,
    pret: false,
    peints: 0,
    fige: false,
    souffleT: null as number | null,
    souffleForce: null as number | null,
    gl: false,
    erreur: null as string | null,
    cede: 0,
  };
  PEL.vise = PEL.palier;
  const vue: VuePelote = { lac: 2.9, tan: G.TANG, vlac: 0, vtan: 0, om: AUTO, lacAv: 2.9, tau: G.TAU, rampe: null };
  const DRV: Derive = creerDerive(h.hasard);
  let DRW: PasDerive | { tan: number; lac: number; roll: number } = { tan: 0, lac: AUTO, roll: 0 };
  let roll = 0;
  // ── LES GESTES : l'empreinte, les traces (v21 : la Pelote redevient lisse à chaque ouverture) ──
  let TRACES: Trace[] = [];
  let TVER = 0;
  const AC: AccesPelote = {
    vue,
    emp: null,
    prise: false,
    file: [],
    poser(t) {
      const av = TRACES;
      TRACES = TRACES.concat([t]).slice(-G.TRACES);
      TVER++;
      retouche(av, TRACES);
    },
    relisser() {
      const av = TRACES;
      TRACES = [];
      AC.file = [];
      TVER++;
      retouche(av, TRACES);
    },
    roulis: () => roll,
    arreterRoulis: () => {
      /* le calque ne tourne plus seul depuis v210 (C-302) : la boucle le pose à chaque image */
    },
  };
  let raf: number | null = null;
  let tp = 0;

  function lireEntier(cle: string, d: number, min: number, max: number): number {
    try {
      const v = JSON.parse(h.stockage.lire(cle) ?? 'null') as unknown;
      return typeof v === 'number' ? Math.max(min, Math.min(max, v | 0)) : d;
    } catch {
      return d;
    }
  }
  const reduit = (): boolean => {
    try {
      return matchMedia('(prefers-reduced-motion: reduce)').matches;
    } catch {
      return false;
    }
  };

  // ── LES COULEURS : ce que l'écran sait au moment de décider ──
  const rgbDe = (s: string): RGB | null => {
    const m = /(\d+)[, ]+(\d+)[, ]+(\d+)/.exec(s);
    return m ? [+m[1]!, +m[2]!, +m[3]!] : null;
  };
  const cleMonde = (p: Parole): string => {
    const m = (p.monde ?? {}) as Partial<MondeDalle>;
    return `${String(p.id)}|${String(m.m)}/${String(m.p)}/${String(m.h)}`;
  };
  /** une dalle par Promi et par monde, rendue une fois (§4) */
  const DALLES = new Map<string, HTMLCanvasElement & { __dalleInfo?: { lab?: number[]; plein?: number } }>();
  const dalleDe = (p: Parole): (HTMLCanvasElement & { __dalleInfo?: { lab?: number[]; plein?: number } }) | null => {
    const k = cleMonde(p);
    const c = DALLES.get(k);
    if (c) return c;
    const d = facade.dalleIle(p.id, p.monde);
    if (d) DALLES.set(k, d);
    return d;
  };
  function ctx(): ContexteCouleurs {
    const iles: (Lab | null)[] = [];
    for (const p of T.slice(0, 40)) {
      const L = dalleDe(p)?.__dalleInfo?.lab;
      iles.push(L && L.length >= 3 ? [L[0]!, L[1]!, L[2]!] : null);
    }
    return {
      palette: facade.tonsPelote().map((c) => [c[0]!, c[1]!, c[2]!] as RGB),
      ingenu: facade.mondeCourant().p === 'signal',
      clair: h.clair(),
      page: rgbDe(getComputedStyle(h.ecran).backgroundColor),
      iles,
      rampe: (b) => M.rampeVelours([b[0], b[1], b[2]]),
    };
  }

  // ── LES PRÉPARATIONS ──
  let ATL: { a: unknown; t: number[] } | null = null;
  const atlas = (): { a: unknown; t: number[] } => {
    if (ATL) return ATL;
    const k = (BO.d / 620) * 1.6;
    const t = [2.5 * k, 4.4 * k, 5.7 * k, 7.3 * k];
    return (ATL = { a: M.atlasAlpha(M.GRAIN_POIL, t, M.ORI, M.NIVA, 0.15, 0.78, true, M.NVAR), t });
  };
  const SEMC = new Map<number, SemisPelote>();
  const semis = (): SemisPelote => {
    const N = PALIERS[PEL.palier]!;
    let s = SEMC.get(N);
    if (!s) {
      s = M.semisPavage(N, 77, 0.0, KDENS, 4, false, 0);
      SEMC.set(N, s);
    }
    return s;
  };
  const invalideSemis = (): void => {
    for (const s of SEMC.values()) s['__stCle'] = null;
  };
  /** une caresse se RETOUCHE, elle ne refait pas tout le cache (les points proches des arcs qui entrent ou sortent) ; les semis des autres
   *  paliers sont invalidés : ils se referont entiers s'ils resservent, jamais avec des caresses périmées */
  function retouche(av: Trace[], nv: Trace[]): void {
    const S = semis();
    for (const s of SEMC.values()) if (s !== S) s['__stCle'] = null;
    if (!S['__st']) return;
    M.retoucheTraces(S['__st'], av, nv);
  }
  /** les segments en attente, inscrits EN UNE FOIS juste après une image (v144, C-113), au plus toutes les 66 ms ; si l'image qui suit dépasse
   *  20 ms, la cadence s'espace (jusqu'à 300 ms) */
  let fileT = 0;
  let fileCad = 66;
  let fileVu = false;
  let fileP = false;
  function videFile(ts: number, force: boolean, dtReel: number): void {
    if (fileVu) {
      fileCad = dtReel * 1000 > 20 ? Math.min(300, fileCad * 1.6) : Math.max(66, fileCad * 0.92);
      fileVu = false;
    }
    if (!AC.file.length) return;
    if (!force && ts - fileT < fileCad) return;
    const av = TRACES;
    TRACES = TRACES.concat(AC.file).slice(-G.TRACES);
    AC.file = [];
    TVER++;
    fileT = ts;
    fileVu = true;
    retouche(av, TRACES);
  }
  /** l'empreinte : posée, elle s'enfonce (q(t) = 1 − 1/(1 + t/0,60)², p = q^1,5) ; lâchée, elle revient, comblée par ce qui file par-dessus */
  function majEmp(dt: number): void {
    const E: Empreinte | null = AC.emp;
    if (!E) return;
    const now = horloge().maintenant();
    if (E.tr === 0) {
      const u = 1 + Math.max(0, (now - E.t0) / 1000) / G.ENF_TAU;
      E.q = 1 - 1 / (u * u);
      E.p = Math.pow(E.q, 1.5);
      return;
    }
    const q = E.qRel * Math.exp(-Math.max(0, now - E.tr) / 1000 / G.RETOUR_TAU);
    E.q = q;
    E.comble += G.COMBLE * vue.om * dt;
    E.p = Math.pow(q, 1.5) * Math.exp(-E.comble / G.COMBLE_K);
    if (E.p < G.EMP_FIN) AC.emp = null;
  }
  const empPour = (E: Empreinte): Record<string, unknown> => ({
    c: E.c,
    ax: E.ax,
    a: E.a,
    el: E.el,
    dmax: E.dmax,
    p: E.p,
    biais: 0.14,
    rho: 0.085,
    ub: 0.35,
    B: 0.32,
    U: 0.5,
  });
  /** les îles qui cèdent leur teinte (chantier 59), par clé de dalle, et leur rang */
  const CEDE: Record<string, number> = {};
  const LISIBLES = new Map<string, HTMLCanvasElement>();
  function dalleLisible(p: Parole): HTMLCanvasElement | null {
    const src = dalleDe(p);
    if (!src) return null;
    const C = ctx();
    // v18 · Q297 : sous Ingénu (la palette de SA plantation), la clarté recalée sur la rampe de sa nature — jamais une autre couleur
    if ((((p.monde ?? {}) as Partial<MondeDalle>).p ?? 'signal') === 'signal') {
      const F = fondIleIngenu(C, etatC, h.hasard);
      const ki = `${cleMonde(p)}|ingenu|${[F[0] | 0, F[1] | 0, F[2] | 0].join(',')}`;
      const deja = LISIBLES.get(ki);
      if (deja) return deja;
      const nat = p.chiche
        ? 'chiche'
        : p.nuee && (p as unknown as { kind?: string }).kind === 'nuee'
          ? 'nuee'
          : 'promi';
      const rendus = new Map<number, HTMLCanvasElement>();
      const best = hauteurIngenu(C.clair, F, (haut) => {
        const c = facade.dalleIle(p.id, p.monde, { rampe: { cols: RAMPE[nat], haut } });
        const L = c?.__dalleInfo?.lab;
        if (!c || !L) return null;
        rendus.set(haut, c);
        return [L[0]!, L[1]!, L[2]!];
      });
      const c = best ? rendus.get(best.h) : null;
      if (!c) return src;
      LISIBLES.set(ki, c);
      return c;
    }
    const F = fondSphere(C, etatC);
    const rang = CEDE[cleMonde(p)] ?? 0;
    const cle = `${cleMonde(p)}|${[F[0] | 0, F[1] | 0, F[2] | 0].join(',')}|${String(rang)}`;
    const deja = LISIBLES.get(cle);
    if (deja) return deja;
    const info = src.__dalleInfo;
    if (!rang || !info?.lab || !((info.plein ?? 0) > 0)) {
      LISIBLES.set(cle, src);
      return src;
    }
    const ch = cessionIle(C.palette, F, rang);
    if (!ch || 'sansPalette' in ch) {
      LISIBLES.set(cle, src);
      return src;
    }
    const out = facade.dalleIle(p.id, p.monde, { decale: { a: ch.a, b: ch.b } }) ?? src;
    LISIBLES.set(cle, out);
    return out;
  }
  let ILES: Iles | null = null;
  let cleI = '';
  const poseIles = (): Iles =>
    M.batIles(T.length, facade.tonsPelote(), {
      pxr: PXR,
      mag: MAG,
      palette: facade.paletteCourante(),
      // la vraie dalle du Promi, calée sur l'emprise que la planche taillait à son île (sa forme vient du moteur, sa taille de l'île)
      dalle: (k: number, _I: unknown, g: number) => {
        const p = T[k];
        const s = p ? dalleLisible(p) : null;
        if (!s || !p) return null;
        const cote = Math.max(s.width, s.height);
        return { cv: s, sx: s.width / 2, sy: s.height / 2, kk: cote / (g / (PXR / MAG)), monde: p.monde };
      },
    }) as unknown as Iles;
  function iles(): Iles {
    const C = ctx();
    const F = fondSphere(C, etatC);
    const cle = `${T.map(cleMonde).join(',')}|${[F[0] | 0, F[1] | 0, F[2] | 0].join(',')}`;
    if (ILES && cleI === cle) return ILES;
    let r = poseIles();
    cederIles(
      T.map(cleMonde),
      C.clair,
      CEDE,
      () => r.iles.slice(0, T.length).map((I) => (I.m ? (lisibiliteIle(I.m, r.col ?? [], F)?.dE ?? null) : null)),
      () => {
        r = poseIles();
      },
    );
    r.cle = `aura|${cle}`;
    ILES = r;
    cleI = cle;
    return r;
  }

  let sansIles = false;
  let VIDES: Iles | null = null;
  const ilesVides = (): Iles => {
    if (!VIDES) {
      VIDES = M.batIles(0, facade.tonsPelote(), {
        pxr: PXR,
        mag: MAG,
        palette: facade.paletteCourante(),
        dalle: () => null,
      }) as unknown as Iles;
      VIDES.cle = 'aura|vide';
    }
    return VIDES;
  };

  // ── LA RESPIRATION ──
  function souffle(): number {
    if (PEL.souffleForce != null) return SOUFFLE.MAX * PEL.souffleForce;
    if (reduit()) return SOUFFLE.MAX * 0.5;
    const t = PEL.souffleT;
    if (t == null || t <= 0) return 0;
    const c = SOUFFLE.MONTE + SOUFFLE.DESCEND;
    const u = t % c;
    const s =
      u < SOUFFLE.MONTE
        ? (1 - Math.cos((Math.PI * u) / SOUFFLE.MONTE)) / 2
        : (1 + Math.cos((Math.PI * (u - SOUFFLE.MONTE)) / SOUFFLE.DESCEND)) / 2;
    return SOUFFLE.MAX * s;
  }
  /** le sens où la Pelote tourne : il couche les poils du bord (v141) */
  function tour(): number[] | null {
    if (PEL.fige) return null;
    const wl = (AC.prise ? 0 : DRW.lac) + vue.vlac;
    const wt = (AC.prise ? 0 : DRW.tan) + vue.vtan;
    const w = Math.sqrt(wl * wl + wt * wt);
    if (w < 1e-4) return null;
    const s = Math.min(1, w / 1.2);
    const A = 0.18 + 0.72 * s;
    return [(A * wl) / w, (-A * wt) / w];
  }
  function opts(): OptionsPelote {
    const A = atlas();
    const C = ctx();
    return {
      css: BO.d,
      R: R_BOULE,
      sol: solEffectif(C, etatC),
      tailles: A.t,
      atlas: A.a,
      semis: semis(),
      relief: FROISSE,
      env: ENV,
      kn: KN,
      lac: vue.lac,
      tan: vue.tan,
      pal: facade.tonsPelote(),
      trame: sansIles ? ilesVides() : ILES,
      libre: false,
      fond: 'transparent',
      velours: souffle(),
      doux: false,
      contre: 0,
      duvet: 0,
      grade: 0,
      velours2: 1,
      dresse: 0,
      pousse: Math.min(1, T.length / 34),
      traces: TRACES,
      peigneAxial: 1,
      tracesIncr: 1,
      emp: AC.emp && AC.emp.p >= G.EMP_FIN ? empPour(AC.emp) : null,
      peauVers: C.clair ? [CREME[0], CREME[1], CREME[2], PEAU_T] : null,
      corps: corps(C, etatC, h.hasard),
      tour: tour(),
    };
  }
  function peintUne(): boolean {
    try {
      const o = opts();
      PEL.gl = !!M.peintGL(cv, o);
      if (!PEL.gl) M.peint(cv, o);
      PEL.peints++;
      return true;
    } catch (e) {
      PEL.erreur = String((e as Error)?.stack ?? e);
      PEL.pret = false;
      return false;
    }
  }

  // ── LE RÉGULATEUR DE DENSITÉ : il vise pendant qu'on regarde, il applique en quittant (jamais sous les yeux) ──
  const mediane = (L: number[]): number => {
    const s = L.slice().sort((a, b) => a - b);
    return s[s.length >> 1] ?? 0;
  };
  function densite(ms: number, statique: boolean): void {
    if (statique) {
      PEL.skip = 4;
      return;
    }
    if (PEL.skip > 0) {
      PEL.skip--;
      return;
    }
    // le contact a son coût : on ne décide que sur des images ordinaires
    if (AC.emp) return;
    PEL.ms.push(ms);
    if (PEL.ms.length > 90) PEL.ms.shift();
    if (PEL.ms.length < 45) return;
    const med = mediane(PEL.ms.slice(-45));
    const N = PALIERS[PEL.palier]!;
    let v: number;
    if (med > G.BUDGET) {
      for (v = PEL.palier; v < PALIERS.length - 1 && (med * PALIERS[v]!) / N > G.BUDGET; v++);
    } else if (PEL.ms.length >= 90 && PEL.palier > 0) {
      v = (mediane(PEL.ms.slice(-90)) * PALIERS[PEL.palier - 1]!) / N < 15 ? PEL.palier - 1 : PEL.palier;
    } else if (PEL.ms.length >= 90) v = PEL.palier;
    else return;
    if (v === PEL.vise) return;
    if (v > PEL.palier) PEL.cede++;
    PEL.vise = v;
  }
  function applique(): boolean {
    if (PEL.vise === PEL.palier) return false;
    PEL.palier = PEL.vise;
    PEL.ms = [];
    PEL.skip = 4;
    h.stockage.ecrire('promi_pelote_palier', JSON.stringify(PEL.palier));
    return true;
  }

  // ── LA BOUCLE ──
  let rCle = '';
  function boucle(ts: number): void {
    if (!h.visible()) {
      raf = null;
      tp = 0;
      return;
    }
    raf = horloge().image(boucle);
    const dtR = tp ? (ts - tp) / 1000 : 1 / 60;
    const dt = Math.min(0.1, dtR);
    tp = ts;
    if (AC.prise) {
      vue.om = Math.abs(vue.lac - vue.lacAv) / Math.max(dt, 0.001);
      vue.vlac = 0;
      vue.vtan = 0;
      DRW = { tan: 0, lac: 0, roll: 0 };
    } else avancer(dt);
    vue.lacAv = vue.lac;
    majEmp(dt);
    // les segments en attente : inscrits APRÈS l'image, dans leur propre tâche (le calcul tient entre deux images)
    if (AC.file.length && !fileP) {
      fileP = true;
      const force = !AC.prise;
      horloge().minuteur(() => {
        fileP = false;
        videFile(ts, force, dtR);
      }, 0);
    } else if (!AC.file.length) videFile(ts, false, dtR);
    if (!PEL.pret || h.couvert?.()) return;
    const calme =
      !AC.prise &&
      !AC.emp &&
      !AC.file.length &&
      !vue.vlac &&
      !vue.vtan &&
      (PEL.fige || (!DRW.lac && !DRW.tan && !DRW.roll));
    const S = semis();
    const cle = [
      S['__stCle'],
      TVER,
      PEL.palier,
      h.clair() ? 1 : 0,
      cv.width,
      vue.lac.toFixed(4),
      vue.tan.toFixed(4),
    ].join('|');
    if (calme && rCle === cle && PEL.peints > 0) return;
    // le souffle n'avance que quand on la voit — au temps réel ; la borne de 0,5 s ne sert qu'après une pause
    PEL.souffleT = (PEL.souffleT == null ? -SOUFFLE.DEPART : PEL.souffleT) + Math.min(0.5, dtR);
    const av = S['__stCle'];
    const t0 = horloge().maintenant();
    if (!peintUne()) return;
    let ms = horloge().maintenant() - t0;
    // sous la carte graphique, le temps passé en JavaScript ne dit rien : le régulateur juge l'IMAGE
    if (PEL.gl) ms = Math.max(ms, dtR * 1000 - 8);
    if (PEL.peints % 30 === 0) h.apresImage?.();
    densite(ms, S['__stCle'] !== av);
    rCle = [S['__stCle'], TVER, PEL.palier, h.clair() ? 1 : 0, cv.width, vue.lac.toFixed(4), vue.tan.toFixed(4)].join(
      '|',
    );
  }

  /** la rotation lente et l'élan, hors du doigt : ils S'ADDITIONNENT (pas d'instant de reprise, donc pas de saccade) */
  function avancer(dt: number): void {
    const k = Math.exp(-dt / vue.tau);
    vue.vlac *= k;
    vue.vtan *= k;
    if (Math.abs(vue.vlac) < 0.0008) vue.vlac = 0;
    if (Math.abs(vue.vtan) < 0.0008) vue.vtan = 0;
    if (!vue.vlac && !vue.vtan) vue.tau = G.TAU;
    if (vue.rampe) {
      vue.rampe.t += dt;
      const u = Math.min(1, vue.rampe.t / vue.rampe.d);
      const e = u * u * (3 - 2 * u);
      vue.vlac = vue.rampe.vl * e;
      vue.vtan = vue.rampe.vt * e;
      if (u >= 1) vue.rampe = null;
    }
    DRW = PEL.fige || reduit() ? { tan: 0, lac: 0, roll: 0 } : DRV.pas(dt, vue.tan);
    if (!PEL.fige) {
      vue.lac += (DRW.lac + vue.vlac) * dt;
      vue.tan = borne(vue.tan + (DRW.tan + vue.vtan) * dt);
      roll += ((DRW.roll * 180) / Math.PI) * dt;
      rot.style.transform = `rotate(${String(roll % 360)}deg)`;
    }
    vue.om = Math.sqrt(
      (DRW.lac + vue.vlac) * (DRW.lac + vue.vlac) + (DRW.tan + vue.vtan) * (DRW.tan + vue.vtan) + DRW.roll * DRW.roll,
    );
  }

  /* ── LA PRÉPARATION AU REPOS (v146, C-135 : « la Pelote paraît dès l'ouverture ») — au repos (aucun toucher depuis 0,9 s, l'Aura fermée, la
     page visible), le ton de la PROCHAINE ouverture est tiré et tout est préparé, une étape par tâche (une image passe entre deux) : l'atlas, le
     semis, le ton, les dalles des îles (une par tâche), les îles, puis une image peinte dans le canevas fermé ; à l'ouverture, plus rien n'est tiré
     ni calculé, la première image est peinte dans le geste. Le doigt interrompt : la suite reprend au repos suivant. ── */
  const PRE = { pret: false, enCours: false, tTouche: -1e9 };
  for (const t of ['touchstart', 'pointerdown', 'keydown', 'wheel'])
    document.addEventListener(
      t,
      () => {
        PRE.tTouche = horloge().maintenant();
      },
      { capture: true, passive: true },
    );
  const calmeRepos = (): boolean => !document.hidden && !h.visible() && horloge().maintenant() - PRE.tTouche >= 900;
  let preT: number | null = null;
  function planifier(ms: number): void {
    if (preT != null) horloge().annuleMinuteur(preT);
    preT = horloge().minuteur(() => {
      preT = null;
      if (PRE.pret || PRE.enCours) return;
      if (calmeRepos()) prechauffer();
      else planifier(600);
    }, ms);
  }
  function prechauffer(): void {
    if (PRE.enCours || PRE.pret) return;
    PRE.enCours = true;
    let dal: Parole[] | null = null;
    let k = 0;
    const E: Array<() => unknown> = [
      () => {
        applique();
        atlas();
      },
      () => {
        semis();
      },
      () => {
        T = h.tenues();
        if (!solTireAvance) {
          ouverture = nouvelleOuverture(ctx(), etatC, h.hasard, h.stockage, Date.now());
          invalideSemis();
          ILES = null;
          solTireAvance = true;
        }
      },
      () => {
        dal ??= T.slice();
        const p = dal[k++];
        if (!p) return;
        dalleLisible(p);
        return true;
      },
      () => {
        iles();
      },
      () => {
        PEL.pret = true;
        peintUne();
        PRE.pret = true;
      },
    ];
    let i = 0;
    const suite = (): void => {
      if (PRE.pret) {
        PRE.enCours = false;
        return;
      }
      if (!calmeRepos()) {
        PRE.enCours = false;
        planifier(700);
        return;
      }
      let encore = false;
      try {
        encore = !!E[i]!();
      } catch {
        encore = false;
      }
      if (!encore) i++;
      if (i < E.length)
        horloge().image(() => {
          horloge().minuteur(suite, 0);
        });
      else PRE.enCours = false;
    };
    suite();
  }
  planifier(2200);
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) planifier(1500);
  });

  function preparer(): void {
    PEL.pret = false;
    applique();
    atlas();
    semis();
    iles();
    PEL.pret = true;
  }

  return {
    vue,
    acces: AC,
    donner(L) {
      T = L.slice();
    },
    ouvrir() {
      // un ton neuf à chaque ouverture (Tom) — sauf s'il a été tiré d'avance
      if (!solTireAvance) {
        ouverture = nouvelleOuverture(ctx(), etatC, h.hasard, h.stockage, Date.now());
        // le poil a changé : le semis (sa clé de cache) et les îles (leur sol) se refont — la fin de `nouveauSol`
        invalideSemis();
        ILES = null;
      }
      solTireAvance = false;
      PEL.souffleT = -SOUFFLE.DEPART;
      // v21 : à chaque ouverture, la Pelote redevient lisse
      AC.relisser();
      AC.emp = null;
      T = h.tenues();
      preparer();
      if (PEL.pret) peintUne();
      if (raf == null) {
        tp = 0;
        raf = horloge().image(boucle);
      }
    },
    fermer() {
      if (raf != null) horloge().annuleImage(raf);
      raf = null;
      tp = 0;
      if (applique()) invalideSemis();
      PRE.pret = false;
      planifier(500);
    },
    invalider(ton) {
      PRE.pret = false;
      if (ton) {
        solTireAvance = false;
        invalideSemis();
        ILES = null;
        DALLES.clear();
        LISIBLES.clear();
        VIDES = null;
      }
      planifier(500);
    },
    couleurs() {
      const C = ctx();
      return { sol: solEffectif(C, etatC), corps: corps(C, etatC, h.hasard), bouton: texteBouton(C, etatC, h.hasard) };
    },
    fige(b) {
      PEL.fige = b;
    },
    poserTirages(x) {
      Object.assign(etatC, x);
      invalideSemis();
      ILES = null;
      PEL.pret = false;
      atlas();
      semis();
      iles();
      PEL.pret = true;
      h.apresImage?.();
    },
    sansIles(b) {
      sansIles = b;
      invalideSemis();
    },
    traces: () =>
      TRACES.concat(AC.file).map((t) => {
        const c = Math.cos(t.L);
        const s = Math.sin(t.L);
        return { a: t.a, b: [0, 1, 2].map((i) => t.a[i]! * c + t.d[i]! * s), L: t.L, w: t.w, f: t.f };
      }),
    iles: () => ({
      n: T.length,
      peintes: ILES ? ILES.iles.filter((I) => !!I.m).length : 0,
      derniere: ILES?.derniere ? ILES.derniere.slice() : null,
    }),
    poserVue(l, t) {
      vue.lac = +l;
      vue.tan = borne(+t);
      vue.lacAv = vue.lac;
      vue.vlac = 0;
      vue.vtan = 0;
    },
    souffleU(u) {
      PEL.souffleForce = u;
    },
    peindre: () => peintUne(),
    etat: () => ({
      pret: PEL.pret,
      peints: PEL.peints,
      palier: PALIERS[PEL.palier]!,
      vise: PALIERS[PEL.vise]!,
      gl: PEL.gl,
      roll,
      erreur: PEL.erreur,
      souffle: souffle(),
      ouverture,
    }),
  };
}
