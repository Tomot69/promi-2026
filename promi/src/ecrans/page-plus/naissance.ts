/**
 * LA NAISSANCE D'UNE DALLE ET SON VOL (C-237, C-241, Q611 ; le prototype : `lot-V180-NAISSANCE`, `_planteNait`, `_naissanceDalle`,
 * `_fondVivant`, `_atterrit`) — la chorégraphie de l'onboarding, mêmes temps :
 *   t 0       la dalle de la parole (la MÊME image que le haut de la page +, la dalle d'avance du moteur, C-241) naît au milieu du trait, à
 *             l'échelle 0,08, et grandit à 0,85 en 0,5 s (cubic-bezier(.2,1.3,.4,1)) ; le moteur a reçu la parole : sa cellule grandit dessous ;
 *   553 ms    la Toile VIVANTE (recopiée à chaque image, la place de la nouvelle dalle laissée vide — une seule dalle à l'écran, celle qui vole)
 *             couvre la page + en flaques (620 ms) ; la page se ferme dessous, d'un coup ;
 *   808 ms    la dalle vole vers la place où la Toile vivante la pose (765 ms, cubic-bezier(.45,0,.2,1)), relue à mi-vol et rejointe en 200 ms ;
 *   1 615 ms  posée (et cette image peinte), tout ce qui couvrait part dans la même image : la Toile vivante, sa dalle à sa place.
 * La place vide est remplie de la Toile d'avant (son image au moment du trait) : la dalle n'y paraît pas deux fois.
 * « Réduire les animations » : rien ne vole, la page se ferme.
 */
import type { Facade } from '../../moteur/facade.ts';
import type { Horloge } from '../../animation/horloge.ts';
import { masqueFlaques } from '../../animation/flaques/passage.ts';

export interface OptionsNaissance {
  dv: HTMLElement;
  facade: Facade;
  h: Horloge;
  id: number;
  /** la dalle d'avance (déjà rendue, à la taille de la naissance) */
  pre: HTMLCanvasElement;
  /** le point du trait où elle naît, en pt de l'appareil */
  bx: number;
  by: number;
  /** sa largeur de naissance (241 pt : celle de l'onboarding) */
  w: number;
  /** la page + se ferme, d'un coup (sous la Toile qui la couvre) */
  fermer: () => void;
  fin: () => void;
}

const bezier =
  (x1: number, y1: number, x2: number, y2: number) =>
  (u: number): number => {
    let lo = 0;
    let hi = 1;
    let t = u;
    for (let i = 0; i < 22; i++) {
      t = (lo + hi) / 2;
      const x = 3 * t * (1 - t) * (1 - t) * x1 + 3 * t * t * (1 - t) * x2 + t * t * t;
      if (x < u) lo = t;
      else hi = t;
    }
    return 3 * t * (1 - t) * (1 - t) * y1 + 3 * t * t * (1 - t) * y2 + t * t * t;
  };
const VOL = bezier(0.45, 0, 0.2, 1);

