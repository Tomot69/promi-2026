/**
 * LE FICHIER STOREKIT DE TEST (achats/Promi.storekit), ENGENDRÉ depuis la règle des achats (src/metier/achats.ts) — jamais retouché à la
 * main. Xcode le joue quand on lance l'app depuis Xcode (Product › Scheme › Edit Scheme › Run › Options › StoreKit Configuration) :
 * les achats se testent en local, sans compte App Store Connect.
 *   · Soutenir : un consommable par montant de la grille (62), `fr.autier.promi.soutien.N` ;
 *   · les designs du Studio : un achat non consommable par monde payant (12), `fr.autier.promi.design.<monde>`, 4 € ou 6 €.
 * L'abonnement Ma Parole ! n'y est pas : son prix est une décision de Tom (C-090).
 * node outils/storekit-engendrer.ts [--verifie]
 */
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { GRILLE_SOUTIEN, MONDES_PAYANTS, PREFIXE_DESIGN, PREFIXE_SOUTIEN, prixDesign } from '../src/metier/achats.ts';

const NOMS: Record<string, string> = {
  ramage: 'Ramage',
  guingois: 'Guingois',
  chantourne: 'Chantourné',
  volubilis: 'Volubilis',
  madrure: 'Madrure',
  chamade: 'Chamade',
  ritournelle: 'Ritournelle',
  bobinette: 'Bobinette',
  mascaret: 'Mascaret',
  terrazzo: 'Éclisse',
  gravure: 'Taille-douce',
  sillons: 'Houle',
};

let n = 0;
const id = (): string => (++n).toString(16).toUpperCase().padStart(8, '0');
const produit = (
  productID: string,
  prix: number,
  type: 'Consumable' | 'NonConsumable',
  nom: string,
  desc: string,
): object => ({
  displayPrice: prix.toFixed(2),
  familyShareable: false,
  internalID: id(),
  localizations: [{ description: desc, displayName: nom, locale: 'fr_FR' }],
  productID,
  referenceName: nom,
  type,
});

const config = {
  identifier: 'PROMI0L0',
  nonRenewingSubscriptions: [],
  products: [
    ...GRILLE_SOUTIEN.map((m) =>
      produit(PREFIXE_SOUTIEN + m, m, 'Consumable', `Soutenir Promi — ${m} €`, 'Un soutien à Promi.'),
    ),
    ...MONDES_PAYANTS.map((w) =>
      produit(
        PREFIXE_DESIGN + w,
        prixDesign(w),
        'NonConsumable',
        `Design ${NOMS[w] ?? w}`,
        `Le monde ${NOMS[w] ?? w} au Studio.`,
      ),
    ),
  ],
  settings: {
    _applicationInternalID: 'PROMI',
    _developerTeamID: 'B77VBMD9BF',
    _locale: 'fr_FR',
    _storefront: 'FRA',
    _storeKitErrors: [],
  },
  subscriptionGroups: [],
  version: { major: 4, minor: 0 },
};

const f = join(import.meta.dirname, '..', 'achats', 'Promi.storekit');
const texte = JSON.stringify(config, null, 2) + '\n';
if (process.argv.includes('--verifie')) {
  if (!existsSync(f) || readFileSync(f, 'utf8') !== texte) {
    console.error('achats/Promi.storekit diffère de ce que la règle engendre');
    process.exit(1);
  }
  console.log('✓ achats/Promi.storekit');
} else {
  writeFileSync(f, texte);
  console.log(`achats/Promi.storekit : ${config.products.length} produits`);
}
