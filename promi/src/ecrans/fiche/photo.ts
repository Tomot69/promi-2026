/**
 * LA PHOTO D'UNE FICHE (lot 3b-3 ; le prototype : `_photoMenu` de lot-V117-PHOTO-MENU, ses entrées de lot-V132-DESSIN, `_photoPeint` de
 * lot-PHOTO, `_origineBande` de lot-V118-ORIGINE).
 *
 * LE MENU DU BOUTON PHOTO (compact : 33 pt, 4 pt entre deux, à gauche du bouton, son bas sur le bas du bouton, jamais plus haut que 106) :
 * « Dessiner » en tête (le mode dessin, lot 3b-5), « Importer une photo » (le sélecteur du téléphone,
 * ouvert DANS le geste), « La dalle d'origine » / « La dalle du Studio » (une parole qui porte son monde de plantation), « Retirer la photo »,
 * « Retirer le dessin ». Il paraît et part en flaques (C-271 ; le prototype le posait d'un coup) ; un toucher ailleurs le referme.
 *
 * LA PEINTURE : la photo REMPLACE la dalle — la même boîte, en couverture (recadrée au centre), bornée par l'onde ; cadrée au doigt (C-085,
 * C-098 : `photoCadre`), elle se dessine entière, à z fois sa taille de couverture, décalée, tournée. La dalle d'origine : peinte dans le monde
 * de sa plantation, sa couleur gardée sauf ton sur ton face au champ (ΔE < 15 : la rampe de Q30).
 */
import type { Magasin } from '../../etat/magasin.ts';
import type { MondeDalle, Parole } from '../../donnees/schema.ts';
import { masqueFlaques } from '../../animation/flaques/passage.ts';
import { el, surToucher } from '../commun.ts';
import { imagePhotoCache } from '../photo/peinture.ts';
import { TEXTES_PAGE_PLUS as TP } from '../../textes/page-plus.ts';

const TXT = { origine: 'La dalle d’origine', studio: 'La dalle du Studio' } as const;
/** le bouton, une photo posée : « revenir à la dalle » — le signe du retour, pas un mot (lot-PHOTO, `poseBouton`) */
export const SVG_RETOUR =
  '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M8 5 L4 9 L8 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M4 9 h9 a6 6 0 0 1 6 6 v1" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';
const reduit = (): boolean => matchMedia('(prefers-reduced-motion: reduce)').matches;

/** ce que la bande haute porte : la photo (son adresse, son cadrage), ou la dalle — du Studio, ou d'origine */
export function photoDe(p: Parole): string | null {
  const v = p.suite?.['photo'];
  return typeof v === 'string' && v ? v : null;
}
export function mondeOrigine(p: Parole): MondeDalle | null {
  return p.suite?.['dalleOrigine'] === true && p.monde?.m ? p.monde : null;
}

export interface MenuPhoto {
  ouvert(): boolean;
  fermer(anime?: boolean): void;
}

