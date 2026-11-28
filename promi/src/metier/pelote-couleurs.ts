/**
 * LES COULEURS DE LA PELOTE (lot 6) — ce qui DÉCIDE des couleurs de l'Aura, sans rien peindre : le ton du poil (le sol), celui du corps, celui de
 * « PARTAGER MA PELOTE », le fond de la sphère, et ce qui décide de la lisibilité d'une île (la cession de teinte du chantier 59, la hauteur de
 * rampe d'une île sous Ingénu).
 *
 * Le prototype : le bloc `lot-AURA-PELOTE` d'app.html — `plancher`, `_lab`, `_okl`, `_kaki`, `_dE00`, `_lumRel`, `_contraste`, `ingenu`,
 * `solIdxEff`, `couleursIles`, `solPalette`, `corpsTient`, `nouveauCorps`, `corps`, `nouveauTexte`, `texteBouton`, `_rendue`, `nouveauSol`,
 * `pageCouleur`, `fondPage`, `versBlanc`, `versNoir`, `solEffectif`, `_prochede`, `fondSphere`, `lisibiliteIle`, la partie qui décide de
 * `dalleLisible` et la boucle de cession d'`iles` — et `window._teinte` (lot-V119-PELOTE : `okl`, `deOkl`, `ajuste`, `vive`, `kaki`). Les
 * formules et l'ordre des tirages sont les siens, à l'identique : tests/unitaires/pelote-couleurs.test.ts porte en dur ce que le prototype rend.
 *
 * Les règles qui les fixent (CLAUDE.md) : v123 (le corps, une autre teinte de la palette, jamais kaki), v124 et v125 (le ton du bouton, ≥ 3:1,
 * jamais kaki, sa teinte gardée), v125 (« jamais le même sol ni le même corps deux fois de suite »), v142 (sous Ingénu, jamais le crème), v202a et
 * v203 (C-275, C-204 : le poil et le corps sont des tons EXACTS de la palette ; l'intérieur, le ton qui contraste le plus avec le poil), Q210 (le
 * fond de la sphère en clair, tiré vers le crème), le chantier 59 (seule la teinte cède, et seulement en sombre).
 *
 * Tout ce que le prototype lisait dans la page est un PARAMÈTRE : la palette du Studio (`Toile.cols()`), Ingénu (`mondeCourant().p === 'signal'`),
 * le thème, la couleur de la page de l'Aura (lue sur l'écran), les îles (le Lab que le moteur déclare pour chaque parole tenue), la rampe du
 * velours (le moteur de la Pelote), le stockage, le hasard (l'ordre des tirages est celui de `Math.random` dans le prototype) et l'heure.
 * Ce qui changeait d'une ouverture à l'autre (le ton tiré, l'ordre du corps, l'ordre du bouton) vit dans un `EtatCouleurs` que l'écran garde et
 * que ces fonctions mettent à jour. Aucune minuterie, aucune page, aucun stockage du navigateur ici.
 */

/** une couleur sRGB, de 0 à 255 (une palette peut porter des fractions : la jauge de teinte du Studio les décale) */
export type RGB = readonly [number, number, number];
/** une couleur CIELAB (D65), celle que le moteur déclare pour une dalle (`__dalleInfo.lab`) */
export type Lab = readonly [number, number, number];
/** une couleur OKLCH : clarté, chroma, teinte en degrés */
export type Oklch = readonly [number, number, number];

/** ce que l'écran sait au moment où l'on décide */
export interface ContexteCouleurs {
  /** les tons de la palette du Studio, déjà décalés par la jauge (`Toile.cols()`) */
  readonly palette: readonly RGB[];
  /** la palette est Ingénu (clé `signal`) */
  readonly ingenu: boolean;
  /** le thème clair */
  readonly clair: boolean;
  /** la couleur de fond de l'écran de l'Aura, lue sur l'écran ; null si elle ne se lit pas */
  readonly page: RGB | null;
  /** pour chaque parole tenue, dans l'ordre des îles : le Lab moyen que le moteur déclare pour sa dalle (null : la dalle ne s'est pas rendue) */
  readonly iles: readonly (Lab | null | undefined)[];
  /** la rampe du velours d'un ton (le moteur de la Pelote : `rampeVelours`) */
  readonly rampe: (base: RGB) => readonly (readonly number[])[];
}

/** ce qui change d'une ouverture de l'Aura à l'autre, gardé par l'écran (le prototype : `SOL_IDX`, `SOL_EVITE`, `CORPS_ORDRE`, `TEXTE_ORDRE`) */
export interface EtatCouleurs {
  /** le ton tiré pour le poil à l'ouverture (`SOL_IDX`) — le ton VU peut en être un autre (`solIdxEff`) */
  solTire: number;
  /** le ton du poil de l'ouverture d'avant, qui cède (`SOL_EVITE`) ; −1 : aucun */
  solEvite: number;
  /** l'ordre tiré des tons du corps (`CORPS_ORDRE`) */
  corpsOrdre: number[];
  /** l'indice du dernier corps rendu (`CORPS_MEMO.idx`) ; −1 : aucun ton de la palette (dernier recours) */
  corpsIdx: number;
  /** l'ordre tiré des tons de « PARTAGER MA PELOTE » (`TEXTE_ORDRE`) */
  texteOrdre: number[];
}

