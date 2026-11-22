/**
 * LE SOCLE TRANSVERSAL, PARTIE 1 (C-326, Tom, 20 nov. 2026 : « porte en tests Playwright (WebKit) les juges du lot 1 et du socle
 * transversal, chacun avec sa décision écrite en dur, chacun doit rougir sur une sonde »).
 *
 * Les sentinelles du prototype (`redteam_*.py`, à la racine) portées sur la VRAIE APP. Elles parcourent ECRANS_PORTES (aides.ts) : chaque
 * lot y ajoute ses écrans, et ces juges les couvrent sans qu'on les touche. Elles lisent ce qui est RENDU (styles calculés, encre,
 * pixels), jamais la valeur que l'app déclare (CLAUDE.md §7) ; la référence est le prototype ACTUEL, servi tel quel, ouvert au même
 * écran, sur le même état, dans le même WebKit.
 *
 * Un relevé par (écran, thème) — de la vraie app et du prototype — est fait une fois par processus et partagé par les juges qui ne font
 * que lire (couleurs, aspect, air, superposition, joignable, débordement, filets, lexique, volume rendu) ; une sonde active
 * (`PROMI_SONDE`) est posée dans le relevé de la vraie app, jamais dans celui du prototype.
 */
import { test, expect, type Browser, type Page } from '@playwright/test';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { PNG } from 'pngjs';
import {
  ECRANS_PORTES,
  type EcranPorte,
  stockage,
  prototype,
  vraieApp,
  ouvrirPlus,
  sonde,
  GEL,
  ecartAdmis,
} from './aides.ts';

const THEMES = ['sombre', 'clair'] as const;
type Theme = (typeof THEMES)[number];
const lsDe = (t: Theme): Record<string, string> => ({ ...stockage(), promi_theme: t === 'clair' ? 'light' : 'dark' });
const SRC = join(import.meta.dirname, '..', '..', 'src');

// ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
// LES SONDES DU RELEVÉ : le défaut que chaque juge doit prendre, posé dans la vraie app (sur CHAQUE écran porté) quand `PROMI_SONDE`
// porte son nom (tests/rendu/sondes/socle-1.json). Une sonde CSS, ou un défaut posé par script.
// ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
// (chaque sonde nommée en clair par l'aide `sonde`, pour que `npm run sondes` la retrouve dans ce fichier)
const SONDES_RELEVE: Record<string, { actif: boolean; css?: string; js?: string }> = {
  'couleurs-encre': {
    actif: sonde('couleurs-encre'),
    css: '#device .acc-entree .l{color:#C9A8F5!important}',
  },
  'joignable-recouvert': {
    actif: sonde('joignable-recouvert'),
    js: "(()=>{const d=document.createElement('div');d.id='sondeVoile';d.style.cssText='position:absolute;left:0;top:0;width:100%;height:140px;z-index:999';document.getElementById('device').appendChild(d);})()",
  },
  'ecrans-deborde': {
    actif: sonde('ecrans-deborde'),
    css: '#device .acc-barre{right:-40px!important}',
  },
  'volume-rendu': {
    actif: sonde('volume-rendu'),
    css: '#device .acc-plat{box-shadow:0 6px 18px rgba(0,0,0,.35)!important}',
  },
  'air-rapproche': {
    actif: sonde('air-rapproche'),
    css: '#device .acc-rappel{top:calc(var(--ancre-haut) + 62px)!important}#device .acc-pil[data-k="chiche"]{top:70px!important}',
  },
  'superpo-texte': {
    actif: sonde('superpo-texte'),
    css: '#device #souffleBtn{left:30px!important}',
  },
  'aspect-place': {
    actif: sonde('aspect-place'),
    css: '#device .acc-entree .l{translate:0 1px!important}',
  },
  'aspect-image': {
    actif: sonde('aspect-image'),
    css: '#device .acc-entree .l{text-decoration:underline!important}',
  },
  'filets-dom': {
    actif: sonde('filets-dom'),
    css: '#device .acc-plat{border-left:0!important;border-right:0!important;border-radius:0!important}',
  },
  'filets-canevas': {
    actif: sonde('filets-canevas'),
    js: "(()=>{const c=document.createElement('canvas');c.id='sondeFilet';c.width=300;c.height=20;c.style.cssText='position:absolute;left:40px;top:300px;width:300px;height:20px;z-index:50';document.getElementById('device').appendChild(c);const g=c.getContext('2d');g.strokeStyle='rgba(247,240,222,.55)';g.lineWidth=0.8;g.beginPath();g.moveTo(0,10);g.lineTo(300,10);g.stroke();})()",
  },
  'tonsurton-anneau': {
    actif: sonde('tonsurton-anneau'),
    css:
      "#device:not(.light) #createBtn::before{background-image:url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 72 72'><path d='M36.00 6.75 A29.25 29.25 0 1 1 35.90 6.75' fill='none' stroke='%23060403' stroke-width='13.5'/></svg>\")!important}" +
      "#device.light #createBtn::before{background-image:url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 72 72'><path d='M36.00 6.75 A29.25 29.25 0 1 1 35.90 6.75' fill='none' stroke='%23F6EFDD' stroke-width='13.5'/></svg>\")!important}",
  },
  'lexique-terme': {
    actif: sonde('lexique-terme'),
    js: "(()=>{const d=document.createElement('div');d.textContent='3 tâches à valider';d.style.cssText='position:absolute;left:30px;top:300px;z-index:999;color:#F7F0DE;font:500 16px Atkinson';document.getElementById('device').appendChild(d);})()",
  },
  'lexique-point': {
    actif: sonde('lexique-point'),
    js: "(()=>{const d=document.createElement('i');d.className='sonde-point';d.style.cssText='position:absolute;left:30px;top:300px;width:8px;height:8px;border-radius:50%;background:#DD4D23;z-index:999';document.getElementById('device').appendChild(d);})()",
  },
};

async function poserSondeReleve(page: Page): Promise<void> {
  for (const s of Object.values(SONDES_RELEVE)) {
    if (!s.actif) continue;
    if (s.css) await page.addStyleTag({ content: s.css });
    if (s.js) await page.evaluate(s.js);
  }
}

// ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
// LES PIÈGES, posés avant le chargement : qui écoute un toucher (redteam_joignable, A) ; qui peint un filet crème (redteam_filets, 2).
// ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
function piegeEcouteurs(): void {
  const A = EventTarget.prototype.addEventListener;
  const T: Record<string, 1> = {
    click: 1,
    pointerup: 1,
    pointerdown: 1,
    touchend: 1,
    touchstart: 1,
    mousedown: 1,
    mouseup: 1,
    change: 1,
    input: 1,
  };
  EventTarget.prototype.addEventListener = function (this: EventTarget, t: string, f: unknown, o?: unknown) {
    try {
      const n = this as unknown as Node & { __ec?: string };
      if (T[t] && n && n.nodeType === 1 && n !== document.body && n !== document.documentElement)
        n.__ec = (n.__ec ?? '') + t + ' ';
    } catch {
      /* rien */
    }
    return A.call(this, t, f as EventListener, o as AddEventListenerOptions);
  } as typeof EventTarget.prototype.addEventListener;
}

function piegeFilets(): void {
  const o = CanvasRenderingContext2D.prototype.stroke;
  CanvasRenderingContext2D.prototype.stroke = function (this: CanvasRenderingContext2D, ...a: unknown[]) {
    try {
      const t = String(this.strokeStyle).toLowerCase().replace(/\s/g, '');
      if (t === '#f7f0de' || t.startsWith('rgba(247,240,222,') || t === 'rgb(247,240,222)') {
        const c = this.canvas as HTMLCanvasElement;
        const w = window as unknown as { __filets?: string[] };
        if (c.isConnected && c.id !== 'toileCv' && c.closest('#device'))
          (w.__filets ??= []).push(c.id || c.className || 'canvas');
      }
    } catch {
      /* rien */
    }
    return (o as (...x: unknown[]) => void).apply(this, a);
  } as typeof CanvasRenderingContext2D.prototype.stroke;
}

// ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
// LE RELEVÉ, dans la page (vraie app ou prototype : `#device` dans les deux, l'écran 390 × 844 en points)
// ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
type Boite = [number, number, number, number];
interface NoeudR {
  cle: string;
  tag: string;
  texte: string;
  r: Boite;
  st: Record<string, string>;
  ps: Record<string, string>;
}
interface BlocR {
  cle: string;
  x: number;
  y: number;
  w: number;
  h: number;
}
interface Releve {
  noeuds: NoeudR[];
  blocs: BlocR[];
  interactifs: string[];
  injoignables: string[];
  deborde: string[];
  filets: string[];
  termes: string[];
  points: string[];
  volumes: string[];
  superpo: string[];
  champs: number;
}