export function planteNait(o: OptionsNaissance): void {
  const { dv, facade, h } = o;
  const D = dv.getBoundingClientRect();
  const s = D.width / (dv.offsetWidth || 390) || 1;
  const W = dv.offsetWidth || 390;
  const H = dv.offsetHeight || 844;
  const dens = Math.max(2, Math.min(3, (window.devicePixelRatio || 1) * s));
  const tc = facade.toileCanevas();
  // la Toile d'avant (son image au moment du trait) : elle remplit la place vide de la nouvelle dalle
  const avant = document.createElement('canvas');
  avant.width = Math.round(W * dens);
  avant.height = Math.round(H * dens);
  const copie = (g: CanvasRenderingContext2D): void => {
    if (!tc) return;
    const R = tc.getBoundingClientRect();
    g.drawImage(
      tc,
      ((R.left - D.left) / s) * dens,
      ((R.top - D.top) / s) * dens,
      (R.width / s) * dens,
      (R.height / s) * dens,
    );
  };
  copie(avant.getContext('2d')!);

  const hote = document.createElement('div');
  hote.id = 'ppNait';
  hote.className = 'couvre';
  hote.setAttribute('aria-hidden', 'true');
  hote.style.cssText =
    'position:absolute;inset:0;margin:0;padding:0;border:0;z-index:2147482000;pointer-events:none;overflow:hidden';
  const fond = document.createElement('canvas');
  fond.width = avant.width;
  fond.height = avant.height;
  fond.style.cssText = `position:absolute;left:0;top:0;width:${String(W)}px;height:${String(H)}px;margin:0;padding:0;visibility:hidden`;
  hote.appendChild(fond);

  // la dalle qui naît : la dalle d'avance, copiée 1:1
  const dc = document.createElement('canvas');
  dc.width = o.pre.width;
  dc.height = o.pre.height;
  dc.getContext('2d')!.drawImage(o.pre, 0, 0);
  const w = o.w;
  const hh = w * (dc.height / (dc.width || 1));
  dc.style.cssText =
    `position:absolute;margin:0;padding:0;pointer-events:none;transform-origin:50% 50%;left:${String(o.bx - w / 2)}px;` +
    `top:${String(o.by - hh / 2)}px;width:${String(w)}px;height:${String(hh)}px;transform:scale(.08);` +
    'transition:transform .5s cubic-bezier(.2,1.3,.4,1)';
  hote.appendChild(dc);
  dv.appendChild(hote);

  let fini = false;
  let coupe = false;
  let vivante = false;
  let volFini = false;
  const ferme = (): void => {
    if (coupe) return;
    coupe = true;
    o.fermer();
  };
  const termine = (): void => {
    if (fini) return;
    fini = true;
    vivante = false;
    ferme();
    hote.remove();
    o.fin();
  };
  const reduit = ((): boolean => {
    try {
      return matchMedia('(prefers-reduced-motion: reduce)').matches;
    } catch {
      return false;
    }
  })();
  if (reduit) {
    termine();
    return;
  }
  h.image(() => {
    h.image(() => {
      dc.style.transform = 'scale(.85)';
    });
  });

  // la Toile vivante, recopiée à chaque image, la place de la nouvelle dalle laissée vide (remplie de la Toile d'avant)
  const gf = fond.getContext('2d')!;
  const maj = (): void => {
    if (!vivante) return;
    gf.setTransform(1, 0, 0, 1, 0, 0);
    gf.globalCompositeOperation = 'source-over';
    gf.clearRect(0, 0, fond.width, fond.height);
    copie(gf);
    const r = facade.placeDalle(o.id);
    if (r) {
      const mx = r.x * dens;
      const my = r.y * dens;
      const mw = r.w * dens;
      const mh = r.h * dens;
      gf.globalCompositeOperation = 'destination-out';
      gf.drawImage(r.cv, mx, my, mw, mh);
      gf.globalCompositeOperation = 'destination-over';
      gf.drawImage(avant, 0, 0);
      gf.globalCompositeOperation = 'source-over';
    }
    h.image(maj);
  };

  h.minuteur(() => {
    if (fini) return;
    vivante = true;
    maj();
    fond.style.visibility = 'visible';
    masqueFlaques(fond, {
      mode: 'ouvre',
      duree: 620,
      fin: () => {
        ferme();
      },
    });
  }, 553);

  h.minuteur(() => {
    if (fini) return;
    const c0 = facade.placeDalle(o.id);
    if (!c0) return;
    const m = /matrix\(([^,]+)/.exec(getComputedStyle(dc).transform || '');
    const s0 = m ? parseFloat(m[1]!) : 0.85;
    const x0c = o.bx;
    const y0c = o.by;
    dc.style.transition = 'none';
    let cible: { x: number; y: number; w: number; h: number } = c0;
    let suivante: typeof cible | null = null;
    let tSuiv = 0;
    const t0 = h.maintenant();
    const pas = (): void => {
      if (!dc.parentNode) return;
      const t = h.maintenant();
      const u = Math.min(1, (t - t0) / 765);
      const e = VOL(u);
      // à mi-vol la place où la Toile vivante pose la dalle est relue, puis rejointe en 200 ms
      if (!suivante && u >= 0.5) {
        suivante = facade.placeDalle(o.id) ?? cible;
        tSuiv = t;
      }
      let c = cible;
      if (suivante) {
        let k = Math.min(1, (t - tSuiv) / 200);
        k = k * k * (3 - 2 * k);
        const a = cible;
        const b = suivante;
        c = { x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k, w: a.w + (b.w - a.w) * k, h: a.h + (b.h - a.h) * k };
        if (k >= 1) {
          cible = b;
          suivante = b;
        }
      }
      const sc = c.w / w;
      const cx = x0c + (c.x + c.w / 2 - x0c) * e;
      const cy = y0c + (c.y + c.h / 2 - y0c) * e;
      const ss = s0 + (sc - s0) * e;
      dc.style.left = `${String(cx - w / 2)}px`;
      dc.style.top = `${String(cy - hh / 2)}px`;
      dc.style.transform = `scale(${ss.toFixed(5)})`;
      if (u >= 1)
        h.image(() => {
          volFini = true;
        });
      else h.image(pas);
    };
    pas();
  }, 808);

  // l'atterrissage : posée (et cette image peinte, 300 ms au plus d'attente), tout part dans la même image
  h.minuteur(() => {
    const t0 = h.maintenant();
    const attend = (): void => {
      if (fini) return;
      if (!volFini && h.maintenant() - t0 < 300) {
        h.image(attend);
        return;
      }
      h.image(termine);
    };
    ferme();
    attend();
  }, 1615);
  h.minuteur(termine, 4000);
}
