/**
 * LOT 4 — LE FIL, COMME LE PROTOTYPE (SPEC-ECRANS §9 ; `buildFeed`, `_s4Fil` de lot-S4, C-301, C-147, C-191, C-245).
 *
 * Des deux côtés, l'état des fiches (25 paroles, 29 événements) : le prototype dans la fenêtre du banc, la vraie app à 390 × 844, l'horloge
 * pilotée ; le Fil ouvert (le prototype par son bouton de la barre), puis posé :
 *  · l'écran au repos — l'encart et son compte, la recherche, le ⇅, les premiers bandeaux — au pixel ;
 *  · défilé au bout — les derniers bandeaux — au pixel ;
 *  · l'ordre des bandeaux, leurs mots (l'événement, le titre, l'état et l'heure).
 * Sombre et clair. Tolérance : 2 niveaux, 0 pixel au-delà. EXCEPTION NOMMÉE : M1, la matière de chaque dalle (listes.ts) — ici sa boîte seule,
 * sans marge : la dalle d'un bandeau est rendue pour y tenir, et le trait vertical reste jugé.
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { deuxPilotes, sonde, stockageFiches, P_ } from './aides.ts';
import { juger as jugerL, poser, type Liste } from './listes.ts';

const RES = join(import.meta.dirname, 'resultats', 'fil');
const L: Liste = { liste: '#feedList', menu: '#fdMenu', res: RES, marge: 0 };
const juger = (P: Page, A: Page, nom: string): Promise<void> => jugerL(P, A, L, nom);

/** les bandeaux : l'événement, le titre, l'état */
async function bandeaux(pg: Page): Promise<string[]> {
  return pg.evaluate(() =>
    [...document.querySelectorAll('#feedList .s4-carte')].map((c) =>
      [
        c.getAttribute('data-pid'),
        c.querySelector('.s4-ev')?.textContent,
        c.querySelector('.s4-ti')?.textContent,
        c.querySelector('.s4-et')?.textContent,
      ].join(' | '),
    ),
  );
}

/** le Fil ouvert des deux côtés, posé */
async function ouvrirFil(P: Page, A: Page): Promise<void> {
  await P.evaluate(() => (document.getElementById('filBtn') as HTMLElement).click());
  await A.evaluate(`${P_}.fil().ouvrir()`);
  await poser(P, A, 8);
}

for (const theme of ['sombre', 'clair'] as const)
  test(`le Fil au repos et défilé au bout, comme le prototype : ${theme}`, async ({ browser }) => {
    const ls = { ...stockageFiches(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
    const { P, A, erreurs } = await deuxPilotes(browser, ls);
    try {
      mkdirSync(RES, { recursive: true });
      // la sonde (sur « … sombre ») : le bandeau d'une parole tenue garde le corps de sa nature (au lieu de la terre de la fiche, C-147)
      if (sonde('fil-tenu-sans-terre'))
        await A.addStyleTag({ content: '#feedList .s4-carte[data-pid="164"]{background:#0E78F2!important}' });
      await ouvrirFil(P, A);
      expect(await bandeaux(A), 'les bandeaux, leurs mots').toEqual(await bandeaux(P));
      expect(await A.evaluate(() => document.getElementById('fdCount')?.textContent), 'le compte').toBe(
        await P.evaluate(() => document.getElementById('fdCount')?.textContent),
      );
      await juger(P, A, `${theme}-repos`);
      // au milieu : les bandeaux d'un événement venu de quelqu'un (« lire le roman », de Nico ; « envoyer la carte », de Marion) — leur visage
      for (const pg of [P, A])
        await pg.evaluate(() => {
          const l = document.getElementById('feedList')!;
          l.scrollTop = (l.querySelector('.s4-carte[data-pid="160"]') as HTMLElement).offsetTop - 10;
        });
      expect(
        await A.evaluate(() => document.querySelectorAll('#feedList .s4-vis').length),
        'des visages',
      ).toBeGreaterThan(0);
      await juger(P, A, `${theme}-milieu`);
      for (const pg of [P, A])
        await pg.evaluate(() => {
          const l = document.getElementById('feedList')!;
          l.scrollTop = l.scrollHeight;
        });
      await juger(P, A, `${theme}-bout`);
      expect(erreurs).toEqual([]);
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  });
