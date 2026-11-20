import { describe, expect, it } from 'vitest';
import {
  GRILLE_SOUTIEN,
  PALIERS_SUGGERES,
  RANGEE_SOUTIEN,
  arrondirSoutien,
  devisSoutien,
  prixDesign,
  produitDesign,
} from '../../src/metier/achats.ts';

describe('Soutenir : la grille des produits (L0 §5)', () => {
  it('tous les 5 € de 5 à 200, tous les 25 € de 200 à 500, tous les 50 € de 500 à 1 000 — 62 produits', () => {
    expect(GRILLE_SOUTIEN.slice(0, 3)).toEqual([5, 10, 15]);
    expect(GRILLE_SOUTIEN).toContain(195);
    expect(GRILLE_SOUTIEN).toContain(225);
    expect(GRILLE_SOUTIEN).not.toContain(205);
    expect(GRILLE_SOUTIEN).toContain(550);
    expect(GRILLE_SOUTIEN).not.toContain(525);
    expect(GRILLE_SOUTIEN.at(-1)).toBe(1000);
    expect(GRILLE_SOUTIEN.length).toBe(40 + 12 + 10);
  });
  it('la rangée et les paliers suggérés (v214, 400 € gardé) sont des produits', () => {
    for (const m of [...RANGEE_SOUTIEN, ...PALIERS_SUGGERES]) expect(GRILLE_SOUTIEN).toContain(m);
    expect(PALIERS_SUGGERES).toContain(400);
  });
  it('un montant tapé est arrondi au produit le plus proche (égalité : le plus haut ; bornes 5 et 1 000)', () => {
    expect(arrondirSoutien(42)).toBe(40);
    expect(arrondirSoutien(43)).toBe(45);
    expect(arrondirSoutien(212.5)).toBe(225);
    expect(arrondirSoutien(212)).toBe(200);
    expect(arrondirSoutien(1)).toBe(5);
    expect(arrondirSoutien(5000)).toBe(1000);
    expect(arrondirSoutien(Number.NaN)).toBe(5);
  });
  it('le devis dit le montant payé AVANT la confirmation', () => {
    expect(devisSoutien(42)).toEqual({ tape: 42, paye: 40, produit: 'fr.autier.promi.soutien.40', arrondi: true });
    expect(devisSoutien(50).arrondi).toBe(false);
  });
  it('les designs : 4 € Houle, Taille-douce, Éclisse ; 6 € les autres (C-216)', () => {
    expect(prixDesign('sillons')).toBe(4);
    expect(prixDesign('mascaret')).toBe(6);
    expect(produitDesign('ramage')).toBe('fr.autier.promi.design.ramage');
    expect(() => produitDesign('encre')).toThrow();
  });
});
