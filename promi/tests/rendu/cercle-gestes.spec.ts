/**
 * LOT 5 — LA FICHE D'UN CERCLE AU DOIGT (redteam_cercle_defile, redteam_cercle_plus, redteam_cercle_membres ; C-238, C-243, C-230).
 *
 *  · LE FIL DÉFILE (C-238) : la fiche défilée à 60, 140, 250 pt et jusqu'au bout — la même image que le prototype (la vague qui monte puis se couche
 *    à plat sous le plateau, C-259 ; les lignes qui passent sous le bloc collé ; le bout du défilement : la dernière ligne entière au-dessus de lui) ;
 *  · « PLANTER DANS LE CERCLE » (C-230) : le menu (Chiche, Promi) au pixel ; un toucher à côté le referme ; Promi puis Chiche ouvrent la page + de leur
 *    nature, rattachée au Cercle, ses membres déjà choisis (« à qui », « qui ose ? »).
 * Mêmes exceptions que cercle.spec.ts (M1 la matière, M2 le grain des anneaux).
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { deuxPilotes, images, ecart, sonde, stockageCercles, masquerFiche, type Zone, P_ } from './aides.ts';
import { toucherDeux, poser } from './listes.ts';

const RES = join(import.meta.dirname, 'resultats', 'cercle');

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

async function comparer(P: Page, A: Page, nom: string): Promise<void> {
  const dv = await P.evaluate(() => {
    const r = document.getElementById('device')!.getBoundingClientRect();
    return { x: r.left, y: r.top, width: r.width, height: r.height };
  });
  let ip: Buffer = Buffer.alloc(0);
  let ia: Buffer = Buffer.alloc(0);
  let Z: Zone[] = [];
  for (let i = 0; i < 12; i++) {
    await Promise.all([images(P, 30), images(A, 30)]);
    const { Z: Z2, n } = await zones(A, P);
    const ip2 = masquerFiche(await P.screenshot({ clip: dv }), Z2, n);
    const ia2 = masquerFiche(await A.screenshot(), Z2, n);
    const pose = i > 1 && ip2.equals(ip) && ia2.equals(ia);
    [Z, ip, ia] = [Z2, ip2, ia2];
    if (pose) break;
  }
  mkdirSync(RES, { recursive: true });
  writeFileSync(join(RES, `${nom}-prototype.png`), ip);
  writeFileSync(join(RES, `${nom}-app.png`), ia);
  const e = ecart(ip, ia);
  expect(
    { n: e.n, boite: e.boite },
    `${nom} : pixels écartés (zones exceptées ${JSON.stringify(Z)} ; bords lissés hors macOS : ${String(e.bords)})`,
  ).toEqual({ n: 0, boite: null });
}

async function ouvrirCercle(P: Page, A: Page, k: string): Promise<void> {
  await P.evaluate((k) => (window as unknown as { openNueeDetail(k: string): void }).openNueeDetail(k), k);
  await A.evaluate(`${P_}.fiche().ouvrirCercle(${JSON.stringify(k)})`);
  await poser(P, A, 8);
}

const defiler = async (P: Page, A: Page, s: number): Promise<[number, number]> => {
  const p = await P.evaluate((s) => {
    const d = document.getElementById('detailPoster')!;
    d.scrollTop = s;
    return d.scrollTop;
  }, s);
  const a = await A.evaluate((s) => {
    const d = document.getElementById('dpDefile')!;
    d.scrollTop = s;
    return d.scrollTop;
  }, s);
  await poser(P, A, 4);
  return [p, a];
};

test('le fil d’un Cercle défile comme le prototype : 60, 140, 250 pt, jusqu’au bout, puis revenu en haut', async ({
  browser,
}) => {
  const { P, A, erreurs } = await deuxPilotes(browser, { ...stockageCercles(), promi_prenom: 'Tom' });
  try {
    // la sonde : le trait plat de la jonction absent (la vague ne se couche plus sous le plateau, C-259)
    if (sonde('cercle-defile-court'))
      await A.addStyleTag({ content: '#detailPoster #v195Plat{display:none!important}' });
    await ouvrirCercle(P, A, 'n1');
    for (const s of [60, 140, 250, 5000, 0]) {
      const [p, a] = await defiler(P, A, s);
      expect(a, `le défilement (${String(s)})`).toBe(p);
      await comparer(P, A, `defile-${String(s)}`);
    }
    expect(erreurs).toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});

// le prototype : `selNuee` est une déclaration `let` (pas une propriété de `window`, le piège de `createKind`, v177a) — lue par une expression
const etatPlus = (pg: Page, proto: boolean): Promise<string> =>
  proto
    ? pg.evaluate(`(() => { const cs = document.getElementById('createSheet');
        return JSON.stringify([cs.classList.contains('pp-chiche') ? 'chiche' : 'promi', String(window._phrase.qui), selNuee]); })()`)
    : pg.evaluate(`(() => { const e = ${P_}.pagePlus().etat().phrase;
        return JSON.stringify([e.nat, e.qui.join(', '), e.cercle]); })()`);

for (const nat of ['promi', 'chiche'] as const)
  test(`« Planter dans le Cercle » : le menu, puis ${nat === 'promi' ? 'Promi' : 'Chiche'} — la page + rattachée au Cercle, ses membres choisis`, async ({
    browser,
  }) => {
    const { P, A, erreurs } = await deuxPilotes(browser, { ...stockageCercles(), promi_prenom: 'Tom' });
    try {
      // la sonde (sur « … Promi … ») : « Planter dans le Cercle » n'ouvre plus rien
      if (sonde('cercle-planter-sourd') && nat === 'promi')
        await A.evaluate(() => {
          document.addEventListener(
            'pointerdown',
            (ev) => {
              if ((ev.target as Element | null)?.closest('#nfAdd')) ev.stopImmediatePropagation();
            },
            true,
          );
        });
      await ouvrirCercle(P, A, 'n1');
      await toucherDeux(P, A, '#nfAdd');
      await poser(P, A, 3);
      await comparer(P, A, `menu-${nat}`);
      await toucherDeux(P, A, `#cpChoix .cp-pil[data-k="${nat}"]`);
      await poser(P, A, 30);
      expect(await etatPlus(A, false)).toBe(JSON.stringify([nat, 'Rachel, Marion', 'n1']));
      const p = JSON.parse(await etatPlus(P, true)) as string[];
      expect([p[0], p[1], p[2]], 'le prototype').toEqual([nat, 'Rachel, Marion', 'n1']);
      expect(erreurs).toEqual([]);
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  });

test('le menu de « Planter dans le Cercle » : un toucher à côté le referme et n’actionne rien', async ({ browser }) => {
  const { P, A, erreurs } = await deuxPilotes(browser, { ...stockageCercles(), promi_prenom: 'Tom' });
  try {
    await ouvrirCercle(P, A, 'n1');
    await toucherDeux(P, A, '#nfAdd');
    // à côté : sur le titre du Cercle (rien ne s'ouvre dessous)
    await toucherDeux(P, A, '#dptTitre');
    await poser(P, A, 6);
    const ouvert = (pg: Page): Promise<boolean> =>
      pg.evaluate(() => getComputedStyle(document.getElementById('cpChoix')!).display !== 'none');
    expect(await ouvert(A)).toBe(false);
    expect(await ouvert(P)).toBe(false);
    await comparer(P, A, 'menu-referme');
    expect(erreurs).toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});