export function monterMenuPhoto(o: {
  hote: HTMLElement;
  bouton: HTMLElement;
  magasin: Magasin;
  parole: () => Parole | null;
  /** la photo ou la dalle vient de changer : la bande se repeint (la photo neuve paraît en flaques) */
  repeindre: (photoNeuve: boolean) => void;
  /** le dessin (lot 3b-5) : l'ouvrir ; la parole en porte-t-elle un (posé ou commencé) ; le retirer */
  dessiner: () => void;
  aDessin: (p: Parole) => boolean;
  retirerDessin: () => void;
  /** la fiche d'un Cercle ouverte (C-042, v132) : « un Cercle ne porte pas de photo : il dessine » — le menu n'a que « Dessiner » (et
   *  « Retirer le dessin ») ; son dessin posé ou commencé */
  cercle?: () => boolean;
  aDessinCercle?: () => boolean;
}): MenuPhoto {
  const { hote, bouton, magasin } = o;
  const entree = el('input', { type: 'file', accept: 'image/*', class: 'fi-photo-in', 'aria-hidden': 'true' });
  entree.style.display = 'none';
  hote.appendChild(entree);
  let menu: HTMLElement | null = null;

  function fermer(anime = true): void {
    const m = menu;
    if (!m) return;
    menu = null;
    if (!anime || reduit()) m.remove();
    else {
      m.style.pointerEvents = 'none';
      masqueFlaques(m, {
        mode: 'couvre',
        duree: 300,
        fin: () => {
          m.remove();
        },
      });
    }
  }
  function ouvrir(): void {
    const p = o.parole();
    const c = !p && !!o.cercle?.();
    if (!p && !c) return;
    if (menu) {
      fermer();
      return;
    }
    const m = el('div', { class: 'ph-photo-menu dz-compact', role: 'menu' });
    const item = (texte: string, f: (() => void) | null, attr?: string): void => {
      const b = el('button', { type: 'button', role: 'menuitem' });
      if (attr) b.setAttribute(attr, '1');
      b.textContent = texte;
      if (!f) b.setAttribute('aria-disabled', 'true');
      // un vrai clic (le toucher en fabrique un) : le sélecteur de fichiers ne s'ouvre que dans le geste (iOS)
      b.addEventListener('click', (ev) => {
        ev.stopPropagation();
        if (!f) return;
        f();
      });
      m.appendChild(b);
    };
    // le dessin, en tête (v132)
    item(
      TP.menuPhoto.dessiner,
      () => {
        fermer(false);
        o.dessiner();
      },
      'data-dessiner',
    );
    if (p)
      item(TP.menuPhoto.importer, () => {
        entree.click();
        fermer();
      });
    if (p?.monde?.m)
      item(mondeOrigine(p) ? TXT.studio : TXT.origine, () => {
        fermer();
        magasin.photo(p.id, { origine: !mondeOrigine(p) });
        o.repeindre(false);
      });
    if (p && photoDe(p))
      item(TP.menuPhoto.retirer, () => {
        fermer();
        magasin.photo(p.id, { photo: null });
        o.repeindre(false);
      });
    // un dessin posé ou commencé : « Retirer le dessin » (le prototype, `retire`), en dernier
    if (p ? o.aDessin(p) : !!o.aDessinCercle?.())
      item(TP.menuPhoto.retirerDessin, () => {
        fermer();
        o.retirerDessin();
      });
    hote.appendChild(m);
    // la place : à GAUCHE du bouton, son bas aligné sur le bas du bouton (34), jamais plus haut que 106 (le plateau finit à 100)
    const hm = m.offsetHeight;
    m.style.top = `${String(Math.max(106, Math.round(bouton.offsetTop + 34 - hm)))}px`;
    m.style.width = `${String(Math.max(120, bouton.offsetLeft - 8 - 24))}px`;
    menu = m;
    if (!reduit()) masqueFlaques(m, { mode: 'ouvre', duree: 300 });
  }

  surToucher(bouton, () => {
    ouvrir();
  });
  document.addEventListener(
    'pointerdown',
    (ev) => {
      const t = ev.target as Node;
      if (menu && !menu.contains(t) && !bouton.contains(t)) fermer();
    },
    true,
  );
  entree.addEventListener('change', () => {
    const f = entree.files?.[0];
    entree.value = '';
    const p = o.parole();
    if (!f || !p) return;
    const lu = new FileReader();
    lu.onload = () => {
      const src = typeof lu.result === 'string' ? lu.result : null;
      if (!src || o.parole()?.id !== p.id) return;
      const im = new Image();
      im.onload = () => {
        imagePhotoCache(src, im);
        // v140 (C-085) : la photo REMPLACE le dessin — il n'en reste rien
        magasin.photo(p.id, { photo: src });
        o.repeindre(true);
      };
      im.src = src;
    };
    lu.readAsDataURL(f);
  });

  return { ouvert: () => !!menu, fermer };
}
