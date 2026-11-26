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
import { deuxPilotes, images, ecart, sonde, stockageCercles, masquerFiche, vraieApp, type Zone, P_ } from './aides.ts';
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
        // une zone sous Peaufiner ouvert ne se voit pas : elle n'est pas exceptée (sinon elle masquerait Peaufiner)
        const corps = document.getElementById('dpdCorps');
        const C =
          corps && !corps.hidden && getComputedStyle(corps).display !== 'none' ? corps.getBoundingClientRect() : null;
        return out.filter(([x, y, w, h]) => {
          if (!C) return true;
          const cx = D.left + (x! + w! / 2) * k;
          const cy = D.top + (y! + h! / 2) * k;
          return !(cx >= C.left && cx <= C.right && cy >= C.top && cy <= C.bottom);
        });
      })) as Zone[]),
    );
  const anneaux = (await A.evaluate(() => {
    const D = document.getElementById('detailPoster')!.getBoundingClientRect();
    const k = D.width / 390 || 1;
    // un anneau sous Peaufiner ouvert ne se voit pas : il n'est pas excepté
    const corps = document.getElementById('dpdCorps');
    const ouvert = !!corps && !corps.hidden;
    return ouvert
      ? []
      : [...document.querySelectorAll('#detailPoster.fiche canvas.kr-c')].map((c) => {
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

for (const theme of ['sombre', 'clair'] as const)
  test(`Peaufiner d’un Cercle, ouvert par sa barre, comme le prototype : en haut, puis défilé (700, 1400) — ${theme}`, async ({
    browser,
  }) => {
    const ls = { ...stockageCercles(), promi_prenom: 'Tom', promi_theme: theme === 'clair' ? 'light' : 'dark' };
    const { P, A, erreurs } = await deuxPilotes(browser, ls);
    try {
      // la sonde (sur « … sombre ») : la carte MEMBRES 4 pt plus bas
      if (sonde('cercle-peauf-decale') && theme === 'sombre')
        await A.addStyleTag({ content: '#dpdCorps #npMemb{translate:0 4px}' });
      await ouvrirCercle(P, A, 'n1');
      await toucherDeux(P, A, '#dpdTog');
      await poser(P, A, 20);
      await comparer(P, A, `peauf-${theme}`);
      for (const y of [700, 1400]) {
        const p = await P.evaluate((y) => {
          const c = document.getElementById('dpdCorps')!;
          c.scrollTop = y;
          return c.scrollTop;
        }, y);
        const a = await A.evaluate((y) => {
          const c = document.getElementById('dpdCorps')!;
          c.scrollTop = y;
          return c.scrollTop;
        }, y);
        expect(a, `le défilement de Peaufiner (${String(y)})`).toBe(p);
        await poser(P, A, 4);
        await comparer(P, A, `peauf-${theme}-${String(y)}`);
      }
      expect(erreurs).toEqual([]);
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  });

/** les mots d'un Cercle (`promi_cercle_mots` du prototype) : un de Rachel, un de moi */
const MOTS = JSON.stringify({
  n1: [
    { t: 'On commence lundi ?', d: '2026-11-20T10:00:00.000Z', by: 'Rachel', vu: true },
    { t: 'Je prends le dessert', d: '2026-11-21T18:30:00.000Z', by: 'Tom', vu: true },
  ],
});
test('les mots d’un Cercle : le nombre sur « Un mot… », « Les Mots » au bout du fil, comme le prototype (C-248, C-261)', async ({
  browser,
}) => {
  const ls = { ...stockageCercles(), promi_prenom: 'Tom', promi_cercle_mots: MOTS, promi_mots_v184: '1' };
  const { P, A, erreurs } = await deuxPilotes(browser, ls);
  try {
    // la sonde : « Les Mots » 6 pt plus haut (collé au fil)
    if (sonde('cercle-mots-colles'))
      await A.addStyleTag({ content: '#detailPoster #cm5Titre{translate:0 -6px!important}' });
    await ouvrirCercle(P, A, 'n1');
    await comparer(P, A, 'mots-repos');
    const [p, a] = await defiler(P, A, 5000);
    expect(a, 'le bout du défilement').toBe(p);
    await comparer(P, A, 'mots-bas');
    expect(erreurs).toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});

test('« Un mot… » d’un Cercle : écrit, envoyé — la liste et le Fil comme le prototype (lot-V146-CERCLE-MOT, C-260)', async ({
  browser,
}) => {
  const ls = { ...stockageCercles(), promi_prenom: 'Tom', promi_cercle_mots: MOTS, promi_mots_v184: '1' };
  const { P, A, erreurs } = await deuxPilotes(browser, ls);
  try {
    // la sonde : le mot d'un Cercle n'est pas écrit
    if (sonde('mot-cercle-perdu'))
      await A.evaluate(`(() => { const m = ${P_}.magasin; m.motCercle = () => undefined; })()`);
    await ouvrirCercle(P, A, 'n1');
    for (const pg of [P, A]) await pg.addStyleTag({ content: '#device input{caret-color:transparent!important}' });
    await toucherDeux(P, A, '#cm5Ligne');
    await poser(P, A, 3);
    for (const pg of [P, A]) await pg.keyboard.type('Bravo');
    await poser(P, A, 4);
    for (const pg of [P, A]) await pg.keyboard.press('Enter');
    await poser(P, A, 6);
    await comparer(P, A, 'mot-envoye');
    // la ligne du Fil
    const fil = (pg: Page, proto: boolean): Promise<string> =>
      proto ? pg.evaluate(`String(FEED[0] && FEED[0].text)`) : pg.evaluate(`String(${P_}.magasin.etat().fil[0].text)`);
    expect(await fil(A, false)).toBe(await fil(P, true));
    expect(await fil(A, false)).toContain('Marseille');
    expect(erreurs).toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});

test('la fiche d’un Cercle à l’échelle 0,79 (330 × 714) : chaque cote en pt est celle de 390 × 844, et Peaufiner aussi (A3)', async ({
  browser,
}) => {
  const COTES = `(() => [...['dAura', 'dptQui', 'dptTitre', 'dptQuand', 'dpNueeFil', 'cm5Ligne', 'nfAdd'].map((id) => document.getElementById(id)),
      ...document.querySelectorAll('#dpNueeFil .nf-item'), ...document.querySelectorAll('#dpdCorps .np-carte, #dpdCorps .np-murs')]
      .map((e) => (e ? (e.id || e.className) + ':' + e.offsetTop.toFixed(1) + ',' + e.offsetHeight.toFixed(1) : '—')).join(' '))()`;
  const lire = async (vue: { width: number; height: number }): Promise<string[]> => {
    const pg = await (await browser.newContext({ viewport: vue, deviceScaleFactor: 3 })).newPage();
    try {
      await vraieApp(pg, { ...stockageCercles(), promi_prenom: 'Tom' });
      // la sonde : à l'échelle réduite, le fil posé 4 pt plus bas
      if (sonde('cercle-echelle') && vue.width < 390)
        await pg.addStyleTag({ content: '#detailPoster .fi-fil{top:calc(var(--x,0px) + 492px)!important}' });
      await pg.evaluate(`${P_}.fiche().ouvrirCercle('n1')`);
      await pg.waitForTimeout(900);
      const a = (await pg.evaluate(COTES)) as string;
      await pg.evaluate(() =>
        document.getElementById('dpdTog')!.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })),
      );
      await pg.evaluate(() =>
        document.getElementById('dpdTog')!.dispatchEvent(new PointerEvent('pointerup', { bubbles: true })),
      );
      await pg.waitForTimeout(900);
      return [a, (await pg.evaluate(COTES)) as string];
    } finally {
      await pg.context().close();
    }
  };
  const [a, b] = await Promise.all([lire({ width: 390, height: 844 }), lire({ width: 330, height: 714 })]);
  expect(a[1], 'Peaufiner ouvert').toContain('npMemb');
  expect(b, 'à 0,79, les mêmes cotes en pt').toEqual(a);
});
