/**
 * LA FICHE D'UNE PAROLE (lot 3a-1, SPEC-ECRANS §4) — Promi et Chiche, au repos : le champ (l'aplat de la nature borné par la vague, la vraie
 * dalle du moteur teintée par la rampe de sa nature, Q30), le plateau (le mot de la nature, le X), le bouton photo, le trait (ligne.ts), le mot
 * du geste, les Noyaux, la phrase complète (C-069), le titre, la ligne d'état (C-210), « Un mot… » (C-116) et la barre Peaufiner fermée. Elle
 * s'ouvre par la navigation (`nav.ouvrir('fiche', id)` : une dalle de la Toile) et se ferme par son X.
 * Les cotes sont celles du prototype (`ecran()` et `_ficheCotes` de lot-S1B-geo, et les blocs qui les corrigent), comparées au pixel par
 * tests/rendu/fiche.spec.ts. Tracer et tenir (3a-2) : tenir.ts ; l'instant (« le trait se referme » sous le rideau, puis « juste après », qui reste
 * tant que la fiche est ouverte — `inv()` de lot-S5) est posé ici. Pas encore : la jonction au défilement (3a-3), le titre modifiable (3a-4), Peaufiner
 * ouvert, les commentaires, la photo, le dessin (3b), la fiche d'un Cercle (lot 5).
 */
import './fiche.css';
import type { Facade } from '../../moteur/facade.ts';
import type { Magasin } from '../../etat/magasin.ts';
import type { Navigation } from '../../navigation/navigation.ts';
import type { Parole } from '../../donnees/schema.ts';
import { palette } from '../../design/jetons.ts';
import { horloge } from '../../animation/horloge.ts';
import { cheminOnde, onde } from '../page-plus/onde.ts';
import { NATTRAIT, TRAIT_K } from '../page-plus/trait.ts';
import { avecAlpha, el, esc, poserCroix, surToucher, SVG_PHOTO } from '../commun.ts';
import { CRETE, peindreLigne, W } from './ligne.ts';
import { noyauxDe, peindreNoyaux, rangeeNoyaux } from './noyaux.ts';
import { monterTenir, type Instant } from './tenir.ts';
import { monterJonction } from './jonction.ts';
import { monterMots } from './mots.ts';
import { monterTitre } from './titre.ts';
import { monterPeaufinerFiche } from './peaufiner.ts';
import { monterSaisieMot } from './saisie-mot.ts';
import { monterMenuPhoto, mondeOrigine, photoDe, SVG_RETOUR } from './photo.ts';
import { imagePhoto, peindrePhoto } from '../photo/peinture.ts';
import { monterEntier, type Cadre, type Entier } from '../photo/entier.ts';
import { dessinVu, monterBandeDessin } from './dessin-fiche.ts';
import { batirFil, batirTete, monterMenuPlanter, noyauxCercle, peindreBande } from './cercle.ts';
import { AMP_CERCLE, baseCercle, ligneAvec, ligneEtatCercle, parolesDuCercle } from '../../metier/cercle.ts';
import { couleurDe, dessinEntier, dessinPose, modeDessinPartage, type Dessin } from '../page-plus/dessin.ts';
import { origineGardee } from '../../metier/origine.ts';
import { annulable, confirmer } from '../feuilles/feuilles.ts';
import { chargerTrace } from '../../animation/trace/trace.ts';
import { nomPinceau } from '../../animation/trace/pinceau.ts';
import { haptique } from '../../natif/haptique.ts';
import {
  aPlusieurs,
  consigne,
  etatParts,
  initiales,
  ligneEtat,
  ligneJusteApres,
  phraseTenue,
  phraseFiche,
  recue,
  traitFiche,
  type Morceau,
  type Trait,
} from '../../metier/fiche.ts';

export interface Fiche {
  ouvrir(id: number): void;
  /** la fiche d'un Cercle (lot 5) : le même écran, son mode Cercle */
  ouvrirCercle(cle: string): void;
  fermer(): void;
  /** pour les tests : la parole ouverte, et ce que la fiche a posé */
  etat(): {
    id: number | null;
    cercle: string | null;
    base: number;
    amp: number;
    mode: string;
    instant: Instant;
    jonction: ReturnType<ReturnType<typeof monterJonction>['etat']>;
  };
  /** pour les tests : le geste */
  tenir(): ReturnType<ReturnType<typeof monterTenir>['etat']>;
}

type Nature = 'promi' | 'chiche';

const CHAMP: Record<Nature, string> = { promi: palette.bleu45, chiche: palette.framboise54 };
const hex = (v: string): number[] => [1, 3, 5].map((i) => parseInt(v.slice(i, i + 2), 16));
const RAMPE: Record<Nature, number[][]> = {
  promi: [palette.rampePromi1, palette.rampePromi2, palette.rampePromi3].map(hex),
  chiche: [palette.rampeChiche1, palette.rampeChiche2, palette.rampeChiche3].map(hex),
};
const TXT = {
  fermer: 'Fermer',
  fermerGlyphe: 'X',
  photo: 'Photo',
  unMot: 'Un mot…',
  peaufiner: 'Peaufiner',
  chevron: '▾',
  partager: 'Partager',
  supprimerPromi: 'Supprimer ce Promi ?',
  supprimerChiche: 'Supprimer ce Chiche ?',
  supprimer: 'Supprimer',
  garder: 'Garder',
  promiSupprime: 'Promi supprimé',
  chicheSupprime: 'Chiche supprimé',
  annuler: 'Annuler',
} as const;
const SVG_PARTAGE =
  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12v7a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-7"/><path d="M16 6l-4-4-4 4"/><path d="M12 2v14"/></svg>';
/** le « + » des membres : le signe seul, haut d'une capitale de la phrase (18), trait 6,16 sur 22 (C-242, C-254) */
const SVG_PLUS_MEMBRES =
  '<svg width="18" height="18" viewBox="0 0 22 22" aria-hidden="true"><path d="M11 3.08V18.92 M3.08 11H18.92" fill="none" stroke="' +
  palette.orangeDepart +
  '" stroke-width="6.16" stroke-linecap="round"/></svg>';

