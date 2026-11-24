/**
 * LE DESSIN (C-042, v132 ; le prototype : `lot-V132-DESSIN`) — construit dans l'app, et pour la page + d'abord (la fiche : lot 4).
 *
 * LA MISE EN PAGE : en mode dessin la surface prend toute la place, du haut de l'écran jusqu'à la rangée d'outils, posée EN BAS (centrée dans
 * sa zone basse, v133) ; tailles et couleurs se déploient 16 pt au-dessus d'elle et se replient dès le choix fait ; la page dessous n'est pas
 * touchée (le mode est une couche pleine) ; l'encart du haut ne garde que son contour ; un X le quitte sans poser (le dessin en cours gardé).
 *
 * LES DONNÉES — un dessin est une liste de TRAITS, jamais une image : {fond, traits, poses, pose, masque} ; chaque trait garde SA couleur ;
 * `traits` est le dessin en cours, `poses` ce que POSER a posé (la bande ne montre que lui) ; après le premier POSER le fond est fixé. Une photo
 * importée dans le dessin est un élément de la liste, à son rang (v139, C-086) : un doigt la déplace, deux doigts changent sa taille et la
 * tournent (C-098).
 *
 * SANS MA PAROLE ! (C-061, v133) : on dessine à l'encre du mode, sur le fond de la nature ; la zone des couleurs est un MUR (flou 4,8 px, rien
 * ne s'y choisit ; sa phrase : lot 8). L'app ne connaît pas encore Ma Parole ! : le mur est toujours là, comme dans Peaufiner.
 */
import './dessin.css';
import { palette } from '../../design/jetons.ts';
import { poserCroix } from '../commun.ts';
import { ICONES } from '../accueil/icones.ts';
import type { Horloge } from '../../animation/horloge.ts';
import { masqueFlaques, type ControlePassage } from '../../animation/flaques/passage.ts';

export type Nature = 'promi' | 'chiche' | 'nuee';

/** un trait (ses points : x, y, t, p — t l'instant, p la pression d'un stylet, −1 au doigt) ou une photo importée */
export type TraitDessin =
  | { c: string; t: number; g: 0 | 1; pts: number[] }
  | { img: string; x: number; y: number; w: number; h: number; a?: number };
export interface Dessin {
  v: 1;
  w: number;
  h: number;
  fond: string;
  traits: TraitDessin[];
  poses: TraitDessin[];
  pose: boolean;
  masque: boolean;
}

/** ce que le dessin habille : il le lit et l'écrit (la page + : son brouillon) */
export interface CibleDessin {
  lire(): Dessin | null;
  ecrire(d: Dessin | null): void;
  nature: Nature;
  /** la couleur du corps de l'écran d'où l'on vient (le fond du mode, sous la rangée) */
  corps: string;
  /** le mode s'est refermé (posé ou non) : l'écran se repeint */
  apres(pose: boolean): void;
}

/** LES PARAMÈTRES DE MISE EN PAGE (le prototype, `_dessinParams`, points) */
export const DESSIN = {
  RANGEE_H: 44,
  SECU_BAS: 34,
  MARGE_BAS: 12,
  MARGE_HAUT: 12,
  MARGE_COTE: 24,
  PAS_OUTIL: 46,
  POSER_L: 104,
  ECART_DEPLOI: 16,
  TAILLES: [2, 6, 22],
  POINT_PLUS: 3,
  CIBLE: 44,
  TAILLES_GOMME: [8, 18, 36],
  PHOTO_L: 0.6,
  PHOTO_MAX: 1024,
  BANDE_RETRAIT: 7,
} as const;

const NAT: Record<Nature, string> = { promi: palette.bleu45, chiche: palette.framboise54, nuee: palette.mauve77 };
const ENCRE = palette.brun09;
const CREME = palette.creme95;

const W = 390;
const surfH = (H: number): number => H - DESSIN.SECU_BAS - DESSIN.MARGE_BAS - DESSIN.RANGEE_H - DESSIN.MARGE_HAUT;

