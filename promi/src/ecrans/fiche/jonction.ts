/**
 * LA JONCTION (lot 3a-3 — C-259, Q617, C-267, v195 à v201 ; le prototype : lot-V187-HAUT, lot-V189-JONCTION). Quand la fiche défile, le trait
 * monte jusqu'à la jonction (112 pt, le bas du plateau) et s'y couche à plat ; au retour, l'inverse. LA RÈGLE (Tom, v195) : pendant le défilement,
 * rien de visible ne dépend d'une animation ni d'un script — quatre calques posés quand la fiche change, jamais au défilement :
 *  ① la BANDE (z 8) : collée en haut (`sticky`, 0 → 112 pt), une copie du haut du champ ; ce qui monte passe dessous, coupé net ;
 *  ② la VAGUE (z 7) : le trait de la fiche (sa couche, fiche.ts), qui défile avec le contenu ;
 *  ③ la FENÊTRE (z 5), qui défile avec le contenu et découpe (`clip-path`, colonne par colonne) ce qui est sous le dernier pixel plein de la vague ;
 *  ④ dedans, le TRAIT PLAT, collé à la jonction (`sticky`, 110 pt : 2 pt du champ, puis le trait du même peintre, l'onde d'amplitude 0).
 * Au repos le trait plat est hors de la fenêtre ; en défilant il se découvre sous la vague, contigu (v200, C-267 : plus de cache).
 * Accroché (le haut de la vague à la jonction), le geste ne prend plus le doigt : il fait défiler (v191). Au repos, la vague n'est jamais à demi
 * sous la bande (v201 ①, C-267) : pendant un geste, des aimants (`scroll-snap`) tiennent les places sûres — de 0 à `a` (la vague entière sous 112),
 * et de `z` (entière sous la bande) jusqu'au bout ; entre les deux, aucun : le défilement finit sur la plus proche.
 */
import { onde } from '../page-plus/onde.ts';
import { TRAIT_K } from '../page-plus/trait.ts';
import { el } from '../commun.ts';
import { horloge } from '../../animation/horloge.ts';

/** la jonction (le bas du plateau), le débord de chaque côté, la hauteur du trait plat, les 2 pt de champ au-dessus, la marge haute de la vague */
const J = 112;
const XO = 2;
const HP = 40;
const CH = 2;
const MH = 30;
const W = 390;

export interface HoteJonction {
  defile: HTMLElement;
  champ: HTMLCanvasElement;
  /** le fond de la fiche (la bande se peint dessus, puis le haut du champ) */
  fond(): string;
  /** la zone du geste (coupée accrochée) */
  zone(): HTMLElement | null;
  /** le peintre de la ligne de la fiche, sans le doigt (fiche.ts) */
  ligne(g: CanvasRenderingContext2D, base: number, amp: number): void;
}

export interface Bornes {
  a: number;
  z: number;
  m: number;
}

export interface Jonction {
  /** la fiche posée : le trait (base, amplitude), la couleur du champ au-dessus de la vague, la hauteur du contenu */
  poser(o: { base: number; amp: number; champ: string; hauteur: number }): void;
  cacher(): void;
  etat(): {
    montre: boolean;
    coupe: boolean;
    s0: number;
    Ytop: number;
    H: number;
    HW: number;
    bornes: Bornes | null;
    aimants: boolean;
    decoupe: string;
  };
}

