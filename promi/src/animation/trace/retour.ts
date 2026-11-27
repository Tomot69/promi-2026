/**
 * LOT 4b — LA BRIQUE COMMUNE DES TEXTES QUI PARTENT ET REVIENNENT (C-271, C-279 ; le prototype : `_retour` de lot-V203-RETOUR, et le « … » du
 * focus de lot-CURSEUR). « Aucun changement sec à l'écran, nulle part » : un texte d'exemple, de remplacement ou d'origine ne paraît ni ne
 * disparaît d'un coup — il se DÉTRACE (le tracé joué à rebours, même cadence), et revient en se TRAÇANT. Un seul module, le tracé des lettres
 * (C-125) ; « Réduire les animations » : d'un coup. Une veille finit toute transition qui ne rend pas la main (C-274).
 *
 *  · `champExemple(champ)` — le texte d'exemple d'un champ (`placeholder` : la recherche de l'Index, du Fil et d'une personne, la NOTE de
 *    Peaufiner, la DESCRIPTION d'un Cercle) : il part à la première lettre (une copie posée exactement sur lui se détrace, la lettre paraît tout
 *    de suite), revient quand on efface tout (le texte natif caché le temps du tracé) ; au focus il devient « … » (l'ancien se détrace, puis le
 *    neuf se trace), et l'inverse en le quittant. La brique est le SEUL écrivain du `placeholder` du champ.
 *  · `bascule(el, montre)` — un texte posé dans la page qui part et revient (« Un mot… », « un prénom… »).
 *  · `remplacer(el, applique)` — un texte remplacé par un autre à la même place (« + ajouter quelqu’un » ↔ la ligne de saisie).
 *  · `detracerCopie(el)` — un texte qui part (sa copie, à sa place, se détrace).
 */
import { horloge } from '../horloge.ts';
import { chargerTrace } from './trace.ts';

/** le texte d'exemple d'un champ qui a la main (le curseur, lot-CURSEUR) */
export const CURSEUR = '…';

function reduitMouvement(): boolean {
  try {
    return matchMedia('(prefers-reduced-motion: reduce)').matches;
  } catch {
    return false;
  }
}
/** la durée qu'une transition a pour finir avant que la veille la finisse (le prototype : 900 + 30 par caractère, plus 1,5 s) */
function duree(t: string | null | undefined): number {
  return 900 + 30 * String(t ?? '').length;
}
/** visible : une boîte d'au moins 4 pt, aucun ancêtre caché ni transparent */
function visible(e: Element): boolean {
  const r = e.getBoundingClientRect();
  if (r.width < 4 || r.height < 4) return false;
  for (let q: Element | null = e; q; q = q.parentElement) {
    const c = getComputedStyle(q);
    if (c.display === 'none' || c.visibility === 'hidden' || +c.opacity < 0.05) return false;
  }
  return true;
}

/**
 * une copie d'un élément posée exactement à sa place, au-dessus, sans prendre le doigt (le prototype : `copieA`) — le texte seul : ni bordure ni
 * fond ; l'épaisseur de la bordure passe en marge intérieure (le texte reste au même pixel)
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

/* ── bascule : un texte de la page qui part et revient ── */
interface EtatBascule {
  montre: boolean;
  veut: boolean;
  anim: null | 'part' | 'revient';
}
const BASCULES = new WeakMap<HTMLElement, EtatBascule>();
function avance(m: HTMLElement): void {
  const st = BASCULES.get(m);
  if (!st || st.anim) return;
  if (st.veut === st.montre) {
    m.hidden = !st.montre;
    return;
  }
  if (reduitMouvement() || !m.isConnected) {
    st.montre = st.veut;
    m.hidden = !st.montre;
    return;
  }
  const vers = st.veut;
  let fini = false;
  st.anim = vers ? 'revient' : 'part';
  const f = (): void => {
    if (fini) return;
    fini = true;
    st.montre = vers;
    st.anim = null;
    avance(m);
  };
  const t = chargerTrace();
  if (vers) {
    m.hidden = false;
    if (!m.getClientRects().length) {
      f();
      return;
    }
    t.trace(m, null, { surFin: f });
    // la veille
    horloge().minuteur(
      () => {
        if (fini) return;
        t.poseTout(m);
        f();
      },
      duree(m.textContent) + 1500,
    );
  } else {
    if (!m.getClientRects().length) {
      m.hidden = true;
      f();
      return;
    }
    const g = copieA(m);
    m.hidden = true;
    const fg = (): void => {
      g.remove();
      f();
    };
    t.trace(g, null, { inverse: true, depart: 'h', surFin: fg });
    horloge().minuteur(fg, duree(g.textContent) + 1500);
  }
}
/** C-271 — un texte posé dans la page (« Un mot… », « un prénom… ») : `montre` vrai → il se trace ; faux → il se détrace, puis se cache */
export function bascule(el: HTMLElement, montre: boolean): void {
  let st = BASCULES.get(el);
  if (!st) {
    st = { montre: !el.hidden, veut: !el.hidden, anim: null };
    BASCULES.set(el, st);
  }
  st.veut = montre;
  avance(el);
}

