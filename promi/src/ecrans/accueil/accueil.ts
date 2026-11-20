/**
 * L'ACCUEIL (lot 1) — posé sur la Toile vivante : le plateau (PROMI, Partager, Réglages), la barre (Studio, Aura, le +, Index, Fil),
 * le menu du + (les trois natures, sur place), le symbole « recadrer » (C-188). Le prototype rendu est la référence (accueil.css).
 *
 * Ce que l'accueil ne fait pas lui-même : il demande les écrans à la navigation (aucun n'est porté au lot 1 : la demande est notée) ;
 * il ne touche jamais le moteur (la façade) ; son temps est celui de l'horloge unique.
 */
import './accueil.css';
import type { Facade } from '../../moteur/facade.ts';
import type { Magasin } from '../../etat/magasin.ts';
import type { Navigation, Destination } from '../../navigation/navigation.ts';
import { horloge } from '../../animation/horloge.ts';
import { passageFlaques, type ControlePassage } from '../../animation/flaques/passage.ts';
import { ICONES, TRACES_RECADRER } from './icones.ts';
import { anneauCss } from './anneau.ts';
import { compteAnneau, filAttente } from '../../metier/fil.ts';
import { nParoles, rappelDu } from '../../metier/rappel.ts';
import { TEXTES_ACCUEIL as T } from '../../textes/accueil.ts';

function el<K extends keyof HTMLElementTagNameMap>(
  tag: K,
  attrs: Record<string, string>,
  html = '',
): HTMLElementTagNameMap[K] {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  if (html) e.innerHTML = html;
  return e;
}

/** un toucher net : appui puis lever à moins de 10 pt et 600 ms (au doigt, WebKit ne fabrique pas toujours de `click`) */
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

export interface Accueil {
  plateau: HTMLElement;
  barre: HTMLElement;
  choix: HTMLElement;
  recadre: HTMLElement;
  /** l'état du symbole « recadrer » (pour les tests) */
  etatRecadre(): string;
  detruire(): void;
}

