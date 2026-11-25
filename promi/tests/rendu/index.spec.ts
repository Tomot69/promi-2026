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
    // et sous le menu ⇅ ouvert : une dalle qu'il couvre ne masque pas le panneau
    const M = document.querySelector('#ixMenu.on .ix-menu-p');
    const haut = Math.max((L.top - D.top) / k, M ? (M.getBoundingClientRect().bottom - D.top) / k : 0);
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

/** le centre d'un élément, en pt de l'appareil */
async function centre(pg: Page, sel: string): Promise<[number, number]> {
  return (await pg.evaluate((sel) => {
    const D = document.getElementById('device')!.getBoundingClientRect();
    const k = D.width / 390;
    const r = document.querySelector(sel)!.getBoundingClientRect();
    return [(r.left + r.width / 2 - D.left) / k, (r.top + r.height / 2 - D.top) / k];
  }, sel)) as [number, number];
}
async function toucher(pg: Page, x: number, y: number): Promise<void> {
  const r = await pg.evaluate(() => {
    const b = document.getElementById('device')!.getBoundingClientRect();
    return { x: b.left, y: b.top, k: b.width / 390 };
  });
  await pg.mouse.click(r.x + x * r.k, r.y + y * r.k);
}
/** un toucher au même point des deux côtés (celui de la vraie app), puis la page avancée */
async function toucherDeux(P: Page, A: Page, sel: string): Promise<void> {
  const [x, y] = await centre(A, sel);
  await Promise.all([toucher(P, x, y), toucher(A, x, y)]);
  for (let k = 0; k < 3; k++) await Promise.all([images(P, 30), images(A, 30)]);
}

for (const theme of ['sombre', 'clair'] as const)
  test(`le menu ⇅ de l'Index, ses tris et ses filtres, comme le prototype : ${theme}`, async ({ browser }) => {
    const ls = { ...stockageCercle(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
    const { P, A, erreurs } = await deuxPilotes(browser, ls);
    try {
      mkdirSync(RES, { recursive: true });
      // la sonde (sur « … sombre ») : « Par personne » range comme « Récents »
      if (sonde('tri-personne-sourd'))
        await A.evaluate(() => {
          document.addEventListener(
            'pointerup',
            (ev) => {
              if ((ev.target as Element | null)?.closest('[data-tri="personne"]')) ev.stopImmediatePropagation();
            },
            true,
          );
        });
      await ouvrirIndex(P, A);
      await toucherDeux(P, A, '#ixTriBtn');
      expect(
        await A.evaluate(() => document.getElementById('ixMenu')!.classList.contains('on')),
        'le menu est ouvert',
      ).toBe(true);
      await juger(P, A, `${theme}-menu`);
      // un toucher dans le panneau, hors d'un choix (son groupe « TRIER ») : il reste ouvert (Q578)
      await toucherDeux(P, A, '#ixMenu .ix-mg');
      expect(
        await A.evaluate(() => document.getElementById('ixMenu')!.classList.contains('on')),
        'Q578 : il reste',
      ).toBe(true);
      for (const sel of [
        '#ixMenu [data-tri="personne"]',
        '#ixMenu [data-tri="nuee"]',
        '#ixMenu [data-filt="suspens"]',
        '#ixMenu [data-filt="brouillons"]',
        '#ixMenu [data-filt="nuees"]',
      ]) {
        if (!(await A.evaluate(() => document.getElementById('ixMenu')!.classList.contains('on'))))
          await toucherDeux(P, A, '#ixTriBtn');
        await toucherDeux(P, A, sel);
        expect(await cartes(A), `${sel} : les cartes`).toEqual(await cartes(P));
        await juger(P, A, `${theme}-${sel.replace(/[^a-z]/g, '')}`);
      }
      // ailleurs que le panneau : il se referme
      await toucherDeux(P, A, '#ixTriBtn');
      await Promise.all([toucher(P, 195, 800), toucher(A, 195, 800)]);
      await Promise.all([images(P, 30), images(A, 30)]);
      expect(await A.evaluate(() => document.getElementById('ixMenu')!.classList.contains('on')), 'refermé').toBe(
        false,
      );
      expect(erreurs).toEqual([]);
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  });
