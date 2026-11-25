/**
 * PEAUFINER SUR LA FICHE (lot 3b-1 ; le prototype : `bati()` et `ouvre()` de lot-S2, la rangée LE TRAIT de lot-PINCEAU, C-134, C-192, C-197).
 *
 * La barre « Peaufiner » de la fiche ouvre la page de réglages de la parole : elle couvre la fiche jusqu'à la barre (0 → 760, le corps de sa
 * nature : le cobalt d'un Promi, le framboise d'un Chiche, les deux thèmes — C-132), la barre reste à sa place et son ▾ se retourne. Les
 * rangées, dans l'ordre de l'inventaire : la tête (le titre de la parole, le X), LE TRAIT (son aperçu, son nom), À QUI (un Promi qui n'est pas
 * à soi) ou QUI OSE ? (un Chiche que j'ai lancé), AVEC (un Chiche ; vide, en pointillés), AVANT, DANS UN CERCLE (un Promi), la NOTE, les
 * PIÈCES JOINTES, les murs de Ma Parole !, SUPPRIMER CE PROMI / CE CHICHE. Les briques sont celles de la page + (src/ecrans/peaufiner).
 *
 * Il paraît et part en flaques (C-271 ; le prototype le posait d'un coup), comme celui de la page + ; le X et un glissement vers le bas le
 * referment — la fiche reste (C-134, C-193) ; un choix s'écrit tout de suite (le magasin, `peaufiner`) et la valeur de sa rangée se détrace
 * puis se trace (C-279).
 */
import type { Magasin } from '../../etat/magasin.ts';
import type { Parole } from '../../donnees/schema.ts';
import { masqueFlaques, type ControlePassage } from '../../animation/flaques/passage.ts';
import { creerPeauf } from '../peaufiner/briques.ts';
import { PINCEAUX } from '../page-plus/pinceaux.ts';
import { el, surToucher } from '../commun.ts';
import { horloge } from '../../animation/horloge.ts';
import { connus as connusDe, monterAjout, rendreListe } from '../personnes/gens.ts';
import { motAvant, dateQuand } from '../../metier/echeance.ts';
import { recue } from '../../metier/fiche.ts';
import { TEXTES_PAGE_PLUS as TP } from '../../textes/page-plus.ts';

const TXT = {
  trait: 'LE TRAIT',
  aQui: 'À QUI',
  quiOse: 'QUI OSE ?',
  avec: 'AVEC',
  personne: 'personne',
  moi: 'moi',
  moiTete: 'Moi',
  enLair: 'en l’air',
  supprimerPromi: 'SUPPRIMER CE PROMI',
  supprimerChiche: 'SUPPRIMER CE CHICHE',
  visible: (qui: string): string => `visible par ${qui}`,
  visibles: (qui: string): string => `visibles par ${qui}`,
} as const;

/** C-134 (v146) : un glissement de 220 pt vers le bas referme Peaufiner, un de 60 pt non — le seuil est entre les deux */
const SEUIL_GLISSE = 120;

export interface PeaufinerFiche {
  ouvrir(): void;
  fermer(anime?: boolean): void;
  ouvert(): boolean;
  /** la parole a changé (le magasin) : la page se rebâtit si elle est ouverte (jamais calendrier ouvert) */
  reposer(): void;
  /**
   * le « + » des membres (C-254 ; le prototype : `ouvreGens` de lot-V181A-CERCLE) : Peaufiner s'ouvre sur les personnes de la parole, leur rangée
   * dépliée, et le panneau glisse jusqu'à elles (420 ms) ; sur un Promi à soi, la rangée À QUI paraît pour l'occasion (`_v184Qui`)
   */
  ouvrirPersonnes(): void;
}

