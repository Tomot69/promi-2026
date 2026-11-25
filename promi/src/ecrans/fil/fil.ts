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
import { el, surToucher } from '../commun.ts';
import { horloge } from '../../animation/horloge.ts';
import { toast } from '../feuilles/feuilles.ts';
import { NATTRAIT } from '../page-plus/trait.ts';
import { motEtat, motQui } from '../../metier/index.ts';
import {
  entreesFil,
  evenementSansTitre,
  filAttente,
  type EntreeFil,
  motGeste,
  type FiltreFil,
  type Geste,
  type TriFil,
} from '../../metier/fil.ts';
import { ajusterEtat, etatCercle, etatParole, poserPastille, type EtatCarte } from '../index/carte.ts';
import { motsNeufs } from '../../metier/fiche.ts';
import { ecranVide, monterEcranListe } from '../liste/ecran-liste.ts';
import { BANDEAU, bandeau, poserTitre, type TextesBandeau } from './bandeau.ts';

const TXT = {
  titre: 'Fil',
  revenirFil: 'Revenir à tout le Fil.',
  rienTri: 'Rien sous ce tri.',
  rienNeBouge: 'Rien ne bouge encore.',
  anime: 'Une parole donnée à quelqu’un, et le Fil s’anime.',
  reporter: 'Reporter\u2026',
  demain: 'demain',
  semaine: '1 sem.',
  mois: '1 mois',
} as const;
/** l'appui maintenu qui déplie la rangée des gestes (`_s4Fil`) ; la rangée et ce qu'elle ajoute sous son bandeau */
const APPUI = 480;
const RANGEE = { H: 50, PAS: 62, GAP: 12 } as const;
/** un geste « fort » porte le trait de l'état (v89 : RELEVER, REJOINDRE, TRACER) ; REPORTER, non */
const FORT: Record<Geste, boolean> = { tracer: true, releve: true, rejoindre: true, post: false };
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
  /** la recherche tapée (l'état de l'écran, pas une donnée du magasin : elle ne se garde pas) */
  recherche(): string;
}

const estMoi = (v: unknown): boolean => {
  const s = typeof v === 'string' ? v.trim().toLowerCase() : '';
  return !s || s === 'moi';
};

