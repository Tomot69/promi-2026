/**
 * LA FEUILLE DE CONFIRMATION ET LE BANDEAU « ANNULER » (le prototype : `conf` et `annulable` de lot-V16 ; v163b C-195, v187).
 *
 * La feuille : un titre, une phrase, « Garder » et l'action (pleine, à l'encre du mode) ; elle prend le doigt DÈS QU'ELLE EXISTE (v187 : un
 * toucher sur l'action ne passe jamais à travers, sur la fiche dessous), et pendant son arrivée (400 ms) un toucher à côté du panneau ne la
 * referme pas ; ensuite il la referme sans rien faire. Le bandeau : un mot et « Annuler », 5 s.
 * ÉCART NOMMÉ : ils paraissent et partent en FLAQUES (C-130 : jamais un fondu) ; le prototype les fondait (opacité, 0,18 s).
 */
import './feuilles.css';
import { horloge } from '../../animation/horloge.ts';
import { masqueFlaques } from '../../animation/flaques/passage.ts';
import { el, surToucher } from '../commun.ts';

const reduit = (): boolean => matchMedia('(prefers-reduced-motion: reduce)').matches;

function paraitre(e: HTMLElement): void {
  if (!reduit()) masqueFlaques(e, { mode: 'ouvre', duree: 300 });
}
function partir(e: HTMLElement): void {
  if (reduit()) {
    e.remove();
    return;
  }
  e.style.pointerEvents = 'none';
  masqueFlaques(e, {
    mode: 'couvre',
    duree: 300,
    fin: () => {
      e.remove();
    },
  });
}

export function confirmer(
  dv: HTMLElement,
  o: { titre: string; texte: string; oui: string; non: string; faire: () => void },
): void {
  dv.querySelector('#v16Conf')?.remove();
  const v = el('div', { id: 'v16Conf', class: 'v16-conf' });
  const p = el('div', { class: 'v16-conf-p', role: 'alertdialog', 'aria-modal': 'true' });
  const t = el('div', { class: 'v16-conf-t' });
  t.textContent = o.titre;
  const x = el('div', { class: 'v16-conf-x' });
  x.textContent = o.texte;
  const b = el('div', { class: 'v16-conf-b' });
  const non = el('button', { type: 'button', class: 'v16-non' });
  non.textContent = o.non;
  const oui = el('button', { type: 'button', class: 'v16-oui' });
  const ouiT = el('span');
  ouiT.textContent = o.oui;
  oui.appendChild(ouiT);
  b.append(non, oui);
  p.append(t, x, b);
  v.appendChild(p);
  const nee = horloge().maintenant();
  let fini = false;
  const ferme = (): void => {
    if (fini) return;
    fini = true;
    partir(v);
  };
  surToucher(v, (ev) => {
    if (ev.target === v && horloge().maintenant() - nee > 400) ferme();
  });
  surToucher(non, () => {
    ferme();
  });
  surToucher(oui, () => {
    if (fini) return;
    ferme();
    o.faire();
  });
  dv.appendChild(v);
  paraitre(v);
}

let minuteurBandeau: number | null = null;
export function annulable(
  dv: HTMLElement,
  o: { mot: string; annuler: string; defaire: () => void; ms?: number },
): void {
  dv.querySelector('#v16Toast')?.remove();
  const h = horloge();
  if (minuteurBandeau != null) h.annuleMinuteur(minuteurBandeau);
  const t = el('div', { id: 'v16Toast', class: 'v16-toast', role: 'status' });
  const s = el('span');
  s.textContent = o.mot;
  const b = el('button', { type: 'button' });
  b.textContent = o.annuler;
  t.append(s, b);
  let fini = false;
  const ferme = (): void => {
    if (fini) return;
    fini = true;
    if (minuteurBandeau != null) h.annuleMinuteur(minuteurBandeau);
    minuteurBandeau = null;
    partir(t);
  };
  surToucher(b, () => {
    if (fini) return;
    ferme();
    o.defaire();
  });
  dv.appendChild(t);
  paraitre(t);
  minuteurBandeau = h.minuteur(ferme, o.ms ?? 5000);
}

/**
 * LE TOAST (le prototype : `toast(msg, l1, f1, …)`, et v201 — il se découvre en arrivant, se referme en partant, `clip-path`, 220 ms) : un mot et
 * jusqu'à trois choix ; un choix touché agit puis le toast part ; seul, il part après 3,2 s (7 s s'il porte des choix). Un seul à la fois : un
 * nouveau remplace l'ancien aussitôt. Seuls ses choix prennent le doigt.
 */
let minuteurToast: number | null = null;
const EZ = 'cubic-bezier(.33,0,.67,1)';
export function toast(dv: HTMLElement, mot: string, choix: ReadonlyArray<readonly [string, () => void]> = []): void {
  const h = horloge();
  dv.querySelector('#_toast')?.remove();
  if (minuteurToast != null) h.annuleMinuteur(minuteurToast);
  const t = el('div', { id: '_toast', class: 'promi-toast', role: 'status' });
  const s = el('span');
  s.textContent = mot;
  t.appendChild(s);
  let fini = false;
  const part = (): void => {
    if (fini) return;
    fini = true;
    if (minuteurToast != null) h.annuleMinuteur(minuteurToast);
    minuteurToast = null;
    if (reduit()) {
      t.remove();
      return;
    }
    const a = t.animate([{ clipPath: 'inset(0 0 0 0 round 16px)' }, { clipPath: 'inset(50% 0 50% 0 round 16px)' }], {
      duration: 220,
      easing: EZ,
      fill: 'forwards',
    });
    a.onfinish = () => {
      t.remove();
    };
  };
  for (const [mot2, faire] of choix) {
    const b = el('button', { type: 'button' });
    b.textContent = mot2;
    surToucher(b, () => {
      if (fini) return;
      faire();
      part();
    });
    t.appendChild(b);
  }
  dv.appendChild(t);
  if (!reduit())
    t.animate([{ clipPath: 'inset(50% 0 50% 0 round 16px)' }, { clipPath: 'inset(0 0 0 0 round 16px)' }], {
      duration: 220,
      easing: EZ,
    });
  minuteurToast = h.minuteur(part, choix.length ? 7000 : 3200);
}
