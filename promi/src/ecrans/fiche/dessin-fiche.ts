/**
 * LE DESSIN SUR LA FICHE (lot 3b-5 ; le prototype : `bande()` et l'œil de lot-V132-DESSIN, C-042, C-051, C-085, C-086).
 *
 * LA BANDE : le dessin posé REMPLACE la dalle ou la photo — une couche pleine (son fond, puis ses traits, à l'échelle 1, calés EN HAUT) posée sur la
 * bande, découpée à 7 pt au-dessus de l'axe du trait d'état : la bande montre UNE chose. Rien n'est relu ni retouché dans le canevas de la bande :
 * retirer le dessin rend la dalle.
 * L'ŒIL (le masquage, pour soi seul — jamais emporté dans un partage) : un rond de 34 pt au coin bas gauche de la bande (x 24, 52 pt au-dessus du
 * trait), son fond celui du dessin (masqué : la couleur de la nature), son encre la plus lisible des deux ; jamais pendant l'instant.
 */
import { palette } from '../../design/jetons.ts';
import { el } from '../commun.ts';
import { cheminOnde, type Onde } from '../page-plus/onde.ts';
import { DESSIN, dessinEntier, dessinPose, type Dessin } from '../page-plus/dessin.ts';

const W = 390;
const OEIL = { x: 24, ecart: 52 } as const;
const TXT = { masquer: 'Masquer le dessin', afficher: 'Afficher le dessin' } as const;
const SVG_OEIL =
  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 12S6 5.8 12 5.8 21.5 12 21.5 12 18 18.2 12 18.2 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="2.6"/></svg>';
const SVG_OEIL_NON =
  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 12S6 5.8 12 5.8 21.5 12 21.5 12 18 18.2 12 18.2 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="2.6"/><path d="M4 20L20 4"/></svg>';

const lumi = (h: string): number => {
  const c = h.replace('#', '');
  const r = parseInt(c.slice(0, 2), 16) || 0;
  const g = parseInt(c.slice(2, 4), 16) || 0;
  const b = parseInt(c.slice(4, 6), 16) || 0;
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};

/** le dessin que la bande montre : posé et non masqué */
export function dessinVu(d: Dessin | null): boolean {
  return dessinPose(d) && !d!.masque;
}

export interface BandeDessin {
  /** repose la couche et l'œil (la fiche, son onde, sa nature) ; rien d'autre que ce qui change */
  poser(o: { d: Dessin | null; y: Onde; nature: string; instant: boolean; masquer: () => void }): void;
  retirer(): void;
}

export function monterBandeDessin(hote: HTMLElement, apres: HTMLElement): BandeDessin {
  let cv: HTMLCanvasElement | null = null;
  let oeil: HTMLButtonElement | null = null;
  let masquer: () => void = () => undefined;

  function retirer(): void {
    cv?.remove();
    cv = null;
    oeil?.remove();
    oeil = null;
  }

  function poser(o: { d: Dessin | null; y: Onde; nature: string; instant: boolean; masquer: () => void }): void {
    masquer = o.masquer;
    const d = o.d;
    // l'œil : seulement quand un dessin est posé (masqué ou non), jamais pendant l'instant
    if (dessinPose(d) && !o.instant) {
      if (!oeil) {
        oeil = el('button', { type: 'button', class: 'dz-oeil' });
        oeil.addEventListener('click', (ev) => {
          ev.stopPropagation();
          ev.preventDefault();
          masquer();
        });
        hote.appendChild(oeil);
      }
      const m = !!d!.masque;
      const yo = o.y(OEIL.x + 17) - OEIL.ecart;
      const fd = m ? o.nature : d!.fond;
      const etat = `${m ? '1' : '0'}|${String(Math.round(yo * 10))}|${fd}`;
      if (oeil.dataset['etat'] !== etat) {
        oeil.dataset['etat'] = etat;
        oeil.innerHTML = m ? SVG_OEIL_NON : SVG_OEIL;
        oeil.setAttribute('aria-label', m ? TXT.afficher : TXT.masquer);
        oeil.setAttribute('aria-pressed', m ? 'true' : 'false');
        oeil.style.left = `${String(OEIL.x)}px`;
        oeil.style.top = `${String(yo)}px`;
        oeil.style.setProperty('--dz-oeil-fond', fd);
        oeil.style.setProperty('--dz-oeil-encre', lumi(fd) > 128 ? palette.brun09 : palette.creme95);
      }
    } else {
      oeil?.remove();
      oeil = null;
    }
    // la couche : le dessin posé et vu, jamais pendant l'instant
    if (!d || !dessinVu(d) || o.instant) {
      cv?.remove();
      cv = null;
      return;
    }
    const dpr = Math.max(2, Math.min(3, window.devicePixelRatio || 2));
    let bas = 0;
    for (let x = 0; x <= W; x += 6) bas = Math.max(bas, o.y(x));
    bas = Math.ceil(Math.min(bas, d.h));
    if (!cv) {
      cv = el('canvas', { class: 'dz-bande', 'aria-hidden': 'true' });
      apres.after(cv);
    }
    const sig = [JSON.stringify(d.poses).length, d.fond, d.h, o.y(0), o.y(130), o.y(260), o.y(390), dpr]
      .map(String)
      .join('|');
    if (cv.dataset['sig'] === sig) return;
    cv.dataset['sig'] = sig;
    cv.width = Math.round(W * dpr);
    cv.height = Math.round(bas * dpr);
    cv.style.width = `${String(W)}px`;
    cv.style.height = `${String(bas)}px`;
    const g = cv.getContext('2d')!;
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.clearRect(0, 0, W, bas);
    g.save();
    g.beginPath();
    cheminOnde(g, (x) => o.y(x) - DESSIN.BANDE_RETRAIT, 0, W, W);
    g.lineTo(W, 0);
    g.lineTo(0, 0);
    g.closePath();
    g.clip();
    g.setTransform(1, 0, 0, 1, 0, 0);
    // 1:1, calé en haut : la fiche en montre le haut
    g.drawImage(dessinEntier(d, dpr), 0, 0);
    g.restore();
  }

  return { poser, retirer };
}
