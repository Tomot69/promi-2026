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

/** les pastilles d'AVANT (C-197) : demain · 1 sem. · 1 mois · une date… (le calendrier) · un jour (aucune échéance) */
const JOURS: readonly (number | null | 'date')[] = [1, 7, 30, 'date', null];

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
  /**
   * le choix de l'échéance, sous la rangée AVANT `r` (C-197) : une pastille choisie (`choisit`), ou une date du calendrier (`date` l'applique et
   * rend son mot, qui remplace la valeur de la rangée EN PLACE, détracé puis tracé) ; `replie` : le calendrier s'est refermé sur une date
   */
  echeance: (o: {
    r: HTMLElement;
    mots: readonly string[];
    on: number | null;
    dueISO: string | null;
    choisit: (jours: number | null, mot: string) => void;
    date: (iso: string, jours: number) => string;
    replie: () => void;
  }) => HTMLElement;
  /** les réglages de Ma Parole ! : des MURS, flous (4,8 px), sans prise (leur phrase : lot 8) */
  murs: (L: readonly (readonly [string, string])[], couleur?: string | null) => HTMLElement;
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
      const fin = el('input', { type: 'file', multiple: '', class: 's2-fichiers', 'aria-hidden': 'true' });
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
    echeance(o) {
      const lab = o.r.querySelector('.s2-lab')?.textContent ?? '';
      const ch = el('div', { class: 'chips', id: 'dueChips' });
      o.mots.forEach((mot, i) => {
        const d = JOURS[i];
        const c = el('div', { class: 'chip' + (o.on === i ? ' on' : ''), role: 'button' });
        c.textContent = mot;
        if (d === 'date') {
          // ⚑ 2b (Tom, sur l'iPhone : « le calendrier ne s'ouvre pas ») — LA CAUSE : le sélecteur était ouvert au lever du doigt
          // (`pointerup`), que la WebView d'iOS ne compte pas comme un geste : `showPicker()` y est refusé, et le repli `focus()` visait
          // un champ invisible qui ne prenait pas le doigt. Le vrai champ date COUVRE la pastille (invisible) : le doigt le touche
          // lui-même, et c'est iOS qui ouvre son calendrier. Ailleurs (un ordinateur), son clic l'ouvre (`showPicker`, dans le geste).
          const t0 = new Date();
          const di = el('input', {
            type: 'date',
            class: 'due-datein',
            'aria-label': mot,
            min: `${String(t0.getFullYear())}-${String(t0.getMonth() + 1).padStart(2, '0')}-${String(t0.getDate()).padStart(2, '0')}`,
          });
          if (o.dueISO) di.value = o.dueISO;
          c.appendChild(di);
          di.addEventListener('click', () => {
            try {
              di.showPicker();
            } catch {
              /* iOS l'ouvre lui-même (le doigt sur le champ) */
            }
          });
          // ⚑ L2 (Tom, 24 nov., le relevé de sa séance sur l'iPhone) : iOS envoie la date par `input` et `change` — la date du jour dès que son
          // calendrier s'ouvre, puis chaque jour touché —, parfois seulement à sa fermeture (`blur`) : elle s'applique sur les trois, dès qu'elle
          // diffère de la précédente. Elle change EN PLACE (détracé puis tracé), la pastille se coche ; Peaufiner n'est jamais rebâti calendrier
          // ouvert (un champ retiré de la page referme le calendrier d'iOS) : la rangée se replie à sa fermeture
          let iso = o.dueISO;
          const applique = (): void => {
            if (!di.value || di.value === iso) return;
            iso = di.value;
            const t = new Date();
            t.setHours(0, 0, 0, 0);
            const pk = new Date(di.value + 'T00:00:00');
            const jours = Math.max(0, Math.round((pk.getTime() - t.getTime()) / 86400000));
            const v = o.r.querySelector<HTMLElement>('.s2-val');
            const avant = v?.textContent ?? '';
            const neuf = o.date(di.value, jours);
            for (const x of ch.querySelectorAll('.chip')) x.classList.toggle('on', x === c);
            if (v) changerTexte(v, avant, neuf);
          };
          di.addEventListener('input', applique);
          di.addEventListener('change', applique);
          di.addEventListener('blur', () => {
            applique();
            if (iso && pf.ouverte === lab) o.replie();
          });
        }
        surToucher(c, () => {
          if (d === 'date' || d === undefined) return;
          o.choisit(d, mot);
        });
        ch.appendChild(c);
      });
      return ch;
    },
    murs(L, couleur) {
      const murs = el('div', { class: 's2-cercle', 'data-mur': '', 'aria-hidden': 'true' });
      L.forEach(([lab, val], i) => {
        const r = pf.rang(lab, val, i === L.length - 1 ? ' s2-couleur' : '');
        // LA COULEUR d'une parole plantée (lot-CERCLE-COULEUR, `_regCouleur`) : la pastille de la couleur de sa dalle, puis son code
        if (i === L.length - 1 && couleur) {
          const v = r.querySelector<HTMLElement>('.s2-val')!;
          const pas = el('span', { class: 'cc-pas' });
          pas.style.background = couleur;
          v.replaceChildren(pas, document.createTextNode(couleur));
        }
        murs.appendChild(r);
      });
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