/* ── champExemple : le texte d'exemple d'un champ ── */
/** une copie du texte d'exemple, posée EXACTEMENT sur celui du champ (sa police, sa couleur, sa place : le prototype, `fantome`) */
function fantome(inp: HTMLInputElement | HTMLTextAreaElement, txt: string): HTMLElement {
  const cs = getComputedStyle(inp);
  let ph: CSSStyleDeclaration | null = null;
  try {
    ph = getComputedStyle(inp, '::placeholder');
  } catch {
    ph = null;
  }
  const src = ph?.fontFamily ? ph : cs;
  const g = document.createElement('span');
  g.className = 'ch-fantome';
  g.setAttribute('aria-hidden', 'true');
  g.textContent = txt;
  const ta = inp.tagName === 'TEXTAREA';
  const n = (v: string): number => parseFloat(v) || 0;
  const pt = n(cs.paddingTop);
  const pb = n(cs.paddingBottom);
  const bt = n(cs.borderTopWidth);
  const bb = n(cs.borderBottomWidth);
  const pl = n(cs.paddingLeft);
  const bl = n(cs.borderLeftWidth);
  const pr = n(cs.paddingRight);
  const br = n(cs.borderRightWidth);
  const hC = inp.offsetHeight - pt - pb - bt - bb;
  const wC = inp.offsetWidth - pl - pr - bl - br;
  const col = ph?.color || cs.color;
  const d: [string, string][] = [
    ['position', 'absolute'],
    ['margin', '0'],
    ['padding', '0'],
    ['border', '0'],
    ['background', 'transparent'],
    ['box-shadow', 'none'],
    ['pointer-events', 'none'],
    ['z-index', '9'],
    ['left', '0px'],
    ['top', '0px'],
    ['overflow', 'visible'],
    ['white-space', ta ? 'pre-wrap' : 'pre'],
    ['width', `${String(wC)}px`],
    ['font-family', src.fontFamily],
    ['font-size', src.fontSize],
    ['font-weight', src.fontWeight],
    ['font-style', src.fontStyle],
    ['letter-spacing', src.letterSpacing],
    ['text-transform', src.textTransform],
    ['text-align', cs.textAlign],
    ['color', col],
    ['-webkit-text-fill-color', col],
    ['opacity', ph?.opacity || '1'],
    ['line-height', ta ? cs.lineHeight : `${String(hC)}px`],
    ['height', ta ? 'auto' : `${String(hC)}px`],
  ];
  for (const [p, v] of d) g.style.setProperty(p, v, 'important');
  inp.parentNode?.insertBefore(g, inp.nextSibling);
  const R = inp.getBoundingClientRect();
  const G = g.getBoundingClientRect();
  const sc = (inp.offsetWidth ? R.width / inp.offsetWidth : 1) || 1;
  g.style.setProperty('left', `${String((R.left + (bl + pl) * sc - G.left) / sc)}px`, 'important');
  g.style.setProperty('top', `${String((R.top + (bt + pt) * sc - G.top) / sc)}px`, 'important');
  return g;
}

export interface ChampExemple {
  /** la valeur a changé par l'app (« Revenir à tout l'Index » vide la recherche) : le texte d'exemple suit */
  etat(): void;
  /** le texte d'exemple au repos change (un autre écran, une autre langue) */
  exemple(t: string): void;
}
/** la classe qui cache le texte d'exemple natif le temps de son tracé (base.css) */
const CACHE_NATIF = 'ch-phx';

