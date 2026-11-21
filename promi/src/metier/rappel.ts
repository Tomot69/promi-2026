/**
 * LE RAPPEL DU COMPTE — le bandeau « Garder ta Toile » de l'accueil (v52, v105, C-200 ①), jamais une notification.
 * Il paraît après le troisième Promi ou deux jours d'usage ; après chaque réponse il revient plus loin (5, puis 10, puis 20 nouvelles
 * paroles, OU 3, puis 7, puis 14 jours, le premier des deux) ; après le deuxième « Plus tard », plus jamais (« Garder ta Toile » reste aux
 * Réglages). Jamais avant la fin de l'onboarding, jamais une fois le compte fait. Les clés sont celles du prototype (`autres`).
 */
import type { Etat } from '../donnees/schema.ts';

const ECART_P = [5, 10, 20];
const ECART_J = [3, 7, 14];
const JOUR = 864e5;

export function nParoles(e: Readonly<Etat>): number {
  return e.paroles.filter((p) => !p.draft).length;
}

export function rappelDu(e: Readonly<Etat>, maintenant: number): boolean {
  const a = e.autres;
  if (a['promi_onb'] !== '1') return false;
  if ((a['promi_compte'] ?? '').startsWith('fait')) return false;
  if (a['promi_rappel_fin'] === '1') return false;
  const n = nParoles(e);
  const d0 = +(a['promi_debut'] ?? 0) || 0;
  let fois = +(a['promi_rappel_n'] ?? 0) || 0;
  let p0 = +(a['promi_rappel_p'] ?? 0) || 0;
  let t0 = +(a['promi_rappel_t'] ?? 0) || 0;
  // l'ancien « vu » compte pour une réponse (le prototype le réécrit ; ici on le lit tel quel, sans écrire)
  if (a['promi_rappel_vu'] === '1' && !fois) {
    fois = 1;
    p0 = n;
    t0 = maintenant;
  }
  if (!fois) return n >= 3 || (!!d0 && maintenant - d0 >= 2 * JOUR);
  const i = Math.min(fois, 3) - 1;
  return n - p0 >= ECART_P[i]! || (!!t0 && maintenant - t0 >= ECART_J[i]! * JOUR);
}
