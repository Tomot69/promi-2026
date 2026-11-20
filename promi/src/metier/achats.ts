/**
 * LES ACHATS — la règle, sans écran. Les produits déclarés dans l'App Store et Google Play (et le fichier StoreKit de test,
 * achats/Promi.storekit, engendré par outils/storekit-engendrer.ts depuis CE fichier).
 *
 * ── SOUTENIR (C-217, C-313, C-318 ; décision du 20 nov. 2026, lot L0 §5) ──
 * Apple n'accepte pas un montant libre pour un achat intégré (règle 3.1.1) : chaque prix est un produit consommable déclaré d'avance.
 * La grille est assez fine pour que presque tout montant tapé existe : tous les 5 € de 5 à 200 €, tous les 25 € de 200 à 500 €,
 * tous les 50 € de 500 à 1 000 €. Un montant tapé est ARRONDI au produit le plus proche (à égale distance : le plus haut) ; le montant
 * réellement payé est affiché AVANT la confirmation d'achat, jamais après.
 * La rangée et les paliers suggérés sont ceux du prototype (v214, C-318 ; 400 € gardé).
 *
 * ── LES DESIGNS DU STUDIO (C-216) ── 4 € pour Houle, Taille-douce, Éclisse (sillons, gravure, terrazzo) ; 6 € pour les neuf autres.
 */

export const PREFIXE_SOUTIEN = 'fr.autier.promi.soutien.';
export const PREFIXE_DESIGN = 'fr.autier.promi.design.';

/** la rangée de Soutenir (C-318) */
export const RANGEE_SOUTIEN = [5, 10, 25, 50, 100, 150] as const;
/** les paliers suggérés sous « Autre montant » (C-318 ; 400 € à la place de 150) */
export const PALIERS_SUGGERES = [15, 20, 30, 40, 75, 200, 250, 300, 400, 500, 750, 1000] as const;

/** la grille des produits consommables, en euros, croissante */
export function grilleSoutien(): number[] {
  const g: number[] = [];
  for (let m = 5; m <= 200; m += 5) g.push(m);
  for (let m = 225; m <= 500; m += 25) g.push(m);
  for (let m = 550; m <= 1000; m += 50) g.push(m);
  return g;
}

export const GRILLE_SOUTIEN: readonly number[] = Object.freeze(grilleSoutien());

export function produitSoutien(euros: number): string {
  if (!GRILLE_SOUTIEN.includes(euros)) throw new Error(`soutien : ${euros} € n'est pas un produit déclaré`);
  return PREFIXE_SOUTIEN + euros;
}

/** Le montant tapé → le produit le plus proche de la grille (égalité : le plus haut ; hors de la grille : ses bornes). */
export function arrondirSoutien(tape: number): number {
  if (!isFinite(tape) || tape <= GRILLE_SOUTIEN[0]!) return GRILLE_SOUTIEN[0]!;
  let meilleur = GRILLE_SOUTIEN[0]!;
  for (const m of GRILLE_SOUTIEN) {
    const d = Math.abs(m - tape);
    const dm = Math.abs(meilleur - tape);
    if (d < dm || (d === dm && m > meilleur)) meilleur = m;
  }
  return meilleur;
}

export interface Devis {
  tape: number;
  paye: number;
  produit: string;
  /** vrai si le montant payé diffère du montant tapé : l'écran le dit avant la confirmation */
  arrondi: boolean;
}

export function devisSoutien(tape: number): Devis {
  const paye = arrondirSoutien(tape);
  return { tape, paye, produit: produitSoutien(paye), arrondi: paye !== tape };
}

export const MONDES_A_4 = ['sillons', 'gravure', 'terrazzo'] as const;
export const MONDES_PAYANTS = [
  'ramage',
  'guingois',
  'chantourne',
  'volubilis',
  'madrure',
  'chamade',
  'ritournelle',
  'bobinette',
  'mascaret',
  'terrazzo',
  'gravure',
  'sillons',
] as const;

export function prixDesign(monde: string): 4 | 6 {
  return (MONDES_A_4 as readonly string[]).includes(monde) ? 4 : 6;
}
export function produitDesign(monde: string): string {
  if (!(MONDES_PAYANTS as readonly string[]).includes(monde))
    throw new Error(`design : ${monde} n'est pas un monde payant`);
  return PREFIXE_DESIGN + monde;
}
