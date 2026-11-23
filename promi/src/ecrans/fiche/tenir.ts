/**
 * TENIR UNE PAROLE (lot 3a-2, SPEC-GESTE §2.6, SPEC-ECRANS §4 ; le prototype : `_tenirInit` l. 4982, `lot-V148-RUBAN`, `lot-V146-MAREE`,
 * `lot-S5` « le moteur de l'instant », `lot-V145-PARTS`) — le geste de la fiche, et ce qu'il déclenche :
 *  · LE GESTE : la zone de 118 pt calée sur le bas de la boîte du trait ; le doigt part de la première moitié (x ≤ 239) ; pendant les 340 premières
 *    ms le doigt n'est pas encore suivi (l'ouverture de la zone, comme le prototype) ; ensuite le plein suit le doigt (C-247, C-264) ; 60 pt d'avancée
 *    (C-107, `_traitRegle.MIN`) posent le ruban ; lâché avant, le trait revient (la loi de la page +, rapportée à la pointe : 300 ms, linéaire).
 *  · LE RUBAN (C-148, C-156) : amande pleine, 43 pt au-dessus du trait, 51 dessous, ses bords ondulent à peine ; il naît en 200 ms et découpe le mot
 *    du geste ; tenue : son haut redescend à la vitesse du rideau, qui part de son bord bas ; ma part seule : il tient 520 ms puis se resserre.
 *  · LE RIDEAU (C-118, C-155, C-156, C-167, C-311) : une seule matière amande, du bord haut du trait jusqu'à un front qui descend à vitesse
 *    constante jusqu'à la barre (700 ms), « Parole tenue ! » / « Défi relevé ! » à l'encre, fixe à l'écran ; il remonte à 2 150 ms (560 ms), ou dès
 *    qu'on touche l'écran (le toucher est avalé).
 *  · « Réduire les animations » (E3) : ni ruban qui dure, ni rideau, ni instant — la fiche passe tenue d'un coup.
 * Les constantes sont celles du prototype, en dur ; les tests les portent (tests/rendu/tenir*.spec.ts).
 */
import { horloge } from '../../animation/horloge.ts';
import { palette } from '../../design/jetons.ts';
import { onde, type Onde } from '../page-plus/onde.ts';
import { el } from '../commun.ts';
import { W } from './ligne.ts';

/** C-107 : un trait ne compte qu'à 60 pt d'avancée */
export const MIN_TRAIT = 60;
/** le départ du doigt : la première moitié et 44 pt au-delà */
export const DEPART_MAX = W / 2 + 44;
/** la zone s'ouvre : le doigt n'est suivi qu'après (le prototype, `fin0 = Date.now() + 340`) */
export const OUVERTURE = 340;
/** C-167 : le temps que le vert reste posé (2 150 ms) */
export const AMANDE = 2150;
export const RUBAN = { HAUT: 43, BAS: 51, NAIT: 200, RENTRE: 240, PART_TIENT: 520, PART_RENTRE: 320 } as const;
export const RIDEAU = { BAR: 760, DESC: 700, MONTE: 560, EP: 12, BORD: 7 } as const;
const VERT = palette.menthe82;
const ENCRE = palette.brun09;

export type Instant = null | 'referme' | 'apres';

export interface HoteTenir {
  fi: HTMLElement;
  /** le mot du geste (« trace pour tenir ») : le ruban le découpe */
  mot: HTMLElement;
  /** l'onde du trait au repos */
  trait(): { base: number; amp: number };
  /** le geste est-il permis (une parole ouverte, pas tenue) */
  actif(): boolean;
  /** repeint le trait, le plein jusqu'au doigt (null : au repos) */
  doigt(x: number | null): void;
  /**
   * le trait est tracé jusqu'au bout : la parole est tenue (ou ma part). `referme` : la fiche se repose dans l'instant « le trait se referme »
   * (sous le rideau) — sinon (mouvement réduit), directement tenue.
   */
  tenir(trace: Array<{ x: number; y: number }>, referme: boolean): 'tenue' | 'part' | 'rien';
  /** la phrase de la célébration */
  phrase(): string;
  /** « juste après » : la fiche se repose (elle le reste tant qu'elle est ouverte, comme le prototype) */
  apres(): void;
}

