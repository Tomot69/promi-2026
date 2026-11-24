/**
 * LA PAGE + (lot 2a) — Promi, Chiche, Cercle : le plateau (le mot de la nature, le X), le champ de la nature et la dalle d'avance du moteur
 * (C-241), l'horizon BAS et rien du trait tant que la parole n'est pas validée (C-213, C-229), la phrase-pastilles (le verbe et son cycle
 * pour un Promi), les exemples des pastilles vides (`lot-EXEMPLES-V20`, C-312), la saisie du titre et du nom, le choix des personnes
 * (`lot-GENS`, C-269, C-122), le rail du pinceau (C-196), « garder de côté » (C-149), la barre Peaufiner au repos.
 * Le prototype rendu (v214b) est la référence ; ses règles de composition sont relues dans app.html (`lot-S3-page-plus` : `ecran`, `cotes`,
 * `trait`, `hautBouton` ; `lot-V172-INVITE` : `hzCible`) et réécrites ici.
 *
 * Et (fin du 2a) : le choix des personnes d'un Cercle (« Moi » en tête, ses tailles) ; la mise en page de saisie (`pp-ouvert` : l'onde à
 * 144, la phrase à 230, « DÉJÀ PROMIS ») et le mouvement qui y mène et qui en revient (Q598, C-234 : 360 ms, jamais d'un coup) ; le champ
 * « un prénom… » (C-122) ; le panneau Peaufiner (C-134, C-220) ; le menu du bouton photo (v117, v132) et la photo importée.
 *
 * Ce que 2a ne fait pas (2b, 2c) : le trait et sa genèse, la plantation, la naissance et le vol de la dalle, les textes longs, la première
 * lettre, le détracé des changements de mots (la phrase se recompose : C-271 au 2c) ; le dessin (son lot) ; les choix DANS Peaufiner
 * (l'échéance, le Cercle, les pièces jointes, les membres) ; la phrase des murs (lot 8).
 *
 * L'état de la page (la phrase qu'on écrit) n'appartient qu'à elle ; ce qui se garde passe par le magasin (le tirage des exemples, le gardé
 * de côté). Son temps est celui de l'horloge unique ; le moteur, par la façade.
 */
import './page-plus.css';
import type { Facade } from '../../moteur/facade.ts';
import type { Magasin } from '../../etat/magasin.ts';
import type { Navigation } from '../../navigation/navigation.ts';
import type { Brouillon } from '../../donnees/schema.ts';
import { horloge } from '../../animation/horloge.ts';
import { chargerTrace, copieA, detracerCopie, remplacer, type ControleTrace } from '../../animation/trace/trace.ts';
import { masqueFlaques, passageFlaques, type ControlePassage } from '../../animation/flaques/passage.ts';
import { palette } from '../../design/jetons.ts';
import {
  EXEMPLES,
  EXEMPLES_FIXES,
  PRENOMS_EXEMPLE,
  TEXTES_PAGE_PLUS as T,
  type TypeExemple,
} from '../../textes/page-plus.ts';
import { variante } from '../../metier/exemples.ts';
import { elision } from '../../metier/elision.ts';
import { champSansEmoji } from '../../metier/emoji.ts';
import { PINCEAUX } from './pinceaux.ts';
import { avecAlpha, el, esc, poserCroix, surToucher, SVG_PHOTO } from '../commun.ts';
import { creerPeauf } from '../peaufiner/briques.ts';
import { dateQuand } from '../../metier/echeance.ts';
import { basOnde, cheminOnde, onde, type Onde } from './onde.ts';
import { NATTRAIT, peindreTrait } from './trait.ts';
import { planteNait } from './naissance.ts';
import { creerContinu } from './continu.ts';
import { creerDouceur } from './douceur.ts';
import {
  creerModeDessin,
  couleurDe,
  dessinEntier,
  dessinPose,
  DESSIN,
  type Dessin,
  type ModeDessin,
} from './dessin.ts';

export type Nature = 'promi' | 'chiche' | 'nuee';
export type Sens = 'soi' | 'faire' | 'demander';

/** ce que la page écrit (le `_phrase` du prototype, et ses voisins) */
export interface PhrasePage {
  nat: Nature;
  sens: Sens;
  titre: string;
  /** à qui (Promi), qui ose (Chiche) */
  qui: string[];
  /** avec qui (Chiche) */
  avec: string[];
  /** le nom d'un Cercle, ses membres */
  nom: string;
  membres: string[];
  pinceau: string;
  /** C-304 : la place du destinataire touchée sans personne passe à « moi » (entre pointillés) */
  moi: boolean;
  /** Peaufiner : la note ; l'échéance (son mot) */
  note: string;
  ech: string;
  /** l'échéance a été choisie (le prototype ne coche une pastille qu'une fois choisie : « un jour » par défaut n'est pas coché) */
  echChoisie: boolean;
  /** l'échéance choisie (Peaufiner, AVANT) : des jours (null : « un jour », aucune) et la date du calendrier (« une date… ») */
  due: number | null;
  dueISO: string | null;
  /** le Cercle où l'on plante (Peaufiner, DANS UN CERCLE) — sa clé */
  cercle: string | null;
  /** les pièces jointes (leurs noms) */
  fichiers: string[];
  /** la photo importée (une adresse `data:`), qui remplace la dalle dans la bande (lot-PHOTO) */
  photo: string | null;
  /** le dessin (C-042) : il REMPLACE la dalle ou la photo dans la bande (v128) ; la photo importée le retire, le dessin posé retire la photo (v140) */
  dessin: Dessin | null;
}

export interface PagePlus {
  racine: HTMLElement;
  ouvrir(nat: Nature): void;
  /** un gardé de côté rouvert (sa porte : l'Index, lot 3) — faux s'il n'existe pas */
  reprendre(id: number): boolean;
  fermer(): void;
  ouverte(): boolean;
  /** pour les tests : la phrase, la mise en page (en pt du cadre 390), le choix ouvert */
  etat(): {
    phrase: PhrasePage;
    base: number;
    amp: number;
    hz: number;
    lignes: number;
    taille: number;
    choix: string | null;
    gardeActif: boolean;
    exemples: Partial<Record<TypeExemple, string>>;
    /** la saisie ouverte (le titre, le nom), Peaufiner ouvert, le menu photo ouvert, la zone « un prénom… » active, un mouvement en cours */
    saisie: string | null;
    peauf: boolean;
    menu: boolean;
    ajout: boolean;
    mouvement: boolean;
    /** ce qui bouge encore (le mouvement du clavier, une transition de mot, un glissement) : pour nommer un mouvement qui ne finit pas */
    mouvementDe: string[];
    /** C-209, C-213, C-229 : l'invite à tracer — née (le trait, le libellé), en train de partir, l'horizon bas, le premier toucher du trait */
    invite: { visible: boolean; sortie: boolean; haut: boolean; anim: boolean; touche: boolean };
    /** le mode dessin ouvert (son outil, sa couleur, son fond…), sinon null */
    dessin: ReturnType<ModeDessin['etat']>;
  };
  detruire(): void;
}

const CHAMP: Record<Nature, string> = { promi: palette.bleu45, chiche: palette.framboise54, nuee: palette.mauve77 };
const NATURES: readonly Nature[] = ['promi', 'chiche', 'nuee'];
/** C-184, v164b : le trait × 1,3, ses points × 1,15 — le pas du mot et de la phrase (`--pp-dyt`) en découle : ⌈14 × (K − 1,05)⌉ / 2 */
const TRAIT_K = 1.3;
const TRAIT_PTS = 1.15;
const DT = Math.ceil(14 * Math.max(0, TRAIT_K - 1.05)) / 2;
/** v150, v162 (C-158, C-183) : la phrase d'un Chiche remonte de 10 pt, celle d'un Cercle de 31 */
const DY_PHRASE: Record<Nature, number> = { promi: 0, chiche: -10, nuee: -31 };
/** C-229 : pas prête, l'horizon est 40 pt plus bas que sa place, jamais à moins de 12 pt de l'encre de la phrase */
const HZ_BAS = 40;
const HZ_AIR = 12;
/** §2.8 (v20, v115) : l'exemple passe à la ligne plutôt que de réduire la phrase sous 28 */
const PLANCHER_PH = 28;
/** la grammaire du lien « garder de côté » : son encre est 0,5 pt sous sa boîte (`INK_LIEN`) ; le rail se pose à mi-chemin */
const INK_LIEN = 0.5;
/** C-134 (v146) : un glissement de 220 pt vers le bas referme Peaufiner, un de 60 pt non — le seuil est entre les deux */
const SEUIL_GLISSE = 120;

const SVG_BASCULE =
  '<svg viewBox="0 0 22 22" width="17" height="17" aria-hidden="true"><path d="M3 8h16" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><path d="M15.4 4.6 L19 8 L15.4 11.4" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M19 15H3" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><path d="M6.6 11.6 L3 15 L6.6 18.4" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
const SVG_PLUS =
  '<svg viewBox="0 0 10 10" aria-hidden="true"><path class="h" d="M0 5 H10"/><path class="v" d="M5 0 V10"/></svg>';
const SVG_X =
  '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 2 L10 10 M10 2 L2 10" fill="none" stroke-width="2" stroke-linecap="round"/></svg>';

