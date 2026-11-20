/**
 * Les dessins des icônes de l'accueil — des DONNÉES (des tracés), relevées sur le prototype (`lot-ACCUEIL`, `ICO` ; le + ; le symbole
 * « recadrer » de `lot-ZOOM`, C-099). Le trait est porté par la feuille de style (accueil.css), jamais ici : un seul propriétaire.
 */
export const ICONES = {
  studio:
    '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="M7 11 L14 9 L16 15 L11 20 L6 17 Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M18 8 L25 10 L26 17 L20 19 L17 13 Z" fill="currentColor"/><path d="M13 20 L20 21 L19 26 L13 26 Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
  aura: '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><circle cx="16" cy="16" r="10" stroke="currentColor" stroke-width="2"/><path d="M16 16 L16 8 A8 8 0 0 1 23.4 19 Z" fill="currentColor"/></svg>',
  index:
    '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><rect x="4.5" y="5" width="10" height="22" rx="3"/><rect x="17.5" y="5" width="10" height="22" rx="3"/><path d="M4.5 14 Q7 12 9.5 14 T14.5 14 M17.5 14 Q20 12 22.5 14 T27.5 14" stroke-linecap="round"/></svg>',
  fil: '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="M16 6.4 C11.6 6.4 9.4 9.2 9.4 13.2 C9.4 18.6 7.6 20.4 7.6 20.4 L24.4 20.4 C24.4 20.4 22.6 18.6 22.6 13.2 C22.6 9.2 20.4 6.4 16 6.4 Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M13.6 23.4 A2.6 2.6 0 0 0 18.4 23.4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
  partager:
    '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="M16 20 L16 7 M16 7 L11.5 11.5 M16 7 L20.5 11.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M8.5 15 L8.5 25 L23.5 25 L23.5 15" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
  reglages:
    '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="M5 11 H8.6 M15.4 11 H27 M5 21 H17.6 M24.4 21 H27" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="11" r="3.4" stroke="currentColor" stroke-width="2"/><circle cx="21" cy="21" r="3.4" stroke="currentColor" stroke-width="2"/></svg>',
  plus: '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 7.5 V24.5 M7.5 16 H24.5" stroke-linecap="round"/></svg>',
  recadrer:
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 9V5.5A1.5 1.5 0 0 1 5.5 4H9"/><path d="M15 4h3.5A1.5 1.5 0 0 1 20 5.5V9"/><path d="M20 15v3.5a1.5 1.5 0 0 1-1.5 1.5H15"/><path d="M9 20H5.5A1.5 1.5 0 0 1 4 18.5V15"/></svg>',
} as const;

/** les tracés du symbole « recadrer », pour le peindre en flaques (son image) */
export const TRACES_RECADRER = [
  'M4 9V5.5A1.5 1.5 0 0 1 5.5 4H9',
  'M15 4h3.5A1.5 1.5 0 0 1 20 5.5V9',
  'M20 15v3.5a1.5 1.5 0 0 1-1.5 1.5H15',
  'M9 20H5.5A1.5 1.5 0 0 1 4 18.5V15',
] as const;
