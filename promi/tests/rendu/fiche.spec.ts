/**
 * LOT 3a-1 — LA FICHE AU REPOS : IDENTITÉ AU PIXEL (releve-S1-fiches, redteam_fiches_theme, redteam_fiches_orange, redteam_deux_etats,
 * redteam_phrase_fiche, redteam_motmarque, redteam_etat_fiche, redteam_formes, redteam_champ, redteam_contraste_trait, redteam_ronds).
 *
 * La fiche de la vraie app à 390 × 844 contre celle du prototype (son appareil dans la fenêtre du banc), le même état des deux côtés
 * (`banc-etats/etat-fiches.json` : un cas par état de fiche), même WebKit, ×3, clair et sombre (C-132 : la même fiche), échelles 1 et 0,79 :
 * Promi en cours à soi, à Marion, à cinq personnes, date passée (« EN COURS · 12 OCT. »), reçue ; tenue ; Chiche lancé à soi, à Adrien,
 * à Rachel et Marion avec une part tracée (C-115), reçu à relever (D2), tenu, tenu à deux. La fiche est ouverte par la façade de chaque côté
 * (`openDetail(id)` ; `fiche().ouvrir(id)`), les animations gelées. Tolérance : 2 niveaux, 0 pixel au-delà (Q616 hors du Mac, aides.ts `ecart`).
 *
 * EXCEPTIONS NOMMÉES (et seulement elles), masquées des deux côtés :
 *  · M1 — la MATIÈRE de la dalle (§8 bis : « zéro écart » excepte la matière) : la boîte que le peintre déclare (`data-matiere`), + 8 pt ;
 *  · M2 — le GRAIN des anneaux des Noyaux (`_grain`) : le prototype le tire au hasard à chaque chargement (`Math.random`), la vraie app d'une
 *         graine fixe ; la bande de chaque anneau est masquée, ses arcs (couleurs, parts, jour de 3 pt) jugés à part (`fiche-juges.spec.ts`).
 *  · M3 — le FONDU à droite de la rangée des Noyaux quand elle déborde (plus de trois personnes) : un dégradé en masque d'août (`.aura-band`),
 *         une dette du volume du prototype (volume-dette.json) que la vraie app ne reprend pas — sa rangée s'arrête net ; ses 46 derniers pt
 *         sont masqués, et seulement quand elle déborde.
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { PNG } from 'pngjs';
import { GEL, prototype, vraieApp, ecart, sonde, stockageFiches, CAS_FICHES } from './aides.ts';

const RES = join(import.meta.dirname, 'resultats', 'fiche');
type Zone = [number, number, number, number];

/** les zones exceptées, en pt de l'appareil : la matière (M1) et les bandes des anneaux (M2) */
async function zones(A: Page, P: Page): Promise<Zone[]> {
  const z: Zone[] = [];
  for (const [pg, sel] of [
    [A, '#detailPoster.fiche .fi-champ'],
    [P, '#dpTrameCv'],
  ] as const) {
    const m = (await pg.evaluate((sel) => {
      const cv = document.querySelector(sel);
      const v = cv?.getAttribute('data-matiere');
      if (!cv || !v) return null;
      const D = (document.getElementById('device') ?? document.getElementById('detailPoster'))!.getBoundingClientRect();
      const k = D.width / 390 || 1;
      const c = cv.getBoundingClientRect();
      const [x, y, w, h] = v.split(',').map(Number) as [number, number, number, number];
      return [(c.left - D.left) / k + x, (c.top - D.top) / k + y, w, h];
    }, sel)) as Zone | null;
    if (m) z.push([m[0] - 8, m[1] - 8, m[2] + 16, m[3] + 16]);
  }
  const anneaux = (await A.evaluate(() => {
    const D = document.getElementById('detailPoster')!.getBoundingClientRect();
    const k = D.width / 390 || 1;
    return [...document.querySelectorAll('#detailPoster.fiche canvas.kr-c')].map((c) => {
      const r = c.getBoundingClientRect();
      return [(r.left - D.left) / k, (r.top - D.top) / k, r.width / k, r.height / k];
    });
  })) as Zone[];
  // M3 : les 46 derniers pt de la rangée des Noyaux, quand elle déborde
  const fondu = (await A.evaluate(() => {
    const a = document.getElementById('dAura')!;
    if (a.scrollWidth <= a.clientWidth + 1) return null;
    const D = document.getElementById('detailPoster')!.getBoundingClientRect();
    const k = D.width / 390 || 1;
    const r = a.getBoundingClientRect();
    return [(r.right - D.left) / k - 46, (r.top - D.top) / k, 46, r.height / k];
  })) as Zone | null;
  if (fondu) z.push(fondu);
  return [...z, ...anneaux];
}

