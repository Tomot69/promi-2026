/**
 * L'APPAREIL : l'app est composée pour un écran de 390 × 844 pt (celui de l'iPhone 16e de Tom, celui du prototype). Sur un écran d'une
 * autre taille, elle est réduite pour tenir, centrée — comme le prototype dans Safari (l'échelle 0,79 de la porte A3). Les cotes des
 * écrans restent en points 390 × 844. (Adapter la mise en page à d'autres tailles d'écran : une décision à venir, PLAN-APP.md.)
 */
export const LARGEUR = 390;
export const HAUTEUR = 844;

export function ajusterAppareil(device: HTMLElement): () => void {
  const pose = (): void => {
    const k = Math.min(window.innerWidth / LARGEUR, window.innerHeight / HAUTEUR);
    device.style.width = LARGEUR + 'px';
    device.style.height = HAUTEUR + 'px';
    device.style.left = (window.innerWidth - LARGEUR * k) / 2 + 'px';
    device.style.top = (window.innerHeight - HAUTEUR * k) / 2 + 'px';
    device.style.transform = k === 1 ? '' : `scale(${k})`;
  };
  pose();
  window.addEventListener('resize', pose);
  return () => {
    window.removeEventListener('resize', pose);
  };
}