/**
 * LE TEXTE D'EXEMPLE D'UN CHAMP. `exemple` : celui du repos (« Rechercher », « ajoute un mot, un contexte… », « présente le Cercle, son but… ») ;
 * le champ focalisé montre « … » (lot-CURSEUR). La brique pose elle-même le `placeholder` et elle seule l'écrit.
 */
export function champExemple(inp: HTMLInputElement | HTMLTextAreaElement, exemple: string): ChampExemple {
  let repos = exemple;
  let vide = !inp.value;
  let anim: null | 'part' | 'revient' | 'echange' = null;
  inp.setAttribute('placeholder', document.activeElement === inp ? CURSEUR : repos);
  let montre = inp.getAttribute('placeholder') ?? '';
  const h = horloge();
  const txt = (): string => inp.getAttribute('placeholder') ?? '';
  const anime = (): boolean => !reduitMouvement() && inp.isConnected && visible(inp);

  function etat(): void {
    if (anim || !inp.isConnected) return;
    const v = !inp.value;
    if (v === vide) {
      // le texte d'exemple a changé pendant une transition : l'échange se joue après elle
      if (v && montre !== txt()) {
        const a = montre;
        montre = txt();
        echange(a, montre);
      }
      return;
    }
    vide = v;
    if (v) montre = txt();
    if (!txt() || !anime()) return;
    if (v) revient();
    else part();
  }
  function part(): void {
    const t = chargerTrace();
    const g = fantome(inp, txt());
    let fini = false;
    anim = 'part';
    const f = (): void => {
      if (fini) return;
      fini = true;
      g.remove();
      anim = null;
      etat();
    };
    t.trace(g, null, { inverse: true, depart: 'h', surFin: f });
    h.minuteur(f, duree(txt()) + 1500);
  }
  function revient(): void {
    const t = chargerTrace();
    inp.classList.add(CACHE_NATIF);
    const g = fantome(inp, txt());
    let fini = false;
    anim = 'revient';
    const f = (): void => {
      if (fini) return;
      fini = true;
      inp.classList.remove(CACHE_NATIF);
      g.remove();
      anim = null;
      etat();
    };
    t.trace(g, null, { surFin: f });
    // la veille
    h.minuteur(
      () => {
        if (fini) return;
        t.poseTout(g);
        f();
      },
      duree(txt()) + 1500,
    );
  }
  /** le texte d'exemple qui change, le champ vide (« Rechercher » ↔ « … » au focus) : l'ancien se détrace, PUIS le neuf se trace (C-271) */
  function echange(ancien: string, neuf: string): void {
    if (anim) return;
    if (inp.value || ancien === neuf || !anime()) {
      montre = txt();
      return;
    }
    montre = neuf;
    anim = 'echange';
    inp.classList.add(CACHE_NATIF);
    const t = chargerTrace();
    let fini = false;
    let go: HTMLElement | null = null;
    let gn: HTMLElement | null = null;
    const f = (): void => {
      if (fini) return;
      fini = true;
      go?.remove();
      gn?.remove();
      inp.classList.remove(CACHE_NATIF);
      anim = null;
      vide = !inp.value;
      etat();
    };
    const deux = (): void => {
      if (fini) return;
      go?.remove();
      if (!neuf || inp.value) {
        f();
        return;
      }
      gn = fantome(inp, neuf);
      t.trace(gn, null, { surFin: f });
    };
    if (ancien) {
      go = fantome(inp, ancien);
      t.trace(go, null, { inverse: true, depart: 'h', surFin: deux });
    } else deux();
    // la veille
    h.minuteur(f, duree(ancien) + duree(neuf) + 1500);
  }
  function poser(p: string): void {
    const a = txt();
    if (a === p) return;
    inp.setAttribute('placeholder', p);
    echange(a, p);
  }
  inp.addEventListener('input', etat);
  inp.addEventListener('focus', () => {
    poser(CURSEUR);
  });
  inp.addEventListener('blur', () => {
    poser(repos);
  });
  return {
    etat,
    exemple(t) {
      repos = t;
      if (document.activeElement !== inp) poser(repos);
    },
  };
}