export function monterPagePlus(facade: Facade, magasin: Magasin, nav: Navigation): PagePlus {
  const h = horloge();
  const dv = facade.appareil();

  // ── la feuille ──
  const cs = el('div', { id: 'createSheet', class: 'pp', role: 'dialog' });
  cs.hidden = true;
  const cv = el('canvas', { id: 'csTrameCv', 'aria-hidden': 'true' });
  const plateau = el('div', { class: 'enh' });
  const mot = el('div', { class: 'cs-mark enh-t' });
  const croix = el('div', { class: 'closeb', role: 'button', 'aria-label': T.fermer, 'data-close': '' });
  const croixG = el('span', { class: 'cb-mot' });
  croixG.textContent = T.fermerGlyphe;
  croix.appendChild(croixG);
  plateau.append(mot, croix);
  const nid = el('div', { class: 'ph-photo-nid' });
  const photo = el('button', { type: 'button', class: 'ph-photo-btn', 'aria-label': T.photo });
  photo.innerHTML = SVG_PHOTO;
  photo.style.backgroundColor = avecAlpha(palette.brun09, 0.18);
  nid.appendChild(photo);
  const phrase = el('div', { id: 'csPhrase', class: 'pp-phrase' });
  const txt = el('div', { class: 'ph-txt' });
  const choixHote = el('div', { id: 'csChoix', class: 'ph-choix' });
  phrase.append(txt, choixHote);
  const pinceau = el('div', { id: 'csPinceau', 'data-glisse': '' });
  const rail = el('div', { id: 'csPinceauRail', class: 'pc-rail' });
  pinceau.appendChild(rail);
  const garder = el('div', { class: 'pp-garder inactif', role: 'button', 'aria-disabled': 'true' });
  garder.textContent = T.garder;
  const barre = el('div', { id: 'csBotBar', role: 'button', 'aria-label': T.peaufiner });
  const barreLab = el('span', { class: 'cbb-lab' });
  barreLab.textContent = T.peaufiner;
  const barreChev = el('span', { class: 'cbb-chev', 'aria-hidden': 'true' });
  barreChev.textContent = T.chevron;
  barre.append(barreLab, barreChev);
  const saisie = el('input', {
    class: 'ph-in',
    id: 'phIn',
    type: 'text',
    enterkeyhint: 'done',
    autocomplete: 'off',
    'aria-label': T.titresChoix.titre,
    // le champ est caché (la phrase EST la saisie, C-004) : il s'ouvre en touchant la pastille du titre ou du nom — il le déclare
    // (redteam_champs y passe par cette porte)
    'data-porte': '.pp-phrase .ph-m[data-ph="titre"], .pp-phrase .ph-m[data-np="nom"]',
  });
  saisie.style.cssText =
    'position:absolute;left:0;top:0;width:1px;height:1px;opacity:0;border:0;padding:0;margin:0;pointer-events:none;font-size:16px';
  // la photo importée : sa couche, au-dessus du champ, découpée par l'onde (lot-PHOTO : elle remplace la dalle, même boîte, en couverture)
  const photoCv = el('canvas', { id: 'csPhotoCv', 'aria-hidden': 'true' });
  // le champ de fichier : jamais hors cadre (`display:none`, lot-PHOTO) — il s'ouvre DANS le geste qui le demande
  const photoIn = el('input', { type: 'file', accept: 'image/*', class: 'ph-photo-in', 'aria-hidden': 'true' });
  // « DÉJÀ PROMIS » : sous la phrase, pendant la saisie d'un titre
  const deja = el('div', { class: 'ppo-dejas' });
  deja.hidden = true;
  // un toucher sur un mot déjà promis ne retire pas le clavier (le focus reste au champ)
  deja.addEventListener('mousedown', (ev) => {
    ev.preventDefault();
  });
  phrase.appendChild(deja);
  // C-122 : le champ (invisible) du prénom qu'on écrit dans la zone en pointillés
  const gnIn = el('input', {
    type: 'text',
    id: 'gnSaisie',
    class: 'gn-saisie',
    autocomplete: 'off',
    autocorrect: 'off',
    autocapitalize: 'words',
    spellcheck: 'false',
    enterkeyhint: 'done',
    maxlength: '24',
    'aria-label': T.prenom,
  });
  // il n'existe pour la page que pendant qu'on écrit un prénom (hors de là, aucun champ sans porte : redteam_champs)
  gnIn.hidden = true;
  // le panneau Peaufiner (lot-S2 : la page de réglages de la page +, le MÊME bloc que la fiche)
  const peauf = el('div', { id: 'csPeauf', class: 'dpd-corps', role: 'region', 'aria-label': T.peaufiner });
  peauf.hidden = true;
  // le départ du trait, sur SA couche tant qu'il clignote (le prototype : `#ppDepart`) ; le libellé « trace pour … » (`.pp-trace`)
  const departCv = el('canvas', { id: 'ppDepart', 'aria-hidden': 'true' });
  const lib = el('div', { class: 'pp-trace' });
  lib.hidden = true;
  cs.append(cv, departCv, photoCv, phrase, pinceau, garder, peauf, barre, plateau, nid, saisie, gnIn, photoIn, lib);
  // C-129 : aucun emoji n'entre (le titre, le nom, un prénom ; la note de Peaufiner aussi, plus bas)
  champSansEmoji(saisie);
  champSansEmoji(gnIn);
  for (const p of PINCEAUX) {
    const b = el('button', { type: 'button', class: 'pc-t' + (p.libre ? '' : ' pc-mur'), 'data-t': p.nom });
    const e = el('span', { class: 'pc-e' });
    if (p.dessin)
      e.innerHTML = `<svg width="60" height="11.7" viewBox="0 0 60 11.7" fill="none" aria-hidden="true">${p.dessin}</svg>`;
    const n = el('span', { class: 'pc-n' });
    n.textContent = p.nom;
    b.append(e, n);
    surToucher(b, () => {
      // un pinceau de Ma Parole ! est un MUR : il ne se choisit pas (C-196 ; sa phrase de mur : lot 8)
      if (!p.libre) return;
      P.pinceau = p.nom;
      majRail();
      majGarder();
    });
    rail.appendChild(b);
  }
  dv.appendChild(cs);

  // ── l'état de la page ──
  let P: PhrasePage = neuve('promi');
  let signature0 = '';
  let exemples: Partial<Record<TypeExemple, string>> = {};
  let prenomRang = 0;
  let choix: 'qui' | 'avec' | 'membres' | null = null;
  let saisieDe: 'titre' | 'nom' | null = null;
  let dalleT: { w: number; h: number; nat: Nature } | null = null;
  let repris: number | null = null;
  let mise = { base: 312, amp: 36, hz: 0, nl: 2, taille: 36 };
  /** ce qui part en flaques (un mouvement l'a pris) : `composer` ne le cache pas d'un coup sous lui */
  const sortants = new Set<HTMLElement>();
  /** C-122 : la zone « un prénom… » est active (on y écrit) */
  let ajoutActif = false;
  let peaufOuvert = false;
  let menu: HTMLElement | null = null;
  /** le mouvement en cours (Q598, C-234) : son image, la place VUE (l'onde, la phrase, le bouton photo, la barre) */
  let mv: { id: number; fin: () => void } | null = null;
  /** une lettre tapée depuis l'ouverture de la saisie (Q620) */
  let aTape = false;
  // C-271, C-278 : la taille, les mots de liaison et les places de la phrase changent en douceur (continu.ts)
  const continu = creerContinu({
    cs,
    txt,
    rail: pinceau,
    choixHote,
    h,
    trace: () => {
      try {
        return chargerTrace();
      } catch {
        return null;
      }
    },
    montree: () => !cs.hidden && !cs.classList.contains('pp-part') && !cs.classList.contains('pp-compose'),
    cle: () => P.nat,
    choixOuvert: () => choix !== null,
    // Q620 : ce qu'on TAPE paraît tel quel — à partir de la première lettre ; l'entrée dans la saisie, elle, glisse (le prototype ne glissait
    // pas dès le champ ouvert : les mots y sautaient de 5 pt, C-271)
    frappe: () =>
      saisieDe !== null &&
      aTape &&
      !douceur.enCours() &&
      !!txt.querySelector('.ph-m[data-ph="titre"]:not(.ph-vide), .ph-m[data-np="nom"]:not(.ph-vide)'),
    mouvement: () => mv !== null,
    placeEnDetrace: () => douceur.enCours(),
  });
  // C-271 : une place de la phrase qui change ne change jamais d'un coup (douceur.ts, le prototype `lot-V200-DOUCEUR`)
  let ouverteA = -1e9;
  const douceur = creerDouceur({
    txt,
    hote: phrase,
    h,
    trace: () => {
      try {
        return chargerTrace();
      } catch {
        return null;
      }
    },
    vivante: () =>
      !cs.hidden &&
      !cs.classList.contains('pp-part') &&
      !cs.classList.contains('pp-compose') &&
      h.maintenant() - ouverteA >= 600,
    cle: () => P.nat,
    change: () => {
      continu.verifie();
    },
  });
  try {
    (chargerTrace() as unknown as { horsAnim?: (el: Element) => (() => void) | null }).horsAnim = (el) =>
      continu.horsAnim(el);
  } catch {
    /* (sans le module, rien ne se trace) */
  }
  let vue = { base: 312, amp: 36, hz: 0 };
  /** le décalage de « DÉJÀ PROMIS » sous une phrase plus longue (le prototype : `dec`) */
  let decDeja: number | null = null;

  function neuve(nat: Nature): PhrasePage {
    return {
      nat,
      sens: 'soi',
      titre: '',
      qui: [],
      avec: [],
      nom: '',
      membres: [],
      pinceau: 'Plein',
      moi: false,
      note: '',
      ech: T.peauf.echeanceDefaut,
      echChoisie: false,
      due: null,
      dueISO: null,
      cercle: null,
      fichiers: [],
      photo: null,
      dessin: null,
    };
  }
  const largeur = (): number => cs.clientWidth || 390;
  const haut0 = (): number => parseFloat(getComputedStyle(cs).getPropertyValue('--pp-h')) || 0;

  /** l'exemple de la pastille vide de ce type, pour cette ouverture (un tirage par ouverture) */
  function exemple(t: TypeExemple): string {
    const deja = exemples[t];
    if (deja != null) return deja;
    const L = EXEMPLES[t];
    const rang = magasin.tirerExemple(t, L.length, EXEMPLES_FIXES[t], Math.random);
    const v = L[rang] ?? L[0]!;
    exemples[t] = v;
    return v;
  }
  const typeExemple = (): TypeExemple => (P.nat === 'promi' ? P.sens : P.nat);
  // le prototype : plusieurs personnes, « tout le monde », ou un Cercle choisi (Peaufiner) — « vous » et « promettez-moi »
  const pluriel = (): boolean => P.qui.length > 1 || !!P.cercle || P.qui.includes(T.toutLeMonde);
  /**
   * ⚑ C-332 (Tom, 22 nov. 2026) — « MOI » SE COCHE ET SE DÉCOCHE COMME N'IMPORTE QUELLE PERSONNE : on peut toujours le remettre, il coexiste
   * avec les autres, le toucher ne retire jamais quelqu'un d'autre ; la liste n'est jamais vide (retirée la dernière, « Moi » revient). Il vit
   * DANS la liste (`MOI`, en tête) dès qu'il est à côté de quelqu'un ; seul, la liste est vide et la place dit « moi » (C-304, en pointillés).
   * La phrase dit ce qui est coché (« à Maman et moi », Q624) ; la parole plantée et le gardé de côté portent les autres (le prototype : `newWhoSel`).
   */
  const MOI = T.moi;
  /** ⚑ Q624 (Tom, 22 nov. 2026) : « moi » coché avec d'autres se dit EN DERNIER, après « et » — « à Maman et moi », « à Maman, Rachel et moi »,
   *  « avec Maman et moi » ; sans lui, les noms seuls, comme avant */
  const ecrit = (L: string[], sep: string): string => {
    const a = autres(L);
    return L.includes(MOI) && a.length ? `${a.join(sep)} ${T.liaisons.et} ${T.vides.moi}` : a.join(sep);
  };
  const autres = (L: string[]): string[] => L.filter((n) => n !== MOI);

  // ── LA PHRASE ──
  /**
   * le visage d'une personne (§2.10, le prototype `_visageSvg`) : un disque de 0,76 × 33 = 25 pt à la couleur de la nature, la silhouette
   * crème — dans la pastille d'un prénom rempli (« à Maman », « tout le monde »), jamais d'une place vide ni d'un « avec »
   */
  const visage = (): string => {
    const d = 25;
    const col = P.nat === 'chiche' ? palette.framboise54 : palette.bleu45;
    const x0 = (d / 2 - 0.3 * d).toFixed(2);
    const x1 = (d / 2 + 0.3 * d).toFixed(2);
    const ye = (0.98 * d).toFixed(2);
    return (
      `<span class="pp-visage" style="width:${String(d)}px;height:${String(d)}px;background:${col}">` +
      `<svg viewBox="0 0 ${String(d)} ${String(d)}" xmlns="http://www.w3.org/2000/svg">` +
      `<circle cx="${String(d / 2)}" cy="${((0.78 * d) / 2).toFixed(2)}" r="${(0.19 * d).toFixed(2)}" fill="${palette.creme95}"/>` +
      `<path d="M${x0} ${ye} A${(0.3 * d).toFixed(2)} ${(0.27 * d).toFixed(2)} 0 0 1 ${x1} ${ye} Z" fill="${palette.creme95}"/>` +
      `</svg></span>`
    );
  };
  const pastille = (cle: string, texte: string, vide: boolean, attr = 'data-ph', vis = false): string =>
    `<span class="ph-m${vide ? ' ph-vide' : ''}${vis && !vide ? ' ph-avec-visage' : ''}" ${attr}="${cle}">${vis && !vide ? visage() : ''}${esc(texte)}</span>`;
  /**
   * le contenu d'une place qui s'écrit (le titre, le nom) : vide, son exemple ; pendant la saisie (`ph-on`, lot-CURSEUR), ce qu'on tape et
   * le curseur qui clignote après lui (le prototype n'en pose pas tant que la place est vide : l'exemple reste)
   */
  const contenuPlace = (v: string, ex: string, ici: boolean): string =>
    ici && v ? `${esc(v)}<i class="ph-caret" aria-hidden="true"></i>` : esc(v || ex);
  function titrePastille(): { html: string; li: string } {
    const v = P.titre.trim();
    const ex = variante(exemple(typeExemple()), pluriel());
    const li = elision(v || ex);
    const cls = li === 'd’' ? 'ph-li ph-elide' : 'ph-li';
    const ici = saisieDe === 'titre';
    return {
      li,
      html: `<em class="${cls}">${li}</em> <span class="ph-m${v ? '' : ' ph-vide'}${ici ? ' ph-on' : ''}" data-ph="titre" data-plein="${esc(v || ex)}">${contenuPlace(ici ? P.titre : v, ex, ici)}</span>`,
    };
  }
  function htmlPhrase(): string {
    const n = P.nat;
    if (n === 'nuee') {
      const nom = P.nom.trim();
      const ex = exemple('nuee');
      // C-304 (v199, `lot-V199-MOI`) : la place « avec » touchée sans personne passe à « moi », comme celle d'un Promi ou d'un Chiche
      const avec = P.membres.length ? ecrit(P.membres, ' · ') : P.moi ? T.vides.moi : T.vides.toutLeMonde;
      const ici = saisieDe === 'nom';
      return (
        `<span class="ph-b ph-b-fixe">${esc(T.cercle)}</span><br>` +
        `<em>${T.liaisons.nomme}</em> <span class="ph-m${nom ? '' : ' ph-vide'}${ici ? ' ph-on' : ''}" data-np="nom" data-plein="${esc(nom || ex)}">${contenuPlace(ici ? P.nom : nom, ex, ici)}</span><br>` +
        `<em>${T.liaisons.avec}</em> ${pastille('avec', avec, !P.membres.length, 'data-np')}`
      );
    }
    const titre = titrePastille().html;
    if (n === 'chiche') {
      const qui = P.qui.length ? ecrit(P.qui, ', ') + ',' : P.moi ? T.vides.moi : T.vides.quiOse;
      const verbe = P.qui.length ? T.chiche.toLowerCase() : T.chiche;
      const avec = P.avec.length ? ecrit(P.avec, ', ') : T.vides.quiEnEst;
      return (
        `<em>${T.liaisons.a}</em> ${pastille('qui', qui, !P.qui.length, 'data-ph', true)}<br>` +
        `<span class="ph-b ph-b-fixe" data-ph="sens">${verbe}</span> <br>${titre}<br>` +
        `<em>${T.liaisons.avec}</em> ${pastille('avec', avec, !P.avec.length)}`
      );
    }
    // (après le verbe, une espace avant le retour à la ligne : le texte de la phrase est celui du prototype, sans effet à l'écran)
    const verbe = (v: string): string => `<span class="ph-b" data-ph="sens">${esc(v)}${SVG_BASCULE}</span>`;
    if (P.sens === 'soi') return `${verbe(T.verbe.soi)} <br>${titre}`;
    if (P.sens === 'faire') {
      const qui = P.qui.length ? ecrit(P.qui, ', ') : P.moi ? T.vides.moi : T.vides.qui;
      return `${verbe(T.verbe.faire)} <br>${titre}<br><em>${T.liaisons.a}</em> ${pastille('qui', qui, !P.qui.length, 'data-ph', true)}`;
    }
    const prenom = P.qui.length ? ecrit(P.qui, ', ') + ',' : PRENOMS_EXEMPLE[prenomRang]!;
    return `${pastille('qui', prenom, !P.qui.length, 'data-ph', true)}<br>${verbe(pluriel() ? T.verbe.demanderPluriel : T.verbe.demander)} <br>${titre}`;
  }

  const lignes = (): number => txt.querySelectorAll('br').length + 1;
  const appli = (t: number): void => {
    txt.style.setProperty('font-size', `${String(t)}px`);
    // v102 : l'interligne d'une étiquette est 1,2 × la taille × l'agrandissement des faces (112 %, v96), plus 24
    txt.style.setProperty('line-height', `${String(Math.floor(t * 1.2 * 1.12) + 24)}px`);
  };
  /** la plus longue ligne rendue de la phrase, en pt (la mesure du §2.8 corrigé) */
  const mesure = (t: number): number => {
    appli(t);
    txt.style.whiteSpace = 'nowrap';
    const w = txt.scrollWidth;
    txt.style.whiteSpace = '';
    return w;
  };

  /**
   * §2.8 (v20, v46, v115, v180b) — la taille de la phrase : 36 si elle tient en trois lignes, 34 à quatre, 30 au-delà (30 sur un choix ouvert),
   * réduite tant qu'une ligne dépasse la largeur ; plutôt que de descendre sous la taille de départ, l'EXEMPLE se coupe en deux morceaux
   * équilibrés (jamais seul après « de »), sinon en trois, à la plus grande taille où une coupe tient ; la coupe change le nombre de lignes,
   * donc la taille de départ : on recommence une fois, et une troisième passe fige (la bascule de v150). Puis C-240 : la phrase laisse la
   * place du rail (12 · 44 · 12) au-dessus de « garder de côté », sinon elle perd un point et l'on recompose.
   */
  function composerPhrase(ouvert: boolean, cap: number): { taille: number; nl: number } {
    const lim = largeur() - 48;
    txt.innerHTML = htmlPhrase();
    // v46 (Tom) : « le reste reste indemne » — la taille de la phrase se calcule comme si la parole tapée était courte (son premier mot,
    // 14 caractères au plus) ; une parole longue faisait tomber toute la phrase au plancher. La pastille du titre (ou du nom d'un Cercle) est
    // traitée après, seule (`titrePlein`). Une place qui porte un nœud (une enveloppe de tracé) n'est pas touchée.
    const ptL = txt.querySelector<HTMLElement>(
      '.ph-m[data-ph="titre"]:not(.ph-vide), .ph-m[data-np="nom"]:not(.ph-vide)',
    );
    let ptOrig: string | null = null;
    if (ptL && !ptL.querySelector('*')) {
      ptOrig =
        ptL.dataset['ph'] === 'titre' && P.titre.trim() ? P.titre.trim() : (ptL.textContent ?? '').replace(/…$/, '');
      ptL.textContent = (ptOrig.split(/\s+/)[0] || ptOrig).slice(0, 14);
    }
    let taille = 36;
    let nlAvant = lignes();
    for (let passe = 0; passe < 3; passe++) {
      const pmC = txt.querySelector<HTMLElement>('.ph-m.ph-vide[data-ph="titre"], .ph-m.ph-vide[data-np="nom"]');
      const plein = pmC?.getAttribute('data-plein') ?? '';
      if (passe === 2) break;
      nlAvant = lignes();
      txt.classList.remove('ph-coupe');
      if (pmC) pmC.textContent = plein;
      let depart = ouvert ? 30 : nlAvant <= 3 ? 36 : nlAvant === 4 ? 34 : 30;
      if (cap) depart = Math.min(depart, cap);
      let t = depart;
      while (t > 16 && mesure(t) > lim) t--;
      taille = t;
      if (t < depart && pmC && !ouvert) {
        const mots = plein.split(' ');
        const bord = (): number => {
          const R = txt.getBoundingClientRect();
          let d = 0;
          for (const q of pmC.getClientRects()) d = Math.max(d, q.right - R.left);
          return d;
        };
        const html = (ks: number[]): string => {
          const p = [0, ...ks, mots.length];
          const o: string[] = [];
          for (let j = 0; j < p.length - 1; j++)
            o.push(`<span style="white-space:nowrap">${esc(mots.slice(p[j], p[j + 1]).join(' '))}</span>`);
          return o.join('<br>');
        };
        let trouve: { t: number; ks: number[] } | null = null;
        if (mots.length > 1) {
          txt.classList.add('ph-coupe');
          for (let tt = depart; tt >= PLANCHER_PH && !trouve; tt--) {
            appli(tt);
            let best: { k: number; ec: number } | null = null;
            for (let kk = 1; kk < mots.length; kk++) {
              pmC.innerHTML = html([kk]);
              if (bord() > lim || mesure(tt) > lim) continue;
              const rq = pmC.getClientRects();
              const L = [...rq].map((q) => q.width);
              let ec = L.length >= 2 ? Math.abs(L[0]! - L[L.length - 1]!) : 1e9;
              if (rq.length && rq[0]!.left - txt.getBoundingClientRect().left < 20) ec += 1e6;
              if (!best || ec < best.ec) best = { k: kk, ec };
            }
            if (best && best.ec < 1e6) trouve = { t: tt, ks: [best.k] };
          }
          for (let t3 = depart; t3 >= PLANCHER_PH && !trouve && mots.length > 2; t3--) {
            appli(t3);
            let b3: { ks: number[]; e: number } | null = null;
            for (let a1 = 1; a1 < mots.length - 1; a1++)
              for (let a2 = a1 + 1; a2 < mots.length; a2++) {
                pmC.innerHTML = html([a1, a2]);
                if (bord() > lim || mesure(t3) > lim) continue;
                const q3 = pmC.getClientRects();
                if (!q3.length || q3[0]!.left - txt.getBoundingClientRect().left < 20) continue;
                const w3 = [...q3].map((q) => q.width).slice(1);
                const e3 = Math.max(...w3) - Math.min(...w3);
                if (!b3 || e3 < b3.e) b3 = { ks: [a1, a2], e: e3 };
              }
            if (b3) trouve = { t: t3, ks: b3.ks };
          }
        }
        if (trouve) {
          taille = trouve.t;
          appli(taille);
          pmC.innerHTML = html(trouve.ks);
        } else {
          txt.classList.remove('ph-coupe');
          pmC.textContent = plein;
        }
      }
      appli(taille);
      if (lignes() === nlAvant) break;
    }
    if (ptL && ptOrig !== null) {
      ptL.textContent = ptOrig;
      ptL.style.setProperty('overflow-wrap', 'anywhere', 'important');
    }
    return { taille, nl: lignes() };
  }

  /**
   * LE TITRE ÉCRIT ET LA HAUTEUR (v181b, C-244 §5.1 ; v182b, C-240 ; le prototype : `tient`, `taillePt`) — sous la phrase (et sous l'aide d'une
   * pastille vide), il doit rester 20 pt d'air, la rangée du pinceau (44) et 20 pt avant « garder de côté » : sinon le titre se réduit (deux,
   * puis trois lignes, jusqu'à 16) ; si ça ne suffit pas, la phrase entière descend d'un palier (2 pt, 1 sous 14) et le titre de 16 à 12, avec
   * l'air de C-240 (12 · 44 · 12). Une phrase qui tient ne change pas. Rend vrai si le titre a été réduit. (La coupe « … » d'un titre qui ne
   * tient pas même à 12 : le 2c, les textes longs.)
   */
  function titrePlein(r: { taille: number; nl: number }): boolean {
    const ptL = txt.querySelector<HTMLElement>(
      '.ph-m[data-ph="titre"]:not(.ph-vide), .ph-m[data-np="nom"]:not(.ph-vide)',
    );
    if (!ptL) return false;
    const pr = ptL.previousElementSibling;
    const liL = pr && pr.classList.contains('ph-li') ? (pr as HTMLElement) : null;
    const C = cs.getBoundingClientRect();
    const k = C.width / (cs.offsetWidth || 390) || 1;
    const finMax = garder.hidden ? 760 : (garder.getBoundingClientRect().top - C.top) / k;
    const aideH = txt.querySelector('.ph-m.ph-vide') ? 34 + 24 : 0;
    const lim = largeur() - 48 + 0.5;
    const lignesDe = (x: HTMLElement): number => {
      const t: [number, number][] = [];
      const rg = document.createRange();
      rg.selectNodeContents(x);
      for (const q of rg.getClientRects()) {
        if (q.width < 1 || q.height < 1) continue;
        const c = (q.top + q.bottom) / 2;
        if (t.some(([a, b]) => c > a && c < b)) continue;
        t.push([q.top, q.bottom]);
      }
      return t.length;
    };
    const tient = (n: number, air = 20): boolean => {
      if (lignesDe(ptL) > n) return false;
      const R = txt.getBoundingClientRect();
      for (const q of ptL.getClientRects()) if ((q.right - R.left) / k > lim) return false;
      return (R.bottom - C.top) / k + aideH + air + 44 + air <= finMax;
    };
    const taillePt = (t: number): void => {
      for (const x of [ptL, liL]) {
        if (!x) continue;
        x.style.setProperty('font-size', `${String(t)}px`, 'important');
        x.style.setProperty('line-height', `${String(Math.round(t * 1.2))}px`, 'important');
      }
    };
    if (tient(2)) return false;
    let fait = false;
    for (let n = 2; n <= 3 && !fait; n++)
      for (let tp = r.taille; tp >= 16; tp--) {
        taillePt(tp);
        if (tient(n)) {
          fait = true;
          break;
        }
      }
    for (let tg = r.taille; tg >= 12 && !fait; tg -= tg > 14 ? 2 : 1) {
      appli(tg);
      for (let tp2 = Math.min(16, tg); tp2 >= 12 && !fait; tp2--) {
        taillePt(tp2);
        if (tient(20, 12)) {
          fait = true;
          r.taille = tg;
        }
      }
    }
    if (!fait) {
      appli(r.taille);
      taillePt(16);
      // C-244 §5.1 : la coupe ne vient qu'après — la plus longue part du titre qui tient (3 lignes, puis 2, puis 1), terminée par « … » ;
      // jamais un titre vidé (v162 : un titre qui ne tient pas même à « … » reste entier, à la plus grande taille qui tient en largeur)
      const orig = ptL.textContent ?? '';
      let lo = 0;
      for (let limT = 3; limT >= 1; limT--) {
        let a = 0;
        let b = orig.length;
        while (a < b) {
          const mid = (a + b + 1) >> 1;
          ptL.textContent = orig.slice(0, mid).replace(/\s+$/, '') + '…';
          if (tient(limT)) a = mid;
          else b = mid - 1;
        }
        ptL.textContent = orig.slice(0, a).replace(/\s+$/, '') + '…';
        lo = a;
        if (lo > 0) break;
      }
      if (lo === 0 && orig) {
        ptL.textContent = orig;
        const R = txt.getBoundingClientRect();
        const tientL = (n: number): boolean =>
          lignesDe(ptL) <= n && [...ptL.getClientRects()].every((q) => (q.right - R.left) / k <= lim);
        let tpL = 16;
        for (let tq = r.taille; tq >= 16; tq--) {
          taillePt(tq);
          if (tientL(3)) {
            tpL = tq;
            break;
          }
        }
        taillePt(tpL);
      }
      ptL.classList.add('ph-coupe-t');
    }
    return true;
  }

  /** le bas de l'encre de la phrase (le TEXTE, pas les boîtes), en pt du cadre */
  function basEncre(): number {
    const r = document.createRange();
    r.selectNodeContents(txt);
    const C = cs.getBoundingClientRect();
    let b = 0;
    for (const q of r.getClientRects()) if (q.width > 1 && q.height > 1) b = Math.max(b, q.bottom - C.top);
    return b;
  }

  // ── LE CHAMP : l'aplat de la nature au-dessus de la vague, la dalle d'avance ──
  function peindreChamp(
    base: number,
    amp: number,
    hz: number,
    H: number,
    sous = choix !== null || saisieDe !== null,
  ): void {
    peindreFond(base, amp, hz, H, sous);
    peindreInvite(base + hz, amp, H);
  }
  function peindreFond(base: number, amp: number, hz: number, H: number, sous: boolean): void {
    const W = largeur();
    const dpr = Math.max(2, Math.min(3, window.devicePixelRatio || 2));
    cv.width = Math.round(W * dpr);
    cv.height = Math.round(H * dpr);
    cv.style.width = `${String(W)}px`;
    cv.style.height = `${String(H)}px`;
    const g = cv.getContext('2d');
    if (!g) return;
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.clearRect(0, 0, W, H);
    g.imageSmoothingEnabled = true;
    g.imageSmoothingQuality = 'high';
    const y = onde(base + hz, amp, W);
    g.beginPath();
    cheminOnde(g, y, 0, W, W);
    g.lineTo(W, 0);
    g.lineTo(0, 0);
    g.closePath();
    g.fillStyle = CHAMP[P.nat];
    g.fill();
    cv.setAttribute('data-champ', CHAMP[P.nat]);
    // C-241 : la dalle que CETTE parole aura (Promi, Chiche), sa taille fixée à l'ouverture (C-234), 16 pt plus bas tant que l'horizon est
    // bas (Q599) ; sous la vague quand le champ descend sous elle (un choix ouvert)
    // C-241, v183b : la dalle est née au trait — la page + ne la montre plus (une seule dalle à l'écran)
    const dz = P.dessin && dessinPose(P.dessin) && !P.dessin.masque ? P.dessin : null;
    if (dz || !dalleT || plantee) {
      peindreDessin(y, dz, W, H, dpr);
      return;
    }
    const dw = dalleT.w;
    const dh = dalleT.h;
    const x = Math.floor((W - dw) / 2);
    const yD = 88 + dzDalle();
    peindrePhoto(y, x, yD, dw, dh, W, H, dpr);
    const clip = (): void => {
      g.save();
      g.beginPath();
      cheminOnde(g, y, 0, W, W);
      g.lineTo(W, 0);
      g.lineTo(0, 0);
      g.closePath();
      g.clip();
    };
    if (P.nat === 'nuee') {
      // un Cercle n'a pas de dalle d'avance : la page + montre la dalle d'une parole d'un Cercle (de préférence entière), teinte par la rampe
      // de sa nature (Q30, peinte par le moteur) ; à défaut, la dernière parole (le prototype, `trait()`)
      const ps = magasin.etat().paroles;
      const pool = ps.filter((q) => !q.draft && !!q.nuee);
      const entieres = pool.filter((q) => facade.dalleEntiere(q.id));
      const id = (entieres.at(-1) ?? pool.at(-1) ?? ps.at(-1))?.id;
      if (id == null) return;
      if (sous) clip();
      const hex = (v: string): number[] => [1, 3, 5].map((i) => parseInt(v.slice(i, i + 2), 16));
      const r = facade.poserDalle(g, id, x, yD, dw, dh, {
        rampe: { cols: [palette.rampeCercle1, palette.rampeCercle2, palette.rampeCercle3].map(hex), haut: 2 },
        courant: 1,
      });
      if (sous) g.restore();
      if (r) cv.setAttribute('data-matiere', [r.x, r.y, r.w, r.h].map((v) => Math.round(v)).join(','));
      return;
    }
    const av = facade.dalleAvenir(magasin.etat().compteurs.nid, dw * dpr, dh * dpr, {
      chiche: P.nat === 'chiche',
      title: P.titre.trim(),
      who: autres(P.qui).length ? autres(P.qui).join(', ') : 'moi',
    });
    if (!av) return;
    if (sous) clip();
    facade.poserUn(g, av, x + dw / 2, yD + dh / 2);
    if (sous) g.restore();
    const aw = av.width / dpr;
    const ah = av.height / dpr;
    cv.setAttribute(
      'data-matiere',
      [x + dw / 2 - aw / 2, yD + dh / 2 - ah / 2, aw, ah].map((v) => Math.round(v)).join(','),
    );
  }

  // ── LE DESSIN DANS LA BANDE (C-042, v128 ; le prototype `bande`) : il REMPLACE la dalle ou la photo — une couche pleine (son fond, ses traits,
  //    à l'échelle 1, calés EN HAUT), découpée à 7 pt au-dessus de l'axe du trait : la bande montre UNE chose. Sa couche : celle de la photo. ──
  function peindreDessin(y: Onde, d: Dessin | null, W: number, H: number, dpr: number): void {
    photoCv.width = cv.width;
    photoCv.height = cv.height;
    photoCv.style.width = `${String(W)}px`;
    photoCv.style.height = `${String(H)}px`;
    const g = photoCv.getContext('2d');
    if (!g) return;
    g.setTransform(1, 0, 0, 1, 0, 0);
    g.clearRect(0, 0, photoCv.width, photoCv.height);
    if (!d) return;
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.save();
    g.beginPath();
    cheminOnde(g, (x) => y(x) - DESSIN.BANDE_RETRAIT, 0, W, W);
    g.lineTo(W, 0);
    g.lineTo(0, 0);
    g.closePath();
    g.clip();
    g.setTransform(1, 0, 0, 1, 0, 0);
    g.drawImage(dessinEntier(d, dpr), 0, 0);
    g.restore();
  }

  // ── LA PHOTO IMPORTÉE (lot-PHOTO) : elle REMPLACE la dalle — la même boîte, recadrée au centre (couverture), bornée par l'onde ; l'aplat
  //    de la nature reste dessous. Sa couche (`#csPhotoCv`) a les cotes du champ. ──
  const images = new Map<string, HTMLImageElement>();
  function peindrePhoto(
    y: Onde,
    x: number,
    yD: number,
    dw: number,
    dh: number,
    W: number,
    H: number,
    dpr: number,
  ): void {
    photoCv.width = cv.width;
    photoCv.height = cv.height;
    photoCv.style.width = `${String(W)}px`;
    photoCv.style.height = `${String(H)}px`;
    const g = photoCv.getContext('2d');
    if (!g) return;
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.clearRect(0, 0, W, H);
    const src = P.photo;
    if (!src) return;
    let im = images.get(src);
    if (!im) {
      im = new Image();
      im.onload = () => {
        if (!cs.hidden) peindreChamp(vue.base, vue.amp, vue.hz, vue.base + vue.amp + 60 + vue.hz);
      };
      im.src = src;
      images.set(src, im);
    }
    if (!im.complete || !im.naturalWidth) return;
    g.save();
    g.beginPath();
    cheminOnde(g, y, 0, W, W);
    g.lineTo(W, 0);
    g.lineTo(0, 0);
    g.closePath();
    g.clip();
    const r = im.naturalWidth / im.naturalHeight;
    const br = dw / dh;
    let sw: number, sh: number, sx: number, sy: number;
    if (r > br) {
      sh = im.naturalHeight;
      sw = sh * br;
      sx = (im.naturalWidth - sw) / 2;
      sy = 0;
    } else {
      sw = im.naturalWidth;
      sh = sw / br;
      sx = 0;
      sy = (im.naturalHeight - sh) / 2;
    }
    g.drawImage(im, sx, sy, sw, sh, x, yD, dw, dh);
    g.restore();
  }

  /** v164a (C-201) : le bouton photo au-dessus de l'encre du trait, 8 pt d'air (`hautBouton` du prototype) */
  function hautBouton(base: number, amp: number): number {
    const W = largeur();
    const y = onde(base, amp, W);
    const ep = Math.max(5 * TRAIT_K, 6 * TRAIT_PTS, 4.5 * TRAIT_PTS);
    let m = 1e9;
    for (let x = W - 24 - 34 - 2; x <= W - 24 + 2; x += 2) m = Math.min(m, y(x));
    return Math.round(Math.min(y(W - 41) - 52, m - ep - 8 - 34));
  }

  // ── L'INVITE À TRACER (C-209, C-213, C-229 ; le prototype : `lot-V172-INVITE`) — À L'OUVERTURE, RIEN DU TRAIT : l'horizon est 40 pt plus bas
  //    que sa place (jamais à moins de 12 pt de l'encre de la phrase). LA PAROLE PRÊTE (la phrase ; le nom d'un Cercle) et VALIDÉE (ni saisie,
  //    ni choix ouverts, la page posée) : l'horizon remonte (360 ms, une courbe douce), PUIS le trait naît en flaques sur l'image d'avant
  //    (700 ms), le libellé « trace pour … » se TRACE, le départ CLIGNOTE avec le I de PROMI jusqu'au premier toucher du trait. Redevenue
  //    incomplète : le trait repart en flaques (300 ms), le libellé se détrace, puis l'horizon redescend. ──
  const HZ_DUREE = 360;
  const inv = {
    vis: false,
    sortie: false,
    touche: false,
    haut: true,
    anim: null as { de: number; a: number; acc: number; tp: number; jeu: number } | null,
    v: 0,
    jeu: 0,
    trace: null as ControleTrace | null,
    passes: [] as ControlePassage[],
  };
  let hzC = HZ_BAS;
  let derniereCompo = 0;
  const hzEff = (): number => (inv.anim ? inv.v : inv.haut ? hzC : 0);
  /** Q599, C-234 : la dalle suit l'ÉTAT de l'horizon (bas : 16 pt ; en mouvement : la même part de sa course ; haut : 0) */
  function dzDalle(): number {
    const A = inv.anim;
    let f = inv.haut ? 1 : 0;
    if (A) {
      const lo = Math.min(A.de, A.a);
      const hi = Math.max(A.de, A.a);
      if (hi - lo >= 0.5) f = Math.max(0, Math.min(1, (inv.v - lo) / (hi - lo)));
    }
    return Math.round(16 * f * 4) / 4;
  }
  const prete = (): boolean => (P.nat === 'nuee' ? P.nom : P.titre).trim().length > 0;
  function repeindre(): void {
    if (cs.hidden) return;
    const hz = hzEff();
    mise.hz = hz;
    peindreChamp(mise.base, mise.amp, hz, mise.base + mise.amp + 60 + hz);
  }
  /** l'horizon va à sa place « pas prête » (enHaut, sous sa place) ou à sa place (0), en 360 ms */
  function bouge(enHaut: boolean, fin?: () => void): void {
    const de = hzEff();
    inv.haut = enHaut;
    cs.classList.toggle('pp-haut', enHaut);
    const a = enHaut ? hzC : 0;
    if (reduit() || Math.abs(a - de) < 0.5) {
      inv.anim = null;
      repeindre();
      fin?.();
      return;
    }
    const A = { de, a, acc: 17, tp: h.maintenant(), jeu: ++inv.jeu };
    inv.anim = A;
    inv.v = de;
    const pas = (): void => {
      if (inv.anim !== A) return;
      const t = h.maintenant();
      A.acc += Math.min(34, t - A.tp);
      A.tp = t;
      if (enHaut) A.a = hzC;
      const u = Math.min(1, A.acc / HZ_DUREE);
      inv.v = A.de + (A.a - A.de) * doux(u);
      repeindre();
      if (u < 1) h.image(pas);
      else {
        inv.anim = null;
        repeindre();
        fin?.();
      }
    };
    pas();
  }
  /** le trait et le départ, sur le champ et sur la couche du départ (vidée quand rien ne clignote) */
  function peindreInvite(baseH: number, amp: number, H: number): void {
    const W = largeur();
    const dpr = Math.max(2, Math.min(3, window.devicePixelRatio || 2));
    if (departCv.width !== cv.width) departCv.width = cv.width;
    if (departCv.height !== cv.height) departCv.height = cv.height;
    departCv.style.width = `${String(W)}px`;
    departCv.style.height = `${String(H)}px`;
    const gd = departCv.getContext('2d');
    const g = cv.getContext('2d');
    if (!gd || !g) return;
    gd.setTransform(1, 0, 0, 1, 0, 0);
    gd.clearRect(0, 0, departCv.width, departCv.height);
    if (!(inv.vis || inv.sortie)) {
      cv.removeAttribute('data-depart');
      return;
    }
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    gd.setTransform(dpr, 0, 0, dpr, 0, 0);
    const clignote = inv.vis && !inv.touche && !reduit();
    const y = onde(baseH, amp, W);
    const cx = peindreTrait({
      depart: clignote ? gd : g,
      champ: g,
      y,
      base: baseH,
      W,
      col: NATTRAIT[P.nat],
      etat: plantee ? 'signe' : doigt != null ? 'cours' : 'plate',
      doigt: doigt ?? 0,
      entier: P.nat === 'nuee',
    });
    cv.setAttribute('data-depart', `${String(Math.round(cx * 10) / 10)},${String(Math.round(y(cx) * 10) / 10)}`);
  }
  /** le départ clignote avec le I de PROMI (son animation, calée sur sa phase) jusqu'au premier toucher ; fixe sous « Réduire les animations » */
  function clignote(on: boolean): void {
    if (!on || inv.touche || reduit()) {
      departCv.classList.remove('clignote');
      return;
    }
    departCv.classList.add('clignote');
    const cale = (): void => {
      const I = document.querySelector('.acc-mm i');
      const An = I?.getAnimations().find((a) => (a as CSSAnimation).animationName === 'promiBlink');
      const Af = departCv.getAnimations().find((a) => (a as CSSAnimation).animationName === 'promiBlink');
      if (Af && An?.currentTime != null) Af.currentTime = An.currentTime;
    };
    cale();
    h.image(() => {
      cale();
      h.image(cale);
    });
  }
  /** le libellé du trait : « trace pour planter » (à soi) · « trace ta moitié » (à quelqu'un) · « trace pour lancer » (Chiche, Cercle) */
  function poseLibelle(base: number, amp: number, ouvert: boolean): void {
    const mt =
      P.nat === 'promi'
        ? ouvert || P.sens === 'soi' || !autres(P.qui).length
          ? T.trace.planter
          : T.trace.moitie
        : T.trace.lancer;
    if (lib.dataset['mot'] !== mt) {
      lib.textContent = mt;
      lib.dataset['mot'] = mt;
    }
    // C-157 : sur un Promi et un Chiche, 7,5 pt plus bas et 3 pt à droite (aligné sur la flèche, sans la toucher) ; un Cercle ne bouge pas
    const mdx = P.nat === 'nuee' ? 0 : 3;
    const mdy = P.nat === 'nuee' ? 0 : 7.5;
    const boite = base + amp + 60;
    lib.style.left = `${String(Math.round(largeur() * 0.11 + 39.1 + mdx))}px`;
    lib.style.top = `calc(var(--pp-h) + ${String((ouvert ? 184 : boite - 60) + mdy + DT)}px)`;
    lib.classList.toggle('pp-choix', choix !== null);
  }
  /** l'image de ce qui est là (le corps de la page sous l'onde, puis le champ et le trait) — le passage en flaques part d'elle */
  function copieChamp(): HTMLCanvasElement {
    const k = document.createElement('canvas');
    k.width = cv.width;
    k.height = cv.height;
    const g = k.getContext('2d')!;
    g.fillStyle = getComputedStyle(cs).backgroundColor;
    g.fillRect(0, 0, k.width, k.height);
    g.drawImage(cv, 0, 0);
    g.drawImage(departCv, 0, 0);
    return k;
  }
  /** tout le trait, sur la largeur de l'écran : du haut de l'onde moins 22 pt jusque sous la flèche et le creux de l'onde */
  function rectTrait(): [number, number, number, number] {
    const W = largeur();
    const y = onde(mise.base + hzEff(), mise.amp, W);
    let m = 1e9;
    let b = -1e9;
    for (let x = -12; x <= W + 12; x += 4) {
      m = Math.min(m, y(x));
      b = Math.max(b, y(x));
    }
    const y0 = Math.max(0, m - 22);
    const y1 = Math.max(mise.base + 54, b + 14);
    return [0, y0 + haut0(), W, y1 - y0];
  }
  function purgeInvite(): void {
    for (const p of inv.passes) {
      p.arrete = true;
      p.canevas.remove();
    }
    inv.passes = [];
  }
  /** C-269 (v199, `lot-V199-MOI`) : la parole validée, sans personne choisie, la place du destinataire dit « moi » en pointillés (hors
   *  « promets-moi » et « je me promets ») — tracée avec le trait ; redevenue incomplète, la place reprend son mot */
  function placeMoi(on: boolean): void {
    const cle = P.nat === 'nuee' ? 'avec' : P.nat === 'chiche' || P.sens === 'faire' ? 'qui' : null;
    if (!cle) return;
    const L = P.nat === 'nuee' ? P.membres : P.qui;
    if (L.length || P.moi === on) return;
    P.moi = on;
    transitionPlace();
  }
  function montre(): void {
    if (inv.vis) return;
    placeMoi(true);
    const avant = copieChamp();
    inv.vis = true;
    inv.touche = false;
    inv.sortie = false;
    repeindre();
    clignote(true);
    lib.hidden = false;
    try {
      if (!reduit()) inv.trace = chargerTrace().trace(lib, null, { surFin: () => (inv.trace = null) });
    } catch {
      inv.trace = null;
    }
    if (!reduit()) {
      const z = getComputedStyle(cv).zIndex;
      const p = passageFlaques(cs, {
        mode: 'ouvre',
        rect: rectTrait(),
        image: avant,
        duree: 700,
        apres: departCv,
        z: z && z !== 'auto' ? +z : 0,
        fin: () => {
          inv.passes = inv.passes.filter((x) => x !== p);
        },
      });
      inv.passes.push(p);
    }
  }
  function retire(): void {
    if (!inv.vis) return;
    const j = ++inv.jeu;
    placeMoi(false);
    inv.trace?.stop();
    inv.trace = null;
    if (reduit()) {
      inv.vis = false;
      lib.hidden = true;
      clignote(false);
      repeindre();
      bouge(true);
      return;
    }
    // l'image SANS invite, puis le champ rendu tel qu'il est : rien ne change à l'écran dans cette tâche
    inv.vis = false;
    repeindre();
    const apres = copieChamp();
    inv.sortie = true;
    repeindre();
    clignote(false);
    let n = 0;
    let fait = 0;
    const bout = (): void => {
      if (++fait < n) return;
      if (j !== inv.jeu) return;
      inv.sortie = false;
      lib.hidden = true;
      purgeInvite();
      repeindre();
      bouge(true);
    };
    n++;
    const p = passageFlaques(cs, {
      mode: 'couvre',
      rect: rectTrait(),
      image: apres,
      duree: 300,
      apres: departCv,
      fin: bout,
    });
    inv.passes.push(p);
    n++;
    let fl = false;
    const finL = (): void => {
      if (fl) return;
      fl = true;
      bout();
    };
    try {
      inv.trace = chargerTrace().trace(lib, null, { inverse: true, surFin: finL });
    } catch {
      finL();
    }
    h.minuteur(finL, 2500);
  }
  function cacheInvite(): void {
    purgeInvite();
    arreteRuban();
    lib.style.removeProperty('clip-path');
    lib.style.removeProperty('-webkit-clip-path');
    geste = null;
    doigt = null;
    plantee = false;
    cv.style.removeProperty('transform');
    cv.style.removeProperty('transition');
    cv.style.removeProperty('transform-origin');
    cv.style.removeProperty('background-color');
    inv.trace?.stop();
    inv.trace = null;
    inv.anim = null;
    inv.vis = false;
    inv.sortie = false;
    inv.touche = false;
    inv.haut = true;
    cs.classList.add('pp-haut');
    inv.jeu++;
    lib.hidden = true;
    clignote(false);
  }
  /** le premier toucher du trait : le départ cesse de clignoter, il reste orange, fixe */
  function toucheTrait(): void {
    if (!inv.vis || inv.touche) return;
    inv.touche = true;
    clignote(false);
    repeindre();
  }
  // ── LE GESTE : PLANTER, C'EST TRACER LA MOITIÉ (C-237 ; le prototype : « LOT 1 · le geste pour PLANTER », `init(…, moitie)`) — le doigt posé
  //    sur le trait (la zone de 118 pt autour de l'onde, du départ jusqu'à 130 pt après lui) ; le plein orange suit le doigt, jamais au-delà
  //    du milieu ; 60 pt d'avancée (C-107) posent le ruban (C-148, C-154) ; un Promi et un Chiche se plantent quand le doigt atteint le milieu
  //    (195), sans attendre le lever ; un Cercle se lance au lever, son trait entier ; lâché avant, rien n'est planté : le trait revient
  //    (300 ms). ──
  const RUBAN_HAUT = 43;
  const RUBAN_BAS = 51;
  let doigt: number | null = null;
  let plantee = false;
  let geste: { id: number; x0: number; xm: number; atteint: boolean } | null = null;
  let ruban: { cv: HTMLCanvasElement; t0: number; rentre: number; mode: string; ph: number[]; fin: boolean } | null =
    null;
  const enCoordonnees = (ev: PointerEvent): { x: number; y: number } => {
    const C = cs.getBoundingClientRect();
    const k = C.width / (cs.offsetWidth || 390) || 1;
    return { x: (ev.clientX - C.left) / k, y: (ev.clientY - C.top) / k - haut0() };
  };
  /** le ruban de la création (C-148, C-154) : la couleur de l'état « en cours », 43 pt au-dessus du trait, 51 dessous, ses bords ondulent */
  function poseRuban(): void {
    if (ruban && !ruban.fin) return;
    const W = largeur();
    const base = mise.base + hzEff();
    const y0 = Math.floor(base - mise.amp - RUBAN_HAUT - 6);
    const hh = Math.ceil(2 * mise.amp + RUBAN_HAUT + RUBAN_BAS + 12);
    const dpr = Math.max(2, Math.min(3, window.devicePixelRatio || 2));
    const rc = el('canvas', { id: 'ppRuban', 'aria-hidden': 'true' });
    rc.width = Math.round(W * dpr);
    rc.height = Math.round(hh * dpr);
    rc.style.cssText = `position:absolute;left:0;top:calc(var(--pp-h) + ${String(y0)}px);width:${String(W)}px;height:${String(hh)}px;pointer-events:none;z-index:6`;
    cs.appendChild(rc);
    const R = {
      cv: rc,
      t0: h.maintenant(),
      rentre: 0,
      mode: '',
      ph: [0, 1, 2, 3].map(() => Math.random() * 6.28),
      fin: false,
    };
    ruban = R;
    const g = rc.getContext('2d')!;
    const io = (u: number): number => 1 - Math.pow(1 - Math.max(0, Math.min(1, u)), 3);
    const y = onde(base, mise.amp, W);
    const bord = (x: number, k: number, t: number): number =>
      k *
      (1.6 * Math.sin(x * 0.024 + R.ph[k > 0 ? 0 : 2]! + t * 0.9) +
        0.9 * Math.sin(x * 0.061 + R.ph[k > 0 ? 1 : 3]! - t * 1.3));
    const decoupe = (k: number): void => {
      const v = `inset(0 0 0 ${(Math.max(0, Math.min(1, k)) * 100).toFixed(1)}%)`;
      lib.style.setProperty('clip-path', v, 'important');
      lib.style.setProperty('-webkit-clip-path', v, 'important');
    };
    const dessine = (): void => {
      if (R.fin) return;
      const now = h.maintenant();
      const t = (now - R.t0) / 1000;
      const e = reduit() ? 1 : io((now - R.t0) / 200);
      let hautK = e;
      let basK = e;
      if (R.rentre) {
        const r = reduit() ? 1 : io((now - R.rentre) / 240);
        hautK = e * (1 - r);
        if (R.mode !== 'valide') {
          basK = e * (1 - r);
          decoupe(basK);
        }
        if (r >= 1 && R.mode !== 'valide') {
          arreteRuban();
          return;
        }
      } else decoupe(e);
      g.setTransform(dpr, 0, 0, dpr, 0, -y0 * dpr);
      g.clearRect(0, y0, W, hh);
      g.beginPath();
      g.moveTo(-2, y(0) - RUBAN_HAUT * hautK + bord(0, 1, t) * hautK);
      for (let x = 4; x <= W + 2; x += 4) g.lineTo(x, y(Math.min(W, x)) - RUBAN_HAUT * hautK + bord(x, 1, t) * hautK);
      for (let x = W + 2; x >= -2; x -= 4)
        g.lineTo(x, y(Math.max(0, Math.min(W, x))) + RUBAN_BAS * basK + bord(x, -1, t) * basK);
      g.closePath();
      g.fillStyle = palette.mauve12;
      g.fill();
      h.image(dessine);
    };
    dessine();
  }
  function arreteRuban(): void {
    if (!ruban) return;
    ruban.fin = true;
    ruban.cv.remove();
    // une plantation : le mot reste découpé jusqu'à la fermeture de la page ; sinon il revient
    if (ruban.mode !== 'valide') {
      lib.style.removeProperty('clip-path');
      lib.style.removeProperty('-webkit-clip-path');
    }
    ruban = null;
  }
  function rentreRuban(mode: 'valide' | 'annule'): void {
    if (!ruban || ruban.rentre) return;
    ruban.mode = mode;
    ruban.rentre = h.maintenant();
  }
  cs.addEventListener(
    'pointerdown',
    (ev) => {
      if (!inv.vis || plantee || geste || mv || choix !== null || saisieDe !== null || peaufOuvert || menu) return;
      const { x, y } = enCoordonnees(ev);
      const W = largeur();
      if (Math.abs(y - onde(mise.base + hzEff(), mise.amp, W)(x)) > 59) return;
      if (x > (W * 42) / 308 + 130) return;
      toucheTrait();
      geste = { id: ev.pointerId, x0: x, xm: x, atteint: false };
      doigt = Math.max(0, Math.min(W, x));
      repeindre();
      ev.preventDefault();
      ev.stopPropagation();
    },
    true,
  );
  window.addEventListener('pointermove', (ev) => {
    if (!geste || ev.pointerId !== geste.id || plantee) return;
    const { x } = enCoordonnees(ev);
    const W = largeur();
    geste.xm = Math.max(geste.xm, x);
    doigt = Math.max(0, Math.min(W, x));
    const avance = geste.xm - geste.x0;
    if (!geste.atteint && avance >= 60) {
      geste.atteint = true;
      poseRuban();
    }
    if (P.nat !== 'nuee' && doigt >= W / 2 - 2 && avance >= 60) {
      doigt = W / 2;
      geste = null;
      planter();
      return;
    }
    repeindre();
  });
  const leve = (ev: PointerEvent): void => {
    if (!geste || ev.pointerId !== geste.id) return;
    const g = geste;
    geste = null;
    if (P.nat === 'nuee' && g.xm - g.x0 >= 60) {
      doigt = largeur();
      planter();
      return;
    }
    // lâché avant : rien n'est planté, le trait revient (300 ms)
    rentreRuban('annule');
    const d0 = doigt ?? 0;
    const t0 = h.maintenant();
    const r = (): void => {
      if (geste || plantee) return;
      const u = Math.min(1, (h.maintenant() - t0) / 300);
      doigt = u < 1 ? d0 * (1 - u) : null;
      repeindre();
      if (u < 1) h.image(r);
    };
    r();
  };
  window.addEventListener('pointerup', leve);
  window.addEventListener('pointercancel', leve);
  /** PLANTER (C-226 : la parole écrite dans la tâche du trait, avant toute animation) */
  function planter(): void {
    if (plantee) return;
    plantee = true;
    rentreRuban('valide');
    const maintenant = Date.now();
    if (P.nat === 'nuee') {
      const cle = magasin.creerCercle(P.nom.trim(), autres(P.membres), maintenant, P.dessin);
      facade.planterCercle(cle);
      repeindre();
      // le prototype (`printTirage`) : le champ grandit (× 7, 320 ms, linéaire) jusqu'à couvrir l'écran, puis on coupe
      cv.style.transformOrigin = '68% 40%';
      cv.style.transition = 'transform .32s linear -17ms, background-color .32s linear -17ms';
      cv.style.transform = 'scale(7)';
      cv.style.backgroundColor = palette.mauve86;
      h.minuteur(() => {
        fermer(true);
      }, 400);
      return;
    }
    const W = largeur();
    const id = magasin.etat().compteurs.nid;
    const titre = P.titre.trim();
    const who = autres(P.qui).length ? autres(P.qui).join(', ') : 'moi';
    const k = dv.getBoundingClientRect().width / (dv.offsetWidth || 390) || 1;
    const E = Math.min(2, window.devicePixelRatio || 1) * k;
    const w0 = 241;
    // la dalle d'avance, rendue AVANT que le moteur reçoive la parole : la même image que le haut de la page + (C-241)
    const pre = facade.dalleAvenir(id, w0 * E, 1e5, { chiche: P.nat === 'chiche', title: titre, who });
    magasin.planter(
      {
        titre,
        who,
        chiche: P.nat === 'chiche',
        sens: P.sens,
        avec: autres(P.avec).join(', '),
        note: P.note,
        monde: facade.mondeCourant(),
        due: P.due,
        dueISO: P.dueISO,
        cercle: P.cercle,
        fichiers: P.fichiers.slice(),
        dessin: P.dessin,
      },
      maintenant,
    );
    facade.planterUne(id);
    repeindre();
    const by = haut0() + onde(mise.base + hzEff(), mise.amp, W)(W / 2);
    if (!pre) {
      fermer(true);
      return;
    }
    planteNait({
      dv,
      facade,
      h,
      id,
      pre,
      bx: W / 2,
      by,
      w: w0,
      fermer: () => {
        fermer(true);
      },
      fin: () => {},
    });
  }

  /** la veille (toutes les 50 ms, la page + ouverte) : la parole prête et validée, l'horizon remonte puis le trait naît ; incomplète, il repart */
  h.intervalle(() => {
    if (cs.hidden || cs.classList.contains('pp-part') || cs.classList.contains('pp-entre')) return;
    if (mv || saisieDe !== null || choix !== null || peaufOuvert || menu) return;
    if (!prete()) {
      if (inv.vis) retire();
      else if (!inv.haut && !inv.anim && !inv.sortie) bouge(true);
      return;
    }
    if (inv.vis || inv.sortie || inv.anim) return;
    if (h.maintenant() - derniereCompo < 160) return;
    if (inv.haut) bouge(false, montre);
    else montre();
  }, 50);

  // ── LA COMPOSITION ──
  function composer(): void {
    const ad = douceur.avant();
    const av = continu.avant();
    try {
      composerBrut();
    } finally {
      douceur.apres(ad);
      continu.apres(av);
    }
  }
  function composerBrut(): void {
    // la mise en page « ouverte » (cadres 18 à 23) : un choix des personnes, ou la saisie d'un mot ; la barre Peaufiner se cache pendant la
    // saisie d'un Promi ou d'un Chiche (§2.11, le seul cas du produit) — un Cercle la garde (le prototype, `pp-saisie` sur #csChoix)
    const ouvert = choix !== null || saisieDe !== null;
    const enSaisie = saisieDe !== null && P.nat !== 'nuee';
    // un Promi rangé dans un Cercle (Peaufiner, DANS UN CERCLE : le prototype `cs-nuee`) : la barre Peaufiner prend l'écriture d'un Cercle
    cs.classList.toggle('pp-dans-cercle', P.nat === 'promi' && !!P.cercle);
    const dh = haut0();
    // les mesures se lisent sur la mise en page : un mouvement en cours (une translation) est mis de côté le temps de composer
    const enCours = [phrase, garder].map((e) => [e, e.style.translate] as const);
    for (const [e] of enCours) e.style.removeProperty('translate');
    // « garder de côté » se MESURE (C-240 : la phrase laisse la place du rail au-dessus de lui) : caché, il n'aurait pas de boîte — il est
    // posé le temps de composer (aucune image ne passe), sa visibilité est décidée plus bas
    garder.hidden = false;
    cs.classList.remove(...NATURES.map((n) => 'pp-' + n));
    cs.classList.add('pp-' + P.nat);
    cs.classList.toggle('pp-ouvert', ouvert);
    cs.classList.toggle('pp-saisie', enSaisie);
    phrase.id = P.nat === 'nuee' ? 'nueePhrase' : 'csPhrase';
    choixHote.id = P.nat === 'nuee' ? 'nueeChoix' : 'csChoix';
    mot.innerHTML = '';
    if (P.nat === 'promi') {
      mot.append(T.mots.promi);
      const i = el('i', { class: 'mm-i' });
      i.textContent = T.mots.promiI;
      mot.appendChild(i);
    } else mot.textContent = P.nat === 'chiche' ? T.mots.chiche : T.mots.nuee;
    // le X face au mot-marque, centré sur ses capitales, à la taille des titres (lot-V157-CROIX, comme la fiche)
    poserCroix(croix, croixG, mot);

    let cap = 0;
    let r = composerPhrase(ouvert, cap);
    let base = 0;
    let amp = 36;
    for (let essai = 0; essai < 20; essai++) {
      base = ouvert ? 144 : Math.max(196, 344 - 32 * (r.nl - 1));
      amp = ouvert ? 16 : 36;
      const boite = base + amp + 60;
      phrase.style.top = `calc(var(--pp-h) + ${String(ouvert ? 228 + DT : boite + 6 + DY_PHRASE[P.nat] + DT)}px)`;
      if (ouvert) break;
      // le titre écrit trop haut pour la page : il se réduit (et la phrase avec lui) ; ses lignes changent, la page se recompose
      if (titrePlein(r)) {
        const nl = lignes();
        if (nl !== r.nl) {
          r = { ...r, nl };
          continue;
        }
      }
      // C-240 : la place du rail et de son air au-dessus de « garder de côté »
      const gTop = garder.getBoundingClientRect().top - cs.getBoundingClientRect().top;
      const trop = basEncre() - DY_PHRASE[P.nat] + 12 + 44 + 12 - gTop;
      if (trop <= 0.5 || r.taille <= 16) break;
      cap = r.taille - 1;
      r = composerPhrase(ouvert, cap);
    }
    // la dalle : sa taille se fixe à la première composition de l'ouverture, sur la base au repos (C-234)
    if (!dalleT || dalleT.nat !== P.nat) {
      const bR = Math.max(196, 344 - 32 * (r.nl - 1));
      const h0 = Math.min(300, bR - 112);
      dalleT = { h: h0, w: Math.min(320, Math.floor(1.2 * h0)), nat: P.nat };
    }
    // C-229 : l'horizon bas, 12 pt au-dessus de l'encre de la phrase au plus
    const C = cs.getBoundingClientRect();
    let hautPills = 1e9;
    for (const n of txt.querySelectorAll(':scope > .ph-m, :scope > .ph-b')) {
      const q = n.getBoundingClientRect();
      if (q.width) hautPills = Math.min(hautPills, q.top - C.top - dh);
    }
    const W = largeur();
    hzC = Math.max(0, Math.min(HZ_BAS, Math.floor((hautPills - HZ_AIR - basOnde(onde(base, amp, W), W)) * 2) / 2));
    const hz = hzEff();
    peindreChamp(base, amp, hz, base + amp + 60 + hz);
    poseLibelle(base, amp, ouvert);
    derniereCompo = h.maintenant();
    photo.style.top = `calc(var(--pp-h) + ${String(hautBouton(base, amp))}px)`;
    mise = { base, amp, hz, nl: r.nl, taille: r.taille };
    // le rail : à mi-chemin, à l'encre, entre la phrase et « garder de côté » (il se compte comme si la phrase n'avait pas remonté) ;
    // ce qui part en flaques (un mouvement l'a pris) n'est pas caché d'un coup sous lui
    if (!sortants.has(pinceau)) pinceau.hidden = ouvert;
    if (!sortants.has(garder)) garder.hidden = ouvert;
    if (!sortants.has(barre)) barre.hidden = enSaisie;
    if (!ouvert) {
      let dessus = 0;
      for (const n of txt.querySelectorAll(':scope > .ph-m, :scope > .ph-b')) {
        const q = n.getBoundingClientRect();
        if (q.width) dessus = Math.max(dessus, q.bottom - C.top);
      }
      dessus -= DY_PHRASE[P.nat];
      const dessous = garder.getBoundingClientRect().top - C.top + INK_LIEN - 10;
      pinceau.style.top = `${String(Math.round((dessus + (dessous - dessus - 44) / 2) * 4) / 4)}px`;
    }
    majRail();
    majGarder();
    rendreChoix();
    rendreDeja();
    for (const [e, v] of enCours) if (v) e.style.setProperty('translate', v);
  }

  // ── LES MOUVEMENTS (C-271 : rien ne paraît ni ne part d'un coup) ──
  const reduit = (): boolean => {
    try {
      return matchMedia('(prefers-reduced-motion: reduce)').matches;
    } catch {
      return false;
    }
  };
  const passages = new Map<HTMLElement, ControlePassage>();
  /** une chose paraît ou part EN FLAQUES (C-329) : la scène du passage, posée en masque sur la chose elle-même, 300 ms */
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
  function partir(e: HTMLElement): void {
    if (e.hidden) return;
    sortants.add(e);
    enFlaques(e, 'part', () => {
      sortants.delete(e);
      e.hidden = true;
    });
  }
  function paraitre(e: HTMLElement): void {
    sortants.delete(e);
    e.hidden = false;
    enFlaques(e, 'paraît');
  }
  /** Q598, C-234 : 360 ms, la courbe de l'horizon (aller-retour quadratique) */
  const DUREE_MV = 360;
  /** la barre Peaufiner sort par le bas pendant la saisie, et revient d'où elle est partie (884 → 760 dans le prototype) */
  const BARRE_BAS = 124;
  const doux = (p: number): number => (p < 0.5 ? 2 * p * p : 1 - (-2 * p + 2) ** 2 / 2);
  const ty = (e: HTMLElement): number => {
    const m = /(-?[\d.]+)px\s*$/.exec(e.style.translate || '');
    return m ? +m[1]! : 0;
  };
  const glisse = (e: HTMLElement, y: number): void => {
    if (Math.abs(y) < 0.01) e.style.removeProperty('translate');
    else e.style.setProperty('translate', `0 ${String(Math.round(y * 100) / 100)}px`);
  };

  /**
   * Recomposer la page, et — quand la mise en page « ouverte » change (la saisie, un choix) — y aller d'un MOUVEMENT (Q598, v177a ; C-234,
   * v180b) : l'onde va de sa place vue à la nouvelle, repeinte à chaque image ; la phrase et le bouton photo glissent ; le rail et « garder
   * de côté » partent en flaques (ils reviennent en flaques en glissant avec la phrase) ; la barre Peaufiner descend sous l'écran pendant la
   * saisie et remonte du bas ; « DÉJÀ PROMIS » paraît en flaques, et à la fermeture sa copie descend (C-303 : posée dans la tâche même de la
   * validation, elle ne disparaît jamais d'un coup). Réduire les animations : la page se pose.
   */
  function recomposer(anime: boolean): void {
    const ouvAv = cs.classList.contains('pp-ouvert');
    const saiAv = cs.classList.contains('pp-saisie');
    const av = { ph: phrase.offsetTop + ty(phrase), photo: photo.offsetTop + ty(photo), barre: ty(barre), ...vue };
    const fermeSaisie = !deja.hidden && saisieDe === null;
    let copie: HTMLElement | null = null;
    if (anime && !reduit() && fermeSaisie) {
      copie = deja.cloneNode(true) as HTMLElement;
      copie.classList.add('ppo-copie');
      copie.setAttribute('aria-hidden', 'true');
      copie.style.top = `${String(av.ph + (decDeja ?? 0) + ty(deja))}px`;
      copie.style.removeProperty('translate');
      cs.appendChild(copie);
    }
    if (mv) {
      h.annuleImage(mv.id);
      mv.fin();
      mv = null;
    }
    const versOuvert = choix !== null || saisieDe !== null;
    const versSaisie = saisieDe !== null && P.nat !== 'nuee';
    const bouge = anime && !reduit() && (versOuvert !== ouvAv || versSaisie !== saiAv);
    // ce qui va partir reste à l'écran le temps de son passage
    if (bouge && versOuvert && !ouvAv) for (const e of [pinceau, garder]) if (!e.hidden) sortants.add(e);
    if (bouge && versSaisie && !saiAv && !barre.hidden) sortants.add(barre);
    for (const e of [phrase, photo, pinceau, garder]) e.style.removeProperty('translate');
    composer();
    vue = { base: mise.base, amp: mise.amp, hz: mise.hz };
    if (!bouge) {
      copie?.remove();
      glisse(barre, 0);
      return;
    }
    const ap = { ph: phrase.offsetTop, photo: photo.offsetTop };
    const dPh = av.ph - ap.ph;
    const dPhoto = av.photo - ap.photo;
    const barreSort = versSaisie && !saiAv;
    const barreRevient = !versSaisie && saiAv;
    const reviennent = !versOuvert && ouvAv;
    if (versOuvert && !ouvAv) {
      for (const e of [pinceau, garder]) if (sortants.has(e)) partir(e);
      if (!deja.hidden) enFlaques(deja, 'paraît');
    }
    if (reviennent) for (const e of [pinceau, garder]) paraitre(e);
    const fin = { base: mise.base, amp: mise.amp, hz: mise.hz };
    const H0 = av.base + av.amp + 60 + av.hz;
    const H1 = fin.base + fin.amp + 60 + fin.hz;
    const t0 = h.maintenant();
    const bas = cs.offsetHeight - av.ph;
    const pas = (): void => {
      const p = Math.min(1, (h.maintenant() - t0) / DUREE_MV);
      const e = doux(p);
      const l = (a: number, b: number): number => a + (b - a) * e;
      vue = { base: l(av.base, fin.base), amp: l(av.amp, fin.amp), hz: l(av.hz, fin.hz) };
      peindreChamp(vue.base, vue.amp, vue.hz, l(H0, H1), true);
      glisse(phrase, dPh * (1 - e));
      glisse(photo, dPhoto * (1 - e));
      if (reviennent) for (const x of [pinceau, garder]) glisse(x, dPh * (1 - e));
      if (barreSort) glisse(barre, l(av.barre, BARRE_BAS));
      if (barreRevient) glisse(barre, l(av.barre || BARRE_BAS, 0));
      if (copie) glisse(copie, e * bas);
      if (p < 1) mv = { id: h.image(pas), fin: finir };
      else finir();
    };
    const finir = (): void => {
      mv = null;
      for (const x of [phrase, photo, pinceau, garder]) x.style.removeProperty('translate');
      if (barreSort) {
        sortants.delete(barre);
        barre.hidden = saisieDe !== null && P.nat !== 'nuee';
      }
      glisse(barre, barre.hidden ? 0 : 0);
      copie?.remove();
      vue = { base: mise.base, amp: mise.amp, hz: mise.hz };
      peindreChamp(mise.base, mise.amp, mise.hz, mise.base + mise.amp + 60 + mise.hz);
    };
    pas();
  }

  // ── « DÉJÀ PROMIS » (§5, `panneau` du prototype) : pendant la saisie d'un titre, les paroles déjà promises (les deux plus récentes, jamais
  //    le titre en cours), à reprendre d'un toucher ; le libellé 30 pt sous la phrase (420 sur le cadre), les pastilles 26 pt plus bas ──
  function rendreDeja(): void {
    deja.innerHTML = '';
    if (saisieDe !== 'titre') {
      deja.hidden = true;
      decDeja = null;
      return;
    }
    const etaitLa = !deja.hidden;
    deja.hidden = false;
    const C = phrase.getBoundingClientRect();
    const k = C.width / (phrase.offsetWidth || 1) || 1;
    let fin = 0;
    for (const n of txt.querySelectorAll(':scope > .ph-m, :scope > .ph-b')) {
      const q = n.getBoundingClientRect();
      if (q.height) fin = Math.max(fin, (q.bottom - C.top) / k);
    }
    // le prototype compte depuis le haut de sa phrase au cadre 18 (280) : libellé à 420, pastilles à 446, décalés si la phrase est plus longue
    const dec = Math.max(0, Math.round(280 + fin + 30) - 420);
    // la phrase gagne ou perd une ligne en cours de frappe : « DÉJÀ PROMIS » GLISSE à sa nouvelle place (320 ms, C-278 ④), jamais d'un saut
    const ancien = decDeja;
    decDeja = dec;
    deja.style.top = `${String(dec)}px`;
    if (etaitLa && ancien != null && ancien !== dec && !reduit()) {
      const de = ancien - dec;
      const t0 = h.maintenant();
      const pas = (): void => {
        if (decDeja !== dec) return;
        const p = Math.min(1, (h.maintenant() - t0) / 320);
        glisse(deja, de * (1 - doux(p)));
        if (p < 1) h.image(pas);
      };
      pas();
    } else if (!etaitLa || ancien !== dec) glisse(deja, 0);
    // (même place : le glissement en cours continue)
    const lab = el('div', { class: 'ppo-deja' });
    lab.textContent = T.dejaPromis;
    lab.style.top = '140px';
    const rang = el('div', { class: 'ppo-dejarow' });
    rang.style.top = '166px';
    const cour = P.titre.trim();
    const mots: string[] = [];
    for (const q of [...magasin.etat().paroles].reverse()) {
      const t = (q.title || '').trim();
      if (t && t !== cour && !mots.includes(t) && mots.length < 2) mots.push(t);
    }
    for (const m of mots) {
      const b = el('span', { class: 'ppo-d', role: 'button' });
      b.textContent = m;
      surToucher(b, () => {
        // reprendre un mot : il devient le titre (la frappe, comme si on l'avait tapé)
        saisie.value = m;
        saisie.dispatchEvent(new Event('input', { bubbles: true }));
      });
      rang.appendChild(b);
    }
    deja.append(lab, rang);
    // les mots sont ceux de l'utilisateur : deux pastilles qui ne tiennent pas dans la largeur (342 à la taille de référence), on n'en garde qu'une
    while (rang.children.length > 1 && rang.scrollWidth > Math.min(342, largeur() - 48)) rang.lastChild!.remove();
  }

  function majRail(): void {
    for (const b of rail.children) {
      const on = (b as HTMLElement).dataset['t'] === P.pinceau;
      b.classList.toggle('on', on);
      // l'état du choix, dit à VoiceOver (et aux juges : un pinceau déjà choisi n'a rien à changer)
      if (!b.classList.contains('pc-mur')) b.setAttribute('aria-pressed', on ? 'true' : 'false');
    }
  }

  // ── « GARDER DE CÔTÉ » (C-149) : actif quand la page a changé depuis son ouverture ──
  const signature = (): string =>
    [
      P.nat,
      P.sens,
      P.titre.trim(),
      P.qui.join('|'),
      P.avec.join('|'),
      P.nom.trim(),
      P.membres.join('|'),
      P.pinceau,
      P.note,
      P.photo ? P.photo.length : 0,
      P.dessin ? JSON.stringify(P.dessin).length : 0,
      P.ech,
      P.dueISO ?? '',
      P.cercle ?? '',
      P.fichiers.join('|'),
    ].join('¦');
  function majGarder(): void {
    const actif = signature() !== signature0;
    garder.classList.toggle('inactif', !actif);
    garder.setAttribute('aria-disabled', actif ? 'false' : 'true');
    // ⚑ C-330 (Tom, 22 nov. 2026) : inactif, il prend la teinte de SA NATURE — #82AEF8 · #FFB8D2 · #C9A8F5 (le champ). Le prototype le
    // sort bleu ou lilas selon une course : l'app ne copie pas ce défaut (écart admis, nommé dans le test d'identité)
    if (actif) garder.style.removeProperty('color');
    else garder.style.setProperty('color', CHAMP[P.nat]);
  }
  surToucher(garder, () => {
    if (garder.classList.contains('inactif')) return;
    const b: Brouillon = {
      v: 1,
      nat: P.nat,
      phrase: {
        sens: P.nat === 'chiche' ? 'chiche' : P.sens === 'demander' ? 'demander' : 'faire',
        titre: P.titre,
        qui: P.qui.join(', ') || 'Moi',
        avec: P.avec.join(', '),
        // la photo et le dessin de la bande (le prototype : `_phrase` entière, `photo` et `dessin` compris) : la reprise les rend
        photo: P.photo,
        dessin: P.dessin,
      },
      who: autres(P.qui),
      sens: P.sens,
      nom: P.nom.trim(),
      membres: autres(P.membres),
      pinceau: P.pinceau,
      note: P.note,
      // le prototype (`lot-V162-GARDER`) : l'état ENTIER — l'échéance, le Cercle, les pièces jointes
      due: P.due,
      dueISO: P.dueISO,
      cercle: P.cercle,
      fichiers: P.fichiers.slice(),
      // les listes telles que la page les tient (« Moi » compris), pour une reprise exacte
      quiListe: P.qui.slice(),
      avecListe: P.avec.slice(),
      membresListe: P.membres.slice(),
      moi: P.moi,
      ech: P.ech,
      echChoisie: P.echChoisie,
    };
    const titre = (P.nat === 'nuee' ? P.nom : P.titre).trim() || T.sansTitre;
    const qui = autres(P.qui).length ? autres(P.qui).join(', ') : 'moi';
    magasin.garderDeCote(b, titre, P.nat === 'nuee' ? T.leGroupe : qui, repris, Date.now());
    fermer();
  });

  // ── LE CHOIX DES PERSONNES (lot-GENS) : « Moi » ou « tout le monde » en tête, les connus, « + ajouter quelqu'un » ──
  function connus(): string[] {
    const e = magasin.etat();
    const out: string[] = [];
    const vu = (n: string): void => {
      const m = n.trim();
      if (m && !/^(moi|le groupe|tout le monde)$/i.test(m) && !out.includes(m)) out.push(m);
    };
    for (const p of [...e.paroles].reverse())
      for (const w of [p.who, p.from, (p.suite?.['avec'] as string | undefined) ?? ''])
        for (const n of String(w ?? '').split(/\s*[,·]\s*/)) vu(n);
    for (const v of e.personnes) if (typeof v === 'string') for (const n of v.split(/\s*[,·]\s*/)) vu(n);
    for (const l of Object.values(e.membres)) for (const n of l) vu(n);
    return out;
  }
  const liste = (): string[] => (choix === 'qui' ? P.qui : choix === 'avec' ? P.avec : P.membres);
  /** C-332 : une personne ajoutée à côté de « Moi » seul (la liste vide) ne le retire pas — sauf « promets-moi » (on demande à d'autres)
   *  et « avec qui en est ? » d'un Chiche (pas de « Moi » dans ce choix) */
  function ajouterA(L: string[], n: string): void {
    if (!L.length && choix !== 'avec' && !(choix === 'qui' && P.nat === 'promi' && P.sens === 'demander')) L.push(MOI);
    L.push(n);
  }
  /**
   * un changement du choix des personnes : la liste change tout de suite (les pastilles avec elle) ; la place de la phrase se DÉTRACE pendant
   * que son encart change de largeur, puis la neuve se TRACE (C-279, C-271 : aucun changement sec — douceur.ts). Un toucher pendant la
   * transition change la liste : elle finit sur ce qui est coché à ce moment-là.
   */
  function changerPersonnes(mut: (L: string[]) => void): void {
    const cle = choix;
    if (!cle) return;
    const L = liste();
    mut(L);
    // « Moi » seul n'est pas une personne ajoutée : la liste redevient vide, la place dit « moi » en pointillés (C-304)
    if (L.length === 1 && L[0] === MOI) {
      L.splice(0);
      P.moi = true;
    }
    transitionPlace(rendreChoix);
  }
  /** une place de la phrase change (son état est déjà écrit) : la phrase se recompose ; la transition (détracé, encart, flaques, tracé) est
   *  celle de toute reconstruction (douceur.ts, le prototype `lot-V200-DOUCEUR`) */
  function transitionPlace(pendant?: () => void): void {
    pendant?.();
    composer();
  }
  function rendreChoix(): void {
    choixHote.innerHTML = '';
    choixHote.classList.toggle('ouvert', choix !== null);
    if (!choix) {
      if (ajoutActif) {
        ajoutActif = false;
        gnIn.value = '';
        if (document.activeElement === gnIn) gnIn.blur();
        gnIn.hidden = true;
        suisClavier();
      }
      return;
    }
    const pris = liste();
    const noms = autres(pris);
    for (const n of connus()) if (!noms.includes(n) && noms.length < autres(pris).length + 6) noms.push(n);
    const gn = el('div', { class: 'ph-opts gn', 'data-nat': P.nat });
    const gl = el('div', { class: 'gn-liste' });
    // « Moi » en tête, choisi tant que personne d'autre (C-269, v199) — dans un Cercle aussi (le prototype : la place « avec » passe à « moi »)
    const teteOn = !pris.length || pris.includes(MOI);
    const bouton = (nom: string, on: boolean, tetee: boolean): HTMLElement => {
      const b = el('button', { type: 'button', class: 'ph-o' + (on ? ' on' : '') });
      if (tetee) b.dataset['gnTete'] = '1';
      else b.dataset['v'] = nom;
      const ini = el('span', { class: 'ppo-ini' });
      ini.textContent = nom.charAt(0).toUpperCase();
      b.appendChild(ini);
      const nm = el('span', { class: 'ppo-nom' });
      nm.textContent = nom;
      b.appendChild(nm);
      if (on) {
        const x = el('span', { class: 'ppo-x', role: 'button', 'aria-label': `${T.retirer} ${nom.toLowerCase()}` });
        x.innerHTML = SVG_X;
        b.appendChild(x);
      }
      surToucher(b, (ev) => {
        changerPersonnes((L) => {
          if (tetee) {
            // C-332 : « Moi » se décoche (s'il reste seul, la liste vide le remet : jamais vide) ou se remet, à côté des autres
            if (L.includes(MOI)) L.splice(L.indexOf(MOI), 1);
            else if (L.length) L.unshift(MOI);
          } else if ((ev.target as Element).closest('.ppo-x') || L.includes(nom)) L.splice(L.indexOf(nom), 1);
          else ajouterA(L, nom);
        });
      });
      return b;
    };
    // « avec qui en est ? » d'un Chiche n'a pas de « Moi » en tête (le prototype : `tete: (champ === 'qui') ? 'Moi' : null`)
    if (choix !== 'avec') gl.appendChild(bouton(T.moi, teteOn, true));
    for (const n of noms) gl.appendChild(bouton(n, pris.includes(n), false));
    const ajout = el('div', { class: 'ph-o ph-add', role: 'button', tabindex: '0', 'data-add': '1' });
    rendreAjout(ajout);
    surToucher(ajout, (ev) => {
      if ((ev.target as Element).closest('.gn-plus')) {
        validerAjout();
        return;
      }
      ouvrirAjout();
    });
    gn.append(gl, ajout);
    choixHote.appendChild(gn);
    // sous la phrase (28 pt d'air ; 25 sous celle d'un Cercle, `#nueeChoix .gn{margin-top:25px}`) ; la liste montre autant de RANGÉES
    // entières que la place en laisse pour que « + ajouter quelqu'un » reste au-dessus de la barre Peaufiner, 16 pt d'air (v116,
    // `_gensBorne`) — elle défile pour le reste
    const haut = txt.offsetHeight + (P.nat === 'nuee' ? 25 : 28);
    gn.style.top = `${String(haut)}px`;
    const debut = phrase.offsetTop + haut;
    // (la cote de MISE EN PAGE de la barre : un mouvement en cours la translate)
    const finBarre = barre.offsetTop - 16;
    let n = 1;
    while (debut + 52 * (n + 1) + 8 * n + 8 + 14 + 52 <= finBarre) n++;
    gl.style.maxHeight = `${String(52 * n + 8 * (n - 1))}px`;
    posePrenom();
  }

  // ── C-122 (v146) — AJOUTER UNE PERSONNE : on écrit DANS la zone en pointillés (aucun second encart) ; le nom à l'encre du mode, le mot
  //    d'attente « un prénom… » dans la teinte de la zone ; dès la première lettre, un « + » orange (`--c-orange-depart`), tracé, à la hauteur
  //    des capitales du nom, valide (Retour aussi) ; le nom validé est posé, la zone se propose pour le suivant ; le clavier reste. ──
  function rendreAjout(z: HTMLElement): void {
    // C-271 (v203 clôture §2) : « + ajouter quelqu’un » ↔ la ligne de saisie, l'ancien se détrace et le neuf se trace ; « un prénom… » part et
    // revient par le tracé — rien ne change d'un coup
    const etaitEdit = z.classList.contains('gn-edit');
    const phAvant = z.querySelector<HTMLElement>('.gn-ph');
    if (!ajoutActif) {
      const bouton = (): void => {
        delete z.dataset['v'];
        z.className = 'ph-o ph-add';
        z.setAttribute('role', 'button');
        z.removeAttribute('aria-label');
        z.textContent = T.ajouter;
      };
      if (etaitEdit) remplacer(z, bouton);
      else bouton();
      return;
    }
    const v = gnIn.value;
    const nom = v.replace(/\s+/g, ' ').trim();
    // rien n'a changé (un focus, le clavier qui bouge) : la ligne reste — rebâtie, elle perdrait son tracé en cours (il paraîtrait d'un coup)
    if (etaitEdit && z.dataset['v'] === v) {
      z.classList.toggle('gn-repos', document.activeElement !== gnIn);
      return;
    }
    z.dataset['v'] = v;
    if (etaitEdit && phAvant && v) detracerCopie(phAvant);
    const devientEdit = !etaitEdit && !!(z.textContent ?? '').trim();
    const copie = devientEdit && !reduit() && z.getClientRects().length ? copieA(z) : null;
    z.className = 'ph-o ph-add gn-edit' + (document.activeElement === gnIn ? '' : ' gn-repos');
    z.setAttribute('role', 'group');
    z.setAttribute('aria-label', T.ajouterQuelquun);
    const ligne = el('span', { class: 'gn-ligne' });
    const t = el('span', { class: 'gn-txt' });
    t.textContent = v;
    const car = el('i', { class: 'ph-caret', 'aria-hidden': 'true' });
    ligne.append(t, car);
    if (!v) {
      const ph = el('span', { class: 'gn-ph' });
      ph.textContent = T.unPrenom;
      ligne.appendChild(ph);
    }
    if (nom) {
      const pl = el('span', { class: 'gn-plus', role: 'button', 'aria-label': `${T.ajouterNom} ${nom}` });
      pl.innerHTML = SVG_PLUS;
      // un toucher sur le « + » ne prend pas le focus au champ (sinon le clavier clignote, des lettres se perdent : v146)
      pl.addEventListener('mousedown', (ev) => {
        ev.preventDefault();
      });
      ligne.appendChild(pl);
    }
    z.replaceChildren(ligne);
    if (copie) {
      const fin = (): void => {
        copie.remove();
      };
      const tl = chargerTrace();
      tl.trace(ligne, null);
      tl.trace(copie, null, { inverse: true, surFin: fin });
      h.minuteur(fin, 2500);
    } else if (etaitEdit && !phAvant && !v && !reduit()) {
      const ph = ligne.querySelector<HTMLElement>('.gn-ph');
      if (ph) chargerTrace().trace(ph, null);
    }
    // (le « + » se mesure sur la police du nom RENDUE : une fois la ligne posée)
    const pl = ligne.querySelector<HTMLElement>('.gn-plus');
    if (pl) {
      dessinePlus(pl, t, !plusVu);
      plusVu = true;
    } else plusVu = false;
  }
  let plusVu = false;
  /** le « + » : la hauteur des capitales du nom, l'épaisseur de son fût (lues sur sa police) ; il se TRACE (deux traits nets, sans fondu) */
  function dessinePlus(pl: HTMLElement, t: HTMLElement, anime: boolean): void {
    const s = getComputedStyle(t);
    const f = `${s.fontWeight} ${s.fontSize} ${s.fontFamily}`;
    const fs = parseFloat(s.fontSize) || 16;
    let cap = fs * 0.78;
    let fut = fs * 0.2;
    const g = document.createElement('canvas').getContext('2d');
    if (g) {
      g.font = f;
      const H = g.measureText('H');
      const L = g.measureText('l');
      const a = Math.max(H.actualBoundingBoxAscent || 0, L.actualBoundingBoxAscent || 0);
      if (a > 4) cap = a;
      const w = (L.actualBoundingBoxLeft || 0) + (L.actualBoundingBoxRight || 0);
      if (w > 1 && w < cap * 0.5) fut = w;
    }
    const sv = pl.querySelector('svg');
    if (!sv) return;
    sv.setAttribute('width', cap.toFixed(2));
    sv.setAttribute('height', cap.toFixed(2));
    const ep = Math.max(1.6, Math.min(3.4, (fut / cap) * 10));
    const [hb, vb] = [sv.querySelector<SVGPathElement>('.h'), sv.querySelector<SVGPathElement>('.v')];
    for (const q of [hb, vb]) {
      q?.setAttribute('stroke-width', ep.toFixed(2));
      q?.setAttribute('stroke-dasharray', '10');
      q?.setAttribute('stroke-dashoffset', anime && !reduit() ? '10' : '0');
    }
    if (!anime || reduit()) return;
    const t0 = h.maintenant();
    const D = 120;
    const pas = (): void => {
      const tt = h.maintenant() - t0;
      const a = Math.min(1, tt / D);
      const b = Math.min(1, Math.max(0, (tt - D * 0.7) / D));
      hb?.setAttribute('stroke-dashoffset', (10 * (1 - a)).toFixed(2));
      vb?.setAttribute('stroke-dashoffset', (10 * (1 - b)).toFixed(2));
      if (b < 1 && pl.isConnected) h.image(pas);
    };
    h.image(pas);
  }
  const zoneAjout = (): HTMLElement | null => choixHote.querySelector<HTMLElement>('.ph-add');
  function ouvrirAjout(): void {
    if (!ajoutActif) {
      ajoutActif = true;
      gnIn.value = '';
      plusVu = false;
    }
    gnIn.hidden = false;
    // le focus DANS le geste : iOS n'ouvre le clavier qu'ainsi (v115)
    gnIn.focus({ preventScroll: true });
    const z = zoneAjout();
    if (z) rendreAjout(z);
    posePrenom();
    suisClavier();
  }
  function validerAjout(): void {
    let n = gnIn.value.replace(/\s+/g, ' ').trim();
    if (!n || !choix) return;
    // un nom déjà connu garde SON écriture (« rachel » → « Rachel »)
    for (const c of connus()) if (c.toLowerCase() === n.toLowerCase()) n = c;
    gnIn.value = '';
    plusVu = false;
    changerPersonnes((L) => {
      if (!L.includes(n)) ajouterA(L, n);
    });
    // le nom est posé ; la zone se propose pour le suivant, le clavier reste
    gnIn.focus({ preventScroll: true });
    const z = zoneAjout();
    if (z) rendreAjout(z);
    suisClavier();
  }
  function fermerAjout(): void {
    if (!ajoutActif) return;
    ajoutActif = false;
    gnIn.value = '';
    if (document.activeElement === gnIn) gnIn.blur();
    gnIn.hidden = true;
    const z = zoneAjout();
    if (z) rendreAjout(z);
    suisClavier();
  }
  /** l'entrée invisible se tient SUR la zone : si le navigateur cherche le curseur, il le trouve là */
  function posePrenom(): void {
    const z = zoneAjout();
    if (!z) return;
    const C = cs.getBoundingClientRect();
    const k = C.width / (cs.offsetWidth || 1) || 1;
    const r = z.getBoundingClientRect();
    gnIn.style.left = `${String(Math.round((r.left - C.left) / k + r.width / k / 2))}px`;
    gnIn.style.top = `${String(Math.round((r.top - C.top) / k + r.height / k / 2 - 10))}px`;
  }
  /** rien ne passe sous le clavier (v146) : la page monte pour garder la zone 14 pt au-dessus de lui (le haut du clavier se LIT) */
  let clavierDec = 0;
  function suisClavier(): void {
    const vv = window.visualViewport;
    const z = ajoutActif ? zoneAjout() : null;
    let besoin = 0;
    if (vv && z && document.activeElement === gnIn && window.innerHeight - vv.height >= 100) {
      const k = cs.getBoundingClientRect().width / (cs.offsetWidth || 1) || 1;
      besoin = Math.max(
        0,
        (z.getBoundingClientRect().bottom + clavierDec * k + 14 * k - (vv.offsetTop + vv.height)) / k,
      );
    }
    besoin = Math.round(besoin);
    if (besoin === clavierDec) return;
    const de = clavierDec;
    clavierDec = besoin;
    // la page glisse (jamais d'un coup) : le mouvement du clavier, 300 ms
    const t0 = h.maintenant();
    const pas = (): void => {
      const p = reduit() ? 1 : Math.min(1, (h.maintenant() - t0) / 300);
      const y = de + (besoin - de) * doux(p);
      if (Math.abs(y) < 0.01) cs.style.removeProperty('translate');
      else cs.style.setProperty('translate', `0 ${String(-Math.round(y * 100) / 100)}px`);
      if (p < 1 && clavierDec === besoin) h.image(pas);
    };
    pas();
  }
  gnIn.addEventListener('input', () => {
    const z = zoneAjout();
    if (z) rendreAjout(z);
  });
  gnIn.addEventListener('keydown', (ev) => {
    if (ev.key === 'Enter') {
      ev.preventDefault();
      validerAjout();
    } else if (ev.key === 'Escape') fermerAjout();
  });
  gnIn.addEventListener('focus', () => {
    const z = zoneAjout();
    if (z) rendreAjout(z);
    suisClavier();
  });
  // le clavier se retire sur une zone VIDE : elle reprend son mot ; sur un nom écrit, il reste, avec son « + »
  gnIn.addEventListener('blur', () => {
    h.minuteur(() => {
      if (!ajoutActif || document.activeElement === gnIn) return;
      if (!gnIn.value.trim()) fermerAjout();
      else {
        const z = zoneAjout();
        if (z) rendreAjout(z);
        suisClavier();
      }
    }, 0);
  });
  window.visualViewport?.addEventListener('resize', suisClavier);

  // ── LES GESTES DE LA PHRASE ──
  surToucher(txt, (ev) => {
    const t = ev.target as Element;
    const sens = t.closest('[data-ph="sens"]');
    if (sens && P.nat === 'promi') {
      // le cycle du verbe (SPEC-ECRANS §3) : « Je me promets » → « Je promets … à qui ? » → « qui ?, promets-moi » → retour
      P.sens = P.sens === 'soi' ? 'faire' : P.sens === 'faire' ? 'demander' : 'soi';
      if (P.sens === 'demander') prenomRang = magasin.avancerPrenom();
      choix = null;
      recomposer(true);
      return;
    }
    let m = t.closest<HTMLElement>('.ph-m');
    // un titre ou un nom sur deux lignes a un creux entre ses lignes : le doigt y tombe sur la phrase, et la saisie s'ouvre quand même
    // (v180b, C-234 — un déclencheur lu sur la pastille seule manquait ces touchers)
    if (!m && !t.closest('em, .ph-b'))
      for (const c of txt.querySelectorAll<HTMLElement>('.ph-m[data-ph="titre"], .ph-m[data-np="nom"]')) {
        const q = c.getBoundingClientRect();
        if (ev.clientX >= q.left && ev.clientX <= q.right && ev.clientY >= q.top && ev.clientY <= q.bottom) m = c;
      }
    if (!m) return;
    const cle = m.dataset['ph'] ?? m.dataset['np'];
    if (cle === 'titre' || cle === 'nom') {
      ouvrirSaisie(cle);
      return;
    }
    if (cle === 'qui' || cle === 'avec') {
      // C-304 : la place du destinataire (sans personne, hors « promets-moi ») passe à « moi » ; celle d'un Cercle (« avec ») aussi
      if (cle === 'qui' && !P.qui.length && P.sens !== 'demander') P.moi = true;
      if (P.nat === 'nuee' && !P.membres.length) P.moi = true;
      choix = P.nat === 'nuee' ? 'membres' : cle;
      recomposer(true);
    }
  });

  // ── LA SAISIE (le titre, le nom d'un Cercle) : le clavier s'ouvre DANS le geste ; la frappe remplit la pastille ; Retour valide ──
  function ouvrirSaisie(de: 'titre' | 'nom'): void {
    saisieDe = de;
    aTape = false;
    choix = null;
    saisie.value = de === 'nom' ? P.nom : P.titre;
    saisie.maxLength = de === 'nom' ? 40 : 280;
    saisie.focus({ preventScroll: true });
    fermerMenu();
    recomposer(true);
  }
  saisie.addEventListener('input', () => {
    if (!saisieDe) return;
    aTape = true;
    if (saisieDe === 'nom') P.nom = saisie.value;
    else P.titre = saisie.value;
    composer();
  });
  saisie.addEventListener('keydown', (ev) => {
    if (ev.key === 'Enter') {
      ev.preventDefault();
      saisie.blur();
    }
  });
  // Q598 : à la fermeture du clavier (Retour, un toucher ailleurs), la page rejoint sa place en 360 ms, jamais d'un coup
  saisie.addEventListener('blur', () => {
    if (!saisieDe) return;
    saisieDe = null;
    recomposer(!cs.classList.contains('pp-part'));
  });

  // un toucher ailleurs que sur le choix des personnes le referme
  surToucher(cs, (ev) => {
    if (!choix) return;
    const t = ev.target as Element;
    if (t.closest('.gn') || t.closest('.ph-m')) return;
    choix = null;
    recomposer(true);
  });

  // ── PEAUFINER (lot-S2, C-134, C-220) : la barre l'ouvre et le referme ; il couvre la page (son corps), la barre au-dessus ; il reste ouvert
  //    pendant qu'on y choisit ; on en sort par son X, par la barre, ou par un glissement vers le bas (C-134 : 220 pt referment, 60 non, un
  //    panneau défilé non) ; refermé, il n'en reste rien (C-220). Il paraît et part en flaques (C-271 : le prototype le pose d'un coup). ──
  /** les briques de Peaufiner (la tête, la rangée, le dépliage, la NOTE, les PIÈCES JOINTES, les murs, la pose) : communes à la fiche */
  const pf = creerPeauf(peauf);
  const deplie = pf.deplie;
  /** `ouverte` : la rangée qui reste dépliée (un membre coché) ; sans elle, Peaufiner se rebâtit replié (un choix fait la replie) */
  function rendrePeauf(ouverte: string | null = null): void {
    pf.ouverte = ouverte;
    const L = T.peauf;
    const liste = el('div', { class: 's2-liste' });
    liste.appendChild(
      pf.tete(L.titres[P.nat], T.fermerGlyphe, T.fermer, () => {
        fermerPeauf();
      }),
    );
    const rang = pf.rang;
    if (P.nat === 'nuee') {
      const r = rang(L.membres, autres(P.membres).length ? autres(P.membres).join(', ') : L.personneEncore);
      deplie(r, () => {
        // le choix des membres (le prototype : `_gensPage('nuee')`, sans « Moi » en tête) : un toucher coche ou décoche
        const liste2 = el('div', { class: 'gn-liste' });
        const pris = autres(P.membres);
        const noms = [...pris];
        for (const n of connus()) if (!noms.includes(n) && noms.length < pris.length + 6) noms.push(n);
        for (const n of noms) {
          const b = el('button', { type: 'button', class: 'ph-o' + (pris.includes(n) ? ' on' : ''), 'data-v': n });
          const ini = el('span', { class: 'ppo-ini' });
          ini.textContent = n.charAt(0).toUpperCase();
          const nm = el('span', { class: 'ppo-nom' });
          nm.textContent = n;
          b.append(ini, nm);
          surToucher(b, () => {
            const i = P.membres.indexOf(n);
            if (i >= 0) P.membres.splice(i, 1);
            else P.membres.push(n);
            if (!autres(P.membres).length) P.membres.splice(0);
            composer();
            rendrePeauf(L.membres);
          });
          liste2.appendChild(b);
        }
        const gn = el('div', { class: 'ph-opts gn', 'data-nat': 'nuee' });
        gn.appendChild(liste2);
        return gn;
      });
      liste.appendChild(r);
    } else {
      // AVANT : demain · 1 sem. · 1 mois · une date… (le calendrier) · un jour (aucune échéance) — C-197
      const ra = rang(L.avant, P.ech);
      deplie(ra, () =>
        pf.echeance({
          r: ra,
          mots: L.echeances,
          on: !P.echChoisie
            ? null
            : P.dueISO
              ? 3
              : (L.echeances as readonly string[]).indexOf(P.ech) >= 0
                ? (L.echeances as readonly string[]).indexOf(P.ech)
                : null,
          dueISO: P.dueISO,
          choisit: (d, mot) => {
            P.due = d;
            P.dueISO = null;
            P.ech = mot;
            P.echChoisie = true;
            majGarder();
            rendrePeauf();
          },
          date: (iso, jours) => {
            P.due = jours;
            P.dueISO = iso;
            P.ech = dateQuand(new Date(iso + 'T00:00:00'), jours);
            P.echChoisie = true;
            majGarder();
            return P.ech;
          },
          replie: () => {
            rendrePeauf();
          },
        }),
      );
      liste.appendChild(ra);
      if (P.nat === 'promi') {
        // DANS UN CERCLE : aucune, ou l'un des Cercles (le prototype : `#nueeChips`)
        const cercles = magasin.etat().cercles;
        const rc = rang(L.dansUnCercle, P.cercle ? (cercles[P.cercle] ?? L.aucune) : L.aucune);
        deplie(rc, () => {
          const ch = el('div', { class: 'chips', id: 'nueeChips' });
          for (const [k, nom] of [['', L.aucune] as const, ...Object.entries(cercles)]) {
            const c = el('div', { class: 'chip' + ((P.cercle ?? '') === k ? ' on' : ''), role: 'button' });
            c.textContent = nom;
            surToucher(c, () => {
              P.cercle = k || null;
              // le prototype (`buildCreateNuees`) : un Cercle choisi, la phrase devient « Je promets … à tout le monde » ; « aucune » la rend
              // à « Je me promets … »
              P.sens = k ? 'faire' : 'soi';
              P.qui = k ? [T.toutLeMonde] : [];
              P.moi = false;
              recomposer(true);
              majGarder();
              rendrePeauf();
            });
            ch.appendChild(c);
          }
          return ch;
        });
        liste.appendChild(rc);
      }
      liste.appendChild(
        pf.note({
          lab: L.note,
          vide: L.noteVide,
          vis: L.notePrivee,
          valeur: P.note,
          id: 'fNote',
          change: (v) => {
            P.note = v;
            majGarder();
          },
        }),
      );
      liste.appendChild(
        pf.pieces({
          lab: L.pieces,
          val: L.piecesVal(P.fichiers.length),
          vis: L.piecesPrivees,
          ajoute: (noms) => {
            for (const n of noms) if (!P.fichiers.includes(n)) P.fichiers.push(n);
            majGarder();
            rendrePeauf();
          },
        }),
      );
    }
    // les réglages de Ma Parole ! : des MURS, flous (4,8 px), qui ne se choisissent pas (leur phrase : lot 8)
    liste.appendChild(pf.murs(L.murs));
    // C-279 : une valeur qui a changé (un choix fait) se détrace, puis la neuve se trace — jamais d'un coup
    pf.poser(liste);
  }
  /** un mot qui change (le chevron ▾ ↔ ▴) part en flaques, puis le neuf paraît en flaques (C-271) */
  function echange(e: HTMLElement, texte: string): void {
    if (reduit()) {
      e.textContent = texte;
      return;
    }
    enFlaques(e, 'part', () => {
      queueMicrotask(() => {
        e.textContent = texte;
        enFlaques(e, 'paraît');
      });
    });
  }
  function ouvrirPeauf(): void {
    if (peaufOuvert) return;
    peaufOuvert = true;
    fermerMenu();
    if (saisieDe) saisie.blur();
    if (choix) {
      choix = null;
      recomposer(true);
    }
    rendrePeauf();
    peauf.hidden = false;
    peauf.scrollTop = 0;
    pf.croix();
    cs.classList.add('pp-peauf');
    barre.setAttribute('aria-expanded', 'true');
    enFlaques(peauf, 'paraît');
    echange(barreChev, T.chevronOuvert);
  }
  function fermerPeauf(anime = true): void {
    if (!peaufOuvert) return;
    peaufOuvert = false;
    barre.setAttribute('aria-expanded', 'false');
    const fin = (): void => {
      if (peaufOuvert) return;
      peauf.hidden = true;
      peauf.replaceChildren();
      cs.classList.remove('pp-peauf');
    };
    if (!anime || reduit()) {
      passages.get(peauf)?.stop?.();
      passages.delete(peauf);
      fin();
      barreChev.textContent = T.chevron;
      return;
    }
    enFlaques(peauf, 'part', fin);
    echange(barreChev, T.chevron);
  }
  barre.setAttribute('aria-expanded', 'false');
  surToucher(barre, () => {
    if (peaufOuvert) fermerPeauf();
    else ouvrirPeauf();
  });
  // C-134 : la sortie par un glissement vers le bas (le panneau en haut de sa liste), jamais par un défilement
  let glisseDe: { y: number; s: number; id: number } | null = null;
  peauf.addEventListener('pointerdown', (ev) => {
    glisseDe = { y: ev.clientY, s: peauf.scrollTop, id: ev.pointerId };
  });
  peauf.addEventListener('pointermove', (ev) => {
    const g = glisseDe;
    if (!g || g.id !== ev.pointerId || g.s > 0) return;
    const k = cs.getBoundingClientRect().width / (cs.offsetWidth || 1) || 1;
    if ((ev.clientY - g.y) / k > SEUIL_GLISSE) {
      glisseDe = null;
      fermerPeauf();
    }
  });
  for (const t of ['pointerup', 'pointercancel'] as const)
    peauf.addEventListener(t, () => {
      glisseDe = null;
    });

  // ── LE MENU DU BOUTON PHOTO (v117, v128, v132) : « Dessiner » en tête, puis « Importer une photo » (pas sur un Cercle : il ne porte pas de
  //    photo, C-199), puis « Retirer la photo » quand elle est là ; compact, à gauche du bouton, son bas sur le bas du bouton (jamais plus haut
  //    que 106) ; il paraît et part en flaques ; un toucher ailleurs le referme ──
  const modeDessin = creerModeDessin({
    dv,
    h,
    clair: () => dv.classList.contains('light'),
    tons: () => facade.tonsStudio(),
  });
  /** la page + habille le dessin de son brouillon (le prototype : la cible `brouillon`) */
  const cibleDessin = (): Parameters<ModeDessin['ouvrir']>[0] => ({
    lire: () => P.dessin,
    ecrire: (d) => {
      P.dessin = d;
      majGarder();
    },
    nature: P.nat,
    corps: couleurDe(cs),
    apres: (pose) => {
      // v140 (C-086, C-085) : poser un dessin retire la photo de la bande
      if (pose) P.photo = null;
      if (!cs.hidden) repeindre();
      majGarder();
    },
  });
  function ouvrirMenu(): void {
    if (menu) {
      fermerMenu();
      return;
    }
    const m = el('div', { class: 'ph-photo-menu dz-compact', role: 'menu' });
    const item = (texte: string, f: () => void, attr?: string): void => {
      const b = el('button', { type: 'button', role: 'menuitem' });
      if (attr) b.setAttribute(attr, '1');
      b.textContent = texte;
      // un vrai clic (le toucher en fabrique un) : le sélecteur de fichiers ne s'ouvre que dans le geste (iOS)
      b.addEventListener('click', (ev) => {
        ev.stopPropagation();
        f();
      });
      m.appendChild(b);
    };
    // le dessin, en tête (v132) : le mode dessin s'ouvre sur la page
    item(
      T.menuPhoto.dessiner,
      () => {
        fermerMenu(false);
        modeDessin.ouvrir(cibleDessin());
      },
      'data-dessiner',
    );
    if (P.nat !== 'nuee') {
      item(T.menuPhoto.importer, () => {
        photoIn.click();
        fermerMenu();
      });
      if (P.photo)
        item(T.menuPhoto.retirer, () => {
          fermerMenu();
          retirerPhoto();
        });
    }
    // un dessin posé ou commencé : « Retirer le dessin » (le prototype, `retire`)
    if (P.dessin && (dessinPose(P.dessin) || P.dessin.traits.length))
      item(T.menuPhoto.retirerDessin, () => {
        fermerMenu();
        P.dessin = null;
        repeindre();
        majGarder();
      });
    cs.appendChild(m);
    const hm = m.offsetHeight;
    m.style.top = `${String(Math.max(106, Math.round(photo.offsetTop + 34 - hm)))}px`;
    m.style.width = `${String(Math.max(120, photo.offsetLeft - 8 - 24))}px`;
    menu = m;
    enFlaques(m, 'paraît');
  }
  function fermerMenu(anime = true): void {
    const m = menu;
    if (!m) return;
    menu = null;
    if (!anime || reduit()) m.remove();
    else
      enFlaques(m, 'part', () => {
        m.remove();
      });
  }
  surToucher(photo, () => {
    ouvrirMenu();
  });
  cs.addEventListener(
    'pointerdown',
    (ev) => {
      const t = ev.target as Node;
      if (menu && !menu.contains(t) && !photo.contains(t)) fermerMenu();
    },
    true,
  );
  photoIn.addEventListener('change', () => {
    const f = photoIn.files?.[0];
    photoIn.value = '';
    if (!f) return;
    const lu = new FileReader();
    lu.onload = () => {
      const src = typeof lu.result === 'string' ? lu.result : null;
      if (!src) return;
      const im = new Image();
      im.onload = () => {
        images.set(src, im);
        P.photo = src;
        // v140 (C-085) : la photo REMPLACE le dessin — il n'en reste rien
        P.dessin = null;
        peindreChamp(vue.base, vue.amp, vue.hz, vue.base + vue.amp + 60 + vue.hz);
        majGarder();
        // la photo remplace la dalle : elle paraît en flaques sur elle (C-271)
        enFlaques(photoCv, 'paraît');
      };
      im.src = src;
    };
    lu.readAsDataURL(f);
  });
  function retirerPhoto(): void {
    enFlaques(photoCv, 'part', () => {
      P.photo = null;
      peindreChamp(vue.base, vue.amp, vue.hz, vue.base + vue.amp + 60 + vue.hz);
      majGarder();
    });
  }

  // ── OUVRIR, FERMER ──
  /** tout ce qu'une page ouverte a posé s'en va avec elle (« rien ne survit à closeAll ») */
  function ranger(): void {
    if (mv) {
      h.annuleImage(mv.id);
      mv.fin();
      mv = null;
    }
    for (const c of passages.values()) c.stop?.();
    passages.clear();
    sortants.clear();
    fermerMenu(false);
    fermerPeauf(false);
    if (modeDessin.ouvert()) modeDessin.sortir(false);
    ajoutActif = false;
    gnIn.value = '';
    gnIn.hidden = true;
    for (const x of [phrase, photo, pinceau, garder, barre]) x.style.removeProperty('translate');
    cs.style.removeProperty('translate');
    clavierDec = 0;
    for (const c of cs.querySelectorAll('.ppo-copie')) c.remove();
  }
  /**
   * LA REPRISE d'un gardé de côté (le prototype : `lot-V162-GARDER`, `restaure`) — la page + dans sa nature, puis l'état gardé : la phrase,
   * les personnes, Peaufiner, la photo et le dessin de la bande. « Garder de côté » le met à jour ensuite (jamais un second). La porte : l'Index.
   */
  function reprendre(id: number): boolean {
    const p = magasin.etat().paroles.find((x) => x.id === id && x.draft);
    const b = p?.brouillon;
    if (!b) return false;
    ouvrir(b.nat);
    const liste = (v: unknown): string[] =>
      Array.isArray(v) ? v.filter((x): x is string => typeof x === 'string') : [];
    const ph = b.phrase;
    const sens = b.sens === 'faire' || b.sens === 'demander' || b.sens === 'soi' ? b.sens : 'soi';
    P = {
      ...neuve(b.nat),
      sens,
      titre: typeof ph.titre === 'string' ? ph.titre : '',
      qui: liste(b['quiListe']),
      avec: liste(b['avecListe']),
      nom: b.nom,
      membres: liste(b['membresListe']),
      pinceau: typeof b['pinceau'] === 'string' ? b['pinceau'] : 'Plein',
      moi: b['moi'] === true,
      note: typeof b['note'] === 'string' ? b['note'] : '',
      ech: typeof b['ech'] === 'string' ? b['ech'] : T.peauf.echeanceDefaut,
      echChoisie: b['echChoisie'] === true,
      due: typeof b['due'] === 'number' ? b['due'] : null,
      dueISO: typeof b['dueISO'] === 'string' ? b['dueISO'] : null,
      cercle: typeof b['cercle'] === 'string' ? b['cercle'] : null,
      fichiers: liste(b['fichiers']),
      photo: typeof ph['photo'] === 'string' ? ph['photo'] : null,
      dessin: (ph['dessin'] as Dessin | null | undefined) ?? null,
    };
    repris = id;
    composer();
    repeindre();
    majGarder();
    return true;
  }
  function ouvrir(nat: Nature): void {
    ranger();
    P = neuve(nat);
    cacheInvite();
    // un détracé, un tracé de la place qui court encore (C-332) : la page neuve ne les reprend pas
    douceur.arrete();
    exemples = {};
    choix = null;
    saisieDe = null;
    dalleT = null;
    repris = null;
    const r = magasin.etat().autres['promi_ex_prenom'];
    prenomRang = r != null && r !== '' && +r >= 0 ? +r % 2 : 0;
    if (finFermeture != null) h.annuleMinuteur(finFermeture);
    if (finOuverture != null) h.annuleMinuteur(finOuverture);
    cs.classList.remove('pp-part', 'pp-entre');
    // composée cachée, en bas (v103 : rien ne paraît une fraction de seconde à moitié composé)…
    // (composée à sa place : ses mesures se lisent sur l'écran, jamais sous la réduction du départ)
    cs.classList.add('pp-compose');
    cs.hidden = false;
    continu.ouvre();
    ouverteA = h.maintenant();
    composer();
    signature0 = signature();
    majGarder();
    cs.classList.add('pp-bas');
    cs.classList.remove('pp-compose');
    // …puis ⚑ C-331 (Tom, 22 nov. 2026) : elle MONTE, le mouvement exact de sa fermeture à l'envers — même courbe, même durée, la même
    // règle (`pp-bas` ↔ `pp-part`, page-plus.css) ; l'accueil reste dessous pendant qu'elle monte, il n'est couvert qu'à l'arrivée
    cs.getBoundingClientRect();
    cs.classList.add('pp-entre');
    cs.classList.remove('pp-bas');
    finOuverture = h.minuteur(() => {
      finOuverture = null;
      cs.classList.remove('pp-entre');
      // la page couvre l'appareil : ce qui est dessous (l'accueil, la Toile) ne se voit plus et ne prend plus le doigt (base.css, `.couvert`)
      cs.classList.add('couvre');
      dv.classList.add('couvert');
    }, 480);
  }
  let finOuverture: number | null = null;
  let finFermeture: number | null = null;
  /** `coupe` : la page se cache d'un coup (une plantation : la Toile la couvre déjà, v103) ; sinon elle glisse vers le bas */
  function fermer(coupe = false): void {
    if (cs.hidden || (cs.classList.contains('pp-part') && !coupe)) return;
    if (coupe) {
      if (finOuverture != null) h.annuleMinuteur(finOuverture);
      if (finFermeture != null) h.annuleMinuteur(finFermeture);
      finOuverture = null;
      finFermeture = null;
      saisieDe = null;
      saisie.blur();
      fermerMenu();
      dv.classList.remove('couvert');
      cs.classList.remove('pp-entre', 'pp-part', 'couvre');
      cs.hidden = true;
      cacheInvite();
      ranger();
      return;
    }
    if (finOuverture != null) {
      h.annuleMinuteur(finOuverture);
      finOuverture = null;
    }
    cs.classList.remove('pp-entre');
    saisieDe = null;
    saisie.blur();
    if (document.activeElement === gnIn) gnIn.blur();
    fermerMenu();
    // l'accueil reparaît dessous, la page glisse par-dessus lui
    dv.classList.remove('couvert');
    cs.classList.add('pp-part');
    if (finFermeture != null) h.annuleMinuteur(finFermeture);
    finFermeture = h.minuteur(() => {
      finFermeture = null;
      cs.hidden = true;
      cs.classList.remove('pp-part');
      cacheInvite();
      ranger();
    }, 480);
  }
  surToucher(croix, () => {
    fermer();
  });
  nav.poser('pagePlus', (arg) => {
    const n = NATURES.includes(arg as Nature) ? (arg as Nature) : 'promi';
    ouvrir(n);
  });
  // une police chargée après coup, une autre largeur : la page se recompose
  const surTaille = (): void => {
    if (!cs.hidden && !cs.classList.contains('pp-part')) composer();
  };
  window.addEventListener('resize', surTaille);

  return {
    racine: cs,
    ouvrir,
    reprendre,
    fermer,
    ouverte: () => !cs.hidden && !cs.classList.contains('pp-part'),
    etat: () => ({
      phrase: { ...P, qui: [...P.qui], avec: [...P.avec], membres: [...P.membres] },
      base: mise.base,
      amp: mise.amp,
      hz: mise.hz,
      lignes: mise.nl,
      taille: mise.taille,
      choix,
      gardeActif: !garder.classList.contains('inactif'),
      exemples: { ...exemples },
      saisie: saisieDe,
      peauf: peaufOuvert,
      menu: !!menu,
      ajout: ajoutActif,
      mouvement: !!mv || douceur.actif() || continu.actif(),
      mouvementDe: [mv ? 'clavier' : '', douceur.actif() ? 'douceur' : '', continu.actif() ? 'continu' : ''].filter(
        Boolean,
      ),
      invite: { visible: inv.vis, sortie: inv.sortie, haut: inv.haut, anim: !!inv.anim, touche: inv.touche },
      dessin: modeDessin.etat(),
    }),
    detruire() {
      window.removeEventListener('resize', surTaille);
      cs.remove();
    },
  };
}