export interface Tenir {
  /** la zone suit la boîte du trait ; cachée si rien n'est à tracer */
  poser(visible: boolean): void;
  /** tout s'arrête (la fiche se ferme) */
  arreter(): void;
  /** pour les tests */
  etat(): {
    geste: boolean;
    atteint: boolean;
    doigt: number | null;
    avance: number;
    ruban: boolean;
    rideau: null | { t0: number; v: number; monte: boolean };
    instant: Instant;
    dernier: null | { avance: number; ok: boolean };
  };
}

function reduit(): boolean {
  try {
    return matchMedia('(prefers-reduced-motion: reduce)').matches;
  } catch {
    return false;
  }
}
const io3 = (u: number): number => 1 - Math.pow(1 - Math.max(0, Math.min(1, u)), 3);
const ioS = (u: number): number => {
  u = Math.max(0, Math.min(1, u));
  return u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
};

export function monterTenir(h: HoteTenir): Tenir {
  const H = horloge();
  const env = el('div', { class: 'geste-env' });
  const zone = el('div', { id: 'tenirZone', class: 'tenir', 'aria-label': 'Trace pour tenir' });
  env.appendChild(zone);
  h.fi.appendChild(env);
  let instant: Instant = null;
  let dernier: null | { avance: number; ok: boolean } = null;

  // ── LE GESTE ──
  let g: null | {
    id: number;
    x0: number;
    xm: number;
    fin0: number;
    atteint: boolean;
    pts: Array<{ x: number; y: number }>;
  } = null;
  let doigt: number | null = null;
  let retour: number | null = null;
  const local = (ev: PointerEvent): { x: number; y: number } => {
    const r = zone.getBoundingClientRect();
    const k = r.width / (zone.offsetWidth || W) || 1;
    return { x: (ev.clientX - r.left) / k, y: (ev.clientY - r.top) / k };
  };
  zone.addEventListener('pointerdown', (ev) => {
    if (!h.actif() || instant || rideau) return;
    const p = local(ev);
    if (p.x > DEPART_MAX) return;
    if (retour != null) H.annuleImage(retour);
    retour = null;
    g = { id: ev.pointerId, x0: p.x, xm: p.x, fin0: H.maintenant() + OUVERTURE, atteint: false, pts: [] };
    zone.classList.add('ouvert');
    h.fi.classList.add('tracant');
    try {
      zone.setPointerCapture(ev.pointerId);
    } catch {
      /* un pointeur déjà levé */
    }
    ev.preventDefault();
  });
  zone.addEventListener('pointermove', (ev) => {
    if (!g || ev.pointerId !== g.id) return;
    if (H.maintenant() < g.fin0) return;
    const p = local(ev);
    g.pts.push(p);
    g.xm = Math.max(g.xm, p.x);
    if (!g.atteint && g.xm - g.x0 >= MIN_TRAIT) {
      g.atteint = true;
      zone.classList.add('atteint');
      poseRuban();
    }
    doigt = Math.max(0, Math.min(W, p.x));
    h.doigt(doigt);
  });
  const leve = (ev: PointerEvent): void => {
    if (!g || ev.pointerId !== g.id) return;
    const G = g;
    g = null;
    const avance = G.xm - G.x0;
    const ok = avance >= MIN_TRAIT;
    dernier = { avance, ok };
    zone.classList.remove('ouvert', 'atteint');
    h.fi.classList.remove('tracant');
    if (!ok) {
      rentreRuban('part');
      revient();
      return;
    }
    doigt = null;
    h.doigt(null);
    // l'onde du repos, prise avant que la fiche se repose (le rideau part de ce trait-là)
    const T = h.trait();
    const animer = !reduit();
    if (animer) {
      instant = 'referme';
      demarreRideau(T);
    }
    const r = h.tenir(G.pts, animer);
    if (r !== 'tenue' || !animer) {
      if (rideau) arreteRideau();
      instant = null;
      rentreRuban('part');
      return;
    }
    rentreRuban('rideau');
  };
  zone.addEventListener('pointerup', leve);
  zone.addEventListener('pointercancel', leve);

  /** lâché avant : le plein revient à la pointe (la loi de la page +, rapportée à la pointe : `_ficheDoigt = MI + max(0, v0·(1−u) − P0)`) */
  function revient(): void {
    if (doigt == null) return;
    const P0 = W * 0.11;
    const MI = W / 2;
    const v0 = Math.max(0, doigt - MI) + P0;
    const t0 = H.maintenant();
    const pas = (): void => {
      retour = null;
      if (g) return;
      const u = Math.min(1, (H.maintenant() - t0) / 300);
      doigt = u < 1 ? MI + Math.max(0, v0 * (1 - u) - P0) : null;
      h.doigt(doigt);
      if (u < 1) retour = H.image(pas);
    };
    pas();
  }

  // ── LE RUBAN AMANDE (lot-V148-RUBAN) ──
  let ruban: null | {
    cv: HTMLCanvasElement;
    t0: number;
    rentre0: number;
    mode: '' | 'rideau' | 'part';
    basK: number;
    tps: number;
    y: Onde;
    ph: number[];
    img: number | null;
  } = null;
  const decoupe = (k: number): void => {
    const v = `inset(0 0 0 ${(Math.max(0, Math.min(1, k)) * 100).toFixed(1)}%)`;
    h.mot.style.setProperty('clip-path', v);
    h.mot.style.setProperty('-webkit-clip-path', v);
  };
  const bord = (R: { ph: number[] }, x: number, k: number, tps: number): number =>
    k *
    (1.6 * Math.sin(x * 0.024 + R.ph[k > 0 ? 0 : 2]! + tps * 0.9) +
      0.9 * Math.sin(x * 0.061 + R.ph[k > 0 ? 1 : 3]! - tps * 1.3));
  function poseRuban(): void {
    if (ruban) arreteRuban();
    const T = h.trait();
    const y0 = Math.floor(T.base - T.amp - RUBAN.HAUT - 6);
    const hh = Math.ceil(2 * T.amp + RUBAN.HAUT + RUBAN.BAS + 12);
    const dpr = Math.max(2, Math.min(3, window.devicePixelRatio || 2));
    const cv = el('canvas', { id: 'tenirRuban', 'aria-hidden': 'true' });
    cv.width = Math.round(W * dpr);
    cv.height = Math.round(hh * dpr);
    cv.style.cssText = `position:absolute;left:0;top:${String(y0)}px;width:${String(W)}px;height:${String(hh)}px;pointer-events:none;z-index:39`;
    h.fi.appendChild(cv);
    const c = cv.getContext('2d')!;
    c.setTransform(dpr, 0, 0, dpr, 0, -y0 * dpr);
    const R = {
      cv,
      t0: H.maintenant(),
      rentre0: 0,
      mode: '' as '' | 'rideau' | 'part',
      basK: 0,
      tps: 0,
      y: onde(T.base, T.amp),
      ph: [0, 1, 2, 3].map(() => Math.random() * 6.28),
      img: null as number | null,
    };
    ruban = R;
    const dessine = (): void => {
      R.img = null;
      if (ruban !== R) return;
      const now = H.maintenant();
      const tps = (now - R.t0) / 1000;
      const e = reduit() ? 1 : io3((now - R.t0) / RUBAN.NAIT);
      let hautK = e;
      let basK = e;
      if (R.rentre0 && R.mode === 'rideau') {
        // ① le haut redescend sur le trait à la vitesse du rideau, le bas tient : le rideau part de lui
        if (!rideau) {
          if (now - R.rentre0 > 220) {
            arreteRuban();
            return;
          }
        } else {
          const q = Math.min(1, ((now - rideau.t0) * Math.max(0.2, rideau.v)) / RUBAN.HAUT);
          hautK = e * (1 - q);
          if (q >= 1) {
            arreteRuban();
            return;
          }
        }
      } else if (R.rentre0 && R.mode === 'part') {
        // ② la vague sous le trait, seule : le haut se retire, le bas tient un instant puis se resserre à vitesse constante
        const r2 = reduit() ? 1 : io3((now - R.rentre0) / RUBAN.RENTRE);
        hautK = e * (1 - r2);
        const q2 = reduit() ? 1 : Math.max(0, Math.min(1, (now - R.rentre0 - RUBAN.PART_TIENT) / RUBAN.PART_RENTRE));
        basK = e * (1 - q2);
        decoupe(basK);
        if (q2 >= 1) {
          arreteRuban();
          return;
        }
      } else decoupe(e);
      R.basK = basK;
      R.tps = tps;
      c.clearRect(0, y0, W, hh);
      c.beginPath();
      c.moveTo(-2, R.y(0) - RUBAN.HAUT * hautK + bord(R, 0, 1, tps) * hautK);
      for (let x = 4; x <= W + 2; x += 4)
        c.lineTo(x, R.y(Math.min(W, x)) - RUBAN.HAUT * hautK + bord(R, x, 1, tps) * hautK);
      for (let x = W + 2; x >= -2; x -= 4)
        c.lineTo(x, R.y(Math.max(0, Math.min(W, x))) + RUBAN.BAS * basK + bord(R, x, -1, tps) * basK);
      c.closePath();
      c.fillStyle = VERT;
      c.fill();
      R.img = H.image(dessine);
    };
    dessine();
  }
  function rentreRuban(mode: 'rideau' | 'part'): void {
    if (!ruban || ruban.rentre0) return;
    ruban.mode = mode;
    ruban.rentre0 = H.maintenant();
    if (mode === 'rideau') {
      const R = ruban;
      H.minuteur(() => {
        if (ruban === R) arreteRuban();
      }, 1200);
    }
  }
  function arreteRuban(): void {
    if (!ruban) return;
    if (ruban.img != null) H.annuleImage(ruban.img);
    ruban.cv.remove();
    // tenue : le mot reste découpé (l'instant le cache) ; sinon il revient
    if (ruban.mode !== 'rideau') {
      h.mot.style.removeProperty('clip-path');
      h.mot.style.removeProperty('-webkit-clip-path');
    }
    ruban = null;
  }
  /** le bord bas du ruban tel qu'il est peint (x de 392 à −2, pas de 4) — le départ du rideau */
  function basRuban(): number[] | null {
    const R = ruban;
    if (!R) return null;
    const A: number[] = [];
    for (let x = W + 2; x >= -2; x -= 4)
      A.push(R.y(Math.max(0, Math.min(W, x))) + RUBAN.BAS * R.basK + bord(R, x, -1, R.tps) * R.basK);
    return A;
  }

  // ── LE RIDEAU (lot-V146-MAREE) ──
  let rideau: null | {
    cv: HTMLCanvasElement;
    t0: number;
    v: number;
    monte0: number;
    vite: number;
    img: number | null;
    garde: number | null;
  } = null;
  function demarreRideau(T: { base: number; amp: number }): void {
    if (rideau) arreteRideau();
    const { BAR, DESC, MONTE, EP, BORD } = RIDEAU;
    const y = onde(T.base, T.amp);
    const y0 = Math.floor(T.base - T.amp - EP);
    let F0 = 1e9;
    for (let x = 0; x <= W; x += 4) F0 = Math.min(F0, y(x) + EP / 2 - y0);
    const FIN = BAR - y0 + BORD + 4;
    const ph = [0, 1, 2].map(() => Math.random() * 6.28);
    const chemin = (c: CanvasRenderingContext2D, u: number, tps: number, depart: number[]): void => {
      const a = BORD * Math.min(1, u * 5) * Math.min(1, (1 - u) * 6 + 0.35);
      let smax = -1e9;
      for (const d of depart) if (d > smax) smax = d;
      const q = Math.min(1, u / 0.25);
      const s = q * q * (3 - 2 * q);
      const Hh = smax + u * (FIN - smax);
      c.moveTo(-2, y0 - 4);
      c.lineTo(392, y0 - 4);
      let i = 0;
      for (let x = 392; x >= -2; x -= 4, i++) {
        const e =
          0.55 * Math.sin(x * 0.021 + ph[0]! + tps * 1.1) +
          0.3 * Math.sin(x * 0.047 + ph[1]! - tps * 1.7) +
          0.15 * Math.sin(x * 0.093 + ph[2]! + tps * 2.3);
        const d0 = depart[i]!;
        c.lineTo(x, y0 + (1 - s) * (d0 + u * (FIN - d0)) + s * Hh + a * e);
      }
      c.closePath();
    };
    const MONT: number[] = [];
    for (let x = 392; x >= -2; x -= 4) MONT.push(y(Math.max(0, Math.min(W, x))) + EP / 2 - y0);
    const rb = basRuban();
    const DEP = rb ? rb.map((v) => Math.max(v - y0, F0)) : MONT.slice();
    let vMoy = 0;
    for (const s of DEP) vMoy += FIN - s;
    vMoy = vMoy / DEP.length / DESC;
    const dpr = Math.max(2, Math.min(3, window.devicePixelRatio || 2));
    const cv = el('canvas', { id: 'tenirMaree', role: 'img', 'aria-label': h.phrase(), 'data-eng': 'tenir' });
    cv.width = Math.round(W * dpr);
    cv.height = Math.round(844 * dpr);
    cv.style.cssText = 'position:absolute;left:0;top:0;width:390px;height:844px;pointer-events:none;z-index:7';
    h.fi.appendChild(cv);
    const c = cv.getContext('2d')!;
    // la phrase, écrite une fois hors du document (le prototype : `TX`), posée à chaque image ; fixe à l'écran (C-311)
    const mot = h.phrase();
    const fs = 40;
    const fx = W / 2;
    const fy = 388 + 40 * 1.1 * 0.78;
    const police = `${String(fs)}px Gilbert, system-ui`;
    const TX = document.createElement('canvas');
    let tg = TX.getContext('2d')!;
    tg.font = police;
    const lw = tg.measureText(mot).width;
    const TXx = Math.floor((fx - lw / 2 - 8) * dpr);
    const TXy = Math.floor((fy - fs * 1.25) * dpr);
    TX.width = Math.ceil((lw + 16) * dpr);
    TX.height = Math.ceil(fs * 1.8 * dpr);
    tg = TX.getContext('2d')!;
    tg.setTransform(dpr, 0, 0, dpr, -TXx, -TXy);
    tg.font = police;
    tg.fillStyle = ENCRE;
    tg.textBaseline = 'alphabetic';
    tg.textAlign = 'center';
    tg.fillText(mot, fx, fy);
    const zoneZ = (): void => {
      c.beginPath();
      c.moveTo(0, y(0) - EP / 2);
      for (let x = 6; x <= W; x += 6) c.lineTo(x, y(x) - EP / 2);
      c.lineTo(W, BAR);
      c.lineTo(0, BAR);
      c.closePath();
    };
    const bande = (e: number): void => {
      c.beginPath();
      c.moveTo(0, y(0) - EP / 2);
      for (let x = 6; x <= W; x += 6) c.lineTo(x, y(x) - EP / 2);
      for (let x = W; x >= 0; x -= 6) c.lineTo(x, y(x) - EP / 2 + e);
      c.closePath();
    };
    const R = {
      cv,
      t0: H.maintenant(),
      v: vMoy,
      monte0: 0,
      vite: 0,
      img: null as number | null,
      garde: null as number | null,
    };
    rideau = R;
    const f = (): void => {
      R.img = null;
      if (rideau !== R) return;
      const now = H.maintenant();
      const t = now - R.t0;
      if (!R.monte0 && (t >= AMANDE || R.vite)) {
        R.monte0 = now;
        if (instant === 'referme') {
          instant = 'apres';
          h.apres();
        }
      }
      const u = R.monte0 ? 1 - ioS((now - R.monte0) / MONTE) : Math.max(0, Math.min(1, t / DESC));
      c.setTransform(dpr, 0, 0, dpr, 0, 0);
      c.clearRect(0, 0, W, 844);
      if (u <= 0.001 && R.monte0) {
        arreteRideau();
        return;
      }
      const tps = t / 1000;
      c.save();
      zoneZ();
      c.clip();
      c.fillStyle = VERT;
      bande(R.monte0 ? EP + 34 * Math.min(1, u / 0.35) : EP);
      c.fill();
      if (u > 0) {
        c.beginPath();
        chemin(c, u, tps, R.monte0 ? MONT : DEP);
        c.fill();
      }
      c.restore();
      if (u > 0.02) {
        const sd = h.fi.scrollTop || 0;
        c.save();
        zoneZ();
        c.clip();
        c.beginPath();
        chemin(c, Math.max(u, 0.0001), tps, R.monte0 ? MONT : DEP);
        c.clip();
        c.setTransform(1, 0, 0, 1, 0, 0);
        c.drawImage(TX, TXx, TXy + Math.round(sd * dpr));
        c.restore();
      }
      R.img = H.image(f);
    };
    f();
    // garde-fou : rien ne reste suspendu si l'affichage s'arrête
    R.garde = H.minuteur(() => {
      if (rideau === R) arreteRideau();
    }, 4500);
  }
  function arreteRideau(): void {
    if (!rideau) return;
    if (rideau.img != null) H.annuleImage(rideau.img);
    if (rideau.garde != null) H.annuleMinuteur(rideau.garde);
    rideau.cv.remove();
    rideau = null;
  }

  // C-167 : pendant que le vert est posé, un toucher n'importe où le fait remonter tout de suite ; le toucher est avalé (rien dessous ne s'ouvre)
  let aval = 0;
  const presse = (ev: Event): void => {
    const n = H.maintenant();
    if (aval && n - aval < 700) {
      ev.stopImmediatePropagation();
      if (ev.cancelable && ev.type !== 'touchstart' && ev.type !== 'pointerdown') ev.preventDefault();
      return;
    }
    if (!rideau || n - rideau.t0 < 300 || rideau.vite || rideau.monte0) return;
    rideau.vite = n;
    aval = n;
    ev.stopImmediatePropagation();
    if (ev.cancelable && ev.type !== 'touchstart' && ev.type !== 'pointerdown') ev.preventDefault();
  };
  const suite = (ev: Event): void => {
    if (aval && H.maintenant() - aval < 700) {
      ev.stopImmediatePropagation();
      if (ev.cancelable) ev.preventDefault();
    }
  };
  for (const n of ['touchstart', 'pointerdown', 'mousedown'])
    document.addEventListener(n, presse, { capture: true, passive: false });
  for (const n of ['touchend', 'pointerup', 'mouseup', 'click'])
    document.addEventListener(n, suite, { capture: true, passive: false });

  return {
    poser(visible) {
      if (!visible) {
        env.hidden = true;
        return;
      }
      env.hidden = false;
      const T = h.trait();
      env.style.top = `${String(T.base + T.amp + 40 - 118)}px`;
    },
    arreter() {
      g = null;
      if (retour != null) H.annuleImage(retour);
      retour = null;
      doigt = null;
      arreteRuban();
      arreteRideau();
      instant = null;
      zone.classList.remove('ouvert', 'atteint');
      h.fi.classList.remove('tracant');
    },
    etat: () => ({
      geste: !!g,
      atteint: !!g?.atteint,
      doigt,
      avance: g ? g.xm - g.x0 : 0,
      ruban: !!ruban,
      rideau: rideau ? { t0: rideau.t0, v: rideau.v, monte: !!rideau.monte0 } : null,
      instant,
      dernier,
    }),
  };
}