function releverDansPage(): Releve {
  const dv = document.getElementById('device')!;
  const D = dv.getBoundingClientRect();
  const k = D.width / 390;
  const arr = (v: number): number => Math.round(v * 100) / 100;
  const pt = (r: { left: number; top: number; width: number; height: number }): Boite => [
    arr((r.left - D.left) / k),
    arr((r.top - D.top) / k),
    arr(r.width / k),
    arr(r.height / k),
  ];
  const opEff = (e: Element): number => {
    let o = 1;
    for (let q: Element | null = e; q; q = q.parentElement) {
      o *= +getComputedStyle(q).opacity;
      if (q === dv) break;
    }
    return o;
  };
  // RECOUVERT (lot 2a) : un élément dont le centre est sous un fond OPAQUE qui n'est ni lui, ni un de ses ancêtres, ni un de ses
  // descendants n'est pas vu — l'accueil sous la page + : le prototype le laisse peint sous elle, la vraie app le cache (`.couvert`) ;
  // des deux côtés il n'est pas à l'écran. La pile se lit avec tous les éléments touchables le temps du relevé (`elementsFromPoint` ne
  // voit pas un élément `pointer-events: none`), puis l'app est rendue telle quelle
  const recouverts = new Set<Element>();
  {
    const st = document.createElement('style');
    st.textContent = '*{pointer-events:auto!important}';
    document.head.appendChild(st);
    const opaque = (q: Element): boolean => {
      const m = /rgba?\(([^)]+)\)/.exec(getComputedStyle(q).backgroundColor);
      if (!m) return false;
      const v = m[1]!.split(',').map((x) => +x);
      return (v.length < 4 ? 1 : v[3]!) >= 0.95;
    };
    for (const e of document.querySelectorAll('[data-recouvert]')) e.removeAttribute('data-recouvert');
    for (const e of dv.querySelectorAll('*')) {
      const r = e.getBoundingClientRect();
      if (r.width < 1 || r.height < 1) continue;
      for (const q of document.elementsFromPoint(r.left + r.width / 2, r.top + r.height / 2)) {
        if (q === e || e.contains(q) || q.contains(e)) break;
        if (opaque(q)) {
          recouverts.add(e);
          e.setAttribute('data-recouvert', '');
          break;
        }
      }
    }
    st.remove();
  }
  const vu = (e: Element): DOMRect | null => {
    if (recouverts.has(e)) return null;
    const r = e.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return null;
    if (r.right < D.left || r.left > D.right || r.bottom < D.top || r.top > D.bottom) return null;
    const c = getComputedStyle(e);
    if (c.visibility === 'hidden' || c.display === 'none') return null;
    if (opEff(e) < 0.05) return null;
    return r;
  };
  const cles = new Map<Element, string>();
  const cle = (e: Element): string => {
    const deja = cles.get(e);
    if (deja) return deja;
    let s: string;
    if (e === dv) s = '#device';
    else if (e.id) s = '#' + e.id;
    else {
      const p = e.parentElement;
      if (!p) s = e.tagName.toLowerCase();
      else {
        // le rang parmi les frères du même nom, rendus, et qui portent du texte s'il en porte (une pastille sans texte posée avant un
        // nom, dans le prototype, ne décale pas le nom)
        const porte = (x: Element): boolean => !!(x.textContent ?? '').trim();
        const fr = [...p.children].filter(
          (x) => x.tagName === e.tagName && getComputedStyle(x).display !== 'none' && porte(x) === porte(e),
        );
        s = cle(p) + '>' + e.tagName.toLowerCase() + ':' + String(fr.indexOf(e));
      }
    }
    cles.set(e, s);
    return s;
  };
  const idAncetre = (e: Element): string => {
    for (let q: Element | null = e; q; q = q.parentElement) if (q.id) return '#' + q.id;
    return '';
  };
  const texteDe = (e: Element): string =>
    [...e.childNodes]
      .filter((n) => n.nodeType === 3)
      .map((n) => n.nodeValue ?? '')
      .join(' ')
      .replace(/\s+/g, ' ')
      .trim();
  const PROPS = [
    'color',
    'webkitTextFillColor',
    'backgroundColor',
    'backgroundImage',
    'borderTopColor',
    'borderRightColor',
    'borderBottomColor',
    'borderLeftColor',
    'borderTopWidth',
    'borderRightWidth',
    'borderBottomWidth',
    'borderLeftWidth',
    'borderTopLeftRadius',
    'outlineStyle',
    'outlineColor',
    'fill',
    'stroke',
    'boxShadow',
    'textShadow',
    'filter',
    'fontFamily',
    'fontSize',
    'fontWeight',
    'fontStyle',
    'letterSpacing',
    'lineHeight',
    'textTransform',
    'textDecorationLine',
    'mixBlendMode',
  ];
  const PPROPS = [
    'backgroundColor',
    'backgroundImage',
    'borderTopColor',
    'borderTopWidth',
    'boxShadow',
    'filter',
    'opacity',
    'mixBlendMode',
  ];
  const lire = (c: CSSStyleDeclaration, L: string[]): Record<string, string> => {
    const o: Record<string, string> = {};
    for (const p of L) o[p] = String((c as unknown as Record<string, string>)[p] ?? '');
    return o;
  };
  // une ombre ou un halo est un VOLUME s'il a un flou (troisième longueur > 0) et n'est pas « inset » (redteam_volume, `floue`)
  const floue = (v: string, n: number): boolean => {
    if (!v || v === 'none') return false;
    for (const part of v.split(/,(?![^(]*\))/)) {
      if (part.includes('inset')) continue;
      const L = [...part.replace(/rgba?\([^)]*\)/g, '').matchAll(/(-?[\d.]+)px/g)].map((m) => +m[1]!);
      if (L.length >= n && L[n - 1]! > 0) return true;
    }
    return false;
  };

  const noeuds: NoeudR[] = [];
  const interactifs: string[] = [];
  const injoignables: string[] = [];
  const deborde: string[] = [];
  const filets: string[] = [];
  const termes: string[] = [];
  const points: string[] = [];
  const volumes: string[] = [];
  let champs = 0;
  const BANNIS = [
    'tâche',
    'to-do',
    'todo',
    'objectif',
    'valider',
    'urgent',
    'score',
    'brouillon',
    'orbite',
    'la sphère',
    'belle parole',
    'en replanter un',
    'dire un mot',
  ];
  const SANCTIONNES = [
    'csBotBar',
    'cbb',
    'dpDetails',
    'dpdTog',
    'dpd-tog',
    'dpm-filet',
    'dpMsg',
    'mg-note-line',
    'ix-hair',
  ];
  const sanctionne = (e: Element): boolean => {
    let n: Element | null = e;
    for (let i = 0; i < 4 && n; i++, n = n.parentElement) {
      const sig = (n.id || '') + ' ' + (typeof n.className === 'string' ? n.className : '');
      if (SANCTIONNES.some((s) => sig.includes(s))) return true;
    }
    return false;
  };
  const INTER = 'button, a[href], input, select, textarea, [role=button], [contenteditable=""], [contenteditable=true]';
  const tous = [dv, ...dv.querySelectorAll('*')];
  for (const e of tous) {
    const r = vu(e);
    if (!r) continue;
    const c = getComputedStyle(e);
    const texte = texteDe(e);
    const ps: Record<string, string> = {};
    for (const pe of ['::before', '::after']) {
      const pc = getComputedStyle(e, pe);
      if (pc.content === 'none' || pc.display === 'none') continue;
      for (const [p, v] of Object.entries(lire(pc, PPROPS))) ps[pe + ' ' + p] = v;
      if (floue(pc.boxShadow, 3)) volumes.push(cle(e) + pe + ' box-shadow ' + pc.boxShadow);
      if (/gradient\(/.test(pc.backgroundImage)) volumes.push(cle(e) + pe + ' ' + pc.backgroundImage.slice(0, 60));
      if (/drop-shadow\(/.test(pc.filter)) volumes.push(cle(e) + pe + ' filter ' + pc.filter);
    }
    noeuds.push({ cle: cle(e), tag: e.tagName.toLowerCase(), texte, r: pt(r), st: lire(c, PROPS), ps });
    // VOLUME (redteam_volume, au rendu)
    if (floue(c.boxShadow, 3)) volumes.push(cle(e) + ' box-shadow ' + c.boxShadow);
    if (floue(c.textShadow, 3)) volumes.push(cle(e) + ' text-shadow ' + c.textShadow);
    if (/gradient\(/.test(c.backgroundImage)) volumes.push(cle(e) + ' ' + c.backgroundImage.slice(0, 60));
    if (/drop-shadow\(/.test(c.filter)) volumes.push(cle(e) + ' filter ' + c.filter);
    // JOIGNABLE (redteam_joignable, A) : au CENTRE de l'élément, le doigt le trouve
    const ec = (e as unknown as { __ec?: string }).__ec;
    if (e !== dv && e.id !== 'app' && (ec || e.matches(INTER))) {
      interactifs.push(cle(e));
      const cx = r.left + r.width / 2;
      const cy = r.top + r.height / 2;
      // une rangée qui défile et le déclare (data-glisse, C-196 : le rail du pinceau) : ce qui est hors de sa vue s'atteint en glissant
      const gl = e.closest('[data-glisse]');
      const glR = gl && gl !== e ? gl.getBoundingClientRect() : null;
      if (glR && (cx < glR.left || cx > glR.right)) {
        /* atteint en glissant la rangée */
      } else if (cx < 0 || cy < 0 || cx > innerWidth || cy > innerHeight)
        injoignables.push(cle(e) + ' (hors de la fenêtre)');
      else {
        const h = document.elementFromPoint(cx, cy);
        if (!h || !(h === e || e.contains(h)))
          injoignables.push(
            cle(e) + ' ← ' + (h ? cle(h) : 'rien') + ' au centre (' + Math.round(cx) + ',' + Math.round(cy) + ')',
          );
      }
    }
    if (e.matches('input:not([type=hidden]), textarea, [contenteditable=""], [contenteditable=true]')) champs++;
    // DÉBORDEMENT (redteam_ecrans, DEBORDE) : rien ne sort de l'appareil, sauf une rangée qui défile et le déclare (data-glisse)
    if (e !== dv && c.position !== 'fixed' && r.width >= 2 && r.height >= 2) {
      if (r.right > D.right + 2 || r.left < D.left - 2 || r.bottom > D.bottom + 2 || r.top < D.top - 2) {
        const g = e.closest('[data-glisse]');
        let excuse = false;
        if (g && g !== e) {
          const gr = g.getBoundingClientRect();
          const ov = getComputedStyle(g).overflowX;
          excuse = gr.left >= D.left - 2 && gr.right <= D.right + 2 && /hidden|auto|scroll/.test(ov);
        }
        if (!excuse) deborde.push(cle(e) + ' ' + JSON.stringify(pt(r)));
      }
    }
    // FILETS (redteam_filets, 1) : un trait HORIZONTAL large (≥ la moitié de l'écran), hors d'une pastille ou d'une boîte
    if (r.width >= 40 && !sanctionne(e)) {
      const radius = parseFloat(c.borderTopLeftRadius) || 0;
      const box4 = parseFloat(c.borderLeftWidth) >= 0.5 && parseFloat(c.borderRightWidth) >= 0.5;
      const largeur = r.width / D.width;
      if (!(radius >= 40 || box4) && largeur >= 0.5) {
        for (const s of ['Top', 'Bottom']) {
          const w = parseFloat((c as unknown as Record<string, string>)['border' + s + 'Width']!);
          const col = (c as unknown as Record<string, string>)['border' + s + 'Color']!;
          if (w >= 0.5 && col && !/,\s*0\)\s*$/.test(col))
            filets.push(cle(e) + ' border' + s + ' ' + String(w) + 'px ' + col);
        }
        const m = c.boxShadow.match(/(?:rgba?\([^)]*\)|#\w+)\s+0px\s+(-?[\d.]+)px\s+0px/);
        if (m && Math.abs(parseFloat(m[1]!)) >= 0.5) filets.push(cle(e) + ' ombre ' + c.boxShadow.slice(0, 40));
      }
    }
    // LEXIQUE (redteam_lexique) : A les termes bannis ; B la loi des points
    for (const d of [texte, e.getAttribute('aria-label') ?? '', e.getAttribute('placeholder') ?? '']) {
      if (!d) continue;
      const bas = d.toLowerCase();
      for (const b of BANNIS) {
        const re = new RegExp(
          '(^|[^a-zàâçéèêëîïôûùüÿœ])' + b.replace(/[-]/g, '[- ]?') + '(s?)($|[^a-zàâçéèêëîïôûùüÿœ])',
        );
        if (re.test(bas)) termes.push(b + ' ← « ' + d.slice(0, 60) + ' » (' + cle(e) + ')');
      }
      if (/^\s*échéance\s*:?\s*$/i.test(d)) termes.push('échéance (libellé de champ) ← « ' + d + ' »');
    }
    if (!e.closest('.dz-tailles')) {
      if (texte && /^[\s·.•‧∙⋅●○]+$/.test(texte) && (texte.match(/[·.•‧∙⋅●○]/g) ?? []).length >= 2)
        points.push('texte de points ' + cle(e) + ' « ' + texte.slice(0, 20) + ' »');
      if (!texte && !e.children.length && !/^(CANVAS|INPUT|TEXTAREA)$/.test(e.tagName)) {
        const w = r.width / k;
        const h = r.height / k;
        const bg = c.backgroundColor;
        const plein = bg && bg !== 'rgba(0, 0, 0, 0)' && c.backgroundImage === 'none';
        const rond = parseFloat(c.borderTopLeftRadius) >= Math.min(r.width, r.height) / 2 - 0.6;
        if (plein && rond && w <= 14 && h <= 14 && w >= 2 && Math.abs(w - h) <= 1) points.push('point ' + cle(e));
      }
    }
  }

  // L'AIR (redteam_air, MESURE) : les blocs de texte, rectangle du TEXTE (Range : ascendantes et descendantes), dans la feuille du dessus
  // (celle qui couvre au moins 55 % de l'appareil et porte des mots ; sinon l'appareil)
  const EN_LIGNE = ['B', 'I', 'EM', 'STRONG', 'SPAN', 'SMALL', 'BR', 'U', 'A', 'CODE', 'SUP', 'SUB'];
  let hote: Element = dv;
  let best = -1;
  const ordre = [...document.querySelectorAll('*')];
  dv.querySelectorAll('[id]').forEach((e) => {
    const c = getComputedStyle(e);
    if (c.display === 'none' || c.visibility === 'hidden' || +c.opacity < 0.5) return;
    const r = e.getBoundingClientRect();
    // la part VISIBLE de l'appareil (un écran fermé, glissé hors champ, garde sa taille : il ne couvre rien)
    const ix = Math.max(0, Math.min(r.right, D.right) - Math.max(r.left, D.left));
    const iy = Math.max(0, Math.min(r.bottom, D.bottom) - Math.max(r.top, D.top));
    const part = (ix * iy) / (D.width * D.height);
    if (part < 0.55 || part > 1.02) return;
    // une feuille qui porte des mots VISIBLES (le #stage du prototype garde les textes cachés de l'onboarding)
    const wk = document.createTreeWalker(e, NodeFilter.SHOW_TEXT);
    let porte = false;
    for (let t = wk.nextNode(); t && !porte; t = wk.nextNode())
      if ((t.nodeValue ?? '').trim() && t.parentElement && vu(t.parentElement)) porte = true;
    if (!porte) return;
    const rang = (+c.zIndex || 0) * 1000 + ordre.indexOf(e) / 1e6;
    if (rang >= best) {
      best = rang;
      hote = e;
    }
  });
  const COLLANT = ['dpdTog', 'dpDetails'];
  const blocs: BlocR[] = [];
  hote.querySelectorAll('*').forEach((e) => {
    const c = getComputedStyle(e);
    if (c.display === 'none' || c.visibility === 'hidden' || opEff(e) < 0.05) return;
    for (let n: Element | null = e; n && n !== hote; n = n.parentElement) if (n.id && COLLANT.includes(n.id)) return;
    // seulement le texte RENDU (un nom caché sous une icône, `display:none`, n'est pas un bloc : le #shareBtn du prototype en porte un)
    const vis = (q: Element): string => {
      const wk = document.createTreeWalker(q, NodeFilter.SHOW_TEXT);
      let s = '';
      for (let x = wk.nextNode(); x; x = wk.nextNode())
        if (x.parentElement && vu(x.parentElement)) s += x.nodeValue ?? '';
      return s.trim();
    };
    const t = vis(e);
    if (!t) return;
    for (const q of e.children) if (!EN_LIGNE.includes(q.tagName) && vis(q)) return;
    // le rectangle du TEXTE : la réunion des rectangles de ses nœuds de texte rendus (Range)
    let x0 = Infinity;
    let y0 = Infinity;
    let x1 = -Infinity;
    let y1 = -Infinity;
    const wk = document.createTreeWalker(e, NodeFilter.SHOW_TEXT);
    for (let x = wk.nextNode(); x; x = wk.nextNode()) {
      if (!(x.nodeValue ?? '').trim() || !x.parentElement || !vu(x.parentElement)) continue;
      const rg = document.createRange();
      rg.selectNodeContents(x);
      const q = rg.getBoundingClientRect();
      if (!(q.width > 0 && q.height > 0)) continue;
      x0 = Math.min(x0, q.left);
      y0 = Math.min(y0, q.top);
      x1 = Math.max(x1, q.right);
      y1 = Math.max(y1, q.bottom);
    }
    if (!isFinite(x0)) return;
    const r = { left: x0, top: y0, width: x1 - x0, height: y1 - y0 };
    const b = pt(r);
    if (b[2] < 12 || b[3] < 6 || b[1] < -40 || b[1] > 884) return;
    blocs.push({
      cle: idAncetre(e) + '«' + t.replace(/\s+/g, ' ').slice(0, 20) + '»',
      x: b[0],
      y: b[1],
      w: b[2],
      h: b[3],
    });
  });

  // LA SUPERPOSITION (redteam_superpo) : deux textes visibles qui se recouvrent, confirmés AU DOIGT (la pile coupée au premier fond opaque)
  const tx: Array<{ e: Element; t: string; x: number; y: number; w: number; h: number }> = [];
  for (const e of dv.querySelectorAll('*')) {
    const c = getComputedStyle(e);
    if (c.display === 'none' || c.visibility === 'hidden' || opEff(e) < 0.05) continue;
    const t = texteDe(e);
    if (!t) continue;
    const r = e.getBoundingClientRect();
    if (r.width < 4 || r.height < 4) continue;
    const b = pt(r);
    if (b[1] + b[3] < 0 || b[1] > 844) continue;
    tx.push({ e, t: t.slice(0, 18), x: b[0], y: b[1], w: b[2], h: b[3] });
  }
  const superpo: string[] = [];
  for (let i = 0; i < tx.length; i++)
    for (let j = i + 1; j < tx.length; j++) {
      const a = tx[i]!;
      const b = tx[j]!;
      if (a.e.contains(b.e) || b.e.contains(a.e)) continue;
      const ox = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x);
      const oy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
      if (ox <= 3 || oy <= 3) continue;
      const cx = Math.max(a.x, b.x) + ox / 2;
      const cy = Math.max(a.y, b.y) + oy / 2;
      let pile = document.elementsFromPoint(D.left + cx * k, D.top + cy * k);
      let sol = pile.length;
      for (let z = 0; z < pile.length; z++) {
        const m = getComputedStyle(pile[z]!).backgroundColor.match(/[\d.]+/g);
        if (m && (m.length < 4 || +m[3]! > 0.92)) {
          sol = z;
          break;
        }
      }
      pile = pile.slice(0, sol + 1);
      const vuA = pile.some((z) => z === a.e || a.e.contains(z));
      const vuB = pile.some((z) => z === b.e || b.e.contains(z));
      if (vuA && vuB)
        superpo.push('« ' + a.t + ' » ⨯ « ' + b.t + ' » ' + Math.round(ox) + '×' + Math.round(oy) + ' pt');
    }
  return {
    noeuds,
    blocs,
    interactifs,
    injoignables,
    deborde,
    filets,
    termes,
    points,
    volumes,
    superpo,
    champs,
  };
}

/** l'écran posé : plus aucun nœud qui naît ou disparaît depuis deux relevés (redteam_air, `releve`), 5 s au plus */
async function stable(page: Page): Promise<void> {
  await page.evaluate(async () => {
    await document.fonts.ready;
    const compte = (): number =>
      [...document.querySelectorAll('#device *')].filter((e) => {
        const r = e.getBoundingClientRect();
        return r.width > 4 && r.height > 4;
      }).length;
    let prec = -1;
    let n = 0;
    const t0 = performance.now();
    while (n < 2 && performance.now() - t0 < 5000) {
      await new Promise((f) => setTimeout(f, 250));
      const c = compte();
      n = c === prec ? n + 1 : 0;
      prec = c;
    }
    // et plus rien ne se trace ni ne passe (un texte en cours de tracé est découpé : il n'est pas encore à l'écran), aucune transition
    // finie ne court — hors du Mac une image dure 0,7 s et ces minuteurs finissent bien après le compte des nœuds (30 s au plus)
    const calme = (): boolean => {
      const w = window as unknown as { TraceLettres?: { actif(): boolean } };
      if (w.TraceLettres?.actif() || document.querySelector('[data-flaques-mode]')) return false;
      return !document.getAnimations().some((a) => {
        if (a.playState !== 'running') return false;
        const t = (a.effect as KeyframeEffect | null)?.target;
        return (
          t instanceof Element &&
          !!t.closest('#device') &&
          (a.effect as KeyframeEffect).getTiming().iterations !== Infinity
        );
      });
    };
    const t1 = performance.now();
    let ok = 0;
    while (ok < 2 && performance.now() - t1 < 30000) {
      await new Promise((f) => setTimeout(f, 250));
      ok = calme() ? ok + 1 : 0;
    }
  });
}

/** tout ce qui n'est pas du texte rendu transparent, sur un fond plat (redteam_aspect, B : « la phrase seule ») */
const FOND_PLAT = '#7f7f7f';
// (la page + du prototype vit HORS de #device, dans .frame : elle est nommée ; et ce qu'un écran opaque recouvre — l'accueil sous la page +,
// marqué au relevé `data-recouvert` — n'est pas à l'écran : on le cache, sinon il reparaîtrait sous les fonds devenus transparents)
/** les fonds posés EN LIGNE avec `important` (le prototype en pose : la pastille du verbe, les pointillés, la barre Peaufiner) ne cèdent pas
 *  à une feuille : ils sont retirés en ligne, des deux côtés */
const TEXTES_SEULS_LIGNE = `(() => { for (const e of document.querySelectorAll('#device *, #createSheet, #createSheet *')) {
  for (const [p, v] of [['background-color', 'transparent'], ['background-image', 'none'], ['border-color', 'transparent'],
    ['box-shadow', 'none'], ['outline-color', 'transparent'], ['filter', 'none']]) e.style.setProperty(p, v, 'important'); } })()`;
const TEXTES_SEULS =
  '#device *,#device *::before,#device *::after,#createSheet#createSheet#createSheet,#createSheet#createSheet#createSheet *,' +
  '#createSheet#createSheet#createSheet *::before,#createSheet#createSheet#createSheet *::after' +
  '{background:transparent!important;background-image:none!important;' +
  'border-color:transparent!important;box-shadow:none!important;outline-color:transparent!important;filter:none!important}' +
  '#device svg,#device canvas,#device img,#createSheet#createSheet#createSheet :is(svg,canvas,img){visibility:hidden!important}' +
  '[data-recouvert]{visibility:hidden!important}#device::before,#device::after{display:none!important}' +
  `html,body,.frame,#device{background:${FOND_PLAT}!important}`;

type Rel = Releve & { png: Buffer; pngTextes: Buffer; erreurs: string[]; filetsCanevas: string[] };
const memo = new Map<string, Promise<Rel>>();

async function releveApp(browser: Browser, theme: Theme, e: EcranPorte): Promise<Rel> {
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3 });
  try {
    const page = await ctx.newPage();
    const erreurs: string[] = [];
    page.on('pageerror', (x) => erreurs.push(String(x)));
    await page.addInitScript(piegeEcouteurs);
    await page.addInitScript(piegeFilets);
    await vraieApp(page, lsDe(theme));
    await e.ouvrir(page);
    await poserSondeReleve(page);
    await stable(page);
    const r = await page.evaluate(releverDansPage);
    const filetsCanevas = (await page.evaluate('window.__filets || []')) as string[];
    await page.addStyleTag({ content: GEL });
    await page.waitForTimeout(400);
    const png = await page.screenshot();
    await page.addStyleTag({ content: TEXTES_SEULS });
    await page.evaluate(TEXTES_SEULS_LIGNE);
    await page.waitForTimeout(250);
    const pngTextes = await page.screenshot();
    return { ...r, png, pngTextes, erreurs, filetsCanevas };
  } finally {
    await ctx.close();
  }
}