/** le stockage de l'appareil (une clé, une chaîne) */
export interface StockageCouleurs {
  lire(cle: string): string | null;
  ecrire(cle: string, v: string): void;
}

/** le hasard, dans [0, 1) ; l'ordre des appels est celui du prototype */
export type Hasard = () => number;

export function etatCouleursInitial(): EtatCouleurs {
  return { solTire: 0, solEvite: -1, corpsOrdre: [], corpsIdx: -1, texteOrdre: [] };
}

/* ── LES CONSTANTES (lot-AURA-PELOTE) ───────────────────────────────────────────────────────────────────────────────────────────────── */

/** la nature de base : le poil avant que la palette soit là (`NAT.promi`) */
export const NAT_PROMI: RGB = [130, 174, 248];
/** le fond clair (§3) */
export const CREME: RGB = [0xf7, 0xf0, 0xde];
/** la page de l'Aura quand elle ne se lit pas (v207, C-294) : #EAD9B9 en clair, la seiche #050302 en sombre */
export const PAGE_CLAIR: RGB = [0xea, 0xd9, 0xb9];
export const PAGE_SOMBRE: RGB = [0x05, 0x03, 0x02];
/** l'encre du clair, la couleur du bouton quand la palette manque */
export const ENCRE_CLAIR: RGB = [32, 25, 8];
/** la cession de teinte se déclenche sous 31 sur le masque (le juge garde SON plancher, 15) */
export const DE_DECLENCHE = 31;
export const DE_PLANCHER = 15;
/** la visée d'une cession, et celle d'une île sous Ingénu en clair (v203) */
export const DE_VISE = 32;
export const DE_VISE_C = 48;
/** jamais plus de trois tours de cession */
export const DE_ESSAIS = 3;
/** le corps tient ΔE00 ≥ 15 face au poil (v123) */
export const CORPS_ECART = 15;
/** un ton du poil se détache de la page à 42 de luminosité (§3) */
export const ECART_LUM_PAGE = 42;
/** le poil s'écarte des îles (C-275, v203) : 30, sinon 18 */
export const ECART_ILE = 30;
export const ECART_ILE2 = 18;
/** en clair, le fond de la sphère est le poil tiré vers le crème (Q210) */
export const SOL_CREME = 0.39;
/** une couleur d'état à moins de 24 (Lab) d'un ton l'exclut d'une cession (§3 : un état ne se dit jamais par une dalle) */
export const PROCHE_ETAT = 24;
/** une ouverture qui passe deux fois dans les 400 ms garde la référence de l'ouverture d'avant */
export const DOUBLE_OUVERTURE_MS = 400;
/** la couleur rendue change d'au moins 14 (ΔE00) d'une ouverture à l'autre (v125), en douze tirages au plus */
export const ECART_OUVERTURE = 14;
export const TIRAGES_OUVERTURE = 12;
/** la clé du stockage : la couleur vue à l'ouverture d'avant */
export const CLE_VUE = 'promi_pelote_vue';
/** les hauteurs de rampe d'une île sous Ingénu, dans l'ordre où on les essaie (1,8 d'abord en clair : là où il suffit, rien ne change) */
export const HAUTEURS_INGENU_CLAIR = [1.8, 1.1, 0.85, 0.65, 0.45, 2.3] as const;
export const HAUTEURS_INGENU_SOMBRE = [1.1, 0.85, 1.4, 0.65, 1.8, 0.45, 2.3] as const;

/** le plancher de cession d'une île, sur le masque (`plancher`) */
export function plancher(): number {
  return DE_DECLENCHE;
}

/* ── LES CONVERSIONS — celles du prototype, au chiffre près ───────────────────────────────────────────────────────────────────────── */

