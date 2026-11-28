/**
 * L'AURA (lot 6, SPEC-ECRANS §10 ; le prototype : lot-AURA-PELOTE, ses cotes B figées en v126, C-005) — de haut en bas, et rien d'autre :
 *  · la Pelote (pelote.ts) et son ombre (v139) ;
 *  · « PARTAGER MA PELOTE », juste sous l'ombre (v118, Q367) ;
 *  · la phrase — elle qualifie L'OBJET, tirée du nombre de paroles tenues (jamais au hasard d'une ouverture) ; une Aura vide ou sans tenue
 *    dit ses deux lignes (E4), la seconde se touche ;
 *  · les Noyaux (§2.9) : « Toi » puis les personnes, dans l'ordre alphabétique — deux arcs d'état au plus (C-210), un jour de 3 px d'arc ;
 *  · la légende (deux rectangles d'aperçu, v173) et ses deux chiffres (R-015) ;
 *  · « Ce que tu as tenu » : toutes les tenues, la plus récente en premier (C-052, v132), chacune en vraie dalle, rendue à sa boîte ;
 *  · « Ce qu'on t'a tenu » (Q215) : en gratuit, flouté, l'encart « ✦ Ma Parole ! » posé dessus.
 * LA COLONNE SE CALCULE (§8 : une cote dérivée n'est pas un espace) : sous la phrase, tout se dérive de son bas réel. Ce qui dépasse l'écran défile
 * sous le plateau. L'écran est une feuille de l'Index (ecran-liste : l'entrée du bas, l'encart du haut, le corps d'écran).
 */
import './aura.css';
import type { Facade } from '../../moteur/facade.ts';
import type { Magasin } from '../../etat/magasin.ts';
import type { Navigation } from '../../navigation/navigation.ts';
import type { Parole } from '../../donnees/schema.ts';
import { palette } from '../../design/jetons.ts';
import { el, surToucher } from '../commun.ts';
import { encart, glissiere } from '../liste/ecran-liste.ts';
import { fondVisage } from '../fiche/mots.ts';
import { horloge } from '../../animation/horloge.ts';
import { donneesAura, type DonneesAura } from '../../metier/aura.ts';
import { monterPelote, type Pelote } from './pelote.ts';
import { brancherGestes } from './gestes.ts';

const TXT = {
  titre: ['L', '’', 'aura'],
  info: 'i',
  infoAria: 'À propos de l’Aura',
  partager: 'PARTAGER MA PELOTE',
  partagerAria: 'Partager ma Pelote',
  toi: 'Toi',
  tenu: 'Ce que tu as tenu',
  onTaTenu: 'Ce qu’on t’a tenu',
  maParole: '✦ Ma Parole !',
  etats: ['tenues', 'en cours'],
} as const;

/** LES COTES — composition B (v126, C-005), en pt de l'écran 390 × 844 ; `releve-aura` les portait en dur, `aura.spec.ts` aussi */
const _CMP = [14, 12, 12] as const;
const K = {
  nx: { y: 482.061 - 38, h: 107 },
  lgH: 24.25,
  cptH: 30,
  cptAIR: 16 + 2.714,
  bt: { h: 60 },
  marge: 22,
  toi: { d: 78, arc: 12, ph: 48 },
  pers: { d: 58, arc: 9, ph: 36 },
  /** l'écart de la boîte à l'encre (cotes déclarées, relevées police chargée : §8) */
  lgINK: -6 - 2.714,
  moINK: -9.5,
  MOT_INK: 2.5,
  AIR: 28,
  ombre: { y: 405.224 - _CMP[0], h: 16.245 },
  G2: 34 - _CMP[1],
  G2_OMBRE: 28,
  MOT_ENCRE: -1.87,
} as const;
const AIR_MOT = 30.71 - _CMP[2] - K.MOT_INK;
const BT_Y = K.ombre.y + K.ombre.h + K.G2_OMBRE;
const MOT_Y2 = BT_Y + K.bt.h + K.G2 + K.MOT_ENCRE;
/** les deux états, une seule table, dans les deux thèmes (C-210) */
const ETATS = [palette.menthe11, palette.mauve12] as const;
/** le jour entre deux arcs : en pixels d'arc, le même sur tous les anneaux (23 sept.) */
const JOUR_PX = 3;

