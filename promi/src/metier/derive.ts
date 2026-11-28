/**
 * LA ROTATION DE LA PELOTE (v210, C-302 ; v207, C-298) — un seul mouvement : la vitesse angulaire ω = vitesse × axe, l'axe dans le repère de la vue
 * (x : l'inclinaison `tan`, y : le tour `lac`, z : le roulis du calque). L'axe passe d'une orientation à la suivante par un slerp lissé (départ et
 * arrivée à vitesse nulle), en 8 à 18 s ; la cible est tirée à 30–80° de l'axe du moment (jamais une inversion), sa part d'inclinaison rappelée vers le
 * centre ; la vitesse varie doucement entre 0,85 et 1,15 × celle de C-298 (un tour en 66,7 s). Le prototype : `Derive` de lot-AURA-PELOTE — la même
 * loi, le même ordre des tirages (tests/unitaires/derive.test.ts rejoue `_peloteDerive.simule` du prototype, valeurs en dur).
 */

/** un tour en 100 / 1,5 = 66,7 s (v207, C-298 ; 100 s depuis le 12 sept.) */
export const TOUR_S = 100 / 1.5;
/** la vitesse de la rotation lente, en rad/s */
export const AUTO = 6.283185307 / TOUR_S;
/** la borne de l'inclinaison de la vue */
export const TANGMAX = 1.15;

export type Vec3 = [number, number, number];

export interface PasDerive {
  tan: number;
  lac: number;
  roll: number;
  ax: Vec3;
  w: number;
}

export interface Derive {
  readonly ax: Vec3;
  readonly f: number;
  pas(dt: number, tan: number): PasDerive;
}

export const borne = (t: number): number => Math.max(-TANGMAX, Math.min(TANGMAX, t));

function norme(v: readonly number[]): Vec3 {
  const n = Math.hypot(v[0]!, v[1]!, v[2]!) || 1;
  return [v[0]! / n, v[1]! / n, v[2]! / n];
}
function angle(a: Vec3, b: Vec3): number {
  return Math.acos(Math.max(-1, Math.min(1, a[0] * b[0] + a[1] * b[1] + a[2] * b[2])));
}
function slerp(a: Vec3, b: Vec3, u: number): Vec3 {
  const o = angle(a, b);
  if (o < 1e-6) return [a[0], a[1], a[2]];
  const s = Math.sin(o);
  const p = Math.sin((1 - u) * o) / s;
  const q = Math.sin(u * o) / s;
  return norme([a[0] * p + b[0] * q, a[1] * p + b[1] * q, a[2] * p + b[2] * q]);
}

/** la dérive de l'axe ; `al` : le hasard dans [0, 1), appelé dans l'ordre du prototype */
export function creerDerive(al: () => number): Derive {
  let ax: Vec3 = [0, 0.82, 0.57];
  let de: Vec3 = ax;
  let vers: Vec3 | null = null;
  let t = 0;
  let dur = 1;
  let f = 1;
  let fDe = 1;
  let fVers = 1;
  const cible = (tan: number): Vec3 => {
    for (let k = 0; k < 60; k++) {
      const z = al() * 2 - 1;
      const th = al() * 6.283185307;
      const r = Math.sqrt(1 - z * z);
      let v: Vec3 = [r * Math.cos(th), r * Math.sin(th), z];
      // l'inclinaison, rappelée vers le centre
      v[0] = Math.max(-0.45, Math.min(0.45, v[0] * 0.45 - (0.55 * (tan || 0)) / TANGMAX));
      v = norme(v);
      const o = angle(v, ax);
      if (o > 0.52 && o < 1.4) return v;
    }
    return norme([(-(tan || 0) / TANGMAX) * 0.3, ax[1] + 0.3, ax[2] - 0.3]);
  };
  const suivante = (tan: number): void => {
    de = [ax[0], ax[1], ax[2]];
    vers = cible(tan);
    t = 0;
    dur = 8 + al() * 10;
    fDe = f;
    fVers = 0.85 + al() * 0.3;
  };
  return {
    get ax() {
      return ax;
    },
    get f() {
      return f;
    },
    pas(dt, tan) {
      if (!vers || t >= dur) suivante(tan);
      t = Math.min(dur, t + dt);
      const u = t / dur;
      const e = u * u * (3 - 2 * u);
      ax = slerp(de, vers!, e);
      f = fDe + (fVers - fDe) * e;
      const w = AUTO * f;
      let wx = w * ax[0];
      // à l'approche de la borne d'inclinaison, la part qui l'y pousse s'efface en douceur (jamais l'arrêt sec de `borne`)
      const tb = Math.abs(tan || 0) / TANGMAX;
      if (tb > 0.6 && wx * (tan || 0) > 0) wx *= Math.max(0, 1 - Math.pow((tb - 0.6) / 0.4, 2));
      return { tan: wx, lac: w * ax[1], roll: w * ax[2], ax: [ax[0], ax[1], ax[2]], w };
    },
  };
}

/** le hasard d'une graine (celui de `_peloteDerive.simule`) */
export function hasardGraine(graine: number): () => number {
  let a = graine >>> 0 || 12345;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** la même loi rejouée `sec` secondes (le juge) : [tan', lac', roll', tan] à chaque pas */
export function simuleDerive(sec: number, dt = 1 / 60, graine = 12345): number[][] {
  const D = creerDerive(hasardGraine(graine));
  let tan = 0.32;
  const L: number[][] = [];
  for (let t = 0; t < sec; t += dt) {
    const W = D.pas(dt, tan);
    tan = borne(tan + W.tan * dt);
    L.push([+W.tan.toFixed(7), +W.lac.toFixed(7), +W.roll.toFixed(7), +tan.toFixed(5)]);
  }
  return L;
}
