/**
 * LOT 5 — LA FICHE D'UN CERCLE AU REPOS : IDENTITÉ AU PIXEL (SPEC-ECRANS §7 ; redteam_nuee, redteam_cercle_dalles, redteam_cercle_tom).
 *
 * Des deux côtés, l'état des fiches et ses deux Cercles (`stockageCercles` : « Marseille », cinq paroles, Rachel et Marion ; « Atelier », vide), même
 * WebKit, ×3, l'horloge pilotée ; la fiche du Cercle ouverte par la façade (`openNueeDetail(k)` ; `fiche().ouvrirCercle(k)`), posée : le plateau,
 * la bande et la vague, les Noyaux (« Toi », le Cercle), le « + » des membres, « Avec … », le nom, la ligne d'état, le fil (ses lignes, leurs traits),
 * « Un mot… », « Planter dans le Cercle », la barre Peaufiner — clair et sombre (C-132 : la même fiche). Tolérance : 2 niveaux, 0 pixel au-delà.
 *
 * EXCEPTIONS NOMMÉES, masquées des deux côtés :
 *  · M1 — la MATIÈRE (§8 bis) : la bande entière (le peintre déclare le champ, Q74) et la mini-dalle de chaque ligne du fil (+ 8 pt) ;
 *  · M2 — le GRAIN des anneaux (le prototype le tire au hasard ; fiche.spec.ts).
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { deuxPilotes, images, ecart, sonde, stockageCercles, masquerFiche, type Zone, P_ } from './aides.ts';

const RES = join(import.meta.dirname, 'resultats', 'cercle');

/** les zones exceptées, en pt de l'appareil : la bande (M1), les mini-dalles du fil (M1), les anneaux (M2, en dernier) */
async function zones(A: Page, P: Page): Promise<{ Z: Zone[]; n: number }> {
  const z: Zone[] = [];
  for (const pg of [A, P])
    z.push(
      ...((await pg.evaluate(() => {
        const D = document.getElementById('device')!.getBoundingClientRect();
        const k = D.width / 390 || 1;
        const out: number[][] = [];
        const cv = document.getElementById('dpTrameCv');
        const v = cv?.getAttribute('data-matiere');
        if (cv && v) {
          const c = cv.getBoundingClientRect();
          const [x, y, w, h] = v.split(',').map(Number) as [number, number, number, number];
          out.push([(c.left - D.left) / k + x - 8, (c.top - D.top) / k + y - 8, w + 16, h + 16]);
        }
        for (const d of document.querySelectorAll('#detailPoster .nf-d')) {
          const r = d.getBoundingClientRect();
          out.push([(r.left - D.left) / k - 8, (r.top - D.top) / k - 8, r.width / k + 16, r.height / k + 16]);
        }
        return out;
      })) as Zone[]),
    );
  const anneaux = (await A.evaluate(() => {
    const D = document.getElementById('detailPoster')!.getBoundingClientRect();
    const k = D.width / 390 || 1;
    return [...document.querySelectorAll('#detailPoster.fiche canvas.kr-c')].map((c) => {
      const r = c.getBoundingClientRect();
      return [(r.left - D.left) / k, (r.top - D.top) / k, r.width / k, r.height / k];
    });
  })) as Zone[];
  return { Z: [...z, ...anneaux], n: anneaux.length };
}

/** ce que la fiche montre : le mot du plateau, « Avec … », le nom, la ligne d'état, les lignes du fil (leur mot, leur titre) */
const compo = (pg: Page): Promise<string> =>
  pg.evaluate(() =>
    JSON.stringify([
      ...['#dptNat', '#dptQui', '#dptTitre', '#dptQuand'].map((s) => document.querySelector(s)?.textContent?.trim()),
      [...document.querySelectorAll('#dpNueeFil .nf-item')].map(
        (c) => c.querySelector('em')?.textContent + '|' + c.querySelector('b')?.textContent,
      ),
    ]),
  );

for (const theme of ['sombre', 'clair'] as const)
  for (const k of ['n1', 'n2'] as const)
    test(`identité au pixel : la fiche d'un Cercle — ${k === 'n1' ? 'cinq paroles' : 'vide'}, ${theme}`, async ({
      browser,
    }) => {
      const ls = { ...stockageCercles(), promi_prenom: 'Tom', promi_theme: theme === 'clair' ? 'light' : 'dark' };
      const { P, A, erreurs } = await deuxPilotes(browser, ls);
      try {
        // la sonde (sur « … cinq paroles, sombre ») : le fil du Cercle 4 pt plus bas
        if (sonde('cercle-fil-decale')) await A.addStyleTag({ content: '#detailPoster .fi-fil{translate:0 4px}' });
        await P.evaluate((k) => (window as unknown as { openNueeDetail(k: string): void }).openNueeDetail(k), k);
        await A.evaluate(`${P_}.fiche().ouvrirCercle(${JSON.stringify(k)})`);
        const dv = await P.evaluate(() => {
          const r = document.getElementById('device')!.getBoundingClientRect();
          return { x: r.left, y: r.top, width: r.width, height: r.height };
        });
        let ip: Buffer = Buffer.alloc(0);
        let ia: Buffer = Buffer.alloc(0);
        let Z: Zone[] = [];
        for (let i = 0; i < 20; i++) {
          await Promise.all([images(P, 40), images(A, 40)]);
          const { Z: Z2, n } = await zones(A, P);
          const ip2 = masquerFiche(await P.screenshot({ clip: dv }), Z2, n);
          const ia2 = masquerFiche(await A.screenshot(), Z2, n);
          const pose = i > 1 && ip2.equals(ip) && ia2.equals(ia);
          [Z, ip, ia] = [Z2, ip2, ia2];
          if (pose) break;
        }
        expect(await compo(A)).toBe(await compo(P));
        mkdirSync(RES, { recursive: true });
        writeFileSync(join(RES, `${k}-${theme}-prototype.png`), ip);
        writeFileSync(join(RES, `${k}-${theme}-app.png`), ia);
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
