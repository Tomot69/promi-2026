/**
 * L'INDEX (SPEC-ECRANS §8 ; le prototype : `#indexSheet` et lot-S4, l'encart de lot-V210-ENCART, C-301 : « l'Index est le Fil ») — un écran
 * plein qui monte du bas (la feuille : 0,4 s, `cubic-bezier(.32,.72,0,1)`), par-dessus l'accueil :
 *  · l'encart du haut (24 / 40, 342 × 60) : « INDEX » et le X ;
 *  · la recherche (24 / 116, 278 × 52) et le bouton ⇅ (314 / 116, 52 × 52) ;
 *  · la grille (dès 204) : deux cartes par ligne, 165 × 198, de 210 en 210 — la carte (carte.ts) porte sa nature, sa dalle, son trait, ses mots.
 * Une carte touchée ouvre SA fiche, par-dessus l'Index ; le X de la fiche ramène à l'Index tel qu'il était (C-193, C-250).
 */
import './index.css';
import type { Facade } from '../../moteur/facade.ts';
import type { Magasin } from '../../etat/magasin.ts';
import type { Navigation } from '../../navigation/navigation.ts';
import type { Etat, Parole } from '../../donnees/schema.ts';
import { el, poserCroix, centrerTitre, surToucher } from '../commun.ts';
import { horloge } from '../../animation/horloge.ts';
import { entreesIndex, motEtat, motQui, type Entree, type Filtre, type Tri } from '../../metier/index.ts';
import { ajusterEtat, ajusterTitre, carte, DEUX, etatCercle, etatParole } from './carte.ts';

const TXT = {
  titre: 'Index',
  fermer: 'Fermer',
  fermerGlyphe: 'X',
  rechercher: 'Rechercher',
  trier: 'Trier et filtrer',
  tri: '⇅',
  trier_: 'TRIER',
  filtrer: 'NE MONTRER QUE',
} as const;
const TRIS: ReadonlyArray<[Tri, string]> = [
  ['recent', 'Récents'],
  ['personne', 'Par personne'],
  ['nuee', 'Par Cercle'],
];
const FILTRES: ReadonlyArray<[Filtre, string]> = [
  ['tous', 'Tout'],
  ['suspens', 'En suspens'],
  ['promi', 'Promi'],
  ['nuees', 'Cercles'],
  ['brouillons', 'Gardés de côté'],
  ['demandes', 'Demandes'],
];

export interface Index {
  ouvrir(): void;
  fermer(): void;
  ouvert(): boolean;
}

