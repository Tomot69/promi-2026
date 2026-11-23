/**
 * UNE PLACE DE LA PHRASE QUI CHANGE NE CHANGE JAMAIS D'UN COUP (C-271, règle permanente ; C-269, C-274, C-279, C-282) — le port de
 * `lot-V200-DOUCEUR` du prototype : à chaque reconstruction de la phrase de la page +, chaque place qui change de mot passe par `mot`.
 *
 * - `mot` : l'ancien mot se DÉTRACE (le tracé de C-125 à rebours, même cadence) pendant que l'ENCART va en douceur à la largeur du neuf (la
 *   suite de la phrase glisse avec lui) ; si la place passe de vide à pleine (une personne ajoutée), le filet pointillé s'amincit jusqu'à rien
 *   pendant que la pastille se remplit EN FLAQUES (la matière du produit, bord net) — à rebours, le fond plein se retire en flaques pendant que le
 *   filet revient ; puis le neuf SE TRACE, à sa couleur finale. Les pointillés ne clignotent jamais : le tracé découpe une enveloppe du texte
 *   (`.ph-mt`), jamais l'encart. Une cible qui change pendant la transition : elle finit sur la cible du moment.
 * - `premiere` (C-282, v205–v206) : à la première lettre tapée, l'exemple part EN ENTIER en 150 ms (son opacité baisse à chaque image, la sortie
 *   amortie 1 − (1 − p)²) — EXCEPTION NOMMÉE à C-279, décidée par Tom ; la lettre tapée paraît tout de suite, posée au-dessus (la copie de
 *   l'exemple est découpée là où s'écrit le texte tapé) ; la pastille se remplit en flaques (200 ms) et l'encart va à sa largeur.
 * - La place vidée (C-274) : le texte tapé se détrace, les pointillés reviennent en flaques, l'exemple SE TRACE (`mot`).
 * - À la bascule du sens, une place qui PART se détrace à l'endroit où elle était ; une place qui ARRIVE se trace.
 * - Un nœud en transition survit aux reconstructions : il est regreffé à la place du neuf (la phrase est rebâtie à chaque lettre).
 *
 * Jamais dans les 600 ms qui suivent l'ouverture (la page se pose), ni d'une nature à l'autre (une page neuve), ni sous « Réduire les
 * animations » (le mot change d'un coup, la règle de C-125).
 */
import type { Horloge } from '../../animation/horloge.ts';
import type { TraceLettres } from '../../animation/trace/trace.ts';
import { passageFlaques } from '../../animation/flaques/passage.ts';

const COURBE = 'cubic-bezier(.33,0,.67,1)';
const D_FL = 420;
/** C-282 : la pastille se remplit en 200 ms ; l'exemple part en 150 ms */
const PREM = 200;
const FONDU = 150;
const CLES = ['qui', 'avec', 'sens', 'titre', 'nom'];

interface Cible {
  html: string;
  cls: string;
  brut?: boolean;
}
interface Etat {
  cible: Cible;
  fini: boolean;
  phase: 'detrace' | 'flaques' | 'trace' | 'premiere';
  t: number;
  trace?: Cible;
  tape?: Cible;
}
interface Avant {
  E: Record<string, { html: string; cls: string; w: number }>;
  G: Record<string, { r: DOMRect; html: string; fs: string; lh: string; style: Record<string, string> }>;
  av: Record<string, HTMLElement>;
  cle: string;
}

export interface OptionsDouceur {
  txt: HTMLElement;
  /** le conteneur de la phrase (jamais rebâti) : la copie de l'exemple qui s'efface y vit */
  hote: HTMLElement;
  h: Horloge;
  trace: () => TraceLettres | null;
  /** la page est montrée et posée (ouverte depuis 600 ms, ni cachée, ni en train de partir) */
  vivante: () => boolean;
  /** la nature : une autre est une page neuve */
  cle: () => string;
  /** un mot a changé (la fin d'une transition) : le glissement de la phrase le voit avant la peinture (le prototype, `_v203Verifie`) */
  change?: () => void;
}
export interface Douceur {
  avant(): Avant | null;
  apres(a: Avant | null): void;
  /** une place est en transition (la liaison neuve et le glissement attendent qu'elle ait fini son détracé) */
  enCours(): boolean;
  /** une transition est en cours (une place, la première lettre) : la page n'est pas posée */
  actif(): boolean;
  /** la page se ferme : les transitions s'arrêtent là */
  arrete(): void;
}

