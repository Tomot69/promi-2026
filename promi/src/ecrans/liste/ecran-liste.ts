/**
 * L'ÉCRAN D'UNE LISTE — L'INDEX ET LE FIL (C-301, v210 : « l'Index est le Fil : même encart, même recherche, même ⇅, au pixel hors titre ») — une
 * brique, deux écrans. Un écran plein qui monte du bas (la feuille du prototype : 0,4 s, `cubic-bezier(.32,.72,0,1)`), par-dessus l'accueil :
 *  · l'encart du haut (24 / 40, 342 × 60) : le titre (et, au Fil, son compte) et le X ;
 *  · la recherche (24 / 116, 278 × 52) et le bouton ⇅ (314 / 116, 52 × 52) ; le menu ⇅ (un bouton, deux groupes — trier, ne montrer que : des
 *    FILTRES, pas des sections) — un choix trie ou filtre puis le menu se referme ; un toucher dans le panneau, hors d'un choix, ne le referme pas
 *    (Q578) ; ailleurs, il se referme ; sans voile ni ombre (C-185) ;
 *  · la liste (dès 204), que l'écran bâtit (`batir`).
 * L'écran se rebâtit quand l'état change (C-049, une seule source de vérité) ; une fiche s'ouvre par-dessus lui et son X le rend tel qu'il était.
 */
import './ecran-liste.css';
import type { Facade } from '../../moteur/facade.ts';
import type { Magasin } from '../../etat/magasin.ts';
import { el, poserCroix, centrerTitre, surToucher } from '../commun.ts';
import { horloge } from '../../animation/horloge.ts';

const TXT = {
  fermer: 'Fermer',
  fermerGlyphe: 'X',
  rechercher: 'Rechercher',
  trier: 'Trier et filtrer',
  tri: '⇅',
  groupeTri: 'TRIER',
  groupeFiltre: 'NE MONTRER QUE',
} as const;

export interface CfgEcranListe<T extends string, F extends string> {
  /** les ids du prototype : la feuille, la recherche, le ⇅, le menu, la liste */
  ids: { feuille: string; champ: string; tri: string; menu: string; liste: string };
  titre: string;
  /** le compte à côté du titre (le Fil : ce qui attend un geste) */
  compte?: { id: string };
  tris: ReadonlyArray<[T, string]>;
  filtres: ReadonlyArray<[F, string]>;
  tri: T;
  filtre: F;
  /** bâtir la liste (`force` : même si rien n'a changé) */
  batir(force: boolean): void;
  /** une fois l'écran posé (visible, polices prêtes) : les ajustements qui se lisent sur le rendu */
  ajuster(): void;
}

export interface EcranListe<T extends string, F extends string> {
  feuille: HTMLElement;
  champ: HTMLInputElement;
  liste: HTMLElement;
  grille: HTMLElement;
  compte: HTMLElement | null;
  q(): string;
  tri(): T;
  filtre(): F;
  /** la recherche vidée (la seconde ligne d'un écran vide) */
  viderRecherche(): void;
  /** le filtre « Tout » rendu (la seconde ligne d'un écran vide) */
  toutMontrer(): void;
  ouvrir(): void;
  fermer(): void;
  ouvert(): boolean;
}

