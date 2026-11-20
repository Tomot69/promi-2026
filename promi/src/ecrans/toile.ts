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

  const mondes = Object.keys(MONDES_ORDRE);
  let x0: number | null = null;
  let y0 = 0;
  const debut = (ev: PointerEvent): void => {
    x0 = ev.clientX;
    y0 = ev.clientY;
  };
  const fin = (ev: PointerEvent): void => {
    if (x0 == null) return;
    const dx = ev.clientX - x0;
    const dy = ev.clientY - y0;
    x0 = null;
    if (Math.abs(dx) < 60 || Math.abs(dx) < Math.abs(dy) * 1.5) return;
    const i = mondes.indexOf(magasin.etat().studio.monde);
    const n = mondes.length;
    const suivant = mondes[((((i < 0 ? 0 : i) + (dx < 0 ? 1 : -1)) % n) + n) % n]!;
    magasin.choisirMonde(suivant);
  };
  conteneur.addEventListener('pointerdown', debut);
  conteneur.addEventListener('pointerup', fin);
  return () => {
    desabonne();
    conteneur.removeEventListener('pointerdown', debut);
    conteneur.removeEventListener('pointerup', fin);
  };
}
