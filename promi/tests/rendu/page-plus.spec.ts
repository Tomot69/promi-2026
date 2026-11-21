/**
 * LOT 2a — LA PAGE + : IDENTITÉ AU PIXEL (releve-S3-page-plus, redteam_pages_plus).
 *
 * La page + de la vraie app à 390 × 844 contre celle du prototype (son appareil dans la fenêtre du banc), même état importé des deux côtés
 * (`stockage()` : les exemples tirés d'avance, les personnes connues), même WebKit, ×3, clair et sombre : Promi, Chiche, Cercle au repos, et
 * le choix des personnes ouvert (« qui ose ? » d'un Chiche). La Toile dessous est masquée, les animations gelées. Tolérance : 2 niveaux, 0
 * pixel au-delà (Q616 hors du Mac, aides.ts `ecart`).
 *
 * EXCEPTIONS NOMMÉES (et seulement elles), déclarées et masquées DES DEUX CÔTÉS :
 *  · M1 — la MATIÈRE de la dalle du haut (§8 bis : « zéro écart » excepte la matière) : la zone que le peintre déclare (`data-matiere`) ;
 *  · P1 — le petit carré noir que le prototype peint à gauche du rail du pinceau (12,7 × 25,7 pt, « sans aucun élément dessous », déjà noté en
 *         v174a) : un défaut du prototype, que la vraie app ne reproduit pas ;
 *  · P2 — le flou du premier pinceau de Ma Parole ! au bord droit (x ≥ 366, la rangée du rail) : dans le prototype WebKit le coupe au bord de la
 *         couche qui défile, la vraie app le laisse entier (le même `filter: blur(4.8px)`, C-196) ;
 *  · P3 — NON EXPLIQUÉ, MESURÉ : un pixel du pointillé de l'exemple d'un Chiche, à (238,3 ; 514), 27 niveaux (les boîtes des deux côtés sont les
 *         mêmes au centième de point) : écrit « non tenu » au rapport du lot 2a, à reprendre.
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { PNG } from 'pngjs';
import { ETAT, stockage, GEL, prototype, vraieApp, ouvrirPagePlus, ecart, sonde } from './aides.ts';

const RES = join(import.meta.dirname, 'resultats', 'page-plus');

type Zone = [number, number, number, number];

/** les zones exceptées, lues sur la vraie app (en pt) : la matière déclarée, le carré P1, le bord P2 */
async function zones(A: Page): Promise<Zone[]> {
  return (await A.evaluate(() => {
    const z: number[][] = [];
    const cv = document.getElementById('csTrameCv');
    const m = cv?.getAttribute('data-matiere');
    const C = document.getElementById('createSheet')!.getBoundingClientRect();
    if (m && cv) {
      const [x, y, w, h] = m.split(',').map(Number) as [number, number, number, number];
      const top = cv.getBoundingClientRect().top - C.top;
      z.push([x - 2, top + y - 2, w + 4, h + 4]);
    }
    const r = document.getElementById('csPinceau');
    if (r && !r.hidden) {
      const t = r.getBoundingClientRect().top - C.top;
      z.push([0, t - 14, 14, 28]);
      z.push([366, t - 6, 24, 56]);
    }
    if (document.getElementById('createSheet')!.classList.contains('pp-chiche')) z.push([237.5, 513.5, 1.5, 1.5]);
    return z;
  })) as Zone[];
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

/** un toucher sur la place « qui » (au doigt, WebKit ne fabrique pas toujours de `click` — le prototype écoute `click`, la vraie app le geste) */
async function touchePlace(p: Page, sel: string, proto: boolean): Promise<void> {
  await p.evaluate(
    ([s, proto]) => {
      const e = document.querySelector<HTMLElement>(s as string)!;
      const r = e.getBoundingClientRect();
      const o = { bubbles: true, clientX: r.left + r.width / 2, clientY: r.top + r.height / 2, pointerId: 21 };
      e.dispatchEvent(new PointerEvent('pointerdown', o));
      e.dispatchEvent(new PointerEvent('pointerup', o));
      // le prototype ouvre le choix au `click` ; la place passe à « moi » à l'appui (C-304, `lot-V199-MOI`)
      if (proto) e.click();
    },
    [sel, proto] as const,
  );
  if (proto)
    // C-304 : dans le prototype, la place passe à « moi » par une transition (détracé puis tracé, C-271) : on attend qu'elle soit finie
    await p.waitForFunction(
      (s) => {
        const e = document.querySelector(s);
        const w = window as unknown as { TraceLettres?: { actif(): boolean } };
        return !!e && (e.textContent ?? '').trim() === 'moi' && !w.TraceLettres?.actif();
      },
      sel,
      { timeout: 30000 },
    );
  await p.waitForTimeout(proto ? 1500 : 600);
}

const CAS = [
  { nat: 'promi', choix: null },
  { nat: 'chiche', choix: null },
  { nat: 'nuee', choix: null },
  { nat: 'chiche', choix: '#csPhrase .ph-m[data-ph="qui"]' },
] as const;

for (const theme of ['sombre', 'clair'] as const)
  for (const c of CAS)
    test(`identité au pixel : la page + ${c.nat}${c.choix ? ', le choix des personnes ouvert' : ''}, ${theme}`, async ({
      browser,
    }) => {
      const ls = { ...stockage(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
      const P = await (
        await browser.newContext({ viewport: { width: 430, height: 932 }, deviceScaleFactor: 3 })
      ).newPage();
      const A = await (
        await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3 })
      ).newPage();
      const erreurs: string[] = [];
      A.on('pageerror', (e) => erreurs.push(String(e)));
      await Promise.all([prototype(P, ls), vraieApp(A, ls)]);
      await Promise.all([ouvrirPagePlus(P, c.nat, true), ouvrirPagePlus(A, c.nat)]);
      if (c.choix) await Promise.all([touchePlace(P, c.choix, true), touchePlace(A, c.choix, false)]);
      for (const pg of [P, A]) await pg.addStyleTag({ content: GEL });
      // la sonde : la phrase de la vraie app décalée d'un point
      if (sonde('pp-identite-decale')) await A.addStyleTag({ content: '#createSheet .pp-phrase{translate:1px 0}' });
      await P.waitForTimeout(600);
      const Z = await zones(A);
      const dv = await P.evaluate(() => {
        const r = document.getElementById('device')!.getBoundingClientRect();
        return { x: r.left, y: r.top, width: r.width, height: r.height };
      });
      const ip = masquer(await P.screenshot({ clip: dv }), Z);
      const ia = masquer(await A.screenshot(), Z);
      mkdirSync(RES, { recursive: true });
      const nom = `${theme}-${c.nat}${c.choix ? '-choix' : ''}`;
      writeFileSync(join(RES, `${nom}-prototype.png`), ip);
      writeFileSync(join(RES, `${nom}-app.png`), ia);
      const e = ecart(ip, ia);
      expect(erreurs).toEqual([]);
      expect(
        { n: e.n, boite: e.boite },
        `pixels écartés de plus de 2 niveaux (état : ${ETAT} ; zones exceptées ${JSON.stringify(Z)} ; bords lissés hors macOS : ${String(e.bords)})`,
      ).toEqual({ n: 0, boite: null });
    });
