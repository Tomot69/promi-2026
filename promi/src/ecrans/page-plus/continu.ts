/**
 * CE QUI CHANGE DANS LA PHRASE DE LA PAGE + CHANGE EN DOUCEUR (C-271 : aucun changement sec) — trois mécanismes du prototype, portés ensemble
 * parce qu'ils lisent et écrivent la même phrase :
 *
 * 1. LA TAILLE (lot-V202A-TAILLE, C-273, C-278 ①) : la composition pose la phrase à sa taille FINALE ; seule l'image va de l'ancienne taille à
 *    la nouvelle, par `scale` depuis son coin haut gauche, 320 ms, la courbe (.33,0,.67,1). Une passe de composition qui tombe pendant le
 *    mouvement le met à sa fin le temps de mesurer (`avant`), puis le rend (`apres`) — une valeur animée ne s'écrit jamais au milieu d'une passe.
 * 2. LES MOTS DE LIAISON (lot-V203-LIAISONS, C-278 ⑥, C-312) : après une composition, un mot de liaison neuf (« à », « avec », « de » / « d’ »)
 *    se TRACE (armé tout de suite, lancé 340 ms plus tard, quand la phrase a glissé à sa place) ; un mot qui part se DÉTRACE à sa place (une
 *    copie posée là où on le voyait, à son style rendu).
 * 3. LE GLISSEMENT (lot-V203-CONTINU, C-278 §4) : à chaque image, la place de MISE EN PAGE de la phrase, de chacun de ses mots (par rapport à
 *    elle) et du rail est relue ; dès qu'elle change, l'élément glisse de la place où on le voyait à la nouvelle (320 ms, au compositeur :
 *    `translate`, le rail par `transform`). Pendant la frappe rien ne glisse (Q620) mais la place est relevée ; un choix ouvert : seule sa
 *    liste est suivie ; pendant le mouvement du clavier (Q598) la phrase et le rail sont portés par lui.
 *
 * Jamais dans les 600 ms qui suivent l'ouverture de la page (sa première composition se pose telle quelle), ni d'une nature à l'autre (une page
 * neuve), ni sous « Réduire les animations ».
 */
import type { Horloge } from '../../animation/horloge.ts';
import type { TraceLettres } from '../../animation/trace/trace.ts';

const DUREE = 320;
const EZ = 'cubic-bezier(.33,0,.67,1)';
const ID = 'pp-continu';

export interface OptionsContinu {
  cs: HTMLElement;
  txt: HTMLElement;
  rail: HTMLElement;
  choixHote: HTMLElement;
  h: Horloge;
  trace: () => TraceLettres | null;
  /** la page est montrée (ni cachée, ni en train de partir) */
  montree: () => boolean;
  /** la nature, et l'état ouvert (une page neuve ne glisse pas) */
  cle: () => string;
  /** un choix ouvert (les personnes) — sa liste seule est suivie */
  choixOuvert: () => boolean;
  /** la frappe : ce qu'on tape paraît tel quel (Q620) */
  frappe: () => boolean;
  /** le mouvement du clavier (Q598) porte la phrase et le rail */
  mouvement: () => boolean;
  /** une place de la phrase se détrace (la liaison neuve attend qu'elle ait fini) */
  placeEnDetrace: () => boolean;
}

export interface Avant {
  fs: number;
  liaisons: string[] | null;
  copies: Copie[] | null;
  rendre: (() => void)[];
}
interface Copie {
  x: string;
  l: number;
  t: number;
  st: [string, string][];
}
interface Suivi {
  e: HTMLElement;
  p: [number, number];
  vr?: [number, number];
  off?: [number, number];
  mvt?: boolean;
}

export interface Continu {
  avant(): Avant;
  apres(a: Avant): void;
  /** la page s'ouvre : la première composition se pose */
  ouvre(): void;
  /** pour le tracé des lettres : les mouvements de `el` (et de ses ancêtres) mis à leur fin le temps d'une mesure */
  horsAnim(el: Element): (() => void) | null;
}

