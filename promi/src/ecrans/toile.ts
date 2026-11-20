/**
 * L'ÉCRAN DE PREUVE DU SOCLE (L0) : la Toile de Tom, au repos, rendue par la vraie app.
 * Ce n'est pas encore l'accueil (lot 1 : le plateau, la barre, le + ; la Toile vivante). Il n'y a rien d'autre à l'écran que la Toile.
 * Un glissé horizontal passe au monde suivant ou précédent (l'ordre du Studio), pour voir la Toile sous les vingt mondes. Rien n'est
 * acheté : en L0 tous les mondes se montrent.
 */
import type { Facade } from '../moteur/facade.ts';
import { MONDES_ORDRE } from '../moteur/facade.ts';
import type { Magasin } from '../etat/magasin.ts';

export function monterToile(conteneur: HTMLElement, magasin: Magasin, facade: Facade): () => void {
  facade.monter(conteneur);
  facade.planterTout();
  const desabonne = magasin.abonner((e, action) => {
    if (action === 'choisirMonde') facade.choisirMonde(e.studio.monde);
    if (action === 'choisirTheme') facade.appliquerTheme(e.reglages.theme);
    if (action === 'importer') facade.planterTout();
  });

  // ⚠ Le moteur arrête la propagation du doigt sur son canevas (`pointerdown` : stopPropagation et setPointerCapture, promi-moteur.js
  // ≈ l. 8231) : écouté en phase de BULLE sur le parent, le glissé n'arrivait jamais (vu par Tom sur l'iPhone, 20 nov.). Il est écouté en
  // phase de CAPTURE, avant le canevas, sans rien arrêter : le moteur garde ses gestes (glisser la vue, pincer). Un seul doigt seulement.
  const mondes = Object.keys(MONDES_ORDRE);
  const doigts = new Map<number, { x: number; y: number }>();
  let depart: { id: number; x: number; y: number } | null = null;
  const debut = (ev: PointerEvent): void => {
    doigts.set(ev.pointerId, { x: ev.clientX, y: ev.clientY });
    depart = doigts.size === 1 ? { id: ev.pointerId, x: ev.clientX, y: ev.clientY } : null;
  };
  const fin = (ev: PointerEvent): void => {
    doigts.delete(ev.pointerId);
    if (!depart || depart.id !== ev.pointerId) return;
    const dx = ev.clientX - depart.x;
    const dy = ev.clientY - depart.y;
    depart = null;
    if (ev.type === 'pointercancel' || Math.abs(dx) < 60 || Math.abs(dx) < Math.abs(dy) * 1.5) return;
    const i = mondes.indexOf(magasin.etat().studio.monde);
    const n = mondes.length;
    magasin.choisirMonde(mondes[((((i < 0 ? 0 : i) + (dx < 0 ? 1 : -1)) % n) + n) % n]!);
    facade.recadrer();
  };
  conteneur.addEventListener('pointerdown', debut, true);
  conteneur.addEventListener('pointerup', fin, true);
  conteneur.addEventListener('pointercancel', fin, true);
  return () => {
    desabonne();
    conteneur.removeEventListener('pointerdown', debut, true);
    conteneur.removeEventListener('pointerup', fin, true);
    conteneur.removeEventListener('pointercancel', fin, true);
  };
}
