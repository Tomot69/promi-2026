/**
 * ÉCRIRE UN MOT SUR LA FICHE (lot 3b-2 ; le prototype : `ouvre`, `ferme`, `envoie`, `glisse` de lot-V145-COMM — C-116, C-257, C-260 ; « Un mot… »
 * qui part et revient par le tracé : `motLigne` de lot-V203-RETOUR).
 *
 * La ligne « Un mot… » (692 → 748) s'ouvre au toucher : le champ la prend (le clavier s'ouvre dans le geste), un filet crème de 2 pt dessous,
 * la flèche d'envoi à droite ; « Un mot… » reste en surimpression jusqu'à la première lettre (il se détrace), et revient en se traçant quand le
 * champ se vide. Envoyer (la flèche, ou Retour) : le doigt posé sur la flèche ne retire pas le focus (le clavier ne bouge pas), la flèche se
 * presse (160 ms) ; au lever le champ se vide, le mot s'écrit (le magasin) et son texte, posé sur une copie à la place du champ, vole jusqu'à sa
 * place en tête de la liste (240 ms, départ vif, arrivée douce), puis la découvre ; s'il tomberait sous la barre, la fiche glisse d'autant. Un
 * toucher ailleurs referme la saisie. Le nombre de mots (fermée) : un toucher fait glisser la fiche jusqu'au premier mot neuf, ou au plus récent.
 */
import { el, surToucher } from '../commun.ts';
import { bascule } from '../../animation/trace/retour.ts';
import { horloge } from '../../animation/horloge.ts';

const TXT = { voix: 'Un mot', envoyer: 'Envoyer' } as const;
const SVG_VA =
  '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';

export interface SaisieMot {
  ouvert(): boolean;
  fermer(): void;
}

