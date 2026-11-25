/**
 * LA FICHE D'UNE PERSONNE (SPEC-ECRANS §22 ; le prototype : `openPerson` de lot-FICHE-PERSONNE, PLANCHE-FICHE-PERSONNE-4, Q184, Q193 ; ses dalles
 * mènent à leur fiche, lot-DALLE-PORTE). Ce qui reste (Tom) : le nom, le visage, l'anneau sans chiffre (§2.9), « Tenu ensemble » (les paroles
 * tenues, en dalles, trois par rangée), « Ce que tu partages avec … » (les VRAIES cartes de l'Index : la dalle, le champ de sa nature, le trait qui
 * dit l'état — l'état n'est plus écrit), « + Planter un Promi » et « + Lancer un Chiche » (la page +, la personne déjà choisie). Tout le reste
 * sort. Elle monte du bas par-dessus l'écran d'où l'on vient ; son X la referme sur lui (C-193).
 */
import './personne.css';
import type { Facade } from '../../moteur/facade.ts';
import type { Magasin } from '../../etat/magasin.ts';
import type { Navigation } from '../../navigation/navigation.ts';
import type { Parole } from '../../donnees/schema.ts';
import { palette } from '../../design/jetons.ts';
import { el, surToucher } from '../commun.ts';
import { fondVisage } from '../fiche/mots.ts';
import { motEtat, motQui } from '../../metier/index.ts';
import { ajusterEtat, ajusterTitre, carte, deux, etatParole, type Densite } from '../index/carte.ts';
import { encart, glissiere } from '../liste/ecran-liste.ts';

const TXT = {
  tenues: 'tenues',
  enCours: 'en cours',
  tenuEnsemble: 'Tenu ensemble',
  partages: 'Ce que tu partages avec ',
  rien: 'Rien entre vous pour l’instant.',
  planter: '+ Planter un Promi',
  lancer: '+ Lancer un Chiche',
} as const;

/** les cartes : celles de l'Index, deux par rangée (A3 : à la largeur de l'écran) ; le titre part de 20, l'état est en 10 (le prototype : la carte
 *  hors de `#device`) */
const personne = (largeur: number): Densite => ({ ...deux(largeur), FTI: 20, FET: 10 });
/** le Noyau du §2.9 : 58 pt, l'arc de 6, le visage au centre à 36 */
const NY = { D: 58, LW: 6 } as const;
/** « l'état n'est plus écrit — le trait le dit » : ces mots sortent de la ligne du bas (le temps et le Cercle restent) */
const MOTS_ETAT = /^(TENUE?S?|TENU À DEUX|EN COURS|LANCÉ|RELEVÉ|À RELEVER|GARDÉ DE CÔTÉ|DEMANDÉ|EN ATTENTE)$/i;

export interface Personne {
  ouvrir(nom: string): void;
  fermer(): void;
  ouvert(): boolean;
}

/** les paroles partagées : celles où la personne est « à qui », « de qui » OU « avec » (le compagnon d'un Chiche) */
function paroles(L: readonly Parole[], nom: string): Parole[] {
  return L.filter((p) => !p.draft && (p.who === nom || p.from === nom || p.suite?.['avec'] === nom));
}