/** masque les zones (en magenta), un anneau par sa BANDE seulement (le visage dedans reste jugé) */
function masquer(png: Buffer, Z: Zone[], nAnneaux: number): Buffer {
  const im = PNG.sync.read(png);
  const k = im.width / 390;
  Z.forEach(([x, y, w, h], i) => {
    const anneau = i >= Z.length - nAnneaux;
    const cx = (x + w / 2) * k;
    const cy = (y + h / 2) * k;
    const Rx = (w / 2) * k;
    const Ri = Rx * (w === 78 ? 27 / 39 : 20 / 29);
    // un anneau : sa bande, et 3 px de part et d'autre (WebKit compose la rangée au demi-point près, différemment des deux côtés)
    const m = anneau ? 3 : 0;
    for (let j = Math.max(0, Math.floor(y * k) - m); j < Math.min(im.height, Math.ceil((y + h) * k) + m); j++)
      for (let i2 = Math.max(0, Math.floor(x * k) - m); i2 < Math.min(im.width, Math.ceil((x + w) * k) + m); i2++) {
        if (anneau) {
          const d = Math.hypot(i2 + 0.5 - cx, j + 0.5 - cy);
          if (d < Ri - 3 || d > Rx + 3) continue;
        }
        const q = (j * im.width + i2) * 4;
        im.data[q] = 255;
        im.data[q + 1] = 0;
        im.data[q + 2] = 255;
      }
  });
  return PNG.sync.write(im);
}

for (const theme of ['sombre', 'clair'] as const)
  for (const [id, cas] of CAS_FICHES)
    test(`identité au pixel : la fiche — ${cas}, ${theme}`, async ({ browser }) => {
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
        await Promise.all([prototype(P, ls), vraieApp(A, ls)]);
        await P.evaluate((id) => (window as unknown as { openDetail(i: number): void }).openDetail(id), id);
        await A.evaluate(
          (id) =>
            (window as unknown as { __promi: { fiche(): { ouvrir(i: number): void } } }).__promi.fiche().ouvrir(id),
          id,
        );
        // la sonde (sur « identité au pixel : la fiche — Promi en cours, à soi, sombre ») : le titre de la vraie app décalé d'un point
        if (sonde('fiche-identite-decale'))
          await A.addStyleTag({ content: '#detailPoster.fiche .fi-titre{translate:0 1px!important}' });
        for (const pg of [P, A]) await pg.addStyleTag({ content: GEL });
        const dv = await P.evaluate(() => {
          const r = document.getElementById('device')!.getBoundingClientRect();
          return { x: r.left, y: r.top, width: r.width, height: r.height };
        });
        // les deux côtés POSÉS : deux images identiques (matière exceptée) à 700 ms d'écart
        let Z: Zone[] = [];
        let n = 0;
        let ip: Buffer = Buffer.alloc(0);
        let ia: Buffer = Buffer.alloc(0);
        for (let k = 0; k < 25; k++) {
          await P.waitForTimeout(700);
          const Z2 = await zones(A, P);
          const n2 = await A.evaluate(() => document.querySelectorAll('#detailPoster.fiche canvas.kr-c').length);
          const ip2 = masquer(await P.screenshot({ clip: dv }), Z2, n2);
          const ia2 = masquer(await A.screenshot(), Z2, n2);
          // le X du prototype passe parfois, à l'ouverture d'une fiche tenue, par une place transitoire (sur le « P » de PROMI : la veille
          // de `lot-V157-CROIX` qui le repose) — on attend qu'il soit à SA place (x 300 ± 0,5) avant de comparer
          const xEnPlace = await P.evaluate(() => {
            const D = document.getElementById('device')!.getBoundingClientRect();
            const x = document.querySelector('#detailPoster .closeb')?.getBoundingClientRect();
            return !!x && Math.abs((x.left - D.left) / (D.width / 390) - 300) < 0.5;
          });
          const pose = k > 1 && xEnPlace && ip2.equals(ip) && ia2.equals(ia);
          [Z, n, ip, ia] = [Z2, n2, ip2, ia2];
          if (pose) break;
        }
        void n;
        mkdirSync(RES, { recursive: true });
        writeFileSync(join(RES, `${theme}-${String(id)}-prototype.png`), ip);
        writeFileSync(join(RES, `${theme}-${String(id)}-app.png`), ia);
        const e = ecart(ip, ia);
        expect(erreurs).toEqual([]);
        expect(
          { n: e.n, boite: e.boite },
          `pixels écartés de plus de 2 niveaux (zones exceptées ${JSON.stringify(Z)} ; bords lissés hors macOS : ${String(e.bords)})`,
        ).toEqual({ n: 0, boite: null });
      } finally {
        await Promise.all([P.context().close(), A.context().close()]);
      }
    });
