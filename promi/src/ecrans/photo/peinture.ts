/**
 * LA PHOTO DANS LA BANDE (le prototype : `_photoPeint` de lot-PHOTO ; v139 C-085, v141 C-098) — commune à la fiche et à la page + : la photo
 * REMPLACE la dalle (la même boîte, en couverture : recadrée au centre), bornée par l'onde ; cadrée au doigt (`photoCadre` = {z, dx, dy, a, n}),
 * elle se dessine entière, à z fois sa taille de couverture, décalée de (dx, dy), tournée de a — `n`, la longueur de l'adresse de la photo : une
 * autre photo repart de zéro.
 */
import { cheminOnde, type Onde } from '../page-plus/onde.ts';

const images = new Map<string, HTMLImageElement>();
/** une image déjà chargée (l'import vient de la lire) */
export function imagePhotoCache(src: string, im: HTMLImageElement): void {
  images.set(src, im);
}

/** l'image d'une photo, chargée une fois ; `quand` : elle vient d'arriver (repeindre) */
export function imagePhoto(src: string, quand: () => void): HTMLImageElement | null {
  let im = images.get(src);
  if (!im) {
    im = new Image();
    im.onload = quand;
    im.src = src;
    images.set(src, im);
  }
  return im.complete && im.naturalWidth ? im : null;
}

/** `_photoPeint` : dans la boîte de la dalle, en couverture (ou cadrée), découpée au chemin de l'onde — rien ne dépasse en bas */
export function peindrePhoto(
  g: CanvasRenderingContext2D,
  im: HTMLImageElement,
  b: { x: number; y: number; w: number; h: number },
  y: Onde,
  W: number,
  cadre: unknown,
  n: number,
): void {
  g.save();
  g.beginPath();
  cheminOnde(g, y, 0, W, W);
  g.lineTo(W, 0);
  g.lineTo(0, 0);
  g.closePath();
  g.clip();
  const iw = im.naturalWidth;
  const ih = im.naturalHeight;
  const pc = cadre as { z?: number; dx?: number; dy?: number; a?: number; n?: number } | null;
  if (pc && pc.n === n && typeof pc.z === 'number') {
    const s1 = Math.max(b.w / iw, b.h / ih) * pc.z;
    const dw = iw * s1;
    const dh = ih * s1;
    const cx = b.x + b.w / 2 + (pc.dx ?? 0);
    const cy = b.y + b.h / 2 + (pc.dy ?? 0);
    if (pc.a) {
      g.translate(cx, cy);
      g.rotate(pc.a);
      g.drawImage(im, -dw / 2, -dh / 2, dw, dh);
    } else g.drawImage(im, cx - dw / 2, cy - dh / 2, dw, dh);
  } else {
    const r = iw / ih;
    const br = b.w / b.h;
    let sw: number, sh: number, sx: number, sy: number;
    if (r > br) {
      sh = ih;
      sw = ih * br;
      sx = (iw - sw) / 2;
      sy = 0;
    } else {
      sw = iw;
      sh = iw / br;
      sx = 0;
      sy = (ih - sh) / 2;
    }
    g.drawImage(im, sx, sy, sw, sh, b.x, b.y, b.w, b.h);
  }
  g.restore();
}
