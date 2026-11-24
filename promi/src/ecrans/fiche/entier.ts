/**
 * LA PHOTO D'UNE FICHE, EN ENTIER ET CADRÉE AU DOIGT (lot 3b-4 ; le prototype : lot-V131-ENTIER, C-051 ; lot-V139-CADRE, C-085 ; v141, C-098 ;
 * lot-V140-ENREGISTRER, C-091).
 *
 * EN ENTIER : toucher la bande quand elle porte une photo (jamais la dalle) l'affiche en entier, par-dessus tout l'appareil, sur un fond PLEIN — la
 * seiche, sans transparence, ni ombre, ni fondu ; l'image entière (`contain`) : on y voit ce que la bande recadrait. Un nouveau toucher, ou le X,
 * referme ; le bouton « Enregistrer » (la flèche dans son socle) donne la photo d'origine — la feuille de partage du téléphone quand elle prend un
 * fichier, sinon un téléchargement. VoiceOver : la bande se déclare « Voir la photo en entier » seulement quand elle porte une photo.
 *
 * CADRÉE AU DOIGT : deux doigts zooment dans le rapport de leur écart (1:1), le point sous leur milieu y reste, et elle TOURNE de l'angle des
 * doigts ; un doigt la déplace (elle le rattrape après 10 pt) ; z de 0,3 à 8. Le cadrage est mémorisé (`photoCadre` = {z, dx, dy, a, n}, en pt de
 * l'écran 390 ; `n` : la longueur de l'adresse de la photo — une autre photo repart de zéro). Un toucher sans glisser reste le toucher qui ouvre la
 * photo en entier.
 */
import { el, poserCroix } from '../commun.ts';

const TXT = {
  fermer: 'Fermer',
  glyphe: 'X',
  enregistrer: 'Enregistrer',
  vue: { photo: 'La photo en entier', dessin: 'Le dessin en entier' },
  alt: { photo: 'La photo de cette parole, en entier', dessin: 'Le dessin de cette parole, en entier' },
  voir: { photo: 'Voir la photo en entier', dessin: 'Voir le dessin en entier' },
} as const;
const SVG_ENREGISTRER =
  '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true" data-symbole="enregistrer"><path d="M16 7 L16 20 M16 20 L11.5 15.5 M16 20 L20.5 15.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8.5 19 L8.5 25 L23.5 25 L23.5 19" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>';

export const BORNES_CADRE = { ZMIN: 0.3, ZMAX: 8, SEUIL: 10 } as const;

export interface Cadre {
  z: number;
  dx: number;
  dy: number;
  a?: number;
  n: number;
}

export interface Entier {
  ouverte(): boolean;
  fermer(): void;
  /** la bande porte-t-elle une photo : elle se déclare commande (VoiceOver), ou plus */
  annoncer(): void;
}

