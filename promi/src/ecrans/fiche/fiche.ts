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
  fermer(): void;
  /** pour les tests : la parole ouverte, et ce que la fiche a posé */
  etat(): { id: number | null; base: number; amp: number; mode: string; instant: Instant };
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
  // pas encore portées (lot 3b : le menu photo, Peaufiner, les membres ; lot 8 : Partager) : elles se déclarent inactives (`aria-disabled`),
  // et le retirent quand leur lot les branche
  for (const c of [photo, plusM, barreTog, partage]) c.setAttribute('aria-disabled', 'true');
  fi.append(champ, trait, plateau, photo, geste, noyaux, plusM, phrase, titre, etatL, unMot, barre);
  dv.appendChild(fi);

  let courant: Parole | null = null;
  let deplie = false;
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
  // « + x personnes » : un toucher déroule la liste entière dans la phrase, qui s'allonge vers le bas ; le titre descend (C-069)
  surToucher(phrase, (ev) => {
    if (!courant || !(ev.target instanceof Element) || !ev.target.closest('.fi-plus')) return;
    deplie = true;
    poser(courant);
  });

  function nature(p: Parole): Nature {
    return p.chiche ? 'chiche' : 'promi';
  }

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
    const r = facade.poserDalle(g, p.id, b.x, b.y, b.w, b.h, { rampe: { cols: RAMPE[n], haut: 2 } });
    champ.setAttribute('data-matiere', r ? [r.x, r.y, r.w, r.h].map((v) => Math.round(v)).join(',') : '');
  }

  // ── LE TRAIT : sur sa couche (la jonction, 3a-3, la tiendra au défilement) ──
  function peindreTrait(p: Parole): void {
    const n = nature(p);
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
    const tenu = p.status === 'tenu';
    const plusieurs = !tenu && aPlusieurs(p);
    const S = plusieurs ? etatParts(p) : null;
    const col = instantF ? palette.menthe82 : tenu ? CRETE : NATTRAIT[n];
    peindreLigne(g, T.base, T.amp, {
      mode: T.mode,
      col,
      attend: !instantF && !!consigne(p),
      parts: S && !instantF ? { S, initiales: initiales(S.T, moiNom()), encre: palette.creme95 } : undefined,
      doigt: doigtX ?? undefined,
    });
    trait.setAttribute('data-trait', [T.base, T.amp, col, T.mode].join(','));
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
    noyaux.innerHTML = rangeeNoyaux(noyauxDe(p, magasin.etat().paroles), CHAMP[n], p.status === 'tenu', court);
    peindreNoyaux(noyaux);
    partage.style.borderColor = n === 'chiche' ? palette.brun09 : palette.creme95;
    poserPhoto();
    // le nombre de mots sur la ligne « Un mot… » (C-257) : le total ; « +N » orange quand des mots d'autres ne sont pas encore vus (C-253)
    const mots = p.comments ?? [];
    const moi = moiNom();
    const neufs = mots.filter((m) => !m.vu && !/^moi$/i.test(String(m.by)) && m.by !== moi).length;
    nbMots.hidden = !mots.length;
    nbMots.textContent = neufs ? '+' + String(neufs) : String(mots.length);
    nbMots.classList.toggle('cm5-neufs', !!neufs);
    coter(!!c);
    tenir.poser(!instantF && p.status !== 'tenu');
    poserInstant(p);
    poserPlus(p);
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
  function poserPlus(p: Parole): void {
    plusM.hidden = recue(p) || instantF === 'referme';
    if (plusM.hidden) return;
    const ds = noyaux.querySelectorAll<HTMLElement>('.kr-wrap');
    const a = ds[ds.length - 1]!;
    const r = a.getBoundingClientRect();
    const f = fi.getBoundingClientRect();
    const k = f.width / fi.offsetWidth || 1;
    const gx = (r.right - f.left) / k + 26;
    const cy = (r.top - f.top) / k + r.height / k / 2;
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
    // « Un mot… » (692 → 748) garde 8 pt sous la ligne d'état (lot-V181B-TEXTES, `ajusteLigne`)
    const bas = yEtat + etatL.offsetHeight;
    unMot.style.translate = `0 ${String(Math.max(0, bas - 692 + 8))}px`;
  }

  /** ce que l'agrandissement des faces (v96, × 1,12) ajoute à l'encre au-dessus et au-dessous d'une ligne (`_encreSup`) */
  function encre(fs: number): { haut: number; bas: number } {
    const d = fs * (1.12 - 1);
    return { haut: d * 0.8, bas: d * 0.62 };
  }

  function ajusterTitre(): number {
    const lignes = (f: number): number => Math.round(titre.offsetHeight / (f * 1.02));
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
      if (!ok && courant) {
        fs = 24;
        titre.style.fontSize = '24px';
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
    fi,
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

  function ouvrir(id: number): void {
    const p = magasin.etat().paroles.find((q) => q.id === id);
    if (!p || p.draft) return;
    tenir.arreter();
    instantF = null;
    doigtX = null;
    courant = p;
    deplie = false;
    // montrée AVANT d'être posée (en bas, invisible) : les cotes se lisent sur le rendu (le titre, la phrase, les disques) ; puis elle monte
    if (finFermeture != null) horloge().annuleMinuteur(finFermeture);
    finFermeture = null;
    fi.classList.add('fi-bas');
    fi.hidden = false;
    poser(p);
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
    tenir.arreter();
    courant = null;
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
  magasin.abonner((e) => {
    if (!courant || fi.hidden) return;
    const p = e.paroles.find((q) => q.id === courant!.id);
    if (!p) {
      fermer();
      return;
    }
    if (p === courant) return;
    courant = p;
    poser(p);
  });

  nav.poser('fiche', (arg) => {
    ouvrir(Number(arg));
  });

  return {
    ouvrir,
    fermer,
    etat: () => ({ id: courant?.id ?? null, base: T.base, amp: T.amp, mode: T.mode, instant: instantF }),
    tenir: () => tenir.etat(),
  };
}