function lin(v: number): number {
  const x = v / 255;
  return x <= 0.04045 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4);
}
function fl(t: number): number {
  return t > 0.008856 ? Math.pow(t, 1 / 3) : 7.787 * t + 16 / 116;
}
/** sRGB → CIELAB (`_lab`) */
export function lab(c: readonly number[]): Lab {
  const r = lin(c[0]!),
    g = lin(c[1]!),
    b = lin(c[2]!);
  const X = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047,
    Y = 0.2126 * r + 0.7152 * g + 0.0722 * b,
    Z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883;
  const fx = fl(X),
    fy = fl(Y),
    fz = fl(Z);
  return [116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)];
}
/** sRGB → OKLCH (`_okl`, `_teinte.okl`) */
export function okl(c: readonly number[]): Oklch {
  const r = lin(c[0]!),
    g = lin(c[1]!),
    b = lin(c[2]!);
  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b),
    m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b),
    s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
  const L = 0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s,
    a = 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s,
    bb = 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s;
  return [L, Math.hypot(a, bb), ((Math.atan2(bb, a) * 180) / Math.PI + 360) % 360];
}
function okBrut(L: number, C: number, h: number): [number, number, number] {
  const a = C * Math.cos((h * Math.PI) / 180),
    b = C * Math.sin((h * Math.PI) / 180);
  let l = L + 0.3963377774 * a + 0.2158037573 * b,
    m = L - 0.1055613458 * a - 0.0638541728 * b,
    s = L - 0.0894841775 * a - 1.291485548 * b;
  l = l * l * l;
  m = m * m * m;
  s = s * s * s;
  return [
    4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
    -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
    -0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s,
  ];
}
function gam(v: number): number {
  const x = v < 0 ? 0 : v > 1 ? 1 : v;
  return Math.round(255 * (x <= 0.0031308 ? 12.92 * x : 1.055 * Math.pow(x, 1 / 2.4) - 0.055));
}
/** OKLCH → sRGB, la chroma réduite jusqu'à rentrer dans l'écran (`_teinte.deOkl`) */
export function deOkl(L: number, C: number, h: number): RGB {
  let q = okBrut(L, C, h);
  for (let k = 0; k < 60; k++) {
    q = okBrut(L, C, h);
    if (q[0] >= -0.0006 && q[0] <= 1.0006 && q[1] >= -0.0006 && q[1] <= 1.0006 && q[2] >= -0.0006 && q[2] <= 1.0006)
      break;
    C *= 0.95;
  }
  return [gam(q[0]), gam(q[1]), gam(q[2])];
}
/** le kaki (v115) : OKLCH h 78–140°, C 0,015–0,10, L 0,20–0,80 (`_kaki`, `_teinte.kaki`) */
export function kaki(c: readonly number[]): boolean {
  const o = okl(c);
  return o[2] >= 78 && o[2] <= 140 && o[1] >= 0.015 && o[1] <= 0.1 && o[0] >= 0.2 && o[0] <= 0.8;
}
/** ΔE 2000 entre deux couleurs sRGB (`_dE00`) */
export function dE00(c1: readonly number[], c2: readonly number[]): number {
  const A = lab(c1),
    B = lab(c2),
    R = Math.PI / 180,
    L1 = A[0],
    a1 = A[1],
    b1 = A[2],
    L2 = B[0],
    a2 = B[1],
    b2 = B[2];
  const C1 = Math.hypot(a1, b1),
    C2 = Math.hypot(a2, b2),
    Cb = (C1 + C2) / 2,
    G7 = 0.5 * (1 - Math.sqrt(Math.pow(Cb, 7) / (Math.pow(Cb, 7) + Math.pow(25, 7))));
  const ap1 = (1 + G7) * a1,
    ap2 = (1 + G7) * a2,
    Cp1 = Math.hypot(ap1, b1),
    Cp2 = Math.hypot(ap2, b2);
  const h1 = (Math.atan2(b1, ap1) / R + 360) % 360,
    h2 = (Math.atan2(b2, ap2) / R + 360) % 360,
    dL = L2 - L1,
    dC = Cp2 - Cp1;
  let dh = h2 - h1;
  if (Cp1 * Cp2 === 0) dh = 0;
  else if (dh > 180) dh -= 360;
  else if (dh < -180) dh += 360;
  const dH = 2 * Math.sqrt(Cp1 * Cp2) * Math.sin((dh * R) / 2),
    Lb = (L1 + L2) / 2,
    Cpb = (Cp1 + Cp2) / 2;
  let hb = h1 + h2;
  if (Cp1 * Cp2 !== 0)
    hb = Math.abs(h1 - h2) <= 180 ? (h1 + h2) / 2 : h1 + h2 < 360 ? (h1 + h2 + 360) / 2 : (h1 + h2 - 360) / 2;
  const T =
    1 -
    0.17 * Math.cos((hb - 30) * R) +
    0.24 * Math.cos(2 * hb * R) +
    0.32 * Math.cos((3 * hb + 6) * R) -
    0.2 * Math.cos((4 * hb - 63) * R);
  const Sl = 1 + (0.015 * (Lb - 50) * (Lb - 50)) / Math.sqrt(20 + (Lb - 50) * (Lb - 50)),
    Sc = 1 + 0.045 * Cpb,
    Sh = 1 + 0.015 * Cpb * T;
  const Rt =
    -2 *
    Math.sqrt(Math.pow(Cpb, 7) / (Math.pow(Cpb, 7) + Math.pow(25, 7))) *
    Math.sin(60 * R * Math.exp(-Math.pow((hb - 275) / 25, 2)));
  return Math.sqrt(Math.pow(dL / Sl, 2) + Math.pow(dC / Sc, 2) + Math.pow(dH / Sh, 2) + Rt * (dC / Sc) * (dH / Sh));
}
/** la luminance relative (WCAG) (`_lumRel`) */
export function lumRel(c: readonly number[]): number {
  return 0.2126 * lin(c[0]!) + 0.7152 * lin(c[1]!) + 0.0722 * lin(c[2]!);
}
/** le contraste WCAG (`_contraste`) */
export function contraste(a: readonly number[], b: readonly number[]): number {
  const x = lumRel(a),
    y = lumRel(b);
  return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05);
}
/** la luminosité « à l'œil » du §3, sur 0–255 (`_lum`) */
export function lumOeil(c: readonly number[]): number {
  return 0.2126 * c[0]! + 0.7152 * c[1]! + 0.0722 * c[2]!;
}
/** la teinte gardée, la clarté OKLCH déplacée par pas de 0,005 jusqu'au contraste voulu face au fond (`_teinte.ajuste`, v125) */
export function ajuste(c0: readonly number[], fond: readonly number[], ratio: number): RGB {
  const c: RGB = [c0[0]! | 0, c0[1]! | 0, c0[2]! | 0];
  if (contraste(c, fond) >= ratio) return c;
  const o = okl(c),
    sens = lumRel(fond) > 0.18 ? -1 : 1;
  let L = o[0],
    q: RGB = c;
  for (let i = 0; i < 220; i++) {
    L += sens * 0.005;
    if (L < 0.02 || L > 0.995) break;
    q = deOkl(L, o[1], o[2]);
    if (contraste(q, fond) >= ratio) return q;
  }
  return q;
}
/** la même teinte sortie du kaki par la chroma (`_teinte.vive`) */
export function vive(c: readonly number[]): RGB {
  const o = okl(c);
  return deOkl(o[0], Math.max(o[1], 0.112), o[2]);
}
/** vers le blanc, de t (`versBlanc`) */
export function versBlanc(c: readonly number[], t: number): RGB {
  return [c[0]! + (255 - c[0]!) * t, c[1]! + (255 - c[1]!) * t, c[2]! + (255 - c[2]!) * t];
}
/** vers le noir, de t (`versNoir`) */
export function versNoir(c: readonly number[], t: number): RGB {
  return [c[0]! * (1 - t), c[1]! * (1 - t), c[2]! * (1 - t)];
}
function entier(c: readonly number[]): RGB {
  return [c[0]! | 0, c[1]! | 0, c[2]! | 0];
}
function arrondi(c: readonly number[]): RGB {
  return [Math.round(c[0]!), Math.round(c[1]!), Math.round(c[2]!)];
}
function ecartLab(a: readonly number[], b: readonly number[]): number {
  return Math.sqrt(Math.pow(a[0]! - b[0]!, 2) + Math.pow(a[1]! - b[1]!, 2) + Math.pow(a[2]! - b[2]!, 2));
}
/** un tableau mélangé (Fisher–Yates, du dernier au premier : l'ordre des appels au hasard est celui du prototype) */
function melange(L: number[], hasard: Hasard): number[] {
  for (let i = L.length - 1; i > 0; i--) {
    const j = (hasard() * (i + 1)) | 0;
    const t = L[i]!;
    L[i] = L[j]!;
    L[j] = t;
  }
  return L;
}