export function monterAccueil(facade: Facade, magasin: Magasin, nav: Navigation): Accueil {
  const h = horloge();
  const dv = facade.appareil();

  // ── le plateau ──
  const plateau = el('div', { id: 'accPlat', class: 'acc-plat' });
  const mm = el('span', { class: 'acc-mm', role: 'button', 'aria-label': T.marqueVoix });
  mm.textContent = T.marque;
  const i = document.createElement('i');
  i.textContent = T.marqueI;
  mm.appendChild(i);
  const partager = el(
    'div',
    { id: 'shareBtn', class: 'acc-rond', role: 'button', 'aria-label': T.partager },
    ICONES.partager,
  );
  const reglages = el(
    'div',
    { id: 'settingsBtn', class: 'acc-rond', role: 'button', 'aria-label': T.reglages },
    ICONES.reglages,
  );
  plateau.append(mm, partager, reglages);

  // ── la barre ──
  const barre = el('div', { id: 'accBarre', class: 'acc-barre' });
  const entree = (id: string, icone: string, nom: string, vers: Destination): HTMLElement => {
    const e = el('div', { id, class: 'acc-entree', role: 'button', 'aria-label': nom }, icone);
    const l = el('span', { class: 'l' });
    l.textContent = nom;
    e.appendChild(l);
    surToucher(e, () => {
      nav.ouvrir(vers);
    });
    return e;
  };
  const studio = entree('studioBtn', ICONES.studio, T.studio, 'studio');
  const aura = entree('souffleBtn', ICONES.aura, T.aura, 'aura');
  const plus = el('div', { id: 'createBtn', class: 'acc-plus', role: 'button', 'aria-label': T.plus }, ICONES.plus);
  const index = entree('indexBtn', ICONES.index, T.index, 'index');
  const fil = entree('filBtn', ICONES.fil, T.fil, 'fil');
  const pastille = el('span', { id: 'filDot', class: 'acc-pastille' });
  fil.appendChild(pastille);
  barre.append(studio, aura, plus, index, fil);

  // ── le menu du + ──
  const choix = el('div', { id: 'accChoix', class: 'acc-choix' });
  for (const n of T.natures) {
    const p = el('div', { class: 'acc-pil', 'data-k': n.k, role: 'button' });
    const un = el('span', { class: 'acc-un' });
    un.append('Un ');
    const nat = el('i', { class: 'acc-nat' });
    nat.textContent = n.nom;
    un.appendChild(nat);
    const aide = document.createElement('small');
    aide.textContent = n.aide;
    p.append(un, aide);
    surToucher(p, () => {
      choix.classList.remove('ouvert');
      nav.ouvrir('pagePlus', n.k);
    });
    choix.appendChild(p);
  }
  surToucher(plus, () => {
    choix.classList.toggle('ouvert');
  });
  // un toucher ailleurs referme le menu (v165, chemin b : au doigt, il n'y a pas toujours de `click`)
  let ailleurs: { x: number; y: number; t: number } | null = null;
  const debutAilleurs = (ev: PointerEvent): void => {
    ailleurs = { x: ev.clientX, y: ev.clientY, t: ev.timeStamp };
  };
  const finAilleurs = (ev: PointerEvent): void => {
    const g = ailleurs;
    ailleurs = null;
    if (!g || !choix.classList.contains('ouvert')) return;
    if (Math.hypot(ev.clientX - g.x, ev.clientY - g.y) > 10 || ev.timeStamp - g.t > 600) return;
    const t = ev.target as Element | null;
    if (t?.closest('#accChoix') || t?.closest('#createBtn')) return;
    choix.classList.remove('ouvert');
  };
  window.addEventListener('pointerdown', debutAilleurs, true);
  window.addEventListener('pointerup', finAilleurs, true);

  surToucher(mm, () => {
    nav.ouvrir('offre');
  });
  surToucher(partager, () => {
    nav.ouvrir('partager');
  });
  surToucher(reglages, () => {
    nav.ouvrir('reglages');
  });

  // ── le symbole « recadrer » (C-188) : il naît en flaques quand la main bouge la vue, part en flaques après 4 s sans toucher ──
  const recadre = el(
    'div',
    { id: 'accRecadre', class: 'acc-recadre', role: 'button', 'aria-label': T.recadrer },
    ICONES.recadrer,
  );
  surToucher(recadre, (ev) => {
    ev.stopPropagation();
    facade.recadrer();
  });
  const DUREE = 300;
  const ATTENTE = 4000;
  let etat: 'absent' | 'nait' | 'la' | 'part' = 'absent';
  let tDernier = 0;
  let sig = '';
  let ctl: ControlePassage | null = null;
  const image = (): HTMLCanvasElement => {
    const d = Math.max(2, Math.min(3, window.devicePixelRatio || 2));
    const cv = document.createElement('canvas');
    cv.width = Math.round(44 * d);
    cv.height = Math.round(44 * d);
    const g = cv.getContext('2d')!;
    g.setTransform((d * 29) / 24, 0, 0, (d * 29) / 24, d * 7.5, d * 7.5);
    g.strokeStyle = getComputedStyle(recadre).color;
    g.lineWidth = 1.655;
    g.lineCap = 'round';
    g.lineJoin = 'round';
    for (const s of TRACES_RECADRER) g.stroke(new Path2D(s));
    return cv;
  };
  const arrete = (): void => {
    if (ctl) {
      ctl.arrete = true;
      ctl.canevas.remove();
      ctl = null;
    }
  };
  const nait = (): void => {
    arrete();
    etat = 'nait';
    recadre.classList.add('vu', 'cache');
    ctl = passageFlaques(recadre, {
      mode: 'couvre',
      image: image(),
      rect: [0, 0, 44, 44],
      duree: DUREE,
      devant: true,
      z: 1,
      fin: (c) => {
        if (etat !== 'nait') return;
        recadre.classList.remove('cache');
        c.canevas.remove();
        ctl = null;
        etat = 'la';
      },
    });
  };
  const part = (coupe: boolean): void => {
    arrete();
    if (coupe || etat === 'nait') {
      recadre.classList.remove('vu', 'cache');
      etat = 'absent';
      return;
    }
    etat = 'part';
    recadre.classList.add('cache');
    ctl = passageFlaques(recadre, {
      mode: 'ouvre',
      image: image(),
      rect: [0, 0, 44, 44],
      duree: DUREE,
      devant: true,
      z: 1,
      fin: () => {
        if (etat !== 'part') return;
        ctl = null;
        recadre.classList.remove('vu', 'cache');
        etat = 'absent';
      },
    });
  };
  const majRecadre = (): void => {
    const v = facade.vue();
    const s = v.s.toFixed(3) + '|' + v.ox.toFixed(1) + '|' + v.oy.toFixed(1);
    const bouge = s !== sig;
    sig = s;
    const t = h.maintenant();
    if (!facade.vueALaMain()) {
      if (etat === 'la' || etat === 'nait') part(false);
      return;
    }
    if (bouge) {
      tDernier = t;
      if (etat === 'absent' || etat === 'part') nait();
      return;
    }
    if (etat === 'la' && t - tDernier >= ATTENTE) part(false);
  };
  const touche = (): void => {
    tDernier = h.maintenant();
  };
  window.addEventListener('pointerdown', touche, { capture: true, passive: true });
  const veille = h.intervalle(majRecadre, 120);

  // ── le bandeau « Garder ta Toile » : relu toutes les 3 s (le prototype), et à chaque changement de l'état ──
  const rappel = el('div', { id: 'accRappel', class: 'acc-rappel' });
  const oui = el('span', { 'data-r': 'oui', role: 'button' });
  oui.textContent = T.garder;
  const non = el('span', { 'data-r': 'non', role: 'button' });
  non.textContent = T.plusTard;
  rappel.append(oui, non);
  const repond = (r: 'oui' | 'non'): void => {
    rappel.classList.remove('vu');
    magasin.repondreRappel(r, nParoles(magasin.etat()), Date.now());
    if (r === 'oui') nav.ouvrir('compte');
  };
  surToucher(oui, () => {
    repond('oui');
  });
  surToucher(non, () => {
    repond('non');
  });
  const majRappel = (): void => {
    if (rappelDu(magasin.etat(), Date.now())) rappel.classList.add('vu');
  };
  const veilleRappel = h.intervalle(majRappel, 3000);

  // ── l'anneau du + et la pastille du Fil suivent l'état ──
  const maj = (): void => {
    const e = magasin.etat();
    const v = anneauCss(compteAnneau(e));
    if (plus.style.getPropertyValue('--anneau') !== v) plus.style.setProperty('--anneau', v);
    pastille.hidden = filAttente(e) === 0;
    majRappel();
  };
  maj();
  const desabonne = magasin.abonner(() => {
    maj();
  });

  dv.append(plateau, rappel, barre, choix, recadre);
  return {
    plateau,
    barre,
    choix,
    recadre,
    etatRecadre: () => etat,
    detruire() {
      desabonne();
      h.annuleMinuteur(veille);
      h.annuleMinuteur(veilleRappel);
      arrete();
      window.removeEventListener('pointerdown', debutAilleurs, true);
      window.removeEventListener('pointerup', finAilleurs, true);
      window.removeEventListener('pointerdown', touche, { capture: true });
      for (const n of [plateau, rappel, barre, choix, recadre]) n.remove();
    },
  };
}
