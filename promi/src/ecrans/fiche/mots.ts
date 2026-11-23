/**
 * « LES MOTS » SUR LA FICHE (lot 3a-3 : la liste affichée, pour que la fiche défile comme dans le prototype ; la saisie, l'envoi, les mots neufs : 3b) —
 * `peintListe`, `rangee` et `titre` de lot-V145-COMM (C-248, C-261) : sous « Un mot… » (692 → 748), le titre « Les Mots » 32 pt plus bas (780,
 * Gilbert 700 13/16, capitales, chasse 0,10 em, `--c-beige67`), puis la liste 16 + 36 pt plus bas (832) : les mots du plus récent au plus ancien —
 * le visage rond de 22 (son fond : `_blobBg`), le nom (Gilbert 700 16/22, coupé à 180 pt comme `_noms.court`) et sa date (Atkinson 13/22,
 * `_noms.date`), le texte (Atkinson 16/1,35). Aucun mot : ni titre ni liste.
 */
import type { Mot } from '../../donnees/schema.ts';
import { el, esc } from '../commun.ts';
import { palette } from '../../design/jetons.ts';
import { chargerTrace } from '../../animation/trace/trace.ts';

/** les quatre tons de la palette d'identité (`_BPAL`, 20 sept.) */
const BPAL = [palette.bleu45, palette.framboise54, palette.mauve77, palette.creme922] as const;
const TXT = { titre: 'Les Mots', instant: 'à l’instant', hier: 'hier' } as const;
/** les cotes de lot-V145-COMM : la ligne « Un mot… » (692, 56 de haut), le titre 32 plus bas, 16 de titre, 36 jusqu'au premier mot */
export const COTES_MOTS = { LIGNE_Y: 692, LIGNE_H: 56, HAUT: 32, TITRE_H: 16, SOUS: 36 } as const;

/**
 * le hachage du prototype (`_hashN`) — tel quel : la multiplication est FLOTTANTE (`(h * 16777619) >>> 0`), pas entière ; au-delà de 2^53 elle
 * arrondit, et c'est cet arrondi qui tire les taches d'un visage (un vrai FNV-1a, `Math.imul`, donnait d'autres visages)
 */
function hashN(s: string): number {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = (h * 16777619) >>> 0;
  }
  return h;
}

/** le fond d'un visage sans photo : quatre taches tirées de la graine, sur un ton de la palette (`_blobBg`) */
export function fondVisage(graine: string): string {
  const h = hashN(graine) >>> 0;
  const L: string[] = [];
  for (let i = 0; i < 4; i++) {
    const hx = Math.imul(h, ((i * 2 + 1) * 2654435761) >>> 0) >>> 0;
    const x = 8 + (hx % 84);
    const y = 8 + ((hx >>> 7) % 84);
    const sp = 38 + ((hx >>> 14) % 34);
    const col = BPAL[(hx >>> 3) % BPAL.length]!;
    L.push(`radial-gradient(circle at ${String(x)}% ${String(y)}%,${col} 0%,transparent ${String(sp)}%)`);
  }
  const base = BPAL[(h >>> 11) % BPAL.length]!;
  return L.join(',') + `,radial-gradient(circle at 50% 50%,${base} 0%,${base} 100%)`;
}

/** la date d'un mot (`_noms.date`) : « à l’instant », « il y a 5 min », « il y a 2 h », « hier », « 3 nov. » (l'année au-delà d'un an) */
export function dateMot(iso: string, maintenant: number): string {
  const d = new Date(iso);
  const n = new Date(maintenant);
  const s = (n.getTime() - d.getTime()) / 1000;
  if (!Number.isFinite(s)) return '';
  if (s < 60) return TXT.instant;
  if (s < 3600) return `il y a ${String(Math.floor(s / 60))} min`;
  if (d.toDateString() === n.toDateString()) return `il y a ${String(Math.floor(s / 3600))} h`;
  const h = new Date(n);
  h.setDate(n.getDate() - 1);
  if (d.toDateString() === h.toDateString()) return TXT.hier;
  const o: Intl.DateTimeFormatOptions = { day: 'numeric', month: 'short' };
  if (s > 365 * 86400) o.year = 'numeric';
  return d.toLocaleDateString('fr-FR', o);
}