/* ── LA PAGE ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── */

/** la page qu'on voit autour de la Pelote (`pageCouleur`, v207) */
export function pageCouleur(ctx: ContexteCouleurs): RGB {
  return ctx.page ?? (ctx.clair ? PAGE_CLAIR : PAGE_SOMBRE);
}
/** le fond contre lequel « PARTAGER MA PELOTE » se lit (`fondPage`) : la crème en clair, la page lue en sombre (l'encre du clair à défaut) */
export function fondPage(ctx: ContexteCouleurs): RGB {
  if (ctx.clair) return CREME;
  return ctx.page ?? ENCRE_CLAIR;
}

/* ── LE POIL (LE SOL) ────────────────────────────────────────────────────────────────────────────────────────────────────────────── */

/** ce que le tirage du poil a décidé : le ton VU, et, quand il y a des îles, son écart à la plus proche et s'il est forcé (C-275 passe avant v125) */
export interface ChoixSol {
  readonly i: number;
  readonly ecart: number | null;
  readonly force: boolean | null;
}

/** les Lab des îles que le poil doit éviter (`couleursIles`) : les quarante premières paroles tenues, celles dont la dalle s'est rendue */
export function couleursIles(ctx: ContexteCouleurs): Lab[] {
  const out: Lab[] = [];
  for (let k = 0; k < ctx.iles.length && k < 40; k++) {
    const l = ctx.iles[k];
    if (l) out.push(l);
  }
  return out;
}

/**
 * LE TON DU POIL QU'ON VERRA (`solIdxEff`, v202a, v203) : le ton tiré ; s'il ne se détache pas de la page (< 42 de luminosité), le suivant qui
 * s'en détache ; à défaut, celui qui s'en détache le plus. Parmi ceux qui se détachent, dans l'ordre du tirage : le premier à 30 des îles qui
 * n'est pas celui de l'ouverture d'avant, puis à 18, puis à 30 même s'il l'est, puis le plus éloigné. Sous Ingénu, jamais le crème.
 */
