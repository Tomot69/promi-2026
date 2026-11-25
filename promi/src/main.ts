/**
 * Le démarrage de la vraie app : l'horloge (la seule), le magasin (l'état unique), la Synchro (locale en v1), la façade du moteur, la
 * navigation, puis l'accueil (la Toile vivante, son plateau, sa barre) et la page + (lot 2a).
 *  · `?pilote=<t0>` : l'horloge en mode piloté (tests de rendu) ;
 *  · `?banc=1`      : l'app attend qu'un test lui donne son état (`window.__promi.demarrer()`) — pour comparer au prototype.
 */
import './design/polices.css';
import './design/jetons.css';
import './design/base.css';
import { installer } from './animation/horloge.ts';
import { creerMagasin } from './etat/magasin.ts';
import { minuit } from './metier/relecture.ts';
import { stockageLocal } from './donnees/stockage.ts';
import { creerFacade } from './moteur/facade.ts';
import { synchroLocale } from './synchro/synchro.ts';
import { monterToile } from './ecrans/toile.ts';
import { monterAccueil, type Accueil } from './ecrans/accueil/accueil.ts';
import { monterPagePlus, type PagePlus } from './ecrans/page-plus/page-plus.ts';
import { monterFiche, type Fiche } from './ecrans/fiche/fiche.ts';
import { monterIndex, type Index } from './ecrans/index/index.ts';
import { monterFil, type Fil } from './ecrans/fil/fil.ts';
import { monterPersonne, type Personne } from './ecrans/personne/personne.ts';
import { creerNavigation } from './navigation/navigation.ts';
import { chargerPolices } from './design/polices.ts';
import { chargerTrace } from './animation/trace/trace.ts';
import { chargerFlaques } from './animation/flaques/flaques.ts';

const q = new URLSearchParams(location.search);
// R3 : la version construite et le fichier du script, écrits au démarrage — sur l'iPhone, la version installée se relit dans le stockage
try {
  localStorage.setItem(
    'promi_version',
    `${__PROMI_VERSION__} ${new URL(import.meta.url).pathname.split('/').pop() ?? ''} ${new Date().toISOString()}`,
  );
} catch {
  /* stockage refusé : rien */
}
const pilote = q.get('pilote');
const h = installer(pilote != null ? 'pilote' : 'reel', pilote != null ? +pilote || 0 : 0);
// C-160 : `?jour=+N` avance aujourd'hui de N jours pour la page (jamais mémorisé) — une échéance se juge sans attendre
const decalJour = Number(q.get('jour') ?? 0) || 0;
const magasin = creerMagasin(stockageLocal(), () => {
  const d = minuit();
  d.setDate(d.getDate() + decalJour);
  return d;
});
// C-160 : au retour au premier plan, les échéances sont recomptées (une parole peut avoir passé sa date pendant la nuit)
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') magasin.recompter();
});
const facade = creerFacade(magasin);
const synchro = synchroLocale();
const nav = creerNavigation(() => h.maintenant());
let accueil: Accueil | null = null;
let pagePlus: PagePlus | null = null;
let fiche: Fiche | null = null;
let index: Index | null = null;
let fil: Fil | null = null;
let personne: Personne | null = null;

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
async function demarrer(o: { accueil?: boolean } = {}): Promise<void> {
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
  monterToile(app, magasin, facade, nav);
  // les bancs de la Toile seule (banc-rendu, entrées du moteur) la jugent sans l'accueil : `demarrer({ accueil: false })`
  if (o.accueil !== false) {
    accueil = monterAccueil(facade, magasin, nav);
    pagePlus = monterPagePlus(facade, magasin, nav);
    index = monterIndex(facade, magasin, nav);
    fil = monterFil(facade, magasin, nav);
    personne = monterPersonne(facade, magasin, nav);
    fiche = monterFiche(facade, magasin, nav);
  }
  void synchro.pousser(magasin.etat());
}

declare global {
  interface Window {
    __promi?: unknown;
  }
}

if (q.get('banc') != null) {
  // les tests : le magasin, la façade, l'horloge, et les modules repris (le tracé et les flaques ne servent encore aucun écran en L0)
  window.__promi = {
    magasin,
    facade,
    horloge: h,
    nav,
    accueil: () => accueil,
    pagePlus: () => pagePlus,
    fiche: () => fiche,
    index: () => index,
    fil: () => fil,
    personne: () => personne,
    demarrer,
    chargerTrace,
    chargerFlaques,
  };
} else {
  void demarrer();
}