function reduit(): boolean {
  try {
    return matchMedia('(prefers-reduced-motion: reduce)').matches;
  } catch {
    return false;
  }
}
/** la courbe (.33,0,.67,1) résolue : le décalage RESTANT d'un glissement (un nœud rebâti le reprend là où on le voit) */
function bez(u: number): number {
  const x1 = 0.33;
  const x2 = 0.67;
  let t = u;
  for (let i = 0; i < 8; i++) {
    const x = 3 * (1 - t) * (1 - t) * t * x1 + 3 * (1 - t) * t * t * x2 + t * t * t - u;
    const dx = 3 * (1 - t) * (1 - t) * x1 + 6 * (1 - t) * t * (x2 - x1) + 3 * t * t * (1 - x2);
    if (Math.abs(x) < 1e-4 || !dx) break;
    t = Math.max(0, Math.min(1, t - x / dx));
  }
  return 3 * (1 - t) * t * t + t * t * t;
}

export function creerContinu(o: OptionsContinu): Continu {
  const { cs, txt, rail, choixHote, h } = o;
  let ouvertT = -1e9;
  let prev: Record<string, Suivi> | null = null;
  let prevCle = '';
  let prevFs = '';
  let attendu = false;
  let ani: { a: Animation; t1: number; k0: number } | null = null;
  const gl = new WeakMap<HTMLElement, { t: number; d: [number, number] }>();
  let boucle: number | null = null;
  let profondeur = 0;

  const actif = (): boolean => o.montree() && !reduit() && h.maintenant() - ouvertT >= 600;

  // ---- la taille ----
  function demarre(t0: number): void {
    const t1 = parseFloat(txt.style.fontSize) || 0;
    if (!(t0 > 0 && t1 > 0 && Math.abs(t1 - t0) >= 0.5) || !actif() || !txt.animate) return;
    let k0 = t0 / t1;
    if (ani && ani.a.playState === 'running') {
      const pr = ani.a.effect?.getComputedTiming().progress;
      if (pr != null && ani.k0 > 0) k0 = (ani.k0 + (1 - ani.k0) * pr) * (ani.t1 / t1);
      ani.a.cancel();
    }
    txt.style.setProperty('transform-origin', '0 0');
    const a = txt.animate([{ scale: String(k0) }, { scale: '1' }], { duration: DUREE, easing: EZ });
    ani = { a, t1, k0 };
    a.onfinish = () => {
      if (ani?.a === a) ani = null;
    };
  }

  // ---- les glissements ----
  const estGlisse = (a: Animation): boolean => a.id === ID && a.playState === 'running';
  function reste(e: HTMLElement): [number, number] | null {
    const g = gl.get(e);
    if (!g) return null;
    const u = (h.maintenant() - g.t) / DUREE;
    if (u >= 1) return [0, 0];
    const f = 1 - bez(Math.max(0, u));
    return [g.d[0] * f, g.d[1] * f];
  }
  function glisse(e: HTMLElement, dx: number, dy: number): void {
    const c = reste(e) ?? [0, 0];
    dx += c[0];
    dy += c[1];
    for (const a of e.getAnimations()) if (a.id === ID) a.cancel();
    const K: Keyframe[] =
      e === rail
        ? [{ transform: `translate(${String(dx)}px,${String(dy)}px)` }, { transform: 'translate(0,0)' }]
        : [{ translate: `${String(dx)}px ${String(dy)}px` }, { translate: '0 0' }];
    const an = e.animate(K, { duration: DUREE, easing: EZ });
    an.id = ID;
    gl.set(e, { t: h.maintenant(), d: [dx, dy] });
    // le canevas d'un tracé en cours est le frère de son mot : il glisse avec lui
    const cv = e.nextElementSibling;
    if (cv instanceof HTMLCanvasElement && cv.hasAttribute('data-trace')) {
      for (const a of cv.getAnimations()) if (a.id === ID) a.cancel();
      cv.animate(K, { duration: DUREE, easing: EZ }).id = ID;
    }
  }
  function pos(e: HTMLElement): [number, number] | null {
    let x = 0;
    let y = 0;
    let q: HTMLElement | null = e;
    let n = 0;
    while (q && q !== cs && n++ < 30) {
      x += q.offsetLeft;
      y += q.offsetTop;
      q = q.offsetParent as HTMLElement | null;
    }
    return q === cs ? [x, y] : null;
  }
  function suivis(): [string, HTMLElement, [number, number]][] {
    const L: [string, HTMLElement, [number, number]][] = [];
    if (o.choixOuvert()) {
      choixHote.querySelectorAll<HTMLElement>('.gn').forEach((g, i) => {
        if (g.offsetHeight <= 10) return;
        const p = pos(g);
        if (p) L.push(['choix' + String(i), g, p]);
      });
      return L;
    }
    const bp = pos(txt);
    if (!bp) return L;
    L.push(['phrase', txt, bp]);
    const cnt: Record<string, number> = {};
    txt.querySelectorAll<HTMLElement>('[data-ph],[data-np],em').forEach((e) => {
      if (e.tagName === 'EM' && e.closest('[data-ph],[data-np]')) return;
      if (e.classList.contains('pp-part-li')) return;
      const s = (e.textContent ?? '').trim();
      const n = (cnt[s] = (cnt[s] ?? 0) + 1);
      const pl = e.dataset['ph'] ?? e.dataset['np'];
      const k = pl ? 'p:' + pl : 'e:' + s + '#' + String(n);
      const p = pos(e);
      if (p) L.push([k, e, [p[0] - bp[0], p[1] - bp[1]]]);
    });
    if (!rail.hidden && rail.offsetHeight > 0) {
      const pr = pos(rail);
      if (pr) L.push(['rail', rail, pr]);
    }
    return L;
  }
  function courant(e: HTMLElement): [number, number] {
    if (!e.getAnimations().some(estGlisse)) return [0, 0];
    const t = getComputedStyle(e).translate;
    if (!t || t === 'none') return [0, 0];
    const p = t.split(' ').map(parseFloat);
    return [p[0] || 0, p[1] || 0];
  }
  function verifie(): void {
    const c = o.cle() + (o.choixOuvert() ? '|liste' : '');
    if (!actif() || c !== prevCle) {
      prevCle = c;
      prev = null;
      return;
    }
    const L = suivis();
    const MVT = o.mouvement();
    const D = cs.getBoundingClientRect();
    const kd = D.width / (cs.offsetWidth || 390) || 1;
    const PR = o.choixOuvert() ? null : txt.getBoundingClientRect();
    const M: Record<string, Suivi> = {};
    for (const [k, e, p] of L) {
      const s: Suivi = { e, p };
      if (MVT && (k === 'phrase' || k === 'rail')) s.mvt = true;
      if (PR && k !== 'phrase' && k !== 'rail') {
        const r = e.getBoundingClientRect();
        s.vr = [(r.left - PR.left) / kd, (r.top - PR.top) / kd];
      }
      M[k] = s;
    }
    // la taille vient de changer : sa mise à l'échelle porte déjà les mots ; on attend UNE image pour compter les places à l'échelle vue
    let tailleChange = false;
    if (ani && !vues.has(ani.a)) {
      vues.add(ani.a);
      tailleChange = true;
    }
    const sc = parseFloat(getComputedStyle(txt).scale) || 1;
    const fs = txt.style.fontSize;
    if (prev && prevFs && fs && fs !== prevFs && !tailleChange && !attendu) {
      attendu = true;
      return;
    }
    attendu = false;
    if (prev && !o.frappe())
      for (const k of Object.keys(M)) {
        const a = prev[k];
        const b = M[k]!;
        if (!a || b.mvt || a.mvt) continue;
        if (tailleChange && k !== 'phrase' && k !== 'rail') {
          if (!a.vr || !b.vr) continue;
          const ex = (a.vr[0] - b.vr[0]) / sc;
          const ey = (a.vr[1] - b.vr[1]) / sc;
          if (Math.abs(ex) >= 1.5 || Math.abs(ey) >= 1.5) glisse(b.e, ex, ey);
          continue;
        }
        let dx = a.p[0] - b.p[0];
        let dy = a.p[1] - b.p[1];
        if (a.e !== b.e) {
          const o2 = reste(a.e) ?? a.off;
          if (o2) {
            dx += o2[0];
            dy += o2[1];
          }
        }
        if (Math.abs(dx) < 1.5 && Math.abs(dy) < 1.5) continue;
        glisse(b.e, dx, dy);
      }
    for (const s of Object.values(M)) if (!s.mvt) s.off = courant(s.e);
    prev = M;
    prevFs = fs;
  }
  const vues = new WeakSet<Animation>();
  /** les mots de liaison neufs, par texte : l'heure de leur tracé (C-278 ⑥) ; les nœuds déjà tracés */
  const enCours = new Map<string, { t: number; fini: boolean }>();
  const vusTrace = new WeakSet<HTMLElement>();
  function image(): void {
    boucle = null;
    if (!o.montree()) {
      prev = null;
      return;
    }
    verifie();
    boucle = h.image(image);
  }

  // ---- les liaisons ----
  function liaisons(): string[] {
    const L: string[] = [];
    txt.querySelectorAll('em').forEach((e) => {
      if (e.closest('[data-ph],[data-np]') || e.classList.contains('pp-part-li')) return;
      L.push((e.textContent ?? '').trim());
    });
    return L;
  }
  function copies(): Copie[] {
    const L: Copie[] = [];
    const H = cs.getBoundingClientRect();
    const k = H.width / (cs.offsetWidth || H.width) || 1;
    txt.querySelectorAll('em').forEach((e) => {
      if (e.closest('[data-ph],[data-np]') || e.classList.contains('pp-part-li')) return;
      const x = (e.textContent ?? '').trim();
      const r = e.getBoundingClientRect();
      if (!x || !(r.width > 0)) return;
      const c = getComputedStyle(e);
      L.push({
        x,
        l: (r.left - H.left) / k,
        t: (r.top - H.top) / k,
        st: [
          'font-family',
          'font-size',
          'font-weight',
          'font-style',
          'line-height',
          'letter-spacing',
          'color',
          '-webkit-text-fill-color',
          'text-transform',
        ].map((p) => [p, c.getPropertyValue(p)] as [string, string]),
      });
    });
    return L;
  }
  function part(q: Copie, tl: TraceLettres): void {
    const s = document.createElement('em');
    s.textContent = q.x;
    s.setAttribute('aria-hidden', 'true');
    s.className = 'pp-part-li';
    s.style.cssText = `position:absolute!important;margin:0!important;padding:0!important;white-space:nowrap!important;pointer-events:none!important;left:${String(q.l)}px!important;top:${String(q.t)}px!important`;
    for (const [p, v] of q.st) if (v) s.style.setProperty(p, v, 'important');
    cs.appendChild(s);
    const fin = (): void => {
      s.remove();
    };
    tl.trace(s, null, { inverse: true, surFin: fin });
    h.minuteur(fin, 2500);
  }

  return {
    ouvre() {
      ouvertT = h.maintenant();
      prev = null;
      prevCle = '';
      ani?.a.cancel();
      ani = null;
      if (boucle == null) boucle = h.image(image);
    },
    avant() {
      profondeur++;
      const rendre: (() => void)[] = [];
      const fige = (a: Animation): void => {
        const t = a.currentTime;
        a.pause();
        a.currentTime = DUREE;
        rendre.push(() => {
          try {
            a.currentTime = t;
            a.play();
          } catch {
            /* (l'animation a été annulée) */
          }
        });
      };
      if (ani && ani.a.playState === 'running') fige(ani.a);
      for (const e of [txt, rail, ...txt.querySelectorAll<HTMLElement>('[data-ph],[data-np],em,canvas[data-trace]')])
        for (const a of e.getAnimations()) if (estGlisse(a)) fige(a);
      const vu = profondeur === 1 && actif();
      return {
        fs: parseFloat(txt.style.fontSize) || 0,
        liaisons: vu ? liaisons() : null,
        copies: vu ? copies() : null,
        rendre,
      };
    },
    apres(av) {
      profondeur = Math.max(0, profondeur - 1);
      for (const f of av.rendre) f();
      if (profondeur > 0) return;
      demarre(av.fs);
      const tl = o.trace();
      if (av.liaisons && tl) {
        const reste = av.liaisons.slice();
        const apres: string[] = [];
        txt.querySelectorAll<HTMLElement>('em').forEach((e) => {
          if (e.closest('[data-ph],[data-np]')) return;
          const x = (e.textContent ?? '').trim();
          if (!x) return;
          apres.push(x);
          const i = reste.indexOf(x);
          if (i >= 0) {
            reste.splice(i, 1);
            // un mot neuf qui se traçait encore, rebâti par cette composition (la validation recompose la phrase) : son tracé reprend sur le
            // nœud neuf — resté sur l'ancien, retiré, le mot paraîtrait d'un coup
            const ec = enCours.get(x);
            if (ec && !ec.fini && h.maintenant() - ec.t < 2500 && !vusTrace.has(e)) {
              vusTrace.add(e);
              tl.trace(e, null, {
                surFin: () => {
                  ec.fini = true;
                },
              });
            }
            return;
          }
          const ec = { t: h.maintenant(), fini: false };
          enCours.set(x, ec);
          vusTrace.add(e);
          // armé (la découpe vide posée tout de suite), lancé quand la phrase a glissé à sa place ; une place qui se détrace encore d'abord
          const ct = tl.trace(e, null, {
            arme: true,
            surFin: (r) => {
              if (!r.interrompu && e.isConnected) ec.fini = true;
            },
          });
          const t0 = h.maintenant();
          const go = (): void => {
            if (o.placeEnDetrace() && h.maintenant() - t0 < 2500) {
              h.minuteur(go, 30);
              return;
            }
            ct.lance?.();
          };
          h.minuteur(go, 340);
        });
        if (av.copies) {
          const dispo = apres.slice();
          for (const q of av.copies) {
            const j = dispo.indexOf(q.x);
            if (j >= 0) dispo.splice(j, 1);
            else part(q, tl);
          }
        }
      }
      // un rebâti : vérifié dans la tâche, avant la peinture (sinon le nœud neuf paraît une image à sa place)
      queueMicrotask(verifie);
    },
    horsAnim(el) {
      const R: (() => void)[] = [];
      const fige = (a: Animation): void => {
        const t = a.currentTime;
        a.pause();
        a.currentTime = DUREE;
        R.push(() => {
          try {
            a.currentTime = t;
            a.play();
          } catch {
            /* (annulée) */
          }
        });
      };
      if (ani && ani.a.playState === 'running' && txt.contains(el)) fige(ani.a);
      for (let q: Element | null = el; q; q = q.parentElement)
        for (const a of q.getAnimations()) if (estGlisse(a)) fige(a);
      el.querySelectorAll('[data-ph],[data-np],em,canvas[data-trace]').forEach((q) => {
        for (const a of q.getAnimations()) if (estGlisse(a)) fige(a);
      });
      return R.length
        ? () => {
            for (const f of R) f();
          }
        : null;
    },
  };
}