export function monterSaisieMot(o: {
  fi: HTMLElement;
  defile: HTMLElement;
  ligne: HTMLElement;
  mot: HTMLElement;
  nb: HTMLElement;
  /** la saisie peut-elle s'ouvrir (une fiche ouverte, au repos) */
  actif: () => boolean;
  /** le mot s'écrit (le magasin) : la liste de la fiche se repose dans la même tâche */
  envoyer: (texte: string) => void;
  /** le bloc collé où vit la ligne (« Un mot… » d'un Cercle, lot 5) : le mot neuf doit se poser au-dessus de lui */
  bloc?: () => HTMLElement | null;
  /** C-267 (v201b) : la place sûre d'un défilement posé par l'app — jamais la vague à demi sous la bande (`_ficheSure`, au-delà quand il le peut) */
  sure?: (t: number) => number;
}): SaisieMot {
  const { fi, defile, ligne, mot, nb } = o;
  const saisie = el('input', {
    class: 'cm5-saisie',
    type: 'text',
    enterkeyhint: 'send',
    autocomplete: 'off',
    autocapitalize: 'sentences',
    'aria-label': TXT.voix,
  });
  const va = el('button', { type: 'button', class: 'cm5-va', 'aria-label': TXT.envoyer });
  va.innerHTML = SVG_VA;
  mot.after(saisie);
  ligne.appendChild(va);
  let ouvert = false;
  const reduit = (): boolean => matchMedia('(prefers-reduced-motion: reduce)').matches;

  // « Un mot… » : montré tant que le champ est vide (il se trace en revenant), parti à la première lettre (il se détrace)
  // (la brique commune du lot 4b, `bascule` : le prototype, `motLigne` → `avance`)
  function motVisible(v: boolean): void {
    bascule(mot, v);
  }
  saisie.addEventListener('input', () => {
    motVisible(!saisie.value);
  });

  function ouvrir(): void {
    if (ouvert || !o.actif()) return;
    ouvert = true;
    ligne.classList.add('cm5-ouvert');
    ligne.setAttribute('role', 'group');
    // le clavier s'ouvre DANS le geste (v114)
    saisie.focus({ preventScroll: true });
  }
  function fermer(): void {
    if (!ouvert) return;
    ouvert = false;
    ligne.classList.remove('cm5-ouvert');
    ligne.setAttribute('role', 'button');
    saisie.blur();
    motVisible(true);
  }

  function presse(): void {
    const g = va.querySelector('svg');
    if (!g || reduit()) return;
    g.animate([{ transform: 'scale(1)' }, { transform: 'scale(.82)', offset: 0.38 }, { transform: 'scale(1)' }], {
      duration: 160,
      easing: 'cubic-bezier(.2,.7,.3,1)',
    });
  }

  /** C-260 : le retour visuel à l'image qui suit le toucher ; le texte vole jusqu'à sa place dans la liste */
  function envoie(): void {
    const v = saisie.value.trim();
    if (!v) return;
    const R = fi.getBoundingClientRect();
    const k = R.width / (fi.offsetWidth || 1) || 1;
    const r = saisie.getBoundingClientRect();
    const cs = getComputedStyle(saisie);
    const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.2;
    const copie = el('div', { class: 'cm5-vol', 'aria-hidden': 'true' });
    copie.textContent = v;
    const x0 = (r.left - R.left) / k;
    const y0 = (r.top - R.top) / k + (r.height / k - lh) / 2;
    Object.assign(copie.style, {
      left: `${x0.toFixed(2)}px`,
      top: `${y0.toFixed(2)}px`,
      width: `${(r.width / k).toFixed(2)}px`,
      height: `${String(lh)}px`,
      font: cs.font,
      color: cs.color,
    });
    fi.appendChild(copie);
    saisie.value = '';
    saisie.focus({ preventScroll: true });
    motVisible(true);
    o.envoyer(v);
    // la cible : le texte du mot neuf, en tête de la liste ; la copie le rejoint, prend sa largeur (il passe à la ligne comme lui), puis le découvre
    const t = defile.querySelector<HTMLElement>('#cm5Liste .cm5-un .cm5-t');
    if (!t || t.textContent !== v || reduit()) {
      copie.remove();
      return;
    }
    const rt = t.getBoundingClientRect();
    const ct = getComputedStyle(t);
    const x1 = (rt.left - R.left) / k;
    const y1 = (rt.top - R.top) / k;
    const w1 = rt.width / k;
    const h1 = rt.height / k;
    t.style.visibility = 'hidden';
    Object.assign(copie.style, {
      font: ct.font,
      whiteSpace: 'pre-wrap',
      overflowWrap: 'anywhere',
      width: `${w1.toFixed(2)}px`,
      height: `${h1.toFixed(2)}px`,
      lineHeight: ct.lineHeight,
      overflow: 'visible',
    });
    const haut = Math.max(0, h1 - (parseFloat(ct.lineHeight) || 22));
    const a = copie.animate(
      [
        { transform: 'translate(0px,0px)', clipPath: `inset(0px 0px ${haut.toFixed(1)}px 0px)` },
        {
          transform: `translate(${(x1 - x0).toFixed(2)}px,${(y1 - y0).toFixed(2)}px)`,
          clipPath: 'inset(0px 0px 0px 0px)',
        },
      ],
      { duration: 240, easing: 'cubic-bezier(.33,1,.68,1)', fill: 'forwards' },
    );
    a.onfinish = (): void => {
      t.style.removeProperty('visibility');
      copie.remove();
    };
    // le mot neuf doit se VOIR se poser : s'il tomberait sous la barre (760, le clavier, ou le bloc « Un mot… » d'un Cercle), la fiche glisse
    // d'autant ; au-dessus de 120, elle remonte ; jamais au-delà de ce qui défile, ni la vague à demi sous la bande (le prototype : `envoie`)
    const vv = window.visualViewport;
    let bas = 760;
    const hb = o.bloc?.();
    const rb = hb?.getBoundingClientRect();
    if (rb?.height) bas = Math.min(bas, (rb.top - R.top) / k);
    if (vv) bas = Math.min(bas, (vv.offsetTop + vv.height - R.top) / k);
    const un = t.closest('.cm5-un')!.getBoundingClientRect();
    const hu = (un.top - R.top) / k;
    const bu = (un.bottom - R.top) / k - 12;
    let sc = 0;
    if (bu > bas - 8) {
      sc = bu - (bas - 8);
      if (!rb?.height) sc = Math.min(sc, Math.max(0, (ligne.getBoundingClientRect().top - R.top) / k - 120));
    } else if (hu < 120) sc = hu - 120;
    sc = Math.max(-defile.scrollTop, Math.min(sc, defile.scrollHeight - defile.clientHeight - defile.scrollTop));
    if (o.sure) sc = o.sure(defile.scrollTop + sc) - defile.scrollTop;
    if (Math.abs(sc) > 0.5) defile.scrollTo({ top: defile.scrollTop + sc, behavior: 'smooth' });
  }

  /** C-257 : le nombre touché, la fiche glisse jusqu'au premier mot neuf, ou au plus récent, 16 pt sous l'en-tête (le défilement doux natif) */
  function glisse(): void {
    const un =
      defile.querySelector<HTMLElement>('#cm5Liste .cm5-un[data-neuf]') ??
      defile.querySelector<HTMLElement>('#cm5Liste .cm5-un');
    if (!un) return;
    const R = defile.getBoundingClientRect();
    const k = R.width / (defile.offsetWidth || 1) || 1;
    const cible = Math.max(
      0,
      Math.min(
        defile.scrollHeight - defile.clientHeight,
        defile.scrollTop + (un.getBoundingClientRect().top - R.top) / k - 128,
      ),
    );
    if (Math.abs(cible - defile.scrollTop) >= 0.5) defile.scrollTo({ top: cible, behavior: 'smooth' });
  }

  // le doigt posé sur la flèche ne retire pas le focus du champ (le clavier ne descend pas), et elle se presse tout de suite
  va.addEventListener('pointerdown', (ev) => {
    if (!ouvert) return;
    ev.preventDefault();
    if (saisie.value.trim()) presse();
  });
  surToucher(va, () => {
    if (ouvert) envoie();
  });
  surToucher(nb, (ev) => {
    if (ouvert) return;
    ev.stopPropagation();
    glisse();
  });
  surToucher(ligne, (ev) => {
    if (ev.target instanceof Element && (ev.target.closest('.cm5-va') || ev.target.closest('.cm5-nb'))) return;
    ouvrir();
  });
  saisie.addEventListener('keydown', (ev) => {
    if (ev.key !== 'Enter') return;
    ev.preventDefault();
    envoie();
  });
  // un toucher ailleurs referme la saisie (et ne fait rien d'autre dans la fiche : son clic est avalé, 450 ms)
  let fermeA = -1e9;
  document.addEventListener(
    'pointerdown',
    (ev) => {
      if (!ouvert || (ev.target instanceof Node && ligne.contains(ev.target))) return;
      if (ev.target instanceof Node && fi.contains(ev.target)) fermeA = horloge().maintenant();
      fermer();
    },
    true,
  );
  document.addEventListener(
    'click',
    (ev) => {
      if (horloge().maintenant() - fermeA < 450) {
        ev.stopPropagation();
        ev.preventDefault();
      }
    },
    true,
  );
  ligne.setAttribute('role', 'button');
  ligne.setAttribute('aria-label', TXT.voix);

  return { ouvert: () => ouvert, fermer };
}