export function choixSol(ctx: ContexteCouleurs, etat: EtatCouleurs): ChoixSol {
  const c = ctx.palette;
  if (!c.length) return { i: -1, ecart: null, force: null };
  const ing = ctx.ingenu,
    n = c.length,
    b = Math.max(0, Math.min(ing && etat.solTire > 2 ? etat.solTire % 3 : etat.solTire, n - 1));
  const pl = lumOeil(pageCouleur(ctx)),
    ok: number[] = [];
  let best = -1,
    bd = -1;
  for (let k = 0; k < n; k++) {
    const i = (b + k) % n;
    if (ing && i > 2) continue;
    const d = Math.abs(lumOeil(c[i]!) - pl);
    if (d >= ECART_LUM_PAGE) ok.push(i);
    else if (d > bd) {
      bd = d;
      best = i;
    }
  }
  if (!ok.length) return { i: best, ecart: null, force: null };
  const IL = couleursIles(ctx);
  if (!IL.length) return { i: ok[0]!, ecart: null, force: null };
  const M = ok.map((i) => {
    const t = lab(c[i]!);
    let m = 1e9;
    for (const L of IL) m = Math.min(m, ecartLab(t, L));
    return m;
  });
  const evite = etat.solEvite;
  let bi = -1,
    bm = -1,
    j: number;
  for (j = 0; j < ok.length && bi < 0; j++)
    if (M[j]! >= ECART_ILE && ok[j] !== evite) {
      bi = ok[j]!;
      bm = M[j]!;
    }
  for (j = 0; j < ok.length && bi < 0; j++)
    if (M[j]! >= ECART_ILE2 && ok[j] !== evite) {
      bi = ok[j]!;
      bm = M[j]!;
    }
  for (j = 0; j < ok.length && bi < 0; j++)
    if (M[j]! >= ECART_ILE) {
      bi = ok[j]!;
      bm = M[j]!;
    }
  if (bi < 0) {
    for (j = 0; j < ok.length; j++)
      if (M[j]! > bm) {
        bm = M[j]!;
        bi = ok[j]!;
      }
  }
  let autres = 0;
  for (j = 0; j < ok.length; j++) if (ok[j] !== bi && M[j]! >= ECART_ILE2) autres++;
  return { i: bi, ecart: Math.round(bm * 10) / 10, force: bi === evite && !autres };
}
/** l'indice du ton du poil qu'on verra (`solIdxEff`) ; −1 : pas de palette */
export function solIdxEff(ctx: ContexteCouleurs, etat: EtatCouleurs): number {
  return choixSol(ctx, etat).i;
}
/** le poil : un ton EXACT de la palette (`solPalette`, `solEffectif` — v202a, C-275) ; la nature de base avant que la palette soit là */
export function solEffectif(ctx: ContexteCouleurs, etat: EtatCouleurs): RGB {
  const c = ctx.palette,
    i = solIdxEff(ctx, etat);
  if (c.length && i >= 0) {
    const t = c[i] ?? c[0];
    if (t) return entier(t);
  }
  return NAT_PROMI;
}

/* ── LE CORPS ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── */

/** le corps tient : jamais kaki, ΔE00 ≥ 15 face au poil et à chaque marche de sa rampe (`corpsTient`, v123) */
export function corpsTient(ctx: ContexteCouleurs, c: readonly number[], poil: RGB): boolean {
  if (kaki(c) || dE00(c, poil) < CORPS_ECART) return false;
  for (const m of ctx.rampe(poil)) if (dE00(c, m) < CORPS_ECART) return false;
  return true;
}
/** un ordre neuf des tons du corps (`nouveauCorps`) — sous Ingénu, jamais le crème (le quatrième ton) */
export function nouveauCorps(ctx: ContexteCouleurs, etat: EtatCouleurs, hasard: Hasard): void {
  const n = ctx.palette.length || 4,
    L: number[] = [];
  for (let i = 0; i < n; i++) if (!(ctx.ingenu && i > 2)) L.push(i);
  etat.corpsOrdre = melange(L, hasard);
}
/**
 * LE CORPS (`corps`, v123, v202a, v203 — Q618/Q619) : parmi les autres tons exacts de la palette, celui qui contraste le PLUS avec le poil (ΔE00),
 * jamais kaki tant qu'un ton qui ne l'est pas existe. Les replis qui suivent (écarter un ton en clarté, la crème ou la seiche) ne servent qu'à
 * une palette sans autre ton. Met à jour `etat.corpsIdx` (et `etat.corpsOrdre` s'il n'est plus valable). null : pas de palette.
 */
