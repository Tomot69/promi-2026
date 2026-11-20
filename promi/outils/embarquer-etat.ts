/**
 * L0 — L'ÉTAT EMBARQUÉ DANS LA CONSTRUCTION (le choix du 20 nov. 2026 pour le lot de preuve) : au premier lancement, l'app importe cet export
 * par le code des tests (src/donnees/migrations/prototype.ts). Cet outil copie un export dans src/donnees/etat-embarque.json (hors dépôt).
 *   node outils/embarquer-etat.ts                 l'export le plus récent de ../etats/ qui porte au moins une parole
 *   node outils/embarquer-etat.ts <fichier>       un export donné (l'intégration continue : ../banc-etats/etat-25.json)
 * L'état de Tom sur son iPhone : `python3 outils/etat_iphone.py` (à la racine) l'écrit dans etats/.
 */
import { copyFileSync, existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const ICI = import.meta.dirname;
const ETATS = join(ICI, '..', '..', 'etats');
const CIBLE = join(ICI, '..', 'src', 'donnees', 'etat-embarque.json');

function paroles(f: string): number {
  try {
    const x = JSON.parse(readFileSync(f, 'utf8')) as { ls?: Record<string, string> } & Record<string, string>;
    const st = JSON.parse((x.ls ?? x)['promi_state'] ?? '{"promises":[]}') as { promises: unknown[] };
    return st.promises.length;
  } catch {
    return 0;
  }
}

let source = process.argv[2];
if (!source) {
  if (!existsSync(ETATS)) throw new Error('aucun export : ../etats/ absent');
  source = readdirSync(ETATS)
    .filter((f) => f.endsWith('.json'))
    .map((f) => join(ETATS, f))
    .filter((f) => paroles(f) > 0)
    .sort((a, b) => statSync(b).mtimeMs - statSync(a).mtimeMs)[0];
  if (!source) throw new Error('aucun export de ../etats/ ne porte de parole');
}
copyFileSync(source, CIBLE);
console.log(`embarqué : ${source} (${paroles(source)} parole(s)) → src/donnees/etat-embarque.json`);