export function monterIndex(facade: Facade, magasin: Magasin, nav: Navigation): Index {
  const dv = facade.appareil();
  const sh = el('div', { id: 'indexSheet', class: 'ix', role: 'dialog' });
  sh.hidden = true;
  const plateau = el('div', { class: 'enh' });
  const titre = el('h2', { class: 'scr-ti enh-t' });
  titre.textContent = TXT.titre;
  const croix = el('div', { class: 'closeb', role: 'button', 'aria-label': TXT.fermer, 'data-close': '' });
  const croixG = el('span', { class: 'cb-mot' });
  croixG.textContent = TXT.fermerGlyphe;
  croix.appendChild(croixG);
  plateau.append(titre, croix);
  const barre = el('div', { class: 'ix-bar' });
  const srch = el('div', { class: 'ix-srch' });
  const champ = el('input', {
    id: 'ixSearch',
    class: 'ix-search',
    placeholder: TXT.rechercher,
    autocomplete: 'off',
    'aria-label': TXT.rechercher,
  });
  srch.appendChild(champ);
  const tri_ = el('button', { type: 'button', id: 'ixTriBtn', class: 'ix-tri', 'aria-label': TXT.trier });
  tri_.textContent = TXT.tri;
  barre.append(srch, tri_);
  const liste = el('div', { id: 'indexList' });
  const grille = el('div', { class: 's4-grille' });
  liste.appendChild(grille);
  // le menu ⇅ (lot-S2 de l'Index : un bouton, deux groupes — les catégories sont des FILTRES, pas des sections) ; il se pose par-dessus la grille
  const menu = el('div', { id: 'ixMenu', class: 'ix-menu' });
  const panneau = el('div', { class: 'ix-menu-p' });
  menu.appendChild(panneau);
  const option = (mot: string, attr: 'tri' | 'filt', val: string): HTMLElement => {
    const o = el('div', { class: 'ix-mi', role: 'button', [`data-${attr}`]: val });
    o.textContent = mot;
    o.appendChild(el('i', { 'aria-hidden': 'true' }));
    return o;
  };
  const groupe = (mot: string): HTMLElement => {
    const g = el('div', { class: 'ix-mg' });
    g.textContent = mot;
    return g;
  };
  panneau.append(
    groupe(TXT.trier_),
    ...TRIS.map(([v, m]) => option(m, 'tri', v)),
    groupe(TXT.filtrer),
    ...FILTRES.map(([v, m]) => option(m, 'filt', v)),
  );
  sh.append(plateau, barre, liste, menu);
  dv.appendChild(sh);

  let q = '';
  let tri: Tri = 'recent';
  let filtre: Filtre = 'tous';
  function poserMenu(): void {
    for (const o of panneau.querySelectorAll<HTMLElement>('.ix-mi'))
      o.classList.toggle('on', o.dataset['tri'] ? o.dataset['tri'] === tri : o.dataset['filt'] === filtre);
  }
  poserMenu();
  /** la signature de ce que la grille montre : elle ne se rebâtit que si elle change (C-049) */
  let sig = '';

  /** les paroles plantées d'un Cercle, dans l'ordre de l'état */
  const duCercle = (e: Readonly<Etat>, k: string): Parole[] => e.paroles.filter((q) => q.nuee === k && !q.draft);

  function textes(e: Readonly<Etat>, x: Entree): { eb: string; titre: string; et: string } {
    if (x.kind === 'nuee') {
      const lp = duCercle(e, x.k);
      const mem = e.membres[x.k] ?? [];
      const nt = lp.filter((q) => q.status === 'tenu').length;
      return {
        // « avec +4 » (le mot du moodboard) ; sans membre, celui de l'app (« perso ») ; « TENU » s'accorde (cadre 72, `promi-nuee-toile` cadre 10)
        eb: mem.length ? `avec +${String(mem.length)}` : 'perso',
        titre: e.cercles[x.k] || x.k,
        // Q213 : un Cercle vide reste un Cercle (un contenant) — « AUCUNE PAROLE »
        et: lp.length ? `${String(lp.length)} PROMI · ${String(nt)} TENU${nt > 1 ? 'S' : ''}` : 'AUCUNE PAROLE',
      };
    }
    return { eb: motQui(x.p), titre: x.p.title || '', et: motEtat(x.p, new Date()) };
  }

  function batir(force = false): void {
    const e = magasin.etat();
    const ent = entreesIndex(e, q, filtre, tri, e.utilisateur.prenom ?? 'Moi');
    const ingenu = facade.mondeCourant().p === 'signal';
    const clair = dv.classList.contains('light');
    const s = JSON.stringify([
      ent.map((x) => (x.kind === 'nuee' ? [x.k, e.cercles[x.k], e.membres[x.k], duCercle(e, x.k)] : x.p)),
      ingenu,
      clair,
      facade.mondeCourant(),
    ]);
    if (!force && s === sig) return;
    sig = s;
    const D = DEUX;
    grille.replaceChildren();
    grille.style.height = `${String(Math.ceil(ent.length / D.GX.length) * D.PAS + 40)}px`;
    const repeindre = (): void => {
      batir(true);
    };
    ent.forEach((x, i) => {
      const t = textes(e, x);
      let d: HTMLElement;
      if (x.kind === 'nuee') {
        const lp = duCercle(e, x.k);
        d = carte(
          D,
          etatCercle(lp.map((q) => q.id)),
          t,
          { facade, p: lp.at(-1) ?? null, ingenu, repeindre },
          {
            tenue: false,
            garde: false,
            clair,
          },
        );
        d.dataset['nk'] = x.k;
        d.dataset['etat'] = 'nuee';
        const k = x.k;
        surToucher(d, () => {
          nav.ouvrir('cercle', k);
        });
      } else {
        const p = x.p;
        d = carte(
          D,
          etatParole(p),
          t,
          { facade, p, ingenu, repeindre },
          {
            tenue: /^TENU/.test(t.et),
            garde: !!p.draft,
            clair,
          },
        );
        d.dataset['pid'] = String(p.id);
        d.dataset['etat'] = p.draft ? 'garde' : p.status === 'tenu' ? 'tenue' : p.chiche ? 'lance' : 'encours';
        surToucher(d, () => {
          nav.ouvrir(p.draft ? 'pagePlus' : 'fiche', p.id);
        });
      }
      d.style.left = `${String(D.GX[i % D.GX.length])}px`;
      d.style.top = `${String(Math.floor(i / D.GX.length) * D.PAS)}px`;
      d.setAttribute('role', 'button');
      grille.appendChild(d);
    });
    ajuster();
  }

  function ajuster(): void {
    if (sh.hidden) return;
    for (const d of grille.querySelectorAll<HTMLElement>('.s4-carte')) {
      ajusterEtat(d);
      ajusterTitre(d, DEUX.FTI);
    }
  }

  function poserEncart(): void {
    centrerTitre(plateau, titre);
    poserCroix(croix, croixG, titre);
  }

  let finFermeture: number | null = null;
  let finOuverture: number | null = null;
  function ouvrir(): void {
    if (finFermeture != null) horloge().annuleMinuteur(finFermeture);
    finFermeture = null;
    sh.classList.add('ix-bas');
    sh.hidden = false;
    batir(true);
    poserEncart();
    ajuster();
    sh.getBoundingClientRect();
    sh.classList.remove('ix-bas');
    finOuverture = horloge().minuteur(() => {
      finOuverture = null;
      sh.classList.add('couvre');
      dv.classList.add('couvert');
    }, 420);
  }
  function fermer(): void {
    if (sh.hidden || sh.classList.contains('ix-bas')) return;
    if (finOuverture != null) horloge().annuleMinuteur(finOuverture);
    finOuverture = null;
    sh.classList.remove('couvre');
    dv.classList.remove('couvert');
    sh.classList.add('ix-bas');
    finFermeture = horloge().minuteur(() => {
      finFermeture = null;
      sh.hidden = true;
    }, 420);
  }

  surToucher(croix, () => {
    fermer();
  });
  // ⇅ ouvre le menu ; un choix trie (ou filtre), puis le menu se referme ; un toucher dans le panneau, hors d'un choix, ne le referme pas (Q578) ;
  // ailleurs, il se referme
  surToucher(tri_, () => {
    menu.classList.add('on');
    tri_.classList.add('on');
  });
  surToucher(menu, (ev) => {
    const t = ev.target instanceof Element ? ev.target : null;
    const o = t?.closest<HTMLElement>('.ix-mi');
    if (o) {
      if (o.dataset['tri']) tri = o.dataset['tri'] as Tri;
      if (o.dataset['filt']) filtre = o.dataset['filt'] as Filtre;
      poserMenu();
      batir();
    } else if (t?.closest('.ix-menu-p')) return;
    menu.classList.remove('on');
    tri_.classList.remove('on');
  });
  champ.addEventListener('input', () => {
    q = champ.value;
    batir();
  });
  void document.fonts.ready.then(() => {
    poserEncart();
    ajuster();
  });
  // C-049 : une seule source de vérité — planter, tenir, retirer : la grille ouverte suit
  magasin.abonner(() => {
    if (!sh.hidden) batir();
  });
  nav.poser('index', () => {
    ouvrir();
  });

  return {
    ouvrir,
    fermer,
    ouvert: () => !sh.hidden && !sh.classList.contains('ix-bas'),
  };
}