export function corps(ctx: ContexteCouleurs, etat: EtatCouleurs, hasard: Hasard): RGB | null {
  const P = ctx.palette;
  if (!P.length) return null;
  const ing = ctx.ingenu;
  if (!etat.corpsOrdre.length || etat.corpsOrdre.some((i) => i >= P.length || (ing && i > 2)))
    nouveauCorps(ctx, etat, hasard);
  const sE = solIdxEff(ctx, etat),
    poil = solEffectif(ctx, etat);
  const ORD = etat.corpsOrdre.filter((i) => i !== sE);
  let c: RGB | null = null,
    idx = -1,
    bd = -1,
    bdK = -1,
    cK: RGB | null = null,
    idxK = -1;
  for (const o of ORD) {
    const q = entier(P[o]!),
      de = dE00(q, poil);
    if (!kaki(q)) {
      if (de > bd) {
        bd = de;
        c = q;
        idx = o;
      }
    } else if (de > bdK) {
      bdK = de;
      cK = q;
      idxK = o;
    }
  }
  if (!c && cK) {
    c = cK;
    idx = idxK;
  }
  if (!c) {
    for (let k = 0; k < P.length && !c; k++) {
      if (k !== sE && !(ing && k > 2)) {
        c = entier(P[k]!);
        idx = k;
      }
    }
  }
  if (c) {
    etat.corpsIdx = idx;
    return c;
  }
  for (let k = 0; k < etat.corpsOrdre.length && !c; k++) {
    const o = etat.corpsOrdre[k]!,
      q = P[o]!;
    for (let pas = 1; pas <= 16 && !c; pas++) {
      const s = arrondi(versBlanc(q, pas * 0.05));
      if (corpsTient(ctx, s, poil)) {
        c = s;
        idx = o;
      }
    }
    for (let pas = 1; pas <= 16 && !c; pas++) {
      const s = arrondi(versNoir(q, pas * 0.05));
      if (corpsTient(ctx, s, poil)) {
        c = s;
        idx = o;
      }
    }
  }
  if (!c && ing && etat.corpsOrdre.length) {
    const o = etat.corpsOrdre[0]!;
    c = arrondi(versNoir(P[o]!, 0.45));
    idx = o;
  }
  if (!c) {
    c = corpsTient(ctx, CREME, poil) ? CREME : [5, 3, 2];
    idx = -1;
  }
  etat.corpsIdx = idx;
  return c;
}

/* ── « PARTAGER MA PELOTE » ──────────────────────────────────────────────────────────────────────────────────────────────────────── */

/** un ordre neuf des tons du bouton (`nouveauTexte`) */
export function nouveauTexte(ctx: ContexteCouleurs, etat: EtatCouleurs, hasard: Hasard): void {
  const n = ctx.palette.length || 4,
    L: number[] = [];
  for (let i = 0; i < n; i++) L.push(i);
  etat.texteOrdre = melange(L, hasard);
}
/**
 * LE TON DE « PARTAGER MA PELOTE » (`texteBouton`, v124, v125) : dans l'ordre tiré, le premier ton — ni celui tiré pour le poil, ni celui du
 * corps — qui, sa clarté ajustée à 3:1 face au fond, n'est pas kaki ; à défaut le même sorti du kaki par la chroma ; l'encre du mode seulement
 * sans autre ton. idx −1 : l'encre.
 */
export function texteBouton(ctx: ContexteCouleurs, etat: EtatCouleurs, hasard: Hasard): { rgb: RGB; idx: number } {
  const P = ctx.palette,
    f = fondPage(ctx),
    encre: RGB = ctx.clair ? ENCRE_CLAIR : CREME;
  if (!P.length) return { rgb: encre, idx: -1 };
  if (!etat.texteOrdre.length || etat.texteOrdre.some((i) => i >= P.length)) nouveauTexte(ctx, etat, hasard);
  corps(ctx, etat, hasard); /* le corps d'abord : son indice entre dans l'exclusion */
  const exclu = (i: number): boolean => i === etat.solTire || i === etat.corpsIdx;
  for (const i of etat.texteOrdre) {
    if (exclu(i)) continue;
    const q = ajuste(P[i]!, f, 3);
    if (!kaki(q)) return { rgb: q, idx: i };
  }
  for (const i of etat.texteOrdre) {
    if (exclu(i)) continue;
    const q = ajuste(vive(ajuste(P[i]!, f, 3)), f, 3);
    if (!kaki(q)) return { rgb: q, idx: i };
  }
  return { rgb: encre, idx: -1 };
}

/* ── LA COULEUR RENDUE, L'OUVERTURE ──────────────────────────────────────────────────────────────────────────────────────────────── */

/** la couleur que la boule rend, à peu près : la marche médiane de la rampe du poil pour deux tiers, le corps pour un tiers (`_rendue`) */
export function couleurRendue(ctx: ContexteCouleurs, etat: EtatCouleurs, hasard: Hasard): RGB | null {
  const p = solEffectif(ctx, etat),
    R = ctx.rampe(p),
    m = R[(R.length * 0.55) | 0] ?? p,
    c = corps(ctx, etat, hasard);
  if (!c) return null;
  return [
    Math.round(m[0]! * 0.675 + c[0] * 0.325),
    Math.round(m[1]! * 0.675 + c[1] * 0.325),
    Math.round(m[2]! * 0.675 + c[2] * 0.325),
  ];
}

type Brut = Record<string, unknown>;
function objet(v: unknown): Brut | null {
  return v && typeof v === 'object' && !Array.isArray(v) ? (v as Brut) : null;
}
function rgbLu(v: unknown): RGB | null {
  return Array.isArray(v) && v.length >= 3 && v.slice(0, 3).every((x) => typeof x === 'number')
    ? [v[0] as number, v[1] as number, v[2] as number]
    : null;
}

/** ce que l'ouverture a décidé, et ce qu'elle a écrit dans le stockage */
export interface Ouverture {
  /** le ton tiré pour le poil (`SOL_IDX`) */
  readonly solTire: number;
  /** le ton vu, le corps, sa couleur rendue */
  readonly solVu: number;
  readonly corpsIdx: number;
  readonly rendue: RGB | null;
}

