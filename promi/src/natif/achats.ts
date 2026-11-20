/**
 * LES ACHATS, CÔTÉ APPAREIL — une interface, deux implémentations.
 *  · `achatsLocaux` (L0, et tant qu'il n'y a pas de comptes payants) : rien ne part ; l'achat réussit tout de suite. Sur l'appareil,
 *    Xcode joue le fichier StoreKit de test (achats/Promi.storekit) quand on lance l'app depuis Xcode.
 *  · RevenueCat (`@revenuecat/purchases-capacitor`, StoreKit 2 et Google Play Billing) : branché au lot 7 (Studio et achats), quand
 *    Tom aura ouvert ses comptes ; il faut sa clé d'API publique. Rien d'autre ne change : l'écran parle à cette interface.
 * Le montant tapé de Soutenir est arrondi par src/metier/achats.ts, et affiché AVANT la confirmation.
 */
import { devisSoutien, produitDesign, type Devis } from '../metier/achats.ts';

export type Resultat = { ok: true; produit: string } | { ok: false; raison: 'annule' | 'erreur'; detail?: string };

export interface Achats {
  readonly nom: 'local' | 'revenuecat';
  /** le devis à montrer avant la confirmation (montant tapé → montant payé) */
  devis(tape: number): Devis;
  soutenir(d: Devis): Promise<Resultat>;
  acheterDesign(monde: string): Promise<Resultat>;
  /** les designs acquis (pour la réouverture, et la restauration) */
  acquis(): Promise<string[]>;
}

export function achatsLocaux(): Achats {
  const designs = new Set<string>();
  return {
    nom: 'local',
    devis: devisSoutien,
    soutenir: (d) => Promise.resolve({ ok: true, produit: d.produit }),
    acheterDesign(monde) {
      const produit = produitDesign(monde);
      designs.add(monde);
      return Promise.resolve({ ok: true, produit });
    },
    acquis: () => Promise.resolve([...designs]),
  };
}
