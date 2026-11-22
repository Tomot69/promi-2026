/**
 * LA PAGE + (lot 2a) — Promi, Chiche, Cercle : le plateau (le mot de la nature, le X), le champ de la nature et la dalle d'avance du moteur
 * (C-241), l'horizon BAS et rien du trait tant que la parole n'est pas validée (C-213, C-229), la phrase-pastilles (le verbe et son cycle
 * pour un Promi), les exemples des pastilles vides (`lot-EXEMPLES-V20`, C-312), la saisie du titre et du nom, le choix des personnes
 * (`lot-GENS`, C-269, C-122), le rail du pinceau (C-196), « garder de côté » (C-149), la barre Peaufiner au repos.
 * Le prototype rendu (v214b) est la référence ; ses règles de composition sont relues dans app.html (`lot-S3-page-plus` : `ecran`, `cotes`,
 * `trait`, `hautBouton` ; `lot-V172-INVITE` : `hzCible`) et réécrites ici.
 *
 * Ce que 2a ne fait pas (2b, 2c) : le trait et sa genèse, la plantation, la naissance et le vol de la dalle, la mise en page de saisie
 * (« DÉJÀ PROMIS », la page qui monte avec le clavier), le panneau de Peaufiner, les textes longs, la première lettre, le détracé des
 * changements de mots (la phrase se recompose : C-271 au 2c).
 *
 * L'état de la page (la phrase qu'on écrit) n'appartient qu'à elle ; ce qui se garde passe par le magasin (le tirage des exemples, le gardé
 * de côté). Son temps est celui de l'horloge unique ; le moteur, par la façade.
 */
import './page-plus.css';
import type { Facade } from '../../moteur/facade.ts';
import type { Magasin } from '../../etat/magasin.ts';
import type { Navigation } from '../../navigation/navigation.ts';
import type { Brouillon } from '../../donnees/schema.ts';
import { horloge } from '../../animation/horloge.ts';
import { palette } from '../../design/jetons.ts';
import {
  EXEMPLES,
  EXEMPLES_FIXES,
  PRENOMS_EXEMPLE,
  TEXTES_PAGE_PLUS as T,
  type TypeExemple,
} from '../../textes/page-plus.ts';
import { variante } from '../../metier/exemples.ts';
import { elision } from '../../metier/elision.ts';
import { PINCEAUX } from './pinceaux.ts';
import { basOnde, cheminOnde, onde } from './onde.ts';

export type Nature = 'promi' | 'chiche' | 'nuee';
export type Sens = 'soi' | 'faire' | 'demander';

/** ce que la page écrit (le `_phrase` du prototype, et ses voisins) */
export interface PhrasePage {
  nat: Nature;
  sens: Sens;
  titre: string;
  /** à qui (Promi), qui ose (Chiche) */
  qui: string[];
  /** avec qui (Chiche) */
  avec: string[];
  /** le nom d'un Cercle, ses membres */
  nom: string;
  membres: string[];
  pinceau: string;
  /** C-304 : la place du destinataire touchée sans personne passe à « moi » (entre pointillés) */
  moi: boolean;
}

export interface PagePlus {
  racine: HTMLElement;
  ouvrir(nat: Nature): void;
  fermer(): void;
  ouverte(): boolean;
  /** pour les tests : la phrase, la mise en page (en pt du cadre 390), le choix ouvert */
  etat(): {
    phrase: PhrasePage;
    base: number;
    amp: number;
    hz: number;
    lignes: number;
    taille: number;
    choix: string | null;
    gardeActif: boolean;
    exemples: Partial<Record<TypeExemple, string>>;
  };
  detruire(): void;
}

const CHAMP: Record<Nature, string> = { promi: palette.bleu45, chiche: palette.framboise54, nuee: palette.mauve77 };
const NATURES: readonly Nature[] = ['promi', 'chiche', 'nuee'];
/** C-184, v164b : le trait × 1,3, ses points × 1,15 — le pas du mot et de la phrase (`--pp-dyt`) en découle : ⌈14 × (K − 1,05)⌉ / 2 */
const TRAIT_K = 1.3;
const TRAIT_PTS = 1.15;
const DT = Math.ceil(14 * Math.max(0, TRAIT_K - 1.05)) / 2;
/** v150, v162 (C-158, C-183) : la phrase d'un Chiche remonte de 10 pt, celle d'un Cercle de 31 */
const DY_PHRASE: Record<Nature, number> = { promi: 0, chiche: -10, nuee: -31 };
/** C-229 : pas prête, l'horizon est 40 pt plus bas que sa place, jamais à moins de 12 pt de l'encre de la phrase */
const HZ_BAS = 40;
const HZ_AIR = 12;
/** §2.8 (v20, v115) : l'exemple passe à la ligne plutôt que de réduire la phrase sous 28 */
const PLANCHER_PH = 28;
/** la grammaire du lien « garder de côté » : son encre est 0,5 pt sous sa boîte (`INK_LIEN`) ; le rail se pose à mi-chemin */
const INK_LIEN = 0.5;

const SVG_BASCULE =
  '<svg viewBox="0 0 22 22" width="17" height="17" aria-hidden="true"><path d="M3 8h16" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><path d="M15.4 4.6 L19 8 L15.4 11.4" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M19 15H3" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><path d="M6.6 11.6 L3 15 L6.6 18.4" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
