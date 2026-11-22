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
import { masqueFlaques, passageFlaques, type ControlePassage } from '../../animation/flaques/passage.ts';
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
  /** l'état du symbole « recadrer », et depuis combien de ms la vue n'a pas bougé ni le doigt touché (pour les tests ; `_recadreEtat` du prototype) */
  etatRecadre(): { etat: string; depuis: number; remises: Array<{ t: number; pourquoi: string }> };
  detruire(): void;
}

export function monterAccueil(facade: Facade, magasin: Magasin, nav: Navigation): Accueil {
  const h = horloge();
  const dv = facade.appareil();
  /**
   * Une chose de l'accueil paraît ou part EN FLAQUES (C-329) : la scène du passage déjà porté (celle du symbole « recadrer »), posée en
   * MASQUE sur la chose elle-même (`masqueFlaques`) — elle paraît là où l'eau naît, ou s'efface ; rien de la Toile n'est recopié
   * (redteam_decoupe), et la Toile reste vivante dessous. Même durée que le symbole « recadrer » (300 ms).
   */
  const enFlaques = (cible: HTMLElement, sens: 'paraît' | 'part', fin: () => void): ControlePassage =>
    masqueFlaques(cible, {
      mode: sens === 'paraît' ? 'ouvre' : 'couvre',
      duree: 300,
      fin: (c) => {
        if (!c.arrete) fin();
      },
    });

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
      // la page + monte par-dessus le menu (C-331) : il reste dessous, et ne part qu'une fois recouvert — sinon il disparaîtrait d'un
      // coup sous la page encore transparente (C-271)
      nav.ouvrir('pagePlus', n.k);
      h.minuteur(() => {
        fermeMenu(true);
      }, 500);
    });
    choix.appendChild(p);
  }
  // ⚑ C-329 (Tom, 21 nov. 2026 : « aucun changement sec ») — le menu s'ouvre et se ferme EN FLAQUES (le passage déjà porté) ; dans le
  // prototype il paraît d'un coup : un des trois écarts admis, nommé dans le test d'identité
  let ctlMenu: ControlePassage | null = null;
  const ouvreMenu = (): void => {
    arreteMenu();
    choix.classList.add('ouvert');
    ctlMenu = enFlaques(choix, 'paraît', () => {
      ctlMenu = null;
    });
  };
  const fermeMenu = (coupe = false): void => {
    if (!choix.classList.contains('ouvert')) return;
    arreteMenu();
    if (coupe) {
      choix.classList.remove('ouvert');
      return;
    }
    ctlMenu = enFlaques(choix, 'part', () => {
      ctlMenu = null;
      choix.classList.remove('ouvert');
    });
  };
  const arreteMenu = (): void => {
    if (!ctlMenu) return;
    ctlMenu.stop?.();
    ctlMenu = null;
  };
  surToucher(plus, () => {
    if (choix.classList.contains('ouvert') && !(ctlMenu && ctlMenu.mode === 'couvre')) fermeMenu();
    else ouvreMenu();
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
    fermeMenu();
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
  /** ce qui a remis le compte de 4 s à zéro (les 20 derniers) : pour comprendre un écart sur une autre machine (les tests le lisent) */
  const remises: Array<{ t: number; pourquoi: string }> = [];
  const remise = (pourquoi: string): void => {
    remises.push({ t: Math.round(h.maintenant()), pourquoi });
    if (remises.length > 20) remises.shift();
  };
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
      remise('vue ' + s);
      if (etat === 'absent' || etat === 'part') nait();
      return;
    }
    if (etat === 'la' && t - tDernier >= ATTENTE) part(false);
  };
  const touche = (ev: PointerEvent): void => {
    tDernier = h.maintenant();
    remise(
      'doigt ' +
        ev.type +
        ' ' +
        ev.pointerType +
        ' ' +
        String(Math.round(ev.clientX)) +
        ',' +
        String(Math.round(ev.clientY)),
    );
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
  // ⚑ C-329 — le bandeau paraît et part EN FLAQUES (dans le prototype : d'un coup ; écart admis, nommé dans le test d'identité)
  let ctlRappel: ControlePassage | null = null;
  const partRappel = (): void => {
    if (!rappel.classList.contains('vu') || (ctlRappel && ctlRappel.mode === 'couvre')) return;
    if (ctlRappel) {
      ctlRappel.stop?.();
    }
    ctlRappel = enFlaques(rappel, 'part', () => {
      ctlRappel = null;
      rappel.classList.remove('vu');
    });
  };
  const repond = (r: 'oui' | 'non'): void => {
    partRappel();
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
    if (rappel.classList.contains('vu') || !rappelDu(magasin.etat(), Date.now())) return;
    rappel.classList.add('vu');
    ctlRappel = enFlaques(rappel, 'paraît', () => {
      ctlRappel = null;
    });
  };
  const veilleRappel = h.intervalle(majRappel, 3000);

  // ⚑ C-329 — la pastille du Fil s'ouvre et se referme SUR SON CENTRE, comme la pastille « pas encore vu » (C-247 : le même code,
  // `v201pop`, 0,26 s) ; au premier affichage elle est posée (rien ne change à l'écran : elle naît avec l'accueil)
  let pastillePremiere = true;
  const pastilleVue = (v: boolean): void => {
    const vue = !pastille.hidden && !pastille.classList.contains('part');
    if (pastillePremiere) {
      pastillePremiere = false;
      pastille.hidden = !v;
      return;
    }
    if (v === vue) return;
    pastille.classList.remove('nait', 'part');
    if (v) {
      pastille.hidden = false;
      pastille.getBoundingClientRect(); // l’animation repart du début
      pastille.classList.add('nait');
    } else {
      pastille.getBoundingClientRect(); // l’animation repart du début
      pastille.classList.add('part');
    }
  };
  pastille.addEventListener('animationend', () => {
    if (pastille.classList.contains('part')) pastille.hidden = true;
    pastille.classList.remove('nait', 'part');
  });
  // ── l'anneau du + et la pastille du Fil suivent l'état ──
  const maj = (): void => {
    const e = magasin.etat();
    const v = anneauCss(compteAnneau(e));
    if (plus.style.getPropertyValue('--anneau') !== v) plus.style.setProperty('--anneau', v);
    pastilleVue(filAttente(e) > 0);
    majRappel();
  };
  maj();
  const desabonne = magasin.abonner(() => {
    maj();
  });

  dv.classList.add('grain');
  dv.append(plateau, rappel, barre, choix, recadre);
  return {
    plateau,
    barre,
    choix,
    recadre,
    etatRecadre: () => ({ etat, depuis: Math.round(h.maintenant() - tDernier), remises: remises.slice() }),
    detruire() {
      desabonne();
      h.annuleMinuteur(veille);
      h.annuleMinuteur(veilleRappel);
      arrete();
      window.removeEventListener('pointerdown', debutAilleurs, true);
      window.removeEventListener('pointerup', finAilleurs, true);
      window.removeEventListener('pointerdown', touche, { capture: true });
      dv.classList.remove('grain');
      for (const n of [plateau, rappel, barre, choix, recadre]) n.remove();
    },
  };
}