async function releveProto(browser: Browser, theme: Theme, e: EcranPorte): Promise<Rel> {
  const ctx = await browser.newContext({ viewport: { width: 430, height: 932 }, deviceScaleFactor: 3 });
  try {
    const page = await ctx.newPage();
    await prototype(page, lsDe(theme));
    await e.prototype(page);
    await stable(page);
    const r = await page.evaluate(releverDansPage);
    const dv = await page.evaluate(() => {
      const q = document.getElementById('device')!.getBoundingClientRect();
      return { x: q.left, y: q.top, width: q.width, height: q.height };
    });
    await page.addStyleTag({ content: GEL });
    await page.waitForTimeout(400);
    const png = await page.screenshot({ clip: dv });
    await page.addStyleTag({ content: TEXTES_SEULS });
    await page.evaluate(TEXTES_SEULS_LIGNE);
    await page.waitForTimeout(250);
    const pngTextes = await page.screenshot({ clip: dv });
    return { ...r, png, pngTextes, erreurs: [], filetsCanevas: [] };
  } finally {
    await ctx.close();
  }
}

function releve(browser: Browser, cote: 'app' | 'proto', theme: Theme, e: EcranPorte): Promise<Rel> {
  const k = `${cote}|${theme}|${e.nom}|${process.env['PROMI_SONDE'] ?? ''}`;
  let p = memo.get(k);
  if (!p) {
    p = cote === 'app' ? releveApp(browser, theme, e) : releveProto(browser, theme, e);
    memo.set(k, p);
  }
  return p;
}

/** chaque (écran porté, thème) : le relevé de la vraie app, et celui du prototype si on le demande */
async function parcours(
  browser: Browser,
  avecProto: boolean,
  f: (x: { nom: string; app: Rel; proto: Rel | null }) => void,
): Promise<void> {
  for (const theme of THEMES)
    for (const e of ECRANS_PORTES) {
      const [app, proto] = await Promise.all([
        releve(browser, 'app', theme, e),
        avecProto ? releve(browser, 'proto', theme, e) : Promise.resolve(null),
      ]);
      f({ nom: `${e.nom}, ${theme}`, app, proto });
    }
}

const parCle = (r: Rel): Map<string, NoeudR> => new Map(r.noeuds.map((n) => [n.cle, n]));

// ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
// PIXELS ET COULEURS
// ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
type RGB = [number, number, number];
const hex = (h: string): RGB => {
  const s = h.replace('#', '');
  return [parseInt(s.slice(0, 2), 16), parseInt(s.slice(2, 4), 16), parseInt(s.slice(4, 6), 16)];
};
const rgbCss = (h: string): string => {
  const [r, g, b] = hex(h);
  return `rgb(${String(r)}, ${String(g)}, ${String(b)})`;
};
function lab(c: RGB): [number, number, number] {
  const f = (v: number): number => {
    const x = v / 255;
    return x <= 0.04045 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4;
  };
  const [r, g, b] = [f(c[0]), f(c[1]), f(c[2])];
  const X = r * 0.4124564 + g * 0.3575761 + b * 0.1804375;
  const Y = r * 0.2126729 + g * 0.7151522 + b * 0.072175;
  const Z = r * 0.0193339 + g * 0.119192 + b * 0.9503041;
  const q = (t: number): number => (t > 216 / 24389 ? Math.cbrt(t) : (841 / 108) * t + 4 / 29);
  const fx = q(X / 0.95047);
  const fy = q(Y);
  const fz = q(Z / 1.08883);
  return [116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)];
}
const deltaE = (a: RGB, b: RGB): number => {
  const A = lab(a);
  const B = lab(b);
  return Math.hypot(A[0] - B[0], A[1] - B[1], A[2] - B[2]);
};
function pixel(img: PNG, xPt: number, yPt: number): RGB {
  const k = img.width / 390;
  const x = Math.min(img.width - 1, Math.max(0, Math.round(xPt * k)));
  const y = Math.min(img.height - 1, Math.max(0, Math.round(yPt * k)));
  const i = (y * img.width + x) * 4;
  return [img.data[i]!, img.data[i + 1]!, img.data[i + 2]!];
}
/** la couleur la plus fréquente d'une boîte (en points), hors des couleurs à `ecartDe` (ΔE < 6) */
function dominante(img: PNG, b: Boite, ecartDe: RGB[]): RGB | null {
  const k = img.width / 390;
  const n = new Map<string, number>();
  for (let y = Math.floor(b[1] * k); y < Math.ceil((b[1] + b[3]) * k); y++)
    for (let x = Math.floor(b[0] * k); x < Math.ceil((b[0] + b[2]) * k); x++) {
      if (x < 0 || y < 0 || x >= img.width || y >= img.height) continue;
      const i = (y * img.width + x) * 4;
      const c: RGB = [img.data[i]!, img.data[i + 1]!, img.data[i + 2]!];
      if (ecartDe.some((z) => deltaE(z, c) < 6)) continue;
      const s = c.join(',');
      n.set(s, (n.get(s) ?? 0) + 1);
    }
  let m: string | null = null;
  let v = 0;
  for (const [s, q] of n)
    if (q > v) {
      v = q;
      m = s;
    }
  return m ? (m.split(',').map(Number) as RGB) : null;
}

// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// 1 · redteam_couleurs_ref — LES COULEURS SONT CELLES DE LA RÉFÉRENCE (v121 : « toutes les couleurs de tous les écrans, dans les deux
//     thèmes, identiques » à la référence ; la vraie app : la référence est le prototype ACTUEL, CLAUDE.md « IDENTIQUE AU PROTOTYPE »).
//     Les styles calculés de chaque nœud visible, mêmes nœuds des deux côtés (par leur id, sinon par leur place sous l'id le plus proche) :
//     encre et remplissage d'un texte, fond, image de fond, bordures, contour, fill / stroke d'un dessin, ombres, filtre ; et les
//     pseudo-éléments (::before, ::after) qui peignent. Exception NOMMÉE, en dur : E1 — le CONTENU des canevas de la Toile (le moteur
//     repris, jugé au pixel par banc-rendu.spec). Un nœud qui n'existe que d'un côté n'est pas un écart de couleur : il est LISTÉ.
// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
const COULEURS_TEXTE = ['color', 'webkitTextFillColor'];
const COULEURS_TOUJOURS = ['backgroundColor', 'backgroundImage', 'boxShadow', 'textShadow', 'filter'];
const DESSIN = /^(svg|path|circle|rect|line|polyline|polygon|ellipse|g|use)$/;
/** LES EXCEPTIONS NOMMÉES (en dur, CLAUDE.md §7 — rien d'autre n'est toléré) :
 *  E2 · le CADRE DE TÉLÉPHONE que le prototype dessine autour de son appareil (l'ombre de `#device`) : la vraie app n'en a pas, elle est
 *       l'écran (base.css : « sans le cadre de téléphone que Safari dessinait » ; accueil.spec excepte de même les coins du téléphone) ;
 *  E3 · le `fill` du tracé du + de l'accueil : deux segments qui se croisent, sans surface — rien n'est rempli, quelle que soit la valeur
 *       (le prototype hérite du noir, la vraie app pose `none` ; l'identité au pixel d'accueil.spec le confirme). */
const EXCEPTIONS_COULEURS = ['#device boxShadow', '#createBtn>svg:0>path:0 fill'];

test('couleurs : chaque écran porté a les couleurs du prototype, nœud par nœud (styles calculés), clair et sombre', async ({
  browser,
}) => {
  const ecarts: string[] = [];
  const seuls: string[] = [];
  let compares = 0;
  await parcours(browser, true, ({ nom, app, proto }) => {
    const P = parCle(proto!);
    const A = parCle(app);
    for (const [cle, a] of A) {
      const p = P.get(cle);
      if (!p) {
        seuls.push(`${nom} : ${cle} (la vraie app seule)`);
        continue;
      }
      compares++;
      const props = [...COULEURS_TOUJOURS];
      if (a.texte || p.texte) props.push(...COULEURS_TEXTE);
      if (DESSIN.test(a.tag)) props.push('fill', 'stroke');
      for (const s of ['Top', 'Right', 'Bottom', 'Left'])
        if (parseFloat(a.st[`border${s}Width`] ?? '0') > 0 || parseFloat(p.st[`border${s}Width`] ?? '0') > 0)
          props.push(`border${s}Color`, `border${s}Width`);
      if (a.st['outlineStyle'] !== 'none' || p.st['outlineStyle'] !== 'none')
        props.push('outlineStyle', 'outlineColor');
      for (const q of props)
        if (a.st[q] !== p.st[q] && !EXCEPTIONS_COULEURS.includes(`${cle} ${q}`))
          ecarts.push(`${nom} : ${cle} ${q} ${String(p.st[q]).slice(0, 90)} → ${String(a.st[q]).slice(0, 90)}`);
      for (const q of new Set([...Object.keys(a.ps), ...Object.keys(p.ps)])) {
        // une bordure de pseudo-élément ne peint que si elle a une épaisseur
        if (q.endsWith('borderTopColor')) {
          const w = q.replace('Color', 'Width');
          if (!(parseFloat(a.ps[w] ?? '0') > 0) && !(parseFloat(p.ps[w] ?? '0') > 0)) continue;
        }
        if (EXCEPTIONS_COULEURS.includes(`${cle}${q}`)) continue;
        if (a.ps[q] !== p.ps[q])
          ecarts.push(`${nom} : ${cle}${q} ${String(p.ps[q]).slice(0, 90)} → ${String(a.ps[q]).slice(0, 90)}`);
      }
    }
    for (const cle of P.keys()) if (!A.has(cle)) seuls.push(`${nom} : ${cle} (le prototype seul)`);
  });
  test.info().annotations.push({ type: 'nœuds d’un seul côté (listés, pas jugés)', description: seuls.join(' · ') });
  expect(compares, 'des nœuds comparés').toBeGreaterThan(40);
  expect(ecarts, 'les couleurs rendues, contre le prototype').toEqual([]);
});

// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// 2 · redteam_decisions — CHAQUE DÉCISION DE COULEUR DE TOM, EN DUR AVEC SA SOURCE, CONFRONTÉE À L'ÉCRAN RENDU (v122). Pour la vraie
//     app au lot 1 : les zones de l'accueil et de son menu du + que Tom a décidées. Là où une zone n'a AUCUNE décision, elle n'est pas
//     jugée ici : c'est le juge des couleurs (1) qui la tient au prototype. Lu sur les styles calculés, et sur l'IMAGE là où le pixel est
//     exact (le plateau passe au-dessus du grain de l'appareil, v203 : son fond et le I de PROMI).
// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
const CREME = '#F7F0DE';
const ENCRE = '#201908';
const SEICHE = '#050302';
type Decision = { theme: Theme; menu: boolean; sel: string; prop: string; pseudo?: string; val: string; src: string };
const DECISIONS: Decision[] = [];
for (const theme of THEMES) {
  const s = theme === 'sombre';
  const D = (d: Omit<Decision, 'theme' | 'menu'>, menu = false): void => {
    DECISIONS.push({ theme, menu, ...d });
  };
  D({
    sel: '#accPlat',
    prop: 'backgroundColor',
    val: s ? SEICHE : CREME,
    src: s
      ? 'v116 + v121 (Tom, 3 oct. 2026) : la seiche #050302 dans les pages'
      : '§3 : #F7F0DE, le fond du mode clair',
  });
  D({
    sel: '#accPlat',
    prop: 'borderTopColor',
    val: s ? CREME : ENCRE,
    src: 'grammaire des contours (Tom, 2 sept. 2026) : trait de 2 px à l’encre du mode ; 17 sept. : l’encre #201908 en clair',
  });
  D({
    sel: '#accPlat .acc-mm',
    prop: 'color',
    val: s ? CREME : ENCRE,
    src: '17 sept. 2026 : le texte du plateau à l’encre en clair (redteam_decisions « motMarque »)',
  });
  D({
    sel: '#accPlat .acc-mm i',
    prop: 'color',
    val: '#82AEF8',
    src: 'C-281 (v203 clôture) : le I de PROMI est le bleu clair exact #82AEF8, dans les deux thèmes',
  });
  D({
    sel: '#accBarre',
    prop: 'backgroundColor',
    val: s ? SEICHE : CREME,
    src: s ? 'v116 + v121 : la seiche dans les pages' : '§3 : #F7F0DE, le fond du mode clair',
  });
  for (const id of ['studioBtn', 'souffleBtn', 'indexBtn', 'filBtn'])
    D({
      sel: `#${id} .l`,
      prop: 'color',
      val: s ? CREME : '#022140',
      src: 'v146 §5–§7 : les noms sous les icônes de l’accueil en #022140 en clair ; en sombre, la crème',
    });
  D({
    sel: '#createBtn svg path',
    prop: 'stroke',
    val: '#FB4C0D',
    src: 'v146 (le + de l’accueil, son signe en orange) ; D6 v173 (C-210) : #FB4C0D, le seul orange',
  });
  D({
    sel: '#filDot',
    prop: 'backgroundColor',
    val: '#FB4C0D',
    src: 'D6 v173 (C-210) : l’orange marque ce qui attend un geste — la pastille du Fil',
  });
  D({
    sel: '#accRecadre',
    prop: 'color',
    val: s ? CREME : ENCRE,
    src: 'C-188 (v163a) : le symbole « recadrer », l’encre du mode',
  });
  D(
    {
      sel: '#accChoix .acc-pil[data-k="nuee"]',
      prop: 'backgroundColor',
      val: '#C9A8F5',
      src: '17 sept. 2026, planche des correspondances : le lilas d’un Cercle',
    },
    true,
  );
  D(
    {
      sel: '#accChoix .acc-pil[data-k="chiche"]',
      prop: 'backgroundColor',
      val: '#FFB8D2',
      src: '17 sept. 2026 : le rose d’un Chiche',
    },
    true,
  );
  D(
    {
      sel: '#accChoix .acc-pil[data-k="promi"]',
      prop: 'backgroundColor',
      val: '#82AEF8',
      src: '17 sept. 2026 : le bleu d’un Promi',
    },
    true,
  );
  D(
    {
      sel: '#accChoix .acc-pil[data-k="nuee"] .acc-nat',
      prop: 'color',
      val: '#291547',
      src: '17 sept. 2026 : « le violet : trait et texte posés sur le lilas d’un Cercle »',
    },
    true,
  );
  for (const k of ['chiche', 'promi'])
    D(
      {
        sel: `#accChoix .acc-pil[data-k="${k}"] .acc-nat`,
        prop: 'color',
        val: s ? SEICHE : ENCRE,
        src: '17 sept. 2026 : le texte posé sur un champ pastel passe à l’encre #201908 — rendue seiche en sombre (v116, v121)',
      },
      true,
    );
  if (s)
    for (const k of ['nuee', 'chiche', 'promi'])
      D(
        {
          sel: `#accChoix .acc-pil[data-k="${k}"]`,
          prop: 'borderTopColor',
          val: CREME,
          src: 'v179b (C-230) : les encarts du menu du +, contour crème 2 pt',
        },
        true,
      );
}

test('décisions de couleur de Tom : l’accueil et son menu du + rendus aux valeurs décidées, clair et sombre', async ({
  browser,
}) => {
  const fautes: string[] = [];
  for (const theme of THEMES) {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3 });
    const page = await ctx.newPage();
    await vraieApp(page, lsDe(theme));
    if (sonde('decisions-i')) await page.addStyleTag({ content: '#device .acc-mm i{color:#4971B6!important}' });
    for (const menu of [false, true]) {
      if (menu) await ouvrirPlus(page);
      const lus = (await page.evaluate(
        (L) =>
          L.map((d) => {
            const e = document.querySelector(d.sel);
            if (!e) return null;
            return (getComputedStyle(e) as unknown as Record<string, string>)[d.prop] ?? null;
          }),
        DECISIONS.filter((d) => d.theme === theme && d.menu === menu).map((d) => ({ sel: d.sel, prop: d.prop })),
      )) as Array<string | null>;
      DECISIONS.filter((d) => d.theme === theme && d.menu === menu).forEach((d, i) => {
        if (lus[i] !== rgbCss(d.val))
          fautes.push(`${theme} ${d.sel} ${d.prop} : ${String(lus[i])} ≠ ${d.val} (${d.src})`);
      });
    }
    // L'ANNEAU DU + : ses arcs ne portent que les deux états (Q262, 22 sept. 2026 : « #00341A, #291547, exactement celles-là » ; v173
    // C-210 : deux états, deux arcs au plus) — lus dans l'image que le pseudo-élément peint
    const anneau = (await page.evaluate(
      () => getComputedStyle(document.getElementById('createBtn')!, '::before').backgroundImage,
    )) as string;
    const traits = [...decodeURIComponent(anneau).matchAll(/stroke=["']?(#[0-9a-fA-F]{6})/g)].map((m) =>
      m[1]!.toUpperCase(),
    );
    if (!traits.length || traits.some((t) => !['#00341A', '#291547'].includes(t)))
      fautes.push(`${theme} l’anneau du + : arcs ${JSON.stringify(traits)} (Q262 ; v173, C-210)`);
    // sur l'image : le fond du plateau (exact, au-dessus du grain) et le cœur du I (C-281 : « à 1,5 près »)
    await page.addStyleTag({ content: GEL });
    await page.waitForTimeout(300);
    const img = PNG.sync.read(await page.screenshot());
    const fondPlat = pixel(img, 34, 70);
    const attenduFond = hex(theme === 'sombre' ? SEICHE : CREME);
    if (deltaE(fondPlat, attenduFond) > 1)
      fautes.push(
        `${theme} le fond du plateau, lu sur l’image : rgb(${fondPlat.join(',')}) ≠ ${theme === 'sombre' ? SEICHE : CREME}`,
      );
    const bI = (await page.evaluate(() => {
      const r = document.querySelector('#accPlat .acc-mm i')!.getBoundingClientRect();
      return [r.left, r.top, r.width, r.height];
    })) as Boite;
    const coeur = dominante(img, bI, [attenduFond]);
    const i0 = hex('#82AEF8');
    if (!coeur || Math.max(...coeur.map((v, j) => Math.abs(v - i0[j]!))) > 1.5)
      fautes.push(
        `${theme} le cœur du I, lu sur l’image : ${coeur ? `rgb(${coeur.join(',')})` : 'aucun'} ≠ #82AEF8 (C-281)`,
      );
    await ctx.close();
  }
  expect(fautes).toEqual([]);
});

// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// 3 · redteam_joignable — CE QUI SE TOUCHE EST JOIGNABLE (v118, Tom, 2 oct. 2026). A · au rendu : pour chaque élément interactif
//     visible (bouton, lien, champ, [role=button], ou qui écoute un toucher — piégé avant le chargement), `elementFromPoint` AU CENTRE
//     rend l'élément ou un de ses descendants. Aucune dette : la vraie app naît sans. (B, « chaque fonction appelée existe », est tenue
//     par le compilateur : TypeScript strict, `npm run types` à chaque commit ; et aucun gestionnaire en attribut `on…=""` dans les
//     sources, compté ici.)
// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
function sources(dir: string, ext: RegExp, hors = /[\\/]repris[\\/]/): Array<{ f: string; s: string }> {
  const out: Array<{ f: string; s: string }> = [];
  for (const n of readdirSync(dir)) {
    const p = join(dir, n);
    if (hors.test(p)) continue;
    if (statSync(p).isDirectory()) out.push(...sources(p, ext, hors));
    else if (ext.test(n)) out.push({ f: p, s: readFileSync(p, 'utf8') });
  }
  return out;
}

test('joignable : chaque élément qui se touche reçoit le doigt en son centre, sur chaque écran porté', async ({
  browser,
}) => {
  const fautes: string[] = [];
  let n = 0;
  await parcours(browser, false, ({ nom, app }) => {
    n += app.interactifs.length;
    for (const x of app.injoignables) fautes.push(`${nom} : ${x}`);
  });
  const attributs = sources(SRC, /\.(ts|html)$/).flatMap(({ f, s }) =>
    [...s.matchAll(/\son(click|pointer\w+|touch\w+|mouse\w+)\s*=\s*["']/g)].map((m) => `${f} : on${m[1]!}=""`),
  );
  expect(n, 'des éléments interactifs relevés').toBeGreaterThan(8);
  expect(fautes, 'injoignables au doigt').toEqual([]);
  expect(attributs, 'aucun gestionnaire en attribut on…=""').toEqual([]);
});

// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// 4 · redteam_ecrans — CHAQUE ÉCRAN S'OUVRE, SES ÉLÉMENTS CLÉS, SA GÉOMÉTRIE, CLAIR ET SOMBRE.
//     (a) transversal : chaque écran porté s'ouvre sans erreur de page et rien ne sort de l'appareil (DEBORDE : sauf une rangée qui défile
//         et le déclare, `data-glisse`, Q128 §3) ;
//     (b) les contrôles de l'accueil et de la Toile du juge : la Toile remplit l'écran et porte des dalles colorées, `hit()` ignore les
//         cellules grises et désigne un Promi planté, planter garde la densité ; un seul Fil, dans la barre, avec sa pastille qui s'allume
//         sur ce qui attend un geste (Q347) ; l'anneau du + porte la part des tenues (± 1,5°) ; il tourne lentement (≥ 40 s).
// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
test('écrans : chaque écran porté s’ouvre sans erreur et rien ne sort de l’appareil, clair et sombre', async ({
  browser,
}) => {
  const fautes: string[] = [];
  await parcours(browser, false, ({ nom, app }) => {
    for (const x of app.erreurs) fautes.push(`${nom} : erreur de page ${x}`);
    if (app.noeuds.filter((q) => q.texte).length === 0)
      fautes.push(`${nom} : aucun texte visible (l’écran ne s’est pas ouvert)`);
    for (const x of app.deborde) fautes.push(`${nom} : déborde ${x}`);
  });
  expect(fautes).toEqual([]);
});

type EtatProto = { promises: Array<Record<string, unknown>>; FEED?: Array<Record<string, unknown>> } & Record<
  string,
  unknown
>;
function avecEtat(ls: Record<string, string>, f: (st: EtatProto) => void): Record<string, string> {
  const st = JSON.parse(ls['promi_state'] ?? '{"promises":[]}') as EtatProto;
  f(st);
  return { ...ls, promi_state: JSON.stringify(st) };
}

test('écrans : l’accueil — la Toile, le Fil et sa pastille, l’anneau du + (redteam_ecrans)', async ({ browser }) => {
  const fautes: string[] = [];
  const ok = (n: string, c: boolean, d: unknown = ''): void => {
    if (!c) fautes.push(`${n}${d === '' ? '' : ' — ' + JSON.stringify(d)}`);
  };
  const ouvre = async (
    ls: Record<string, string>,
  ): Promise<{ page: Page; erreurs: string[]; fin(): Promise<void> }> => {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
    const page = await ctx.newPage();
    const erreurs: string[] = [];
    page.on('pageerror', (x) => erreurs.push(String(x)));
    await vraieApp(page, ls);
    if (sonde('ecrans-pastille')) await page.addStyleTag({ content: '#filDot{display:none!important}' });
    return { page, erreurs, fin: () => ctx.close() };
  };
  const ls0 = stockage();
  {
    const { page, erreurs, fin } = await ouvre(ls0);
    // les dalles colorées : la Toile lue jusqu'à 60 s, le meilleur relevé gardé (sur l'intégration continue, une image toutes les 0,7 s, et
    // un relevé pris à un instant tombait sur un canevas pas encore repeint)
    const colMax = (await page.evaluate(async () => {
      let m = 0;
      const t0 = performance.now();
      while (performance.now() - t0 < 60000) {
        const c = document.getElementById('toileCv') as HTMLCanvasElement;
        const im = c.getContext('2d')!.getImageData(0, 0, c.width, c.height).data;
        let col = 0;
        for (let i = 0; i < im.length; i += 400)
          if (Math.abs(im[i]! - im[i + 1]!) > 18 || Math.abs(im[i + 1]! - im[i + 2]!) > 18) col++;
        m = Math.max(m, col);
        if (m > 30) break;
        await new Promise((f) => setTimeout(f, 250));
      }
      return m;
    })) as number;
    const t = (await page.evaluate(`(() => {
      const c = document.getElementById('toileCv'), d = document.getElementById('device').getBoundingClientRect(), r = c.getBoundingClientRect();
      const g = c.getContext('2d'), im = g.getImageData(0, 0, c.width, c.height).data;
      let col = 0; for (let i = 0; i < im.length; i += 400) { const a = im[i], b = im[i + 1], e = im[i + 2]; if (Math.abs(a - b) > 18 || Math.abs(b - e) > 18) col++; }
      const v = Toile.vue();
      const h0 = Toile.hit(-9999, -9999);
      const ids = window.__promi.magasin.etat().paroles.filter((p) => !p.draft).map((p) => p.id);
      let plante = false; for (let x = 8; x < 390 && !plante; x += 7) for (let y = 8; y < 760; y += 7) { const h = Toile.hit(x, y); if (h && h.pid != null && ids.indexOf(h.pid) >= 0) { plante = true; break; } }
      const n0 = Toile.cells(); Toile.plantOne(); const n1 = Toile.cells(); Toile.unplantOne();
      const fils = [...document.querySelectorAll('[role=button]')].filter((e) => { const q = e.querySelector('.l'); return /^Fil$/i.test(((q ? q.textContent : e.textContent) || '').trim()); }).length;
      const dur = parseFloat(getComputedStyle(document.getElementById('createBtn'), '::before').animationDuration);
      return { w: r.width, h: r.height, dw: d.width, dh: d.height, col, vue: !!v && 's' in v, gris: h0 === null || h0.pid == null, plante, n0, n1, fils,
        filDansBarre: !!document.querySelector('#accBarre #filBtn'), pastille: !!document.getElementById('filDot'), dur,
        anneau: getComputedStyle(document.getElementById('createBtn'), '::before').backgroundImage };
    })()`)) as Record<string, unknown> & { anneau: string; w: number; h: number; dw: number; dh: number; col: number };
    ok('la Toile remplit l’écran', t.w >= t.dw - 4 && t.h >= t.dh - 90, [t.w, t.h]);
    ok('la Toile porte des dalles colorées', Math.max(t.col, colMax) > 30, [t.col, colMax]);
    ok('Toile.vue() se lit', t['vue'] === true);
    ok('hit() ignore les cellules grises', t['gris'] === true);
    ok('hit() désigne un Promi planté', t['plante'] === true);
    ok('planter garde la densité', t['n0'] === t['n1'], [t['n0'], t['n1']]);
    ok('un seul Fil dans l’app', t['fils'] === 1, t['fils']);
    ok('le Fil a son bouton dans la barre', t['filDansBarre'] === true);
    ok('le Fil a sa pastille', t['pastille'] === true);
    ok('le + tourne lentement (≥ 40 s)', (t['dur'] as number) >= 40, t['dur']);
    // l'anneau : la part des tenues, comptée ICI sur l'état importé (ni gardées de côté, ni demandées), contre l'arc peint
    const st = JSON.parse(ls0['promi_state'] ?? '{"promises":[]}') as EtatProto;
    const ps = st.promises.filter((p) => !p['draft'] && !p['req']);
    const tenues = ps.filter((p) => p['status'] === 'tenu').length;
    const svg = decodeURIComponent(t.anneau);
    const arcs = [
      ...svg.matchAll(
        /d=["']M([\d.]+) ([\d.]+) A([\d.]+) [\d.]+ 0 ([01]) 1 ([\d.]+) ([\d.]+)["'][^>]*stroke=["'](#\w+)/g,
      ),
    ];
    const tenu = arcs.find((m) => m[7]!.toUpperCase() === '#00341A');
    let deg = 0;
    if (tenu) {
      const a0 = Math.atan2(+tenu[2]! - 36, +tenu[1]! - 36);
      const a1 = Math.atan2(+tenu[6]! - 36, +tenu[5]! - 36);
      let L = a1 - a0;
      while (L <= 0) L += 2 * Math.PI;
      const jour = arcs.length > 1 ? 3 / +tenu[3]! : 0;
      deg = ((L + jour) * 180) / Math.PI;
    }
    const attendu = ps.length ? (360 * tenues) / ps.length : 0;
    ok(
      'l’anneau du + porte la part des tenues (± 1,5°)',
      Math.abs(deg - (tenues === ps.length && ps.length ? 360 : attendu)) <= 1.5,
      { deg: Math.round(deg * 10) / 10, attendu: Math.round(attendu * 10) / 10, tenues, paroles: ps.length },
    );
    ok('aucune erreur de page', erreurs.length === 0, erreurs.slice(0, 2));
    await fin();
  }
  // la pastille s'allume sur ce qui attend un geste (Q347) : rien ne m'attend → éteinte ; un Chiche reçu → allumée
  const calme = avecEtat(ls0, (st) => {
    st.FEED = (st.FEED ?? []).filter(
      (f) => !['chiche_recu', 'received', 'invitation', 'moitie'].includes(String(f['type'])),
    );
    st.promises = st.promises.filter((p) => !p['req']);
  });
  const attend = avecEtat(calme, (st) => {
    st.FEED = [
      { id: 99901, type: 'chiche_recu', text: 'Test te lance un chiche : « essai »', from: 'Test', unread: true },
      ...(st.FEED ?? []),
    ];
  });
  for (const [ls, allume] of [
    [calme, false],
    [attend, true],
  ] as const) {
    const { page, fin } = await ouvre(ls);
    const vu = await page.evaluate(() => {
      const e = document.getElementById('filDot')!;
      const r = e.getBoundingClientRect();
      return getComputedStyle(e).display !== 'none' && r.width > 0;
    });
    ok(
      allume ? 'la pastille s’allume sur ce qui attend un geste' : 'la pastille reste éteinte quand rien n’attend',
      vu === allume,
    );
    await fin();
  }
  expect(fautes).toEqual([]);
});

// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// 5 · redteam_volume — AUCUN VOLUME, NULLE PART (v114 ; v137, C-071 : « plus aucun effet autour de la Pelote » ; v139, C-083 : une seule
//     exception nominative, l'ombre de la Pelote, `lot-V139-OMBRE-css` — elle s'étend au lot de l'Aura, qui n'est pas encore porté :
//     la LISTE BLANCHE DE LA VRAIE APP EST VIDE). Un halo, une ombre floue (3e longueur > 0, hors inset), un dégradé. (a) dans les
//     sources de la vraie app (hors pièces reprises : copies octet pour octet du prototype — outils/reprendre.py --verifie —, dont la
//     dette est celle du prototype, volume-dette.json) ; (b) au rendu, sur chaque écran porté, éléments et pseudo-éléments.
// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
const VOLUME_BLANCHE: string[] = [];

test('volume : aucun halo, ombre floue ni dégradé dans les sources de la vraie app', () => {
  const fichiers = [
    ...sources(SRC, /\.(ts|css)$/),
    { f: 'index.html', s: readFileSync(join(SRC, '..', 'index.html'), 'utf8') },
  ];
  if (sonde('volume-source')) fichiers.push({ f: 'sonde.css', s: '.x{box-shadow:0 8px 24px rgba(0,0,0,.3)}' });
  const MOTIFS =
    /(?:repeating-)?(?:radial|linear|conic)-gradient\(|create(?:Radial|Linear|Conic)Gradient|shadowBlur|shadowColor|drop-shadow\(|text-shadow\s*:[^;}"'`]*|box-shadow\s*:[^;}"'`]*/g;
  const floue = (val: string): boolean => {
    for (const part of val
      .split(':')
      .slice(1)
      .join(':')
      .split(/,(?![^(]*\))/)) {
      if (part.includes('inset')) continue;
      const n = [...part.replace(/!important/g, ' ').matchAll(/(-?\d*\.?\d+)(?:px|em|rem)?(?=\s|$|!)/g)].map(
        (m) => +m[1]!,
      );
      if (n.length >= 3 && n[2]! > 0) return true;
    }
    return false;
  };
  const trouves: string[] = [];
  for (const { f, s } of fichiers)
    for (const m of s.matchAll(MOTIFS)) {
      const v = m[0];
      if (/^(text|box)-shadow/.test(v) && !floue(v)) continue;
      const ou = `${f.replace(SRC, 'src')} : ${v.slice(0, 70)}`;
      if (!VOLUME_BLANCHE.some((b) => ou.includes(b))) trouves.push(ou);
    }
  expect(trouves).toEqual([]);
});

test('volume : aucun halo, ombre floue ni dégradé rendu sur un écran porté', async ({ browser }) => {
  const fautes: string[] = [];
  await parcours(browser, false, ({ nom, app }) => {
    for (const x of app.volumes) fautes.push(`${nom} : ${x}`);
  });
  expect(fautes).toEqual([]);
});

// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// 6 · redteam_air — L'AIR ENTRE LES TEXTES (Tom, 29 août 2026 : « deux blocs de texte ne sont jamais à moins de leur écart
//     d'origine » ; v102 : « on mesure toujours l'encre, jamais la boîte »). Chaque bloc de texte et son plus proche voisin du dessous
//     (recouvrement horizontal ≥ 34 %, < 200 pt), mesurés au rectangle du TEXTE ; la référence est le prototype, même écran, même état.
//     Tolérance en dur : 0,6 pt (le bruit de rendu). Une paire du prototype qu'on ne retrouve plus fait échouer (assainissement, 30 sept.).
// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
const TOL_AIR = 0.6;
function paires(b: BlocR[]): Map<string, number> {
  const bl = [...b].sort((x, y) => x.y - y.y);
  const out = new Map<string, number>();
  for (let i = 0; i < bl.length; i++) {
    let best: { g: number; b: BlocR } | null = null;
    for (let j = 0; j < bl.length; j++) {
      if (i === j) continue;
      const a = bl[i]!;
      const c = bl[j]!;
      if (c.y < a.y + a.h - 0.5) continue;
      const rec = Math.min(a.x + a.w, c.x + c.w) - Math.max(a.x, c.x);
      if (rec < Math.min(a.w, c.w) * 0.34) continue;
      const g = c.y - (a.y + a.h);
      if (!best || g < best.g) best = { g, b: c };
    }
    if (best && best.g < 200) out.set(`${bl[i]!.cle} → ${best.b.cle}`, Math.round(best.g * 10) / 10);
  }
  return out;
}

test('air : entre deux blocs de texte, jamais moins d’air à l’encre que dans le prototype', async ({ browser }) => {
  const fautes: string[] = [];
  let n = 0;
  await parcours(browser, true, ({ nom, app, proto }) => {
    const A = paires(app.blocs);
    for (const [k, g] of paires(proto!.blocs)) {
      n++;
      const a = A.get(k);
      if (a === undefined) fautes.push(`${nom} : ${k} — la paire n’est plus mesurée (prototype ${String(g)} pt)`);
      else if (a < g - TOL_AIR) fautes.push(`${nom} : ${k} — ${String(g)} → ${String(a)} pt`);
    }
  });
  expect(n, 'des paires de textes mesurées dans le prototype').toBeGreaterThan(2);
  expect(fautes).toEqual([]);
});

// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// 7 · redteam_flash — RIEN NE PARAÎT UNE FRACTION DE SECONDE (Tom, 30 sept. 2026 ; C-271 : « rien n'apparaît ni ne disparaît d'une image
//     à l'autre »). Relevé IMAGE PAR IMAGE dans la page : à chaque image, sur une grille 6 × 11 de l'appareil, la couche du dessus qui
//     PEINT (opacité effective ≥ 0,12). Une couche (≥ 2 points de grille) qui paraît puis disparaît en moins de 800 ms — ou sur une
//     seule image — sans être là au début ni à la fin, est un flash ; l'ancien chrome (.topbar, .footer, .statusbar) ne paraît jamais.
//     Fenêtres : l'ouverture de l'app, puis l'ouverture de chaque écran porté (au moins 2,5 s et 14 images chacune). Seuils en dur.
//     (B « la page + paraît composée » et C « une plantation coupe » : ils s'étendent au lot de la page +.)
// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
const COURT_MS = 800;
const POINTS = 2;
const INTERDITS = ['.topbar', '.footer', '.statusbar'];
type Image_ = { t: number; m: Record<string, number>; bouge?: string[] };

function enregistreurFlash(): void {
  const w = window as unknown as {
    __fl?: { on: boolean; frames: Image_[]; t0: number; go(): void; stop(): Image_[]; sonde: number };
  };
  if (w.__fl) return;
  const F = { on: false, frames: [] as Image_[], t0: 0, sonde: -1, go() {}, stop: () => [] as Image_[] };
  w.__fl = F;
  const effOp = (e: Element | null): number => {
    let o = 1;
    while (e && e.nodeType === 1) {
      const s = getComputedStyle(e);
      if (s.visibility === 'hidden' || s.display === 'none') return 0;
      o *= parseFloat(s.opacity);
      if (o < 0.02) return 0;
      e = e.parentElement;
    }
    return o;
  };
  const peint = (e: Element): boolean => {
    if (/^(CANVAS|IMG|SVG|svg|VIDEO|path|circle|rect|polygon)$/.test(e.tagName)) return true;
    const s = getComputedStyle(e);
    const bg = s.backgroundColor;
    if (bg && bg !== 'transparent' && !/rgba\([^)]*,\s*0\)$/.test(bg)) return true;
    if (s.backgroundImage && s.backgroundImage !== 'none') return true;
    for (let n = e.firstChild; n; n = n.nextSibling) if (n.nodeType === 3 && (n.textContent ?? '').trim()) return true;
    return false;
  };
  const nom = (x: Element | undefined): string => {
    if (!x) return '';
    if (x.id) return '#' + x.id;
    const c =
      typeof x.className === 'string' ? x.className : ((x.className as unknown as { baseVal?: string }).baseVal ?? '');
    return '.' + (String(c).split(' ')[0] || x.tagName);
  };
  const cle = (e: Element): string => {
    const dv = document.getElementById('device');
    const fr = dv?.parentElement;
    const ch: Element[] = [];
    let q: Element | null = e;
    while (q && q !== document.body && q !== document.documentElement) {
      const p: Element | null = q.parentElement;
      ch.unshift(q);
      if (p === dv || p === fr || p === document.body) break;
      q = p;
    }
    return nom(ch[0]) + (ch[1] ? '>' + nom(ch[1]) : '');
  };
  let sondeEl: HTMLElement | null = null;
  const pas = (): void => {
    if (F.on) {
      const dv = document.getElementById('device');
      const m: Record<string, number> = {};
      // les couches qui GLISSENT à cette image (une transition ou une animation en cours sur la couche elle-même : la page + qui monte,
      // C-331) — ses parties traversent les points du relevé, elles ne paraissent pas
      const bouge: string[] = [];
      // (et les couches qu'elle recouvre en glissant — celles qui la précèdent dans l'appareil, donc dessous : l'accueil sous la page +)
      if (dv) {
        const L = [...dv.children];
        L.forEach((c, k) => {
          if (c.getAnimations().some((a) => a.playState === 'running'))
            for (const d of L.slice(0, k + 1)) if (!bouge.includes(nom(d))) bouge.push(nom(d));
        });
      }
      if (dv) {
        const r = dv.getBoundingClientRect();
        for (let i = 0; i < 6; i++)
          for (let j = 0; j < 11; j++) {
            const L = document.elementsFromPoint(
              r.left + (r.width * (i + 0.5)) / 6,
              r.top + (r.height * (j + 0.5)) / 11,
            );
            for (const e of L) {
              if (e === dv || e === document.body || e === document.documentElement) break;
              if (effOp(e) < 0.12 || !peint(e)) continue;
              const c = cle(e);
              m[c] = (m[c] ?? 0) + 1;
              break;
            }
          }
      }
      F.frames.push({ t: Math.round(performance.now() - F.t0), m, bouge });
      // LA SONDE : une couche posée pour UNE image relevée, au milieu de la fenêtre (le défaut que le juge doit prendre)
      if (sondeEl) {
        sondeEl.remove();
        sondeEl = null;
      }
      if (F.sonde >= 0 && F.frames.length === F.sonde && dv) {
        sondeEl = document.createElement('div');
        sondeEl.id = 'sondeFlash';
        sondeEl.style.cssText =
          'position:absolute;left:60px;top:300px;width:240px;height:200px;background:#C9A8F5;z-index:999';
        dv.appendChild(sondeEl);
      }
    }
    requestAnimationFrame(pas);
  };
  F.go = () => {
    F.frames = [];
    F.t0 = performance.now();
    F.on = true;
  };
  F.stop = () => {
    F.on = false;
    return F.frames;
  };
  requestAnimationFrame(pas);
}

function flashs(fr: Image_[]): string[] {
  const out: string[] = [];
  const cles = new Set(fr.flatMap((f) => Object.keys(f.m)));
  for (const k of cles) {
    let run: [number, number] | null = null;
    for (let i = 0; i < fr.length; i++) {
      const v = (fr[i]!.m[k] ?? 0) >= POINTS;
      if (v && run === null) run = [i, i];
      else if (v && run) run[1] = i;
      if ((!v || i === fr.length - 1) && run) {
        const [a, b] = run;
        run = null;
        const dur = (b + 1 < fr.length ? fr[b + 1]!.t : fr.at(-1)!.t) - fr[a]!.t;
        // une couche qui GLISSE (une transition décidée, C-331 : la page + qui monte) : ce qui traverse les points du relevé pendant
        // qu'elle glisse ne paraît pas — seulement si elle glisse à chacune de ces images
        const couche = k.split('>')[0]!;
        if (fr.slice(a, b + 1).every((f) => (f.bouge ?? []).includes(couche))) continue;
        // une PARTIE d'écran (« couche>partie ») qui paraît pendant que son écran est là et s'en va avec lui n'apparaît pas
        if (k.includes('>')) {
          const L = k.split('>')[0]!;
          const tot = (f: Image_): number =>
            Object.entries(f.m)
              .filter(([kk]) => kk.split('>')[0] === L)
              .reduce((s, [, v2]) => s + v2, 0);
          if (
            a > 0 &&
            tot(fr[a - 1]!) >= POINTS &&
            (b + 1 >= fr.length || fr.slice(b + 1, b + 3).every((f) => tot(f) < POINTS))
          )
            continue;
        }
        if ((dur < COURT_MS || a === b) && a > 2 && b < fr.length - 3)
          out.push(`${k} à ${String(fr[a]!.t)} ms, ${String(dur)} ms (${String(b - a + 1)} image(s))`);
      }
    }
  }
  for (const k of cles)
    if (INTERDITS.includes(k.split('>')[0]!) && fr.some((f) => f.m[k]))
      out.push(`${k} (ancien chrome) à ${String(fr.find((f) => f.m[k])!.t)} ms`);
  return out.sort();
}

async function attendreImages(page: Page, n: number, ms: number, cle: string): Promise<void> {
  await page.waitForFunction(
    ([n, ms, cle]) => {
      const w = window as unknown as Record<string, { frames: Array<{ t: number }> } | undefined>;
      const F = w[cle as string];
      return !!F && F.frames.length >= (n as number) && (F.frames.at(-1)?.t ?? 0) >= (ms as number);
    },
    [n, ms, cle] as const,
    { timeout: 120000, polling: 100 },
  );
}

test('flash : rien ne paraît une fraction de seconde, à l’ouverture et à chaque écran porté', async ({ browser }) => {
  const fautes: string[] = [];
  for (const theme of THEMES)
    for (const [i, e] of ECRANS_PORTES.entries()) {
      const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
      await ctx.addInitScript(enregistreurFlash);
      await ctx.addInitScript(
        'requestAnimationFrame(function g(){ if(window.__fl) window.__fl.go(); else requestAnimationFrame(g); })',
      );
      const page = await ctx.newPage();
      await vraieApp(page, lsDe(theme));
      await attendreImages(page, 14, 4000, '__fl');
      // l'ouverture de l'app (une fois par thème)
      if (i === 0) {
        const fr = (await page.evaluate('window.__fl.stop()')) as Image_[];
        for (const f of flashs(fr)) fautes.push(`${theme}, ouverture : ${f}`);
      }
      await page.evaluate(`window.__fl.go(); window.__fl.sonde = ${sonde('flash-couche') ? 6 : -1};`);
      await e.ouvrir(page);
      await attendreImages(page, 14, 2500, '__fl');
      const fr = (await page.evaluate('window.__fl.stop()')) as Image_[];
      for (const f of flashs(fr)) fautes.push(`${theme}, ${e.nom} : ${f}`);
      await ctx.close();
    }
  expect(fautes).toEqual([]);
});

// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// 8 · redteam_superpo — JAMAIS DE SUPERPOSITION (Tom, 3 sept. 2026 : « jamais de mauvaises mises en page, de superposition »). Deux
//     textes visibles ne se recouvrent jamais (plus de 3 pt dans les deux sens), sur aucun écran, dans aucun thème — confirmé au doigt :
//     la pile `elementsFromPoint` au centre du recouvrement, coupée au premier fond opaque, porte les deux.
// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
test('superposition : deux textes visibles ne se recouvrent jamais, sur chaque écran porté', async ({ browser }) => {
  const fautes: string[] = [];
  await parcours(browser, false, ({ nom, app }) => {
    for (const x of app.superpo) fautes.push(`${nom} : ${x}`);
  });
  expect(fautes).toEqual([]);
});

// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// 9 · redteam_aspect — L'ASPECT AU REPOS NE CHANGE PAS SANS DEMANDE (v203 clôture, C-285, porte A1). Contre le prototype, même écran :
//     A · chaque morceau de texte (le plus petit élément qui porte du texte) : son texte, sa police, sa taille (± 0,1), sa graisse, son
//         style, sa chasse, son interligne, sa casse, ses couleurs (color, -webkit-text-fill-color) et sa place (± 0,5 pt) ; un morceau
//         d'un seul côté fait échouer ;
//     B · l'image des textes seuls (tout le reste rendu transparent, sur un fond plat), boîte par boîte (+ 4 pt) : au plus 0,5 % de
//         pixels qui diffèrent de plus de 24 niveaux.
//     (D, le détracé pas à pas : il s'étend aux lots qui tracent — l'onboarding, le guide, la page +, la fiche ; l'accueil ne trace rien.)
// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
const ASPECT = [
  'fontFamily',
  'fontWeight',
  'fontStyle',
  'letterSpacing',
  'lineHeight',
  'textTransform',
  'color',
  'webkitTextFillColor',
];

test('aspect A : chaque morceau de texte a le texte, la police, la taille, la couleur et la place du prototype', async ({
  browser,
}) => {
  const fautes: string[] = [];
  let n = 0;
  await parcours(browser, true, ({ nom, app, proto }) => {
    const textes = (r: Rel): Map<string, NoeudR> => new Map(r.noeuds.filter((q) => q.texte).map((q) => [q.cle, q]));
    const A = textes(app);
    const P = textes(proto!);
    // un morceau sans id se nomme par son rang parmi ses frères : ce rang dépend de l'ORDRE DE CONSTRUCTION du DOM, pas de l'écran — un
    // morceau que sa clé ne retrouve pas est apparié au morceau de l'autre côté qui porte le même texte et la même balise, s'il est seul
    const seul = (M: Map<string, NoeudR>, autre: Map<string, NoeudR>, q: NoeudR): string | null => {
      const L = [...M].filter(([k, x]) => !autre.has(k) && x.texte === q.texte && x.tag === q.tag);
      return L.length === 1 ? L[0]![0] : null;
    };
    for (const [k, p] of [...P]) {
      if (A.has(k)) continue;
      const ka = seul(A, P, p);
      if (ka) {
        A.set(k, A.get(ka)!);
        A.delete(ka);
      }
    }
    for (const [k, p] of P) {
      const a = A.get(k);
      if (!a) {
        fautes.push(`${nom} : « ${p.texte} » (${k}) n’est plus là`);
        continue;
      }
      n++;
      if (a.texte !== p.texte) fautes.push(`${nom} : ${k} texte « ${p.texte} » → « ${a.texte} »`);
      for (const q of ASPECT)
        if (a.st[q] !== p.st[q] && !ecartAdmis(nom, p.texte, q))
          fautes.push(`${nom} : « ${p.texte} » ${q} ${String(p.st[q])} → ${String(a.st[q])}`);
      if (Math.abs(parseFloat(a.st['fontSize']!) - parseFloat(p.st['fontSize']!)) > 0.1)
        fautes.push(`${nom} : « ${p.texte} » taille ${String(p.st['fontSize'])} → ${String(a.st['fontSize'])}`);
      for (const [j, c] of ['x', 'y', 'largeur', 'hauteur'].entries())
        if (Math.abs(a.r[j]! - p.r[j]!) > 0.5)
          fautes.push(`${nom} : « ${p.texte} » ${c} ${String(p.r[j])} → ${String(a.r[j])} pt`);
    }
    for (const [k, a] of A) if (!P.has(k)) fautes.push(`${nom} : « ${a.texte} » (${k}) n’est pas dans le prototype`);
  });
  expect(n, 'des morceaux de texte comparés').toBeGreaterThan(5);
  expect(fautes).toEqual([]);
});

function partEcartee(a: PNG, b: PNG, bt: Boite): number {
  const k = a.width / 390;
  let n = 0;
  let d = 0;
  for (
    let y = Math.max(0, Math.floor((bt[1] - 4) * k));
    y < Math.min(a.height, Math.ceil((bt[1] + bt[3] + 4) * k));
    y++
  )
    for (
      let x = Math.max(0, Math.floor((bt[0] - 4) * k));
      x < Math.min(a.width, Math.ceil((bt[0] + bt[2] + 4) * k));
      x++
    ) {
      const i = (y * a.width + x) * 4;
      n++;
      const e = Math.max(
        Math.abs(a.data[i]! - b.data[i]!),
        Math.abs(a.data[i + 1]! - b.data[i + 1]!),
        Math.abs(a.data[i + 2]! - b.data[i + 2]!),
      );
      if (e > 24) d++;
    }
  return n ? d / n : 0;
}

test('aspect B : les textes seuls, au pixel, comme dans le prototype (≤ 0,5 % au-delà de 24 niveaux)', async ({
  browser,
}) => {
  const fautes: string[] = [];
  let n = 0;
  await parcours(browser, true, ({ nom, app, proto }) => {
    const A = PNG.sync.read(app.pngTextes);
    const P = PNG.sync.read(proto!.pngTextes);
    if (A.width !== P.width || A.height !== P.height) {
      fautes.push(`${nom} : images de tailles différentes`);
      return;
    }
    for (const p of proto!.noeuds.filter((q) => q.texte)) {
      n++;
      const part = partEcartee(A, P, p.r);
      if (part > 0.005 && !ecartAdmis(nom, p.texte, 'color'))
        fautes.push(`${nom} : « ${p.texte} » ${(100 * part).toFixed(2)} % des pixels écartés`);
    }
  });
  expect(n, 'des morceaux de texte comparés').toBeGreaterThan(5);
  expect(fautes).toEqual([]);
});

// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// 10 · redteam_filets — AUCUN TRAIT HORIZONTAL NULLE PART, SAUF S'IL EST AU MOODBOARD (le moodboard n'a quasiment aucun filet : ses
//      séparations sont des respirations ; les seuls sanctionnés : la barre Peaufiner et le filet sous la carte message — leurs noms, en
//      dur). (a) le DOM : border-top / border-bottom / ombre inset horizontale, sur un élément large (≥ la moitié de l'écran) qui n'est ni
//      une pastille ni une boîte ; (b) le CANEVAS : aucun filet crème (#F7F0DE, adouci rgba(247,240,222,.55)) peint dans un canevas d'un
//      écran porté — v135 (C-059) : « retire le filet autour des disques et des Noyaux, et celui sous le trait » : la liste blanche est
//      VIDE. (La Toile, le moteur repris, est jugée par banc-rendu.spec.)
// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
test('filets : aucun trait horizontal hors de ceux du moodboard, sur chaque écran porté', async ({ browser }) => {
  const fautes: string[] = [];
  await parcours(browser, false, ({ nom, app }) => {
    for (const x of app.filets) fautes.push(`${nom} : ${x}`);
  });
  expect(fautes).toEqual([]);
});

test('filets : aucun filet crème peint dans un canevas d’un écran porté', async ({ browser }) => {
  const fautes: string[] = [];
  await parcours(browser, false, ({ nom, app }) => {
    for (const x of app.filetsCanevas) fautes.push(`${nom} : ${x}`);
  });
  expect(fautes).toEqual([]);
});

// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// 11 · redteam_tonsurton — UN TRAIT NE SE CONFOND JAMAIS AVEC SON CHAMP (§3 ; Q216, Tom, 18 sept. 2026 : « juge en ΔE, pas en Δlum » ;
//      plancher ΔE 15, CIELAB). On lit les PIXELS PEINTS. Au lot 1, le seul trait d'état porté est l'ANNEAU DU + posé sur la barre : chaque
//      arc (sa place prise dans l'image du pseudo-élément — un pointeur —, son verdict lu sur l'écran, au milieu de l'arc) contre le fond
//      de la barre lu à côté. (Les traits de la fiche, de la page +, des cartes de l'Index et des bandeaux du Fil s'étendent aux lots 2 à 4.)
// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
const SEUIL_DE = 15;

test('ton sur ton : chaque arc de l’anneau du + se détache de la barre (ΔE ≥ 15), lu sur les pixels', async ({
  browser,
}) => {
  const fautes: string[] = [];
  let arcsLus = 0;
  await parcours(browser, false, ({ nom, app }) => {
    const plus = app.noeuds.find((q) => q.cle === '#createBtn');
    const barre = app.noeuds.find((q) => q.cle === '#accBarre');
    if (!plus || !barre) return;
    const img = PNG.sync.read(app.png);
    const cx = plus.r[0] + plus.r[2] / 2;
    const cy = plus.r[1] + plus.r[3] / 2;
    const champ = pixel(img, cx, barre.r[1] + 6);
    const svg = decodeURIComponent(plus.ps['::before backgroundImage'] ?? '');
    for (const m of svg.matchAll(/d=["']M([\d.]+) ([\d.]+) A([\d.]+) [\d.]+ 0 ([01]) 1 ([\d.]+) ([\d.]+)["']/g)) {
      const R = +m[3]!;
      const a0 = Math.atan2(+m[2]! - 36, +m[1]! - 36);
      let L = Math.atan2(+m[6]! - 36, +m[5]! - 36) - a0;
      while (L <= 0) L += 2 * Math.PI;
      const am = a0 + L / 2;
      const ech = plus.r[2] / 72;
      const c = pixel(img, cx + R * ech * Math.cos(am), cy + R * ech * Math.sin(am));
      arcsLus++;
      const de = deltaE(c, champ);
      if (de < SEUIL_DE)
        fautes.push(`${nom} : un arc rgb(${c.join(',')}) sur la barre rgb(${champ.join(',')}) — ΔE ${de.toFixed(1)}`);
    }
  });
  expect(arcsLus, 'des arcs lus (l’état porte des paroles)').toBeGreaterThan(0);
  expect(fautes).toEqual([]);
});

// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// 12 · redteam_lexique — LES TERMES BANNIS ET LA LOI DES POINTS, jugés à l'écran (v135, C-065).
//      A · aucun texte AFFICHÉ (texte rendu, libellé VoiceOver, texte d'invite) ne porte un terme banni (CLAUDE.md §2, liste complétée par
//          Tom le 18 août et le 23 sept. 2026 — en dur) ; « échéance » n'est banni que comme libellé de champ.
//      B · la loi des points (Tom, 4 oct. 2026, v128) : « Les points disent qu'il manque quelque chose […]. Ils ne servent jamais à autre
//          chose. » Aucun petit nœud rond et plein (≤ 14 pt), aucun texte fait de points. Exception nominative : `.dz-tailles` (le choix de
//          taille du dessin). Dette NOMMÉE (lexique-dette.json, née le 6 oct. 2026) : la pastille du Fil, `#filDot` (D6 v173 : elle dit
//          qu'un geste m'attend). Rien d'autre.
// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
const DETTE_POINTS = ['point #filDot'];

test('lexique : aucun terme banni affiché, sur chaque écran porté', async ({ browser }) => {
  const fautes: string[] = [];
  await parcours(browser, false, ({ nom, app }) => {
    for (const x of app.termes) fautes.push(`${nom} : ${x}`);
  });
  expect(fautes).toEqual([]);
});

test('lexique : la loi des points — aucun point qui ne dit pas qu’il manque quelque chose', async ({ browser }) => {
  const fautes: string[] = [];
  await parcours(browser, false, ({ nom, app }) => {
    for (const x of app.points) if (!DETTE_POINTS.includes(x)) fautes.push(`${nom} : ${x}`);
  });
  expect(fautes).toEqual([]);
});

// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// 13 · redteam_emoji — PAS D'EMOJI DANS PROMI (v146, Tom, 14 oct. 2026, C-129 : « un emoji tapé ou collé n'est tout simplement pas
//      inséré : rien ne s'affiche, aucun message »). Chaque champ de saisie visible d'un écran porté : au clavier (chaque emoji inséré
//      d'un bloc, comme le clavier d'iOS), au collage (un vrai évènement `paste`) ; le texte autour reste. En dur : pictogrammes, teinte de
//      peau, jonction (famille), drapeau, touche numérotée, cœur, étincelles. ⚠ Le lot 1 ne porte AUCUN champ : le juge s'étend au
//      premier lot qui en porte (l'onboarding, la page +, la fiche — lots 2 et 3) ; la sonde pose un champ qui laisse entrer les emojis.
//      (« À l'enregistrement : aucun emoji dans la sauvegarde » s'étend au lot qui écrit une parole : la page +.)
// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
const EMO = ['🏃', '👍🏽', '👨‍👩‍👧', '🇫🇷', '1️⃣', '❤️', '✨'];

test('emoji : aucun champ de saisie d’un écran porté n’accepte un emoji (tapé ou collé)', async ({ browser }) => {
  const fautes: string[] = [];
  let champs = 0;
  for (const e of ECRANS_PORTES) {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
    const page = await ctx.newPage();
    await vraieApp(page, stockage());
    await e.ouvrir(page);
    if (sonde('emoji-champ'))
      await page.evaluate(() => {
        const i = document.createElement('input');
        i.type = 'text';
        i.style.cssText = 'position:absolute;left:40px;top:300px;width:300px;height:40px;z-index:999';
        document.getElementById('device')!.appendChild(i);
      });
    const sels = await page.evaluate(() => {
      const out: string[] = [];
      document
        .querySelectorAll(
          '#device input:not([type=hidden]), #device textarea, #device [contenteditable=""], #device [contenteditable=true]',
        )
        .forEach((x, i) => {
          const r = x.getBoundingClientRect();
          const c = getComputedStyle(x);
          if (r.width < 2 || r.height < 2 || c.visibility === 'hidden' || c.display === 'none') return;
          x.setAttribute('data-emoji-champ', String(i));
          out.push(`[data-emoji-champ="${String(i)}"]`);
        });
      return out;
    });
    for (const sel of sels) {
      champs++;
      const vider = (): Promise<void> =>
        page.evaluate((s) => {
          const x = document.querySelector<HTMLElement>(s)!;
          x.focus();
          if (x.isContentEditable) x.textContent = '';
          else (x as HTMLInputElement).value = '';
        }, sel);
      const valeur = (): Promise<string> =>
        page.evaluate((s) => {
          const x = document.querySelector<HTMLElement>(s)!;
          return x.isContentEditable ? (x.textContent ?? '') : (x as HTMLInputElement).value;
        }, sel);
      await vider();
      for (const [m, emoji] of [
        ['marcher ', false],
        [EMO[0]!, true],
        [' une ', false],
        [EMO[1]!, true],
        [' heure ', false],
        [EMO[4]!, true],
      ] as const)
        await (emoji ? page.keyboard.insertText(m) : page.keyboard.type(m, { delay: 15 }));
      const v1 = await valeur();
      if (
        EMO.join('')
          .split('')
          .some((c) => c.trim() && v1.includes(c)) ||
        !/marcher.*une.*heure/.test(v1)
      )
        fautes.push(`${e.nom} ${sel} au clavier : ${JSON.stringify(v1)}`);
      await vider();
      const v2 = (await page.evaluate(
        ([s, t]) => {
          const x = document.querySelector<HTMLElement>(s as string)!;
          x.focus();
          const dt = new DataTransfer();
          dt.setData('text/plain', t as string);
          const ev = new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true });
          if (x.dispatchEvent(ev) && !x.isContentEditable) {
            const q = x as HTMLInputElement;
            q.setRangeText(t as string, q.selectionStart ?? 0, q.selectionEnd ?? 0, 'end');
            q.dispatchEvent(new Event('input', { bubbles: true }));
          }
          return x.isContentEditable ? (x.textContent ?? '') : (x as HTMLInputElement).value;
        },
        [sel, `lire ${EMO[2]!} Proust ${EMO[3]!} ce ${EMO[5]!} soir ${EMO[6]!}`] as const,
      )) as string;
      if ([...v2].some((c) => (c.codePointAt(0) ?? 0) >= 0x2000 && !'’…'.includes(c)) || !/Proust.*soir/.test(v2))
        fautes.push(`${e.nom} ${sel} au collage : ${JSON.stringify(v2)}`);
    }
    await ctx.close();
  }
  if (!champs)
    test
      .info()
      .annotations.push({ type: 'non jugé', description: 'aucun champ de saisie sur les écrans portés (lot 1)' });
  expect(fautes).toEqual([]);
});

// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
// 14 · redteam_secs — AUCUN CHANGEMENT SEC (C-271, Tom, 13 nov. 2026 : « un texte qui change se détrace puis le nouveau se trace » ;
//      « rien n'apparaît ni ne disparaît d'une image à l'autre »). Relevé à chaque image (après la peinture), pendant l'ouverture de chaque
//      écran porté et le temps qu'il se pose (au moins 2,5 s et 14 images) :
//      T · un texte visible qui change à sa place sans transition déclarée (ni tracé, ni découpe, ni animation finie en cours) ;
//      B · une rangée ou une carte (sa clé : data-v, data-pid, data-nk) qui saute de plus de 12 pt d'une image à l'autre sans animation.
//      La frappe n'est pas jugée (ce qu'on tape s'écrit lettre par lettre). Seuil en dur : 12 pt.
// ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
function enregistreurSecs(): void {
  const w = window as unknown as {
    __au?: { frames: Array<{ t: number }>; fautes: string[]; t0: number; on: boolean; sonde: number };
  };
  if (w.__au) return;
  const A = { frames: [] as Array<{ t: number }>, fautes: [] as string[], t0: performance.now(), on: false, sonde: -1 };
  w.__au = A;
  let prev = new Map<string, { v: string; tr: boolean }>();
  let prevB = new Map<string, { x: number; y: number; a: boolean }>();
  const trans = (e: Element): boolean => {
    for (let x: Element | null = e; x && x.nodeType === 1; x = x.parentElement) {
      const h = x as HTMLElement & { __trace?: unknown; __v200?: unknown };
      if (h.__trace || h.__v200) return true;
      const c = h.style && (h.style.clipPath || h.style.getPropertyValue('-webkit-clip-path'));
      if (c && c !== 'none') return true;
      if (
        x.getAnimations().some((a) => {
          try {
            const t = a.effect?.getComputedTiming();
            return a.playState === 'running' && !!t && isFinite(Number(t.activeDuration));
          } catch {
            return false;
          }
        })
      )
        return true;
    }
    return false;
  };
  const saisie = (e: Element): boolean => !!e.closest('input, textarea, [contenteditable]');
  const nom = (e: Element): string => {
    let s = '';
    for (let x: Element | null = e, i = 0; x && i < 4; x = x.parentElement, i++) {
      s = (x.id ? '#' + x.id : x.tagName.toLowerCase()) + (s ? '>' + s : '');
      if (x.id) break;
    }
    return s;
  };
  const tour = (): void => {
    const dv = document.getElementById('device');
    if (dv && A.on) {
      const R = dv.getBoundingClientRect();
      const s = R.width / 390;
      const cur = new Map<string, { v: string; tr: boolean; e: Element }>();
      const wk = document.createTreeWalker(dv, NodeFilter.SHOW_TEXT);
      let t: Node | null;
      while ((t = wk.nextNode())) {
        const v = (t.nodeValue ?? '').trim();
        if (!v) continue;
        const e = t.parentElement;
        if (!e) continue;
        const r = e.getBoundingClientRect();
        if (!r.width || r.bottom < R.top || r.top > R.bottom) continue;
        const cs = getComputedStyle(e);
        if (cs.visibility === 'hidden' || +cs.opacity < 0.05) continue;
        const cb = e.closest('[data-v],[data-pid],[data-nk]');
        const nm =
          (cb
            ? '[' + (cb.getAttribute('data-v') ?? cb.getAttribute('data-pid') ?? cb.getAttribute('data-nk')) + '] '
            : '') + nom(e);
        let j = 0;
        while (cur.has(nm + '@' + String(j)) && cur.get(nm + '@' + String(j))!.e !== e) j++;
        const key = nm + '@' + String(j);
        const o = cur.get(key);
        cur.set(key, { v: (o ? o.v : '') + v, tr: trans(e) || saisie(e), e });
      }
      cur.forEach((c, key) => {
        const o = prev.get(key);
        if (o && o.v !== c.v && !c.tr && !o.tr)
          A.fautes.push('T ' + key + ' « ' + o.v.slice(0, 40) + ' » → « ' + c.v.slice(0, 40) + ' »');
      });
      prev = new Map([...cur].map(([k, v]) => [k, { v: v.v, tr: v.tr }]));
      const curB = new Map<string, { x: number; y: number; a: boolean }>();
      dv.querySelectorAll('[data-v],[data-pid],[data-nk]').forEach((b) => {
        const r = b.getBoundingClientRect();
        if (!r.width) return;
        const k2 =
          (b.getAttribute('data-v') ?? b.getAttribute('data-pid') ?? b.getAttribute('data-nk')) +
          '|' +
          nom(b.parentElement ?? b);
        curB.set(k2, { x: r.left / s, y: r.top / s, a: trans(b) });
      });
      curB.forEach((c, k2) => {
        const o = prevB.get(k2);
        if (o && !c.a && !o.a && Math.hypot(c.x - o.x, c.y - o.y) > 12)
          A.fautes.push('B ' + k2 + ' ' + o.y.toFixed(0) + ' → ' + c.y.toFixed(0) + ' pt');
      });
      prevB = curB;
      A.frames.push({ t: Math.round(performance.now() - A.t0) });
      // LA SONDE : un texte qui change d'un coup, au milieu de la fenêtre (le nom « Studio » de la barre)
      if (A.sonde >= 0 && A.frames.length === A.sonde) {
        const l = dv.querySelector('#studioBtn .l');
        if (l) l.textContent = 'Studios';
      }
    }
    requestAnimationFrame(apres);
  };
  const MC = new MessageChannel();
  MC.port1.onmessage = tour;
  const apres = (): void => {
    MC.port2.postMessage(0);
  };
  requestAnimationFrame(apres);
}

test('changements secs : aucun texte ne change à sa place sans transition, aucune rangée ne saute', async ({
  browser,
}) => {
  const fautes: string[] = [];
  for (const e of ECRANS_PORTES) {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
    await ctx.addInitScript(enregistreurSecs);
    const page = await ctx.newPage();
    await vraieApp(page, stockage());
    await page.evaluate(
      `(() => { const A = window.__au; A.frames = []; A.fautes = []; A.t0 = performance.now(); A.on = true; A.sonde = ${sonde('secs-texte') ? 5 : -1}; })()`,
    );
    await e.ouvrir(page);
    await attendreImages(page, 14, 2500, '__au');
    const f = (await page.evaluate('window.__au.fautes')) as string[];
    for (const x of f) fautes.push(`${e.nom} : ${x}`);
    await ctx.close();
  }
  expect(fautes).toEqual([]);
});
