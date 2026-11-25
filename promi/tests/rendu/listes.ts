/**
 * LOT 4 — LES OUTILS DES JUGES DE L'INDEX ET DU FIL (une liste : sa grille de cartes ou de bandeaux, son menu ⇅) : l'image de l'appareil, la matière
 * de chaque dalle masquée (EXCEPTION NOMMÉE M1 : sa boîte déclarée `data-matiere`, 8 pt autour — elle respire, §8 bis — bornée à la liste et sous
 * le panneau du menu ouvert), le jugement au pixel une fois la page posée, le toucher au même point des deux côtés.
 */
import { expect, type Page } from '@playwright/test';
import { writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { PNG } from 'pngjs';
import { images, ecart, type Zone } from './aides.ts';

/** une liste : sa grille (`#indexList`, `#feedList`) et son menu (`#ixMenu`, `#fdMenu`) ; où ranger les images */
export interface Liste {
  liste: string;
  menu: string;
  res: string;
  /** la marge de M1 autour de la boîte déclarée (8 pt ; le bandeau du Fil : 0 — sa dalle est rendue pour tenir dans sa boîte, et 8 pt couvriraient
   *  son trait vertical) */
  marge?: number;
  /** d'autres matières, masquées dans leur boîte entière (la fiche d'une personne : les dalles de « Tenu ensemble », `.ps-bx`) */
  autres?: string;
}

export async function image(pg: Page): Promise<Buffer> {
  const clip = await pg.evaluate(() => {
    const r = document.getElementById('device')!.getBoundingClientRect();
    return { x: r.left, y: r.top, width: r.width, height: r.height };
  });
  return pg.screenshot({ clip });
}

/** M1 : la matière de chaque carte (sa boîte déclarée), en pt de l'appareil */
export async function matieres(pg: Page, L: Liste): Promise<Zone[]> {
  return (await pg.evaluate(
    ([liste, menu, m0, L2]) => {
      const m = Number(m0);
      const D = document.getElementById('device')!.getBoundingClientRect();
      const k = D.width / 390;
      const z: number[][] = [];
      // bornée à la liste : une carte sortie par le haut ne masque pas l'encart ; et sous le menu ⇅ ouvert : une dalle qu'il couvre ne masque pas
      // le panneau
      const R = document.querySelector(liste!)?.getBoundingClientRect();
      const M = document.querySelector(`${menu!}.on .ix-menu-p`);
      const haut = Math.max(R ? (R.top - D.top) / k : 0, M ? (M.getBoundingClientRect().bottom - D.top) / k : 0);
      for (const cv of document.querySelectorAll(`${liste!} .s4-carte > canvas`)) {
        const v = cv.getAttribute('data-matiere');
        if (!v) continue;
        const c = cv.getBoundingClientRect();
        const [x, y, w, h] = v.split(',').map(Number) as [number, number, number, number];
        const y0 = Math.max(haut, (c.top - D.top) / k + y - m);
        const y1 = (c.top - D.top) / k + y + h + m;
        if (y1 > y0) z.push([(c.left - D.left) / k + x - m, y0, w + 2 * m, y1 - y0]);
      }
      for (const b of L2 ? document.querySelectorAll(L2) : []) {
        const c = b.getBoundingClientRect();
        z.push([(c.left - D.left) / k, (c.top - D.top) / k, c.width / k, c.height / k]);
      }
      return z;
    },
    [L.liste, L.menu, String(L.marge ?? 8), L.autres ?? ''],
  )) as Zone[];
}

export function masquer(png: Buffer, Z: Zone[]): Buffer {
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

/** au pixel, hors matière (M1), la page posée (deux relevés identiques des deux côtés) */
export async function juger(P: Page, A: Page, L: Liste, nom: string): Promise<void> {
  let ip: Buffer = Buffer.alloc(0);
  let ia: Buffer = Buffer.alloc(0);
  for (let k = 0; k < 20; k++) {
    await Promise.all([images(P, 40), images(A, 40)]);
    const Z = [...(await matieres(P, L)), ...(await matieres(A, L))];
    const p2 = masquer(await image(P), Z);
    const a2 = masquer(await image(A), Z);
    const pose = k > 1 && p2.equals(ip) && a2.equals(ia);
    [ip, ia] = [p2, a2];
    if (pose) break;
  }
  writeFileSync(join(L.res, `${nom}-prototype.png`), ip);
  writeFileSync(join(L.res, `${nom}-app.png`), ia);
  const e = ecart(ip, ia);
  expect(
    { n: e.n, boite: e.boite },
    `${nom} : pixels écartés de plus de 2 niveaux (bords lissés hors macOS : ${String(e.bords)})`,
  ).toEqual({ n: 0, boite: null });
}

/** le centre d'un élément, en pt de l'appareil */
export async function centre(pg: Page, sel: string): Promise<[number, number]> {
  return (await pg.evaluate((sel) => {
    const D = document.getElementById('device')!.getBoundingClientRect();
    const k = D.width / 390;
    const r = document.querySelector(sel)!.getBoundingClientRect();
    return [(r.left + r.width / 2 - D.left) / k, (r.top + r.height / 2 - D.top) / k];
  }, sel)) as [number, number];
}
export async function toucher(pg: Page, x: number, y: number): Promise<void> {
  const r = await pg.evaluate(() => {
    const b = document.getElementById('device')!.getBoundingClientRect();
    return { x: b.left, y: b.top, k: b.width / 390 };
  });
  await pg.mouse.click(r.x + x * r.k, r.y + y * r.k);
}
/** un toucher au même point des deux côtés (celui de la vraie app), puis la page avancée */
export async function toucherDeux(P: Page, A: Page, sel: string): Promise<void> {
  const [x, y] = await centre(A, sel);
  await Promise.all([toucher(P, x, y), toucher(A, x, y)]);
  for (let k = 0; k < 3; k++) await Promise.all([images(P, 30), images(A, 30)]);
}
/** la page avancée par tranches : les passes du prototype partent d'observateurs et de minuteurs, qui ne tournent qu'entre deux tâches */
export async function poser(P: Page, A: Page, n = 6): Promise<void> {
  for (let k = 0; k < n; k++) await Promise.all([images(P, 30), images(A, 30)]);
}