export function monterPersonne(facade: Facade, magasin: Magasin, nav: Navigation): Personne {
  const dv = facade.appareil();
  const sh = el('div', { id: 'personSheet', class: 'ecran-liste ecran-personne', role: 'dialog' });
  sh.hidden = true;
  const { plateau, titre, croix, poserEncart } = encart('');
  titre.id = 'psName';
  const col = el('div', { class: 'ps-col', 'data-defile': '1', 'data-glisse': '' });
  const pile = el('div', { class: 'ps-pile' });
  col.appendChild(pile);
  sh.append(col, plateau);
  dv.appendChild(sh);
  let nom = '';
  let sig = '';

  /** le Noyau : la piste, les arcs d'état à bout franc (un jour de 2 entre deux), le filet crème de chaque arc en sombre ; le visage au centre */
  function noyau(L: readonly Parole[]): HTMLElement {
    const w = el('div', { class: 'ps-ny' });
    const r = (NY.D - NY.LW) / 2;
    const C = 2 * Math.PI * r;
    const n = L.length;
    const parts = n
      ? [L.filter((p) => p.status === 'tenu').length / n, L.filter((p) => p.status === 'encours').length / n]
      : [0, 0];
    const nb = parts.filter((v) => v > 0).length;
    const clair = dv.classList.contains('light');
    const R = r + NY.LW / 2 - 0.5;
    const k = R / r;
    let s = `<svg viewBox="0 0 58 58" width="58" height="58"><circle cx="29" cy="29" r="${String(r)}" fill="none" stroke="${clair ? palette.creme87 : palette.brun19}" stroke-width="${String(NY.LW)}"/>`;
    let a = 0;
    const cols = [palette.menthe11, palette.mauve12];
    parts.forEach((f, i) => {
      if (f <= 0) return;
      const l = f * C - (nb > 1 ? 2 : 0);
      s += `<circle class="ps-arc" data-part="${String(i)}" cx="29" cy="29" r="${String(r)}" fill="none" stroke="${cols[i]!}" stroke-width="${String(NY.LW)}" stroke-dasharray="${l.toFixed(2)} ${(C - l).toFixed(2)}" stroke-dashoffset="${(-a).toFixed(2)}" transform="rotate(-90 29 29)"/>`;
      // v18 : un filet crème suit le bord extérieur de chaque arc posé sur le sombre (1 px), s'interrompt dans les jours
      if (!clair)
        s += `<circle cx="29" cy="29" r="${R.toFixed(3)}" stroke-dasharray="${(l * k).toFixed(3)} ${(2 * Math.PI * R - l * k).toFixed(3)}" stroke-dashoffset="${(-a * k).toFixed(3)}" transform="rotate(-90 29 29)" fill="none" stroke="${palette.creme95}" stroke-width="1" stroke-linecap="butt"/>`;
      a += f * C;
    });
    w.innerHTML = s + '</svg>';
    const v = el('div', { class: 'ps-vis' });
    v.style.background = fondVisage(nom);
    w.appendChild(v);
    return w;
  }

  function legende(): HTMLElement {
    const g = el('div', { class: 'ps-lg' });
    for (const [mot, c] of [
      [TXT.tenues, palette.menthe11],
      [TXT.enCours, palette.mauve12],
    ] as const) {
      const s = el('span');
      const i = el('i');
      i.style.background = c;
      s.append(i, document.createTextNode(mot));
      g.appendChild(s);
    }
    return g;
  }

  const pose = (e: HTMLElement, x: number, y: number): HTMLElement => {
    e.style.left = `${String(x)}px`;
    e.style.top = `${String(y)}px`;
    pile.appendChild(e);
    return e;
  };

  function batir(force: boolean): void {
    const e = magasin.etat();
    const L = paroles(e.paroles, nom);
    const T = L.filter((p) => p.status === 'tenu');
    const s = JSON.stringify([nom, L, facade.mondeCourant(), dv.classList.contains('light')]);
    if (!force && s === sig) return;
    sig = s;
    titre.textContent = nom;
    // A3 : la largeur de l'écran (390 : les cotes du prototype)
    const W = col.clientWidth || 390;
    const PERSONNE = personne(W);
    pile.replaceChildren();
    pose(noyau(L), 24, 124);
    if (L.length) pose(legende(), 100, 145);
    let y = 124 + 58 + 32;
    if (T.length) {
      const h = el('div', { class: 'ps-h' });
      h.textContent = TXT.tenuEnsemble;
      pose(h, 24, y);
      y += 30;
      // les dalles tenues, trois par rangée (117 de pas, 101 de rangée) ; chacune rendue à la taille de sa boîte (105 × 56), posée 1:1
      const dp = Math.min(2, window.devicePixelRatio || 1);
      T.forEach((p, i) => {
        const c = el('div', { class: 'ps-c', 'data-pid': String(p.id), role: 'button' });
        const bx = el('div', { class: 'ps-bx' });
        const src = facade.rendreDalle(p.id, 105 * dp, 56 * dp);
        if (src) {
          const cv = src.cv;
          cv.style.width = `${String(cv.width / dp)}px`;
          cv.style.height = `${String(cv.height / dp)}px`;
          bx.appendChild(cv);
        }
        const t = el('span');
        t.textContent = p.title || '';
        c.append(bx, t);
        surToucher(c, () => {
          nav.ouvrir('fiche', p.id);
        });
        pose(c, 24 + (i % 3) * ((117 * (W - 48)) / 342), y + Math.floor(i / 3) * 101);
      });
      y += Math.ceil(T.length / 3) * 101 - 12 + 32;
    }
    if (!L.length) {
      // E4 (v178c) : une ligne, sans seconde ligne — les deux boutons restent
      const v = el('div', { class: 'e4-l1 e4-ps' });
      v.textContent = TXT.rien;
      pose(v, 24, y);
      y += 30 + 28;
    } else {
      const h = el('div', { class: 'ps-h' });
      h.textContent = TXT.partages + nom;
      pose(h, 24, y);
      y += 30;
      const box = pose(el('div', { id: 'psCartes', class: 'ps-cartes' }), 0, y);
      const ingenu = facade.mondeCourant().p === 'signal';
      const clair = dv.classList.contains('light');
      let bas = 0;
      L.forEach((p, i) => {
        const tout = motEtat(p, magasin.aujourdhui());
        const et = tout
          .split(' · ')
          .map((x) => x.trim())
          .filter((x) => x && !MOTS_ETAT.test(x));
        if (p.nuee) et.push((e.cercles[p.nuee] || p.nuee).toUpperCase());
        const d = carte(
          PERSONNE,
          etatParole(p),
          { eb: motQui(p), titre: p.title || '', et: tout },
          {
            facade,
            p,
            ingenu,
            repeindre: () => {
              batir(true);
            },
          },
          { tenue: p.status === 'tenu', garde: false, clair },
        );
        d.dataset['pid'] = String(p.id);
        // la ligne du bas, une fois le titre ajusté (le prototype l'ajuste à la construction, l'état encore écrit, puis le retire)
        d.dataset['et'] = et.join(' · ');
        d.setAttribute('role', 'button');
        d.style.left = `${String(PERSONNE.GX[i % PERSONNE.GX.length])}px`;
        const top = Math.floor(i / PERSONNE.GX.length) * PERSONNE.PAS;
        d.style.top = `${String(top)}px`;
        surToucher(d, () => {
          nav.ouvrir('fiche', p.id);
        });
        box.appendChild(d);
        bas = Math.max(bas, top + PERSONNE.CH);
      });
      box.style.height = `${String(bas)}px`;
      y += bas;
    }
    // entiers à l'ouverture, ou franchement sous le pli
    let bt = Math.max(760, y + 28);
    if (bt + 62 > 822 && bt < 844) bt = 844;
    // les deux gestes : 167 × 62 à 390, 8 pt entre eux
    const lb = (W - 56) / 2;
    for (const [mot, chiche, x] of [
      [TXT.planter, false, 24],
      [TXT.lancer, true, 32 + lb],
    ] as const) {
      const b = el('div', { class: 'ps-bt', role: 'button', 'data-geste': chiche ? 'chiche' : 'promi' });
      b.textContent = mot;
      b.style.width = `${String(lb)}px`;
      const qui = nom;
      surToucher(b, () => {
        nav.ouvrir('pagePlus', `${chiche ? 'chiche' : 'promi'}:qui:${qui}`);
      });
      pose(b, x, bt);
    }
    pile.style.height = `${String(bt + 62 + 22)}px`;
    ajuster();
  }

  function ajuster(): void {
    if (sh.hidden) return;
    for (const d of pile.querySelectorAll<HTMLElement>('.s4-carte')) {
      const et = d.querySelector<HTMLElement>('.s4-et');
      if (!et) continue;
      if (et.dataset['tout'] != null) et.textContent = et.dataset['tout'];
      else et.dataset['tout'] = et.textContent;
      ajusterEtat(d);
      ajusterTitre(d, 20);
      et.textContent = d.dataset['et'] ?? '';
    }
  }

  const G = glissiere(sh, dv, false, () => {
    batir(true);
    poserEncart();
    ajuster();
  });
  surToucher(croix, () => {
    G.fermer();
  });
  void document.fonts.ready.then(() => {
    poserEncart();
    ajuster();
  });
  magasin.abonner(() => {
    if (!sh.hidden) batir(false);
  });

  const ouvrir = (n: string): void => {
    if (!n) return;
    nom = n;
    col.scrollTop = 0;
    G.ouvrir();
  };
  // UN NOM QUI SE TOUCHE mène à la fiche de la personne, jamais pour soi (`data-moi`) — la phrase d'une fiche, ses Noyaux, un mot (le prototype :
  // lot-V146-NOMS, en capture sur tout le document ; une fiche ne produit pas toujours de `click` au doigt : on lit le geste, le clic qui suit est avalé)
  let g: { s: HTMLElement; x: number; y: number; t: number } | null = null;
  let fait = -1e9;
  const lien = (t: EventTarget | null): HTMLElement | null => {
    const s = t instanceof Element ? t.closest<HTMLElement>('.nom-lien[data-nom]') : null;
    return s && !s.dataset['moi'] ? s : null;
  };
  dv.addEventListener(
    'pointerdown',
    (ev) => {
      const s = lien(ev.target);
      g = s ? { s, x: ev.clientX, y: ev.clientY, t: ev.timeStamp } : null;
      if (g) ev.stopPropagation();
    },
    true,
  );
  dv.addEventListener(
    'pointerup',
    (ev) => {
      const x = g;
      g = null;
      if (!x || Math.abs(ev.clientX - x.x) > 10 || Math.abs(ev.clientY - x.y) > 10 || ev.timeStamp - x.t > 700) return;
      ev.stopPropagation();
      ev.preventDefault();
      fait = ev.timeStamp;
      nav.ouvrir('personne', x.s.dataset['nom']);
    },
    true,
  );
  dv.addEventListener(
    'click',
    (ev) => {
      const s = lien(ev.target);
      if (!s) return;
      ev.stopPropagation();
      ev.preventDefault();
      if (ev.timeStamp - fait > 600) nav.ouvrir('personne', s.dataset['nom']);
    },
    true,
  );

  nav.poser('personne', (arg) => {
    if (typeof arg === 'string') ouvrir(arg);
  });
  return { ouvrir, fermer: G.fermer, ouvert: G.ouvert };
}
