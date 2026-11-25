/**
 * LOT 3b-7 — LE TRAIT D'UNE FICHE, CHOISI DEPUIS PEAUFINER (lot-PINCEAU, lot-PINCEAU-PEAUFINER, lot-V163B-PINCEAU ; Q128, C-196).
 *
 * Des deux côtés, la même fiche (le prototype dans la fenêtre du banc, la vraie app à 390 × 844, l'horloge pilotée) :
 *  · la barre « Peaufiner » touchée, puis la rangée LE TRAIT : son rail déplié (douze pastilles, les huit de Ma Parole ! en murs flous) — au pixel ;
 *  · un pinceau touché dans le rail : le choix écrit sur la parole, le rail repeint — au pixel ;
 *  · Peaufiner refermé par son X : la fiche, son trait dans la matière du pinceau (la moitié plantée, la moitié tracée, la crête, les parts) —
 *    au pixel.
 * Sombre et clair. Tolérance : 2 niveaux, 0 pixel au-delà. EXCEPTIONS NOMMÉES : C1, les coins de l'appareil Peaufiner ouvert (fiche-peaufiner
 * .spec) ; N1, après le choix, le champ de la NOTE (le prototype repose sa marge par une mesure, à 0,7 pt près selon l'instant) ; celles de la
 * fiche (M1 la matière de la dalle, M2, M3 : `zonesFiche`).
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { PNG } from 'pngjs';
import {
  fichesPilotees,
  images,
  ecart,
  sonde,
  stockageFiches,
  zonesFiche,
  masquerFiche,
  P_,
  type Zone,
} from './aides.ts';

const RES = join(import.meta.dirname, 'resultats', 'fiche-pinceau');
const COINS: Zone[] = [
  [0, 0, 24, 24],
  [366, 0, 24, 24],
  [0, 820, 24, 24],
  [366, 820, 24, 24],
];

async function toucher(pg: Page, x: number, y: number): Promise<void> {
  const r = await pg.evaluate(() => {
    const b = document.getElementById('device')!.getBoundingClientRect();
    return { x: b.left, y: b.top, k: b.width / 390 };
  });
  await pg.mouse.click(r.x + x * r.k, r.y + y * r.k);
}
/** le centre de `sel` (en pt de l'écran 390), l'élément amené dans son rail s'il glisse */
async function centre(pg: Page, sel: string, gauche = false): Promise<[number, number]> {
  return (await pg.evaluate(
    ([sel, gauche]) => {
      const e = document.querySelector<HTMLElement>(sel as string)!;
      const gl = e.closest<HTMLElement>('.pc-glisse');
      if (gl) {
        const a = e.getBoundingClientRect();
        const b = gl.getBoundingClientRect();
        if (a.right > b.right) gl.scrollLeft += a.right - b.right;
      }
      const D = document.getElementById('device')!.getBoundingClientRect();
      const k = D.width / 390;
      const r = e.getBoundingClientRect();
      return [
        (r.left - D.left) / k + (gauche ? 30 : r.width / k / 2),
        (r.top - D.top) / k + Math.min(32, r.height / k / 2),
      ];
    },
    [sel, gauche] as const,
  )) as [number, number];
}
async function image(pg: Page): Promise<Buffer> {
  const clip = await pg.evaluate(() => {
    const r = document.getElementById('device')!.getBoundingClientRect();
    return { x: r.left, y: r.top, width: r.width, height: r.height };
  });
  return pg.screenshot({ clip });
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

/** le champ de la NOTE (en pt de l'écran 390), 2 pt de marge */
async function zoneNote(A: Page): Promise<Zone[]> {
  return (await A.evaluate(() => {
    const n = document.querySelector('#dNote');
    if (!n) return [];
    const D = document.getElementById('device')!.getBoundingClientRect();
    const k = D.width / 390;
    const b = n.getBoundingClientRect();
    return [[(b.left - D.left) / k - 2, (b.top - D.top) / k - 2, b.width / k + 4, b.height / k + 4]];
  })) as Zone[];
}

const CAS: ReadonlyArray<[number, string, string]> = [
  [144, 'Promi en cours, à soi', 'Coulé'],
  [146, 'Promi tenu, à Rachel', 'Peigné'],
  [156, 'Chiche à Rachel et Marion, une part tracée', 'Sec'],
  [167, 'Chiche tenu à deux', 'Coulé'],
];

for (const theme of ['sombre', 'clair'] as const)
  for (const [id, cas, nom] of CAS)
    test(`le trait choisi depuis Peaufiner, comme le prototype : ${cas}, ${nom}, ${theme}`, async ({ browser }) => {
      const ls = { ...stockageFiches(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
      const { P, A, erreurs } = await fichesPilotees(browser, ls, id);
      try {
        // la sonde (sur « … Chiche à Rachel et Marion, une part tracée, Sec, clair ») : les pinceaux de Ma Parole ! nets, sans leur mur
        if (sonde('rail-sans-mur')) await A.addStyleTag({ content: '#dpdCorps .pc-t.pc-mur{filter:none!important}' });
        for (const pg of [P, A])
          await pg.addStyleTag({ content: '#device input,#device textarea{caret-color:transparent!important}' });
        mkdirSync(RES, { recursive: true });
        const juge = async (quoi: string, peauf: boolean): Promise<void> => {
          let ip: Buffer = Buffer.alloc(0);
          let ia: Buffer = Buffer.alloc(0);
          for (let k = 0; k < 20; k++) {
            await Promise.all([images(P, 40), images(A, 40)]);
            let p2: Buffer;
            let a2: Buffer;
            if (peauf) {
              // N1 (« choisi » seulement) : le champ de la NOTE — après un choix, le prototype rebâtit Peaufiner et repose la marge de ce champ par
              // une mesure (15,6 ou 16,3 pt selon l'instant : son texte d'exemple monte ou descend de 0,7 pt) ; la vraie app la tient à 15,6
              const Z = quoi === 'choisi' ? [...COINS, ...(await zoneNote(A))] : COINS;
              p2 = masquer(await image(P), Z);
              a2 = masquer(await image(A), Z);
            } else {
              const Z = await zonesFiche(A, P);
              const n = await A.evaluate(() => document.querySelectorAll('#detailPoster.fiche canvas.kr-c').length);
              p2 = masquerFiche(await image(P), Z, n);
              a2 = masquerFiche(await image(A), Z, n);
            }
            const pose = k > 1 && p2.equals(ip) && a2.equals(ia);
            [ip, ia] = [p2, a2];
            if (pose) break;
          }
          writeFileSync(join(RES, `${theme}-${String(id)}-${quoi}-prototype.png`), ip);
          writeFileSync(join(RES, `${theme}-${String(id)}-${quoi}-app.png`), ia);
          const e = ecart(ip, ia);
          expect(
            { n: e.n, boite: e.boite },
            `${quoi} : pixels écartés de plus de 2 niveaux (bords lissés hors macOS : ${String(e.bords)})`,
          ).toEqual({ n: 0, boite: null });
        };
        // Peaufiner, puis la rangée LE TRAIT : le rail déplié
        await Promise.all([toucher(P, 80, 802), toucher(A, 80, 802)]);
        await Promise.all([images(P, 60), images(A, 60)]);
        const [rx, ry] = await centre(A, '#dpdCorps .s2-reg.s2-trait', true);
        await Promise.all([toucher(P, rx, ry), toucher(A, rx, ry)]);
        await Promise.all([images(P, 60), images(A, 60)]);
        expect(await A.evaluate(() => document.querySelectorAll('#dpdCorps .pc-t').length), 'les douze pinceaux').toBe(
          12,
        );
        await juge('rail', true);
        // le rail glissé au bout : les pinceaux de Ma Parole !, des murs flous
        await P.evaluate(() => {
          const g = document.querySelector<HTMLElement>('#dpTraitReg .pc-glisse')!;
          g.scrollLeft = g.scrollWidth;
        });
        await A.evaluate(() => {
          const g = document.querySelector<HTMLElement>('#dpdCorps .pc-glisse')!;
          g.scrollLeft = g.scrollWidth;
        });
        await juge('rail-fin', true);
        for (const [pg, sel] of [
          [P, '#dpTraitReg .pc-glisse'],
          [A, '#dpdCorps .pc-glisse'],
        ] as const)
          await pg.evaluate((sel) => {
            document.querySelector<HTMLElement>(sel)!.scrollLeft = 0;
          }, sel);
        // un pinceau touché : le choix écrit, le rail repeint
        const sel = `.pc-t[data-t="${nom}"]`;
        const cp = await centre(P, `#dpTraitReg ${sel}`);
        const ca = await centre(A, `#dpdCorps ${sel}`);
        await Promise.all([toucher(P, cp[0], cp[1]), toucher(A, ca[0], ca[1])]);
        await Promise.all([images(P, 60), images(A, 60)]);
        expect(
          await P.evaluate(`promises.find(q => q.id === ${String(id)}).trait`),
          'le prototype a pris le pinceau',
        ).toBe(nom);
        expect(
          await A.evaluate(`${P_}.magasin.etat().paroles.find(q => q.id === ${String(id)}).suite.trait`),
          'le pinceau écrit sur la parole',
        ).toBe(nom);
        // le prototype POSÉ : sa passe des plateaux (`_plateauPartout`, qui porte le plancher des textes, §6) suit chaque toucher par des minuteurs
        // fusionnés au temps réel — sous l'horloge pilotée elle tombe tantôt avant, tantôt après la capture (ses libellés à 11,5 ou à 13 pt) : on
        // la passe une fois, comme elle le fait d'elle-même
        await P.evaluate(() => {
          (window as unknown as { _plateauPartout?: () => void })._plateauPartout?.();
        });
        await juge('choisi', true);
        // la sonde (sur « le trait choisi depuis Peaufiner, comme le prototype : Promi en cours, à soi, Coulé, sombre ») : la vraie app reprend le
        // trait plein juste avant la fermeture — la fiche doit le montrer
        if (sonde('trait-sans-matiere'))
          await A.evaluate(`${P_}.magasin.peaufiner(${String(id)}, { trait: 'Plein' }, Date.now())`);
        // Peaufiner refermé par son X : la fiche, son trait dans la matière choisie
        const [xx, xy] = await centre(A, '#dpdCorps .s2-fermer');
        await Promise.all([toucher(P, xx, xy), toucher(A, xx, xy)]);
        await Promise.all([images(P, 80), images(A, 80)]);
        await juge('fiche', false);
        expect(erreurs).toEqual([]);
      } finally {
        await Promise.all([P.context().close(), A.context().close()]);
      }
    });
