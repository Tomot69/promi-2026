/**
 * PEAUFINER — LES BRIQUES COMMUNES (lot 3b ; le prototype : lot-S2, `_s2Briques` — `reg`, `emprunte`, la tête, les zones, le bloc de Ma Parole !).
 * La page + et la fiche bâtissent leur Peaufiner avec les MÊMES briques (une seule grammaire, §5) : la tête (le titre, le X), la rangée (libellé à
 * gauche, valeur à droite, pilule de 64), la rangée qui se déplie (`s2-ouv`, ses choix dessous ; un choix la replie), la NOTE, les PIÈCES JOINTES,
 * les murs de Ma Parole ! (flous, sans prise), et la pose : une valeur qui a changé se détrace puis se trace (C-279), jamais d'un coup.
 * Ce qui est propre à un écran (ses rangées, leurs choix, ce qu'un choix écrit) reste dans l'écran.
 */
import './peaufiner.css';
import { changerTexte } from '../../animation/trace/trace.ts';
import { champSansEmoji } from '../../metier/emoji.ts';
import { el, poserCroix, surToucher } from '../commun.ts';

export interface Peauf {
  /** la rangée dépliée (son libellé) : elle le reste quand Peaufiner se rebâtit après un choix fait ailleurs */
  ouverte: string | null;
  rang: (lab: string, val: string, cls?: string) => HTMLElement;
  /** une rangée qui déplie ses choix au toucher (le prototype : `s2-ouv`, `.s2-ctl`) ; un choix la replie */
  deplie: (r: HTMLElement, choix: () => HTMLElement) => void;
  /** la tête : le titre et le X (posé face au titre, lot-V157-CROIX) */
  tete: (titre: string, glyphe: string, etiquette: string, fermer: () => void) => HTMLElement;
  /** la NOTE : un champ (sans emoji), sa ligne de visibilité dessous */
  note: (o: {
    lab: string;
    vide: string;
    vis: string;
    valeur: string;
    id?: string;
    change: (v: string) => void;
  }) => HTMLElement;
  /** les PIÈCES JOINTES : le sélecteur de fichiers s'ouvre DANS le geste (le clic du doigt) */
  pieces: (o: { lab: string; val: string; vis: string; ajoute: (noms: string[]) => void }) => HTMLElement;
  /** les réglages de Ma Parole ! : des MURS, flous (4,8 px), sans prise (leur phrase : lot 8) */
  murs: (L: readonly (readonly [string, string])[]) => HTMLElement;
  /** pose la liste neuve dans le panneau ; une valeur qui a changé se détrace puis se trace (C-279) */
  poser: (liste: HTMLElement) => void;
  /** le X face au titre (à reposer quand le panneau est montré) */
  croix: () => void;
}

export function creerPeauf(hote: HTMLElement): Peauf {
  const pf: Peauf = {
    ouverte: null,
    rang(lab, val, cls = '') {
      const r = el('div', { class: 's2-reg' + cls });
      const l = el('div', { class: 's2-lab' });
      l.textContent = lab;
      const v = el('div', { class: 's2-val' });
      v.textContent = val;
      r.append(l, v);
      return r;
    },
    deplie(r, choix) {
      const lab = r.querySelector('.s2-lab')?.textContent ?? '';
      const ouvre = (): void => {
        const ctl = el('div', { class: 's2-ctl' });
        ctl.appendChild(choix());
        r.appendChild(ctl);
        r.classList.add('s2-ouv');
      };
      if (pf.ouverte === lab) ouvre();
      surToucher(r, (ev) => {
        if ((ev.target as Element).closest('.s2-ctl')) return;
        const etait = r.classList.contains('s2-ouv');
        for (const x of hote.querySelectorAll('.s2-reg.s2-ouv')) {
          x.classList.remove('s2-ouv');
          x.querySelector('.s2-ctl')?.remove();
        }
        pf.ouverte = etait ? null : lab;
        if (!etait) ouvre();
      });
    },
    tete(titre, glyphe, etiquette, fermer) {
      const tete = el('div', { class: 's2-tete' });
      const t = el('div', { class: 's2-titre' });
      t.textContent = titre;
      const x = el('div', { class: 's2-fermer', role: 'button', 'aria-label': etiquette });
      const xg = el('span', { class: 's2-x' });
      xg.textContent = glyphe;
      x.appendChild(xg);
      surToucher(x, () => {
        fermer();
      });
      tete.append(t, x);
      return tete;
    },
    note(o) {
      const zone = el('div', { class: 's2-reg s2-zone' });
      const zl = el('div', { class: 's2-lab' });
      zl.textContent = o.lab;
      const ta = el('textarea', {
        ...(o.id ? { id: o.id } : {}),
        class: 's2-txt',
        rows: '1',
        placeholder: o.vide,
        'aria-label': o.lab,
      });
      ta.value = o.valeur;
      champSansEmoji(ta);
      ta.addEventListener('input', () => {
        o.change(ta.value);
      });
      const zv = el('div', { class: 's2-vis' });
      zv.textContent = o.vis;
      zone.append(zl, ta, zv);
      return zone;
    },
    pieces(o) {
      const pj = el('div', { class: 's2-reg s2-vis2' });
      const ph = el('div', { class: 's2-haut' });
      const pl = el('div', { class: 's2-lab' });
      pl.textContent = o.lab;
      const pv = el('div', { class: 's2-val' });
      pv.textContent = o.val;
      ph.append(pl, pv);
      const fin = el('input', { type: 'file', multiple: '', class: 'ph-photo-in', 'aria-hidden': 'true' });
      fin.addEventListener('change', () => {
        o.ajoute([...(fin.files ?? [])].map((f) => f.name));
      });
      pj.appendChild(fin);
      // le sélecteur de fichiers s'ouvre DANS le geste (le clic du doigt), sinon le navigateur le refuse
      pj.addEventListener('click', () => {
        fin.click();
      });
      const pvis = el('div', { class: 's2-vis' });
      pvis.textContent = o.vis;
      pj.append(ph, pvis);
      return pj;
    },
    murs(L) {
      const murs = el('div', { class: 's2-cercle', 'data-mur': '', 'aria-hidden': 'true' });
      L.forEach(([lab, val], i) => murs.appendChild(pf.rang(lab, val, i === L.length - 1 ? ' s2-couleur' : '')));
      return murs;
    },
    poser(liste) {
      const avant = new Map<string, string>();
      for (const rg of hote.querySelectorAll('.s2-reg'))
        avant.set(rg.querySelector('.s2-lab')?.textContent ?? '', rg.querySelector('.s2-val')?.textContent ?? '');
      hote.replaceChildren(liste);
      pf.croix();
      for (const rg of liste.querySelectorAll('.s2-reg')) {
        const v = rg.querySelector<HTMLElement>('.s2-val');
        const a = avant.get(rg.querySelector('.s2-lab')?.textContent ?? '');
        if (v && a != null && a !== v.textContent) changerTexte(v, a, v.textContent ?? '');
      }
    },
    croix() {
      const x = hote.querySelector<HTMLElement>('.s2-fermer');
      const g = x?.querySelector<HTMLElement>('.s2-x');
      if (x && g) poserCroix(x, g, hote.querySelector<HTMLElement>('.s2-titre'));
    },
  };
  return pf;
}