export interface Aura {
  ouvrir(): void;
  fermer(): void;
  ouvert(): boolean;
  /** pour les juges : la Pelote (figer la vue, poser une vue, peindre), la colonne posée */
  pelote(): Pelote;
  colonne(): Record<string, number> | null;
}

export function monterAura(facade: Facade, magasin: Magasin, nav: Navigation): Aura {
  const dv = facade.appareil();
  const sh = el('div', { id: 'auraScreen', class: 'ecran-liste ecran-aura', role: 'dialog' });
  sh.hidden = true;
  const { plateau, titre, croix, poserEncart } = encart('');
  titre.append(document.createTextNode(TXT.titre[0]));
  const apo = el('span', { class: 'ti-x au-apo' });
  apo.textContent = TXT.titre[1];
  titre.append(apo, document.createTextNode(TXT.titre[2] + ' '));
  const info = el('span', { id: 'auraInfoBtn', class: 'aura-info', role: 'button', 'aria-label': TXT.infoAria });
  info.textContent = TXT.info;
  titre.appendChild(info);

  const cad = el('div', { id: 'auCadre', class: 'au-cadre au-voile', 'data-defile': '1' });
  const ombre = el('div', { id: 'auPeloteOmbre', class: 'au-ombre' });
  const bo = el('div', { class: 'au-bo' });
  const rot = el('div', { class: 'au-rot' });
  const cv = el('canvas', { id: 'auBoule' });
  rot.appendChild(cv);
  const prise = el('div', { class: 'au-prise' });
  bo.append(rot, prise);
  const mot = el('div', { class: 'au-mot' });
  const inv = el('div', { class: 'au-inv' });
  const nx = el('div', { class: 'au-nx', 'data-glisse': '1' });
  const lg = el('div', { class: 'au-lg' });
  TXT.etats.forEach((m, i) => {
    const s = el('span');
    const p = el('i');
    p.style.background = ETATS[i]!;
    s.append(p, document.createTextNode(m));
    lg.appendChild(s);
  });
  const cpt = el('div', { class: 'au-cpt' });
  cpt.append(el('span'), el('span'));
  const mo = el('div', { class: 'au-mo' });
  const h3 = el('h3');
  h3.textContent = TXT.tenu;
  const gr = el('div', { class: 'au-gr' });
  mo.append(h3, gr);
  const mo2 = el('div', { class: 'au-mo2' });
  const h32 = el('h3');
  h32.textContent = TXT.onTaTenu;
  const z2 = el('div', { class: 'au-zone2' });
  const gr2 = el('div', { class: 'au-gr2' });
  const enc2 = el('div', { class: 'au-enc2', role: 'button' });
  const enc2s = el('span');
  enc2s.textContent = TXT.maParole;
  enc2.appendChild(enc2s);
  z2.append(gr2, enc2);
  mo2.append(h32, z2);
  const bt = el('div', { id: 'auPartage', class: 'au-bt', role: 'button', 'aria-label': TXT.partagerAria });
  bt.textContent = TXT.partager;
  const fin = el('div', { class: 'au-fin' });
  cad.append(ombre, bo, mot, inv, nx, lg, cpt, mo, mo2, bt, fin);
  sh.append(cad, plateau);
  dv.appendChild(sh);

  const clair = (): boolean => dv.classList.contains('light');
  const stockage = {
    lire: (k: string) => magasin.etat().autres[k] ?? null,
    ecrire: (k: string, v: string) => {
      magasin.noterPelote(k, v);
    },
  };
  const G = glissiere(sh, dv, false, () => {
    remplir();
    poserEncart();
    poserInfo();
  });
  let couv = false;
  let couvN = 0;
  const pel = monterPelote({
    facade,
    cv,
    rot,
    ecran: sh,
    clair,
    visible: () => !sh.hidden,
    stockage,
    hasard: Math.random,
    apresImage: () => {
      placer();
    },
    tenues: () => donnees().T,
    // jugé AU DOIGT (ce qui est vraiment au-dessus du centre de la Pelote), une image sur six : `elementFromPoint` force la mise en page
    couvert: () => {
      if (couvN++ % 6) return couv;
      const r = cv.getBoundingClientRect();
      const x = r.left + r.width / 2;
      const y = r.top + r.height / 2;
      if (!r.width || x < 0 || y < 0 || x >= innerWidth || y >= innerHeight) return (couv = false);
      const t = document.elementFromPoint(x, y);
      return (couv = !!t && !sh.contains(t));
    },
  });

  // la prise : un doigt posé sur la Pelote la tourne, il ne fait pas défiler la colonne
  brancherGestes(prise, cv, dv, pel.acces);

  let D: DonneesAura | null = null;
  let col: Record<string, number> | null = null;
  let colK = '';

  /** l'image d'une personne (le visage du produit) ; la mienne : ma graine */
  function visage(d: number, nom: string, moi: boolean): HTMLElement {
    const w = el('div', { class: 'au-vis' });
    w.style.width = w.style.height = `${String(d)}px`;
    w.style.background = fondVisage(moi ? 'u' + String(magasin.etat().utilisateur.graine ?? 0) : nom);
    const g = el('div', { class: 'au-grain' });
    g.style.backgroundImage = `url(${grain()})`;
    w.appendChild(g);
    return w;
  }
  /** un Noyau du §2.9 : deux arcs d'état au plus, n arcs et n jours identiques, le jour centré sur midi ; en sombre, le filet crème de chaque arc */
  function noyau(
    t: { d: number; arc: number; ph: number },
    pa: [number, number] | null,
    nom: string,
    moi: boolean,
  ): HTMLElement {
    const w = el('div', { class: `au-n${moi ? ' au-moi' : ''}`, 'data-qui': moi ? 'moi' : nom });
    const box = el('div', { class: 'au-nb' });
    box.style.width = box.style.height = `${String(t.d)}px`;
    const r = (t.d - t.arc) / 2;
    const cx = t.d / 2;
    const pt = (a: number, rr: number): string => {
      const q = ((a - 90) * Math.PI) / 180;
      return `${(cx + rr * Math.cos(q)).toFixed(2)} ${(cx + rr * Math.sin(q)).toFixed(2)}`;
    };
    let s = `<svg viewBox="0 0 ${String(t.d)} ${String(t.d)}" width="${String(t.d)}" height="${String(t.d)}">`;
    if (pa && pa[0] + pa[1] > 0) {
      const n = pa.filter((v) => v > 0).length;
      const GJ = n > 1 ? ((JOUR_PX / r) * 180) / Math.PI : 0.1;
      let a = GJ / 2;
      const sombre = !clair();
      const rf = r + t.arc / 2 - 0.5;
      pa.forEach((v, z) => {
        if (v <= 0) return;
        const a1 = a + v * 360 - GJ;
        if (a1 - a > 0.3) {
          const g = a1 - a > 180 ? 1 : 0;
          s += `<path class="au-arc" data-z="${String(z)}" d="M${pt(a, r)} A${String(r)} ${String(r)} 0 ${String(g)} 1 ${pt(a1, r)}" fill="none" stroke="${ETATS[z]!}" stroke-width="${String(t.arc)}" stroke-linecap="butt"/>`;
          // v18 : le filet crème suit le bord extérieur de chaque arc posé sur le sombre (1 px), il s'interrompt dans les jours — ses bouts tirés de
          // ceux de l'arc ÉCRITS (au centième), son rayon au millième, comme la passe du prototype (`cerne`, lot-V16)
          if (sombre) {
            const ang = (x: string): number => {
              const [px, py] = x.split(' ').map(Number) as [number, number];
              return Math.atan2(py - cx, px - cx);
            };
            const P = (q: number): string =>
              `${(cx + rf * Math.cos(q)).toFixed(3)} ${(cx + rf * Math.sin(q)).toFixed(3)}`;
            s += `<path class="au-filet" d="M${P(ang(pt(a, r)))} A${rf.toFixed(3)} ${rf.toFixed(3)} 0 ${String(g)} 1 ${P(ang(pt(a1, r)))}" fill="none" stroke="${palette.creme95}" stroke-width="1" stroke-linecap="butt"/>`;
          }
        }
        a += v * 360;
      });
    }
    box.innerHTML = s + '</svg>';
    const f = visage(t.ph, nom, moi);
    f.style.left = f.style.top = `${String((t.d - t.ph) / 2)}px`;
    box.appendChild(f);
    const lb = el('div', { class: 'au-lb' });
    lb.textContent = moi ? TXT.toi : nom;
    w.append(box, lb);
    return w;
  }
  /** une dalle de la moisson : rendue à la taille de SA boîte (101 × 64 au plus), dans le monde de sa plantation, posée 1:1 */
  function cellule(p: Parole, cls: string): HTMLElement {
    const c = el('div', { class: cls, 'data-pid': String(p.id), role: 'button' });
    const bx = el('div', { class: 'au-bx' });
    const cvd = el('canvas', { 'data-pid': String(p.id) });
    bx.appendChild(cvd);
    const t = el('span');
    t.textContent = p.title || '';
    c.append(bx, t);
    surToucher(c, () => {
      nav.ouvrir('fiche', p.id);
    });
    return c;
  }
  function peindreMoisson(): void {
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    for (const c of cad.querySelectorAll<HTMLCanvasElement>('.au-gr canvas[data-pid], .au-gr2 canvas[data-pid]')) {
      if (c.dataset['ok']) continue;
      const bx = c.parentElement;
      const p = magasin.etat().paroles.find((q) => q.id === +(c.dataset['pid'] ?? -1));
      if (!bx || !p) continue;
      const bw = bx.clientWidth || 64;
      const bh = bx.clientHeight || 64;
      const s = facade.rendreDalle(p.id, bw * dpr, bh * dpr, p.monde ? { monde: p.monde } : undefined);
      if (!s) continue;
      c.width = s.cv.width;
      c.height = s.cv.height;
      c.style.width = `${String(s.cv.width / dpr)}px`;
      c.style.height = `${String(s.cv.height / dpr)}px`;
      c.getContext('2d')?.drawImage(s.cv, 0, 0);
      c.dataset['ok'] = '1';
    }
  }

  /** ce que l'Aura dit, lu dans l'état ; l'ordre des îles gardé (une ancienne ne bouge jamais) */
  function donnees(): DonneesAura {
    const e = magasin.etat();
    let ordre: number[] = [];
    try {
      const o = JSON.parse(e.autres['promi_pelote_ordre'] ?? '[]') as unknown;
      if (Array.isArray(o)) ordre = o.filter((x): x is number => typeof x === 'number');
    } catch {
      ordre = [];
    }
    const d = donneesAura(e.paroles, { moi: e.utilisateur.prenom ?? '', cercles: e.cercles, ordre });
    if (JSON.stringify(d.ordre) !== JSON.stringify(ordre))
      stockage.ecrire('promi_pelote_ordre', JSON.stringify(d.ordre));
    return d;
  }

  function remplir(): void {
    D = donnees();
    const vide = D.P.length === 0;
    cad.classList.toggle('au-vide', vide);
    const l2 = (txt: string, mene: 'plus' | 'index'): HTMLElement => {
      const x = el('em', { class: 'au-l2', role: 'button', 'data-e4': mene });
      x.textContent = txt;
      // E4 : l'Aura se ferme d'abord (le prototype : `ferme()` de lot-V178C), puis la destination s'ouvre
      surToucher(x, () => {
        fermer();
        if (mene === 'index') nav.ouvrir('index');
        else nav.ouvrir('pagePlus', 'promi');
      });
      return x;
    };
    if (vide) {
      inv.replaceChildren(document.createTextNode(D.phrase.l1), l2(D.phrase.l2!, 'plus'));
      mot.textContent = '';
    } else {
      inv.textContent = '';
      if (D.phrase.l2) mot.replaceChildren(document.createTextNode(D.phrase.l1), l2(D.phrase.l2, 'index'));
      else mot.textContent = D.phrase.l1;
    }
    nx.replaceChildren();
    if (!vide) {
      nx.appendChild(noyau(K.toi, D.toi, 'toi', true));
      const gp = el('div', { class: 'au-gp' });
      for (const g of D.gens) gp.appendChild(noyau(K.pers, g.parts, g.nom, false));
      nx.appendChild(gp);
      nx.scrollLeft = 0;
    }
    gr.replaceChildren(...D.moisson.map((p) => cellule(p, 'au-c')));
    gr2.replaceChildren(...D.moisson2.map((p) => cellule(p, 'au-c2')));
    mo2.classList.toggle('au-sans', vide || !D.moisson2.length);
    mo.classList.toggle('au-sans', vide || !D.moisson.length);
    const s = cpt.children;
    D.chiffres.forEach((v, i) => {
      const x = s[i];
      if (x && x.textContent !== String(v)) x.textContent = String(v);
    });
    pel.donner(D.T);
    horloge().image(() => {
      peindreMoisson();
    });
    cad.scrollTop = 0;
    colK = '';
    placer();
  }

  /** la colonne : hauteur du bloc + air, jamais une cote figée (§8) ; on compare avant d'écrire */
  function placer(): void {
    if (!D) return;
    // la couleur du bouton : un ton de la palette tiré à chaque ouverture (v124)
    const b = pel.couleurs().bouton.rgb;
    const bc = `rgb(${String(b[0])}, ${String(b[1])}, ${String(b[2])})`;
    if (bt.style.color !== bc) bt.style.color = bc;
    let c: Record<string, number>;
    if (cad.classList.contains('au-vide')) {
      c = { nx: K.nx.y, lg: K.nx.y, cpt: K.nx.y, bt: BT_Y, inv: BT_Y + K.bt.h + K.G2 };
      c['mo'] = c['inv']!;
      c['mo2'] = c['inv']!;
      c['fin'] = c['inv']! + K.AIR + K.marge;
    } else {
      // la hauteur EXACTE de la phrase (v124 : `offsetHeight` l'arrondit)
      const r = mot.getBoundingClientRect();
      const mh = r.width > 0 && mot.offsetWidth > 0 ? (r.height * mot.offsetWidth) / r.width : mot.offsetHeight;
      const n = MOT_Y2 + mh + AIR_MOT;
      const lgy = n + K.nx.h + K.AIR + K.lgINK;
      const cy = lgy + K.lgH + K.cptAIR;
      const moy = cy + K.cptH + K.AIR + K.moINK;
      let bas = mo.classList.contains('au-sans') ? moy : moy + mo.offsetHeight;
      const mo2y = bas + K.AIR;
      if (!mo2.classList.contains('au-sans')) bas = mo2y + mo2.offsetHeight;
      c = { nx: n, lg: lgy, cpt: cy, mo: moy, mo2: mo2y, bt: BT_Y, fin: bas + K.marge, inv: BT_Y + K.bt.h + K.G2 };
    }
    c['mot'] = MOT_Y2;
    // les chiffres, chacun centré sous SON entrée de légende (sa position vient de la légende, jamais du chiffre : pas de boucle)
    const L = lg.children;
    const S = cpt.children;
    for (let i = 0; i < S.length && i < L.length; i++) {
      const l = L[i] as HTMLElement;
      const x = `${(l.offsetLeft + l.offsetWidth / 2).toFixed(1)}px`;
      const sp = S[i] as HTMLElement;
      if (sp.style.left !== x) sp.style.left = x;
    }
    const k = ['nx', 'lg', 'cpt', 'mo', 'mo2', 'bt', 'fin', 'mot', 'inv'].map((x) => c[x]!.toFixed(2)).join('|');
    if (k === colK) return;
    colK = k;
    col = c;
    const poser = (e: HTMLElement, y: number): void => {
      e.style.top = `${y.toFixed(2)}px`;
    };
    poser(nx, c['nx']!);
    poser(lg, c['lg']!);
    poser(cpt, c['cpt']!);
    poser(mo, c['mo']!);
    poser(mo2, c['mo2']!);
    poser(bt, c['bt']!);
    poser(fin, c['fin']! - 1);
    poser(mot, c['mot']);
    poser(inv, c['inv']!);
  }

  /** le « i » centré sur l'encart (lot-V210-ENCART : son centre au milieu du plateau, le décalage du titre retiré) */
  function poserInfo(): void {
    if (!info.offsetHeight || !plateau.offsetWidth) return;
    const rb = plateau.getBoundingClientRect();
    const k = rb.width / plateau.offsetWidth || 1;
    const bt0 = parseFloat(getComputedStyle(plateau).borderTopWidth) || 0;
    const deja = (e: HTMLElement): number =>
      parseFloat((getComputedStyle(e).translate || '').split(' ')[1] ?? '0') || 0;
    const ri = info.getBoundingClientRect();
    const yi = (ri.top - rb.top) / k - bt0 - deja(info) - deja(titre) + ri.height / k / 2;
    const v = `0px ${String(Math.round((plateau.clientHeight / 2 - yi - deja(titre)) * 100) / 100)}px`;
    if (info.style.getPropertyValue('translate') !== v) info.style.setProperty('translate', v);
  }

  surToucher(croix, () => {
    fermer();
  });
  surToucher(bt, () => {
    nav.ouvrir('partager', 'pelote');
  });
  surToucher(info, () => {
    nav.ouvrir('aideAura');
  });
  surToucher(enc2, () => {
    nav.ouvrir('offre');
  });
  // un Noyau touché ouvre la personne (jamais pour soi) ; un glissement de la rangée ne l'ouvre pas
  let d0: { x: number; y: number; n: HTMLElement | null; sl: number } | null = null;
  nx.addEventListener('pointerdown', (e) => {
    d0 = {
      x: e.clientX,
      y: e.clientY,
      n: (e.target as Element | null)?.closest<HTMLElement>('.au-n') ?? null,
      sl: nx.scrollLeft,
    };
  });
  nx.addEventListener('pointercancel', () => {
    d0 = null;
  });
  nx.addEventListener('pointerup', (e) => {
    const x = d0;
    d0 = null;
    if (!x?.n) return;
    const s = dv.getBoundingClientRect().width / 390 || 1;
    const dd = Math.hypot(e.clientX - x.x, e.clientY - x.y) / s + Math.abs(nx.scrollLeft - x.sl) / s;
    const q = x.n.dataset['qui'];
    if (dd <= 6 && q && q !== 'moi') nav.ouvrir('personne', q);
  });
  void document.fonts.ready.then(() => {
    if (sh.hidden) return;
    poserEncart();
    poserInfo();
    colK = '';
    placer();
  });
  // C-049 : une seule source de vérité — une parole tenue, plantée ou retirée : l'Aura ouverte suit, sans ton neuf
  magasin.abonner((_e, action) => {
    if (action === 'noterPelote') return;
    // l'Aura fermée : la préparation au repos se refait (une autre palette, un autre monde, un autre thème : un ton neuf)
    if (sh.hidden) {
      pel.invalider(action === 'choisirPalette' || action === 'choisirMonde' || action === 'choisirTheme');
      return;
    }
    if (G.ouvert()) {
      const avant = JSON.stringify(D?.T.map((p) => p.id));
      remplir();
      if (JSON.stringify(D?.T.map((p) => p.id)) !== avant) pel.peindre();
    }
  });

  function ouvrir(): void {
    G.ouvrir();
    pel.ouvrir();
    placer();
  }
  function fermer(): void {
    G.fermer();
    pel.fermer();
  }
  nav.poser('aura', () => {
    ouvrir();
  });
  return { ouvrir, fermer, ouvert: G.ouvert, pelote: () => pel, colonne: () => col };
}

/** le grain d'un visage (`_NOISE` : un bruit 96 × 96) — tiré d'une graine fixe : la même image d'une ouverture à l'autre */
let grainUrl = '';
function grain(): string {
  if (grainUrl) return grainUrl;
  const c = document.createElement('canvas');
  c.width = c.height = 96;
  const g = c.getContext('2d');
  if (!g) return '';
  const im = g.createImageData(96, 96);
  let s = 0x2545f491;
  const r = (): number => {
    s ^= s << 13;
    s ^= s >>> 17;
    s ^= s << 5;
    return (s >>> 0) / 4294967296;
  };
  for (let i = 0; i < im.data.length; i += 4) {
    const v = 140 + r() * 115;
    im.data[i] = im.data[i + 1] = im.data[i + 2] = v;
    im.data[i + 3] = r() * 24;
  }
  g.putImageData(im, 0, 0);
  grainUrl = c.toDataURL();
  return grainUrl;
}