/**
 * UNE OUVERTURE DE L'AURA (`nouveauSol`, v125) : jusqu'à douze couples (poil, corps) tirés ; on garde le premier dont la couleur RENDUE est à
 * ΔE00 ≥ 14 de celle de l'ouverture d'avant, avec un poil ET un corps différents ; à défaut, le plus éloigné. La couleur vue est gardée
 * (`promi_pelote_vue`) ; une ouverture qui repasse dans les 400 ms garde la référence de l'ouverture d'avant. Puis un ordre neuf pour le bouton.
 * `maintenant` : l'heure en ms (le prototype : `Date.now()`).
 */
export function nouvelleOuverture(
  ctx: ContexteCouleurs,
  etat: EtatCouleurs,
  hasard: Hasard,
  stockage: StockageCouleurs,
  maintenant: number,
): Ouverture {
  const n = ctx.palette.length || 4;
  let av: Brut | null = null;
  try {
    av = objet(JSON.parse(stockage.lire(CLE_VUE) ?? 'null'));
  } catch {
    av = null;
  }
  const t0 = typeof av?.['t'] === 'number' ? av['t'] : 0;
  const ref: Brut | null = av && av['p'] && maintenant - t0 < DOUBLE_OUVERTURE_MS ? objet(av['p']) : av;
  av = ref;
  const avS = av?.['s'],
    avK = av?.['k'],
    avC = av ? rgbLu(av['c']) : null;
  etat.solEvite = av && avS != null && n > 2 && typeof avS === 'number' ? avS : -1;
  let best: { d: number; s: number; o: number[]; c: RGB | null } | null = null;
  for (let essai = 0; essai < TIRAGES_OUVERTURE; essai++) {
    etat.solTire = (hasard() * (ctx.ingenu ? Math.min(3, n) : n)) | 0;
    nouveauCorps(ctx, etat, hasard);
    const mx = couleurRendue(ctx, etat, hasard);
    const sE = solIdxEff(ctx, etat);
    const d = avC && mx ? dE00(mx, avC) : 99,
      meme = !!(av && (avS === sE || avK === etat.corpsIdx)) && n > 2;
    if (!best || (meme ? 0 : d) > best.d)
      best = { d: meme ? 0 : d, s: etat.solTire, o: etat.corpsOrdre.slice(), c: mx };
    if (!meme && d >= ECART_OUVERTURE) break;
  }
  let rendue: RGB | null = null;
  if (best) {
    etat.solTire = best.s;
    etat.corpsOrdre = best.o;
    rendue = best.c;
    corps(ctx, etat, hasard);
    const vue = {
      s: solIdxEff(ctx, etat),
      k: etat.corpsIdx,
      c: best.c,
      t: maintenant,
      p: ref ? { s: ref['s'], k: ref['k'], c: ref['c'] } : null,
    };
    stockage.ecrire(CLE_VUE, JSON.stringify(vue));
  }
  nouveauTexte(ctx, etat, hasard); /* v124 : et une couleur neuve pour « PARTAGER MA PELOTE » */
  return { solTire: etat.solTire, solVu: solIdxEff(ctx, etat), corpsIdx: etat.corpsIdx, rendue };
}

/* ── LE FOND DE LA SPHÈRE, LES ÎLES ──────────────────────────────────────────────────────────────────────────────────────────────── */

/** le fond de la sphère (`fondSphere`) : le poil ; en clair, tiré vers le crème de 0,39 (Q210) — sans arrondi, comme le prototype */
export function fondSphere(ctx: ContexteCouleurs, etat: EtatCouleurs): RGB {
  const s = solEffectif(ctx, etat);
  if (ctx.clair)
    return [
      s[0] + (CREME[0] - s[0]) * SOL_CREME,
      s[1] + (CREME[1] - s[1]) * SOL_CREME,
      s[2] + (CREME[2] - s[2]) * SOL_CREME,
    ];
  return s;
}

/**
 * LA LISIBILITÉ D'UNE ÎLE, LÀ OÙ LE PEINTRE LA FABRIQUE (`lisibiliteIle`) : le masque de l'île donne pour chaque pixel l'indice de sa couleur dans
 * la table de `batIles`, et l'indice 0 est le sol ; l'écart (CIELAB) entre la couleur moyenne de ce mélange et le fond. null : masque vide.
 */
export function lisibiliteIle(
  masque: ArrayLike<number>,
  table: readonly (readonly number[] | null | undefined)[],
  fond: readonly number[],
): { dE: number; sol: 0 } | null {
  let n = 0,
    sL = 0,
    sa = 0,
    sb = 0;
  for (let q = 0; q < masque.length; q++) {
    const idx = masque[q]!,
      c = idx === 0 ? fond : table[idx];
    if (!c) continue;
    const l = lab(c);
    n++;
    sL += l[0];
    sa += l[1];
    sb += l[2];
  }
  if (!n) return null;
  return { dE: ecartLab([sL / n, sa / n, sb / n], lab(fond)), sol: 0 };
}

/**
 * LA BOUCLE DE CESSION (chantier 59, `iles`) — seulement en sombre, trois tours au plus : à chaque tour, les îles encore sous le plancher
 * cèdent d'un rang (`cede`, par clé de dalle, mis à jour) et l'écran rebâtit ; un tour qui ne gagne rien est le dernier. `mesure` rend l'écart
 * de chaque île bâtie (null : à ne pas compter), `rebatit` refait les îles avec les rangs de `cede`.
 */
