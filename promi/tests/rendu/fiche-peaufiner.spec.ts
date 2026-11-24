/**
 * LOT 3b-1 — PEAUFINER SUR LA FICHE : IDENTITÉ AU PIXEL (releve-S2, redteam_peaufiner, redteam_peauf_rangees, redteam_peauf_x).
 *
 * La barre « Peaufiner » touchée au doigt des deux côtés (le prototype dans la fenêtre du banc, la vraie app à 390 × 844), sur chaque fiche du
 * banc (`banc-etats/etat-fiches.json`), clair et sombre (C-132 : la même page) : la page de réglages ouverte, ses rangées (la tête et son X, LE
 * TRAIT et son aperçu, À QUI / QUI OSE ?, AVEC, AVANT, DANS UN CERCLE, NOTE, PIÈCES JOINTES, les murs, SUPPRIMER), la barre et son ▾ retourné.
 * Puis son X la referme : la fiche est revenue telle qu'elle était, au pixel. Tolérance : 2 niveaux, 0 pixel au-delà (Q616 hors du Mac).
 *
 * ÉCART NOMMÉ : la page de la vraie app paraît en flaques (C-271, comme celle de la page +) ; le prototype la posait d'un coup — la capture est
 * prise une fois arrivée.
 * EXCEPTIONS NOMMÉES, masquées des deux côtés :
 *  · C1 — les quatre COINS de l'appareil (24 × 24 pt) : Peaufiner ouvert, le prototype sort sa barre (#dpDetails, posée en absolu à 760 par
 *         lot-S2) du masque arrondi de son appareil — ses coins bas deviennent carrés, et le bord de ses coins hauts change ; la vraie app garde ses
 *         coins, comme l'écran arrondi de l'iPhone. Un accident du banc du prototype, pas un dessin ;
 *  · M1 — hors du Mac seulement (comme la page +) : le texte flouté des murs (4,8 px), dont la coupe dépend des métriques de police du système.
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { PNG } from 'pngjs';
import { fichesPilotees, images, ecart, sonde, stockageFiches, CAS_FICHES, PAROLE_CERCLE, type Zone } from './aides.ts';

const RES = join(import.meta.dirname, 'resultats', 'fiche-peaufiner');

/** un toucher au doigt (pointeur, puis le clic que le navigateur fabrique) au point de l'appareil (x, y), en pt */
async function toucher(pg: Page, x: number, y: number): Promise<void> {
  const r = await pg.evaluate(() => {
    const b = document.getElementById('device')!.getBoundingClientRect();
    return { x: b.left, y: b.top, k: b.width / 390 };
  });
  await pg.mouse.click(r.x + x * r.k, r.y + y * r.k);
}

async function image(pg: Page): Promise<Buffer> {
  const clip = await pg.evaluate(() => {
    const r = document.getElementById('device')!.getBoundingClientRect();
    return { x: r.left, y: r.top, width: r.width, height: r.height };
  });
  return pg.screenshot({ clip });
}

/** hors du Mac : le texte flouté des murs (au-dessus de la barre, qui reste jugée) */
const COINS: Zone[] = [
  [0, 0, 24, 24],
  [366, 0, 24, 24],
  [0, 820, 24, 24],
  [366, 820, 24, 24],
];
async function zones(A: Page): Promise<Zone[]> {
  if (process.platform === 'darwin') return COINS;
  return (await A.evaluate((coins) => {
    const z: number[][] = [];
    const C = document.getElementById('device')!.getBoundingClientRect();
    const k = C.width / 390;
    for (const m of document.querySelectorAll('#dpdCorps .s2-cercle .s2-reg')) {
      const b = m.getBoundingClientRect();
      const y0 = (b.top - C.top) / k + 6;
      const y1 = Math.min((b.bottom - C.top) / k - 6, 759);
      if (b.height && y1 > y0) z.push([(b.left - C.left) / k + 6, y0, b.width / k - 12, y1 - y0]);
    }
    return [...coins, ...z];
  }, COINS)) as Zone[];
}

function masquer(png: Buffer, Z: Zone[]): Buffer {
  const im = PNG.sync.read(png);
  const k = im.width / 390;
  for (const [x, y, w, h] of Z)
    for (let j = Math.max(0, Math.floor(y * k)); j < Math.min(im.height, Math.ceil((y + h) * k)); j++)
      for (let i = Math.max(0, Math.floor(x * k)); i < Math.min(im.width, Math.ceil((x + w) * k)); i++) {
        const q = (j * im.width + i) * 4;
        im.data[q] = 255;
        im.data[q + 1] = 0;
        im.data[q + 2] = 255;
      }
  return PNG.sync.write(im);
}

