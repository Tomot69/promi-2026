/**
 * LE TITRE MODIFIABLE (lot 3a-4 — C-280, le prototype : lot-V203-TITRE et lot-V203-TITRE-css ; C-244 pour le dépliage, lot-V181B-TEXTES).
 * Un toucher sur le titre d'une fiche : entier, il se modifie ; coupé (« … »), le premier toucher le DÉPLIE (fiche.ts) et le second le modifie
 * (C-280 corrige C-244 : le second toucher ne replie plus). Le titre lui-même devient modifiable (`contenteditable`), le curseur au point
 * touché ; 280 caractères au plus, sans retour à la ligne ni emoji. Retour, ou un toucher dehors, valide ; Échap rend l'ancien ; vidé, l'ancien
 * revient en se traçant. Aucun encart : ni contour, ni bordure, ni fond (`ti-edition`, C-280 §1) — seul le curseur clignote. Clavier ouvert,
 * la fiche glisse pour garder le curseur au-dessus de lui (une cale invisible, `#tiCale`, quand la fiche n'a pas la hauteur de glisser).
 */
import { horloge } from '../../animation/horloge.ts';
import { sansEmoji } from '../../metier/emoji.ts';

/** 280 caractères pour une parole (C-244 §5.3, `_limiteTexte`) */
export const LIMITE_TITRE = 280;

export interface HoteTitre {
  defile: HTMLElement;
  titre: HTMLElement;
  /** le titre entier de la parole ouverte (jamais l'affichage coupé) ; null : aucune */
  long(): string | null;
  /** la fiche reçoit un toucher sur son titre : ouverte, posée, ni l'instant ni le geste en cours */
  actif(): boolean;
  coupe(): boolean;
  deplie(): boolean;
  /** coupé : le premier toucher déplie (fiche.ts, le mouvement de 360 ms) */
  deplier(): void;
  /** le titre s'affiche entier tant qu'il se modifie (`_titreDeplie` du prototype, rendu à la sortie) */
  entier(on: boolean): void;
  /** pendant la frappe : ce qui suit le titre se replace (sa hauteur change) */
  recoter(): void;
  renommer(v: string): void;
  /** vidé : l'ancien titre revient en se traçant */
  retracer(): void;
}

export interface Titre {
  /** en cours de modification */
  edite(): boolean;
  /** la fiche se ferme ou Peaufiner s'ouvre : on valide (`_rangeurs`, `_s2Ouvre` du prototype) */
  sortir(valide: boolean): void;
}

