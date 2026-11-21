/**
 * LE PASSAGE EN FLAQUES (v148, C-141, C-271) — la seule façon dont une chose paraît ou s'en va, partout dans l'app. Porté de
 * `_passageFlaques` (lot-V147-TRANSITIONS du prototype), même algorithme, mêmes paramètres ; la scène est celle du module repris
 * (`Flaques.Scene` : 12 à 20 germes, naissances étalées, ponts, bord ondulé) ; le temps est celui de l'horloge unique.
 *
 *   mode 'ouvre'  : le canevas couvre d'abord `rect` (une couleur, ou une image) ; des trous y naissent en flaques jusqu'à ne plus rien laisser ;
 *   mode 'couvre' : la couleur ou l'image naît en flaques par-dessus ce qui est là, jusqu'à tout couvrir.
 * `rect` : [x, y, l, h] en pt de l'hôte. `image` : un canevas aux cotes de l'hôte (sa largeur en pt × densité), lu à `rect`.
 */
import { horloge } from '../horloge.ts';
import { chargerFlaques } from './flaques.ts';

export interface OptionsPassage {
  mode: 'ouvre' | 'couvre';
  rect?: [number, number, number, number];
  couleur?: string;
  image?: HTMLCanvasElement;
  duree?: number;
  lent?: number;
  graine?: number;
  devant?: boolean;
  z?: number;
  garde?: boolean;
  attend?: boolean;
  avance?: number;
  fin?: (c: ControlePassage) => void;
}

export interface ControlePassage {
  canevas: HTMLCanvasElement;
  arrete: boolean;
  duree: number;
  mode: 'ouvre' | 'couvre';
  image(t: number): void;
  lance?: () => void;
  /** arrête le passage et retire ce qu'il a posé (le masque de `masqueFlaques`) */
  stop?: () => void;
}

interface SceneFlaques {
  couvre(u: number): void;
  peint(): void;
}

function reduit(): boolean {
  try {
    return matchMedia('(prefers-reduced-motion: reduce)').matches;
  } catch {
    return false;
  }
}

export function passageFlaques(hote: HTMLElement, o: OptionsPassage): ControlePassage {
  const F = chargerFlaques() as unknown as {
    Scene: (cv: HTMLCanvasElement, opts: Record<string, unknown>) => SceneFlaques;
  };
  const h0 = horloge();
  const W0 = hote.offsetWidth || 390;
  const H0 = hote.offsetHeight || 844;
  const r = o.rect ?? [0, 0, W0, H0];
  const [x, y] = r;
  const l = Math.max(1, Math.round(r[2]));
  const h = Math.max(1, Math.round(r[3]));
  const Hb = hote.getBoundingClientRect();
  const kk = Hb.width / W0 || 1;
  const dens = Math.max(2, Math.min(3, (window.devicePixelRatio || 1) * kk));
  const cv = document.createElement('canvas');
  cv.className = 'passage-flaques';
  cv.setAttribute('aria-hidden', 'true');
  const styles: Array<[string, string]> = [
    ['position', 'absolute'],
    ['left', String(x) + 'px'],
    ['top', String(y) + 'px'],
    ['width', String(l) + 'px'],
    ['height', String(h) + 'px'],
    ['margin', '0'],
    ['padding', '0'],
    ['max-width', 'none'],
    ['pointer-events', 'none'],
    ['display', 'block'],
    ['visibility', 'visible'],
    ['opacity', '1'],
    ['transform', 'none'],
    ['filter', 'none'],
  ];
  if (o.z != null) styles.push(['z-index', String(o.z)]);
  for (const [k, v] of styles) cv.style.setProperty(k, v, 'important');
  if (o.devant) hote.appendChild(cv);
  else hote.insertBefore(cv, hote.firstChild);
  // la couverture : une couleur, ou l'image découpée à `rect`
  const couv = document.createElement('canvas');
  couv.width = Math.round(l * dens);
  couv.height = Math.round(h * dens);
  const gc = couv.getContext('2d')!;
  if (o.image) {
    const im = o.image;
    const ex = (im.width || W0) / W0;
    gc.drawImage(im, x * ex, y * ex, l * ex, h * ex, 0, 0, couv.width, couv.height);
  } else {
    gc.fillStyle = o.couleur ?? '#000';
    gc.fillRect(0, 0, couv.width, couv.height);
  }
  const graine = ((o.graine ?? Date.now()) & 0xffffff) | 1;
  const ouvre = o.mode !== 'couvre';
  // 'couvre' : la scène peint la couverture DANS l'eau ; 'ouvre' : l'eau est un masque (noir), retiré de la couverture
  const masque = ouvre ? document.createElement('canvas') : cv;
  const SC = F.Scene(
    masque,
    ouvre ? { l, h, densite: dens, aplat: '#000', graine } : { l, h, densite: dens, flou: couv, graine },
  );
  if (ouvre) {
    cv.width = masque.width;
    cv.height = masque.height;
  }
  const g = cv.getContext('2d')!;
  const dur = (o.duree ?? 1100) * (o.lent ?? 1);
  cv.setAttribute('data-mode', ouvre ? 'ouvre' : 'couvre');
  const ctl: ControlePassage = {
    canevas: cv,
    arrete: false,
    duree: dur,
    mode: ouvre ? 'ouvre' : 'couvre',
    image(t: number) {
      const u = Math.max(0, Math.min(1, t / dur));
      SC.couvre(u);
      SC.peint();
      cv.setAttribute('data-u', u.toFixed(3));
      if (ouvre) {
        g.setTransform(1, 0, 0, 1, 0, 0);
        g.globalCompositeOperation = 'source-over';
        g.clearRect(0, 0, cv.width, cv.height);
        if (u < 1) {
          g.drawImage(couv, 0, 0, cv.width, cv.height);
          g.globalCompositeOperation = 'destination-out';
          g.drawImage(masque, 0, 0);
          g.globalCompositeOperation = 'source-over';
        }
      }
    },
  };
  const fini = (): void => {
    if (ouvre && !o.garde && cv.parentNode) cv.remove();
    o.fin?.(ctl);
  };
  const av = o.avance ?? 0;
  const go = (): void => {
    if (reduit()) {
      ctl.image(dur);
      fini();
      return;
    }
    const t0 = h0.maintenant() - av;
    const pas = (): void => {
      if (ctl.arrete) return;
      const t = h0.maintenant() - t0;
      ctl.image(t);
      if (t < dur) h0.image(pas);
      else fini();
    };
    pas();
  };
  ctl.image(av);
  if (o.attend) {
    ctl.lance = go;
    return ctl;
  }
  h0.image(() => {
    go();
  });
  return ctl;
}

