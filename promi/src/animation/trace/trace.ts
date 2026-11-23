/**
 * LE TRACÉ DES LETTRES (C-125, C-279 : le seul langage pour tracer et détracer) — le module repris du prototype, derrière une interface
 * typée. Le module (src/animation/repris/trace-lettres.js et ses trois tables de chemins) est une copie octet pour octet ; il prend son
 * temps de l'horloge unique (installée à sa place, src/animation/horloge.ts).
 * L0 : le chargement et l'interface. Le premier écran qui trace (lot 2, la page +) s'en sert.
 */
import { horloge } from '../horloge.ts';
import traceSource from '../repris/trace-lettres.js?raw';
import cheminsGilbert from '../repris/trace-chemins-gilbert.js?raw';
import cheminsAtkinson from '../repris/trace-chemins-atkinson.js?raw';
import cheminsPromiLate from '../repris/trace-chemins-promilate.js?raw';

export interface Segment {
  t: string;
  couleur?: string;
  police?: string;
  classe?: string;
  style?: string;
}

export interface OptionsTrace {
  cps?: number;
  vitesse?: number;
  inverse?: boolean;
  preparer?: boolean;
  arme?: boolean;
  /** rappel de fin (le module : `surFin`) ; interrompu si `stop()` l'a coupé */
  surFin?: (r: { interrompu: boolean }) => void;
}

export interface ControleTrace {
  stop(): void;
  lance?(): void;
  accelere?(k: number): void;
  /** la lettre en cours, la part du texte réel déjà montrée, le total, les lettres en cours, le temps de plume */
  etat(): { glyphe: number; texteReel: number; total: number; actives: number[]; t: number };
}

export interface TraceLettres {
  trace(cible: HTMLElement, contenu: null | string | Segment[], options?: OptionsTrace): ControleTrace;
  actif(): boolean;
}

let charge: TraceLettres | null = null;

function injecter(src: string, nom: string): void {
  const s = document.createElement('script');
  s.text = src + '\n//# sourceURL=' + nom;
  document.head.appendChild(s);
}

export function chargerTrace(): TraceLettres {
  if (charge) return charge;
  injecter(cheminsGilbert, 'trace-chemins-gilbert.js');
  injecter(cheminsAtkinson, 'trace-chemins-atkinson.js');
  injecter(cheminsPromiLate, 'trace-chemins-promilate.js');
  injecter(traceSource, 'trace-lettres.js');
  const t = (window as unknown as { TraceLettres?: TraceLettres }).TraceLettres;
  if (!t) throw new Error("tracé : le module n'a pas été posé");
  charge = t;
  return t;
}

/**
 * C-279, C-271 — UN TEXTE QUI CHANGE SE DÉTRACE, PUIS LE NOUVEAU SE TRACE (le prototype : `_douceur.valeur` → détracé puis tracé, les valeurs
 * de Peaufiner, v203) : le même module, la même cadence. « Réduire les animations » : le texte change d'un coup.
 */
export function changerTexte(el: HTMLElement, ancien: string, neuf: string): void {
  let reduit = false;
  try {
    reduit = matchMedia('(prefers-reduced-motion: reduce)').matches;
  } catch {
    reduit = false;
  }
  if (reduit || ancien === neuf || !ancien) {
    el.textContent = neuf;
    return;
  }
  const t = chargerTrace();
  el.textContent = ancien;
  t.trace(el, null, {
    inverse: true,
    surFin: () => {
      if (!el.isConnected) return;
      el.textContent = neuf;
      t.trace(el, null);
    },
  });
}

function reduitMouvement(): boolean {
  try {
    return matchMedia('(prefers-reduced-motion: reduce)').matches;
  } catch {
    return false;
  }
}
/**
 * une copie d'un élément posée exactement à sa place, au-dessus, sans prendre le doigt (le prototype : `copieA`, lot-V203-RETOUR) — le texte
 * seul : ni bordure ni fond ; l'épaisseur de la bordure passe en marge intérieure (le texte reste au même pixel)
 */
export function copieA(el: HTMLElement): HTMLElement {
  const g = el.cloneNode(true) as HTMLElement;
  const r = el.getBoundingClientRect();
  const cs = getComputedStyle(el);
  g.removeAttribute('id');
  g.setAttribute('aria-hidden', 'true');
  g.classList.add('trace-copie');
  const pad = (['Top', 'Right', 'Bottom', 'Left'] as const)
    .map(
      (s) =>
        `${String((parseFloat(cs.getPropertyValue(`padding-${s.toLowerCase()}`)) || 0) + (parseFloat(cs.getPropertyValue(`border-${s.toLowerCase()}-width`)) || 0))}px`,
    )
    .join(' ');
  const hote = (el.offsetParent as HTMLElement | null) ?? (el.parentNode as HTMLElement);
  hote.appendChild(g);
  const H = hote.getBoundingClientRect();
  const k = (hote.offsetWidth ? H.width / hote.offsetWidth : 1) || 1;
  const d: [string, string][] = [
    ['position', 'absolute'],
    ['margin', '0'],
    ['pointer-events', 'none'],
    ['z-index', '9'],
    ['box-sizing', 'border-box'],
    ['display', 'block'],
    ['white-space', 'nowrap'],
    ['width', `${String(r.width / k)}px`],
    ['height', `${String(r.height / k)}px`],
    ['left', `${String((r.left - H.left) / k - hote.clientLeft)}px`],
    ['top', `${String((r.top - H.top) / k - hote.clientTop)}px`],
    ['transform', 'none'],
    ['background', 'transparent'],
    ['border', '0'],
    ['padding', pad],
    ['outline', '0'],
    ['box-shadow', 'none'],
    ['transition', 'none'],
    ['animation', 'none'],
  ];
  for (const [p, v] of d) g.style.setProperty(p, v, 'important');
  return g;
}
/**
 * C-271 — UN TEXTE REMPLACÉ PAR UN AUTRE À LA MÊME PLACE (« + ajouter quelqu’un » ↔ la ligne de saisie, v203 clôture §2) : l'ancien, copié à sa
 * place, se détrace ; le neuf se trace. « Réduire les animations », ou rien à l'écran : le changement se fait d'un coup.
 */
export function remplacer(el: HTMLElement, applique: () => void): void {
  if (reduitMouvement() || !el.isConnected || !el.getClientRects().length) {
    applique();
    return;
  }
  const t = chargerTrace();
  const g = copieA(el);
  const fin = (): void => {
    g.remove();
  };
  applique();
  t.trace(el, null);
  t.trace(g, null, { inverse: true, surFin: fin });
  horloge().minuteur(fin, 2500);
}
/** un texte qui part par le tracé : sa copie, à sa place, se détrace (l'original est déjà parti) */
export function detracerCopie(el: HTMLElement): void {
  if (reduitMouvement() || !el.isConnected || !el.getClientRects().length) return;
  const g = copieA(el);
  const fin = (): void => {
    g.remove();
  };
  chargerTrace().trace(g, null, { inverse: true, surFin: fin });
  horloge().minuteur(fin, 2500);
}
