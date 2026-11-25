/**
 * L'INDEX (SPEC-ECRANS §8 ; le prototype : `#indexSheet` et lot-S4) — l'écran d'une liste (ecran-liste.ts : l'encart, la recherche, le ⇅, la
 * montée du bas), et sa grille (dès 204) : deux cartes par ligne, 165 × 198, de 210 en 210 — la carte (carte.ts) porte sa nature, sa dalle, son
 * trait, ses mots. Une carte touchée ouvre SA fiche, par-dessus l'Index ; le X de la fiche ramène à l'Index tel qu'il était (C-193, C-250).
 */
import './index.css';
import type { Facade } from '../../moteur/facade.ts';
import type { Magasin } from '../../etat/magasin.ts';
import type { Navigation } from '../../navigation/navigation.ts';
import type { Etat, Parole } from '../../donnees/schema.ts';
import { surToucher } from '../commun.ts';
import { motsNeufs } from '../../metier/fiche.ts';
import { entreesIndex, motEtat, motQui, type Entree, type Filtre, type Tri } from '../../metier/index.ts';
import { ajusterEtat, ajusterTitre, carte, deux, DEUX, etatCercle, etatParole, poserPastille } from './carte.ts';
import { ecranVide, monterEcranListe } from '../liste/ecran-liste.ts';

const TXT = {
  titre: 'Index',
  revenirIndex: 'Revenir à tout l’Index.',
  revenirTout: 'Revenir à toutes les paroles.',
  rienGarde: 'Rien de gardé de côté.',
  rienTri: 'Rien sous ce tri.',
  pasEncore: 'Pas encore de parole.',
  premiere: 'La première se plante en une phrase.',
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
  const E = monterEcranListe<Tri, Filtre>(facade, magasin, {
    ids: { feuille: 'indexSheet', champ: 'ixSearch', tri: 'ixTriBtn', menu: 'ixMenu', liste: 'indexList' },
    titre: TXT.titre,
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
    const ent = entreesIndex(e, E.q(), E.filtre(), E.tri(), e.utilisateur.prenom ?? 'Moi');
    const moi = e.utilisateur.prenom ?? '';
    const ingenu = facade.mondeCourant().p === 'signal';
    const clair = dv.classList.contains('light');
    const s = JSON.stringify([
      ent.map((x) => (x.kind === 'nuee' ? [x.k, e.cercles[x.k], e.membres[x.k], duCercle(e, x.k)] : x.p)),
      ingenu,
      clair,
      facade.mondeCourant(),
      e.fil.filter((f) => f.unread).map((f) => f.pid),
    ]);
    if (!force && s === sig) return;
    sig = s;
    const D = deux(E.liste.clientWidth || 390);
    grille.replaceChildren();
    if (!ent.length) {
      grille.style.height = '';
      grille.appendChild(vide());
      return;
    }
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
        // Q347, C-253 : pas encore vu — une ligne du Fil de cette parole non lue, ou un mot neuf
        if (e.fil.some((f) => f.unread && f.pid === p.id) || motsNeufs(p, moi) > 0) poserPastille(d);
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

  /**
   * E4 (v178c, C-078) — LES ÉCRANS VIDES, mot pour mot (`_e4Index`). La recherche ne dit jamais la même chose qu'un vide de contenu.
   */
  function vide(): HTMLElement {
    const Q = E.q().trim();
    const tout = (): void => {
      E.toutMontrer();
    };
    if (Q)
      // les guillemets tiennent leur mot par des espaces insécables (la passe typographique du prototype)
      return ecranVide(`Rien pour «\u00a0${Q}\u00a0».`, TXT.revenirIndex, () => {
        E.viderRecherche();
      });
    if (E.filtre() === 'brouillons') return ecranVide(TXT.rienGarde, TXT.revenirTout, tout);
    if (E.filtre() !== 'tous') return ecranVide(TXT.rienTri, TXT.revenirTout, tout);
    return ecranVide(TXT.pasEncore, TXT.premiere, () => {
      E.fermer();
      nav.ouvrir('pagePlus', 'promi');
    });
  }

  function ajuster(): void {
    for (const d of grille.querySelectorAll<HTMLElement>('.s4-carte')) {
      ajusterEtat(d);
      ajusterTitre(d, DEUX.FTI);
    }
  }

  nav.poser('index', () => {
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
