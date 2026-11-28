/**
 * LES GESTES DE LA PELOTE (lot 6 ; le prototype : `gestesBoule`, `doigt`, `empSuit`, `lacher` de lot-AURA-PELOTE) — les acquis de la sphère :
 *  · la prise au doigt dans tous les sens (la vue suit la main : 0,011 rad par px sur une boule de 142, rapporté à 116 pt) ;
 *  · l'élan qui S'ADDITIONNE à la rotation lente (pas de reprise, donc pas de saccade) — sa fenêtre suit la cadence réelle (chantier 73), la vitesse
 *    se prend sur la DURÉE des mouvements, à l'heure de chaque événement (regroupés compris) ;
 *  · le toucher qui creuse (v139, C-083 : q(t) = 1 − 1/(1 + t/0,60)², la forme du contact lue sur le toucher), qui revient lentement au lâcher ;
 *  · la trace qui se forme SOUS le doigt (v142) : à chaque mouvement, un segment du point précédent au point touché, large du contact en travers
 *    du geste, couché d'autant plus que le doigt traîne ou appuie (v143) ; inscrite après l'image (pelote.ts, `FILE`) ;
 *  · un appui immobile laisse la forme du contact ; le double toucher relisse.
 * L'état vivant (la vue, l'empreinte, les traces) appartient à pelote.ts ; ce module le lit et l'écrit par `AccesPelote`.
 */
import { horloge } from '../../animation/horloge.ts';
import { borne } from '../../metier/derive.ts';
import { BO, R_BOULE, type VuePelote } from './pelote.ts';

/** la boule à l'écran, en pt (116) */
const RPT = BO.d * R_BOULE;
export const GG = {
  SENS: (0.011 * 142) / RPT,
  TAU: 0.55,
  VMAX: 11,
  TAP: 6,
  PROF: 0.46,
  ENF_TAU: 0.6,
  DOIGT_K: 1,
  A_MIN: 0.035,
  A_MAX: 0.6,
  W: 0.27,
  DOUBLE: 350,
  TRACES: 160,
} as const;
/** la pulpe, en points — sans capteur : le pouce */
const POUCE = [46.4, 0.7] as const;

export type Vec = [number, number, number];
export interface Trace {
  a: Vec;
  d: Vec;
  L: number;
  w: number;
  f: number;
  m?: Vec;
  vif?: number;
  appui?: number;
  et?: number;
}
export interface Empreinte {
  c: Vec;
  ax: Vec;
  a: number;
  el: number;
  el0: number;
  dmax: number;
  p: number;
  q: number;
  t0: number;
  /** 0 : le doigt est posé ; sinon l'heure du lâcher */
  tr: number;
  pRel: number;
  qRel: number;
  comble: number;
  lx: number | null;
  ly: number | null;
  gl: number;
  rx: number;
  ry: number;
  rot: number;
  tp: number;
}

export interface AccesPelote {
  vue: VuePelote;
  /** l'empreinte du doigt (le creux), ou rien */
  emp: Empreinte | null;
  /** un doigt est posé */
  prise: boolean;
  /** les segments qui attendent d'être inscrits après l'image */
  file: Trace[];
  /** les traces posées (pour l'appui immobile, inscrit tout de suite) */
  poser(t: Trace): void;
  relisser(): void;
  /** l'angle du roulis du calque, en degrés */
  roulis(): number;
  /** le roulis arrêté (le geste reprend la main) */
  arreterRoulis(): void;
}

const nrm = (v: readonly number[]): Vec => {
  const m = Math.sqrt(v[0]! * v[0]! + v[1]! * v[1]! + v[2]! * v[2]!) || 1;
  return [v[0]! / m, v[1]! / m, v[2]! / m];
};
const angle = (a: Vec, b: Vec): number => Math.acos(Math.max(-1, Math.min(1, a[0] * b[0] + a[1] * b[1] + a[2] * b[2])));
function arc(a0: Vec, b0: Vec): Trace {
  const a = nrm(a0);
  const b = nrm(b0);
  const d = a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  return { a, d: nrm([b[0] - d * a[0], b[1] - d * a[1], b[2] - d * a[2]]), L: angle(a, b), w: GG.W, f: 0.9 };
}

