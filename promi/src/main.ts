/**
 * Le démarrage de la vraie app : l'horloge (la seule), le magasin (l'état unique), la Synchro (locale en v1), la façade du moteur, puis
 * le premier écran.
 *  · `?pilote=<t0>` : l'horloge en mode piloté (tests de rendu) ;
 *  · `?banc=1`      : l'app attend qu'un test lui donne son état (`window.__promi.demarrer()`) — pour comparer au prototype.
 */
import './design/polices.css';
import './design/jetons.css';
import './design/base.css';
import { installer } from './animation/horloge.ts';
import { creerMagasin } from './etat/magasin.ts';
import { stockageLocal } from './donnees/stockage.ts';
import { creerFacade } from './moteur/facade.ts';
import { synchroLocale } from './synchro/synchro.ts';
import { monterToile } from './ecrans/toile.ts';
import { chargerPolices } from './design/polices.ts';
import { chargerTrace } from './animation/trace/trace.ts';
import { chargerFlaques } from './animation/flaques/flaques.ts';

const q = new URLSearchParams(location.search);
const pilote = q.get('pilote');
const h = installer(pilote != null ? 'pilote' : 'reel', pilote != null ? +pilote || 0 : 0);
const magasin = creerMagasin(stockageLocal());
const facade = creerFacade(magasin);
const synchro = synchroLocale();

async function etatEmbarque(): Promise<unknown> {
  // L0 : l'export de Tom, embarqué à la construction (src/donnees/etat-embarque.json, hors dépôt) ; importé au premier lancement.
  const m = import.meta.glob('./donnees/etat-embarque.json', { import: 'default' });
  const f = m['./donnees/etat-embarque.json'];
  return f ? await f() : null;
}

/**
 * L0 (lot de preuve) : l'export embarqué est importé au premier lancement, et de nouveau quand la construction en embarque un autre (sa
 * signature est gardée). L'app ne crée encore aucune donnée : rien ne se perd. Le portage de la page + (lot 2) retire ce remplacement.
 */
const CLE_EMBARQUE = 'promi.l0.embarque';
async function demarrer(): Promise<void> {
  if (q.get('banc') == null) {
    const x = await etatEmbarque();
    const sig = x ? JSON.stringify(x).length + ':' + String((x as { quand?: unknown }).quand) : null;
    if (x && sig !== localStorage.getItem(CLE_EMBARQUE)) {
      magasin.importer(x);
      localStorage.setItem(CLE_EMBARQUE, sig!);
    }
  }
  await chargerPolices();
  const app = document.getElementById('app');
  if (!app) throw new Error('#app manquant');
  monterToile(app, magasin, facade);
  void synchro.pousser(magasin.etat());
}

declare global {
  interface Window {
    __promi?: unknown;
  }
}

if (q.get('banc') != null) {
  // les tests : le magasin, la façade, l'horloge, et les modules repris (le tracé et les flaques ne servent encore aucun écran en L0)
  window.__promi = { magasin, facade, horloge: h, demarrer, chargerTrace, chargerFlaques };
} else {
  void demarrer();
}
