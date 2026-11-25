/**
 * LE FIL (SPEC-ECRANS §9 ; le prototype : `#feedView`, `buildFeed`, `_s4Fil` de lot-S4, v163b C-191, v181b C-245) — l'écran d'une liste
 * (ecran-liste.ts : le même encart, la même recherche, le même ⇅ que l'Index, C-301), qui glisse de la droite (`fil-cote` : 0,34 s), et ses
 * bandeaux (bandeau.ts) : un par événement, de 140 en 140 — la ligne de l'événement, le titre de la parole, son état et son heure. Le compte à
 * côté du titre : ce qui attend un geste de moi (v89, Q347). Un bandeau touché ouvre SA fiche, par-dessus le Fil ; le X la referme sur le Fil tel
 * qu'il était (C-250).
 */
import './fil.css';
import type { Facade } from '../../moteur/facade.ts';
import type { Magasin } from '../../etat/magasin.ts';
import type { Navigation } from '../../navigation/navigation.ts';
import type { Etat } from '../../donnees/schema.ts';
import { surToucher } from '../commun.ts';
import { NATTRAIT } from '../page-plus/trait.ts';
import { motEtat, motQui } from '../../metier/index.ts';
import {
  entreesFil,
  evenementSansTitre,
  filAttente,
  type EntreeFil,
  type FiltreFil,
  type TriFil,
} from '../../metier/fil.ts';
import { ajusterEtat, etatCercle, etatParole, type EtatCarte } from '../index/carte.ts';
import { ecranVide, monterEcranListe } from '../liste/ecran-liste.ts';
import { BANDEAU, bandeau, poserTitre, type TextesBandeau } from './bandeau.ts';

const TXT = {
  titre: 'Fil',
  revenirFil: 'Revenir à tout le Fil.',
  rienTri: 'Rien sous ce tri.',
  rienNeBouge: 'Rien ne bouge encore.',
  anime: 'Une parole donnée à quelqu’un, et le Fil s’anime.',
} as const;
const TRIS: ReadonlyArray<[TriFil, string]> = [
  ['recent', 'Récents'],
  ['personne', 'Par personne'],
  ['nuee', 'Par Cercle'],
];
const FILTRES: ReadonlyArray<[FiltreFil, string]> = [
  ['tous', 'Tout'],
  ['agir', 'Ce qui attend un geste'],
  ['tenues', 'Paroles tenues'],
  ['demandes', 'Demandes'],
  ['nuees', 'Cercles'],
  ['moi', 'Mes Promi'],
  ['proches', 'Mes proches'],
];

export interface Fil {
  ouvrir(): void;
  fermer(): void;
  ouvert(): boolean;
}

const estMoi = (v: unknown): boolean => {
  const s = typeof v === 'string' ? v.trim().toLowerCase() : '';
  return !s || s === 'moi';
};