export function monterPeaufinerFiche(o: {
  fi: HTMLElement;
  barre: HTMLElement;
  chevron: HTMLElement;
  magasin: Magasin;
  parole: () => Parole | null;
  /** LA COULEUR : celle de la dalle de la parole, telle que la Toile la peint (null : « au hasard ») */
  couleur: (p: Parole) => string | null;
  /** SUPPRIMER (la confirmation, la pierre tombale : lot 3b-1b) — tant qu'il n'est pas branché, sa rangée se déclare inactive */
  supprimer?: (p: Parole) => void;
}): PeaufinerFiche {
  const { fi, barre, chevron, magasin } = o;
  const L = TP.peauf;
  const corps = el('div', { id: 'dpdCorps', class: 'dpd-corps', role: 'region', 'aria-label': 'Peaufiner' });
  corps.hidden = true;
  fi.appendChild(corps);
  const pf = creerPeauf(corps);
  let ouvert = false;

  // ── LES PERSONNES (le prototype : `_gensFiche`) — « à qui » (la tête « Moi », choisie tant que personne d'autre, avec sa croix ; la toucher
  //    retire tout le monde) et « avec » (sans tête) ; une personne touchée s'ajoute, sa croix la retire. Écrit tout de suite ; Peaufiner se
  //    rebâtit, la rangée reste ouverte. ──
  type Cle = 'who' | 'avec';
  let gensOuvert: Cle | null = null;
  /** Peaufiner ouvert par le « + » des membres : la rangée À QUI est là, même sur un Promi à soi (le prototype : `_v184Qui`) */
  let parLePlus = false;
  const lire = (p: Parole, k: Cle): string[] =>
    (k === 'avec' ? (typeof p.suite?.['avec'] === 'string' ? p.suite['avec'] : '') : (p.who ?? ''))
      .replace(/\s+et\s+moi\s*$/i, '')
      .split(/\s*[,·]\s*/)
      .map((n) => n.trim())
      .filter((n) => n && !/^(moi|le groupe|qui \?|personne)$/i.test(n));
  const ecrire = (p: Parole, k: Cle, l: string[]): void => {
    magasin.peaufiner(p.id, k === 'avec' ? { avec: l } : { qui: l }, Date.now());
  };
  const connus = (): string[] => connusDe(magasin.etat());
  let defile0 = 0;
  const ajout = monterAjout({
    parent: fi,
    zone: () => corps.querySelector<HTMLElement>('.s2-reg.s2-ouv .ph-add'),
    surface: fi,
    connus,
    valider: (n) => {
      const p = o.parole();
      if (!p || !gensOuvert) return;
      const l = lire(p, gensOuvert);
      if (!l.includes(n)) ecrire(p, gensOuvert, [...l, n]);
    },
    // rien ne passe sous le clavier : la liste de Peaufiner défile (le prototype : `saSuis`, le conteneur qui défile)
    deplacer: (y) => {
      if (y < 0.01) {
        defile0 = corps.scrollTop;
        return;
      }
      corps.scrollTop = defile0 + y;
    },
  });
  function gens(p: Parole, k: Cle): HTMLElement {
    gensOuvert = k;
    const { gn, zone } = rendreListe(
      {
        nat: p.chiche ? 'chiche' : 'promi',
        choisis: () => lire(p, k),
        tete: k === 'who' ? TXT.moiTete : null,
        teteOn: () => !lire(p, k).length,
        teteCroix: true,
        connus,
        touche: (nom, croix) => {
          const l = lire(p, k);
          if (nom === null) ecrire(p, k, []);
          else if (croix)
            ecrire(
              p,
              k,
              l.filter((x) => x !== nom),
            );
          else if (!l.includes(nom)) ecrire(p, k, [...l, nom]);
        },
      },
      ajout.touche,
    );
    ajout.rendre(zone);
    horloge().image(() => {
      ajout.poser();
    });
    return gn;
  }
  const passages = new Map<HTMLElement, ControlePassage>();

  const reduit = (): boolean => matchMedia('(prefers-reduced-motion: reduce)').matches;
  function enFlaques(e: HTMLElement, sens: 'paraît' | 'part', fin?: () => void): void {
    passages.get(e)?.stop?.();
    passages.delete(e);
    const c = masqueFlaques(e, {
      mode: sens === 'paraît' ? 'ouvre' : 'couvre',
      duree: 300,
      fin: (c) => {
        passages.delete(e);
        if (!c.arrete) fin?.();
      },
    });
    if (!c.arrete) passages.set(e, c);
  }
  /** le ▾ se retourne : il part en flaques, puis revient retourné, en flaques (C-271) */
  function retourne(ouvre: boolean): void {
    if (reduit()) {
      fi.classList.toggle('dpd-ouv', ouvre);
      return;
    }
    enFlaques(chevron, 'part', () => {
      queueMicrotask(() => {
        fi.classList.toggle('dpd-ouv', ouvre);
        enFlaques(chevron, 'paraît');
      });
    });
  }

  /** à qui la note et les pièces sont visibles (`destinataire` de lot-S2) : qui me l'a promise, à qui je la promets, ou son Cercle */
  function destinataire(p: Parole): string | null {
    if (p.from && p.from !== 'moi') return p.from;
    if (p.who && p.who !== 'moi' && p.who !== 'le groupe') return p.who;
    if (p.nuee && p.nuee !== 'soi') return magasin.etat().cercles[p.nuee] ?? p.nuee;
    return null;
  }

  function batir(p: Parole): void {
    const s = p.suite ?? {};
    const chiche = !!p.chiche;
    const liste = el('div', { class: 's2-liste' });
    liste.appendChild(
      pf.tete(p.title, TP.fermerGlyphe, TP.fermer, () => {
        fermer();
      }),
    );
    // LE TRAIT : son aperçu (96 pt, à la teinte des libellés), son nom (le prototype : `#dpTraitReg`, lot-PINCEAU)
    const nom = typeof s['trait'] === 'string' && PINCEAUX.some((x) => x.nom === s['trait']) ? s['trait'] : 'Plein';
    const rt = pf.rang(TXT.trait, nom, ' s2-trait');
    const ap = el('div', { class: 'pc-ap' });
    const dessin = PINCEAUX.find((x) => x.nom === nom)?.apercu ?? '';
    ap.innerHTML = `<svg width="96" height="18.7" viewBox="0 0 96 18.7" fill="none" aria-hidden="true">${dessin}</svg>`;
    rt.insertBefore(ap, rt.querySelector('.s2-val'));
    // au toucher, la rangée déplie le rail des douze pinceaux (lot-PINCEAU-PEAUFINER, C-196 : il glisse ; ceux de Ma Parole ! sont des murs) ;
    // un toucher choisit : la rangée se replie sur le pinceau choisi, le trait de la fiche se refait sous les yeux (« on essaie d'abord »)
    pf.deplie(rt, () =>
      railPinceaux(rt, nom, (n) => {
        pf.ouverte = null;
        magasin.peaufiner(p.id, { trait: n }, Date.now());
      }),
    );
    liste.appendChild(rt);
    // À QUI / QUI OSE ? — un Promi « je me promets » est à soi par définition : pas de rangée ; un Chiche reçu non plus (C-192)
    // Ailleurs, « à qui » et « avec » déplient le choix des personnes (lot-GENS, la brique de la page + : on ajoute, on retire)
    const aSoi = !chiche && !s['req'] && (!p.who || /^moi$/i.test(p.who));
    if ((!aSoi || parLePlus) && !(chiche && recue(p))) {
      const r = pf.rang(chiche ? TXT.quiOse : TXT.aQui, p.who || TXT.moi);
      pf.deplie(r, () => gens(p, 'who'));
      liste.appendChild(r);
    }
    // AVEC : le compagnon d'un Chiche — vide, en pointillés (§3.3)
    const avec = typeof s['avec'] === 'string' ? s['avec'] : '';
    if (chiche) {
      const r = pf.rang(TXT.avec, avec || TXT.personne, avec ? '' : ' s2-vide');
      pf.deplie(r, () => gens(p, 'avec'));
      liste.appendChild(r);
    }
    // AVANT : le même choix que la page + (C-197)
    const ra = pf.rang(L.avant, motAvant(p, magasin.aujourdhui()));
    const choisie = s['dueChoisi'] === true;
    const on = !choisie
      ? null
      : typeof s['dueISO'] === 'string'
        ? 3
        : p.due == null && !s['enLair']
          ? 4
          : ([1, 7, 30] as (number | null)[]).indexOf(p.due) >= 0
            ? ([1, 7, 30] as (number | null)[]).indexOf(p.due)
            : null;
    pf.deplie(ra, () =>
      pf.echeance({
        r: ra,
        mots: L.echeances,
        on,
        dueISO: typeof s['dueISO'] === 'string' ? s['dueISO'] : null,
        choisit: (jours) => {
          pf.ouverte = null;
          magasin.peaufiner(p.id, { echeance: { due: jours, dueISO: null, enLair: false } }, Date.now());
        },
        date: (iso, jours) => {
          magasin.peaufiner(p.id, { echeance: { due: jours, dueISO: iso, enLair: false } }, Date.now());
          return dateQuand(new Date(iso + 'T00:00:00'), jours);
        },
        replie: () => {
          pf.ouverte = null;
          reposer();
        },
      }),
    );
    liste.appendChild(ra);
    // DANS UN CERCLE : un Chiche n'en a pas (l'inventaire)
    if (!chiche) {
      const cercles = magasin.etat().cercles;
      const rc = pf.rang(L.dansUnCercle, p.nuee ? (cercles[p.nuee] ?? p.nuee) : L.aucune);
      pf.deplie(rc, () => {
        const ch = el('div', { class: 'chips', id: 'nueeChips' });
        for (const [k, n] of [['', L.aucune] as const, ...Object.entries(cercles)]) {
          const c = el('div', { class: 'chip' + ((p.nuee ?? '') === k ? ' on' : ''), role: 'button' });
          c.textContent = n;
          surToucher(c, () => {
            pf.ouverte = null;
            magasin.peaufiner(p.id, { cercle: k || null }, Date.now());
          });
          ch.appendChild(c);
        }
        return ch;
      });
      liste.appendChild(rc);
    }
    const qui = destinataire(p);
    liste.appendChild(
      pf.note({
        lab: L.note,
        vide: L.noteVide,
        vis: qui ? TXT.visible(qui) : L.notePrivee,
        valeur: typeof s['note'] === 'string' ? s['note'] : '',
        id: 'dNote',
        change: (v) => {
          magasin.peaufiner(p.id, { note: v }, Date.now());
        },
      }),
    );
    const fichiers = Array.isArray(s['files']) ? (s['files'] as unknown[]).map(String) : [];
    liste.appendChild(
      pf.pieces({
        lab: L.pieces,
        val: L.piecesVal(fichiers.length),
        vis: qui ? TXT.visibles(qui) : L.piecesPrivees,
        ajoute: (noms) => {
          magasin.peaufiner(
            p.id,
            { fichiers: [...fichiers, ...noms.filter((n) => !fichiers.includes(n))] },
            Date.now(),
          );
        },
      }),
    );
    liste.appendChild(pf.murs(L.murs, o.couleur(p)));
    const sup = pf.rang(chiche ? TXT.supprimerChiche : TXT.supprimerPromi, '', ' v16-danger');
    const fs = o.supprimer;
    if (fs)
      surToucher(sup, () => {
        fs(p);
      });
    else sup.setAttribute('aria-disabled', 'true');
    liste.appendChild(sup);
    pf.poser(liste);
  }

  function ouvrir(): void {
    const p = o.parole();
    if (ouvert || !p) return;
    ouvert = true;
    pf.ouverte = null;
    batir(p);
    corps.hidden = false;
    corps.scrollTop = 0;
    pf.croix();
    fi.classList.add('dpd-corps-ouv');
    barre.setAttribute('aria-expanded', 'true');
    if (!reduit()) enFlaques(corps, 'paraît');
    retourne(true);
  }
  function fermer(anime = true): void {
    if (!ouvert) return;
    ouvert = false;
    ajout.remettre();
    gensOuvert = null;
    parLePlus = false;
    barre.setAttribute('aria-expanded', 'false');
    const fin = (): void => {
      if (ouvert) return;
      corps.hidden = true;
      corps.replaceChildren();
      fi.classList.remove('dpd-corps-ouv');
    };
    if (!anime || reduit()) {
      for (const e of [corps, chevron]) {
        passages.get(e)?.stop?.();
        passages.delete(e);
      }
      fin();
      fi.classList.remove('dpd-ouv');
      return;
    }
    enFlaques(corps, 'part', fin);
    retourne(false);
  }
  function reposer(): void {
    const p = o.parole();
    if (!ouvert || !p) return;
    // calendrier ouvert : jamais rebâti (un champ retiré de la page referme le calendrier d'iOS) ; il se rebâtit à sa fermeture
    if (document.activeElement instanceof HTMLElement && corps.contains(document.activeElement)) return;
    batir(p);
  }

  barre.setAttribute('aria-expanded', 'false');
  surToucher(barre, (ev) => {
    // le rond Partager garde sa fonction (lot 8)
    if (ev.target instanceof Element && ev.target.closest('.dpd-part')) return;
    if (ouvert) fermer();
    else ouvrir();
  });
  // C-134 : la sortie par un glissement vers le bas (la page en haut de sa liste), jamais par un défilement
  let glisseDe: { y: number; s: number; id: number } | null = null;
  corps.addEventListener('pointerdown', (ev) => {
    glisseDe = { y: ev.clientY, s: corps.scrollTop, id: ev.pointerId };
  });
  corps.addEventListener('pointermove', (ev) => {
    const g = glisseDe;
    if (!g || g.id !== ev.pointerId || g.s > 0) return;
    const k = fi.getBoundingClientRect().width / (fi.offsetWidth || 1) || 1;
    if ((ev.clientY - g.y) / k > SEUIL_GLISSE) {
      glisseDe = null;
      fermer();
    }
  });
  for (const t of ['pointerup', 'pointercancel'] as const)
    corps.addEventListener(t, () => {
      glisseDe = null;
    });

  function ouvrirPersonnes(): void {
    const p = o.parole();
    if (!p) return;
    const lab = p.chiche ? TXT.quiOse : TXT.aQui;
    if (ouvert) fermer(false);
    parLePlus = true;
    ouvrir();
    // la rangée des personnes, dépliée (Peaufiner se rebâtit sur elle)
    pf.ouverte = lab;
    batir(p);
    const r = [...corps.querySelectorAll<HTMLElement>('.s2-reg')].find(
      (x) => (x.querySelector('.s2-lab')?.textContent ?? '').trim() === lab,
    );
    if (!r) return;
    // le panneau glisse jusqu'à elle (420 ms, aller-retour quadratique ; l'avancée bornée à 34 ms par image : une image longue ne le fait pas sauter)
    const cible = Math.max(0, Math.min(r.offsetTop - 110, corps.scrollHeight - corps.clientHeight));
    if (reduit()) {
      corps.scrollTop = cible;
      return;
    }
    const h = horloge();
    const y0 = corps.scrollTop;
    let tl = 0;
    let tp = h.maintenant();
    const pas = (): void => {
      const n = h.maintenant();
      tl += Math.min(34, n - tp);
      tp = n;
      const u = Math.min(1, tl / 420);
      const e = u < 0.5 ? 2 * u * u : 1 - (-2 * u + 2) ** 2 / 2;
      corps.scrollTop = y0 + (cible - y0) * e;
      if (u < 1 && ouvert) h.image(pas);
    };
    h.image(pas);
  }

  return { ouvrir, fermer, ouvert: () => ouvert, reposer, ouvrirPersonnes };
}

