/**
 * LOT 4 — LA FICHE D'UNE PERSONNE, COMME LE PROTOTYPE (SPEC-ECRANS §22 ; `openPerson` de lot-FICHE-PERSONNE, lot-DALLE-PORTE, lot-V146-NOMS).
 *
 * Des deux côtés, l'état des fiches (25 paroles), l'horloge pilotée ; la fiche d'une personne ouverte (le prototype : `openPerson(nom)`), posée :
 *  · au repos — l'encart, le Noyau et sa légende, « Tenu ensemble », les cartes de l'Index — au pixel, deux thèmes ;
 *  · la personne sans parole (« Rien entre vous pour l’instant. ») ;
 *  · la porte : un nom touché dans la phrase d'une fiche ouvre sa fiche ; un nom à soi n'ouvre rien ;
 *  · « + Planter un Promi » ouvre la page + la personne déjà choisie.
 * Tolérance : 2 niveaux, 0 pixel au-delà. EXCEPTION NOMMÉE M1 : la matière de chaque dalle (la boîte déclarée d'une carte, 8 pt autour ; une dalle de
 * « Tenu ensemble », sa boîte entière).
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { deuxPilotes, fichesPilotees, images, sonde, stockageFiches, P_ } from './aides.ts';
import { juger as jugerL, poser, toucherDeux, type Liste } from './listes.ts';

const RES = join(import.meta.dirname, 'resultats', 'personne');
const L: Liste = { liste: '#psCartes', menu: '#ixMenu', res: RES, autres: '#personSheet .ps-bx' };
const juger = (P: Page, A: Page, nom: string): Promise<void> => jugerL(P, A, L, nom);

async function ouvrirPersonne(P: Page, A: Page, nom: string): Promise<void> {
  await P.evaluate((n) => (window as unknown as { openPerson: (n: string) => void }).openPerson(n), nom);
  await A.evaluate(`${P_}.personne().ouvrir(${JSON.stringify(nom)})`);
  for (let k = 0; k < 6; k++) await Promise.all([images(P, 30), images(A, 30)]);
}

/** ce que la fiche montre : le nom, les dalles tenues, les cartes (leur parole et leurs mots) */
const compo = (pg: Page): Promise<string> =>
  pg.evaluate(() =>
    JSON.stringify([
      document.getElementById('psName')?.textContent,
      [...document.querySelectorAll('#personSheet .ps-c')].map((c) => c.getAttribute('data-pid')),
      [...document.querySelectorAll('#psCartes .s4-carte')].map((c) =>
        [
          c.getAttribute('data-pid'),
          ...[...c.querySelectorAll('.s4-eb, .s4-ti, .s4-et')].map((x) => x.textContent),
        ].join('|'),
      ),
    ]),
  );

for (const theme of ['sombre', 'clair'] as const)
  for (const nom of ['Rachel', 'Marion'] as const)
    test(`la fiche d'une personne au repos, comme le prototype : ${nom}, ${theme}`, async ({ browser }) => {
      const ls = { ...stockageFiches(), promi_prenom: 'Tom', promi_theme: theme === 'clair' ? 'light' : 'dark' };
      const { P, A, erreurs } = await deuxPilotes(browser, ls);
      try {
        mkdirSync(RES, { recursive: true });
        // la sonde (sur « Rachel, sombre ») : l'état écrit de nouveau sous les cartes (« TENUE », « EN COURS »)
        if (sonde('personne-etat-ecrit'))
          await A.addStyleTag({ content: '#psCartes .s4-et::before{content:"EN COURS"}' });
        await ouvrirPersonne(P, A, nom);
        expect(await compo(A)).toBe(await compo(P));
        await juger(P, A, `${nom}-${theme}`);
        expect(erreurs).toEqual([]);
      } finally {
        await Promise.all([P.context().close(), A.context().close()]);
      }
    });

test('une personne sans parole : « Rien entre vous pour l’instant. », les deux boutons restent (E4, v178c)', async ({
  browser,
}) => {
  const { P, A, erreurs } = await deuxPilotes(browser, { ...stockageFiches(), promi_prenom: 'Tom' });
  try {
    mkdirSync(RES, { recursive: true });
    await ouvrirPersonne(P, A, 'Zoé');
    expect(await A.evaluate(() => document.querySelector('#personSheet .e4-ps')?.textContent)).toBe(
      'Rien entre vous pour l’instant.',
    );
    await juger(P, A, 'sans-parole');
    expect(erreurs).toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});

test("un nom touché dans la phrase d'une fiche ouvre la fiche de sa personne ; « + Planter un Promi » ouvre la page + la personne choisie", async ({
  browser,
}) => {
  // « préparer le voyage », à Rachel (166)
  const { P, A, erreurs } = await fichesPilotees(browser, { ...stockageFiches(), promi_prenom: 'Tom' }, 166);
  try {
    mkdirSync(RES, { recursive: true });
    // la sonde : un nom touché n'ouvre plus rien
    if (sonde('nom-sourd'))
      await A.evaluate(() => {
        document.addEventListener(
          'pointerdown',
          (ev) => {
            if ((ev.target as Element | null)?.closest('.nom-lien')) ev.stopImmediatePropagation();
          },
          true,
        );
        window.addEventListener('pointerdown', (ev) => ev.stopImmediatePropagation(), true);
      });
    await toucherDeux(P, A, '#detailPoster .nom-lien[data-nom="Rachel"]');
    for (let k = 0; k < 6; k++) await Promise.all([images(P, 30), images(A, 30)]);
    const ouverte = (pg: Page): Promise<string> =>
      pg.evaluate(() => {
        const s = document.getElementById('personSheet');
        const vu = !!s && getComputedStyle(s).display !== 'none' && s.getBoundingClientRect().top < 50;
        return vu ? (document.getElementById('psName')?.textContent ?? '') : '';
      });
    expect(await ouverte(A), 'la fiche de Rachel').toBe('Rachel');
    expect(await ouverte(P), 'le prototype aussi').toBe('Rachel');
    await juger(P, A, 'depuis-la-fiche');
    // « + Planter un Promi » : la page + d'un Promi, Rachel déjà choisie
    await toucherDeux(P, A, '#personSheet .ps-bt[data-geste="promi"]');
    await poser(P, A, 10);
    const phrase = (pg: Page): Promise<string> =>
      pg.evaluate(() =>
        (document.querySelector('#createSheet .ph-txt, #csPhrase, #createSheet .cs-phrase')?.textContent ?? '')
          .replace(/\s+/g, ' ')
          .trim(),
      );
    expect(await phrase(A), 'la phrase de la page +').toMatch(/^Je promets .*à\s*Rachel$/);
    expect(await phrase(P)).toMatch(/^Je promets .*à\s*Rachel$/);
    expect(erreurs).toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});