const SVG_PHOTO =
  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3.5" y="5" width="17" height="14" rx="2.5"/><path d="M1.5 14.5c2.6-5 5.2-5 7.2-1.6s4.400 3.4 6.4 0 4-4.4 7.400-3.4"/></svg>';
const SVG_X =
  '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 2 L10 10 M10 2 L2 10" fill="none" stroke-width="2" stroke-linecap="round"/></svg>';

const esc = (s: string): string =>
  s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]!);

function el<K extends keyof HTMLElementTagNameMap>(
  tag: K,
  attrs: Record<string, string> = {},
): HTMLElementTagNameMap[K] {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  return e;
}

/** un toucher net : appui puis lever à moins de 10 pt et 600 ms (SPEC-ECRANS §0) — au doigt, WebKit ne fabrique pas toujours de `click` */
function surToucher(cible: HTMLElement, f: (ev: PointerEvent) => void): void {
  let d: { x: number; y: number; t: number; id: number } | null = null;
  cible.addEventListener('pointerdown', (ev) => {
    d = { x: ev.clientX, y: ev.clientY, t: ev.timeStamp, id: ev.pointerId };
  });
  cible.addEventListener('pointerup', (ev) => {
    const g = d;
    d = null;
    if (!g || g.id !== ev.pointerId) return;
    if (Math.hypot(ev.clientX - g.x, ev.clientY - g.y) > 10 || ev.timeStamp - g.t > 600) return;
    f(ev);
  });
  cible.addEventListener('pointercancel', () => {
    d = null;
  });
}