/**
 * le rail de LE TRAIT, déplié (le prototype : `garni()` de lot-PINCEAU-PEAUFINER) — 298 pt qui glissent, douze pastilles de 78 × 44 : leur trait
 * de 2 pt, plein (libre) ou en pointillés (Ma Parole !), à l'encre du contour de la rangée ; la choisie à la teinte du libellé ; l'échantillon
 * (60 pt) d'un pinceau libre ou choisi ; un pinceau de Ma Parole ! est un MUR (lot-V163B-PINCEAU : flou 4,8 px, trait plein, sans prise)
 */
function railPinceaux(r: HTMLElement, choisi: string, choisit: (nom: string) => void): HTMLElement {
  const gl = el('div', { class: 'pc-glisse', 'data-glisse': '1' });
  const rail = el('div', { class: 'pc-rail' });
  const B: Array<[HTMLElement, HTMLElement, HTMLElement, boolean, boolean]> = [];
  for (const p of PINCEAUX) {
    const on = p.nom === choisi;
    const montre = p.libre || on;
    const b = el('button', {
      type: 'button',
      class: 'pc-t' + (on ? ' on' : '') + (!p.libre && !on ? ' pc-mur' : ''),
      'data-t': p.nom,
    });
    b.style.borderRadius = '22px';
    b.style.background = 'transparent';
    if (p.libre) b.setAttribute('aria-pressed', on ? 'true' : 'false');
    const e = el('span', { class: 'pc-e' });
    if (montre && p.dessin)
      e.innerHTML = `<svg width="60" height="11.7" viewBox="0 0 60 11.7" fill="none" aria-hidden="true">${p.dessin}</svg>`;
    const n = el('span', { class: 'pc-n' });
    n.textContent = p.nom;
    b.append(e, n);
    B.push([b, e, n, on, p.libre]);
    surToucher(b, () => {
      // un pinceau de Ma Parole ! est un mur : il ne s'applique pas sans elle (C-196 ; sa phrase de mur : lot 8)
      if (!p.libre || on) return;
      choisit(p.nom);
    });
    rail.appendChild(b);
  }
  gl.appendChild(rail);
  // la teinte (celle du libellé) et l'encre (le contour de la rangée) se LISENT sur la rangée rendue (le prototype : « la teinte se relève à
  // l'écran, jamais dans une règle ») — rebâtie après un choix, la rangée n'est pas encore dans la page : on les lit à l'image qui suit
  const colorer = (): boolean => {
    const teinte = r.isConnected ? getComputedStyle(r.querySelector('.s2-lab')!).color : '';
    const encre = r.isConnected ? getComputedStyle(r).borderTopColor : '';
    if (!teinte || !encre) return false;
    for (const [b, e, n, on, libre] of B) {
      const fg = on ? teinte : encre;
      b.style.border = `2px ${libre ? 'solid' : 'dashed'} ${fg}`;
      e.style.color = fg;
      n.style.color = fg;
    }
    return true;
  };
  if (!colorer())
    horloge().image(() => {
      colorer();
    });
  return gl;
}
