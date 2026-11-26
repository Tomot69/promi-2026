/**
 * LA FICHE D'UN CERCLE (lot 5, SPEC-ECRANS §7) — ce qui est propre au Cercle, posé par la fiche (fiche.ts, son mode Cercle : le même écran que la
 * fiche d'une parole, comme le prototype — `#detailPoster.dp-mode-nuee`) : la bande (ses dalles, ou ses graines), le fil de ses paroles et les
 * Noyaux (« Toi », puis le Cercle). Les cotes et les couleurs sont celles du prototype (`_ficheNuee` de lot-S1B-geo et les blocs qui le corrigent :
 * v179b C-231 pour la bande, v36 pour le liseré du fil), relevées le 26 nov. 2026 (WebKit, ×3) et comparées au pixel par tests/rendu/cercle.spec.ts.
 */
import type { Facade } from '../../moteur/facade.ts';
import type { Parole } from '../../donnees/schema.ts';
import { palette } from '../../design/jetons.ts';
import { cheminOnde, onde } from '../page-plus/onde.ts';
import { NATTRAIT } from '../page-plus/trait.ts';
import { avecAlpha, el, esc } from '../commun.ts';
import { motDuFil } from '../../metier/cercle.ts';
import type { Noyau } from './noyaux.ts';

const W = 390;
/** les tons des graines d'un Cercle vide (§10.6, `GLIGHT`) : sur le champ lilas, dans les deux thèmes */
const GRAINES = [
  palette.graineCercle1,
  palette.graineCercle2,
  palette.graineCercle3,
  palette.graineCercle4,
  palette.graineCercle5,
];

/** le plus bas de l'onde (`fondChamp`) */
function fondChamp(y: (x: number) => number): number {
  let m = 0;
  for (let x = 0; x <= W; x += 2) m = Math.max(m, y(x));
  return m;
}

/**
 * LA BANDE — l'aplat lilas au-dessus de la vague, puis : un Cercle qui porte des paroles, LA GRILLE de « Ce que tu as tenu » (C-231) — chaque
 * dalle rendue à la taille de sa boîte dans le monde de sa plantation, posée 1:1, entière ; des boîtes égales (rapport 1,3), de la marge de gauche,
 * 12 pt entre deux (resserré jusqu'à 3 si les boîtes tomberaient sous 14), chaque colonne centrée entre le plateau (ou le bouton photo) et la vague ;
 * un Cercle vide, LES GRAINES (§10.6) — les dalles de la Toile, la forme du moteur au ton crème, semées à la densité de douze sur le champ vide.
 * Rend ce que la bande DÉCLARE (`data-matiere` : le champ entier, Q74).
 */
export function peindreBande(
  facade: Facade,
  g: CanvasRenderingContext2D,
  o: {
    liste: readonly Parole[];
    toutes: readonly Parole[];
    base: number;
    amp: number;
    /** le bouton photo (la boîte, en pt de la fiche) : la grille ne passe jamais sous lui */
    photo: { x: number; bas: number } | null;
  },
): string {
  const { liste, base, amp } = o;
  const y = onde(base, amp);
  g.beginPath();
  cheminOnde(g, y, 0, W, W);
  g.lineTo(W, 0);
  g.lineTo(0, 0);
  g.closePath();
  g.fillStyle = palette.mauve77;
  g.fill();
  const H2 = fondChamp(y);
  const sx = Math.hypot(g.getTransform().a, g.getTransform().b) || 1;
  g.save();
  g.beginPath();
  cheminOnde(g, y, 0, W, W);
  g.lineTo(W, 0);
  g.lineTo(0, 0);
  g.closePath();
  g.clip();
  if (liste.length) grille(facade, g, liste, base, o.photo, sx);
  else graines(facade, g, o.toutes, H2, sx);
  g.restore();
  return ['0', '0', String(W), String(H2)].join(',');
}