export function monterEntier(o: {
  dv: HTMLElement;
  /** le canevas de la bande (opaque jusqu'à l'onde) */
  bande: HTMLCanvasElement;
  /** ce que le doigt touche dans la bande : la bande elle-même, ou la couche qui la couvre (rien de ce qu'elle porte) */
  surface: (t: Element) => boolean;
  /** la photo de la bande, ou null (une dalle) — seulement quand la fiche est ouverte, au repos, sans rien par-dessus */
  photo: () => string | null;
  /** la bande montre le dessin posé (lot 3b-5) : son image entière (elle s'ouvre en entier, jamais cadrée), ou null */
  dessin: () => string | null;
  /** le cadrage du moment, et son écriture (à la fin du geste) ; `centre` : le centre de la boîte de la photo et sa taille de couverture */
  cadre: () => Cadre | null;
  centre: () => { x: number; y: number } | null;
  cadrer: (c: Cadre, fini: boolean) => void;
}): Entier {
  const { dv, bande } = o;
  let vue: HTMLElement | null = null;

  function batir(): HTMLElement {
    if (vue) return vue;
    const v = el('div', { id: 'entierVue', role: 'dialog', 'aria-modal': 'true', 'aria-label': TXT.vue.photo });
    const im = el('img', { alt: TXT.alt.photo });
    const x = el('button', { type: 'button', class: 'ev-x', 'aria-label': TXT.fermer });
    x.textContent = TXT.glyphe;
    const g = el('button', { type: 'button', class: 'ev-garde enr-btn', 'aria-label': TXT.enregistrer });
    g.innerHTML = SVG_ENREGISTRER;
    v.append(im, x, g);
    dv.appendChild(v);
    vue = v;
    return v;
  }
  /**
   * LE X (lot-V157-CROIX : « le même X partout ») : sans titre, la croix se centre sur la boîte d'origine du « X » (Gilbert 13, capitales — la règle
   * de lot-V131-ENTIER), puis devient la zone de 44 pt et le glyphe PromiLate à la taille des X (`poserCroix`)
   */
  function poserX(v: HTMLElement): void {
    const x = v.querySelector<HTMLElement>('.ev-x')!;
    if (x.classList.contains('ev-pose')) return;
    const D = v.getBoundingClientRect();
    const k = D.width / (v.offsetWidth || 390) || 1;
    const r = x.getBoundingClientRect();
    if (!r.width) return;
    const cx = (r.left + r.width / 2 - D.left) / k;
    const cy = (r.top + r.height / 2 - D.top) / k;
    x.textContent = '';
    const g = el('span', { class: 'ev-g' });
    g.textContent = TXT.glyphe;
    x.appendChild(g);
    x.classList.add('ev-pose');
    x.style.left = `${(cx - 22).toFixed(2)}px`;
    x.style.top = `${(cy - 22).toFixed(2)}px`;
    poserCroix(x, g, null);
  }
  function ouverte(): boolean {
    return !!vue?.classList.contains('ouv');
  }
  /** ce que la bande montre en entier : le dessin posé d'abord (il remplace la photo), sinon la photo */
  function source(): { src: string; quoi: 'photo' | 'dessin' } | null {
    const d = o.dessin();
    if (d) return { src: d, quoi: 'dessin' };
    const p = o.photo();
    return p ? { src: p, quoi: 'photo' } : null;
  }
  function ouvrir(): boolean {
    const s = source();
    if (!s) return false;
    const v = batir();
    v.setAttribute('aria-label', TXT.vue[s.quoi]);
    v.dataset['quoi'] = s.quoi;
    const im = v.querySelector('img')!;
    im.alt = TXT.alt[s.quoi];
    im.src = s.src;
    v.classList.add('ouv');
    poserX(v);
    return true;
  }
  function fermer(): void {
    if (!vue || !ouverte()) return;
    vue.classList.remove('ouv');
    vue.querySelector('img')!.removeAttribute('src');
  }
  /** la photo d'origine, entière : la feuille de partage quand elle prend un fichier, sinon un téléchargement */
  function enregistrer(): void {
    const src = vue?.querySelector('img')?.getAttribute('src');
    if (!src) return;
    const ext = /^data:image\/(png|webp|gif)/.exec(src)?.[1] ?? 'jpg';
    const nom = `${vue?.dataset['quoi'] === 'dessin' ? 'promi-dessin' : 'promi-photo'}.${ext}`;
    const telecharge = (): void => {
      const a = el('a', { href: src, download: nom, rel: 'noopener' });
      document.body.appendChild(a);
      a.click();
      a.remove();
    };
    try {
      if (
        typeof navigator.share === 'function' &&
        typeof navigator.canShare === 'function' &&
        src.startsWith('data:')
      ) {
        const [tete, corps] = src.split(',');
        const bin = atob(corps ?? '');
        const u = new Uint8Array(bin.length);
        for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i);
        const f = new File([u], nom, { type: /^data:([^;]+)/.exec(tete ?? '')?.[1] ?? 'image/jpeg' });
        if (navigator.canShare({ files: [f] })) {
          navigator.share({ files: [f] }).catch(() => undefined);
          return;
        }
      }
    } catch {
      /* le téléchargement */
    }
    telecharge();
  }

  /** le point est-il DANS LA BANDE, sur ce qu'elle peint (opaque), et sur rien d'autre (ni le plateau, ni un bouton, ni un menu) ? */
  function dansBande(x: number, y: number): boolean {
    const h = document.elementFromPoint(x, y);
    if (!h || !o.surface(h)) return false;
    const r = bande.getBoundingClientRect();
    if (x < r.left || x > r.right || y < r.top || y > r.bottom) return false;
    try {
      const px = bande
        .getContext('2d')!
        .getImageData(
          Math.round(((x - r.left) * bande.width) / r.width),
          Math.round(((y - r.top) * bande.height) / r.height),
          1,
          1,
        ).data;
      return (px[3] ?? 0) > 200;
    } catch {
      return false;
    }
  }

  // ── LE TOUCHER : appui puis lever, moins de 10 px, moins de 600 ms — le clic qui pourrait suivre est avalé ──
  let G: { x: number; y: number; t: number; vue: boolean } | null = null;
  let avale = -1e9;
  let cadreT = -1e9;
  document.addEventListener(
    'pointerdown',
    (e) => {
      G = { x: e.clientX, y: e.clientY, t: e.timeStamp, vue: ouverte() };
    },
    true,
  );
  document.addEventListener(
    'pointerup',
    (e) => {
      const g = G;
      G = null;
      if (!g) return;
      if (Math.abs(e.clientX - g.x) > 10 || Math.abs(e.clientY - g.y) > 10 || e.timeStamp - g.t > 600) return;
      if (g.vue) {
        if (!ouverte()) return;
        if (e.target instanceof Element && e.target.closest('.ev-garde')) enregistrer();
        else fermer();
        avale = e.timeStamp;
        e.preventDefault();
        e.stopPropagation();
        return;
      }
      if (e.timeStamp - cadreT < 500) return;
      if (!source() || !dansBande(e.clientX, e.clientY)) return;
      if (ouvrir()) {
        avale = e.timeStamp;
        e.preventDefault();
        e.stopPropagation();
      }
    },
    true,
  );
  document.addEventListener(
    'click',
    (e) => {
      if (e.timeStamp - avale < 450) {
        avale = -1e9;
        e.preventDefault();
        e.stopPropagation();
      }
    },
    true,
  );
  document.addEventListener(
    'keydown',
    (e) => {
      if (ouverte() && (e.key === 'Escape' || e.key === 'Enter' || e.key === ' ')) {
        fermer();
        e.preventDefault();
        return;
      }
      if ((e.key === 'Enter' || e.key === ' ') && e.target === bande && source() && ouvrir()) e.preventDefault();
    },
    true,
  );

  // ── LE CADRAGE AU DOIGT (deux doigts : zoom et tour ; un doigt : déplacer) ──
  type Geste = {
    k: number;
    r: DOMRect;
    mode: 'attente' | 'glisse' | 'pince';
    x0: number;
    y0: number;
    c: Cadre;
    m0?: { x: number; y: number; d: number; g: number };
    z0?: number;
    dx0?: number;
    dy0?: number;
    a0?: number;
  };
  let T: Geste | null = null;
  const milieu = (t: TouchList): { x: number; y: number; d: number; g: number } => ({
    x: (t[0]!.clientX + t[1]!.clientX) / 2,
    y: (t[0]!.clientY + t[1]!.clientY) / 2,
    d: Math.hypot(t[0]!.clientX - t[1]!.clientX, t[0]!.clientY - t[1]!.clientY) || 1,
    g: Math.atan2(t[1]!.clientY - t[0]!.clientY, t[1]!.clientX - t[0]!.clientX),
  });
  const tour = (d: number): number => {
    let v = d;
    while (v > Math.PI) v -= 2 * Math.PI;
    while (v < -Math.PI) v += 2 * Math.PI;
    return v;
  };
  const neuf = (): Cadre | null => {
    const src = o.photo();
    if (!src) return null;
    const c = o.cadre();
    return c && c.n === src.length ? { ...c } : { z: 1, dx: 0, dy: 0, n: src.length };
  };
  document.addEventListener(
    'touchstart',
    (e) => {
      const t = e.touches;
      if (!t.length || ouverte() || !o.photo() || o.dessin()) {
        T = null;
        return;
      }
      if (t.length === 1) {
        if (!dansBande(t[0]!.clientX, t[0]!.clientY)) {
          T = null;
          return;
        }
        const r = bande.getBoundingClientRect();
        const c = neuf();
        if (!c) return;
        T = { k: r.width / 390 || 1, r, mode: 'attente', x0: t[0]!.clientX, y0: t[0]!.clientY, c };
        return;
      }
      if (t.length === 2) {
        if (!T) {
          if (!dansBande(t[0]!.clientX, t[0]!.clientY) && !dansBande(t[1]!.clientX, t[1]!.clientY)) return;
          const r = bande.getBoundingClientRect();
          const c = neuf();
          if (!c) return;
          T = { k: r.width / 390 || 1, r, mode: 'attente', x0: 0, y0: 0, c };
        }
        const m = milieu(t);
        T.mode = 'pince';
        T.m0 = m;
        T.z0 = T.c.z;
        T.dx0 = T.c.dx;
        T.dy0 = T.c.dy;
        T.a0 = T.c.a ?? 0;
        cadreT = e.timeStamp;
        e.preventDefault();
        e.stopPropagation();
      }
    },
    { capture: true, passive: false },
  );
  document.addEventListener(
    'touchmove',
    (e) => {
      if (!T) return;
      const t = e.touches;
      const c = T.c;
      if (T.mode === 'pince' && t.length >= 2) {
        const C = o.centre() ?? { x: 195, y: 190 };
        const m = milieu(t);
        const z = Math.max(BORNES_CADRE.ZMIN, Math.min(BORNES_CADRE.ZMAX, (T.z0! * m.d) / T.m0!.d));
        const f = z / T.z0!;
        // le point sous le milieu des doigts y reste, et la photo tourne de l'angle des doigts (le vecteur centre − milieu tourne avec elle)
        const cx0 = T.r.left + (C.x + T.dx0!) * T.k;
        const cy0 = T.r.top + (C.y + T.dy0!) * T.k;
        const da = tour(m.g - T.m0!.g);
        const co = Math.cos(da);
        const si = Math.sin(da);
        const vx = (cx0 - T.m0!.x) * f;
        const vy = (cy0 - T.m0!.y) * f;
        c.z = z;
        c.a = T.a0! + da;
        c.dx = (m.x + (vx * co - vy * si) - T.r.left) / T.k - C.x;
        c.dy = (m.y + (vx * si + vy * co) - T.r.top) / T.k - C.y;
        cadreT = e.timeStamp;
        e.preventDefault();
        e.stopPropagation();
        o.cadrer({ ...c }, false);
        return;
      }
      if (t.length !== 1) return;
      if (T.mode === 'attente') {
        if (Math.hypot(t[0]!.clientX - T.x0, t[0]!.clientY - T.y0) < BORNES_CADRE.SEUIL) return;
        T.mode = 'glisse';
        T.dx0 = c.dx;
        T.dy0 = c.dy;
      }
      if (T.mode === 'glisse') {
        c.dx = T.dx0! + (t[0]!.clientX - T.x0) / T.k;
        c.dy = T.dy0! + (t[0]!.clientY - T.y0) / T.k;
        cadreT = e.timeStamp;
        e.preventDefault();
        e.stopPropagation();
        o.cadrer({ ...c }, false);
      }
    },
    { capture: true, passive: false },
  );
  const fin = (e: TouchEvent): void => {
    if (!T) return;
    const t = e.touches;
    if (T.mode === 'pince' && t.length === 1) {
      // un doigt reste : il continue de déplacer
      T.mode = 'glisse';
      T.x0 = t[0]!.clientX;
      T.y0 = t[0]!.clientY;
      T.dx0 = T.c.dx;
      T.dy0 = T.c.dy;
      cadreT = e.timeStamp;
      return;
    }
    if (t.length) return;
    if (T.mode !== 'attente') {
      cadreT = e.timeStamp;
      o.cadrer({ ...T.c }, true);
      e.stopPropagation();
    }
    T = null;
  };
  document.addEventListener('touchend', fin, { capture: true, passive: false });
  document.addEventListener('touchcancel', fin, { capture: true });
  // pendant qu'on cadre, les événements de pointeur du même geste ne vont à personne d'autre
  for (const n of ['pointermove', 'pointerup', 'pointercancel', 'click'] as const)
    document.addEventListener(
      n,
      (e) => {
        const p = e;
        if (
          (T && T.mode !== 'attente') ||
          (n !== 'pointermove' && e.timeStamp - cadreT < 350 && p.pointerType !== 'mouse')
        ) {
          e.stopImmediatePropagation();
          if (n === 'click') e.preventDefault();
        }
      },
      true,
    );

  /** VoiceOver : la bande ne se déclare commande QUE lorsqu'elle porte une photo (on compare avant d'écrire) */
  function annoncer(): void {
    const s = source();
    if (s) {
      if (bande.getAttribute('aria-label') !== TXT.voir[s.quoi]) {
        bande.setAttribute('role', 'button');
        bande.setAttribute('tabindex', '0');
        bande.setAttribute('aria-label', TXT.voir[s.quoi]);
        bande.setAttribute('aria-hidden', 'false');
      }
    } else if (bande.getAttribute('aria-label')) {
      bande.removeAttribute('role');
      bande.removeAttribute('tabindex');
      bande.removeAttribute('aria-label');
      bande.setAttribute('aria-hidden', 'true');
    }
  }

  return { ouverte, fermer, annoncer };
}