export function cederIles(
  cles: readonly string[],
  clair: boolean,
  cede: Record<string, number>,
  mesure: () => readonly (number | null)[],
  rebatit: () => void,
): { tours: number; restes: number[] } {
  const restes: number[] = [];
  let tours = 0,
    avant = 1e9;
  for (tours = 0; !clair && tours < DE_ESSAIS; tours++) {
    const dE = mesure(),
      marque: string[] = [];
    for (let k = 0; k < dE.length && k < cles.length; k++) {
      const v = dE[k];
      if (v == null) continue;
      if (v < plancher()) marque.push(cles[k]!);
    }
    const reste = marque.length;
    restes.push(reste);
    if (!reste || reste >= avant) break;
    avant = reste;
    for (const w of marque) cede[w] = (cede[w] ?? 0) + 1;
    rebatit();
  }
  return { tours, restes };
}

/** les deux couleurs d'état qu'une dalle ne porte jamais (§3) : l'amande « tenu » et le terracotta « à tenir » (`ETAT_MENTHE`, `ETAT_TERRA`) */
const ETAT_MENTHE = lab([0x8f, 0xe0, 0x8f]),
  ETAT_TERRA = lab([0xdd, 0x4d, 0x23]);
/** un Lab trop proche d'une couleur d'état (`_prochede`) */
export function procheEtat(t: Lab): boolean {
  return ecartLab(t, ETAT_MENTHE) < PROCHE_ETAT || ecartLab(t, ETAT_TERRA) < PROCHE_ETAT;
}

/**
 * LA CESSION D'UNE ÎLE (chantier 59, la part de `dalleLisible` qui décide, hors Ingénu) : la teinte vers laquelle la dalle se décale (`decale`
 * du moteur) — au rang `rang` parmi les tons de la palette rangés par écart de teinte au fond, ni amande ni terracotta, poussée sur sa propre
 * direction jusqu'à `DE_VISE`. null : rien à céder (rang 0) ; `sansPalette` : aucun ton n'est permis.
 */
export function cessionIle(
  palette: readonly RGB[],
  fond: readonly number[],
  rang: number,
): { a: number; b: number; apres: number } | { sansPalette: true } | null {
  if (!rang) return null;
  const SO = lab(fond),
    CH: { a: number; b: number; d: number }[] = [];
  for (const c of palette) {
    if (!c) continue;
    const t = lab(c);
    if (procheEtat(t)) continue;
    CH.push({ a: t[1], b: t[2], d: Math.sqrt((t[1] - SO[1]) * (t[1] - SO[1]) + (t[2] - SO[2]) * (t[2] - SO[2])) });
  }
  if (!CH.length) return { sansPalette: true };
  CH.sort((x, y) => y.d - x.d);
  const ch = CH[(rang - 1) % CH.length]!;
  let ca = ch.a,
    cb = ch.b;
  const vx = ca - SO[1],
    vy = cb - SO[2];
  let vm = Math.sqrt(vx * vx + vy * vy) || 1;
  if (vm < DE_VISE) {
    ca = SO[1] + (vx / vm) * DE_VISE;
    cb = SO[2] + (vy / vm) * DE_VISE;
    vm = DE_VISE;
  }
  return { a: ca, b: cb, apres: vm };
}

/** le fond contre lequel se choisit la hauteur d'une île sous Ingénu (v203, C-275) : la couleur rendue autour d'elle, le fond de la sphère à défaut */
export function fondIleIngenu(ctx: ContexteCouleurs, etat: EtatCouleurs, hasard: Hasard): RGB {
  return couleurRendue(ctx, etat, hasard) ?? fondSphere(ctx, etat);
}

/**
 * LA HAUTEUR DE RAMPE D'UNE ÎLE SOUS INGÉNU (v18 · Q297, v203 — la part de `dalleLisible` qui décide) : dans l'ordre des hauteurs, la première
 * dont l'île (son Lab moyen, rendu par le moteur à cette hauteur : `labDe`) s'écarte du fond d'au moins la visée (32 en sombre, 48 en clair) ;
 * à défaut, celle qui s'en écarte le plus. null : aucune hauteur ne s'est rendue (la dalle reste telle quelle). `ecart` arrondi au dixième.
 */
export function hauteurIngenu(
  clair: boolean,
  fond: readonly number[],
  labDe: (h: number) => Lab | null,
): { h: number; ecart: number } | null {
  const SO = lab(fond),
    vise = clair ? DE_VISE_C : DE_VISE;
  let best: number | null = null,
    bd = -1;
  for (const h of clair ? HAUTEURS_INGENU_CLAIR : HAUTEURS_INGENU_SOMBRE) {
    const L = labDe(h);
    if (!L) continue;
    const de = ecartLab(L, SO);
    if (de > bd) {
      bd = de;
      best = h;
    }
    if (de >= vise) {
      bd = de;
      best = h;
      break;
    }
  }
  return best == null ? null : { h: best, ecart: Math.round(bd * 10) / 10 };
}