export function monterEcranListe<T extends string, F extends string>(
  facade: Facade,
  magasin: Magasin,
  c: CfgEcranListe<T, F>,
): EcranListe<T, F> {
  const dv = facade.appareil();
  const sh = el('div', { id: c.ids.feuille, class: 'ecran-liste', role: 'dialog' });
  sh.hidden = true;
  const plateau = el('div', { class: 'enh' });
  const titre = el('h2', { class: 'scr-ti enh-t' });
  titre.textContent = c.titre;
  const compte = c.compte ? el('span', { id: c.compte.id, class: 'ix-count' }) : null;
  if (compte) titre.appendChild(compte);
  const croix = el('div', { class: 'closeb', role: 'button', 'aria-label': TXT.fermer, 'data-close': '' });
  const croixG = el('span', { class: 'cb-mot' });
  croixG.textContent = TXT.fermerGlyphe;
  croix.appendChild(croixG);
  plateau.append(titre, croix);
  const barre = el('div', { class: 'ix-bar' });
  const srch = el('div', { class: 'ix-srch' });
  const champ = el('input', {
    id: c.ids.champ,
    class: 'ix-search',
    placeholder: TXT.rechercher,
    autocomplete: 'off',
    'aria-label': TXT.rechercher,
  });
  srch.appendChild(champ);
  const btnTri = el('button', { type: 'button', id: c.ids.tri, class: 'ix-tri', 'aria-label': TXT.trier });
  btnTri.textContent = TXT.tri;
  barre.append(srch, btnTri);
  const liste = el('div', { id: c.ids.liste, class: 'el-liste' });
  const grille = el('div', { class: 's4-grille' });
  liste.appendChild(grille);
  const menu = el('div', { id: c.ids.menu, class: 'ix-menu' });
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
    groupe(TXT.groupeTri),
    ...c.tris.map(([v, m]) => option(m, 'tri', v)),
    groupe(TXT.groupeFiltre),
    ...c.filtres.map(([v, m]) => option(m, 'filt', v)),
  );
  sh.append(plateau, barre, liste, menu);
  dv.appendChild(sh);

  let q = '';
  let tri = c.tri;
  let filtre = c.filtre;
  function poserMenu(): void {
    for (const o of panneau.querySelectorAll<HTMLElement>('.ix-mi'))
      o.classList.toggle('on', o.dataset['tri'] ? o.dataset['tri'] === tri : o.dataset['filt'] === filtre);
  }
  poserMenu();

  function poserEncart(): void {
    centrerTitre(plateau, titre);
    poserCroix(croix, croixG, titre);
  }
  function ajuster(): void {
    if (!sh.hidden) c.ajuster();
  }

  let finFermeture: number | null = null;
  let finOuverture: number | null = null;
  function ouvrir(): void {
    if (finFermeture != null) horloge().annuleMinuteur(finFermeture);
    finFermeture = null;
    sh.classList.add('ix-bas');
    sh.hidden = false;
    c.batir(true);
    poserEncart();
    ajuster();
    // la feuille de style relue avant de retirer `ix-bas` : la transition part de l'état d'en bas
    sh.getBoundingClientRect();
    sh.classList.remove('ix-bas');
    // arrivé, il couvre l'appareil : l'accueil dessous ne se voit plus et ne prend plus le doigt (base.css, `.couvert`)
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
  surToucher(btnTri, () => {
    menu.classList.add('on');
    btnTri.classList.add('on');
  });
  surToucher(menu, (ev) => {
    const t = ev.target instanceof Element ? ev.target : null;
    const o = t?.closest<HTMLElement>('.ix-mi');
    if (o) {
      if (o.dataset['tri']) tri = o.dataset['tri'] as T;
      if (o.dataset['filt']) filtre = o.dataset['filt'] as F;
      poserMenu();
      c.batir(false);
    } else if (t?.closest('.ix-menu-p')) return;
    menu.classList.remove('on');
    btnTri.classList.remove('on');
  });
  champ.addEventListener('input', () => {
    q = champ.value;
    c.batir(false);
  });
  void document.fonts.ready.then(() => {
    poserEncart();
    ajuster();
  });
  // C-049 : une seule source de vérité — planter, tenir, retirer : la liste ouverte suit
  magasin.abonner(() => {
    if (!sh.hidden) c.batir(false);
  });

  return {
    feuille: sh,
    champ,
    liste,
    grille,
    compte,
    q: () => q,
    tri: () => tri,
    filtre: () => filtre,
    viderRecherche() {
      champ.value = '';
      q = '';
      c.batir(false);
    },
    toutMontrer() {
      filtre = c.filtres[0]![0];
      poserMenu();
      c.batir(false);
    },
    ouvrir,
    fermer,
    ouvert: () => !sh.hidden && !sh.classList.contains('ix-bas'),
  };
}

/** l'écran vide (E4, v178c, C-078) : deux lignes ; la seconde, seule touchable, mène à son action. Sans tracé (ces écrans n'en ont pas). */
export function ecranVide(l1: string, l2: string, act: () => void): HTMLElement {
  const v = el('div', { class: 'e4v' });
  const a = el('div', { class: 'e4-l1' });
  a.textContent = l1;
  const b = el('div', { class: 'e4-l2', role: 'button' });
  b.textContent = l2;
  surToucher(b, act);
  v.append(a, b);
  return v;
}