/** deux captures identiques à 40 images d'horloge d'écart, des deux côtés */
async function poses(P: Page, A: Page): Promise<{ ip: Buffer; ia: Buffer; Z: Zone[] }> {
  let ip: Buffer = Buffer.alloc(0);
  let ia: Buffer = Buffer.alloc(0);
  let Z: Zone[] = [];
  for (let k = 0; k < 20; k++) {
    await Promise.all([images(P, 40), images(A, 40)]);
    const Z2 = await zones(A);
    const ip2 = masquer(await image(P), Z2);
    const ia2 = masquer(await image(A), Z2);
    const pose = k > 1 && ip2.equals(ip) && ia2.equals(ia);
    [ip, ia, Z] = [ip2, ia2, Z2];
    if (pose) break;
  }
  return { ip, ia, Z };
}

for (const theme of ['sombre', 'clair'] as const)
  for (const [id, cas] of CAS_FICHES)
    test(`identité au pixel : Peaufiner sur la fiche — ${cas}, ${theme}`, async ({ browser }) => {
      const ls = { ...stockageFiches(id === PAROLE_CERCLE.id), promi_theme: theme === 'clair' ? 'light' : 'dark' };
      const { P, A, erreurs } = await fichesPilotees(browser, ls, id);
      try {
        // la sonde (sur « identité au pixel : Peaufiner sur la fiche — Promi en cours, à soi, sombre ») : les rangées de la vraie app 2 pt plus bas
        if (sonde('peauf-fiche-decale'))
          await A.addStyleTag({ content: '#dpdCorps .s2-liste{translate:0 2px!important}' });
        // la sonde (sur « identité au pixel : Peaufiner sur la fiche — Chiche lancé à soi, sombre ») : AVEC vide sans ses pointillés
        if (sonde('peauf-fiche-avec-plein'))
          await A.addStyleTag({ content: '#dpdCorps .s2-vide{border-style:solid!important}' });
        const avant = await poses(P, A);
        // la barre touchée au doigt (son libellé, à gauche du ▾)
        await Promise.all([toucher(P, 80, 802), toucher(A, 80, 802)]);
        await Promise.all([images(P, 60), images(A, 60)]);
        const { ip, ia, Z } = await poses(P, A);
        mkdirSync(RES, { recursive: true });
        writeFileSync(join(RES, `${theme}-${String(id)}-prototype.png`), ip);
        writeFileSync(join(RES, `${theme}-${String(id)}-app.png`), ia);
        const e = ecart(ip, ia);
        expect(erreurs).toEqual([]);
        expect(
          { n: e.n, boite: e.boite },
          `Peaufiner ouvert : pixels écartés de plus de 2 niveaux (zones exceptées ${JSON.stringify(Z)} ; bords lissés hors macOS : ${String(e.bords)})`,
        ).toEqual({ n: 0, boite: null });
        // le bas de la liste (les murs, SUPPRIMER) : la page défilée jusqu'au bout, des deux côtés
        for (const pg of [P, A])
          await pg.evaluate(() => {
            const c = document.getElementById('dpdCorps')!;
            c.scrollTop = c.scrollHeight;
          });
        await Promise.all([images(P, 30), images(A, 30)]);
        const bas = await poses(P, A);
        writeFileSync(join(RES, `${theme}-${String(id)}-bas-prototype.png`), bas.ip);
        writeFileSync(join(RES, `${theme}-${String(id)}-bas-app.png`), bas.ia);
        const eb = ecart(bas.ip, bas.ia);
        expect(
          { n: eb.n, boite: eb.boite },
          `Peaufiner défilé au bout : pixels écartés de plus de 2 niveaux (zones exceptées ${JSON.stringify(bas.Z)} ; bords lissés hors macOS : ${String(eb.bords)})`,
        ).toEqual({ n: 0, boite: null });
        for (const pg of [P, A])
          await pg.evaluate(() => {
            document.getElementById('dpdCorps')!.scrollTop = 0;
          });
        await Promise.all([images(P, 30), images(A, 30)]);
        // son X le referme : la fiche est revenue telle qu'elle était (des deux côtés)
        const x = await A.evaluate(() => {
          const D = document.getElementById('device')!.getBoundingClientRect();
          const b = document.querySelector('#dpdCorps .s2-fermer')!.getBoundingClientRect();
          const k = D.width / 390;
          return [(b.left - D.left) / k + b.width / k / 2, (b.top - D.top) / k + b.height / k / 2];
        });
        await Promise.all([toucher(P, x[0]!, x[1]!), toucher(A, x[0]!, x[1]!)]);
        await Promise.all([images(P, 60), images(A, 60)]);
        const apres = await poses(P, A);
        const ef = ecart(avant.ia, apres.ia);
        expect(
          { n: ef.n, boite: ef.boite },
          'le X referme Peaufiner seul : la fiche de la vraie app revenue au pixel',
        ).toEqual({
          n: 0,
          boite: null,
        });
        expect(
          await A.evaluate(
            () => !!document.getElementById('dpdCorps')?.hidden && !document.getElementById('detailPoster')?.hidden,
          ),
          'Peaufiner fermé, la fiche ouverte',
        ).toBe(true);
      } finally {
        await Promise.all([P.context().close(), A.context().close()]);
      }
    });