export interface HoteMots {
  /** le conteneur où vivent le titre et la liste (la couche qui défile) */
  dans: HTMLElement;
  /** mon prénom et ma graine (un mot de « moi » : mon nom, mon visage) */
  moi(): { nom: string; graine: number };
  /** les prénoms connus, pour couper un nom trop long à la lettre qui le distingue (`_noms.court`) */
  tous(): string[];
  maintenant(): number;
}

export interface Mots {
  /** pose la liste de la parole ; rend le bas de ce qu'elle occupe (pt de la fiche), ou null sans mot */
  poser(mots: readonly Mot[], dy: number): number | null;
  retirer(): void;
}

export function monterMots(h: HoteMots): Mots {
  const titre = el('div', { id: 'cm5Titre', class: 'cm5 cm5-titre', role: 'heading', 'aria-level': '2' });
  const liste = el('div', { id: 'cm5Liste', class: 'cm5 cm5-liste' });
  let sig = '';

  let cv: CanvasRenderingContext2D | null = null;
  function largeur(t: string): number {
    cv ??= document.createElement('canvas').getContext('2d')!;
    cv.font = '700 16px Gilbert';
    return cv.measureText(t).width;
  }
  /** `_noms.court(nom, {largeur: 180})` : entier s'il tient, sinon six lettres et « . », prolongé jusqu'à la lettre qui le distingue */
  function court(nom: string): string {
    if (!nom || largeur(nom) <= 180) return nom;
    const L = Array.from(nom);
    const bas = Array.from(nom.toLowerCase());
    const A = h
      .tous()
      .filter((x) => x.toLowerCase() !== nom.toLowerCase())
      .map((x) => Array.from(x.toLowerCase()));
    let n = 6;
    while (n < L.length && A.some((a) => a.length >= n && a.slice(0, n).join('') === bas.slice(0, n).join(''))) n++;
    return n >= L.length ? nom : L.slice(0, n).join('') + '.';
  }

  function rangee(m: Mot): string {
    const me = h.moi();
    const deMoi = /^moi$/i.test(String(m.by || 'moi'));
    const qui = deMoi ? me.nom : m.by;
    const estMoi = deMoi || qui === me.nom;
    const fond = fondVisage(deMoi ? 'u' + String(me.graine) : String(m.by));
    return (
      '<div class="cm5-un"><i class="cm5-vis" aria-hidden="true" style="background:' +
      fond +
      '"></i><div class="cm5-corps"><div class="cm5-qui"><span class="nom-lien" data-nom="' +
      esc(qui) +
      '"' +
      (estMoi ? ' data-moi="1"' : ' role="link"') +
      '>' +
      esc(court(qui)) +
      '</span><span class="cm5-date">' +
      esc(dateMot(m.d, h.maintenant())) +
      '</span></div><div class="cm5-t">' +
      esc(m.t) +
      '</div></div></div>'
    );
  }

  /** sans mot : ni titre ni liste (cachés ; le titre ne se trace qu'à sa première apparition, comme `titre()` du prototype) */
  function retirer(): void {
    titre.hidden = true;
    liste.hidden = true;
  }

  function poser(mots: readonly Mot[], dy: number): number | null {
    const L = [...mots].sort((a, b) => String(a.d).localeCompare(String(b.d))).reverse();
    if (!L.length) {
      retirer();
      return null;
    }
    const C = COTES_MOTS;
    const yT = C.LIGNE_Y + C.LIGNE_H + C.HAUT;
    titre.style.top = `${String(yT)}px`;
    liste.style.top = `${String(yT + C.TITRE_H + C.SOUS)}px`;
    for (const e of [titre, liste]) e.style.translate = dy ? `0 ${String(dy)}px` : '';
    const s = L.map((m) => [m.d, m.by, m.t].join('|')).join('§');
    if (s !== sig) {
      sig = s;
      liste.innerHTML = L.map(rangee).join('');
    }
    liste.hidden = false;
    titre.hidden = false;
    if (!liste.isConnected) h.dans.appendChild(liste);
    if (!titre.isConnected) {
      // le titre paraît en se traçant, à sa création (`titre()` de lot-V145-COMM ; réduire les animations : posé d'emblée)
      titre.textContent = TXT.titre;
      h.dans.insertBefore(titre, liste);
      if (!matchMedia('(prefers-reduced-motion: reduce)').matches) chargerTrace().trace(titre, null);
    }
    return yT + C.TITRE_H + C.SOUS + liste.offsetHeight + dy;
  }

  return { poser, retirer };
}