function reduit(): boolean {
  try {
    return matchMedia('(prefers-reduced-motion: reduce)').matches;
  } catch {
    return false;
  }
}
function texte(h: string): string {
  const d = document.createElement('div');
  d.innerHTML = h.replace(/<br\s*\/?>/gi, ' ');
  return (d.textContent ?? '').replace(/\s+/g, ' ').trim();
}
function net(c: string): string {
  return c
    .split(/\s+/)
    .filter((x) => x && x !== 'ph-on')
    .sort()
    .join(' ');
}
const vide = (cls: string): boolean => /(^|\s)ph-vide(\s|$)/.test(cls);
/** la largeur suit le détracé (40 car/s, 25 ms par lettre, + la durée d'une lettre) ; jamais moins de 320 ms (l'encart ne bondit pas) */
const dureeMot = (t: string): number => Math.max(320, Math.min(640, 110 + 25 * t.length));
function enveloppe(el: HTMLElement): HTMLElement {
  const deja = el.querySelector<HTMLElement>(':scope > .ph-mt, :scope > .ph-mt-pose');
  if (deja && el.childNodes.length === 1) {
    deja.className = 'ph-mt';
    return deja;
  }
  const e = document.createElement('span');
  e.className = 'ph-mt';
  e.append(...el.childNodes);
  el.appendChild(e);
  return e;
}
function contenu(e: HTMLElement): string {
  const i = e.querySelector<HTMLElement>(':scope > .ph-mt, :scope > .ph-mt-pose');
  return i && e.childNodes.length === 1 ? i.innerHTML : e.innerHTML;
}
/** la largeur et l'allure qu'aura l'encart : une copie hors du flux, au même endroit (mêmes règles), le temps d'une mesure */
function mesure(el: HTMLElement, html: string, cls: string): { w: number; bg: string; rad: string; bw: string } {
  const c = el.cloneNode(false) as HTMLElement;
  c.className = cls;
  c.innerHTML = html;
  c.removeAttribute('style');
  for (const [p, v] of [
    ['position', 'absolute'],
    ['visibility', 'hidden'],
    ['left', '0'],
    ['top', '0'],
    ['pointer-events', 'none'],
  ])
    c.style.setProperty(p!, v!, 'important');
  // la place se mesure dans la largeur de la phrase : hors du flux, une parole longue tiendrait sur une seule ligne
  const par = el.parentElement;
  if (par?.clientWidth) c.style.setProperty('max-width', `${String(par.clientWidth)}px`, 'important');
  el.parentNode!.insertBefore(c, el.nextSibling);
  const s = getComputedStyle(c);
  const r = { w: c.offsetWidth, bg: s.backgroundColor, rad: s.borderTopLeftRadius, bw: s.borderTopWidth };
  c.remove();
  return r;
}
const visible = (el: HTMLElement): boolean => {
  const r = el.getBoundingClientRect();
  return el.isConnected && r.width > 0 && r.height > 0;
};
const PROPS = [
  'width',
  'box-sizing',
  'transition',
  'border-width',
  'border-style',
  'border-color',
  'background-color',
  'position',
  'isolation',
  'justify-content',
];
function nettoie(el: HTMLElement): void {
  for (const p of PROPS) el.style.removeProperty(p);
}