function grille(
  facade: Facade,
  g: CanvasRenderingContext2D,
  liste: readonly Parole[],
  base: number,
  photo: { x: number; bas: number } | null,
  sx: number,
): void {
  const yL = onde(base, 40);
  const n = liste.length;
  const A = 1.3;
  const yT = 112;
  const xL = 24;
  let BX = 326;
  let BY = 134;
  if (photo) {
    BX = Math.min(BX, photo.x - 6);
    BY = Math.max(BY, photo.bas + 6);
  }
  const bas = (x0: number, x1: number): number => {
    let m = 1e9;
    for (let x = x0; x <= x1 + 2.9; x += 3) m = Math.min(m, yL(Math.min(x, x1)));
    return m - 10;
  };
  const haut = (x1: number): number => (x1 > BX ? Math.max(yT, BY) : yT);
  type Essai = { h: number; r: number; c: number; G: number };
  const essai = (Wd: number, r: number, G: number): Essai | null => {
    const c = Math.ceil(n / r);
    let h = Math.min(120, (Wd - (c - 1) * G) / c / A);
    for (let it = 0; it < 3; it++) {
      const bw = h * A;
      let hm = 1e9;
      for (let j = 0; j < c; j++) {
        const x0 = xL + j * (bw + G);
        const x1 = x0 + bw;
        hm = Math.min(hm, (bas(x0, x1) - haut(x1) - (r - 1) * G) / r);
      }
      h = Math.min(h, hm);
    }
    return h >= 6 ? { h, r, c, G } : null;
  };
  let best: Essai | null = null;
  for (const G of [12, 8, 5, 3]) {
    if (best && best.h >= 14) break;
    let b2: Essai | null = null;
    for (let Wd = W - 48; Wd >= 40; Wd -= 4)
      for (let r = 1; r <= Math.min(3, n); r++) {
        const s = essai(Wd, r, G);
        if (s && (!b2 || s.h > b2.h + 0.25)) b2 = s;
      }
    if (b2 && (!best || b2.h > best.h + 0.25)) best = b2;
  }
  if (!best) return;
  const bh = best.h;
  const bw = bh * A;
  const G = best.G;
  const gh = best.r * bh + (best.r - 1) * G;
  liste.forEach((p, i) => {
    const rr = Math.floor(i / best.c);
    const cc = i % best.c;
    const bx = xL + cc * (bw + G);
    const t0 = haut(bx + bw);
    const by = t0 + Math.max(0, (bas(bx, bx + bw) - t0 - gh) / 2) + rr * (bh + G);
    const r = facade.rendreDalle(p.id, bw * sx, bh * sx, p.monde ? { monde: p.monde } : undefined);
    if (r) facade.poserUn(g, r.cv, bx + bw / 2, by + bh / 2);
  });
}

function graines(facade: Facade, g: CanvasRenderingContext2D, toutes: readonly Parole[], H2: number, sx: number): void {
  const semence = toutes.filter((q) => !q.draft).slice(0, 5);
  if (!semence.length) return;
  const SP0 = Math.sqrt((390 * 435) / 12);
  const nD = Math.max(1, Math.round((W * H2) / (SP0 * SP0)));
  const sp = Math.sqrt((W * H2) / nD);
  const cols = Math.max(1, Math.round(W / sp));
  const rows = Math.max(1, Math.round(H2 / sp));
  const cw = W / cols;
  const ch = H2 / rows;
  const oeil = facade.mondeCourant().m === 'madrure';
  const f = oeil ? 0.58 : 1.15;
  const cache = new Map<string, HTMLCanvasElement | null>();
  let kc = 0;
  for (let r = 0; r < rows; r++)
    for (let c = 0; c < cols; c++) {
      const p = semence[kc % semence.length]!;
      const ton = GRAINES[kc % GRAINES.length]!;
      kc++;
      const bw = cw * f;
      const bh = ch * f;
      const cle = `${String(p.id)}|${ton}|${String(Math.round(bw * sx))}x${String(Math.round(bh * sx))}`;
      let src = cache.get(cle);
      if (src === undefined) {
        const rd = facade.rendreDalle(p.id, bw * sx, bh * sx);
        src = null;
        if (rd) {
          // la graine : la FORME du moteur, le TON du §10.6 — une copie 1:1, teintée (`source-in` garde l'alpha de la dalle)
          const cp = document.createElement('canvas');
          cp.width = rd.cv.width;
          cp.height = rd.cv.height;
          const gx = cp.getContext('2d')!;
          gx.drawImage(rd.cv, 0, 0);
          gx.globalCompositeOperation = 'source-in';
          gx.fillStyle = ton;
          gx.fillRect(0, 0, cp.width, cp.height);
          src = cp;
        }
        cache.set(cle, src);
      }
      if (!src) continue;
      // le décalage vient de l'id et de la case — jamais d'un hasard
      const j = ((p.id * 2654435761) >>> 0) ^ (((r * 73856093) ^ (c * 19349663)) >>> 0);
      const dx = ((j & 255) / 255 - 0.5) * cw * 0.34;
      const dy = (((j >> 8) & 255) / 255 - 0.5) * ch * 0.34;
      const bx = c * cw + (cw - bw) / 2 + dx;
      const by = r * ch + (ch - bh) / 2 + dy;
      facade.poserUn(g, src, bx + bw / 2, by + bh / 2);
    }
}