export function monterFiche(facade: Facade, magasin: Magasin, nav: Navigation): Fiche {
  const dv = facade.appareil();
  const fi = el('div', { id: 'detailPoster', class: 'fiche', role: 'dialog' });
  fi.hidden = true;
  // la couche qui défile (le plateau et la barre Peaufiner restent posés au-dessus d'elle, dans la fiche : ils ne défilent pas — lot-V184A)
  const defile = el('div', { id: 'dpDefile', class: 'fi-defile' });
  // la hauteur du contenu : celle de l'écran, ou le bas des mots + 96 (`espace` de lot-V181B-TEXTES)
  const espace = el('div', { class: 'fi-espace', 'aria-hidden': 'true' });
  const champ = el('canvas', { id: 'dpTrameCv', class: 'fi-champ', 'aria-hidden': 'true' });
  const trait = el('canvas', { class: 'fi-trait', 'aria-hidden': 'true' });
  const plateau = el('div', { class: 'enh' });
  const mot = el('div', { id: 'dptNat', class: 'fi-mot enh-t' });
  const croix = el('div', { class: 'closeb', role: 'button', 'aria-label': TXT.fermer, 'data-close': '' });
  const croixG = el('span', { class: 'cb-mot' });
  croixG.textContent = TXT.fermerGlyphe;
  croix.appendChild(croixG);
  plateau.append(mot, croix);
  const photo = el('button', { type: 'button', class: 'ph-photo-btn', 'aria-label': TXT.photo });
  photo.innerHTML = SVG_PHOTO;
  photo.style.backgroundColor = avecAlpha(palette.brun09, 0.18);
  const geste = el('div', { id: 'dptTrace', class: 'fi-trace' });
  const noyaux = el('div', { id: 'dAura', class: 'fi-noyaux' });
  const plusM = el('button', { type: 'button', class: 'fi-plus-membres', 'aria-label': 'Ajouter des membres' });
  plusM.innerHTML = SVG_PLUS_MEMBRES;
  const phrase = el('div', { id: 'dptQui', class: 'fi-phrase' });
  const titre = el('div', { id: 'dptTitre', class: 'fi-titre' });
  const etatL = el('div', { id: 'dptQuand', class: 'fi-etat' });
  const unMot = el('div', { id: 'cm5Ligne', class: 'cm5' });
  const unMotTxt = el('span', { class: 'cm5-mot' });
  unMotTxt.textContent = TXT.unMot;
  const nbMots = el('span', { class: 'cm5-nb' });
  unMot.append(unMotTxt, nbMots);
  const barre = el('div', { id: 'dpDetails' });
  const barreTog = el('div', { id: 'dpdTog', class: 'dpd-tog', role: 'button', 'aria-label': TXT.peaufiner });
  barre.appendChild(barreTog);
  const barreLab = el('span', { class: 'dpd-mot' });
  barreLab.textContent = TXT.peaufiner;
  const barreChev = el('i', { 'aria-hidden': 'true' });
  barreChev.textContent = TXT.chevron;
  const partage = el('span', { class: 'dpd-part', role: 'button', 'aria-label': TXT.partager });
  partage.innerHTML = SVG_PARTAGE;
  barreTog.append(barreLab, barreChev, partage);
  // pas encore porté (lot 8 : Partager) : il se déclare inactif (`aria-disabled`), et le retire quand son lot le branche
  partage.setAttribute('aria-disabled', 'true');
  // le fil d'un Cercle (lot 5), dans la couche qui défile ; sa tête (« Un mot… », « Planter dans le Cercle ») collée au bas, hors d'elle
  const fil = el('div', { id: 'dpNueeFil', class: 'fi-fil' });
  fil.hidden = true;
  const { tete, cale, planter } = batirTete();
  tete.hidden = true;
  // « Planter dans le Cercle » : son menu (C-230) — Chiche ou Promi ; la page + de cette nature, rattachée au Cercle, ses membres déjà choisis
  const menuPlanter = monterMenuPlanter(fi, dv, (nat) => {
    if (cercle) nav.ouvrir('pagePlus', `${nat}:cercle:${cercle}`);
  });
  surToucher(planter, () => {
    if (!cercle) return;
    if (menuPlanter.ouvert()) menuPlanter.fermer();
    else menuPlanter.ouvrir(planter);
  });
  defile.append(champ, trait, photo, geste, noyaux, plusM, phrase, titre, etatL, fil, unMot, espace);
  // le dessin posé, dans la bande (dessin-fiche.ts, lot 3b-5) : sa couche juste après le champ, sous le trait
  const bandeDessin = monterBandeDessin(defile, champ);
  const dessinDe = (p: Parole): Dessin | null => (p.suite?.['dessin'] as Dessin | undefined) ?? null;
  // le plateau d'abord, comme dans le prototype (`.enh`, le premier bloc de la fiche) ; il passe au-dessus de la couche qui défile par son z
  fi.append(plateau, defile, tete, barre);
  dv.appendChild(fi);

  let courant: Parole | null = null;
  /** le Cercle ouvert (sa clé), quand la fiche est en mode Cercle — alors `courant` est nul */
  let cercle: string | null = null;
  let deplie = false;
  /**
   * C-244 : le titre coupé, déplié par un premier toucher (`_titreDeplie`, cette fiche seulement, oublié à la fermeture) ; C-280 : entier tant
   * qu'il se modifie. Déplié ou modifié, « Un mot… » ne suit plus la ligne d'état pas à pas : sa place est figée (`dyFige`, le `_titreDecal`
   * du prototype) — au dépliage, elle garde l'air qu'elle avait sous l'état replié.
   */
  let titreDeplie = false;
  let titreEdite = false;
  let dyFige: number | null = null;
  let T: Trait = { mode: 'moitie', base: 286, amp: 36, carte: false };
  /** l'instant de « tenir » (lot-S5) : null, « le trait se referme » (sous le rideau), « juste après » */
  let instantF: Instant = null;
  /** pendant le geste : l'abscisse du doigt (le plein le suit) */
  let doigtX: number | null = null;
  /** les trois écrans de l'instant : base 300, amplitude 36, la dalle 180 × 150 à (105, 91), le trait amande plein */
  const INSTANT_TRAIT: Trait = { mode: 'complet', base: 300, amp: 36, carte: false };
  const INSTANT_DALLE = { x: 105, y: 91, w: 180, h: 150 } as const;

  surToucher(croix, () => {
    fermer();
  });
  // une ligne du fil d'un Cercle touchée : la fiche redescend, puis remonte sur sa parole (240 ms : le prototype, `renderDetail` › `.nf-item`)
  surToucher(fil, (ev) => {
    const it = ev.target instanceof Element ? ev.target.closest<HTMLElement>('.nf-item') : null;
    const id = Number(it?.dataset['id']);
    if (!cercle || !it || !Number.isFinite(id)) return;
    fermer();
    horloge().minuteur(() => {
      ouvrir(id);
    }, 240);
  });
  // « + x personnes » : un toucher déroule la liste entière dans la phrase, qui s'allonge vers le bas ; le titre descend (C-069)
  surToucher(phrase, (ev) => {
    if (!courant || !(ev.target instanceof Element) || !ev.target.closest('.fi-plus')) return;
    deplie = true;
    poser(courant);
  });

  function nature(p: Parole): Nature {
    return p.chiche ? 'chiche' : 'promi';
  }

  /** la boîte de la photo (celle de la dalle), et son cadrage pendant un geste (écrit à la fin du geste : `magasin.cadrer`) */
  let boitePhoto: { x: number; y: number; w: number; h: number } | null = null;
  let cadreVif: Cadre | null = null;
  /** la vue « en entier » (montée plus bas, avec Peaufiner et la saisie qu'elle doit connaître) */
  let entier: Entier | null = null;

  // ── LE CHAMP : l'aplat de la nature au-dessus de la vague, et la dalle dans sa boîte (`ecran()` : y 124, dh = min(300, base − amp − 136)) ──
  function peindreChamp(p: Parole): void {
    const n = nature(p);
    const H = T.base + T.amp + 40;
    const dpr = Math.max(2, Math.min(3, window.devicePixelRatio || 2));
    champ.width = Math.round(W * dpr);
    champ.height = Math.round(H * dpr);
    champ.style.width = `${String(W)}px`;
    champ.style.height = `${String(H)}px`;
    const g = champ.getContext('2d');
    if (!g) return;
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.clearRect(0, 0, W, H);
    g.imageSmoothingEnabled = true;
    g.imageSmoothingQuality = 'high';
    const y = onde(T.base, T.amp);
    g.beginPath();
    cheminOnde(g, y, 0, W, W);
    g.lineTo(W, 0);
    g.lineTo(0, 0);
    g.closePath();
    g.fillStyle = CHAMP[n];
    g.fill();
    champ.setAttribute('data-champ', CHAMP[n]);
    const dh = Math.min(300, T.base - T.amp - 124 - 12);
    const dw = Math.min(320, Math.floor(1.2 * dh));
    const b = instantF ? INSTANT_DALLE : { x: Math.floor((W - dw) / 2), y: 124, w: dw, h: dh };
    // la dalle : teinte par la rampe de sa nature (Q30) — sauf sous une photo (Q53), ou « La dalle d'origine » loin du champ (Q365 : ΔE ≥ 15,
    // peinte dans le monde de sa plantation, sa couleur gardée)
    const src = photoDe(p);
    const mo = mondeOrigine(p);
    const ob = mo && !src ? origineGardee(facade.labDalle(p.id, mo), CHAMP[n]) : null;
    champ.setAttribute('data-origine', ob ? `${ob.origine ? 'origine' : 'rampe'}|${ob.dE.toFixed(1)}` : '');
    const r = facade.poserDalle(g, p.id, b.x, b.y, b.w, b.h, {
      ...(!src && !ob?.origine && { rampe: { cols: RAMPE[n], haut: 2 } }),
      ...(mo && { monde: mo }),
    });
    champ.setAttribute('data-matiere', r ? [r.x, r.y, r.w, r.h].map((v) => Math.round(v)).join(',') : '');
    // la photo REMPLACE la dalle (lot-PHOTO) : la même boîte, en couverture ou cadrée, bornée par l'onde — jamais pendant l'instant
    const im =
      src && !instantF
        ? imagePhoto(src, () => {
            if (courant && courant.id === p.id) peindreChamp(courant);
          })
        : null;
    boitePhoto = b;
    if (src && im) peindrePhoto(g, im, b, y, W, cadreVif ?? p.suite?.['photoCadre'], src.length);
    champ.setAttribute('data-photo', src && im ? '1' : '');
    // le dessin posé REMPLACE la dalle ou la photo (une couche pleine, découpée 7 pt au-dessus du trait) ; l'œil le masque pour soi
    bandeDessin.poser({
      d: dessinDe(p),
      y,
      nature: CHAMP[n],
      instant: !!instantF,
      masquer: () => {
        const q = courant;
        const d = q && dessinDe(q);
        if (q && d && dessinPose(d)) magasin.dessin(q.id, { ...d, masque: !d.masque });
      },
    });
    entier?.annoncer();
    // le bouton : avec une photo, le signe du retour (« revenir à la dalle ») ; sinon le cadre traversé d'un trait (C-060)
    const ico = src ? SVG_RETOUR : SVG_PHOTO;
    if (photo.dataset['ico'] !== (src ? 'retour' : 'cadre')) {
      photo.innerHTML = ico;
      photo.dataset['ico'] = src ? 'retour' : 'cadre';
    }
  }

  // ── LE TRAIT : sur sa couche (la jonction, 3a-3, la tiendra au défilement) ──
  function peindreTrait(p: Parole): void {
    const H = T.base + T.amp + 40;
    const dpr = Math.max(2, Math.min(3, window.devicePixelRatio || 2));
    trait.width = Math.round(W * dpr);
    trait.height = Math.round(H * dpr);
    trait.style.width = `${String(W)}px`;
    trait.style.height = `${String(H)}px`;
    const g = trait.getContext('2d');
    if (!g) return;
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.clearRect(0, 0, W, H);
    const o = optionsLigne(p);
    peindreLigne(g, T.base, T.amp, { ...o, doigt: doigtX ?? undefined });
    trait.setAttribute('data-trait', [T.base, T.amp, o.col, T.mode].join(','));
  }

  /** ce que le peintre de la ligne reçoit (le trait de la fiche, et son trait plat de la jonction) */
  function optionsLigne(p: Parole): Parameters<typeof peindreLigne>[3] {
    const n = nature(p);
    const tenu = p.status === 'tenu';
    const plusieurs = !tenu && aPlusieurs(p);
    const S = plusieurs ? etatParts(p) : null;
    return {
      mode: T.mode,
      col: instantF ? palette.menthe82 : tenu ? CRETE : NATTRAIT[n],
      attend: !instantF && !!consigne(p),
      parts: S && !instantF ? { S, initiales: initiales(S.T, moiNom()), encre: palette.creme95 } : undefined,
      pinceau: nomPinceau(p.suite?.['trait']),
    };
  }

  function moiNom(): string {
    return magasin.etat().utilisateur.prenom || 'Moi';
  }

  function poser(p: Parole): void {
    const n = nature(p);
    T = instantF ? INSTANT_TRAIT : traitFiche(p);
    fi.classList.toggle('fi-promi', n === 'promi');
    fi.classList.toggle('fi-chiche', n === 'chiche');
    fi.classList.toggle('fi-tenue', p.status === 'tenu');
    mot.innerHTML = n === 'promi' ? 'Prom<i class="mm-i">i</i>' : 'Chiche';
    // le X face au titre, centré sur ses capitales, lu sur la police rendue (lot-V157-CROIX)
    poserCroix(croix, croixG, mot);
    peindreChamp(p);
    peindreTrait(p);
    // « le trait se referme » : tout se retire sous le rideau (posé avant les cotes : elles se lisent sur le rendu)
    for (const e of [noyaux, phrase, titre, etatL]) e.hidden = instantF === 'referme';
    const c = instantF ? null : consigne(p, moiNom());
    geste.hidden = !c;
    geste.textContent = c ?? '';
    geste.classList.toggle('fi-depart', !!c && /^trace pour/.test(c));
    const ph = phraseFiche(p, deplie);
    phrase.innerHTML = ph ? ph.morceaux.map(morceau).join('') : '';
    titre.textContent = p.title;
    const le = ligneEtat(p, magasin.aujourdhui());
    etatL.textContent = le.texte;
    etatL.classList.toggle('fi-tenu', le.tenu);
    noyaux.innerHTML = rangeeNoyaux(
      noyauxDe(p, magasin.etat().paroles, magasin.etat().cercles),
      CHAMP[n],
      p.status === 'tenu',
      court,
    );
    peindreNoyaux(noyaux);
    partage.style.borderColor = n === 'chiche' ? palette.brun09 : palette.creme95;
    poserPhoto();
    poserNombre(p);
    coter(!!c);
    tenir.poser(!instantF && p.status !== 'tenu');
    poserInstant(p);
    poserPlus(recue(p));
    poserMots(p);
  }

  /**
   * LE MODE CERCLE (lot 5, SPEC-ECRANS §7 ; `_ficheNuee` du prototype) — le trait entier sur l'onde (base `baseCercle`, amplitude 40) ; la bande ;
   * les Noyaux à boîte − 29, « Avec … » 127 plus bas, le nom 35 plus bas (38 pt, deux lignes au plus : jusqu'à 26, puis « … »), la ligne d'état
   * 68 sous le nom (un nom de deux lignes : sa hauteur + 29,2), le fil 31 sous elle ; la tête collée au bas (son bas à 748).
   */
  function poserCercle(k: string): void {
    const e = magasin.etat();
    const liste = parolesDuCercle(e.paroles, k);
    const nom = e.cercles[k] ?? k;
    T = { mode: 'complet', base: baseCercle(liste.length), amp: AMP_CERCLE, carte: false };
    fi.classList.remove('fi-promi', 'fi-chiche', 'fi-tenue');
    fi.classList.add('fi-cercle');
    mot.textContent = 'Cercle';
    poserCroix(croix, croixG, mot);
    poserPhoto();
    peindreChampCercle(liste);
    peindreTraitCercle();
    geste.hidden = true;
    tenir.poser(false);
    const boite = T.base + T.amp + 40;
    const yN = boite - 29;
    const yQui = yN + 127;
    const yTitre = yQui + 35;
    noyaux.innerHTML = rangeeNoyaux(noyauxCercle(k, nom, liste, e.paroles), palette.mauve77, false, court);
    peindreNoyaux(noyaux);
    noyaux.style.top = `${String(yN)}px`;
    phrase.textContent = ligneAvec(e.membres[k] ?? []);
    phrase.style.top = `${String(yQui)}px`;
    titre.style.top = `${String(yTitre)}px`;
    titre.textContent = nom;
    ajusterNom(nom);
    const hT = Math.round(
      titre.getBoundingClientRect().height / (fi.getBoundingClientRect().width / fi.offsetWidth || 1),
    );
    const yEtat = Math.round(yTitre + (hT > 50 ? hT + 29.2 : 68));
    etatL.textContent = ligneEtatCercle(liste);
    etatL.classList.remove('fi-tenu');
    etatL.style.top = `${String(yEtat)}px`;
    fil.hidden = false;
    const basFil = batirFil(facade, fil, liste, yEtat + 31);
    // la tête : « Un mot… » seulement si le Cercle porte des paroles (un Cercle vide : 16 pt seulement entre l'état et « Planter », la ligne y
    // recouvrirait l'état — lot-V145-COMM, Q511)
    tete.hidden = false;
    cale.hidden = !liste.length;
    if (unMot.parentElement !== cale) cale.appendChild(unMot);
    unMot.style.translate = '';
    nbMots.hidden = true;
    partage.style.borderColor = palette.creme95;
    poserPlus(false);
    const hauteur = basFil != null && basFil + 282 > 844 ? Math.ceil(basFil + 282) : defile.clientHeight || 844;
    espace.style.height = `${String(hauteur)}px`;
    jonction.poser({ base: T.base, amp: T.amp, champ: palette.mauve77, hauteur });
  }

  /** le nom d'un Cercle : 38 pt ; plus de deux lignes, il descend jusqu'à 26 ; puis « … » (C-244 §5.2) */
  function ajusterNom(nom: string): void {
    const lignes = (): number => {
      const lh = parseFloat(getComputedStyle(titre).lineHeight) || parseFloat(titre.style.fontSize) * 1.02;
      return Math.round(titre.offsetHeight / lh);
    };
    delete titre.dataset['coupe'];
    titre.style.fontSize = '38px';
    if (lignes() <= 2) return;
    let f = 38;
    while (f > 26 && lignes() > 2) {
      f -= 1;
      titre.style.fontSize = `${String(f)}px`;
    }
    if (lignes() <= 2) return;
    titre.dataset['coupe'] = '1';
    let lo = 0;
    let hi = nom.length;
    while (lo < hi) {
      const md = (lo + hi + 1) >> 1;
      titre.textContent = nom.slice(0, md).replace(/\s+$/, '') + '\u2026';
      if (lignes() <= 2) lo = md;
      else hi = md - 1;
    }
    titre.textContent = nom.slice(0, lo).replace(/\s+$/, '') + '\u2026';
  }

  function peindreChampCercle(liste: readonly Parole[]): void {
    const H = T.base + T.amp + 40;
    const dpr = Math.max(2, Math.min(3, window.devicePixelRatio || 2));
    champ.width = Math.round(W * dpr);
    champ.height = Math.round(H * dpr);
    champ.style.width = `${String(W)}px`;
    champ.style.height = `${String(H)}px`;
    const g = champ.getContext('2d');
    if (!g) return;
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.clearRect(0, 0, W, H);
    g.imageSmoothingEnabled = true;
    g.imageSmoothingQuality = 'high';
    const top = parseFloat(photo.style.top) || 0;
    const m = peindreBande(facade, g, {
      liste,
      toutes: magasin.etat().paroles,
      base: T.base,
      amp: T.amp,
      photo: photo.hidden ? null : { x: 332, bas: top + 34 },
    });
    champ.setAttribute('data-champ', palette.mauve77);
    champ.setAttribute('data-matiere', m);
    champ.setAttribute('data-photo', '');
    bandeDessin.poser({ d: null, y: onde(T.base, T.amp), nature: palette.mauve77, instant: false, masquer: () => {} });
  }

  function peindreTraitCercle(): void {
    const H = T.base + T.amp + 40;
    const dpr = Math.max(2, Math.min(3, window.devicePixelRatio || 2));
    trait.width = Math.round(W * dpr);
    trait.height = Math.round(H * dpr);
    trait.style.width = `${String(W)}px`;
    trait.style.height = `${String(H)}px`;
    const g = trait.getContext('2d');
    if (!g) return;
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.clearRect(0, 0, W, H);
    peindreLigne(g, T.base, T.amp, ligneCercle());
    trait.setAttribute('data-trait', [T.base, T.amp, NATTRAIT.nuee, 'complet'].join(','));
  }
  const ligneCercle = (): Parameters<typeof peindreLigne>[3] => ({
    mode: 'complet',
    col: NATTRAIT.nuee,
    attend: false,
  });

  /** sortir du mode Cercle (une parole s'ouvre) : ce que le Cercle a posé est rendu */
  function quitterCercle(): void {
    cercle = null;
    fi.classList.remove('fi-cercle');
    fil.hidden = true;
    fil.innerHTML = '';
    tete.hidden = true;
    if (unMot.parentElement !== defile) defile.insertBefore(unMot, espace);
  }

  /** le nombre de mots sur la ligne « Un mot… » (C-257) : le total ; « +N » orange quand des mots d'autres ne sont pas encore vus (C-253) */
  function poserNombre(p: Parole): void {
    const ms = p.comments ?? [];
    const moi = moiNom();
    const neufs = ms.filter((m) => !m.vu && !/^moi$/i.test(String(m.by)) && m.by !== moi).length;
    nbMots.hidden = !ms.length;
    nbMots.textContent = neufs ? '+' + String(neufs) : String(ms.length);
    nbMots.classList.toggle('cm5-neufs', !!neufs);
  }

  /**
   * « LES MOTS », PUIS LA HAUTEUR DU CONTENU ET LA JONCTION : sous « Un mot… », la liste (mots.ts) ; la fiche défile dès que ce qui suit la ligne
   * d'état passe 748 pt (`ajusteLigne` : le bas + 12 + 84) ; la jonction (jonction.ts) se pose sur ce trait et cette hauteur.
   */
  function poserMots(p: Parole): void {
    const dy = parseFloat(unMot.style.translate.split(' ')[1] ?? '0') || 0;
    // les mots restent sous le rideau (« le trait se referme ») : la fiche garde sa hauteur, son défilement ne retombe pas
    const basMots = mots.poser(p.comments ?? [], dy);
    // sous le rideau, le prototype retire la liste (`inv()` de lot-S5) ; son titre reste
    const liste = defile.querySelector<HTMLElement>('#cm5Liste');
    if (liste) liste.style.visibility = instantF === 'referme' ? 'hidden' : '';
    let bas = 0;
    const R = defile.getBoundingClientRect();
    const k = R.width / defile.offsetWidth || 1;
    for (const e of defile.querySelectorAll<HTMLElement>('#cm5Liste, #cm5Titre, #cm5Ligne')) {
      const r = e.getBoundingClientRect();
      if (r.height) bas = Math.max(bas, (r.bottom - R.top) / k + defile.scrollTop);
    }
    if (basMots != null) bas = Math.max(bas, basMots);
    const hauteur = bas > 748 ? Math.ceil(bas + 12 + 84) : defile.clientHeight || 844;
    espace.style.height = `${String(hauteur)}px`;
    jonction.poser({ base: T.base, amp: T.amp, champ: CHAMP[nature(p)], hauteur });
  }

  /**
   * L'INSTANT (`cotes()` de lot-S5) : « le trait se referme » — tout se retire sous le rideau ; « juste après » (cadre 101) — les Noyaux à 388, la
   * phrase à 515 (21 pt, amande sur la terre), le titre à 546 (38 pt), « TENUE · À L’INSTANT » à 614 (et ce que le titre prend en plus d'une ligne).
   */
  function poserInstant(p: Parole): void {
    photo.hidden = !!instantF;
    fi.classList.toggle('inst-referme', instantF === 'referme');
    fi.classList.toggle('inst-apres', instantF === 'apres');
    if (instantF !== 'apres') return;
    noyaux.style.top = '388px';
    phrase.style.top = '515px';
    phrase.style.fontSize = '21px';
    titre.style.top = '546px';
    titre.textContent = p.title;
    titre.style.fontSize = '38px';
    const lh = parseFloat(getComputedStyle(titre).lineHeight) || 42;
    const hT = titre.offsetHeight;
    const dyT = hT > lh * 1.5 ? Math.round(hT - lh) : 0;
    etatL.textContent = ligneJusteApres(p);
    etatL.classList.add('fi-tenu');
    etatL.style.top = `${String(614 + dyT)}px`;
    const bas = 614 + dyT + etatL.offsetHeight;
    unMot.style.translate = `0 ${String(Math.max(0, bas - 692 + 8))}px`;
  }

  /** le bouton photo : 24 pt du bord droit, 8 pt au-dessus du haut de l'onde sous lui (moins l'épaisseur du trait), au plus 52 au-dessus d'elle en 349 (C-201) */
  function poserPhoto(): void {
    const y = onde(T.base, T.amp);
    let m = 1e9;
    for (let x = 330; x <= 368; x += 2) m = Math.min(m, y(x));
    const h = Math.max(5 * TRAIT_K, 6 * 1.15, 4.5 * 1.15);
    photo.style.top = `${String(Math.round(Math.min(y(349) - 52, m - h - 8 - 34)))}px`;
  }

  /** le « + » des membres : sur une parole que je fais, 26 pt après le dernier petit disque (« Toi » s'il n'y en a pas), centré sur lui */
  function poserPlus(recu: boolean): void {
    plusM.hidden = recu || instantF === 'referme';
    if (plusM.hidden) return;
    const ds = noyaux.querySelectorAll<HTMLElement>('.kr-wrap');
    const a = ds[ds.length - 1]!;
    const r = a.getBoundingClientRect();
    const f = fi.getBoundingClientRect();
    const k = f.width / fi.offsetWidth || 1;
    const gx = (r.right - f.left) / k + 26;
    // en points de la couche qui défile (le « + » y vit) : la fiche peut être défilée quand elle se repose (« juste après », C-311)
    const cy = (r.top - f.top) / k + r.height / k / 2 + defile.scrollTop;
    // la rangée déborde (plus de trois personnes) : le « + » serait hors de l'écran, sous le fondu — il ne paraît pas
    if (gx + 18 > 366) {
      plusM.hidden = true;
      return;
    }
    // sa hauteur : celle d'une capitale de la phrase, lue sur sa police rendue (le « A », `measureText` — elle suit la phrase à 21 pt de « juste
    // après ») ; l'encre commence 26 pt après le disque, la zone (44) centrée sur elle (C-242)
    const cs = getComputedStyle(phrase);
    const fs = parseFloat(cs.fontSize) || 19;
    const g = mesureur();
    g.font = `${cs.fontStyle} ${cs.fontWeight} ${String(fs)}px ${cs.fontFamily}`;
    const asc = g.measureText('A').actualBoundingBoxAscent;
    const cap = asc > 0 ? Math.round(asc * 4) / 4 : Math.round(fs * 0.7 * 4) / 4;
    const sv = plusM.querySelector('svg');
    if (sv) {
      sv.setAttribute('width', String(cap));
      sv.setAttribute('height', String(cap));
    }
    plusM.style.left = `${String(Math.round((gx + cap / 2 - 22) * 4) / 4)}px`;
    plusM.style.top = `${String(Math.round((cy - 22) * 4) / 4)}px`;
  }

  /** un prénom sous son disque : entier s'il tient dans 70 pt (Gilbert 700 12), sinon six lettres et « . » (`_noms.court`) */
  function court(nom: string): string {
    const g = mesureur();
    g.font = '700 12px Gilbert, system-ui';
    if (g.measureText(nom).width <= 70) return nom;
    const L = Array.from(nom);
    return L.length > 6 ? L.slice(0, 6).join('') + '.' : nom;
  }

  function morceau(m: Morceau): string {
    if ('t' in m) return esc(m.t);
    if ('nom' in m)
      return '<b><span class="nom-lien" data-nom="' + esc(m.nom) + '" role="link">' + esc(m.nom) + '</span></b>';
    const mot = '+\u00a0' + String(m.plus) + '\u00a0personnes';
    return (
      '<button type="button" class="fi-plus" aria-expanded="false" aria-label="' +
      esc(mot) +
      ' : voir toute la liste">' +
      esc(mot) +
      '</button>'
    );
  }

  /**
   * LES COTES SOUS LE TRAIT (`ecran()` et `_ficheCotes` du prototype) — le rythme se mesure depuis L'ENCRE du trait (son point bas exact,
   * base + 0,45·amp, plus sa demi-épaisseur) : 26 d'encre entre deux blocs, 20 dans le bloc de la promesse ; l'agrandissement des faces
   * (v96, × 1,12) se garde à l'encre (`_encreSup`) ; la ligne d'état descend du JAMBAGE de la dernière ligne du titre et de l'accent d'une
   * capitale (v18). Le titre : 42 pt, réduit d'un point à la fois jusqu'à tenir sur une ligne (plancher 38) ; long, deux lignes, trois au
   * plus (jusqu'à 24), puis « … » (v46, C-244).
   */
  function coter(aTrace: boolean): void {
    const yEncre = T.base + 0.45 * T.amp + 5;
    const dyTrait = Math.ceil(28 * Math.max(0, TRAIT_K - 1.05)) / 2;
    let yNoyau: number;
    if (aTrace) {
      const yTrace = Math.round(yEncre + 25) + dyTrait;
      geste.style.top = `${String(yTrace)}px`;
      yNoyau = yTrace + 44;
    } else yNoyau = Math.round(yEncre + 27) + dyTrait;
    noyaux.style.top = `${String(yNoyau)}px`;
    const yQui = yNoyau + 128 + Math.round(encre(14).bas + encre(23).haut);
    phrase.style.top = `${String(yQui)}px`;
    phrase.style.removeProperty('font-size');
    let yTitre = Math.round((yQui + 23 * 1.1 + 11.9 + encre(23).bas + encre(42).haut) * 10) / 10;
    // la phrase sur deux lignes et plus : le titre descend de ce qu'elle prend en plus d'une ligne
    const hq = phrase.offsetHeight;
    if (hq > 25.3 * 1.5) yTitre = Math.round(yTitre + hq - 25.3);
    titre.style.top = `${String(yTitre)}px`;
    const fs = ajusterTitre();
    const yEtat =
      Math.round(yTitre + titre.offsetHeight + 26.3) +
      Math.round(jambageDernier(titre)) +
      Math.ceil(encre(fs).bas) +
      Math.round(accentHaut(etatL, 13.5));
    etatL.style.top = `${String(yEtat)}px`;
    // « Un mot… » (692 → 748) garde 8 pt sous la ligne d'état (lot-V181B-TEXTES, `ajusteLigne`) ; déplié ou modifié, sa place est figée
    const bas = yEtat + etatL.offsetHeight;
    unMot.style.translate = `0 ${String(dyFige ?? Math.max(0, bas - 692 + 8))}px`;
  }

  /**
   * C-244 — LE DÉPLIAGE (`bascule` de lot-V181B-TEXTES) : le titre se découvre en entier (de sa hauteur repliée à sa hauteur entière, découpé),
   * et ce qui le suit glisse à sa nouvelle place, d'un seul mouvement (360 ms, aller-retour quadratique) ; « Un mot… » garde l'air qu'il avait
   * sous la ligne d'état. Réduire les animations : posé d'un coup.
   */
  function deplier(): void {
    if (!courant) return;
    const R = defile.getBoundingClientRect();
    const k = R.width / defile.offsetWidth || 1;
    const SUIT = [etatL, ...defile.querySelectorAll<HTMLElement>('#cm5Ligne, #cm5Titre, #cm5Liste')];
    const avant = SUIT.map((e) => e.getBoundingClientRect().top);
    const h0 = titre.getBoundingClientRect().height / k;
    const dy0 = parseFloat(unMot.style.translate.split(' ')[1] ?? '0') || 0;
    const air = 692 + dy0 - (etatL.offsetTop + etatL.offsetHeight);
    titreDeplie = true;
    dyFige = null;
    poser(courant);
    dyFige = Math.max(0, etatL.offsetTop + etatL.offsetHeight - 692 + Math.max(8, air));
    unMot.style.translate = `0 ${String(dyFige)}px`;
    poserMots(courant);
    const h1 = titre.getBoundingClientRect().height / k;
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const dep = SUIT.map((e, i) => (avant[i]! - e.getBoundingClientRect().top) / k);
    const H = horloge();
    const t0 = H.maintenant();
    const doux = (u: number): number => (u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2);
    const f = (): void => {
      const u = Math.min(1, (H.maintenant() - t0) / 360);
      const v = 1 - doux(u);
      SUIT.forEach((e, i) => {
        e.style.transform = u < 1 && dep[i] ? `translateY(${(dep[i] * v).toFixed(2)}px)` : '';
      });
      titre.style.clipPath = u < 1 && h1 > h0 ? `inset(0 0 ${((h1 - h0) * v).toFixed(2)}px 0)` : '';
      if (u < 1) H.image(f);
    };
    f();
  }

  /** ce que l'agrandissement des faces (v96, × 1,12) ajoute à l'encre au-dessus et au-dessous d'une ligne (`_encreSup`) */
  function encre(fs: number): { haut: number; bas: number } {
    const d = fs * (1.12 - 1);
    return { haut: d * 0.8, bas: d * 0.62 };
  }

  function ajusterTitre(): number {
    const lignes = (f: number): number => Math.round(titre.offsetHeight / (f * 1.02));
    delete titre.dataset['coupe'];
    let fs = 42;
    titre.style.fontSize = `${String(fs)}px`;
    while (fs > 38 && titre.offsetHeight > fs * 1.35) {
      fs -= 1;
      titre.style.fontSize = `${String(fs)}px`;
    }
    if (lignes(fs) > 2) {
      let ok = false;
      for (let lim = 2; lim <= 3 && !ok; lim++)
        for (let f = fs; f >= 24; f--) {
          titre.style.fontSize = `${String(f)}px`;
          if (lignes(f) <= lim) {
            fs = f;
            ok = true;
            break;
          }
        }
      if (!ok) {
        fs = 24;
        titre.style.fontSize = '24px';
        titre.dataset['coupe'] = '1';
      }
      // déplié ou en modification : le titre entier, à la taille du replié (C-244) ; sinon coupé par « … » à la troisième ligne
      if (!ok && courant && !titreDeplie && !titreEdite) {
        const long = courant.title;
        let lo = 0;
        let hi = long.length;
        while (lo < hi) {
          const md = (lo + hi + 1) >> 1;
          titre.textContent = long.slice(0, md).replace(/\s+$/, '') + '\u2026';
          if (lignes(fs) <= 3) lo = md;
          else hi = md - 1;
        }
        titre.textContent = long.slice(0, lo).replace(/\s+$/, '') + '\u2026';
      }
    }
    return fs;
  }

  /** la profondeur d'encre de la dernière ligne d'un texte sous sa ligne de base (`_jambageDernier`) */
  function jambageDernier(e: HTMLElement): number {
    const n = e.firstChild;
    if (!n || n.nodeType !== 3) return 0;
    const v = n.nodeValue ?? '';
    const rg = document.createRange();
    let bas = -1e9;
    const L: Array<[number, string]> = [];
    for (let i = 0; i < v.length; i++) {
      rg.setStart(n, i);
      rg.setEnd(n, i + 1);
      const r = rg.getClientRects()[0];
      if (!r) continue;
      L.push([r.top, v.charAt(i)]);
      if (r.top > bas) bas = r.top;
    }
    const t = L.filter((x) => Math.abs(x[0] - bas) < 2)
      .map((x) => x[1])
      .join('')
      .trim();
    if (!t) return 0;
    const c = getComputedStyle(e);
    const g = mesureur();
    g.font = `${c.fontStyle} ${c.fontWeight} ${c.fontSize} ${c.fontFamily}`;
    return Math.max(0, g.measureText(t).actualBoundingBoxDescent);
  }

  /** ce que les accents d'une ligne en capitales ajoutent au-dessus de la hauteur de capitale (`_accentHaut`) */
  function accentHaut(e: HTMLElement, fs: number): number {
    const t = (e.textContent ?? '').trim().toUpperCase();
    if (!t) return 0;
    const c = getComputedStyle(e);
    const g = mesureur();
    g.font = `${c.fontStyle} ${c.fontWeight} ${String(fs)}px ${c.fontFamily}`;
    return Math.max(0, g.measureText(t).actualBoundingBoxAscent - g.measureText('HTE').actualBoundingBoxAscent);
  }

  let cvMesure: CanvasRenderingContext2D | null = null;
  function mesureur(): CanvasRenderingContext2D {
    cvMesure ??= document.createElement('canvas').getContext('2d')!;
    return cvMesure;
  }

  // ── TENIR (tenir.ts) ──
  const tenir = monterTenir({
    fi: defile,
    mot: geste,
    trait: () => ({ base: T.base, amp: T.amp }),
    actif: () => !!courant && !fi.hidden && !instantF && courant.status !== 'tenu',
    doigt(x) {
      doigtX = x;
      if (courant) peindreTrait(courant);
    },
    tenir(trace, referme) {
      if (!courant) return 'rien';
      // l'instant est armé AVANT que la parole change (le prototype l'arme en capture du clic « tenue ») : la fiche se repose directement dans
      // « le trait se referme » (la fiche tenue ordinaire n'est jamais peinte pour rien)
      if (referme) instantF = 'referme';
      const r = magasin.tenir(courant.id, trace, Date.now());
      if (r === 'tenue') haptique('tenir');
      if ((r !== 'tenue' || !referme) && instantF) {
        instantF = null;
        if (courant) poser(courant);
      }
      return r;
    },
    phrase: () => (courant ? phraseTenue(courant) : ''),
    apres() {
      instantF = 'apres';
      if (courant) poser(courant);
    },
  });

  // ── LES MOTS ET LA JONCTION (mots.ts, jonction.ts) ──
  const mots = monterMots({
    dans: defile,
    moi: () => ({ nom: moiNom(), graine: magasin.etat().utilisateur.graine ?? 0 }),
    tous: () => {
      const S = new Set<string>();
      const aj = (v: string | null | undefined): void => {
        for (const x of String(v ?? '').split(/\s*[,·]\s*|\s+et\s+/)) {
          const t = x.trim();
          if (t && !/^(moi|le groupe|tout le monde|toi)$/i.test(t)) S.add(t);
        }
      };
      for (const q of magasin.etat().paroles) {
        aj(q.who);
        aj(q.from);
        aj(typeof q.suite?.['avec'] === 'string' ? q.suite['avec'] : '');
        for (const c of q.comments ?? []) aj(c.by);
      }
      aj(moiNom());
      return [...S];
    },
    maintenant: () => Date.now(),
  });
  const jonction = monterJonction({
    defile,
    champ,
    fond: () => getComputedStyle(fi).backgroundColor,
    zone: () => defile.querySelector<HTMLElement>('#tenirZone'),
    ligne(g, base, amp) {
      if (courant) peindreLigne(g, base, amp, optionsLigne(courant));
      else if (cercle) peindreLigne(g, base, amp, ligneCercle());
    },
  });

  const titreCtl = monterTitre({
    defile,
    titre,
    long: () => courant?.title ?? null,
    actif: () => !!courant && !fi.hidden && !fi.classList.contains('fi-bas') && !instantF && !tenir.etat().geste,
    coupe: () => titre.dataset['coupe'] === '1',
    deplie: () => titreDeplie,
    deplier,
    entier(on) {
      if (on) {
        dyFige ??= parseFloat(unMot.style.translate.split(' ')[1] ?? '0') || 0;
        titreEdite = true;
      } else {
        titreEdite = false;
        if (!titreDeplie) dyFige = null;
      }
    },
    recoter() {
      if (!courant) return;
      coter(!geste.hidden);
      poserMots(courant);
    },
    renommer(v) {
      if (courant) magasin.renommer(courant.id, v, Date.now());
    },
    retracer() {
      chargerTrace().trace(titre, null, {});
    },
  });

  // ── ÉCRIRE UN MOT (saisie-mot.ts, lot 3b-2) : la ligne « Un mot… » s'ouvre au toucher ; le mot s'écrit, la liste se repose (l'abonné) ──
  const saisieMot = monterSaisieMot({
    fi,
    defile,
    ligne: unMot,
    mot: unMotTxt,
    nb: nbMots,
    actif: () => !!courant && !fi.hidden && !fi.classList.contains('fi-bas') && !instantF,
    envoyer: (t) => {
      if (courant) magasin.ajouterMot(courant.id, t, moiNom(), Date.now());
    },
  });

  // ── LE BOUTON PHOTO (photo.ts, lot 3b-3) : son menu ; la photo ou la dalle d'origine, et la bande se repeint ──
  const menuPhoto = monterMenuPhoto({
    hote: defile,
    bouton: photo,
    magasin,
    parole: () => (courant && !fi.hidden && !fi.classList.contains('fi-bas') && !instantF ? courant : null),
    repeindre: () => {
      if (courant) peindreChamp(courant);
    },
    // le mode dessin (le même que la page +) : il habille le dessin de la parole ; POSER le pose dans la bande (la photo retirée, v140)
    dessiner: () => {
      const p = courant;
      if (!p) return;
      modeDessin.ouvrir({
        lire: () => (courant ? dessinDe(courant) : null),
        ecrire: (d) => {
          if (courant) magasin.dessin(courant.id, d);
        },
        nature: nature(p),
        corps: couleurDe(fi),
        apres: (pose) => {
          const q = courant;
          if (q && pose) magasin.dessin(q.id, dessinDe(q), true);
          else if (q) peindreChamp(q);
        },
      });
    },
    aDessin: (p) => {
      const d = dessinDe(p);
      return !!d && (dessinPose(d) || d.traits.length > 0);
    },
    retirerDessin: () => {
      if (courant) magasin.dessin(courant.id, null);
    },
  });
  const modeDessin = modeDessinPartage({
    dv,
    h: horloge(),
    clair: () => dv.classList.contains('light'),
    tons: () => facade.tonsStudio(),
  });

  /** l'image entière du dessin posé (la vue « en entier »), refaite quand le dessin change */
  let vueDessin: { cle: string; src: string } | null = null;
  // ── LA PHOTO EN ENTIER, ET CADRÉE AU DOIGT (entier.ts, lot 3b-4) : sur la bande, au repos, rien par-dessus ──
  const ficheLibre = (): boolean =>
    !!courant &&
    !fi.hidden &&
    !fi.classList.contains('fi-bas') &&
    !instantF &&
    !peauf.ouvert() &&
    !saisieMot.ouvert() &&
    !menuPhoto.ouvert() &&
    !modeDessin.ouvert();
  entier = monterEntier({
    dv,
    bande: champ,
    surface: (t) => t === champ || t === defile || t === fi,
    photo: () => (courant && ficheLibre() ? photoDe(courant) : null),
    dessin: () => {
      const d = courant && ficheLibre() ? dessinDe(courant) : null;
      if (!d || !dessinVu(d)) return null;
      const cle = JSON.stringify([d.fond, d.h, d.poses.length, JSON.stringify(d.poses).length]);
      if (vueDessin?.cle !== cle) vueDessin = { cle, src: dessinEntier(d, 3).toDataURL('image/png') };
      return vueDessin.src;
    },
    cadre: () => (cadreVif ?? (courant?.suite?.['photoCadre'] as Cadre | undefined)) || null,
    centre: () => (boitePhoto ? { x: boitePhoto.x + boitePhoto.w / 2, y: boitePhoto.y + boitePhoto.h / 2 } : null),
    cadrer: (c, fini) => {
      if (!courant) return;
      cadreVif = fini ? null : c;
      if (fini) magasin.cadrer(courant.id, c);
      else peindreChamp(courant);
    },
  });

  // ── PEAUFINER (peaufiner.ts, lot 3b-1) : la barre l'ouvre par-dessus la fiche, la fiche reste dessous ──
  const peauf = monterPeaufinerFiche({
    fi,
    barre: barreTog,
    chevron: barreChev,
    magasin,
    parole: () => courant,
    couleur: (p) => facade.couleurDalle(p),
    // SUPPRIMER (`_v16SupprimerPromi`, v187) : la feuille ; « Supprimer » efface la parole (sa pierre tombale), la fiche se ferme (l'abonné
    // ci-dessous : la parole n'est plus là), sa dalle quitte la Toile ; « Annuler » la rend, 5 s
    supprimer: (p) => {
      const ch = !!p.chiche;
      confirmer(dv, {
        titre: ch ? TXT.supprimerChiche : TXT.supprimerPromi,
        texte: `« ${p.title} » quitte ta Toile.`,
        oui: TXT.supprimer,
        non: TXT.garder,
        faire: () => {
          const x = magasin.effacer(p.id);
          if (!x) return;
          annulable(dv, {
            mot: ch ? TXT.chicheSupprime : TXT.promiSupprime,
            annuler: TXT.annuler,
            defaire: () => {
              magasin.deterrer(x);
            },
          });
        },
      });
    },
  });
  // le « + » des membres (C-254) : Peaufiner s'ouvre sur les personnes de la parole (sa rangée dépliée, le panneau glissé jusqu'à elle)
  surToucher(plusM, () => {
    if (!courant || plusM.hidden) return;
    peauf.ouvrirPersonnes();
  });

  /** ce qu'une fiche ouverte (parole ou Cercle) laisse derrière elle est refermé avant d'en ouvrir une autre */
  function remettre(): void {
    menuPlanter.fermer();
    peauf.fermer(false);
    saisieMot.fermer();
    menuPhoto.fermer(false);
    entier?.fermer();
    cadreVif = null;
    if (modeDessin.ouvert()) modeDessin.sortir(false);
    tenir.arreter();
    titreCtl.sortir(true);
    instantF = null;
    doigtX = null;
    deplie = false;
    titreDeplie = false;
    titreEdite = false;
    dyFige = null;
    // une fiche se rouvre en haut (v182b)
    defile.scrollTop = 0;
  }

  function ouvrir(id: number): void {
    const p = magasin.etat().paroles.find((q) => q.id === id);
    if (!p || p.draft) return;
    remettre();
    quitterCercle();
    courant = p;
    montrer(() => {
      poser(p);
    });
  }

  function ouvrirCercle(k: string): void {
    if (!(k in magasin.etat().cercles)) return;
    remettre();
    courant = null;
    cercle = k;
    montrer(() => {
      poserCercle(k);
    });
  }

  /** montrée AVANT d'être posée (en bas, invisible) : les cotes se lisent sur le rendu (le titre, la phrase, les disques) ; puis elle monte */
  function montrer(poserLa: () => void): void {
    if (finFermeture != null) horloge().annuleMinuteur(finFermeture);
    finFermeture = null;
    fi.classList.add('fi-bas');
    // un écran qui s'ouvre passe devant ceux qui sont ouverts (l'Index, le Fil, la fiche d'une personne : même z) — encore caché, rien ne bouge
    if (dv.lastElementChild !== fi) dv.appendChild(fi);
    fi.hidden = false;
    poserLa();
    // la feuille de style relue avant de retirer `fi-bas` : la transition part de l'état d'en bas
    fi.getBoundingClientRect();
    fi.classList.remove('fi-bas');
    // arrivée, elle couvre l'appareil : l'accueil dessous ne se voit plus et ne prend plus le doigt (base.css, `.couvert` — comme la page +)
    finOuverture = horloge().minuteur(() => {
      finOuverture = null;
      fi.classList.add('couvre');
      dv.classList.add('couvert');
    }, 420);
  }
  let finOuverture: number | null = null;

  let finFermeture: number | null = null;
  /** elle redescend (0,4 s), puis se cache */
  function fermer(): void {
    if (fi.hidden || fi.classList.contains('fi-bas')) return;
    menuPlanter.fermer();
    peauf.fermer(false);
    saisieMot.fermer();
    menuPhoto.fermer(false);
    entier?.fermer();
    cadreVif = null;
    if (modeDessin.ouvert()) modeDessin.sortir(false);
    tenir.arreter();
    titreCtl.sortir(true);
    // C-253 : les mots que la fiche a montrés sont vus, quand on la quitte (les mots neufs perdent leur pastille, « +N » redevient le total)
    const vus = mots.vus();
    if (courant && vus.length) magasin.motsVus(courant.id, vus);
    courant = null;
    cercle = null;
    if (finOuverture != null) horloge().annuleMinuteur(finOuverture);
    finOuverture = null;
    // l'accueil redevient visible dessous pendant qu'elle redescend
    fi.classList.remove('couvre');
    dv.classList.remove('couvert');
    fi.classList.add('fi-bas');
    finFermeture = horloge().minuteur(() => {
      finFermeture = null;
      fi.hidden = true;
    }, 420);
  }

  // C-049 : une seule source de vérité — la parole ouverte qui change (tenue, renommée, une part tracée) se repose ; effacée, la fiche se ferme
  magasin.abonner((e, action) => {
    // le Cercle ouvert : il se repose à chaque changement (ses paroles, son nom, ses membres) ; dissous, la fiche se ferme
    if (cercle && !fi.hidden) {
      if (!(cercle in e.cercles)) fermer();
      else poserCercle(cercle);
      return;
    }
    if (!courant || fi.hidden) return;
    const p = e.paroles.find((q) => q.id === courant!.id);
    if (!p) {
      fermer();
      return;
    }
    if (p === courant) return;
    courant = p;
    // un mot envoyé (3b-2) : seuls le nombre et la liste changent — la fiche ne se repose pas (sur une parole tenue, le premier mot change son
    // trait, 362 → 286 : elle sautait de 76 pt, un changement sec, C-271 ; le prototype ne la repose pas non plus) ; rouverte, elle prend sa place
    if (action === 'ajouterMot') {
      poserNombre(p);
      poserMots(p);
      return;
    }
    poser(p);
    peauf.reposer();
  });

  nav.poser('fiche', (arg) => {
    ouvrir(Number(arg));
  });
  nav.poser('cercle', (arg) => {
    ouvrirCercle(String(arg));
  });

  return {
    ouvrir,
    ouvrirCercle,
    fermer,
    etat: () => ({
      id: courant?.id ?? null,
      cercle,
      base: T.base,
      amp: T.amp,
      mode: T.mode,
      instant: instantF,
      jonction: jonction.etat(),
    }),
    tenir: () => tenir.etat(),
  };
}
