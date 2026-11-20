/**
 * LA TOILE VIVANTE (lot 1) — l'hôte du moteur, ses gestes et ce qu'ils demandent. Le moteur (repris) fait lui-même : glisser la vue,
 * pincer, l'élan, déplacer une dalle (appui 0,8 s, C-101), la vie au repos (C-028), le recadrage. L'app ajoute :
 *  · TOUCHER UNE DALLE (le prototype, app.html ≈ l. 7140–7250) : un toucher net — un doigt, 700 ms au plus entre l'appui et le lever
 *    (l'heure des ÉVÉNEMENTS, v139), 14 pt au plus — sur la dalle d'une parole demande SA fiche, sur celle d'un Cercle sa fiche de Cercle,
 *    260 ms plus tard (le temps de savoir s'il vient un second toucher) ; le DOUBLE TOUCHER (moins de 320 ms, 30 pt) recadre, partout ;
 *    hors de toute dalle, la dalle de parole la plus proche à 22 pt au plus, si elle est petite (C-239) ;
 * ⚠ Le moteur arrête la propagation du doigt sur son canevas (`pointerdown`, `pointerup` : stopPropagation, promi-moteur.js ≈ l. 8231) :
 * tout est écouté en phase de CAPTURE sur le parent, sans rien arrêter.
 */
import type { Facade } from '../moteur/facade.ts';
import type { Magasin } from '../etat/magasin.ts';
import type { Navigation } from '../navigation/navigation.ts';
import { horloge } from '../animation/horloge.ts';
import { toucheTolerant } from './toucher-tolerant.ts';

export function monterToile(conteneur: HTMLElement, magasin: Magasin, facade: Facade, nav: Navigation): () => void {
  const h = horloge();
  facade.monter(conteneur);
  facade.planterTout();
  const desabonne = magasin.abonner((e, action) => {
    if (action === 'choisirMonde') facade.choisirMonde(e.studio.monde);
    if (action === 'choisirTheme') facade.appliquerTheme(e.reglages.theme);
    if (action === 'importer') facade.planterTout();
  });
  const stage = facade.appareil().querySelector<HTMLElement>('#stage')!;
  const cv = facade.appareil().querySelector<HTMLCanvasElement>('#toileCv')!;

  // les doigts posés, par identifiant de pointeur : un même pointeur ne peut pas être posé deux fois — un lever perdu (capturé ailleurs,
  // sorti de la page) ne bloque donc jamais les touchers suivants ; le lever est aussi lu sur la fenêtre
  const poses = new Set<number>();
  let depart: { id: number; x: number; y: number; t: number } | null = null;
  let bouge = false;
  let tapPrecedent: { t: number; x: number; y: number; ouvre: number | null } | null = null;

  const debut = (ev: PointerEvent): void => {
    poses.add(ev.pointerId);
    stage.dataset['doigts'] = String(poses.size);
    if (poses.size > 1) {
      bouge = true;
      depart = null;
      return;
    }
    bouge = false;
    depart = { id: ev.pointerId, x: ev.clientX, y: ev.clientY, t: ev.timeStamp };
  };
  const mouvement = (ev: PointerEvent): void => {
    if (depart && (Math.abs(ev.clientX - depart.x) > 12 || Math.abs(ev.clientY - depart.y) > 12)) bouge = true;
  };
  const leve = (ev: PointerEvent): void => {
    poses.delete(ev.pointerId);
    stage.dataset['doigts'] = String(poses.size);
  };
  const fin = (ev: PointerEvent): void => {
    leve(ev);
    const g = depart;
    if (!g || g.id !== ev.pointerId) return;
    depart = null;
    if (ev.type === 'pointercancel') return;
    const dx = ev.clientX - g.x;
    const dy = ev.clientY - g.y;
    // le toucher net
    if (bouge || poses.size > 0) return;
    if (ev.timeStamp - g.t > 700) return;
    if (Math.abs(dx) > 14 || Math.abs(dy) > 14) return;
    const r = cv.getBoundingClientRect();
    if (!r.width || !r.height) return;
    const sx = (ev.clientX - r.left) * (cv.clientWidth / r.width);
    const sy = (ev.clientY - r.top) * (cv.clientHeight / r.height);
    // l'écart entre deux touchers : l'heure des ÉVÉNEMENTS (§8, v139 — le prototype l'applique à la durée d'un toucher ; ici aussi à
    // l'écart, pour qu'une image longue entre les deux ne les sépare pas)
    const maintenant = ev.timeStamp;
    const p = tapPrecedent;
    if (p && maintenant - p.t < 320 && Math.abs(ev.clientX - p.x) < 30 && Math.abs(ev.clientY - p.y) < 30) {
      tapPrecedent = null;
      if (p.ouvre != null) h.annuleMinuteur(p.ouvre);
      facade.recadrer();
      return;
    }
    let d = facade.toucher(sx, sy);
    if (!(d && (d.pid != null || (d.kind === 'nuee' && d.nuee))))
      d = toucheTolerant((x, y) => facade.toucher(x, y), sx, sy) ?? d;
    let ouvre: (() => void) | null = null;
    if (d && d.kind === 'nuee' && d.nuee) {
      const nuee = d.nuee;
      ouvre = () => {
        nav.ouvrir('cercle', nuee);
      };
    } else if (d && d.pid != null) {
      const pid = d.pid;
      if (magasin.etat().paroles.some((q) => q.id === pid))
        ouvre = () => {
          nav.ouvrir('fiche', pid);
        };
    }
    const moi = { t: maintenant, x: ev.clientX, y: ev.clientY, ouvre: null as number | null };
    if (ouvre) {
      const f = ouvre;
      moi.ouvre = h.minuteur(() => {
        if (tapPrecedent === moi) tapPrecedent = null;
        f();
      }, 260);
    }
    tapPrecedent = moi;
  };
  stage.addEventListener('pointerdown', debut, true);
  stage.addEventListener('pointermove', mouvement, true);
  stage.addEventListener('pointerup', fin, true);
  stage.addEventListener('pointercancel', fin, true);
  window.addEventListener('pointerup', leve, true);
  window.addEventListener('pointercancel', leve, true);
  return () => {
    desabonne();
    stage.removeEventListener('pointerdown', debut, true);
    stage.removeEventListener('pointermove', mouvement, true);
    stage.removeEventListener('pointerup', fin, true);
    stage.removeEventListener('pointercancel', fin, true);
    window.removeEventListener('pointerup', leve, true);
    window.removeEventListener('pointercancel', leve, true);
  };
}