/** les Noyaux d'un Cercle : « Toi » (toutes tes paroles), puis le Cercle (ses paroles) — son nom entier (C-128) */
export function noyauxCercle(cle: string, nom: string, liste: readonly Parole[], toutes: readonly Parole[]): Noyau[] {
  const tous = toutes.filter((q) => !q.draft);
  const cpt = (L: readonly Parole[], s: string): number => L.filter((q) => q.status === s).length;
  return [
    { nom: 'Toi', moi: true, tenues: cpt(tous, 'tenu'), enCours: cpt(tous, 'encours') },
    { nom, moi: false, cercle: cle, tenues: cpt(liste, 'tenu'), enCours: cpt(liste, 'encours') },
  ];
}

/**
 * LE TRAIT D'UNE LIGNE DU FIL (§5, cadre 58) : un seul SVG de 103 × 74, l'onde (base 86, période 1, amplitude 8,6) borne le champ lilas à droite et
 * porte la ligne d'état — le plein de 0 à 37 (la moitié), puis des points r 2,6 tous les 10 ; une parole tenue, le trait entier au vert « tenu ».
 * Un liseré crème adouci (0,55, le filet doux) de 0,8 à droite du tracé (v36 : la fiche est toujours sombre, C-132).
 */
function traitDuFil(tenu: boolean): string {
  const H = 74;
  const LX = 103;
  const BASE = 86;
  const AMP = 8.6;
  const EP = 5;
  const R = 2.6;
  const N = 24;
  const mont = AMP * 0.34;
  const aa = AMP * 0.62;
  const xx = (u: number): number => BASE - mont * u - aa * Math.sin(2 * Math.PI * u);
  const pas = (fin: number, dx = 0): string => {
    let d = 'M' + (xx(0) + dx).toFixed(1) + ' 0';
    for (let j = 1; j <= fin; j++) d += 'L' + (xx(j / N) + dx).toFixed(1) + ' ' + ((H * j) / N).toFixed(1);
    return d;
  };
  const col = tenu ? palette.menthe11 : NATTRAIT.nuee;
  const fin = tenu ? N : Math.round(N * 0.5);
  let pts = '';
  if (!tenu)
    for (let yv = 47; yv < H - R; yv += 10)
      pts +=
        '<circle cx="' + xx(yv / H).toFixed(1) + '" cy="' + String(yv) + '" r="' + String(R) + '" fill="' + col + '"/>';
  return (
    '<div class="s1b-fil-trait"><svg width="' +
    String(LX) +
    '" height="' +
    String(H) +
    '" fill="none"><path d="' +
    pas(N) +
    'L0 ' +
    String(H) +
    'L0 0Z" fill="' +
    palette.mauve77 +
    '"/><path d="' +
    pas(fin) +
    '" stroke="' +
    col +
    '" stroke-width="' +
    String(EP) +
    '" stroke-linecap="round"/><path d="' +
    pas(fin, EP / 2 + 0.4) +
    '" stroke="' +
    avecAlpha(palette.creme95, 0.55) +
    '" stroke-width="0.8" stroke-linecap="butt"/>' +
    pts +
    '</svg></div>'
  );
}

/**
 * LE FIL, l'arbre du prototype (`#dpNueeFil` › `.nf-tete` puis `.nf-liste`) : la liste — une ligne par parole (342 × 79, 12 pt entre deux), sa
 * mini-dalle (70 × 56), son mot (`motDuFil`) et son titre, puis les mots du Cercle (posés par la fiche), 48 pt de pied ; la tête (« Un mot… »,
 * « Planter dans le Cercle ») passe après elle et se COLLE au bas (`sticky`, 96 pt du bas de l'écran : le bandeau et 12 pt) — le fil défile
 * dessous. La première ligne 31 pt sous la ligne d'état. Rend la liste (null : un Cercle vide n'en a pas).
 */
export function batirFil(
  facade: Facade,
  fil: HTMLElement,
  tete: HTMLElement,
  liste: readonly Parole[],
  haut: number,
): HTMLElement | null {
  fil.style.top = `${String(haut)}px`;
  const L = el('div', { class: 'nf-liste' });
  fil.replaceChildren(tete, ...(liste.length ? [L] : []));
  L.innerHTML = liste
    .map(
      (p) =>
        '<div class="nf-item' +
        (p.status === 'tenu' ? ' nf-menthe' : ' nf-cours') +
        '" data-id="' +
        String(p.id) +
        '" role="button">' +
        traitDuFil(p.status === 'tenu') +
        '<div class="nf-tx"><em>' +
        esc(motDuFil(p)) +
        '</em><b>' +
        esc(p.title) +
        '</b></div><span class="nf-dw"><canvas class="nf-d"></canvas></span></div>',
    )
    .join('');
  const dpr = Math.max(2, Math.min(3, window.devicePixelRatio || 2));
  const cvs = L.querySelectorAll<HTMLCanvasElement>('.nf-d');
  liste.forEach((p, i) => {
    const cv = cvs[i]!;
    cv.width = Math.round(70 * dpr);
    cv.height = Math.round(56 * dpr);
    const g = cv.getContext('2d');
    if (!g) return;
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    const r = facade.poserDalle(g, p.id, 0, 0, 70, 56, {}, true);
    cv.setAttribute('data-matiere', r ? [r.x, r.y, r.w, r.h].map((v) => Math.round(v)).join(',') : '');
  });
  return liste.length ? L : null;
}