export function monterJonction(h: HoteJonction): Jonction {
  const d = h.defile;
  const bande = el('canvas', { id: 'v187Bande', 'aria-hidden': 'true' });
  const fenetre = el('div', { id: 'v200Fenetre', 'aria-hidden': 'true' });
  const plat = el('div', { id: 'v195Plat', 'aria-hidden': 'true' });
  const platCv = el('canvas', { 'aria-hidden': 'true' });
  plat.appendChild(platCv);
  fenetre.appendChild(plat);
  const aim = el('div', { class: 'v203-aimants', 'aria-hidden': 'true' });

  let F: null | {
    s0: number;
    Ytop: number;
    H: number;
    haut: number | null;
    basV: number | null;
    m: number;
  } = null;
  let HW = 0;
  let CP = '';
  let montre = false;

  /** l'image de la vague, rendue hors du document dans la géométrie du prototype (largeur 390 + 2 × 2, à partir de Ytop) : ses pixels */
  function lire(
    base: number,
    amp: number,
    E: number,
    Ytop: number,
    H: number,
  ): { LF: number[]; haut: number | null; basV: number | null } {
    const w = Math.round((W + 2 * XO) * E);
    const hh = Math.max(1, Math.round(H * E));
    const T = document.createElement('canvas');
    T.width = w;
    T.height = hh;
    // sans `willReadFrequently` : ce canevas-là est rendu par le processeur et lisse autrement (CLAUDE.md, v164b) — le découpage changerait d'un
    // pixel de l'appareil sur une colonne sur dix
    const g = T.getContext('2d')!;
    g.setTransform(E, 0, 0, E, XO * E, -Ytop * E);
    g.lineCap = 'round';
    g.lineJoin = 'round';
    h.ligne(g, base, amp);
    const a = g.getImageData(0, 0, w, hh).data;
    // le haut et le bas de ce qui est peint (une colonne sur deux) : les bornes des places sûres
    let r0 = -1;
    let r1 = -1;
    for (let r = 0; r < hh && r0 < 0; r++)
      for (let x = 0; x < w; x += 2)
        if (a[(r * w + x) * 4 + 3]! > 8) {
          r0 = r;
          break;
        }
    for (let r = hh - 1; r >= 0 && r1 < 0; r--)
      for (let x = 0; x < w; x += 2)
        if (a[(r * w + x) * 4 + 3]! > 8) {
          r1 = r;
          break;
        }
    // colonne par colonne de l'appareil : le haut du dernier pixel PLEIN (sinon du dernier pixel peint au bord d'un point), sinon le bas du trait
    const P = onde(base, amp);
    const lw = 10 * TRAIT_K;
    const LF: number[] = [];
    for (let x = 0; x < w; x++) {
      let b: number | null = null;
      let bord: number | null = null;
      for (let r = hh - 1; r >= 0; r--) {
        const al = a[(r * w + x) * 4 + 3]!;
        if (al > 250) {
          b = Ytop + r / E;
          break;
        }
        if (al > 8 && bord === null) bord = Ytop + r / E;
      }
      if (b === null && bord !== null) b = bord;
      if (b === null) b = P(Math.min(W, Math.max(0, Math.round(x / E) - XO))) + lw / 2;
      LF.push(b);
    }
    return { LF, haut: r0 >= 0 ? Ytop + r0 / E : null, basV: r1 >= 0 ? Ytop + (r1 + 1) / E : null };
  }

  function poser(o: { base: number; amp: number; champ: string; hauteur: number }): void {
    const E = h.champ.width / W || 2;
    const lw = 10 * TRAIT_K;
    const y = onde(o.base, o.amp);
    let mn = 1e9;
    let mx = -1e9;
    for (let x = 0; x <= W; x += 2) {
      const v = y(x);
      mn = Math.min(mn, v);
      mx = Math.max(mx, v);
    }
    const Ytop = Math.floor(Math.max(Math.min(J, mn - lw / 2 - 17), mn - lw / 2 - MH));
    const H = Math.ceil(mx + lw / 2 + 40 - Ytop);
    const m = Math.max(0, o.hauteur - d.clientHeight);
    const lu = lire(o.base, o.amp, E, Ytop, H);
    F = { s0: mn - lw / 2 - J, Ytop, H, haut: lu.haut, basV: lu.basV, m };

    // ① la bande : le fond de la fiche, puis le haut du champ (0 → 112)
    bande.width = Math.round(W * E);
    bande.height = Math.round(J * E);
    const gb = bande.getContext('2d')!;
    gb.setTransform(1, 0, 0, 1, 0, 0);
    gb.clearRect(0, 0, bande.width, bande.height);
    gb.fillStyle = h.fond();
    gb.fillRect(0, 0, bande.width, bande.height);
    const hc = Math.min(J, h.champ.offsetHeight || J);
    gb.drawImage(h.champ, 0, 0, h.champ.width, hc * E, 0, 0, h.champ.width, hc * E);

    // ④ le trait plat : 2 pt du champ, puis le trait couché à la jonction (le même peintre, l'onde d'amplitude 0), coupé net à 112 + 40
    platCv.width = Math.round((W + 2 * XO) * E);
    platCv.height = Math.round(HP * E);
    const gp = platCv.getContext('2d')!;
    gp.setTransform(1, 0, 0, 1, 0, 0);
    gp.clearRect(0, 0, platCv.width, platCv.height);
    gp.setTransform(E, 0, 0, E, XO * E, -(J - CH) * E);
    gp.imageSmoothingEnabled = true;
    gp.lineCap = 'round';
    gp.lineJoin = 'round';
    gp.fillStyle = o.champ;
    gp.fillRect(-XO, J - CH, W + 2 * XO, CH);
    gp.save();
    gp.beginPath();
    gp.rect(-XO, J, W + 2 * XO, HP);
    gp.clip();
    h.ligne(gp, J + lw / 2, 0);
    gp.restore();

    // ③ la fenêtre : assez haute pour que le trait plat reste collé jusqu'au bout du défilement, sans allonger la fiche (`fenetre()`)
    HW = Math.ceil(Math.max(m + HP + 8, o.hauteur - (J - CH) - 60));
    fenetre.style.height = `${String(HW)}px`;
    fenetre.style.marginBottom = `${String(-(J - CH + HW))}px`;
    const p: string[] = [];
    let yp: number | null = null;
    for (let i = 0; i < lu.LF.length; i++) {
      const v = Math.round((lu.LF[i]! - (J - CH)) * 100) / 100;
      if (v !== yp) {
        const xg = Math.round((i / E) * 1000) / 1000;
        if (yp !== null) p.push(`${String(xg)}px ${String(yp)}px`);
        p.push(`${String(xg)}px ${String(v)}px`);
        yp = v;
      }
    }
    p.push(`${String(W + 2 * XO)}px ${String(yp)}px`, `${String(W + 2 * XO)}px 100%`, '0px 100%');
    const v = `polygon(${p.join(',')})`;
    if (v !== CP) {
      CP = v;
      fenetre.style.clipPath = v;
    }

    if (!montre) {
      montre = true;
      d.prepend(bande, fenetre);
    }
    aimants();
    relit();
  }

  function cacher(): void {
    montre = false;
    F = null;
    HW = 0;
    CP = '';
    bande.remove();
    fenetre.remove();
    aimante(false);
    geste(false);
  }

  // ── LE GESTE ACCROCHÉ : il ne prend plus le doigt (`geste`, `accroche`) ──
  let coupe = false;
  function geste(acc: boolean): void {
    if (acc === coupe) return;
    coupe = acc;
    const z = h.zone();
    if (z) z.style.pointerEvents = coupe ? 'none' : '';
  }
  function relit(): void {
    geste(!!(montre && F && d.scrollTop >= F.s0 + 0.25));
  }

  // ── LES PLACES SÛRES (`bornes`, `aimants`, `aimante`) ──
  function bornes(): Bornes | null {
    if (!F || F.haut == null || F.basV == null) return null;
    return { a: Math.max(0, Math.floor(F.haut - J - 1)), z: Math.ceil(F.basV - J + 1), m: F.m };
  }
  let aimOn = false;
  let aimT: number | null = null;
  function aimants(): void {
    const b = bornes();
    if (!b) {
      aim.remove();
      return;
    }
    const P: number[] = [];
    for (let s = 0; s < b.a; s += 6) P.push(s);
    P.push(b.a);
    if (b.z <= b.m) {
      const pas = Math.max(6, Math.ceil((b.m - b.z) / 300));
      for (let s = b.z; s <= b.m; s += pas) P.push(s);
    }
    const cle = P.join(',');
    if (aim.getAttribute('data-cle') !== cle) {
      aim.setAttribute('data-cle', cle);
      aim.innerHTML = P.map((t) => `<i style="top:${String(t)}px"></i>`).join('');
    }
    if (aimOn && !aim.isConnected) d.appendChild(aim);
  }
  function aimante(on: boolean): void {
    const ok = on && montre && !!F;
    if (ok === aimOn) return;
    aimOn = ok;
    if (ok) {
      aimants();
      d.appendChild(aim);
      d.style.scrollSnapType = 'y proximity';
    } else {
      d.style.removeProperty('scroll-snap-type');
      aim.remove();
    }
  }
  // les doigts sur l'écran (le prototype : `window.__doigts`) : les aimants restent tant qu'un doigt est posé
  let doigts = 0;
  window.addEventListener(
    'touchstart',
    (e) => {
      doigts = e.touches.length;
      relit();
    },
    { capture: true, passive: true },
  );
  for (const t of ['touchend', 'touchcancel'] as const)
    window.addEventListener(
      t,
      (e) => {
        doigts = e.touches.length;
      },
      { capture: true, passive: true },
    );
  window.addEventListener('pointerdown', relit, { capture: true, passive: true });
  d.addEventListener('scroll', relit, { passive: true });
  d.addEventListener('scrollend', relit, { passive: true });
  d.addEventListener(
    'wheel',
    () => {
      aimante(true);
      if (aimT != null) horloge().annuleMinuteur(aimT);
      aimT = horloge().minuteur(() => {
        aimT = null;
      }, 400);
    },
    { passive: true },
  );
  d.addEventListener(
    'touchstart',
    () => {
      aimante(true);
      if (aimT != null) horloge().annuleMinuteur(aimT);
      aimT = null;
    },
    { passive: true },
  );
  d.addEventListener(
    'scrollend',
    () => {
      if (doigts > 0) return;
      if (aimT != null) horloge().annuleMinuteur(aimT);
      aimT = horloge().minuteur(() => {
        aimT = null;
        if (doigts === 0) aimante(false);
      }, 250);
    },
    { passive: true },
  );

  // ── SOUS LA BANDE, RIEN NE SE TOUCHE : la fiche défilée, un toucher au-dessus de 112 pt est avalé (lot-V187-HAUT) ──
  const avale = (e: Event): void => {
    if (!montre || d.scrollTop <= 0.5 || !(e instanceof MouseEvent) || !e.isTrusted) return;
    const t = e.target;
    if (!(t instanceof Element) || t.closest('.ph-photo-btn')) return;
    const R = d.getBoundingClientRect();
    const k = R.width / (d.offsetWidth || W) || 1;
    if ((e.clientY - R.top) / k < J) {
      e.preventDefault();
      e.stopImmediatePropagation();
    }
  };
  for (const t of ['pointerdown', 'pointerup', 'click'] as const) d.addEventListener(t, avale, true);

  return {
    poser,
    cacher,
    etat: () => ({
      montre,
      coupe,
      s0: F?.s0 ?? 0,
      Ytop: F?.Ytop ?? 0,
      H: F?.H ?? 0,
      HW,
      bornes: bornes(),
      aimants: aimOn,
      decoupe: CP,
    }),
  };
}