export function monterFil(facade: Facade, magasin: Magasin, nav: Navigation): Fil {
  const E = monterEcranListe<TriFil, FiltreFil>(facade, magasin, {
    ids: {
      feuille: 'feedView',
      champ: 'fdSearch',
      tri: 'fdTriBtn',
      menu: 'fdMenu',
      liste: 'feedList',
      croix: 'fdClose',
    },
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
  /** le bandeau dont la rangée des gestes est dépliée (`_filGeste`) : sa clé, `p<id>`, `n<cercle>` ou `i<rang>` */
  let ouvert: string | null = null;
  const cle = (x: EntreeFil, i: number): string => (x.p ? `p${String(x.p.id)}` : x.nk ? `n${x.nk}` : `i${String(i)}`);

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
    // Q347, C-253 : pas encore vu — la ligne elle-même, ou un mot neuf de sa parole (sur sa ligne la plus récente seulement)
    const moi = e.utilisateur.prenom ?? '';
    const premiere = new Set<number>();
    const vues = new Set<number>();
    for (const x of L)
      if (x.p && !vues.has(x.p.id)) {
        vues.add(x.p.id);
        premiere.add(x.f.id);
      }
    const deplie = (x: EntreeFil, i: number): boolean => x.gestes.length > 0 && cle(x, i) === ouvert;
    grille.style.height = `${String(L.reduce((a, x, i) => a + BANDEAU.PAS + (deplie(x, i) ? RANGEE.PAS : 0), 0) + 32)}px`;
    let y = 0;
    const repeindre = (): void => {
      batir(true);
    };
    L.forEach((x, i) => {
      const { etat, t } = lire(e, x);
      const d = bandeau(etat, t, {
        facade,
        p: x.p ?? null,
        ingenu,
        repeindre,
        largeur: (E.liste.clientWidth || 390) - 2 * BANDEAU.X,
      });
      d.style.left = `${String(BANDEAU.X)}px`;
      d.style.top = `${String(y)}px`;
      y += BANDEAU.PAS;
      d.setAttribute('role', 'button');
      d.dataset['fid'] = String(x.f.id);
      if (x.p) d.dataset['pid'] = String(x.p.id);
      if (x.nk) d.dataset['nuee'] = x.nk;
      d.dataset['nonvu'] = x.f.unread ? '1' : '0';
      if (x.f.unread || (x.p && premiere.has(x.f.id) && motsNeufs(x.p, moi) > 0)) poserPastille(d);
      const p = x.p;
      const nk = x.nk;
      // un toucher bref ouvre sa fiche ; un appui maintenu (480 ms) déplie — ou replie — la rangée de ses gestes, et n'ouvre rien
      let longue = false;
      const fid = x.f.id;
      if (p && !p.draft)
        surToucher(d, () => {
          if (longue) return;
          magasin.filVu(fid);
          nav.ouvrir('fiche', p.id);
        });
      else if (nk)
        surToucher(d, () => {
          if (!longue) nav.ouvrir('cercle', nk);
        });
      if (x.gestes.length) {
        const k = cle(x, i);
        let m: number | null = null;
        const desarme = (): void => {
          if (m != null) horloge().annuleMinuteur(m);
          m = null;
        };
        d.addEventListener('pointerdown', (ev) => {
          longue = false;
          if (ev.button) return;
          desarme();
          m = horloge().minuteur(() => {
            m = null;
            longue = true;
            ouvert = ouvert === k ? null : k;
            batir(true);
          }, APPUI);
        });
        for (const t of ['pointerup', 'pointerleave', 'pointercancel'] as const) d.addEventListener(t, desarme);
        d.addEventListener('pointermove', (ev) => {
          if (m != null && (Math.abs(ev.movementX) > 3 || Math.abs(ev.movementY) > 3)) desarme();
        });
      }
      grille.appendChild(d);
      if (deplie(x, i)) {
        grille.appendChild(rangee(x, etat, y - 12));
        y += RANGEE.PAS;
      }
    });
    ajuster();
  }

  /** la rangée des gestes d'un bandeau (`_s4Fil`, Q75 : un ajout validé, hors inventaire — elle n'existe qu'au besoin) */
  function rangee(x: EntreeFil, etat: EtatCarte, top: number): HTMLElement {
    const r = el('div', { class: 's4-actes' });
    r.style.left = `${String(BANDEAU.X + 16)}px`;
    r.style.top = `${String(top)}px`;
    for (const g of x.gestes) {
      const b = el('button', { type: 'button', class: `s4-acte${FORT[g] ? ' fort' : ''}`, 'data-geste': g });
      b.textContent = motGeste(g);
      if (FORT[g]) b.style.setProperty('--acte', etat.col);
      surToucher(b, () => {
        ouvert = null; // l'ajout se referme dès qu'il a servi
        geste(g, x);
        batir(true);
      });
      r.appendChild(b);
    }
    return r;
  }

  /** ce que fait un geste (`feedPostpone`, `filTracer` ; RELEVER et REJOINDRE : les deux états neufs de v89, sans événement de ce genre ici) */
  function geste(g: Geste, x: EntreeFil): void {
    const fid = x.f.id;
    if (g === 'tracer' && x.p) nav.ouvrir('fiche', x.p.id);
    else if (g === 'post')
      toast(facade.appareil(), TXT.reporter, [
        [
          TXT.demain,
          () => {
            magasin.reporter(fid, 1, Date.now());
          },
        ],
        [
          TXT.semaine,
          () => {
            magasin.reporter(fid, 7, Date.now());
          },
        ],
        [
          TXT.mois,
          () => {
            magasin.reporter(fid, 30, Date.now());
          },
        ],
      ]);
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
      const et = d.querySelector<HTMLElement>('.s4-et');
      // le prototype laisse un état long déborder de sa boîte jusqu'au bord du bandeau ; seul ce qui dépasse le bandeau s'arrête par « … »
      if (et) {
        et.classList.remove('et-coupe');
        et.classList.toggle('et-coupe', et.offsetLeft + et.scrollWidth > d.clientWidth + 1);
      }
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
    recherche: () => E.q(),
  };
}