/** la tête collée au bas du fil : « Un mot… » (s'il y a des paroles) puis « Planter dans le Cercle » (`#nfAdd`), son bas à 748 */
export function batirTete(): { tete: HTMLElement; cale: HTMLElement; planter: HTMLElement } {
  const tete = el('div', { class: 'nf-tete' });
  const cale = el('div', { id: 'cmCale' });
  const planter = el('button', { type: 'button', id: 'nfAdd', class: 'nf-add' });
  planter.innerHTML =
    '<span class="nf-plus"><svg viewBox="0 0 32 32" width="22" height="22" aria-hidden="true"><path d="M16 6 V26 M6 16 H26" stroke="' +
    palette.mauve12 +
    '" stroke-width="3.6" stroke-linecap="round"/></svg></span>Planter dans le Cercle';
  tete.append(cale, planter);
  return { tete, cale, planter };
}

/**
 * LE MENU DE « PLANTER DANS LE CERCLE » (C-230, v179b ; lot-V179B-CERCLE-PLUS) — deux encarts, Chiche puis Promi, les codes des encarts du + de
 * l'accueil (l'aplat de la nature, le contour crème de 2 pt, « Un » en Gilbert, la nature en PromiLate capitales) à 0,89 de leur taille, sans le
 * texte de droite (300 × 60, 11 pt entre deux), centrés sur le bouton, 10 pt au-dessus de lui. Un encart touché referme le menu et ouvre la page +
 * de sa nature ; un toucher à côté le referme et n'actionne rien dessous.
 */
export interface MenuPlanter {
  ouvrir(bouton: HTMLElement): void;
  fermer(): void;
  ouvert(): boolean;
}
/** posé DANS la fiche (`hote`) : l'appareil couvert par elle ne montre qu'elle (base.css, `.couvert`) ; le doigt se lit sur l'appareil (`dv`) */
export function monterMenuPlanter(
  hote: HTMLElement,
  dv: HTMLElement,
  choisir: (nat: 'promi' | 'chiche') => void,
): MenuPlanter {
  const M = el('div', { id: 'cpChoix', role: 'menu' });
  M.innerHTML =
    '<div class="cp-pil" data-k="chiche" role="menuitem"><span class="acc-un">Un <i class="acc-nat">Chiche</i></span></div>' +
    '<div class="cp-pil" data-k="promi" role="menuitem"><span class="acc-un">Un <i class="acc-nat">Promi</i></span></div>';
  hote.appendChild(M);
  let ouvert = false;
  let d: { k: string | null; x: number; y: number; t: number } | null = null;
  const fermer = (): void => {
    M.classList.remove('ouvert');
    ouvert = false;
  };
  // au doigt (en capture) : sur un encart, le geste ; à côté, le menu se referme et le toucher est avalé (rien dessous ne s'actionne)
  dv.addEventListener(
    'pointerdown',
    (ev) => {
      if (!ouvert) return;
      const t = ev.target instanceof Element ? ev.target : null;
      const pil = t?.closest<HTMLElement>('#cpChoix .cp-pil');
      if (pil) {
        d = { k: pil.dataset['k'] ?? null, x: ev.clientX, y: ev.clientY, t: ev.timeStamp };
        return;
      }
      if (t?.closest('#nfAdd')) return;
      fermer();
      ev.stopPropagation();
      const avale = (e: Event): void => {
        e.stopPropagation();
      };
      dv.addEventListener('pointerup', avale, { capture: true, once: true });
    },
    true,
  );
  dv.addEventListener(
    'pointerup',
    (ev) => {
      const g = d;
      d = null;
      if (!g?.k || Math.hypot(ev.clientX - g.x, ev.clientY - g.y) > 10 || ev.timeStamp - g.t > 600) return;
      ev.stopPropagation();
      fermer();
      choisir(g.k === 'chiche' ? 'chiche' : 'promi');
    },
    true,
  );
  return {
    ouvrir(bouton) {
      const D = hote.getBoundingClientRect();
      const k = D.width / hote.offsetWidth || 1;
      const r = bouton.getBoundingClientRect();
      const cx = (r.left + r.width / 2 - D.left) / k;
      const top = (r.top - D.top) / k;
      M.style.left = `${String(Math.round(cx - 150))}px`;
      M.style.top = `${String(Math.round(top - 10 - 131))}px`;
      M.classList.add('ouvert');
      ouvert = true;
    },
    fermer,
    ouvert: () => ouvert,
  };
}
