/**
 * LE CHOIX DES PERSONNES (le prototype : `rend()` et la saisie `SA` de lot-GENS, C-122, C-269, C-332) — UNE brique, pour la page + et pour
 * Peaufiner sur la fiche (le prototype les sert par le même `rend`).
 *
 * LA LISTE : « Moi » (ou « tout le monde ») en tête quand il y en a une, les personnes choisies, puis les connues (six de plus au plus) — un
 * visage rond (l'initiale), le nom, la croix d'une personne choisie ; dessous, sur sa ligne, « + ajouter quelqu'un » en pointillés.
 * AJOUTER (C-122, v146) : on écrit DANS la zone en pointillés — une entrée invisible garde le clavier ; le nom à l'encre, « un prénom… » dans la
 * teinte de la zone ; dès la première lettre, un « + » orange tracé, à la hauteur des capitales du nom, valide (Retour aussi) ; le nom posé, la
 * zone se propose pour le suivant, le clavier reste ; rien ne passe sous le clavier (l'écran se suit, `suivre`).
 * Ce que le choix FAIT (qui est choisi, ce que « Moi » veut dire) appartient à l'écran : il le dit dans `CfgGens`.
 */
import { el, surToucher } from '../commun.ts';
import { horloge } from '../../animation/horloge.ts';
import { chargerTrace } from '../../animation/trace/trace.ts';
import { copieA, detracerCopie, remplacer } from '../../animation/trace/retour.ts';
import { TEXTES_PAGE_PLUS as T } from '../../textes/page-plus.ts';
import type { Etat } from '../../donnees/schema.ts';

export const SVG_PLUS =
  '<svg viewBox="0 0 10 10" aria-hidden="true"><path class="h" d="M0 5 H10"/><path class="v" d="M5 0 V10"/></svg>';
export const SVG_X =
  '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 2 L10 10 M10 2 L2 10" fill="none" stroke-width="2" stroke-linecap="round"/></svg>';

const reduit = (): boolean => {
  try {
    return matchMedia('(prefers-reduced-motion: reduce)').matches;
  } catch {
    return false;
  }
};

/** les personnes connues : celles des paroles (la plus récente d'abord), puis celles qu'on a écrites, puis les membres des Cercles */
export function connus(e: Etat): string[] {
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

export interface CfgGens {
  nat: string;
  /** les personnes choisies (sans la tête) */
  choisis: () => string[];
  /** la tête (« Moi »), ou rien */
  tete: string | null;
  teteOn: () => boolean;
  /** la tête porte sa croix quand elle est choisie (« Moi », v199) */
  teteCroix: boolean;
  /** un toucher sur une personne (sur sa croix : `croix`) ; sur la tête : `nom` null */
  touche: (nom: string | null, croix: boolean) => void;
  connus: () => string[];
}

/** la liste (`.gn` : `.gn-liste` des pastilles, puis « + ajouter quelqu'un ») ; `ajout` : le toucher sur la zone d'ajout (son « + » : `plus`) */
export function rendreListe(
  cfg: CfgGens,
  ajout: (plus: boolean) => void,
): { gn: HTMLElement; liste: HTMLElement; zone: HTMLElement } {
  const pris = cfg.choisis();
  const noms = [...pris];
  for (const n of cfg.connus()) if (!noms.includes(n) && noms.length < pris.length + 6) noms.push(n);
  const gn = el('div', { class: 'ph-opts gn', 'data-nat': cfg.nat });
  const gl = el('div', { class: 'gn-liste' });
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
    if (on && (!tetee || cfg.teteCroix)) {
      const x = el('span', { class: 'ppo-x', role: 'button', 'aria-label': `${T.retirer} ${nom.toLowerCase()}` });
      x.innerHTML = SVG_X;
      b.appendChild(x);
    }
    surToucher(b, (ev) => {
      cfg.touche(tetee ? null : nom, !!(ev.target as Element).closest('.ppo-x'));
    });
    return b;
  };
  if (cfg.tete) gl.appendChild(bouton(cfg.tete, cfg.teteOn(), true));
  for (const n of noms) gl.appendChild(bouton(n, pris.includes(n), false));
  // la zone d'ajout : vide ici, l'ajout la peint (`Ajout.rendre`) — « + ajouter quelqu'un », ou la ligne où l'on écrit
  const zone = el('div', { class: 'ph-o ph-add', role: 'button', tabindex: '0', 'data-add': '1' });
  surToucher(zone, (ev) => {
    ajout(!!(ev.target as Element).closest('.gn-plus'));
  });
  // 27 nov. 2026 (l'iPhone de Tom : « le clavier ne s'ouvre pas ») — au DOIGT, le navigateur envoie après le lever un `mousedown` de
  // compatibilité qui donne le focus à la zone (`tabindex`) : l'entrée du prénom, focalisée dans le geste, le perdait aussitôt et le clavier
  // se refermait (à la souris l'ordre est inverse : les bancs ne le voyaient pas). La zone ne prend jamais le focus par la souris.
  zone.addEventListener('mousedown', (ev) => {
    ev.preventDefault();
  });
  gn.append(gl, zone);
  return { gn, liste: gl, zone };
}