export function creerDouceur(o: OptionsDouceur): Douceur {
  const { txt, hote, h } = o;
  const ET = new WeakMap<HTMLElement, Etat>();
  const enTransition = new Set<HTMLElement>();
  /** les places qui arrivent à la bascule du sens, le temps de leur tracé */
  const arrivees = new Set<HTMLElement>();
  /** les encarts qui finissent d'aller à leur largeur naturelle (200 ms) */
  const lisses = new Set<HTMLElement>();
  const st = (el: HTMLElement): Etat | null => {
    const s = ET.get(el);
    return s && !s.fini ? s : null;
  };
  const finir = (el: HTMLElement, s: Etat): void => {
    s.fini = true;
    ET.delete(el);
    enTransition.delete(el);
  };
  function pose(el: HTMLElement, c: Cible): void {
    const on = el.classList.contains('ph-on');
    el.className = c.cls;
    el.classList.toggle('ph-on', on);
    el.innerHTML = c.html;
    o.change?.();
  }

  // ── LE MOT D'UNE PLACE ──
  function mot(el: HTMLElement, cible: Cible, w0d?: number): void {
    const enCours = st(el);
    if (enCours) {
      enCours.cible = cible;
      return;
    }
    const html0 = contenu(el);
    const cls0 = el.className;
    if (texte(html0) === texte(cible.html) && net(cls0) === net(cible.cls)) {
      if (cible.html !== html0) pose(el, cible);
      return;
    }
    const tl = o.trace();
    if (reduit() || !tl || !visible(el)) {
      pose(el, cible);
      return;
    }
    const s: Etat = { cible, fini: false, phase: 'detrace', t: h.maintenant() };
    ET.set(el, s);
    enTransition.add(el);
    const w0 = w0d && w0d > 0 ? w0d : el.offsetWidth;
    const m = mesure(el, cible.html, cible.cls);
    el.style.setProperty('box-sizing', 'border-box', 'important');
    el.style.setProperty('width', `${String(w0)}px`, 'important');
    el.style.setProperty('justify-content', 'flex-start', 'important');
    el.getBoundingClientRect();
    el.style.setProperty(
      'transition',
      `width ${String(dureeMot(texte(html0)))}ms ${COURBE}, border-width ${String(D_FL)}ms ${COURBE}`,
      'important',
    );
    el.style.setProperty('width', `${String(m.w)}px`, 'important');
    const env = enveloppe(el);
    const horsPage = (): boolean => {
      if (el.isConnected) return false;
      finir(el, s);
      return true;
    };
    // une transition ne reste jamais en route (v203, le relevé de l'iPhone : une transition ouverte 30 s) : une veille relance l'étape
    const veille = (): void => {
      h.minuteur(() => {
        if (s.fini || ET.get(el) !== s || horsPage()) return;
        const age = h.maintenant() - s.t;
        if (age > (s.phase === 'flaques' ? 1500 : 2500)) {
          s.t = h.maintenant();
          if (s.phase === 'detrace') suite();
          else trace(s.cible);
        }
        veille();
      }, 300);
    };
    veille();
    const suite = (): void => {
      if (s.fini || horsPage()) return;
      s.t = h.maintenant();
      const c = s.cible;
      const v0 = el.classList.contains('ph-vide');
      const v1 = vide(c.cls);
      const m2 = mesure(el, c.html, c.cls);
      el.style.setProperty('width', `${String(m2.w)}px`, 'important');
      if (v0 !== v1) {
        s.phase = 'flaques';
        flaques(el, v1, m2, () => {
          trace(s.cible);
        });
      } else trace(c);
    };
    const trace = (c: Cible): void => {
      if (s.fini || horsPage()) return;
      s.t = h.maintenant();
      s.phase = 'trace';
      s.trace = c;
      el.querySelector(':scope > canvas.passage-flaques')?.remove();
      for (const p of ['background-color', 'border-style', 'border-color', 'position', 'isolation'])
        el.style.removeProperty(p);
      const on = el.classList.contains('ph-on');
      el.className = c.cls;
      el.classList.toggle('ph-on', on);
      if (c.brut) {
        el.innerHTML = c.html;
        fin();
        return;
      }
      const env2 = enveloppe(el);
      env2.innerHTML = c.html;
      o.change?.();
      tl.trace(env2, null, {
        surFin: () => {
          fin();
        },
      });
    };
    const fin = (): void => {
      if (s.fini) return;
      const c = s.cible;
      const t = s.trace!;
      if (texte(c.html) !== texte(t.html) || net(c.cls) !== net(t.cls)) {
        // la cible a changé pendant le tracé : on repart d'ici, sans saut
        finir(el, s);
        mot(el, c);
        return;
      }
      finir(el, s);
      const env3 = el.querySelector<HTMLElement>(':scope > .ph-mt');
      if (env3) {
        env3.style.removeProperty('clip-path');
        env3.style.removeProperty('-webkit-clip-path');
        // dans la pastille d'un prénom, l'enveloppe RESTE jusqu'à la prochaine composition : le visage et le texte y sont serrés, ce que le
        // prototype montre (`.v200-mt`) ; ailleurs elle part — le prototype recompose la phrase à la fin de la transition (le ⇄ du verbe
        // reprend sa place, un exemple coupé ses deux lignes)
        if (el.classList.contains('ph-avec-visage')) env3.className = 'ph-mt-pose';
        else env3.replaceWith(...env3.childNodes);
      }
      o.change?.();
      const wc = el.offsetWidth;
      el.style.removeProperty('transition');
      el.style.removeProperty('width');
      const wn = el.offsetWidth;
      if (Math.abs(wn - wc) > 0.5) {
        el.style.setProperty('width', `${String(wc)}px`, 'important');
        el.getBoundingClientRect();
        el.style.setProperty('transition', `width 200ms ${COURBE}`, 'important');
        el.style.setProperty('width', `${String(wn)}px`, 'important');
        lisses.add(el);
        h.minuteur(() => {
          lisses.delete(el);
          if (!ET.get(el)) nettoie(el);
        }, 220);
      } else nettoie(el);
    };
    if (!env.textContent?.trim()) suite();
    else
      tl.trace(env, null, {
        inverse: true,
        surFin: () => {
          suite();
        },
      });
  }

  /** les pointillés qui partent (ou reviennent) : le filet s'amincit pendant que la pastille se remplit en flaques — ou l'inverse */
  function flaques(
    el: HTMLElement,
    versVide: boolean,
    m: { bg: string; rad: string; bw: string },
    puis: () => void,
  ): void {
    const bgPlein = versVide ? getComputedStyle(el).backgroundColor : m.bg;
    el.style.setProperty('position', 'relative', 'important');
    el.style.setProperty('isolation', 'isolate', 'important');
    el.style.setProperty('background-color', 'transparent', 'important');
    if (versVide) {
      el.style.setProperty('border-width', '0px', 'important');
      el.classList.add('ph-vide');
      el.getBoundingClientRect();
      el.style.setProperty('border-width', m.bw, 'important');
    } else el.style.setProperty('border-width', '0px', 'important');
    let fait = false;
    const fini = (): void => {
      if (fait) return;
      fait = true;
      puis();
    };
    const ctl = passageFlaques(el, {
      mode: versVide ? 'ouvre' : 'couvre',
      couleur: bgPlein,
      duree: D_FL,
      z: -1,
      fin: () => {
        if (versVide) el.querySelector(':scope > canvas.passage-flaques')?.remove();
        fini();
      },
    });
    for (const [p, v] of [
      ['left', '0'],
      ['top', '0'],
      ['width', '100%'],
      ['height', '100%'],
      ['border-radius', m.rad],
    ])
      ctl.canevas.style.setProperty(p!, v!, 'important');
    h.minuteur(fini, D_FL + 1500);
  }

  // ── C-282 : LA PREMIÈRE LETTRE ──
  function premiere(
    el: HTMLElement,
    a: { html: string; cls: string; w: number },
    g: Avant['G'][string] | undefined,
    c: Cible,
  ): void {
    const tl = o.trace();
    if (reduit() || !tl || !visible(el) || !g) return;
    const s: Etat = { cible: { ...c, brut: true }, tape: { ...c }, fini: false, phase: 'premiere', t: h.maintenant() };
    ET.set(el, s);
    enTransition.add(el);
    // la copie de l'exemple : son texte seul, à sa place, au-dessus — dans le conteneur de la phrase (la phrase est rebâtie à chaque lettre)
    const wr = document.createElement('span');
    wr.className = 'pp-ex-part';
    wr.setAttribute('aria-hidden', 'true');
    const gh = document.createElement('span');
    gh.innerHTML = texte(a.html).replace(/&/g, '&amp;').replace(/</g, '&lt;');
    for (const [p, v] of Object.entries(g.style)) gh.style.setProperty(p, v, 'important');
    for (const [p, v] of [
      ['position', 'absolute'],
      ['margin', '0'],
      ['white-space', 'nowrap'],
      ['background', 'transparent'],
      ['border-color', 'transparent'],
      ['border-style', 'solid'],
      ['box-shadow', 'none'],
      ['box-sizing', 'border-box'],
      ['display', 'inline-flex'],
      ['align-items', 'center'],
      ['left', '0px'],
      ['top', '0px'],
    ])
      gh.style.setProperty(p!, v!, 'important');
    for (const [p, v] of [
      ['position', 'absolute'],
      ['left', '0px'],
      ['top', '0px'],
      ['width', '0px'],
      ['height', '0px'],
      ['overflow', 'visible'],
      ['pointer-events', 'none'],
      ['z-index', '3'],
    ])
      wr.style.setProperty(p!, v!, 'important');
    wr.appendChild(gh);
    hote.appendChild(wr);
    const k = (): number => {
      const r = hote.getBoundingClientRect();
      return (hote.offsetWidth ? r.width / hote.offsetWidth : 1) || 1;
    };
    const R = gh.getBoundingClientRect();
    gh.style.setProperty('left', `${String((g.r.left - R.left) / k())}px`, 'important');
    gh.style.setProperty('top', `${String((g.r.top - R.top) / k())}px`, 'important');
    // la pastille : le mot tapé, tout de suite ; l'allure des pointillés gardée le temps du remplissage
    const plein = mesure(el, c.html, c.cls);
    el.style.setProperty('box-sizing', 'border-box', 'important');
    el.style.setProperty('width', `${String(a.w)}px`, 'important');
    el.style.setProperty('justify-content', 'flex-start', 'important');
    el.style.setProperty('background-color', 'transparent', 'important');
    el.style.setProperty('border-style', g.style['border-top-style'] ?? 'dashed', 'important');
    el.style.setProperty('border-color', g.style['border-top-color'] ?? 'currentColor', 'important');
    el.style.setProperty('border-width', g.style['border-top-width'] ?? '2px', 'important');
    el.style.setProperty('position', 'relative', 'important');
    el.style.setProperty('isolation', 'isolate', 'important');
    el.getBoundingClientRect();
    el.style.setProperty(
      'transition',
      `width ${String(PREM)}ms ${COURBE}, border-width ${String(PREM)}ms ${COURBE}`,
      'important',
    );
    el.style.setProperty('width', `${String(plein.w)}px`, 'important');
    el.style.setProperty('border-width', '0px', 'important');
    let finP = false;
    const ctl = passageFlaques(el, {
      mode: 'couvre',
      couleur: plein.bg,
      duree: PREM,
      z: -1,
      fin: () => {
        if (finP) return;
        finP = true;
        termine();
      },
    });
    for (const [p, v] of [
      ['left', '0'],
      ['top', '0'],
      ['width', '100%'],
      ['height', '100%'],
      ['border-radius', plein.rad],
    ])
      ctl.canevas.style.setProperty(p!, v!, 'important');
    h.minuteur(() => {
      if (!finP) {
        finP = true;
        termine();
      }
    }, PREM + 600);
    // la copie suit la place (une recomposition peut la déplacer) ; elle est découpée là où s'écrit le texte tapé et son curseur
    const E0 = el.getBoundingClientRect();
    const masque = (): void => {
      if (!wr.isConnected) return;
      const cible = s.fini ? null : el.isConnected ? el : null;
      if (!cible) return;
      const E = cible.getBoundingClientRect();
      const kk = k();
      wr.style.setProperty(
        'translate',
        `${String((E.left - E0.left) / kk)}px ${String((E.top - E0.top) / kk)}px`,
        'important',
      );
      const W = wr.getBoundingClientRect();
      let pth = "path(evenodd, 'M -9999 -9999 H 9999 V 9999 H -9999 Z";
      const rg = document.createRange();
      const tw = document.createTreeWalker(cible, NodeFilter.SHOW_TEXT);
      const T: DOMRect[] = [];
      for (let n = tw.nextNode(); n; n = tw.nextNode()) {
        const t = n.nodeValue ?? '';
        for (let q = 0; q < t.length; q++) {
          if (/\s/.test(t[q]!)) continue;
          rg.setStart(n, q);
          rg.setEnd(n, q + 1);
          const r = rg.getBoundingClientRect();
          if (r.width > 0.3) T.push(r);
        }
      }
      for (const cr of cible.querySelectorAll('.ph-caret')) {
        const r = cr.getBoundingClientRect();
        if (r.width > 0.3) T.push(r);
      }
      for (const q of T) {
        const x0 = (q.left - W.left) / kk - 0.6;
        const y0 = (q.top - W.top) / kk - 0.6;
        const x1 = (q.right - W.left) / kk + 0.6;
        const y1 = (q.bottom - W.top) / kk + 0.6;
        pth += ` M ${x0.toFixed(1)} ${y0.toFixed(1)} H ${x1.toFixed(1)} V ${y1.toFixed(1)} H ${x0.toFixed(1)} Z`;
      }
      pth += "')";
      wr.style.setProperty('clip-path', pth, 'important');
      wr.style.setProperty('-webkit-clip-path', pth, 'important');
    };
    // l'opacité baisse à chaque image depuis l'instant de la frappe (la courbe part une image avant : l'image qui suit est déjà plus claire)
    const tF = h.maintenant();
    const AV = 16.7;
    const fondu = (): void => {
      if (!wr.isConnected) return;
      const p = Math.min(1, (h.maintenant() - tF + AV) / (FONDU + AV));
      const e = 1 - (1 - p) ** 2;
      gh.style.setProperty('opacity', (1 - e).toFixed(4), 'important');
      masque();
      if (p >= 1) {
        wr.remove();
        return;
      }
      h.image(fondu);
    };
    gh.style.setProperty('opacity', ((1 - AV / (FONDU + AV)) ** 2).toFixed(4), 'important');
    masque();
    h.image(fondu);
    h.minuteur(() => {
      wr.remove();
    }, FONDU + 600);
    function termine(): void {
      const c2 = s.cible;
      finir(el, s);
      el.querySelector(':scope > canvas.passage-flaques')?.remove();
      for (const p of ['background-color', 'border-style', 'border-color', 'border-width', 'position', 'isolation'])
        el.style.removeProperty(p);
      if (!c2.brut) {
        // effacé pendant le remplissage : le chemin de la place vidée (détracé, pointillés, tracé)
        pose(el, s.tape!);
        nettoie(el);
        mot(el, c2);
        return;
      }
      pose(el, c2);
      const wc = el.offsetWidth;
      el.style.removeProperty('transition');
      el.style.removeProperty('width');
      const wn = el.offsetWidth;
      if (Math.abs(wn - wc) > 0.5) {
        el.style.setProperty('width', `${String(wc)}px`, 'important');
        el.getBoundingClientRect();
        el.style.setProperty('transition', `width 160ms ${COURBE}`, 'important');
        el.style.setProperty('width', `${String(wn)}px`, 'important');
        lisses.add(el);
        h.minuteur(() => {
          lisses.delete(el);
          if (!ET.get(el)) nettoie(el);
        }, 200);
      } else nettoie(el);
    }
  }
  /** pendant le remplissage, une lettre tapée s'écrit tout de suite (la frappe n'attend jamais) ; l'encart suit chaque lettre */
  function premiereTexte(el: HTMLElement, c: Cible): void {
    const s = st(el)!;
    s.cible = { ...c, brut: true };
    s.tape = { ...c };
    const on = el.classList.contains('ph-on');
    const garde = PROPS.map((p) => [p, el.style.getPropertyValue(p), el.style.getPropertyPriority(p)] as const);
    const cv = el.querySelector(':scope > canvas.passage-flaques');
    el.className = c.cls;
    el.classList.toggle('ph-on', on);
    el.innerHTML = c.html;
    if (cv) el.insertBefore(cv, el.firstChild);
    for (const [p, v, pr] of garde) if (v) el.style.setProperty(p, v, pr);
    el.style.setProperty('width', `${String(mesure(el, c.html, c.cls).w)}px`, 'important');
  }

  // ── LES RECONSTRUCTIONS DE LA PHRASE ──
  function places(): Record<string, HTMLElement> {
    const o2: Record<string, HTMLElement> = {};
    txt.querySelectorAll<HTMLElement>('[data-ph],[data-np]').forEach((e) => {
      const k = e.dataset['ph'] ?? e.dataset['np'] ?? '';
      if (CLES.includes(k) && !o2[k]) o2[k] = e;
    });
    return o2;
  }
  let cleVue = '';
  const STYLES = [
    'font-family',
    'font-size',
    'font-weight',
    'letter-spacing',
    'color',
    '-webkit-text-fill-color',
    'line-height',
    'padding-top',
    'padding-right',
    'padding-bottom',
    'padding-left',
    'border-top-width',
    'border-top-style',
    'border-top-color',
    'height',
  ];
  return {
    enCours: () => [...enTransition].some((e) => ET.get(e)?.phase === 'detrace'),
    actif: () =>
      [...enTransition].some((e) => !!st(e)) ||
      [...arrivees].some((e) => e.isConnected) ||
      [...lisses].some((e) => e.isConnected) ||
      !!hote.querySelector('.pp-ex-part, .pp-place-part'),
    arrete() {
      for (const e of enTransition) {
        const s = ET.get(e);
        if (s) s.fini = true;
      }
      enTransition.clear();
      arrivees.clear();
      lisses.clear();
      hote.querySelectorAll('.pp-ex-part, .pp-place-part').forEach((x) => {
        x.remove();
      });
      cleVue = '';
    },
    avant() {
      const cle = o.cle();
      if (!o.vivante() || cle !== cleVue) {
        cleVue = cle;
        return null;
      }
      const av = places();
      const E: Avant['E'] = {};
      const G: Avant['G'] = {};
      for (const [k, e] of Object.entries(av)) {
        const s = st(e);
        E[k] = s
          ? { html: s.cible.html, cls: s.cible.cls, w: e.offsetWidth }
          : { html: contenu(e), cls: e.className, w: e.offsetWidth };
        const cs = getComputedStyle(e);
        const style: Record<string, string> = {};
        for (const p of STYLES) style[p] = cs.getPropertyValue(p);
        style['height'] = `${String(e.offsetHeight)}px`;
        G[k] = { r: e.getBoundingClientRect(), html: e.outerHTML, fs: cs.fontSize, lh: cs.lineHeight, style };
      }
      return { E, G, av, cle };
    },
    apres(A) {
      if (!A || A.cle !== o.cle()) return;
      const ap = places();
      const tl = o.trace();
      // le texte NEUF de chaque place, lu avant que la boucle lui rende l'ancien (sans cela la bascule se lisait toujours fausse, v202a)
      const NV: Record<string, string> = {};
      for (const [k, n] of Object.entries(ap)) NV[k] = n.innerHTML;
      for (const [k, n] of Object.entries(ap)) {
        const ol = A.av[k];
        const a = A.E[k];
        if (!ol || ol === n || !a) continue;
        const c: Cible = { html: n.innerHTML, cls: n.className };
        const s = st(ol);
        if (s) {
          // un nœud en transition garde sa place dans la phrase rebâtie (il remplace le neuf) et finira sur la cible du moment
          ol.classList.toggle('ph-on', n.classList.contains('ph-on'));
          n.replaceWith(ol);
          if (s.phase === 'premiere') {
            if (vide(c.cls)) {
              s.cible = c;
              s.cible.brut = false;
            } else premiereTexte(ol, c);
          } else {
            s.cible = c;
            // ce qu'on tape paraît tel quel (Q620) : la transition finit sur le texte tapé sans le tracer
            if ((k === 'titre' || k === 'nom') && !vide(c.cls)) s.cible.brut = true;
          }
          continue;
        }
        if (texte(a.html) === texte(c.html) && net(a.cls) === net(c.cls)) continue;
        const v0 = vide(a.cls);
        const v1 = vide(c.cls);
        if (k === 'titre' || k === 'nom') {
          if (v0 && !v1) {
            premiere(n, a, A.G[k], c);
            continue;
          }
          // une saisie : la frappe s'écrit lettre par lettre (Q620)
          if (!v0 && !v1) continue;
        }
        const on = n.classList.contains('ph-on');
        n.innerHTML = a.html;
        n.className = a.cls;
        n.classList.toggle('ph-on', on);
        mot(n, c, a.w);
      }
      // la bascule du sens : une place qui PART se détrace là où elle était, une place qui ARRIVE se trace
      const basc = !!(A.E['sens'] && ap['sens'] && texte(A.E['sens'].html) !== texte(NV['sens'] ?? ''));
      if (!basc || !tl || reduit()) return;
      for (const [k, g] of Object.entries(A.G)) {
        if ((ap[k] && visible(ap[k])) || !g.r.width) continue;
        const d = document.createElement('div');
        d.innerHTML = g.html;
        const gh = d.firstElementChild as HTMLElement | null;
        if (!gh) continue;
        gh.removeAttribute('data-ph');
        gh.removeAttribute('data-np');
        gh.removeAttribute('style');
        gh.classList.add('pp-place-part');
        gh.setAttribute('aria-hidden', 'true');
        for (const [p, v] of [
          ['position', 'absolute'],
          ['margin', '0'],
          ['pointer-events', 'none'],
          ['white-space', 'nowrap'],
          ['font-size', g.fs],
          ['line-height', g.lh],
          ['left', '0px'],
          ['top', '0px'],
          ['z-index', '2'],
        ])
          gh.style.setProperty(p!, v!, 'important');
        hote.appendChild(gh);
        const R = gh.getBoundingClientRect();
        const sc = (gh.offsetWidth ? R.width / gh.offsetWidth : 1) || 1;
        gh.style.setProperty('left', `${String((g.r.left - R.left) / sc)}px`, 'important');
        gh.style.setProperty('top', `${String((g.r.top - R.top) / sc)}px`, 'important');
        const finG = (): void => {
          gh.remove();
        };
        tl.trace(gh, null, { inverse: true, surFin: finG });
        h.minuteur(finG, 2500);
        // C-296 : son filet pointillé s'amincit jusqu'à rien pendant que son mot se détrace (le padding prend ce que le filet rend)
        const cg = getComputedStyle(gh);
        const bw = parseFloat(cg.borderTopWidth) || 0;
        if (bw > 0 && cg.borderTopStyle !== 'none') {
          const P0 = (['top', 'right', 'bottom', 'left'] as const).map(
            (sd) => (parseFloat(cg.getPropertyValue(`padding-${sd}`)) || 0) + bw,
          );
          gh.style.setProperty(
            'transition',
            `border-width ${String(D_FL)}ms ${COURBE}, padding ${String(D_FL)}ms ${COURBE}`,
            'important',
          );
          gh.getBoundingClientRect();
          gh.style.setProperty('border-width', '0px', 'important');
          gh.style.setProperty('padding', P0.map((v) => `${String(v)}px`).join(' '), 'important');
        }
      }
      for (const [k, n] of Object.entries(ap)) {
        if (A.av[k] || st(n) || !visible(n)) continue;
        // (une place qui arrive n'est pas une transition de mot : rebâtie pendant son tracé, la neuve passe par `mot` depuis ce qu'elle montrait)
        arrivees.add(n);
        tl.trace(n, null, {
          surFin: () => {
            arrivees.delete(n);
          },
        });
        h.minuteur(() => arrivees.delete(n), 4000);
      }
    },
  };
}