export function monterFil(facade: Facade, magasin: Magasin, nav: Navigation): Fil {
  const E = monterEcranListe<TriFil, FiltreFil>(facade, magasin, {
    ids: { feuille: 'feedView', champ: 'fdSearch', tri: 'fdTriBtn', menu: 'fdMenu', liste: 'feedList' },
    titre: TXT.titre,
    compte: { id: 'fdCount' },
    entree: 'droite',
    tris: TRIS,
    filtres: FILTRES,
    tri: 'recent',
    filtre: 'tous',
    batir: (f) => {
      batir(f);
    },
    ajuster: () => {
      ajuster();
    },
  });
  const grille = E.grille;
  let sig = '';

  /** l'état, les mots et le visage d'un bandeau (`_s4Fil`) */
  function lire(e: Readonly<Etat>, x: EntreeFil): { etat: EtatCarte; t: TextesBandeau } {
    const quand = x.f.t ? ` · ${x.f.t.toUpperCase()}` : '';
    if (x.p) {
      const p = x.p;
      // la ligne de l'événement : son texte sans le titre entre guillemets (le titre est la ligne 2)
      const ev = evenementSansTitre(x.f.text || '') || motQui(p);
      // le visage suit l'événement (le premier du Fil sur cette parole), pas le Promi
      const premier = e.fil.find((z) => z.pid === p.id);
      const de = premier?.suite?.['from'] ?? p.from;
      return {
        etat: etatParole(p),
        t: { ev, titre: p.title || '', et: motEtat(p, null) + quand, vis: !estMoi(de) },
      };
    }
    if (x.nk) {
      const lp = e.paroles.filter((q) => q.nuee === x.nk && !q.draft);
      const nt = lp.filter((q) => q.status === 'tenu').length;
      return {
        etat: etatCercle(lp.map((q) => q.id)),
        t: {
          ev: x.f.text || '',
          titre: e.cercles[x.nk] || x.nk,
          et: `${String(lp.length)} PROMI · ${String(nt)} TENU${nt > 1 ? 'S' : ''}`,
          vis: true,
        },
      };
    }
    // sans parole trouvée : le titre est ce qui est entre guillemets, l'événement ce qui le précède ; une invitation reçue est un Cercle
    const m = /«\s*([^»]*?)\s*»/.exec(x.f.text || '');
    const etat: EtatCarte =
      x.f.type === 'invitation'
        ? { ...etatCercle([]), base: 282 }
        : { nat: 'promi', mode: 'complet', base: 262, col: NATTRAIT.promi, sansMatiere: true };
    return {
      etat,
      t: {
        ev: m
          ? (x.f.text || '')
              .slice(0, m.index)
              .replace(/\s*:\s*$/, '')
              .trim()
          : '',
        titre: m ? m[1]! : x.f.text || '',
        et: x.f.t ? x.f.t.toUpperCase() : '',
        vis: false,
      },
    };
  }

  function batir(force: boolean): void {
    const e = magasin.etat();
    const L = entreesFil(e, E.q(), E.filtre(), E.tri(), e.utilisateur.prenom ?? 'Moi');
    const ingenu = facade.mondeCourant().p === 'signal';
    const s = JSON.stringify([L.map((x) => [x.f, x.p, x.nk]), ingenu, facade.mondeCourant()]);
    if (E.compte) E.compte.textContent = String(filAttente(e));
    if (!force && s === sig) return;
    sig = s;
    grille.replaceChildren();
    if (!L.length) {
      grille.style.height = '';
      grille.appendChild(vide());
      return;
    }
    grille.style.height = `${String(L.length * BANDEAU.PAS + 40)}px`;
    const repeindre = (): void => {
      batir(true);
    };
    L.forEach((x, i) => {
      const { etat, t } = lire(e, x);
      const d = bandeau(etat, t, { facade, p: x.p ?? null, ingenu, repeindre });
      d.style.left = `${String(BANDEAU.X)}px`;
      d.style.top = `${String(i * BANDEAU.PAS)}px`;
      d.setAttribute('role', 'button');
      d.dataset['fid'] = String(x.f.id);
      if (x.p) d.dataset['pid'] = String(x.p.id);
      if (x.nk) d.dataset['nuee'] = x.nk;
      const p = x.p;
      const nk = x.nk;
      if (p && !p.draft)
        surToucher(d, () => {
          nav.ouvrir('fiche', p.id);
        });
      else if (nk)
        surToucher(d, () => {
          nav.ouvrir('cercle', nk);
        });
      grille.appendChild(d);
    });
    ajuster();
  }

  /** E4 (v178c, C-078) — le Fil vide, mot pour mot (`_e4Fil`) */
  function vide(): ReturnType<typeof ecranVide> {
    const Q = E.q().trim();
    if (Q)
      return ecranVide(`Rien pour «\u00a0${Q}\u00a0».`, TXT.revenirFil, () => {
        E.viderRecherche();
      });
    if (E.filtre() !== 'tous')
      return ecranVide(TXT.rienTri, TXT.revenirFil, () => {
        E.toutMontrer();
      });
    return ecranVide(TXT.rienNeBouge, TXT.anime, () => {
      E.fermer();
      nav.ouvrir('pagePlus', 'promi:faire');
    });
  }

  function ajuster(): void {
    for (const d of grille.querySelectorAll<HTMLElement>('.s4-carte')) {
      poserTitre(d);
      ajusterEtat(d);
    }
  }

  nav.poser('fil', () => {
    E.ouvrir();
  });

  return {
    ouvrir: () => {
      E.ouvrir();
    },
    fermer: () => {
      E.fermer();
    },
    ouvert: () => E.ouvert(),
  };
}
