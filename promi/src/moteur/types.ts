/**
 * Les types du moteur repris (src/moteur/repris/promi-moteur.js, copie octet pour octet du prototype).
 *
 * `MoteurToile` décrit la porte `window.Toile` TELLE QUE LE PROTOTYPE L'EMPLOIE : chaque membre ci-dessous est appelé par app.html
 * (relevé du 20 nov. 2026, `grep -o "Toile\.[a-zA-Z_]*" app.html`). Seule la façade (facade.ts) a le droit de les appeler : un écran
 * ne touche jamais au moteur (ARCHITECTURE.md g ; règle `no-restricted-properties` du lint et dependency-cruiser).
 *
 * Les signatures sont celles du moteur ; ce qui n'est pas encore employé par la vraie app reste typé `(...a: unknown[]) => unknown`
 * et sera précisé par le lot qui s'en sert.
 */

export type CleMonde =
  | 'pixel'
  | 'braille'
  | 'sillons'
  | 'gravure'
  | 'mosaique'
  | 'encre'
  | 'terrazzo'
  | 'touffe'
  | 'esquille'
  | 'bobinette'
  | 'ritournelle'
  | 'madrure'
  | 'halin'
  | 'brouillamini'
  | 'chamade'
  | 'chantourne'
  | 'guingois'
  | 'mascaret'
  | 'ramage'
  | 'volubilis'
  | (string & { readonly __monde?: never });

/** Le monde de plantation d'une dalle : {design, palette, teinte} (`p.monde`). */
export interface MondeDalle {
  m: string;
  p: string;
  h: number;
}

/** Une graine telle que le moteur la passe à `labelOf`. */
export interface GraineMoteur {
  /** 'gray' (une cellule vide), 'promi' (une parole), 'nuee' (un Cercle) */
  kind: string;
  pid?: number | null;
  nuee?: string;
}

export interface EtiquetteDalle {
  who: string | null;
  title: string;
}

type Libre = (...a: unknown[]) => unknown;

/** La porte `window.Toile` du moteur. */
export interface MoteurToile {
  // ── employé par la vraie app depuis L0 ──
  sync(ids: number[]): void;
  setTheme(m: string): void;
  getTheme(): string;
  curWorld(): string;
  setPalette(k: string): void;
  getPalette(): string;
  setHue(d: number): void;
  getHue(): number;
  palettes(): Record<string, { name: string; cols: number[][] }>;
  renderTo(cv: HTMLCanvasElement, ech: number, clair: boolean, o?: { vue?: boolean }): boolean;
  redraw(): void;
  semisNeuf(): boolean;
  mondeCourant(): MondeDalle;
  cle(): number;
  labelsOn?: () => boolean;
  labelOf?: (s: GraineMoteur) => EtiquetteDalle | null;
  // ── l'inventaire du prototype, à préciser lot par lot ──
  dalleAbs: Libre;
  dalleTrame: Libre;
  cols: Libre;
  preview: Libre;
  addPromi: Libre;
  reserve: Libre;
  voisines: Libre;
  dalleAvenir: Libre;
  vueVers: Libre;
  vue: Libre;
  voisinesBande: Libre;
  shapeOf: Libre;
  repaint: Libre;
  hit: Libre;
  addNuee: Libre;
  repaintWorld: Libre;
  refigeCouleurs: Libre;
  fondToile: Libre;
  colorOf: Libre;
  tonsDe: Libre;
  taille: Libre;
  scale: Libre;
  resetView: Libre;
  reGrayStudio: Libre;
  reGray: Libre;
  fingers: Libre;
  ecarte: Libre;
  dalleGeneree: Libre;
  curTheme: Libre;
  applyReserve: Libre;
  addMember: Libre;
  vu: Libre;
  mauve: Libre;
  apercuImage: Libre;
}

/** Les fonctions `window.Toile_*` du moteur (lecture et commandes de bas niveau). */
export interface MoteurFonctions {
  Toile_resize(): void;
  Toile_state(): { running: boolean; qt: number; theme: string };
  Toile_lecture(): {
    W: number;
    H: number;
    vue: { s: number; ox: number; oy: number };
    graines: Array<{ pid: number | null; x: number; y: number; w: number; kind: string }>;
  };
  Toile_graines(): Array<[number | null, number, number, string]>;
  Toile_liven: Libre;
  Toile_cellules: Libre;
  Toile_recadre: Libre;
  Toile_vueLue: Libre;
  Toile_autoView: Libre;
  Toile_previewLive: Libre;
  Toile_probe: Libre;
}
