/**
 * LOT 4 — L'INDEX, COMME LE PROTOTYPE (SPEC-ECRANS §8 ; lot-S4, lot-V210-ENCART C-301, C-147, C-151).
 *
 * Des deux côtés, l'état des fiches (25 paroles) : le prototype dans la fenêtre du banc, la vraie app à 390 × 844, l'horloge pilotée ; l'Index
 * ouvert (le prototype par son bouton de la barre), puis posé :
 *  · l'écran au repos — l'encart, la recherche, le ⇅, les trois premières rangées de cartes — au pixel ;
 *  · la grille défilée au bout — les dernières cartes — au pixel ;
 *  · l'ordre des cartes (« Récents » : la dernière action, sinon la plus récemment plantée), leurs mots, la taille de chaque titre (C-151).
 * Sombre et clair. Tolérance : 2 niveaux, 0 pixel au-delà. EXCEPTION NOMMÉE : M1, la matière de chaque dalle (sa boîte déclarée `data-matiere`,
 * 8 pt autour) — elle respire (§8 bis) ; la boîte, la place, le champ autour d'elle restent jugés.
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { PNG } from 'pngjs';
import { deuxPilotes, images, ecart, sonde, stockageFiches, P_, PAROLE_CERCLE, type Zone } from './aides.ts';

const RES = join(import.meta.dirname, 'resultats', 'index');

async function image(pg: Page): Promise<Buffer> {
  const clip = await pg.evaluate(() => {
    const r = document.getElementById('device')!.getBoundingClientRect();
    return { x: r.left, y: r.top, width: r.width, height: r.height };
  });
  return pg.screenshot({ clip });
}
/** M1 : la matière de chaque carte (sa boîte déclarée), en pt de l'appareil */
async function matieres(pg: Page): Promise<Zone[]> {
  return (await pg.evaluate(() => {
    const D = document.getElementById('device')!.getBoundingClientRect();
    const k = D.width / 390;
    const z: number[][] = [];
    // bornée à la liste : une carte sortie par le haut ne masque pas l'encart
    const L = document.getElementById('indexList')!.getBoundingClientRect();
    const haut = (L.top - D.top) / k;
    for (const cv of document.querySelectorAll('#indexList .s4-carte > canvas')) {
      const v = cv.getAttribute('data-matiere');
      if (!v) continue;
      const c = cv.getBoundingClientRect();
      const [x, y, w, h] = v.split(',').map(Number) as [number, number, number, number];
      const y0 = Math.max(haut, (c.top - D.top) / k + y - 8);
      const y1 = (c.top - D.top) / k + y + h + 8;
      if (y1 > y0) z.push([(c.left - D.left) / k + x - 8, y0, w + 16, y1 - y0]);
    }
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
/** les cartes : la parole, le titre, sa taille, le sur-titre, l'état */
async function cartes(pg: Page): Promise<string[]> {
  return pg.evaluate(() =>
    [...document.querySelectorAll('#indexList .s4-carte')].map((c) =>
      [
        c.getAttribute('data-pid'),
        c.querySelector('.s4-eb')?.textContent,
        c.querySelector('.s4-ti')?.textContent,
        getComputedStyle(c.querySelector('.s4-ti')!).fontSize,
        c.querySelector('.s4-et')?.textContent,
      ].join(' | '),
    ),
  );
}

/** l'état des fiches, plus un Cercle de deux paroles (« Marseille ») et un gardé de côté (la fin de la liste) */
function stockageCercle(): Record<string, string> {
  const ls = stockageFiches(true);
  const st = JSON.parse(ls['promi_state']!) as { promises: Array<Record<string, unknown>>; nid: number };
  st.promises.push(
    {
      ...PAROLE_CERCLE,
      id: 171,
      title: 'acheter le pain',
      cle: 'acheter le pain',
      derAct: 1795483000000,
      place: [0.3, 0.42, 0],
    },
    {
      id: 170,
      title: 'ranger la cave',
      who: 'moi',
      due: null,
      intensity: 2,
      status: 'encours',
      from: 'moi',
      recur: null,
      remind: null,
      draft: true,
      files: [],
    },
  );
  st.nid = 172;
  ls['promi_state'] = JSON.stringify(st);
  return ls;
}

/** l'Index ouvert des deux côtés, posé */
async function ouvrirIndex(P: Page, A: Page): Promise<void> {
  await P.evaluate(() => (document.getElementById('indexBtn') as HTMLElement).click());
  await A.evaluate(`${P_}.index().ouvrir()`);
  // par tranches : les passes du prototype (`_s4TitresAjuste`) partent d'un observateur et de minuteurs — une seule tranche de 180 images ne
  // leur rend jamais la main (l'observateur ne tourne qu'entre deux tâches)
  for (let k = 0; k < 6; k++) await Promise.all([images(P, 30), images(A, 30)]);
}

/** au pixel, hors matière (M1), la page posée (deux relevés identiques des deux côtés) */
async function juger(P: Page, A: Page, nom: string): Promise<void> {
  let ip: Buffer = Buffer.alloc(0);
  let ia: Buffer = Buffer.alloc(0);
  for (let k = 0; k < 20; k++) {
    await Promise.all([images(P, 40), images(A, 40)]);
    const Z = [...(await matieres(P)), ...(await matieres(A))];
    const p2 = masquer(await image(P), Z);
    const a2 = masquer(await image(A), Z);
    const pose = k > 1 && p2.equals(ip) && a2.equals(ia);
    [ip, ia] = [p2, a2];
    if (pose) break;
  }
  writeFileSync(join(RES, `${nom}-prototype.png`), ip);
  writeFileSync(join(RES, `${nom}-app.png`), ia);
  const e = ecart(ip, ia);
  expect(
    { n: e.n, boite: e.boite },
    `${nom} : pixels écartés de plus de 2 niveaux (bords lissés hors macOS : ${String(e.bords)})`,
  ).toEqual({ n: 0, boite: null });
}

for (const theme of ['sombre', 'clair'] as const)
  test(`l'Index avec un Cercle de deux paroles et un gardé de côté, comme le prototype : ${theme}`, async ({
    browser,
  }) => {
    const ls = { ...stockageCercle(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
    const { P, A, erreurs } = await deuxPilotes(browser, ls);
    try {
      mkdirSync(RES, { recursive: true });
      // la sonde (sur « … sombre ») : le gardé de côté perd son pointillé
      if (sonde('garde-sans-pointille'))
        await A.addStyleTag({ content: '#indexSheet .s4-carte{outline:none!important}' });
      await ouvrirIndex(P, A);
      const c = await cartes(A);
      expect(c, 'les cartes, leurs mots, la taille de chaque titre').toEqual(await cartes(P));
      expect(c[0], 'le Cercle en tête (sa dernière action)').toMatch(/^ \| avec \+2 \| Marseille \|/);
      expect(c.at(-1), 'le gardé de côté ferme la liste').toMatch(/gardé de côté \| ranger la cave/);
      await juger(P, A, `${theme}-cercle-repos`);
      for (const pg of [P, A])
        await pg.evaluate(() => {
          const l = document.getElementById('indexList')!;
          l.scrollTop = l.scrollHeight;
        });
      await juger(P, A, `${theme}-cercle-bout`);
      expect(erreurs).toEqual([]);
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  });

for (const theme of ['sombre', 'clair'] as const)
  test(`l'Index au repos et défilé au bout, comme le prototype : ${theme}`, async ({ browser }) => {
    const ls = { ...stockageFiches(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
    const { P, A, erreurs } = await deuxPilotes(browser, ls);
    try {
      mkdirSync(RES, { recursive: true });
      // la sonde (sur « … sombre ») : la vraie app range les cartes par ordre de plantation, la plus ancienne d'abord
      if (sonde('ordre-plantation'))
        await A.evaluate(`(() => { for (const p of ${P_}.magasin.etat().paroles) p.derAct = 1000 - p.id; })()`);
      // la sonde (sur « … clair ») : les cartes prennent la crème en clair (l'ancien corps clair, avant C-147)
      if (sonde('carte-creme-clair'))
        await A.addStyleTag({ content: '.device.light #indexSheet .s4-carte{background:#F7F0DE!important}' });
      await P.evaluate(() => (document.getElementById('indexBtn') as HTMLElement).click());
      await A.evaluate(`${P_}.index().ouvrir()`);
      // par tranches : les passes du prototype (`_s4TitresAjuste`) partent d'un observateur et de minuteurs — une seule tranche de 180 images ne
      // leur rend jamais la main (l'observateur ne tourne qu'entre deux tâches)
      for (let k = 0; k < 6; k++) await Promise.all([images(P, 30), images(A, 30)]);
      expect(await cartes(A), 'les cartes, leurs mots, la taille de chaque titre').toEqual(await cartes(P));
      const juge = async (quoi: string): Promise<void> => {
        let ip: Buffer = Buffer.alloc(0);
        let ia: Buffer = Buffer.alloc(0);
        for (let k = 0; k < 20; k++) {
          await Promise.all([images(P, 40), images(A, 40)]);
          const Z = [...(await matieres(P)), ...(await matieres(A))];
          const p2 = masquer(await image(P), Z);
          const a2 = masquer(await image(A), Z);
          const pose = k > 1 && p2.equals(ip) && a2.equals(ia);
          [ip, ia] = [p2, a2];
          if (pose) break;
        }
        writeFileSync(join(RES, `${theme}-${quoi}-prototype.png`), ip);
        writeFileSync(join(RES, `${theme}-${quoi}-app.png`), ia);
        const e = ecart(ip, ia);
        expect(
          { n: e.n, boite: e.boite },
          `${quoi} : pixels écartés de plus de 2 niveaux (bords lissés hors macOS : ${String(e.bords)})`,
        ).toEqual({ n: 0, boite: null });
      };
      await juge('repos');
      for (const pg of [P, A])
        await pg.evaluate(() => {
          const l = document.getElementById('indexList')!;
          l.scrollTop = l.scrollHeight;
        });
      await juge('bout');
      expect(erreurs).toEqual([]);
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  });