export function brancherGestes(prise: HTMLElement, cv: HTMLCanvasElement, dv: HTMLElement, P: AccesPelote): void {
  const echelle = (): number => {
    const r = dv.getBoundingClientRect();
    return r.width ? r.width / 390 : 1;
  };
  /** le point de la VUE sous le doigt (x à droite, y en bas, z vers nous), ou rien — ramené dans le repère du calque qui roule */
  function surBoule(cx: number, cy: number): Vec | null {
    const r = cv.getBoundingClientRect();
    if (!r.width) return null;
    const Wc = (cv.offsetWidth || r.width) * echelle();
    const R = Wc * R_BOULE;
    const x0 = (cx - (r.left + r.width / 2)) / R;
    const y0 = (cy - (r.top + r.height / 2)) / R;
    const th = (-P.roulis() * Math.PI) / 180;
    const x = x0 * Math.cos(th) - y0 * Math.sin(th);
    const y = x0 * Math.sin(th) + y0 * Math.cos(th);
    const q = x * x + y * y;
    return q >= 1 ? null : [x, y, Math.sqrt(1 - q)];
  }
  function versObjet(v: Vec): Vec {
    const V = P.vue;
    const cl = Math.cos(V.lac);
    const sl = Math.sin(V.lac);
    const ct = Math.cos(V.tan);
    const st = Math.sin(V.tan);
    const zp = -v[1] * st + v[2] * ct;
    const y = v[1] * ct + v[2] * st;
    return [v[0] * cl - zp * sl, y, v[0] * sl + zp * cl];
  }
  // la forme du contact : le toucher (Safari : `radiusX`, `radiusY`, `rotationAngle`) quand il est là, sinon le pointeur, sinon le pouce
  const TCH = { rx: 0, ry: 0, rot: 0, t: 0, f: 0 };
  function lisTouche(ev: TouchEvent): void {
    const t = ev.touches[0] as (Touch & { webkitForce?: number }) | undefined;
    if (!t) return;
    const rx = +(t.radiusX || 0);
    const ry = +(t.radiusY || 0);
    if (!(rx > 1 && ry > 1)) {
      TCH.t = 0;
      return;
    }
    TCH.rx = rx;
    TCH.ry = ry;
    TCH.rot = +(t.rotationAngle || 0) || 0;
    TCH.t = horloge().maintenant();
    TCH.f = +(t.force || t.webkitForce || 0) || 0;
  }
  function doigt(e: PointerEvent | null): {
    a: number;
    el: number;
    dmax: number;
    ax: Vec;
    capteur: boolean;
    rx: number;
    ry: number;
    rot: number;
  } {
    let a = POUCE[0] / 2.2 / RPT;
    let elp: number = POUCE[1];
    let ax: Vec = [0.62, -0.72, 0];
    let cap = false;
    const s = echelle();
    let rx = 0;
    let ry = 0;
    let rot: number | null = null;
    if (TCH.t && horloge().maintenant() - TCH.t < 400) {
      rx = TCH.rx / s;
      ry = TCH.ry / s;
      rot = (TCH.rot * Math.PI) / 180;
      if (ry > rx) {
        [rx, ry] = [ry, rx];
        rot += Math.PI / 2;
      }
      cap = true;
    } else if (e?.pointerType === 'touch' && e.width > 4 && e.height > 4) {
      rx = Math.max(e.width, e.height) / 2 / s;
      ry = Math.min(e.width, e.height) / 2 / s;
      if (e.height > e.width * 1.08) rot = Math.PI / 2;
      else if (e.width > e.height * 1.08) rot = 0;
      cap = true;
    }
    if (cap) {
      a = Math.max(GG.A_MIN, Math.min(GG.A_MAX, (GG.DOIGT_K * rx) / RPT));
      elp = Math.max(0.5, Math.min(1, ry / rx));
      if (rot != null && elp < 0.93) ax = [Math.cos(rot), Math.sin(rot), 0];
    }
    return { a, el: elp, dmax: GG.PROF * a, ax, capteur: cap, rx, ry, rot: rot ?? 0 };
  }
  /** le contact (en pt) ; sans capteur, la pulpe du pouce */
  function contactRayons(): [number, number, number] {
    let rx = P.emp?.rx ?? 0;
    let ry = P.emp?.ry ?? 0;
    if (!(rx > 0 && ry > 0)) {
      rx = POUCE[0] / 2.2;
      ry = rx * POUCE[1];
    }
    return [rx, ry, P.emp?.rot ?? 0];
  }
  /** de combien les poils se couchent (v143) : la lenteur du doigt et l'appui (la force si elle VARIE, sinon la taille du contact), 0,25 à 1 */
  function intensite(vit: number | null, duree?: number): number {
    const c = contactRayons();
    const ap = Math.max(TCH.f > 0.02 && TCH.f < 0.98 ? TCH.f : 0, Math.max(0, Math.min(1, (c[0] - 7) / 9)));
    const lent =
      vit == null
        ? Math.max(0, Math.min(1, ((duree ?? 0) - 200) / 1000))
        : Math.max(0, Math.min(1, 1 - (vit - 60) / 440));
    return Math.max(0.25, Math.min(1, 0.25 + 0.45 * lent + 0.3 * ap));
  }
  /** le rayon du contact EN TRAVERS d'un geste (dx, dy à l'écran), en radians sur la boule ; jamais moins d'un point */
  function contactTravers(dx: number, dy: number): number {
    const c = contactRayons();
    const m = Math.sqrt(dx * dx + dy * dy) || 1;
    const nx = -dy / m;
    const ny = dx / m;
    const ca = Math.cos(c[2]);
    const sa = Math.sin(c[2]);
    const u = nx * ca + ny * sa;
    const w = -nx * sa + ny * ca;
    return Math.max(1, Math.sqrt(c[0] * c[0] * u * u + c[1] * c[1] * w * w)) / RPT;
  }
  /** un appui immobile laisse la forme du contact, à sa taille réelle (v142) */
  function poseContact(): void {
    const E = P.emp;
    if (!E) return;
    const c = contactRayons();
    const o0 = versObjet(E.c);
    const demi = Math.max(0.5, c[0] - c[1]) / RPT;
    const ax = E.ax;
    let t = nrm([ax[0], ax[1], 0]);
    if (!(c[0] > c[1] * 1.05)) t = [1, 0, 0];
    const p1 = nrm([E.c[0] - t[0] * demi, E.c[1] - t[1] * demi, E.c[2]]);
    const p2 = nrm([E.c[0] + t[0] * demi, E.c[1] + t[1] * demi, E.c[2]]);
    const g = arc(versObjet(p1), versObjet(p2));
    g.w = Math.max(1, c[1]) / RPT;
    g.vif = DG.geste;
    g.m = o0;
    g.appui = 1;
    g.f = intensite(null, E.tp ? horloge().maintenant() - E.tp : 600);
    P.poser(g);
  }
  /** l'empreinte suit le doigt posé : sa taille et son allongement (lissés), son orientation (le sens où il glisse), le poil qui traîne */
  function empSuit(e: PointerEvent, v: Vec): void {
    const E = P.emp;
    if (!E || E.tr !== 0) return;
    const f = doigt(e);
    const k = 0.35;
    if (f.capteur) {
      E.a += (f.a - E.a) * k;
      E.el0 += (f.el - E.el0) * k;
      E.dmax = GG.PROF * E.a;
      E.rx = f.rx;
      E.ry = f.ry;
      E.rot = f.rot;
    }
    const dx = e.clientX - (E.lx ?? e.clientX);
    const dy = e.clientY - (E.ly ?? e.clientY);
    const m = Math.sqrt(dx * dx + dy * dy);
    if (m > 1.5) {
      const s = echelle();
      const R0 = 14 * s;
      const v3 = surBoule(e.clientX + (dx / m) * R0, e.clientY + (dy / m) * R0);
      if (v3) {
        const t = nrm([v3[0] - v[0], v3[1] - v[1], v3[2] - v[2]]);
        const a0 = E.ax;
        const q = 0.45;
        E.ax = nrm([a0[0] + (t[0] - a0[0]) * q, a0[1] + (t[1] - a0[1]) * q, a0[2] + (t[2] - a0[2]) * q]);
      }
      E.lx = e.clientX;
      E.ly = e.clientY;
      E.gl = Math.min(1, E.gl + m / (40 * s));
    } else E.gl = Math.max(0, E.gl - 0.08);
    E.el = Math.max(0.5, E.el0 * (1 - 0.28 * E.gl));
  }

  const DG = {
    x: 0,
    y: 0,
    parc: 0,
    hT: new Float64Array(16),
    hL: new Float64Array(16),
    hG: new Float64Array(16),
    hD: new Float64Array(16),
    tPrev: 0,
    hi: 0,
    hn: 0,
    tap: 0,
    geste: 0,
    vifs: 0,
    oPrec: null as Vec | null,
    ePrec: null as { x: number; y: number; t: number } | null,
  };

  prise.addEventListener('touchstart', lisTouche, { passive: true });
  prise.addEventListener('touchmove', lisTouche, { passive: true });
  prise.addEventListener('pointerdown', (e) => {
    P.arreterRoulis();
    P.prise = true;
    try {
      prise.setPointerCapture(e.pointerId);
    } catch {
      /* le pointeur ne se capture pas : rien */
    }
    DG.x = e.clientX;
    DG.y = e.clientY;
    DG.parc = 0;
    DG.hn = 0;
    DG.hi = 0;
    DG.tPrev = e.timeStamp || horloge().maintenant();
    const V = P.vue;
    V.vlac = 0;
    V.vtan = 0;
    V.tau = GG.TAU;
    V.rampe = null;
    const v = surBoule(e.clientX, e.clientY);
    if (v) {
      const f = doigt(e);
      // un rappui au même endroit repart de la profondeur en cours (v139)
      let q0 = 0;
      const E0 = P.emp;
      if (E0 && E0.q > 0 && E0.comble < 1e-6) {
        const c0 = E0.c;
        if (Math.hypot(v[0] - c0[0], v[1] - c0[1], v[2] - c0[2]) < E0.a * 0.6) q0 = Math.min(0.98, E0.q);
      }
      const n = horloge().maintenant();
      P.emp = {
        c: v,
        ax: f.ax,
        a: f.a,
        el: f.el,
        el0: f.el,
        dmax: f.dmax,
        p: Math.pow(q0, 1.5),
        q: q0,
        t0: n - 1000 * GG.ENF_TAU * (1 / Math.sqrt(1 - q0) - 1),
        tr: 0,
        pRel: 0,
        qRel: 0,
        comble: 0,
        lx: e.clientX,
        ly: e.clientY,
        gl: 0,
        rx: f.rx,
        ry: f.ry,
        rot: f.rot,
        tp: n,
      };
    }
    DG.geste++;
    DG.vifs = 0;
    DG.oPrec = null;
    DG.ePrec = null;
    e.preventDefault();
  });
  prise.addEventListener('pointermove', (e) => {
    if (!P.prise) return;
    // l'heure de l'ÉVÉNEMENT, et chacun des événements REGROUPÉS : sur une image lente, l'élan n'est jamais perdu
    let L = e.getCoalescedEvents?.() ?? [];
    if (!L.length) L = [e];
    const s = echelle();
    const V = P.vue;
    for (const ce of L) {
      const dx0 = (ce.clientX - DG.x) / s;
      const dy0 = (ce.clientY - DG.y) / s;
      const thR = (-P.roulis() * Math.PI) / 180;
      const dx = dx0 * Math.cos(thR) - dy0 * Math.sin(thR);
      const dy = dx0 * Math.sin(thR) + dy0 * Math.cos(thR);
      DG.x = ce.clientX;
      DG.y = ce.clientY;
      DG.parc += Math.sqrt(dx * dx + dy * dy);
      V.lac += dx * GG.SENS;
      V.tan = borne(V.tan - dy * GG.SENS);
      const te = ce.timeStamp || e.timeStamp || horloge().maintenant();
      DG.hT[DG.hi] = te;
      DG.hD[DG.hi] = Math.max(1, te - (DG.tPrev || te));
      DG.tPrev = te;
      DG.hL[DG.hi] = dx * GG.SENS;
      DG.hG[DG.hi] = -dy * GG.SENS;
      DG.hi = (DG.hi + 1) % 16;
      if (DG.hn < 16) DG.hn++;
    }
    const v = surBoule(e.clientX, e.clientY);
    const E = P.emp;
    // la trace sous le doigt : un segment du point précédent au point touché, dès 0,035 rad, large du contact en travers du geste (v142)
    if (v && E && E.tr === 0) {
      const oc = versObjet(v);
      const t = e.timeStamp || horloge().maintenant();
      if (!DG.oPrec || !DG.ePrec) {
        DG.oPrec = oc;
        DG.ePrec = { x: e.clientX, y: e.clientY, t };
      } else if (angle(DG.oPrec, oc) >= 0.035) {
        const g = arc(DG.oPrec, oc);
        g.w = contactTravers(e.clientX - DG.ePrec.x, e.clientY - DG.ePrec.y);
        g.vif = DG.geste;
        const dt = Math.max(1, t - (DG.ePrec.t || 0));
        const ds = Math.hypot(e.clientX - DG.ePrec.x, e.clientY - DG.ePrec.y) / echelle();
        g.f = intensite(DG.ePrec.t ? (ds / dt) * 1000 : 300);
        g.m = nrm([DG.oPrec[0] + oc[0], DG.oPrec[1] + oc[1], DG.oPrec[2] + oc[2]]);
        P.file.push(g);
        DG.vifs++;
        DG.oPrec = oc;
        DG.ePrec = { x: e.clientX, y: e.clientY, t };
      }
    }
    if (v && E && E.tr === 0) {
      E.c = v;
      empSuit(e, v);
    }
    e.preventDefault();
  });
  function lacher(e: PointerEvent): void {
    if (!P.prise) return;
    P.prise = false;
    const now = e.timeStamp || horloge().maintenant();
    const E = P.emp;
    if (E && E.tr === 0) {
      E.pRel = E.p;
      E.qRel = E.q;
      E.tr = horloge().maintenant();
    }
    if (DG.parc <= GG.TAP) {
      // un toucher : le double toucher relisse ; un appui immobile laisse la forme du contact
      if (e.type === 'pointerup' && now - DG.tap < GG.DOUBLE) {
        P.relisser();
        DG.tap = 0;
      } else {
        DG.tap = now;
        if (!DG.vifs) poseContact();
      }
      return;
    }
    DG.tap = 0;
    // CHANTIER 73 : la fenêtre de l'élan suit la cadence réelle — un doigt qui s'arrête avant de lâcher ne lance pas
    const der = DG.hn ? DG.hT[(DG.hi - 1 + 16) % 16]! : now;
    const ec: number[] = [];
    for (let jj = 1; jj < DG.hn && jj < 5; jj++) {
      const ta = DG.hT[(DG.hi - jj + 16) % 16]!;
      const tb = DG.hT[(DG.hi - jj - 1 + 16) % 16]!;
      if (ta > tb) ec.push(ta - tb);
    }
    ec.sort((x, y) => x - y);
    const cad = ec.length ? ec[ec.length >> 1]! : 16;
    const FEN = Math.max(90, 3 * cad);
    let sl = 0;
    let st = 0;
    let dt = 0;
    if (now - der <= FEN)
      for (let i = 0; i < DG.hn; i++) {
        const j = (DG.hi - 1 - i + 32) % 16;
        if (der - DG.hT[j]! > FEN) break;
        sl += DG.hL[j]!;
        st += DG.hG[j]!;
        dt += DG.hD[j]!;
      }
    const dtt = dt / 1000;
    const V = P.vue;
    if (dtt > 0.012) {
      V.vlac = Math.max(-GG.VMAX, Math.min(GG.VMAX, sl / dtt));
      V.vtan = Math.max(-GG.VMAX, Math.min(GG.VMAX, st / dtt));
    }
  }
  prise.addEventListener('pointerup', lacher);
  prise.addEventListener('pointercancel', lacher);
}