export interface Ajout {
  /** l'entrée invisible (le clavier) */
  champ: HTMLInputElement;
  actif: () => boolean;
  /** le toucher sur la zone : le clavier s'ouvre DANS le geste (iOS) ; sur son « + » : le nom est validé */
  touche: (plus: boolean) => void;
  /** la zone `z` (sinon celle de l'écran) repeinte — après une reconstruction de la liste, avant qu'elle soit posée */
  rendre: (z?: HTMLElement) => void;
  /** l'entrée invisible posée sur la zone (une fois la liste à sa place) */
  poser: () => void;
  fermer: () => void;
  /** tout remis à zéro (l'écran se ferme) */
  remettre: () => void;
  /** rien ne passe sous le clavier : l'écart dont l'écran s'est déplacé */
  suivre: () => void;
}

/**
 * l'ajout d'une personne, dans la zone que `zone()` rend : `valider(nom)` pose le nom (sa graphie connue reprise, « rachel » → « Rachel ») ;
 * `deplacer(y)` : l'écran monte de y pt pour garder la zone 14 pt au-dessus du clavier (0 : à sa place)
 */
export function monterAjout(o: {
  parent: HTMLElement;
  zone: () => HTMLElement | null;
  surface: HTMLElement;
  connus: () => string[];
  valider: (nom: string) => void;
  deplacer: (y: number) => void;
}): Ajout {
  const h = horloge();
  const champ = el('input', {
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
  // il n'existe que pendant qu'on écrit un prénom (hors de là, aucun champ sans porte : redteam_champs)
  champ.hidden = true;
  o.parent.appendChild(champ);
  let actif = false;
  let plusVu = false;
  let dec = 0;

  // C-271 (v203 clôture §2) : « + ajouter quelqu’un » ↔ la ligne de saisie, l'ancien se détrace et le neuf se trace ; « un prénom… » part et
  // revient par le tracé — rien ne change d'un coup
  function rendre(zz?: HTMLElement): void {
    const z = zz ?? o.zone();
    if (!z) return;
    const etaitEdit = z.classList.contains('gn-edit');
    const phAvant = z.querySelector<HTMLElement>('.gn-ph');
    if (!actif) {
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
    const v = champ.value;
    const nom = v.replace(/\s+/g, ' ').trim();
    // rien n'a changé (un focus, le clavier qui bouge) : la ligne reste — rebâtie, elle perdrait son tracé en cours (il paraîtrait d'un coup)
    if (etaitEdit && z.dataset['v'] === v) {
      z.classList.toggle('gn-repos', document.activeElement !== champ);
      return;
    }
    z.dataset['v'] = v;
    if (etaitEdit && phAvant && v) detracerCopie(phAvant);
    const devientEdit = !etaitEdit && !!(z.textContent ?? '').trim();
    const copie = devientEdit && !reduit() && z.getClientRects().length ? copieA(z) : null;
    z.className = 'ph-o ph-add gn-edit' + (document.activeElement === champ ? '' : ' gn-repos');
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
  function ouvrir(): void {
    if (!actif) {
      actif = true;
      champ.value = '';
      plusVu = false;
    }
    champ.hidden = false;
    // le focus DANS le geste : iOS n'ouvre le clavier qu'ainsi (v115)
    champ.focus({ preventScroll: true });
    rendre();
    poser();
    suivre();
  }
  function valider(): void {
    let n = champ.value.replace(/\s+/g, ' ').trim();
    if (!n) return;
    for (const c of o.connus()) if (c.toLowerCase() === n.toLowerCase()) n = c;
    champ.value = '';
    plusVu = false;
    o.valider(n);
    // le nom est posé ; la zone se propose pour le suivant, le clavier reste
    champ.focus({ preventScroll: true });
    rendre();
    suivre();
  }
  function fermer(): void {
    if (!actif) return;
    actif = false;
    champ.value = '';
    if (document.activeElement === champ) champ.blur();
    champ.hidden = true;
    rendre();
    suivre();
  }
  /** l'entrée invisible se tient SUR la zone : si le navigateur cherche le curseur, il le trouve là */
  function poser(): void {
    const z = o.zone();
    if (!z) return;
    const C = o.parent.getBoundingClientRect();
    const k = C.width / (o.parent.offsetWidth || 1) || 1;
    const r = z.getBoundingClientRect();
    champ.style.left = `${String(Math.round((r.left - C.left) / k + r.width / k / 2))}px`;
    champ.style.top = `${String(Math.round((r.top - C.top) / k + r.height / k / 2 - 10))}px`;
  }
  /** rien ne passe sous le clavier (v146) : l'écran monte pour garder la zone 14 pt au-dessus de lui (le haut du clavier se LIT) */
  function suivre(): void {
    const vv = window.visualViewport;
    const z = actif ? o.zone() : null;
    let besoin = 0;
    if (vv && z && document.activeElement === champ && window.innerHeight - vv.height >= 100) {
      const k = o.surface.getBoundingClientRect().width / (o.surface.offsetWidth || 1) || 1;
      besoin = Math.max(0, (z.getBoundingClientRect().bottom + dec * k + 14 * k - (vv.offsetTop + vv.height)) / k);
    }
    besoin = Math.round(besoin);
    if (besoin === dec) return;
    const de = dec;
    dec = besoin;
    // l'écran glisse (jamais d'un coup) : le mouvement du clavier, 300 ms
    const doux = (p: number): number => (p < 0.5 ? 2 * p * p : 1 - (-2 * p + 2) ** 2 / 2);
    const t0 = h.maintenant();
    const pas = (): void => {
      const p = reduit() ? 1 : Math.min(1, (h.maintenant() - t0) / 300);
      o.deplacer(de + (besoin - de) * doux(p));
      if (p < 1 && dec === besoin) h.image(pas);
    };
    pas();
  }
  champ.addEventListener('input', () => {
    rendre();
  });
  champ.addEventListener('keydown', (ev) => {
    if (ev.key === 'Enter') {
      ev.preventDefault();
      valider();
    } else if (ev.key === 'Escape') fermer();
  });
  champ.addEventListener('focus', () => {
    rendre();
    suivre();
  });
  // le clavier se retire sur une zone VIDE : elle reprend son mot ; sur un nom écrit, il reste, avec son « + »
  champ.addEventListener('blur', () => {
    h.minuteur(() => {
      if (!actif || document.activeElement === champ) return;
      if (!champ.value.trim()) fermer();
      else {
        rendre();
        suivre();
      }
    }, 0);
  });
  window.visualViewport?.addEventListener('resize', suivre);

  return {
    champ,
    actif: () => actif,
    touche: (plus) => {
      if (plus) valider();
      else ouvrir();
    },
    rendre,
    poser,
    fermer,
    remettre: () => {
      actif = false;
      champ.value = '';
      if (document.activeElement === champ) champ.blur();
      champ.hidden = true;
      dec = 0;
      o.deplacer(0);
    },
    suivre,
  };
}