export function monterTitre(h: HoteTitre): Titre {
  const ti = h.titre;
  let E: null | { avant: string; cale: boolean } = null;
  let sur: null | { x: number; y: number; t: number; id: number } = null;
  let avale = 0;

  function propre(v: string): string {
    const a = Array.from(sansEmoji(v.replace(/[\r\n]+/g, ' ')));
    return a.length > LIMITE_TITRE ? a.slice(0, LIMITE_TITRE).join('') : a.join('');
  }
  function reduit(): boolean {
    return matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  /** le curseur au point touché (`caretRangeFromPoint`), sinon à la fin */
  function curseur(x: number, y: number): void {
    const s = getSelection();
    if (!s) return;
    const c = document.caretPositionFromPoint(x, y);
    let r: Range | null = null;
    if (c && ti.contains(c.offsetNode)) {
      r = document.createRange();
      r.setStart(c.offsetNode, c.offset);
    }
    if (!r) {
      r = document.createRange();
      r.selectNodeContents(ti);
      r.collapse(false);
    } else r.collapse(true);
    s.removeAllRanges();
    s.addRange(r);
  }

  /** clavier ouvert : la fiche glisse pour garder le curseur 24 pt au-dessus du clavier, et 120 pt sous le haut (`visible()`) */
  function visible(): void {
    const vv = window.visualViewport;
    if (!E || !vv) return;
    const d = h.defile;
    let r: DOMRect | null = null;
    const s = getSelection();
    if (s?.rangeCount) {
      const q = s.getRangeAt(0).getClientRects();
      if (q.length) r = q[q.length - 1]!;
    }
    r ??= ti.getBoundingClientRect();
    const bas = vv.offsetTop + vv.height - 24;
    const haut = Math.max(vv.offsetTop, d.getBoundingClientRect().top) + 120;
    const dy =
      r.bottom > bas ? r.bottom - bas : r.top < haut && d.scrollTop > 0 ? -Math.min(d.scrollTop, haut - r.top) : 0;
    if (Math.abs(dy) < 1) return;
    const k = d.getBoundingClientRect().width / (d.offsetWidth || 390) || 1;
    const cible = d.scrollTop + dy / k;
    if (dy > 0 && cible + d.clientHeight > d.scrollHeight) {
      let c = d.querySelector<HTMLElement>('#tiCale');
      if (!c) {
        c = document.createElement('div');
        c.id = 'tiCale';
        c.setAttribute('aria-hidden', 'true');
        d.appendChild(c);
      }
      c.style.top = `${String(Math.ceil(cible + d.clientHeight + 8))}px`;
      E.cale = true;
    }
    d.scrollTo({ top: cible, behavior: reduit() ? 'auto' : 'smooth' });
  }

  function entrer(x: number, y: number): void {
    const long = h.long();
    if (long == null) return;
    E = { avant: long, cale: false };
    h.entier(true);
    if (ti.textContent !== long) ti.textContent = long;
    ti.setAttribute('contenteditable', 'plaintext-only');
    if (ti.contentEditable !== 'plaintext-only') ti.setAttribute('contenteditable', 'true');
    ti.setAttribute('spellcheck', 'false');
    ti.setAttribute('enterkeyhint', 'done');
    ti.setAttribute('autocapitalize', 'off');
    ti.setAttribute('role', 'textbox');
    ti.setAttribute('aria-label', 'Le titre');
    ti.classList.add('ti-edition');
    ti.focus({ preventScroll: true });
    curseur(x, y);
    horloge().minuteur(visible, 350);
    horloge().minuteur(visible, 700);
  }

  function sortir(valide: boolean): void {
    if (!E) return;
    const e = E;
    E = null;
    let v = propre(ti.textContent ?? '')
      .replace(/\s+/g, ' ')
      .trim();
    ti.removeAttribute('contenteditable');
    ti.removeAttribute('role');
    ti.removeAttribute('enterkeyhint');
    ti.removeAttribute('aria-label');
    ti.classList.remove('ti-edition');
    if (document.activeElement === ti) ti.blur();
    getSelection()?.removeAllRanges();
    const c = h.defile.querySelector('#tiCale');
    if (c) {
      const d = h.defile;
      if (d.scrollTop > 0) {
        d.scrollTo({ top: 0, behavior: reduit() ? 'auto' : 'smooth' });
        horloge().minuteur(() => {
          if (!E) c.remove();
        }, 700);
      } else c.remove();
    }
    const vide = !v;
    if (vide || !valide) v = e.avant;
    h.entier(false);
    if (v !== e.avant) h.renommer(v);
    else ti.textContent = v;
    h.recoter();
    if (vide && !reduit()) h.retracer();
  }

  // ── LE TOUCHER (au lever : moins de 10 pt, moins de 0,6 s) ──
  window.addEventListener(
    'pointerdown',
    (ev) => {
      const sur0 = ev.target instanceof Element && ev.target.closest('.fi-titre') === ti;
      // en modification, un toucher ailleurs valide (et fait ce qu'il fait)
      if (E && !sur0) {
        sortir(true);
        return;
      }
      sur = sur0 && !E ? { x: ev.clientX, y: ev.clientY, t: ev.timeStamp, id: ev.pointerId } : null;
    },
    true,
  );
  window.addEventListener(
    'pointerup',
    (ev) => {
      // en modification, un toucher dans le titre ne place que le curseur
      if (E && ev.target instanceof Element && ev.target.closest('.fi-titre') === ti) {
        ev.stopImmediatePropagation();
        return;
      }
      const g = sur;
      sur = null;
      if (!g || g.id !== ev.pointerId) return;
      if (Math.hypot(ev.clientX - g.x, ev.clientY - g.y) > 10 || ev.timeStamp - g.t > 600) return;
      if (!h.actif()) return;
      ev.stopImmediatePropagation();
      avale = ev.timeStamp;
      if (h.coupe() && !h.deplie()) h.deplier();
      else entrer(ev.clientX, ev.clientY);
    },
    true,
  );
  // le clic qui suit le toucher ne fait rien d'autre
  window.addEventListener(
    'click',
    (ev) => {
      if (!avale || ev.timeStamp - avale > 700) return;
      avale = 0;
      if (ev.target instanceof Element && ev.target.closest('.fi-titre') === ti) return;
      ev.stopImmediatePropagation();
      ev.preventDefault();
    },
    true,
  );
  document.addEventListener(
    'keydown',
    (ev) => {
      if (!E || ev.target !== ti) return;
      if (ev.key === 'Enter') {
        ev.preventDefault();
        sortir(true);
      } else if (ev.key === 'Escape') {
        ev.preventDefault();
        sortir(false);
      }
    },
    true,
  );
  document.addEventListener(
    'beforeinput',
    (ev) => {
      if (!E || ev.target !== ti) return;
      if (ev.inputType === 'insertParagraph' || ev.inputType === 'insertLineBreak') {
        ev.preventDefault();
        sortir(true);
      }
    },
    true,
  );
  document.addEventListener(
    'input',
    (ev) => {
      if (!E || ev.target !== ti) return;
      const t = ti.textContent ?? '';
      const p = propre(t);
      if (p !== t) {
        ti.textContent = p;
        const r = document.createRange();
        r.selectNodeContents(ti);
        r.collapse(false);
        const s = getSelection();
        s?.removeAllRanges();
        s?.addRange(r);
      }
      h.recoter();
      horloge().minuteur(visible, 0);
    },
    true,
  );
  document.addEventListener(
    'focusout',
    (ev) => {
      if (E && ev.target === ti)
        horloge().minuteur(() => {
          if (E && document.activeElement !== ti) sortir(true);
        }, 0);
    },
    true,
  );

  return { edite: () => !!E, sortir };
}