function avecAlpha(h: string, a: number): string {
  const [r, g, b] = [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  return `rgba(${String(r)}, ${String(g)}, ${String(b)}, ${String(a)})`;
}

export function monterPagePlus(facade: Facade, magasin: Magasin, nav: Navigation): PagePlus {
  const h = horloge();
  const dv = facade.appareil();

  // ── la feuille ──
  const cs = el('div', { id: 'createSheet', class: 'pp', role: 'dialog' });
  cs.hidden = true;
  const cv = el('canvas', { id: 'csTrameCv', 'aria-hidden': 'true' });
  const plateau = el('div', { class: 'enh' });
  const mot = el('div', { class: 'cs-mark enh-t' });
  const croix = el('div', { class: 'closeb', role: 'button', 'aria-label': T.fermer, 'data-close': '' });
  const croixG = el('span', { class: 'cb-mot' });
  croixG.textContent = T.fermerGlyphe;
  croix.appendChild(croixG);
  plateau.append(mot, croix);
  const nid = el('div', { class: 'ph-photo-nid' });
  const photo = el('button', { type: 'button', class: 'ph-photo-btn', 'aria-label': T.photo });
  photo.innerHTML = SVG_PHOTO;
  photo.style.backgroundColor = avecAlpha(palette.brun09, 0.18);
  nid.appendChild(photo);
  const phrase = el('div', { id: 'csPhrase', class: 'pp-phrase' });
  const txt = el('div', { class: 'ph-txt' });
  const choixHote = el('div', { id: 'csChoix', class: 'ph-choix' });
  phrase.append(txt, choixHote);
  const pinceau = el('div', { id: 'csPinceau', 'data-glisse': '' });
  const rail = el('div', { id: 'csPinceauRail', class: 'pc-rail' });
  pinceau.appendChild(rail);
  const garder = el('div', { class: 'pp-garder inactif', role: 'button', 'aria-disabled': 'true' });
  garder.textContent = T.garder;
  const barre = el('div', { id: 'csBotBar', role: 'button', 'aria-label': T.peaufiner });
  const barreLab = el('span', { class: 'cbb-lab' });
  barreLab.textContent = T.peaufiner;
  const barreChev = el('span', { class: 'cbb-chev', 'aria-hidden': 'true' });
  barreChev.textContent = T.chevron;
  barre.append(barreLab, barreChev);
  const saisie = el('input', {
    class: 'ph-in',
    id: 'phIn',
    type: 'text',
    enterkeyhint: 'done',
    autocomplete: 'off',
    'aria-label': T.titresChoix.titre,
    // le champ est caché (la phrase EST la saisie, C-004) : il s'ouvre en touchant la pastille du titre ou du nom — il le déclare
    // (redteam_champs y passe par cette porte)
    'data-porte': '.pp-phrase .ph-m[data-ph="titre"], .pp-phrase .ph-m[data-np="nom"]',
  });
  saisie.style.cssText =
    'position:absolute;left:0;top:0;width:1px;height:1px;opacity:0;border:0;padding:0;margin:0;pointer-events:none;font-size:16px';
  cs.append(cv, phrase, pinceau, garder, barre, plateau, nid, saisie);
  for (const p of PINCEAUX) {
    const b = el('button', { type: 'button', class: 'pc-t' + (p.libre ? '' : ' pc-mur'), 'data-t': p.nom });
    const e = el('span', { class: 'pc-e' });
    if (p.dessin)
      e.innerHTML = `<svg width="60" height="11.7" viewBox="0 0 60 11.7" fill="none" aria-hidden="true">${p.dessin}</svg>`;
    const n = el('span', { class: 'pc-n' });
    n.textContent = p.nom;
    b.append(e, n);
    surToucher(b, () => {
      // un pinceau de Ma Parole ! est un MUR : il ne se choisit pas (C-196 ; sa phrase de mur : lot 8)
      if (!p.libre) return;
      P.pinceau = p.nom;
      majRail();
      majGarder();
    });
    rail.appendChild(b);
  }
  dv.appendChild(cs);

  // ── l'état de la page ──
  let P: PhrasePage = neuve('promi');
  let signature0 = '';
  let exemples: Partial<Record<TypeExemple, string>> = {};
  let prenomRang = 0;
  let choix: 'qui' | 'avec' | 'membres' | null = null;
  let saisieDe: 'titre' | 'nom' | null = null;
  let dalleT: { w: number; h: number; nat: Nature } | null = null;
  let repris: number | null = null;
  let mise = { base: 312, amp: 36, hz: 0, nl: 2, taille: 36 };

  function neuve(nat: Nature): PhrasePage {
    return { nat, sens: 'soi', titre: '', qui: [], avec: [], nom: '', membres: [], pinceau: 'Plein', moi: false };
  }
  const largeur = (): number => cs.clientWidth || 390;
  const haut0 = (): number => parseFloat(getComputedStyle(cs).getPropertyValue('--pp-h')) || 0;

  /** l'exemple de la pastille vide de ce type, pour cette ouverture (un tirage par ouverture) */
  function exemple(t: TypeExemple): string {
    const deja = exemples[t];
    if (deja != null) return deja;
    const L = EXEMPLES[t];
    const rang = magasin.tirerExemple(t, L.length, EXEMPLES_FIXES[t], Math.random);
    const v = L[rang] ?? L[0]!;
    exemples[t] = v;
    return v;
  }
  const typeExemple = (): TypeExemple => (P.nat === 'promi' ? P.sens : P.nat);
  const pluriel = (): boolean => P.qui.length > 1;

  // ── LA PHRASE ──
  const pastille = (cle: string, texte: string, vide: boolean, attr = 'data-ph'): string =>
    `<span class="ph-m${vide ? ' ph-vide' : ''}" ${attr}="${cle}">${esc(texte)}</span>`;
  function titrePastille(): { html: string; li: string } {
    const v = P.titre.trim();
    const ex = variante(exemple(typeExemple()), pluriel());
    const li = elision(v || ex);
    const cls = li === 'd’' ? 'ph-li ph-elide' : 'ph-li';
    return {
      li,
      html: `<em class="${cls}">${li}</em> <span class="ph-m${v ? '' : ' ph-vide'}" data-ph="titre" data-plein="${esc(v || ex)}">${esc(v || ex)}</span>`,
    };
  }
  function htmlPhrase(): string {
    const n = P.nat;
    if (n === 'nuee') {
      const nom = P.nom.trim();
      const ex = exemple('nuee');
      const avec = P.membres.length ? P.membres.join(' · ') : T.vides.toutLeMonde;
      return (
        `<span class="ph-b ph-b-fixe">${esc(T.cercle)}</span><br>` +
        `<em>${T.liaisons.nomme}</em> <span class="ph-m${nom ? '' : ' ph-vide'}" data-np="nom" data-plein="${esc(nom || ex)}">${esc(nom || ex)}</span><br>` +
        `<em>${T.liaisons.avec}</em> ${pastille('avec', avec, !P.membres.length, 'data-np')}`
      );
    }
    const titre = titrePastille().html;
    if (n === 'chiche') {
      const qui = P.qui.length ? P.qui.join(', ') + ',' : P.moi ? T.vides.moi : T.vides.quiOse;
      const verbe = P.qui.length ? T.chiche.toLowerCase() : T.chiche;
      const avec = P.avec.length ? P.avec.join(', ') : T.vides.quiEnEst;
      return (
        `<em>${T.liaisons.a}</em> ${pastille('qui', qui, !P.qui.length)}<br>` +
        `<span class="ph-b ph-b-fixe" data-ph="sens">${verbe}</span> <br>${titre}<br>` +
        `<em>${T.liaisons.avec}</em> ${pastille('avec', avec, !P.avec.length)}`
      );
    }
    // (après le verbe, une espace avant le retour à la ligne : le texte de la phrase est celui du prototype, sans effet à l'écran)
    const verbe = (v: string): string => `<span class="ph-b" data-ph="sens">${esc(v)}${SVG_BASCULE}</span>`;
    if (P.sens === 'soi') return `${verbe(T.verbe.soi)} <br>${titre}`;
    if (P.sens === 'faire') {
      const qui = P.qui.length ? P.qui.join(', ') : P.moi ? T.vides.moi : T.vides.qui;
      return `${verbe(T.verbe.faire)} <br>${titre}<br><em>${T.liaisons.a}</em> ${pastille('qui', qui, !P.qui.length)}`;
    }
    const prenom = P.qui.length ? P.qui.join(', ') + ',' : PRENOMS_EXEMPLE[prenomRang]!;
    return `${pastille('qui', prenom, !P.qui.length)}<br>${verbe(pluriel() ? T.verbe.demanderPluriel : T.verbe.demander)} <br>${titre}`;
  }

  const lignes = (): number => txt.querySelectorAll('br').length + 1;
  const appli = (t: number): void => {
    txt.style.setProperty('font-size', `${String(t)}px`);
    // v102 : l'interligne d'une étiquette est 1,2 × la taille × l'agrandissement des faces (112 %, v96), plus 24
    txt.style.setProperty('line-height', `${String(Math.floor(t * 1.2 * 1.12) + 24)}px`);
  };
  /** la plus longue ligne rendue de la phrase, en pt (la mesure du §2.8 corrigé) */
  const mesure = (t: number): number => {
    appli(t);
    txt.style.whiteSpace = 'nowrap';
    const w = txt.scrollWidth;
    txt.style.whiteSpace = '';
    return w;
  };

  /**
   * §2.8 (v20, v46, v115, v180b) — la taille de la phrase : 36 si elle tient en trois lignes, 34 à quatre, 30 au-delà (30 sur un choix ouvert),
   * réduite tant qu'une ligne dépasse la largeur ; plutôt que de descendre sous la taille de départ, l'EXEMPLE se coupe en deux morceaux
   * équilibrés (jamais seul après « de »), sinon en trois, à la plus grande taille où une coupe tient ; la coupe change le nombre de lignes,
   * donc la taille de départ : on recommence une fois, et une troisième passe fige (la bascule de v150). Puis C-240 : la phrase laisse la
   * place du rail (12 · 44 · 12) au-dessus de « garder de côté », sinon elle perd un point et l'on recompose.
   */
  function composerPhrase(ouvert: boolean, cap: number): { taille: number; nl: number } {
    const lim = largeur() - 48;
    txt.innerHTML = htmlPhrase();
    let taille = 36;
    let nlAvant = lignes();
    for (let passe = 0; passe < 3; passe++) {
      const pmC = txt.querySelector<HTMLElement>('.ph-m.ph-vide[data-ph="titre"], .ph-m.ph-vide[data-np="nom"]');
      const plein = pmC?.getAttribute('data-plein') ?? '';
      if (passe === 2) break;
      nlAvant = lignes();
      txt.classList.remove('ph-coupe');
      if (pmC) pmC.textContent = plein;
      let depart = ouvert ? 30 : nlAvant <= 3 ? 36 : nlAvant === 4 ? 34 : 30;
      if (cap) depart = Math.min(depart, cap);
      let t = depart;
      while (t > 16 && mesure(t) > lim) t--;
      taille = t;
      if (t < depart && pmC && !ouvert) {
        const mots = plein.split(' ');
        const bord = (): number => {
          const R = txt.getBoundingClientRect();
          let d = 0;
          for (const q of pmC.getClientRects()) d = Math.max(d, q.right - R.left);
          return d;
        };
        const html = (ks: number[]): string => {
          const p = [0, ...ks, mots.length];
          const o: string[] = [];
          for (let j = 0; j < p.length - 1; j++)
            o.push(`<span style="white-space:nowrap">${esc(mots.slice(p[j], p[j + 1]).join(' '))}</span>`);
          return o.join('<br>');
        };
        let trouve: { t: number; ks: number[] } | null = null;
        if (mots.length > 1) {
          txt.classList.add('ph-coupe');
          for (let tt = depart; tt >= PLANCHER_PH && !trouve; tt--) {
            appli(tt);
            let best: { k: number; ec: number } | null = null;
            for (let kk = 1; kk < mots.length; kk++) {
              pmC.innerHTML = html([kk]);
              if (bord() > lim || mesure(tt) > lim) continue;
              const rq = pmC.getClientRects();
              const L = [...rq].map((q) => q.width);
              let ec = L.length >= 2 ? Math.abs(L[0]! - L[L.length - 1]!) : 1e9;
              if (rq.length && rq[0]!.left - txt.getBoundingClientRect().left < 20) ec += 1e6;
              if (!best || ec < best.ec) best = { k: kk, ec };
            }
            if (best && best.ec < 1e6) trouve = { t: tt, ks: [best.k] };
          }
          for (let t3 = depart; t3 >= PLANCHER_PH && !trouve && mots.length > 2; t3--) {
            appli(t3);
            let b3: { ks: number[]; e: number } | null = null;
            for (let a1 = 1; a1 < mots.length - 1; a1++)
              for (let a2 = a1 + 1; a2 < mots.length; a2++) {
                pmC.innerHTML = html([a1, a2]);
                if (bord() > lim || mesure(t3) > lim) continue;
                const q3 = pmC.getClientRects();
                if (!q3.length || q3[0]!.left - txt.getBoundingClientRect().left < 20) continue;
                const w3 = [...q3].map((q) => q.width).slice(1);
                const e3 = Math.max(...w3) - Math.min(...w3);
                if (!b3 || e3 < b3.e) b3 = { ks: [a1, a2], e: e3 };
              }
            if (b3) trouve = { t: t3, ks: b3.ks };
          }
        }
        if (trouve) {
          taille = trouve.t;
          appli(taille);
          pmC.innerHTML = html(trouve.ks);
        } else {
          txt.classList.remove('ph-coupe');
          pmC.textContent = plein;
        }
      }
      appli(taille);
      if (lignes() === nlAvant) break;
    }
    return { taille, nl: lignes() };
  }

  /** le bas de l'encre de la phrase (le TEXTE, pas les boîtes), en pt du cadre */
  function basEncre(): number {
    const r = document.createRange();
    r.selectNodeContents(txt);
    const C = cs.getBoundingClientRect();
    let b = 0;
    for (const q of r.getClientRects()) if (q.width > 1 && q.height > 1) b = Math.max(b, q.bottom - C.top);
    return b;
  }

  // ── LE CHAMP : l'aplat de la nature au-dessus de la vague, la dalle d'avance ──
  function peindreChamp(base: number, amp: number, hz: number, H: number): void {
    const W = largeur();
    const dpr = Math.max(2, Math.min(3, window.devicePixelRatio || 2));
    cv.width = Math.round(W * dpr);
    cv.height = Math.round(H * dpr);
    cv.style.width = `${String(W)}px`;
    cv.style.height = `${String(H)}px`;
    const g = cv.getContext('2d');
    if (!g) return;
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.clearRect(0, 0, W, H);
    g.imageSmoothingEnabled = true;
    g.imageSmoothingQuality = 'high';
    const y = onde(base + hz, amp, W);
    g.beginPath();
    cheminOnde(g, y, 0, W, W);
    g.lineTo(W, 0);
    g.lineTo(0, 0);
    g.closePath();
    g.fillStyle = CHAMP[P.nat];
    g.fill();
    cv.setAttribute('data-champ', CHAMP[P.nat]);
    // C-241 : la dalle que CETTE parole aura (Promi, Chiche), sa taille fixée à l'ouverture (C-234), 16 pt plus bas tant que l'horizon est
    // bas (Q599) ; sous la vague quand le champ descend sous elle (un choix ouvert)
    if (!dalleT) return;
    const dw = dalleT.w;
    const dh = dalleT.h;
    const x = Math.floor((W - dw) / 2);
    const yD = 88 + (hz > 0 ? 16 : 0);
    const sous = choix !== null;
    const clip = (): void => {
      g.save();
      g.beginPath();
      cheminOnde(g, y, 0, W, W);
      g.lineTo(W, 0);
      g.lineTo(0, 0);
      g.closePath();
      g.clip();
    };
    if (P.nat === 'nuee') {
      // un Cercle n'a pas de dalle d'avance : la page + montre la dalle d'une parole d'un Cercle (de préférence entière), teinte par la rampe
      // de sa nature (Q30, peinte par le moteur) ; à défaut, la dernière parole (le prototype, `trait()`)
      const ps = magasin.etat().paroles;
      const pool = ps.filter((q) => !q.draft && !!q.nuee);
      const entieres = pool.filter((q) => facade.dalleEntiere(q.id));
      const id = (entieres.at(-1) ?? pool.at(-1) ?? ps.at(-1))?.id;
      if (id == null) return;
      if (sous) clip();
      const hex = (v: string): number[] => [1, 3, 5].map((i) => parseInt(v.slice(i, i + 2), 16));
      const r = facade.poserDalle(g, id, x, yD, dw, dh, {
        rampe: { cols: [palette.rampeCercle1, palette.rampeCercle2, palette.rampeCercle3].map(hex), haut: 2 },
        courant: 1,
      });
      if (sous) g.restore();
      if (r) cv.setAttribute('data-matiere', [r.x, r.y, r.w, r.h].map((v) => Math.round(v)).join(','));
      return;
    }
    const av = facade.dalleAvenir(magasin.etat().compteurs.nid, dw * dpr, dh * dpr, {
      chiche: P.nat === 'chiche',
      title: P.titre.trim(),
      who: P.qui.length ? P.qui.join(', ') : 'moi',
    });
    if (!av) return;
    if (sous) clip();
    facade.poserUn(g, av, x + dw / 2, yD + dh / 2);
    if (sous) g.restore();
    const aw = av.width / dpr;
    const ah = av.height / dpr;
    cv.setAttribute(
      'data-matiere',
      [x + dw / 2 - aw / 2, yD + dh / 2 - ah / 2, aw, ah].map((v) => Math.round(v)).join(','),
    );
  }

  /** v164a (C-201) : le bouton photo au-dessus de l'encre du trait, 8 pt d'air (`hautBouton` du prototype) */
  function hautBouton(base: number, amp: number): number {
    const W = largeur();
    const y = onde(base, amp, W);
    const ep = Math.max(5 * TRAIT_K, 6 * TRAIT_PTS, 4.5 * TRAIT_PTS);
    let m = 1e9;
    for (let x = W - 24 - 34 - 2; x <= W - 24 + 2; x += 2) m = Math.min(m, y(x));
    return Math.round(Math.min(y(W - 41) - 52, m - ep - 8 - 34));
  }

  // ── LA COMPOSITION ──
  function composer(): void {
    const ouvert = choix !== null;
    const dh = haut0();
    cs.classList.remove(...NATURES.map((n) => 'pp-' + n));
    cs.classList.add('pp-' + P.nat);
    cs.classList.toggle('pp-ouvert', ouvert);
    phrase.id = P.nat === 'nuee' ? 'nueePhrase' : 'csPhrase';
    choixHote.id = P.nat === 'nuee' ? 'nueeChoix' : 'csChoix';
    mot.innerHTML = '';
    if (P.nat === 'promi') {
      mot.append(T.mots.promi);
      const i = el('i', { class: 'mm-i' });
      i.textContent = T.mots.promiI;
      mot.appendChild(i);
    } else mot.textContent = P.nat === 'chiche' ? T.mots.chiche : T.mots.nuee;

    let cap = 0;
    let r = composerPhrase(ouvert, cap);
    let base = 0;
    let amp = 36;
    for (let essai = 0; essai < 20; essai++) {
      base = ouvert ? 144 : Math.max(196, 344 - 32 * (r.nl - 1));
      amp = ouvert ? 16 : 36;
      const boite = base + amp + 60;
      phrase.style.top = `calc(var(--pp-h) + ${String(ouvert ? 228 + DT : boite + 6 + DY_PHRASE[P.nat] + DT)}px)`;
      if (ouvert) break;
      // C-240 : la place du rail et de son air au-dessus de « garder de côté »
      const gTop = garder.getBoundingClientRect().top - cs.getBoundingClientRect().top;
      const trop = basEncre() - DY_PHRASE[P.nat] + 12 + 44 + 12 - gTop;
      if (trop <= 0.5 || r.taille <= 16) break;
      cap = r.taille - 1;
      r = composerPhrase(ouvert, cap);
    }
    // la dalle : sa taille se fixe à la première composition de l'ouverture, sur la base au repos (C-234)
    if (!dalleT || dalleT.nat !== P.nat) {
      const bR = Math.max(196, 344 - 32 * (r.nl - 1));
      const h0 = Math.min(300, bR - 112);
      dalleT = { h: h0, w: Math.min(320, Math.floor(1.2 * h0)), nat: P.nat };
    }
    // C-229 : l'horizon bas, 12 pt au-dessus de l'encre de la phrase au plus
    const C = cs.getBoundingClientRect();
    let hautPills = 1e9;
    for (const n of txt.querySelectorAll(':scope > .ph-m, :scope > .ph-b')) {
      const q = n.getBoundingClientRect();
      if (q.width) hautPills = Math.min(hautPills, q.top - C.top - dh);
    }
    const W = largeur();
    const hz = Math.max(0, Math.min(HZ_BAS, Math.floor((hautPills - HZ_AIR - basOnde(onde(base, amp, W), W)) * 2) / 2));
    peindreChamp(base, amp, hz, base + amp + 60 + hz);
    photo.style.top = `calc(var(--pp-h) + ${String(hautBouton(base, amp))}px)`;
    mise = { base, amp, hz, nl: r.nl, taille: r.taille };
    // le rail : à mi-chemin, à l'encre, entre la phrase et « garder de côté » (il se compte comme si la phrase n'avait pas remonté)
    pinceau.hidden = ouvert;
    garder.hidden = ouvert;
    if (!ouvert) {
      let dessus = 0;
      for (const n of txt.querySelectorAll(':scope > .ph-m, :scope > .ph-b')) {
        const q = n.getBoundingClientRect();
        if (q.width) dessus = Math.max(dessus, q.bottom - C.top);
      }
      dessus -= DY_PHRASE[P.nat];
      const dessous = garder.getBoundingClientRect().top - C.top + INK_LIEN - 10;
      pinceau.style.top = `${String(Math.round((dessus + (dessous - dessus - 44) / 2) * 4) / 4)}px`;
    }
    majRail();
    majGarder();
    rendreChoix();
  }

  function majRail(): void {
    for (const b of rail.children) {
      const on = (b as HTMLElement).dataset['t'] === P.pinceau;
      b.classList.toggle('on', on);
      // l'état du choix, dit à VoiceOver (et aux juges : un pinceau déjà choisi n'a rien à changer)
      if (!b.classList.contains('pc-mur')) b.setAttribute('aria-pressed', on ? 'true' : 'false');
    }
  }

  // ── « GARDER DE CÔTÉ » (C-149) : actif quand la page a changé depuis son ouverture ──
  const signature = (): string =>
    [
      P.nat,
      P.sens,
      P.titre.trim(),
      P.qui.join('|'),
      P.avec.join('|'),
      P.nom.trim(),
      P.membres.join('|'),
      P.pinceau,
    ].join('¦');
  function majGarder(): void {
    const actif = signature() !== signature0;
    garder.classList.toggle('inactif', !actif);
    garder.setAttribute('aria-disabled', actif ? 'false' : 'true');
    // ⚑ C-330 (Tom, 22 nov. 2026) : inactif, il prend la teinte de SA NATURE — #82AEF8 · #FFB8D2 · #C9A8F5 (le champ). Le prototype le
    // sort bleu ou lilas selon une course : l'app ne copie pas ce défaut (écart admis, nommé dans le test d'identité)
    if (actif) garder.style.removeProperty('color');
    else garder.style.setProperty('color', CHAMP[P.nat]);
  }
  surToucher(garder, () => {
    if (garder.classList.contains('inactif')) return;
    const b: Brouillon = {
      v: 1,
      nat: P.nat,
      phrase: {
        sens: P.nat === 'chiche' ? 'chiche' : P.sens === 'demander' ? 'demander' : 'faire',
        titre: P.titre,
        qui: P.qui.join(', ') || 'Moi',
        avec: P.avec.join(', '),
      },
      who: [...P.qui],
      sens: P.sens,
      nom: P.nom.trim(),
      membres: [...P.membres],
      pinceau: P.pinceau,
    };
    const titre = (P.nat === 'nuee' ? P.nom : P.titre).trim() || T.sansTitre;
    const qui = P.qui.length ? P.qui.join(', ') : 'moi';
    magasin.garderDeCote(b, titre, P.nat === 'nuee' ? T.leGroupe : qui, repris, Date.now());
    fermer();
  });

  // ── LE CHOIX DES PERSONNES (lot-GENS) : « Moi » ou « tout le monde » en tête, les connus, « + ajouter quelqu'un » ──
  function connus(): string[] {
    const e = magasin.etat();
    const out: string[] = [];
    const vu = (n: string): void => {
      const m = n.trim();
      if (m && !/^(moi|le groupe|tout le monde)$/i.test(m) && !out.includes(m)) out.push(m);
    };
    for (const p of [...e.paroles].reverse())
      for (const w of [p.who, p.from, (p.suite?.['avec'] as string | undefined) ?? ''])
        for (const n of String(w ?? '').split(/\s*[,·]\s*/)) vu(n);
    for (const v of e.personnes) if (typeof v === 'string') for (const n of v.split(/\s*[,·]\s*/)) vu(n);
    for (const l of Object.values(e.membres)) for (const n of l) vu(n);
    return out;
  }
  const liste = (): string[] => (choix === 'qui' ? P.qui : choix === 'avec' ? P.avec : P.membres);
  function rendreChoix(): void {
    choixHote.innerHTML = '';
    choixHote.classList.toggle('ouvert', choix !== null);
    if (!choix) return;
    const pris = liste();
    const noms = [...pris];
    for (const n of connus()) if (!noms.includes(n) && noms.length < pris.length + 6) noms.push(n);
    const gn = el('div', { class: 'ph-opts gn', 'data-nat': P.nat });
    const gl = el('div', { class: 'gn-liste' });
    const tete = P.nat === 'nuee' ? T.toutLeMonde : T.moi;
    const teteOn = !pris.length;
    const bouton = (nom: string, on: boolean, tetee: boolean): HTMLElement => {
      const b = el('button', { type: 'button', class: 'ph-o' + (on ? ' on' : '') });
      if (tetee) b.dataset['gnTete'] = '1';
      else b.dataset['v'] = nom;
      if (!(tetee && P.nat === 'nuee')) {
        const ini = el('span', { class: 'ppo-ini' });
        ini.textContent = nom.charAt(0).toUpperCase();
        b.appendChild(ini);
      }
      const nm = el('span', { class: 'ppo-nom' });
      nm.textContent = nom;
      b.appendChild(nm);
      if (on && !(tetee && P.nat === 'nuee')) {
        const x = el('span', { class: 'ppo-x', role: 'button', 'aria-label': `${T.retirer} ${nom.toLowerCase()}` });
        x.innerHTML = SVG_X;
        b.appendChild(x);
      }
      surToucher(b, (ev) => {
        const L = liste();
        if (tetee) L.splice(0);
        else if ((ev.target as Element).closest('.ppo-x') || L.includes(nom)) L.splice(L.indexOf(nom), 1);
        else L.push(nom);
        composer();
      });
      return b;
    };
    gl.appendChild(bouton(tete, teteOn, true));
    for (const n of noms) gl.appendChild(bouton(n, pris.includes(n), false));
    const ajout = el('div', { class: 'ph-o ph-add', role: 'button', tabindex: '0', 'data-add': '1' });
    ajout.textContent = T.ajouter;
    gn.append(gl, ajout);
    choixHote.appendChild(gn);
    // sous la phrase (28 pt d'air) ; la liste montre autant de RANGÉES entières que la place en laisse pour que « + ajouter quelqu'un »
    // reste au-dessus de la barre Peaufiner, 16 pt d'air (v116, `_gensBorne`) — elle défile pour le reste
    const haut = txt.offsetHeight + 28;
    gn.style.top = `${String(haut)}px`;
    const C = cs.getBoundingClientRect();
    const debut = phrase.getBoundingClientRect().top - C.top + haut;
    const fin = barre.getBoundingClientRect().top - C.top - 16;
    let n = 1;
    while (debut + 52 * (n + 1) + 8 * n + 8 + 14 + 52 <= fin) n++;
    gl.style.maxHeight = `${String(52 * n + 8 * (n - 1))}px`;
  }

  // ── LES GESTES DE LA PHRASE ──
  surToucher(txt, (ev) => {
    const t = ev.target as Element;
    const sens = t.closest('[data-ph="sens"]');
    if (sens && P.nat === 'promi') {
      // le cycle du verbe (SPEC-ECRANS §3) : « Je me promets » → « Je promets … à qui ? » → « qui ?, promets-moi » → retour
      P.sens = P.sens === 'soi' ? 'faire' : P.sens === 'faire' ? 'demander' : 'soi';
      if (P.sens === 'demander') prenomRang = magasin.avancerPrenom();
      choix = null;
      composer();
      return;
    }
    let m = t.closest<HTMLElement>('.ph-m');
    // un titre ou un nom sur deux lignes a un creux entre ses lignes : le doigt y tombe sur la phrase, et la saisie s'ouvre quand même
    // (v180b, C-234 — un déclencheur lu sur la pastille seule manquait ces touchers)
    if (!m && !t.closest('em, .ph-b'))
      for (const c of txt.querySelectorAll<HTMLElement>('.ph-m[data-ph="titre"], .ph-m[data-np="nom"]')) {
        const q = c.getBoundingClientRect();
        if (ev.clientX >= q.left && ev.clientX <= q.right && ev.clientY >= q.top && ev.clientY <= q.bottom) m = c;
      }
    if (!m) return;
    const cle = m.dataset['ph'] ?? m.dataset['np'];
    if (cle === 'titre' || cle === 'nom') {
      ouvrirSaisie(cle);
      return;
    }
    if (cle === 'qui' || cle === 'avec') {
      // C-304 : la place du destinataire (sans personne, hors « promets-moi ») passe à « moi »
      if (cle === 'qui' && !P.qui.length && P.sens !== 'demander') P.moi = true;
      choix = P.nat === 'nuee' ? 'membres' : cle;
      composer();
    }
  });

  // ── LA SAISIE (le titre, le nom d'un Cercle) : le clavier s'ouvre DANS le geste ; la frappe remplit la pastille ; Retour valide ──
  function ouvrirSaisie(de: 'titre' | 'nom'): void {
    saisieDe = de;
    choix = null;
    saisie.value = de === 'nom' ? P.nom : P.titre;
    saisie.maxLength = de === 'nom' ? 40 : 280;
    saisie.focus({ preventScroll: true });
    cs.classList.add('pp-saisie');
  }
  saisie.addEventListener('input', () => {
    if (!saisieDe) return;
    if (saisieDe === 'nom') P.nom = saisie.value;
    else P.titre = saisie.value;
    composer();
  });
  saisie.addEventListener('keydown', (ev) => {
    if (ev.key === 'Enter') {
      ev.preventDefault();
      saisie.blur();
    }
  });
  saisie.addEventListener('blur', () => {
    saisieDe = null;
    cs.classList.remove('pp-saisie');
    composer();
  });

  // un toucher ailleurs que sur le choix des personnes le referme
  surToucher(cs, (ev) => {
    if (!choix) return;
    const t = ev.target as Element;
    if (t.closest('.gn') || t.closest('.ph-m')) return;
    choix = null;
    composer();
  });

  // ── OUVRIR, FERMER ──
  function ouvrir(nat: Nature): void {
    P = neuve(nat);
    exemples = {};
    choix = null;
    saisieDe = null;
    dalleT = null;
    repris = null;
    const r = magasin.etat().autres['promi_ex_prenom'];
    prenomRang = r != null && r !== '' && +r >= 0 ? +r % 2 : 0;
    if (finFermeture != null) h.annuleMinuteur(finFermeture);
    if (finOuverture != null) h.annuleMinuteur(finOuverture);
    cs.classList.remove('pp-part', 'pp-entre');
    // composée cachée, en bas (v103 : rien ne paraît une fraction de seconde à moitié composé)…
    // (composée à sa place : ses mesures se lisent sur l'écran, jamais sous la réduction du départ)
    cs.classList.add('pp-compose');
    cs.hidden = false;
    composer();
    signature0 = signature();
    majGarder();
    cs.classList.add('pp-bas');
    cs.classList.remove('pp-compose');
    // …puis ⚑ C-331 (Tom, 22 nov. 2026) : elle MONTE, le mouvement exact de sa fermeture à l'envers — même courbe, même durée, la même
    // règle (`pp-bas` ↔ `pp-part`, page-plus.css) ; l'accueil reste dessous pendant qu'elle monte, il n'est couvert qu'à l'arrivée
    cs.getBoundingClientRect();
    cs.classList.add('pp-entre');
    cs.classList.remove('pp-bas');
    finOuverture = h.minuteur(() => {
      finOuverture = null;
      cs.classList.remove('pp-entre');
      // la page couvre l'appareil : ce qui est dessous (l'accueil, la Toile) ne se voit plus et ne prend plus le doigt (base.css, `.couvert`)
      cs.classList.add('couvre');
      dv.classList.add('couvert');
    }, 480);
  }
  let finOuverture: number | null = null;
  let finFermeture: number | null = null;
  function fermer(): void {
    if (cs.hidden || cs.classList.contains('pp-part')) return;
    if (finOuverture != null) {
      h.annuleMinuteur(finOuverture);
      finOuverture = null;
    }
    cs.classList.remove('pp-entre');
    saisie.blur();
    // l'accueil reparaît dessous, la page glisse par-dessus lui
    dv.classList.remove('couvert');
    cs.classList.add('pp-part');
    if (finFermeture != null) h.annuleMinuteur(finFermeture);
    finFermeture = h.minuteur(() => {
      finFermeture = null;
      cs.hidden = true;
      cs.classList.remove('pp-part');
    }, 480);
  }
  surToucher(croix, () => {
    fermer();
  });
  nav.poser('pagePlus', (arg) => {
    const n = NATURES.includes(arg as Nature) ? (arg as Nature) : 'promi';
    ouvrir(n);
  });
  // une police chargée après coup, une autre largeur : la page se recompose
  const surTaille = (): void => {
    if (!cs.hidden && !cs.classList.contains('pp-part')) composer();
  };
  window.addEventListener('resize', surTaille);

  return {
    racine: cs,
    ouvrir,
    fermer,
    ouverte: () => !cs.hidden && !cs.classList.contains('pp-part'),
    etat: () => ({
      phrase: { ...P, qui: [...P.qui], avec: [...P.avec], membres: [...P.membres] },
      base: mise.base,
      amp: mise.amp,
      hz: mise.hz,
      lignes: mise.nl,
      taille: mise.taille,
      choix,
      gardeActif: !garder.classList.contains('inactif'),
      exemples: { ...exemples },
    }),
    detruire() {
      window.removeEventListener('resize', surTaille);
      cs.remove();
    },
  };
}