function rgb3(s: string): [number, number, number] {
  const m = s.match(/[\d.]+/g);
  if (m && m.length >= 3 && !s.includes('#')) return [+m[0], +m[1]!, +m[2]!];
  const h = s.replace('#', '');
  return [parseInt(h.slice(0, 2), 16) || 0, parseInt(h.slice(2, 4), 16) || 0, parseInt(h.slice(4, 6), 16) || 0];
}
const lumi = (c: string): number => {
  const [r, g, b] = rgb3(c);
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
const hex = (c: [number, number, number]): string =>
  '#' +
  c
    .map((v) =>
      Math.max(0, Math.min(255, Math.round(v)))
        .toString(16)
        .padStart(2, '0'),
    )
    .join('')
    .toUpperCase();
export const dessinPose = (d: Dessin | null): boolean => !!d && d.poses.length > 0;

// ── LE TRAIT « STYLET » : plein, opaque, contours nets ; effilé E2 (le début plus épais, la fin effilée sur le dernier quart) ; plus fin quand
//    le geste est rapide ; la pression d'un stylet module la largeur ; jamais sous 1 pt ──
type Pt = { x: number; y: number; t: number; p: number };
function cr(Q: Pt[], n: number): Pt[] {
  const o: Pt[] = [];
  const L = Q.length;
  for (let i = 0; i < L - 1; i++) {
    const a = Q[Math.max(0, i - 1)]!;
    const b = Q[i]!;
    const c = Q[i + 1]!;
    const d = Q[Math.min(L - 1, i + 2)]!;
    for (let k = 0; k < n; k++) {
      const u = k / n;
      const u2 = u * u;
      const u3 = u2 * u;
      o.push({
        x:
          0.5 *
          (2 * b.x +
            (-a.x + c.x) * u +
            (2 * a.x - 5 * b.x + 4 * c.x - d.x) * u2 +
            (-a.x + 3 * b.x - 3 * c.x + d.x) * u3),
        y:
          0.5 *
          (2 * b.y +
            (-a.y + c.y) * u +
            (2 * a.y - 5 * b.y + 4 * c.y - d.y) * u2 +
            (-a.y + 3 * b.y - 3 * c.y + d.y) * u3),
        t: b.t + (c.t - b.t) * u,
        p: b.p + (c.p - b.p) * u,
      });
    }
  }
  o.push(Q[L - 1]!);
  return o;
}
function largeurs(Q: Pt[], base: number, effile: boolean): number[] {
  const n = Q.length;
  const s = [0];
  for (let i = 1; i < n; i++) s.push(s[i - 1]! + Math.hypot(Q[i]!.x - Q[i - 1]!.x, Q[i]!.y - Q[i - 1]!.y));
  const L = s[n - 1] || 1;
  const w: number[] = [];
  const court = L < base * 3.2;
  const FIN = 0.25;
  const DEB = 0.2;
  const SUR = 0.38;
  for (let i = 0; i < n; i++) {
    const a = Math.max(0, i - 3);
    const b = Math.min(n - 1, i + 3);
    const dt = Math.max(1, Q[b]!.t - Q[a]!.t);
    const vit = (s[b]! - s[a]!) / dt;
    const u = s[i]! / L;
    let k = 1;
    if (effile && !court) {
      if (u < DEB) {
        const q = 1 - u / DEB;
        k *= 1 + SUR * q * q;
      }
      k *= Math.max(0.72, Math.min(1.06, 1.06 - 0.42 * vit));
      if (u > 1 - FIN) k *= Math.pow((1 - u) / FIN, 0.85);
    }
    k *= Q[i]!.p < 0 ? 1 : Math.min(1.35, 0.55 + 0.9 * Q[i]!.p);
    w.push(Math.max(1, base * k));
  }
  return w;
}
const points = (a: number[]): Pt[] => {
  const o: Pt[] = [];
  for (let i = 0; i + 3 < a.length; i += 4) o.push({ x: a[i]!, y: a[i + 1]!, t: a[i + 2]!, p: a[i + 3]! });
  return o;
};
const IMGS = new Map<string, HTMLImageElement>();
/** une image du dessin (une photo importée) ; `pret` est rappelé quand elle a fini de charger */
function imageDe(src: string, pret: () => void): HTMLImageElement | null {
  let o = IMGS.get(src);
  if (o) return o.complete && o.naturalWidth ? o : null;
  o = new Image();
  o.onload = pret;
  o.src = src;
  IMGS.set(src, o);
  return o.complete && o.naturalWidth ? o : null;
}
let recharge: () => void = () => undefined;
function traceUn(g: CanvasRenderingContext2D, tr: TraitDessin, enCours = false): void {
  if ('img' in tr) {
    const im = imageDe(tr.img, () => {
      recharge();
    });
    if (!im) return;
    g.save();
    g.globalAlpha = 1;
    g.globalCompositeOperation = 'source-over';
    if (tr.a) {
      g.translate(tr.x, tr.y);
      g.rotate(tr.a);
      g.drawImage(im, -tr.w / 2, -tr.h / 2, tr.w, tr.h);
    } else g.drawImage(im, tr.x - tr.w / 2, tr.y - tr.h / 2, tr.w, tr.h);
    g.restore();
    return;
  }
  const Q = points(tr.pts);
  if (!Q.length) return;
  g.save();
  g.globalAlpha = 1;
  g.globalCompositeOperation = tr.g ? 'destination-out' : 'source-over';
  g.fillStyle = tr.g ? ENCRE : tr.c;
  if (Q.length === 1) {
    g.beginPath();
    g.arc(Q[0]!.x, Q[0]!.y, Math.max(1, tr.t) / 2, 0, 6.2832);
    g.fill();
    g.restore();
    return;
  }
  const R = cr(Q, Q.length > 240 ? 3 : 6);
  const Wd = largeurs(R, tr.t, !tr.g && !enCours ? true : !tr.g);
  const n = R.length;
  const G: number[][] = [];
  const D: number[][] = [];
  for (let i = 0; i < n; i++) {
    const a = R[Math.max(0, i - 1)]!;
    const b = R[Math.min(n - 1, i + 1)]!;
    const dx = b.x - a.x;
    const dy = b.y - a.y;
    const m = Math.hypot(dx, dy) || 1;
    const nx = -dy / m;
    const ny = dx / m;
    const h = Wd[i]! / 2;
    G.push([R[i]!.x + nx * h, R[i]!.y + ny * h]);
    D.push([R[i]!.x - nx * h, R[i]!.y - ny * h]);
  }
  g.beginPath();
  g.moveTo(G[0]![0]!, G[0]![1]!);
  for (let i = 1; i < n; i++) g.lineTo(G[i]![0]!, G[i]![1]!);
  for (let i = n - 1; i >= 0; i--) g.lineTo(D[i]![0]!, D[i]![1]!);
  g.closePath();
  g.fill();
  // ni trou aux virages serrés, ni bout carré
  g.beginPath();
  for (let i = 0; i < n; i++) {
    g.moveTo(R[i]!.x + Wd[i]! / 2, R[i]!.y);
    g.arc(R[i]!.x, R[i]!.y, Wd[i]! / 2, 0, 6.2832);
  }
  g.fill();
  g.restore();
}
/** les traits seuls (sans le fond), dans un canevas à l'échelle k (px par point) */
function calque(traits: TraitDessin[], k: number, hPt: number): HTMLCanvasElement {
  const cv = document.createElement('canvas');
  cv.width = Math.max(1, Math.round(W * k));
  cv.height = Math.max(1, Math.round(hPt * k));
  const g = cv.getContext('2d')!;
  g.setTransform(k, 0, 0, k, 0, 0);
  for (const tr of traits) traceUn(g, tr);
  return cv;
}
/** le dessin POSÉ, entier, avec son fond (la bande, la vue entière, le partage) */
export function dessinEntier(d: Dessin, k: number): HTMLCanvasElement {
  const cv = document.createElement('canvas');
  cv.width = Math.round(W * k);
  cv.height = Math.round(d.h * k);
  const g = cv.getContext('2d')!;
  g.fillStyle = d.fond;
  g.fillRect(0, 0, cv.width, cv.height);
  g.drawImage(calque(d.poses, k, d.h), 0, 0);
  return cv;
}

const SVG = (corps: string): string =>
  `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${corps}</svg>`;
const ICO = {
  plume: SVG('<path d="M4 20l1-4L16.2 4.8a2.1 2.1 0 0 1 3 3L8 19l-4 1z"/><path d="M14 7l3 3"/>'),
  gomme: SVG(
    '<path d="M9 19h10"/><path d="M4.6 14.2l8.6-8.6a2 2 0 0 1 2.8 0l2.4 2.4a2 2 0 0 1 0 2.8L10.2 19H8.4l-3.8-3.4a1 1 0 0 1 0-1.4z"/><path d="M9.6 9.2l5.2 5.2"/>',
  ),
  annuler: SVG('<path d="M9 13L4.5 8.5 9 4"/><path d="M4.5 8.5H14a5.5 5.5 0 0 1 0 11h-3"/>'),
  photo: SVG(
    '<rect x="3.5" y="5" width="17" height="14" rx="2.5"/><path d="M3.5 15.5l4.8-4.6 4.2 4 2.8-2.6 5.2 4.9"/><circle cx="15.6" cy="9.4" r="1.3"/>',
  ),
};
const T = {
  dessiner: 'Dessiner',
  surface: 'La surface de dessin',
  outils: 'Les outils du dessin',
  quitter: 'Quitter le dessin',
  plume: 'Plume',
  gomme: 'Gomme',
  choisieTaille: ', choisie. Toucher de nouveau pour la taille',
  annuler: 'Annuler le dernier trait',
  couleur: 'Couleur',
  photo: 'Photo',
  photoChoisie:
    ', choisie : glisser une photo la déplace, pincer change sa taille. Toucher de nouveau pour en importer une autre',
  poser: 'Poser',
  poserLe: 'Poser le dessin',
  tailleDe: (o: string): string => `La taille de la ${o}`,
  tailles: ['Fin', 'Moyen', 'Gros'],
  couleursMur: 'Les couleurs du dessin, avec Ma Parole !',
  trait: 'Trait',
  fond: 'Fond',
  couleurTrait: 'La couleur du trait',
  couleurFond: 'La couleur du fond',
  teinte: (q: string, i: number, n: number): string => `${q}, teinte ${String(i)} sur ${String(n)}`,
  fermer: 'X',
};

export interface ModeDessin {
  ouvrir(c: CibleDessin): void;
  ouvert(): boolean;
  /** POSER (true) ou la sortie (false) : tout revient, sans fondu */
  sortir(poser: boolean): void;
  etat(): {
    outil: string;
    couleur: string;
    fond: string;
    deploi: string | null;
    traits: number;
    pose: boolean;
    corps: string;
  } | null;
}

export function creerModeDessin(o: {
  dv: HTMLElement;
  h: Horloge;
  clair: () => boolean;
  tons: () => string[];
}): ModeDessin {
  const { dv, h } = o;
  type Etat = {
    c: CibleDessin;
    d: Dessin;
    outil: 'plume' | 'gomme' | 'photo';
    taille: { plume: number; gomme: number };
    deploi: 'plume' | 'gomme' | 'couleur' | null;
    onglet: 'TRAIT' | 'FOND';
    trait: { c: string; t: number; g: 0 | 1; pts: number[]; id: number } | null;
    corps: string;
    encre: string;
    couleur: string;
    k: number;
    hS: number;
    cvV: HTMLCanvasElement;
    gV: CanvasRenderingContext2D;
    cvB: HTMLCanvasElement;
  };
  let M: Etat | null = null;
  const H = (): number => dv.offsetHeight || 844;
  const reduit = (): boolean => {
    try {
      return matchMedia('(prefers-reduced-motion: reduce)').matches;
    } catch {
      return false;
    }
  };
  /**
   * ⚑ 2b (Tom : « la règle de Tom prime, aucun changement sec ») — le mode paraît et part EN FLAQUES (C-329 : la scène du passage, posée en
   * MASQUE sur le mode lui-même, 300 ms) ; le prototype le pose d'un coup (écart nommé, test d'identité). Pendant qu'il part, il ne prend plus
   * le doigt. « Réduire les animations » : d'un coup.
   */
  let passage: ControlePassage | null = null;
  function enFlaques(sens: 'paraît' | 'part', fin?: () => void): void {
    passage?.stop?.();
    passage = null;
    if (reduit()) {
      fin?.();
      return;
    }
    const c = masqueFlaques(r, {
      mode: sens === 'paraît' ? 'ouvre' : 'couvre',
      duree: 300,
      fin: (x) => {
        if (passage === c) passage = null;
        if (!x.arrete) fin?.();
      },
    });
    if (!c.arrete) passage = c;
  }

  const r = document.createElement('div');
  r.id = 'dessinMode';
  // il couvre l'appareil au-dessus de la page + (base.css, `.couvert` : ce qui ne le déclare pas se cache)
  r.className = 'couvre';
  r.setAttribute('role', 'dialog');
  r.setAttribute('aria-modal', 'true');
  r.setAttribute('aria-label', T.dessiner);
  const s = document.createElement('div');
  s.className = 'dz-surface';
  s.setAttribute('role', 'img');
  s.setAttribute('aria-label', T.surface);
  const cvS = document.createElement('canvas');
  s.appendChild(cvS);
  const plateau = document.createElement('div');
  plateau.className = 'dz-plateau';
  plateau.setAttribute('aria-hidden', 'true');
  const rangee = document.createElement('div');
  rangee.className = 'dz-rangee';
  rangee.setAttribute('role', 'toolbar');
  rangee.setAttribute('aria-label', T.outils);
  // le X de C-173 (PromiLate, à la taille du X des écrans) : sortir sans poser, le dessin en cours gardé
  const quitter = document.createElement('button');
  quitter.type = 'button';
  quitter.className = 'dz-quitter';
  quitter.setAttribute('aria-label', T.quitter);
  const qg = document.createElement('span');
  qg.className = 'dz-x';
  qg.textContent = T.fermer;
  quitter.appendChild(qg);
  // sans titre (le plateau du dessin n'en a pas) : le X centré sur sa boîte, à la taille des titres (lot-V157-CROIX)
  poserCroix(quitter, qg, null);
  quitter.addEventListener('click', (ev) => {
    ev.stopPropagation();
    sortir(false);
  });
  const photoIn = document.createElement('input');
  photoIn.type = 'file';
  photoIn.accept = 'image/*';
  photoIn.multiple = true;
  photoIn.className = 'dz-photo-in';
  photoIn.setAttribute('aria-hidden', 'true');
  photoIn.tabIndex = -1;
  r.append(s, plateau, rangee, quitter, photoIn);
  dv.appendChild(r);
  // rien ne traverse le mode : un toucher sur lui n'atteint pas la page dessous
  for (const t of ['click', 'pointerdown', 'pointerup', 'touchstart', 'touchend', 'mousedown', 'mouseup'])
    r.addEventListener(t, (e) => {
      e.stopPropagation();
    });
  s.addEventListener(
    'touchstart',
    (e) => {
      e.preventDefault();
    },
    { passive: false },
  );
  s.addEventListener(
    'touchmove',
    (e) => {
      e.preventDefault();
    },
    { passive: false },
  );

  function fondPose(m: Etat): void {
    r.style.setProperty('--dz-fond', m.d.fond);
    r.style.setProperty('--dz-trait-fin', lumi(m.d.fond) > 128 ? ENCRE : CREME);
  }
  function repeint(): void {
    if (!M) return;
    const g = M.gV;
    g.setTransform(1, 0, 0, 1, 0, 0);
    g.globalCompositeOperation = 'source-over';
    g.clearRect(0, 0, M.cvV.width, M.cvV.height);
    g.drawImage(M.cvB, 0, 0);
    if (M.trait) {
      g.setTransform(M.k, 0, 0, M.k, 0, 0);
      traceUn(g, M.trait, true);
    }
  }
  function rebatit(): void {
    if (!M) return;
    M.cvB = calque(M.d.traits, M.k, M.hS);
    repeint();
  }
  recharge = () => {
    rebatit();
  };
  const garde = (): void => {
    if (M) M.c.ecrire(M.d);
  };

  /** la rangée A, en bas : PLUME · GOMME · ANNULER · COULEUR · PHOTO · POSER ; ce qui se déploie, juste au-dessus */
  function batir(): void {
    const m = M;
    if (!m) return;
    rangee.textContent = '';
    for (const e of r.querySelectorAll('.dz-deploi')) e.remove();
    const yR = H() - DESSIN.SECU_BAS - DESSIN.MARGE_BAS - DESSIN.RANGEE_H;
    rangee.style.top = `${String(yR)}px`;
    rangee.style.height = `${String(DESSIN.RANGEE_H)}px`;
    const b = (
      cls: string,
      x: number,
      w: number,
      html: string,
      label: string,
      fn: () => void,
      on: boolean | null,
      off = false,
    ): HTMLButtonElement => {
      const e = document.createElement('button');
      e.type = 'button';
      e.className = cls + (on ? ' on' : '');
      e.style.left = `${String(x)}px`;
      e.style.top = '0px';
      if (w) e.style.width = `${String(w)}px`;
      e.innerHTML = html;
      e.setAttribute('aria-label', label);
      if (on != null && cls === 'dz-o') e.setAttribute('aria-pressed', on ? 'true' : 'false');
      if (off) {
        e.disabled = true;
        e.setAttribute('aria-disabled', 'true');
      }
      e.addEventListener('click', (ev) => {
        ev.stopPropagation();
        if (!e.disabled) fn();
      });
      rangee.appendChild(e);
      return e;
    };
    const x0 = DESSIN.MARGE_COTE;
    const pas = DESSIN.PAS_OUTIL;
    b(
      'dz-o',
      x0,
      0,
      ICO.plume,
      T.plume + (m.outil === 'plume' ? T.choisieTaille : ''),
      () => {
        outil('plume');
      },
      m.outil === 'plume',
    ).dataset['outil'] = 'plume';
    b(
      'dz-o',
      x0 + pas,
      0,
      ICO.gomme,
      T.gomme + (m.outil === 'gomme' ? T.choisieTaille : ''),
      () => {
        outil('gomme');
      },
      m.outil === 'gomme',
    ).dataset['outil'] = 'gomme';
    b('dz-o', x0 + 2 * pas, 0, ICO.annuler, T.annuler, annuler, null, !m.d.traits.length).dataset['outil'] = 'annuler';
    b(
      'dz-o',
      x0 + 3 * pas,
      0,
      ICONES.studio,
      T.couleur,
      () => {
        deploie(m.deploi === 'couleur' ? null : 'couleur');
      },
      m.deploi === 'couleur',
    ).dataset['outil'] = 'couleur';
    b(
      'dz-o',
      x0 + 4 * pas,
      0,
      ICO.photo,
      T.photo + (m.outil === 'photo' ? T.photoChoisie : ''),
      outilPhoto,
      m.outil === 'photo',
    ).dataset['outil'] = 'photo';
    b(
      'dz-poser',
      W - DESSIN.MARGE_COTE - DESSIN.POSER_L,
      DESSIN.POSER_L,
      T.poser,
      T.poserLe,
      () => {
        sortir(true);
      },
      null,
    ).dataset['outil'] = 'poser';
    const yD = yR - DESSIN.ECART_DEPLOI;
    if (m.deploi === 'plume' || m.deploi === 'gomme') {
      // v140 (C-086) : trois points, chacun une cible de 44 pt ; le point fait le diamètre du trait + 3 pt (au plus 40)
      const ou = m.deploi;
      const p = document.createElement('div');
      p.className = 'dz-deploi dz-tailles';
      p.setAttribute('role', 'group');
      p.setAttribute('aria-label', T.tailleDe(ou));
      const hc = DESSIN.CIBLE + 8;
      p.style.left = `${String(
        Math.max(
          DESSIN.MARGE_COTE - 8,
          Math.min(W - DESSIN.MARGE_COTE + 8 - (8 + 3 * DESSIN.CIBLE + 2 * 4 + 8), x0 + (ou === 'gomme' ? pas : 0)),
        ),
      )}px`;
      p.style.top = `${String(yD - hc)}px`;
      p.style.height = `${String(hc)}px`;
      p.style.borderRadius = `${String(hc / 2)}px`;
      let xt = 8;
      (ou === 'gomme' ? DESSIN.TAILLES_GOMME : DESSIN.TAILLES).forEach((d0, i) => {
        const dd = Math.min(40, d0 + DESSIN.POINT_PLUS);
        const e = document.createElement('button');
        e.type = 'button';
        e.className = m.taille[ou] === i ? 'on' : '';
        const bw = DESSIN.CIBLE;
        e.style.left = `${String(xt)}px`;
        e.style.width = `${String(bw)}px`;
        e.style.height = `${String(bw)}px`;
        e.style.top = `${String((hc - bw) / 2)}px`;
        e.style.borderRadius = `${String(bw / 2)}px`;
        xt += bw + (i < 2 ? 4 : 8);
        p.style.width = `${String(xt)}px`;
        const pt = document.createElement('i');
        pt.style.width = `${String(dd)}px`;
        pt.style.height = `${String(dd)}px`;
        e.appendChild(pt);
        e.setAttribute('aria-label', T.tailles[i]!);
        e.setAttribute('aria-pressed', m.taille[ou] === i ? 'true' : 'false');
        e.dataset['taille'] = String(i);
        e.addEventListener('click', (ev) => {
          ev.stopPropagation();
          m.taille[ou] = i;
          deploie(null);
        });
        p.appendChild(e);
      });
      r.appendChild(p);
    }
    if (m.deploi === 'couleur') {
      // v133 (C-061) : sans Ma Parole !, un MUR — rien ne s'y choisit, les teintes de la palette floutées (sa phrase : lot 8)
      const q = document.createElement('div');
      q.className = 'dz-deploi dz-couleurs dz-mur';
      q.setAttribute('role', 'group');
      q.setAttribute('aria-label', T.couleursMur);
      q.style.top = `${String(yD - 114)}px`;
      const avecFond = !m.d.pose;
      (['TRAIT', 'FOND'] as const).forEach((t, i) => {
        if (t === 'FOND' && !avecFond) return;
        const e = document.createElement('button');
        e.type = 'button';
        e.className = 'dz-onglet' + (avecFond ? '' : ' seul');
        e.style.left = `${String(6 + i * 165)}px`;
        e.textContent = t === 'TRAIT' ? T.trait : T.fond;
        e.setAttribute('role', 'tab');
        e.setAttribute('aria-selected', m.onglet === t ? 'true' : 'false');
        e.setAttribute('aria-label', t === 'TRAIT' ? T.couleurTrait : T.couleurFond);
        e.dataset['onglet'] = t;
        q.appendChild(e);
      });
      const tons = o.tons();
      const pasT = Math.min(64, (342 - 32 - 44) / Math.max(1, tons.length - 1));
      tons.forEach((t, i) => {
        const e = document.createElement('button');
        e.type = 'button';
        const gris = t === m.d.fond;
        e.className = 'dz-ton' + (m.couleur === t ? ' on' : '');
        e.style.left = `${String(14 + i * pasT)}px`;
        e.style.setProperty('--dz-ton', t);
        e.dataset['ton'] = t;
        e.setAttribute('aria-label', T.teinte(T.trait, i + 1, tons.length));
        e.setAttribute('aria-pressed', m.couleur === t ? 'true' : 'false');
        if (gris) {
          e.disabled = true;
          e.setAttribute('aria-disabled', 'true');
        }
        q.appendChild(e);
      });
      r.appendChild(q);
    }
  }
  function deploie(q: Etat['deploi']): void {
    if (!M) return;
    M.deploi = q;
    batir();
  }
  function outil(ou: 'plume' | 'gomme'): void {
    if (!M) return;
    if (M.outil === ou) {
      deploie(M.deploi === ou ? null : ou);
      return;
    }
    M.outil = ou;
    deploie(null);
  }
  const photos = (m: Etat): Array<Extract<TraitDessin, { img: string }>> =>
    m.d.traits.filter((t): t is Extract<TraitDessin, { img: string }> => 'img' in t);
  function outilPhoto(): void {
    if (!M) return;
    if (M.outil === 'photo' || !photos(M).length) {
      M.outil = 'photo';
      deploie(null);
      // le sélecteur de fichiers s'ouvre DANS le geste (le clic du doigt)
      photoIn.click();
      return;
    }
    M.outil = 'photo';
    deploie(null);
  }
  photoIn.addEventListener('change', () => {
    const F = [...(photoIn.files ?? [])];
    photoIn.value = '';
    F.forEach((fi, i) => {
      const rd = new FileReader();
      rd.onload = () => {
        if (typeof rd.result === 'string') ajoutePhoto(rd.result, i);
      };
      rd.readAsDataURL(fi);
    });
  });
  function ajoutePhoto(src: string, rang: number): void {
    const im = new Image();
    im.onload = () => {
      const m = M;
      if (!m) return;
      const mx = Math.max(im.naturalWidth, im.naturalHeight);
      let s2 = src;
      if (mx > DESSIN.PHOTO_MAX) {
        const kq = DESSIN.PHOTO_MAX / mx;
        const c = document.createElement('canvas');
        c.width = Math.round(im.naturalWidth * kq);
        c.height = Math.round(im.naturalHeight * kq);
        c.getContext('2d')!.drawImage(im, 0, 0, c.width, c.height);
        s2 = c.toDataURL('image/jpeg', 0.86);
      }
      let w = W * DESSIN.PHOTO_L;
      let hh = (w * im.naturalHeight) / im.naturalWidth;
      if (hh > m.hS * 0.7) {
        hh = m.hS * 0.7;
        w = (hh * im.naturalWidth) / im.naturalHeight;
      }
      m.d.traits.push({
        img: s2,
        x: W / 2 + rang * 14,
        y: m.hS / 2 + rang * 14,
        w: Math.round(w * 10) / 10,
        h: Math.round(hh * 10) / 10,
      });
      m.outil = 'photo';
      garde();
      imageDe(s2, () => {
        rebatit();
      });
      rebatit();
      batir();
    };
    im.src = src;
  }
  function annuler(): void {
    if (!M || !M.d.traits.length) return;
    M.d.traits.pop();
    garde();
    rebatit();
    deploie(null);
  }

  // ── le geste ──
  const pt = (e: PointerEvent): Pt => {
    const m = M!;
    const q = m.cvV.getBoundingClientRect();
    return {
      x: Math.round(((e.clientX - q.left) / q.width) * W * 10) / 10,
      y: Math.round(((e.clientY - q.top) / q.height) * m.hS * 10) / 10,
      t: Math.round(e.timeStamp || h.maintenant()),
      p: e.pointerType === 'pen' && e.pressure > 0 ? Math.round(e.pressure * 100) / 100 : -1,
    };
  };
  const ajoute = (q: Pt): void => {
    const a = M!.trait!.pts;
    const n = a.length;
    if (n >= 4 && Math.abs(a[n - 4]! - q.x) < 0.3 && Math.abs(a[n - 3]! - q.y) < 0.3) return;
    a.push(q.x, q.y, q.t, q.p);
  };
  let img: number | null = null;
  const peintBientot = (): void => {
    if (img != null) return;
    img = h.image(() => {
      img = null;
      repeint();
    });
  };
  // la photo en main : un doigt la déplace, deux doigts changent sa taille et la tournent (le point sous leur milieu y reste)
  type Main = {
    t: Extract<TraitDessin, { img: string }>;
    ptrs: Map<number, { x: number; y: number }>;
    x0: number;
    y0: number;
    w0: number;
    h0: number;
    a0: number;
    m0: { x: number; y: number; d: number; g: number };
  };
  let PH: Main | null = null;
  const sous = (q: Pt): Extract<TraitDessin, { img: string }> | null => {
    const L = M!.d.traits;
    for (let i = L.length - 1; i >= 0; i--) {
      const t = L[i]!;
      if ('img' in t && Math.abs(q.x - t.x) <= t.w / 2 && Math.abs(q.y - t.y) <= t.h / 2) return t;
    }
    return null;
  };
  const phCale = (P: Main): void => {
    const L = [...P.ptrs.values()];
    const a = L[0]!;
    const b = L[1];
    P.x0 = P.t.x;
    P.y0 = P.t.y;
    P.w0 = P.t.w;
    P.h0 = P.t.h;
    P.a0 = P.t.a ?? 0;
    P.m0 = b
      ? {
          x: (a.x + b.x) / 2,
          y: (a.y + b.y) / 2,
          d: Math.hypot(a.x - b.x, a.y - b.y) || 1,
          g: Math.atan2(b.y - a.y, b.x - a.x),
        }
      : { x: a.x, y: a.y, d: 0, g: 0 };
  };
  s.addEventListener('pointerdown', (e) => {
    const m = M;
    if (!m) return;
    if (m.outil === 'photo') {
      e.preventDefault();
      if (m.deploi) deploie(null);
      const q = pt(e);
      if (!PH) {
        const t = sous(q);
        if (!t) return;
        PH = { t, ptrs: new Map(), x0: 0, y0: 0, w0: 0, h0: 0, a0: 0, m0: { x: 0, y: 0, d: 0, g: 0 } };
      }
      PH.ptrs.set(e.pointerId, { x: q.x, y: q.y });
      phCale(PH);
      try {
        s.setPointerCapture(e.pointerId);
      } catch {
        /* rien */
      }
      return;
    }
    if (m.trait || e.button > 0) return;
    e.preventDefault();
    if (m.deploi) deploie(null);
    try {
      s.setPointerCapture(e.pointerId);
    } catch {
      /* rien */
    }
    const gomme = m.outil === 'gomme';
    m.trait = {
      c: gomme ? '' : m.couleur,
      t: (gomme ? DESSIN.TAILLES_GOMME : DESSIN.TAILLES)[m.taille[gomme ? 'gomme' : 'plume']]!,
      g: gomme ? 1 : 0,
      pts: [],
      id: e.pointerId,
    };
    ajoute(pt(e));
    peintBientot();
  });
  s.addEventListener('pointermove', (e) => {
    if (PH) {
      e.preventDefault();
      if (!PH.ptrs.has(e.pointerId)) return;
      const q = pt(e);
      PH.ptrs.set(e.pointerId, { x: q.x, y: q.y });
      const L = [...PH.ptrs.values()];
      const a = L[0]!;
      const b = L[1];
      const t = PH.t;
      if (b && PH.m0.d) {
        const mm = { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2, d: Math.hypot(a.x - b.x, a.y - b.y) || 1 };
        const w = Math.max(24, Math.min(W * 4, PH.w0 * (mm.d / PH.m0.d)));
        const f = w / PH.w0;
        let da = Math.atan2(b.y - a.y, b.x - a.x) - PH.m0.g;
        while (da > Math.PI) da -= 2 * Math.PI;
        while (da < -Math.PI) da += 2 * Math.PI;
        const co = Math.cos(da);
        const si = Math.sin(da);
        const vx = (PH.x0 - PH.m0.x) * f;
        const vy = (PH.y0 - PH.m0.y) * f;
        t.w = w;
        t.h = PH.h0 * f;
        t.a = PH.a0 + da;
        t.x = mm.x + vx * co - vy * si;
        t.y = mm.y + vx * si + vy * co;
      } else {
        t.x = PH.x0 + (a.x - PH.m0.x);
        t.y = PH.y0 + (a.y - PH.m0.y);
      }
      if (img == null)
        img = h.image(() => {
          img = null;
          rebatit();
        });
      return;
    }
    const m = M;
    if (!m?.trait || e.pointerId !== m.trait.id) return;
    e.preventDefault();
    const L = e.getCoalescedEvents?.() ?? [];
    for (const x of L.length ? L : [e]) ajoute(pt(x));
    peintBientot();
  });
  const fin = (e: PointerEvent): void => {
    if (PH) {
      e.preventDefault();
      if (!PH.ptrs.has(e.pointerId)) return;
      PH.ptrs.delete(e.pointerId);
      if (PH.ptrs.size) {
        phCale(PH);
        return;
      }
      const t = PH.t;
      PH = null;
      t.x = Math.round(t.x * 10) / 10;
      t.y = Math.round(t.y * 10) / 10;
      t.w = Math.round(t.w * 10) / 10;
      t.h = Math.round(t.h * 10) / 10;
      if (t.a) t.a = Math.round(t.a * 1000) / 1000;
      garde();
      rebatit();
      return;
    }
    const m = M;
    if (!m?.trait || e.pointerId !== m.trait.id) return;
    e.preventDefault();
    const tr = m.trait;
    m.trait = null;
    if (tr.pts.length >= 4) {
      const neuf: TraitDessin = { c: tr.c, t: tr.t, g: tr.g, pts: tr.pts };
      m.d.traits.push(neuf);
      const g = m.cvB.getContext('2d')!;
      g.setTransform(m.k, 0, 0, m.k, 0, 0);
      traceUn(g, neuf);
      garde();
    }
    repeint();
    batir();
  };
  s.addEventListener('pointerup', fin);
  s.addEventListener('pointercancel', fin);
  document.addEventListener(
    'keydown',
    (e) => {
      if (M && e.key === 'Escape') {
        sortir(false);
        e.preventDefault();
      }
    },
    true,
  );

  function ouvrir(c: CibleDessin): void {
    const hS0 = surfH(H());
    let d = c.lire();
    if (!d) d = { v: 1, w: W, h: hS0, fond: NAT[c.nature], traits: [], poses: [], pose: false, masque: false };
    else d = { ...d, traits: d.traits.slice(), poses: d.poses.slice() };
    if (d.h > hS0) d.h = hS0;
    const corps = c.corps;
    const enc = lumi(corps) > 128 ? ENCRE : CREME;
    const k = Math.max(2, Math.min(3, window.devicePixelRatio || 2));
    cvS.width = Math.round(W * k);
    cvS.height = Math.round(d.h * k);
    // sans Ma Parole ! (C-061), on dessine à l'encre du MODE ; jamais de la couleur du fond
    const encM = o.clair() ? ENCRE : CREME;
    M = {
      c,
      d,
      outil: 'plume',
      taille: { plume: 1, gomme: 1 },
      deploi: null,
      onglet: 'TRAIT',
      trait: null,
      corps,
      encre: enc,
      couleur: encM !== d.fond ? encM : enc,
      k,
      hS: d.h,
      cvV: cvS,
      gV: cvS.getContext('2d')!,
      cvB: calque(d.traits, k, d.h),
    };
    r.style.setProperty('--dz-corps', corps);
    r.style.setProperty('--dz-encre', enc);
    s.style.height = `${String(d.h)}px`;
    fondPose(M);
    repeint();
    batir();
    r.classList.remove('part');
    r.classList.add('ouv');
    enFlaques('paraît');
  }
  function sortir(poser: boolean): void {
    const m = M;
    if (!m) return;
    const d = m.d;
    m.trait = null;
    PH = null;
    if (poser) {
      if (d.traits.length) {
        d.poses = JSON.parse(JSON.stringify(d.traits)) as TraitDessin[];
        d.pose = true;
        d.masque = false;
        m.c.ecrire(d);
      } else m.c.ecrire(null);
    } else m.c.ecrire(d.traits.length || dessinPose(d) ? d : null);
    M = null;
    // la page dessous se repeint tout de suite (la bande montre le dessin posé) ; le mode part en flaques par-dessus
    m.c.apres(poser && d.traits.length > 0);
    r.classList.add('part');
    enFlaques('part', () => {
      r.classList.remove('ouv', 'part');
      for (const e of r.querySelectorAll('.dz-deploi')) e.remove();
      rangee.textContent = '';
    });
  }
  return {
    ouvrir,
    ouvert: () => !!M,
    sortir,
    etat: () =>
      M
        ? {
            outil: M.outil,
            couleur: M.couleur,
            fond: M.d.fond,
            deploi: M.deploi,
            traits: M.d.traits.length,
            pose: M.d.pose,
            corps: M.corps,
          }
        : null,
  };
}

/** la couleur calculée d'un élément, en hexadécimal (le corps d'où l'on vient) */
export function couleurDe(e: Element): string {
  return hex(rgb3(getComputedStyle(e).backgroundColor));
}
