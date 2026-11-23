/**
 * LOT 3a-2 — TENIR : IDENTITÉ AU PIXEL DE L'INSTANT (releve-S5-instant, redteam_tenir, redteam_centre_validation, redteam_celebration_fixe en
 * partie). Le même geste, tracé au doigt des deux côtés (de x 150 à x 360, 700 ms, sur la vague), puis :
 *  · « le trait se referme », 1,2 s après le lever — le rideau est posé jusqu'à la barre (son front est sous elle) : le champ de la nature, la dalle de
 *    l'instant (180 × 150), le trait amande qui EST le haut du rideau, « Parole tenue ! » / « Défi relevé ! » à l'encre, centrée ;
 *  · « juste après », 3,6 s après le lever — le rideau est remonté : les Noyaux du nouvel état, la phrase en amande, le titre à 38 pt,
 *    « TENUE · À L’INSTANT » (« TENUE À DEUX » avec quelqu'un) ; la fiche reste dans cet état tant qu'elle est ouverte (le prototype).
 * Même WebKit, ×3, les deux thèmes (la fiche est la même, C-132). Exceptions : celles de fiche.spec.ts (M1 la matière, M2 le grain des anneaux).
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { AMORCE_MINUTEURS, PILOTE, T_FIGE } from './banc.ts';
import {
  GEL,
  images,
  tracerPilote,
  prototype,
  vraieApp,
  ecart,
  sonde,
  stockageFiches,
  zonesFiche,
  masquerFiche,
  appareil,
} from './aides.ts';

const RES = join(import.meta.dirname, 'resultats', 'tenir');
const CAS: ReadonlyArray<[number, string]> = [
  [144, 'Promi à soi'],
  [148, 'Promi à Marion'],
  [160, 'Promi reçu de Nico'],
  [147, 'Chiche lancé à soi'],
  [162, 'Chiche lancé à Adrien'],
  [157, 'Chiche reçu'],
];

async function image(pg: Page): Promise<Buffer> {
  return pg.screenshot({ clip: await appareil(pg) });
}

for (const theme of ['sombre', 'clair'] as const)
  for (const [id, cas] of CAS)
    test(`identité au pixel : tenir — ${cas}, ${theme}`, async ({ browser }) => {
      const ls = { ...stockageFiches(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
      const P = await (
        await browser.newContext({ viewport: { width: 430, height: 932 }, deviceScaleFactor: 3 })
      ).newPage();
      const A = await (
        await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3 })
      ).newPage();
      try {
        const erreurs: string[] = [];
        A.on('pageerror', (e) => erreurs.push(String(e)));
        await P.addInitScript((a) => new Function(a)(), AMORCE_MINUTEURS);
        await Promise.all([prototype(P, ls), vraieApp(A, ls, T_FIGE)]);
        await P.evaluate((id) => (window as unknown as { openDetail(i: number): void }).openDetail(id), id);
        await A.evaluate(
          (id) =>
            (window as unknown as { __promi: { fiche(): { ouvrir(i: number): void } } }).__promi.fiche().ouvrir(id),
          id,
        );
        // la sonde (sur « identité au pixel : tenir — Promi à soi, sombre ») : le rideau de la vraie app posé 2 pt plus bas
        if (sonde('tenir-identite-decale'))
          await A.addStyleTag({ content: '#detailPoster #tenirMaree{translate:0 2px!important}' });
        // le prototype ouvert en temps réel, puis PILOTÉ (banc_rendu) ; la vraie app pilotée depuis son départ : son ouverture, 60 images
        await P.waitForTimeout(1600);
        await P.evaluate(`(${PILOTE})()`);
        await images(A, 60);
        // les animations CSS gelées (le I de PROMI clignote) : seul le canevas du rideau bouge
        for (const pg of [P, A]) await pg.addStyleTag({ content: GEL });
        // le même geste des deux côtés, puis les deux instants comptés en images depuis le lever : 1,2 s (le rideau posé : il descend en 700 ms,
        // remonte à 2 150), puis 4,2 s (« juste après » posé, le rideau parti à 2 710 ms et la pose de la fiche finie)
        const cote = async (pg: Page): Promise<[Buffer, Buffer]> => {
          await tracerPilote(pg, 150, 360, 42);
          await images(pg, 72);
          const referme = await image(pg);
          await images(pg, 180);
          return [referme, await image(pg)];
        };
        const [[pR, pA], [aR, aA]] = await Promise.all([cote(P), cote(A)]);
        const Z = await zonesFiche(A, P);
        const n = await A.evaluate(() => document.querySelectorAll('#detailPoster.fiche canvas.kr-c').length);
        mkdirSync(RES, { recursive: true });
        const res: Record<string, { n: number; boite: number[] | null }> = {};
        for (const [nom, ip, ia, ZZ, nn] of [
          ['referme', pR, aR, Z.slice(0, Z.length - n), 0],
          ['apres', pA, aA, Z, n],
        ] as const) {
          const mp = masquerFiche(ip, [...ZZ], nn);
          const ma = masquerFiche(ia, [...ZZ], nn);
          writeFileSync(join(RES, `${theme}-${String(id)}-${nom}-prototype.png`), mp);
          writeFileSync(join(RES, `${theme}-${String(id)}-${nom}-app.png`), ma);
          const e = ecart(mp, ma);
          res[nom] = { n: e.n, boite: e.boite };
        }
        expect(erreurs).toEqual([]);
        expect(res, `pixels écartés de plus de 2 niveaux (zones exceptées ${JSON.stringify(Z)})`).toEqual({
          referme: { n: 0, boite: null },
          apres: { n: 0, boite: null },
        });
      } finally {
        await Promise.all([P.context().close(), A.context().close()]);
      }
    });