/**
 * UNE CHOSE DE L'ÉCRAN PARAÎT OU PART EN FLAQUES, PAR SON PROPRE MASQUE (C-329) — la même scène que `passageFlaques` (le module repris,
 * mêmes germes, mêmes naissances, mêmes ponts), mais l'eau n'est plus une couverture peinte par-dessus : elle est le MASQUE de la chose
 * (`mask-image`). « ouvre » : la chose paraît là où l'eau est née ; « couvre » : elle s'efface là où l'eau naît. Ainsi rien de ce qui est
 * dessous n'est recopié (redteam_decoupe : jamais un morceau de Toile hors du moteur) et la Toile reste vivante sous la chose.
 * Le masque est posé EN LIGNE sans `important` ; la chose porte `data-flaques-mode` et `data-flaques-u` le temps du passage (les tests).
 */
export function masqueFlaques(
  cible: HTMLElement,
  o: { mode: 'ouvre' | 'couvre'; duree?: number; graine?: number; fin?: (c: ControlePassage) => void },
): ControlePassage {
  const F = chargerFlaques() as unknown as {
    Scene: (cv: HTMLCanvasElement, opts: Record<string, unknown>) => SceneFlaques;
  };
  const h0 = horloge();
  const l = Math.max(1, Math.round(cible.offsetWidth));
  const h = Math.max(1, Math.round(cible.offsetHeight));
  const kk = cible.getBoundingClientRect().width / (cible.offsetWidth || 1) || 1;
  const dens = Math.max(1, Math.min(2, (window.devicePixelRatio || 1) * kk));
  const eau = document.createElement('canvas');
  const SC = F.Scene(eau, { l, h, densite: dens, aplat: '#000', graine: ((o.graine ?? Date.now()) & 0xffffff) | 1 });
  const ouvre = o.mode !== 'couvre';
  const m = document.createElement('canvas');
  m.width = eau.width;
  m.height = eau.height;
  const g = m.getContext('2d')!;
  const dur = o.duree ?? 300;
  const pose = (url: string): void => {
    for (const p of ['-webkit-mask-image', 'mask-image']) cible.style.setProperty(p, url);
    for (const [p, v] of [
      ['-webkit-mask-size', '100% 100%'],
      ['mask-size', '100% 100%'],
      ['-webkit-mask-repeat', 'no-repeat'],
      ['mask-repeat', 'no-repeat'],
    ])
      cible.style.setProperty(p!, v!);
  };
  const retire = (): void => {
    for (const p of [
      '-webkit-mask-image',
      'mask-image',
      '-webkit-mask-size',
      'mask-size',
      '-webkit-mask-repeat',
      'mask-repeat',
    ])
      cible.style.removeProperty(p);
    delete cible.dataset['flaquesMode'];
    delete cible.dataset['flaquesU'];
  };
  cible.dataset['flaquesMode'] = ouvre ? 'ouvre' : 'couvre';
  const ctl: ControlePassage = {
    canevas: m,
    arrete: false,
    duree: dur,
    mode: ouvre ? 'ouvre' : 'couvre',
    image(t: number) {
      const u = Math.max(0, Math.min(1, t / dur));
      SC.couvre(u);
      SC.peint();
      g.setTransform(1, 0, 0, 1, 0, 0);
      g.globalCompositeOperation = 'source-over';
      g.clearRect(0, 0, m.width, m.height);
      if (ouvre) g.drawImage(eau, 0, 0);
      else {
        g.fillStyle = '#000';
        g.fillRect(0, 0, m.width, m.height);
        g.globalCompositeOperation = 'destination-out';
        g.drawImage(eau, 0, 0);
        g.globalCompositeOperation = 'source-over';
      }
      cible.dataset['flaquesU'] = u.toFixed(3);
      pose(`url(${m.toDataURL()})`);
    },
  };
  const arrete = (): void => {
    ctl.arrete = true;
    retire();
  };
  ctl.stop = arrete;
  const fini = (): void => {
    o.fin?.(ctl);
    retire();
  };
  if (reduit()) {
    h0.image(() => {
      fini();
    });
    return ctl;
  }
  ctl.image(0);
  h0.image(() => {
    const t0 = h0.maintenant();
    const pas = (): void => {
      if (ctl.arrete) return;
      const t = h0.maintenant() - t0;
      ctl.image(t);
      if (t < dur) h0.image(pas);
      else fini();
    };
    pas();
  });
  return ctl;
}
