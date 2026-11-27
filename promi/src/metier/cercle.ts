/**
 * LA FICHE D'UN CERCLE (lot 5, SPEC-ECRANS §7) — ce qu'elle DIT, sans rien peindre : ses paroles (dans l'ordre où elles sont gardées), la hauteur
 * de son trait (§9), la ligne « Avec … » (cadres 58 et 60), la ligne d'état (Q213), le mot de chaque ligne du fil (« CHICHE LANCÉ », « TENU » :
 * `promi-nuee-toile.html`, cadre 10). Le prototype : `renderDetail` (l'en-tête d'une Nuée), `_ficheNuee` (lot-S1B-geo). Les formes sont celles du
 * prototype, au caractère près ; les tests les portent en dur (tests/unitaires/cercle.test.ts).
 */
import type { Parole } from '../donnees/schema.ts';
import { champ } from './fiche.ts';

/** les dessins des Cercles (C-042 : la clé du prototype, `promi_dessins_cercle` — un objet { clé du Cercle : dessin }), lus dans les clés gardées */
export function dessinsCercles(autres: Readonly<Record<string, string>>): Record<string, unknown> {
  try {
    const L = JSON.parse(autres['promi_dessins_cercle'] ?? '{}') as Record<string, unknown> | null;
    return L && typeof L === 'object' ? L : {};
  } catch {
    return {};
  }
}

/** les paroles d'un Cercle — jamais un gardé de côté — dans l'ordre où elles sont gardées (le fil les montre ainsi) */
export function parolesDuCercle(paroles: readonly Parole[], cle: string): Parole[] {
  return paroles.filter((q) => !q.draft && q.nuee === cle);
}

/**
 * §9 · la base du trait d'un Cercle : `max(176, 460 − 86 n)`, n = les lignes du fil, « Planter dans le Cercle » comprise (Q213) ; amplitude 40,
 * le trait entier (personne ne vient à la rencontre d'un Cercle).
 */
export function baseCercle(nParoles: number): number {
  return Math.max(176, 460 - 86 * (nParoles + 1));
}
export const AMP_CERCLE = 40;

/** « Avec Rachel, Adrien, +3 » — deux nommés, puis le reste, MOI COMPRIS ; « Avec toi seulement » sans membre */
export function ligneAvec(membres: readonly string[]): string {
  if (!membres.length) return 'Avec toi seulement';
  const reste = membres.length - 1;
  return 'Avec ' + membres.slice(0, 2).join(', ') + (reste > 0 ? ', +' + String(reste) : '');
}

/** « 5 Promi · 2 tenus » ; « encore aucune parole » (Q213) — en capitales par la feuille de style */
export function ligneEtatCercle(liste: readonly Parole[]): string {
  if (!liste.length) return 'encore aucune parole';
  const t = liste.filter((q) => q.status === 'tenu').length;
  return String(liste.length) + ' Promi' + (t ? ' · ' + String(t) + ' tenu' + (t > 1 ? 's' : '') : '');
}

/** le mot d'une ligne du fil : l'état d'un Promi (« en cours », « TENU ») ; la nature d'un Chiche (« CHICHE LANCÉ », « CHICHE RELEVÉ ») */
export function motDuFil(p: Parole): string {
  const tenu = p.status === 'tenu';
  if (p.chiche) return champ(p, 'chicheEtat') === 'releve' || tenu ? 'CHICHE RELEVÉ' : 'CHICHE LANCÉ';
  return tenu ? 'TENU' : 'en cours';
}
