/**
 * LOT 1 — L'ACCUEIL ET LA TOILE VIVANTE.
 *
 * (1) IDENTITÉ AU PIXEL (la règle de la vraie app) : l'accueil de la vraie app à 390 × 844 contre celui du prototype (son appareil, dans la
 *     fenêtre du banc), même état importé des deux côtés, même WebKit, ×3, clair et sombre, menu du + fermé et ouvert. La Toile est masquée
 *     des deux côtés (elle est jugée au pixel par banc-rendu.spec et entrees.spec) et les animations gelées (le I qui clignote, l'anneau
 *     qui tourne : leur nom et leur durée sont jugés à part). Seuls les coins arrondis du téléphone que le prototype dessine sont exceptés.
 *     Tolérance : 2 niveaux sur 255 (l'anticrénelage du compositeur), 0 pixel au-delà.
 * (2) LES GESTES (SPEC-ECRANS §1) : toucher une dalle demande SA fiche, 260 ms plus tard ; le double toucher recadre ; le + ouvre les
 *     natures sur place, une pilule demande la page + de sa nature, un toucher ailleurs referme ; chaque entrée de la barre demande son
 *     écran sur toute sa zone (C-106) ; le symbole « recadrer » naît quand la main bouge la vue, part après 4 s (C-188) ; la Toile vit au
 *     repos sous l'accueil (C-028) ; « Plus tard » deux fois, le bandeau ne revient plus (C-200 ①).
 */
import { test, expect, type Page } from '@playwright/test';
import { existsSync, readFileSync, readdirSync, mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { PNG } from 'pngjs';

const RACINE = join(import.meta.dirname, '..', '..', '..');
const ETAT = process.env['PROMI_ETAT']
  ? join(RACINE, process.env['PROMI_ETAT'])
  : (() => {
      // l'état de Tom le plus récent s'il est là (hors dépôt), sinon celui du banc (l'intégration continue)
      const d = join(RACINE, 'etats');
      const tom = existsSync(d)
        ? readdirSync(d)
            .filter((f) => /^tom-\d{8}-\d{6}\.json$/.test(f))
            .sort()
            .pop()
        : undefined;
      return tom ? join(d, tom) : join(RACINE, 'banc-etats', 'etat-25.json');
    })();
const RESULTATS = join(import.meta.dirname, 'resultats', 'accueil');

function stockage(): Record<string, string> {
  const x = JSON.parse(readFileSync(ETAT, 'utf8')) as { ls?: Record<string, string> } & Record<string, unknown>;
  const ls: Record<string, string> = {};
  for (const [k, v] of Object.entries(x.ls ?? x)) if (k !== 'setItem' && typeof v === 'string') ls[k] = v;
  return ls;
}

const GEL =
  '*,*::before,*::after{animation:none!important;transition:none!important}' +
  '#device#device#device #createBtn::before,#device#device#device #createBtn::after{animation:none!important;transform:none!important}' +
  '#device#device#device .acc-mm i{animation:none!important;opacity:1!important}' +
  '#stage{visibility:hidden!important}';

async function prototype(page: Page, ls: Record<string, string>): Promise<void> {
  await page.addInitScript((ls) => {
    try {
      Object.defineProperty(Navigator.prototype, 'webdriver', { get: () => false, configurable: true });
    } catch {
      /* rien */
    }
    localStorage.clear();
    for (const [k, v] of Object.entries(ls)) localStorage.setItem(k, v);
  }, ls);
  await page.goto('http://127.0.0.1:8753/app.html');
  await page.waitForTimeout(9000);
  await page.evaluate(() => {
    const o = document.getElementById('promiOnb');
    if (o) {
      o.classList.add('gone');
      o.style.display = 'none';
    }
  });
}

async function vraieApp(page: Page, ls: Record<string, string>): Promise<void> {
  await page.goto('http://127.0.0.1:5180/?banc=1');
  await page.waitForFunction(() => !!(window as unknown as { __promi?: unknown }).__promi);
  await page.evaluate(async (ls) => {
    const p = (window as unknown as { __promi: { magasin: { importer(x: unknown): void }; demarrer(): Promise<void> } })
      .__promi;
    p.magasin.importer({ ls });
    await p.demarrer();
  }, ls);
  await page.waitForTimeout(1500);
}

async function ouvrirPlus(page: Page): Promise<void> {
  const r = await page.evaluate(() => {
    const b = document.getElementById('createBtn')!.getBoundingClientRect();
    return [b.left + b.width / 2, b.top + b.height / 2];
  });
  await page.mouse.click(r[0]!, r[1]!);
  await page.waitForTimeout(500);
}

/** les pixels qui s'écartent de plus de 2 niveaux, hors des quatre coins du téléphone (30 pt) */
/**
 * Les pixels qui s'écartent de plus de 2 niveaux, hors des quatre coins du téléphone (30 pt). Sur le Mac (le WebKit de l'iPhone) : aucun.
 * Ailleurs (l'intégration continue, WebKit sous Linux), la règle de Q616 (Tom) : le lissage d'un BORD peut différer — un pixel situé sur un
 * bord de la référence (contraste de plus de 24 niveaux dans ses 5 × 5 pixels) et écarté de 12 niveaux au plus n'est pas compté ; hors
 * des bords, la règle reste aucun pixel. (Mesuré sur la CI le 20 nov. : 379 à 661 pixels, tous sur un bord, 8 niveaux au plus.)
 */
function ecart(a: Buffer, b: Buffer): { n: number; boite: number[] | null; bords: number } {
  const A = PNG.sync.read(a);
  const B = PNG.sync.read(b);
  if (A.width !== B.width || A.height !== B.height) return { n: -1, boite: null, bords: 0 };
  const W = A.width;
  const H = A.height;
  const k = W / 390;
  const strict = process.platform === 'darwin';
  const lum = (x: number, y: number): number => {
    const i = (y * W + x) * 4;
    return 0.299 * A.data[i]! + 0.587 * A.data[i + 1]! + 0.114 * A.data[i + 2]!;
  };
  const surBord = (x: number, y: number): boolean => {
    let lo = 255;
    let hi = 0;
    for (let dy = -2; dy <= 2; dy++)
      for (let dx = -2; dx <= 2; dx++) {
        const xx = Math.min(W - 1, Math.max(0, x + dx));
        const yy = Math.min(H - 1, Math.max(0, y + dy));
        const l = lum(xx, yy);
        if (l < lo) lo = l;
        if (l > hi) hi = l;
      }
    return hi - lo > 24;
  };
  let n = 0;
  let bords = 0;
  let x0 = 1e9,
    y0 = 1e9,
    x1 = -1,
    y1 = -1;
  for (let y = 0; y < H; y++)
    for (let x = 0; x < W; x++) {
      const coin = (x < 30 * k || x >= 360 * k) && (y < 30 * k || y >= 814 * k);
      if (coin) continue;
      const i = (y * W + x) * 4;
      const d = Math.max(
        Math.abs(A.data[i]! - B.data[i]!),
        Math.abs(A.data[i + 1]! - B.data[i + 1]!),
        Math.abs(A.data[i + 2]! - B.data[i + 2]!),
      );
      if (d <= 2) continue;
      if (!strict && d <= 12 && surBord(x, y)) {
        bords++;
        continue;
      }
      n++;
      x0 = Math.min(x0, x);
      y0 = Math.min(y0, y);
      x1 = Math.max(x1, x);
      y1 = Math.max(y1, y);
    }
  return { n, boite: n ? [x0 / k, y0 / k, x1 / k, y1 / k].map((v) => Math.round(v)) : null, bords };
}

for (const theme of ['sombre', 'clair'] as const)
  for (const menu of [false, true])
    test(`identité au pixel : l'accueil${menu ? ', menu du + ouvert' : ''}, ${theme}`, async ({ browser }) => {
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
      for (const pg of [P, A]) await pg.addStyleTag({ content: GEL });
      await P.waitForTimeout(600);
      if (menu) await Promise.all([ouvrirPlus(P), ouvrirPlus(A)]);
      const dv = await P.evaluate(() => {
        const r = document.getElementById('device')!.getBoundingClientRect();
        return { x: r.left, y: r.top, width: r.width, height: r.height };
      });
      const ip = await P.screenshot({ clip: dv });
      const ia = await A.screenshot();
      mkdirSync(RESULTATS, { recursive: true });
      const nom = `${theme}${menu ? '-menu' : ''}`;
      writeFileSync(join(RESULTATS, `${nom}-prototype.png`), ip);
      writeFileSync(join(RESULTATS, `${nom}-app.png`), ia);
      const e = ecart(ip, ia);
      expect(erreurs).toEqual([]);
      expect(
        { n: e.n, boite: e.boite },
        `pixels écartés de plus de 2 niveaux (état : ${ETAT} ; bords lissés exceptés hors macOS : ${String(e.bords)})`,
      ).toEqual({ n: 0, boite: null });
    });

test("les animations de l'accueil : le I de PROMI clignote, l'anneau du + tourne", async ({ page }) => {
  await vraieApp(page, stockage());
  const r = await page.evaluate(() => {
    const i = getComputedStyle(document.querySelector('.acc-mm i')!);
    const b = getComputedStyle(document.getElementById('createBtn')!, '::before');
    return {
      i: [i.animationName, i.animationDuration, i.animationTimingFunction],
      anneau: [b.animationName, b.animationDuration, b.animationTimingFunction],
    };
  });
  expect(r.i).toEqual(['promiBlink', '1.15s', 'steps(1)']);
  expect(r.anneau).toEqual(['heroSpin', '100s', 'linear']);
});

const P_ = 'window.__promi';

test('toucher une dalle demande SA fiche, 260 ms plus tard ; le double toucher recadre', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, stockage());
  // les dalles des paroles, à l'écran, hors du plateau et de la barre
  const dalles = (await page.evaluate(`(() => {
    const L = Toile_lecture(); const out = [];
    for (const g of L.graines) { if (g.kind === 'gray' || g.pid == null) continue;
      const x = g.x * L.vue.s + L.vue.ox, y = g.y * L.vue.s + L.vue.oy;
      if (x < 10 || x > 380 || y < 120 || y > 690) continue;
      const h = Toile.hit(x, y); if (h && h.pid === g.pid) out.push({ pid: g.pid, x, y }); }
    return out; })()`)) as Array<{ pid: number; x: number; y: number }>;
  expect(dalles.length, 'au moins une dalle de parole touchable').toBeGreaterThan(0);
  // l'heure du lever du doigt, à l'horloge de l'app (celle de la navigation) : la demande vient 260 ms après, jamais avant
  await page.evaluate(() => {
    const w = window as unknown as { __leve: number[]; __promi: { horloge: { maintenant(): number } } };
    w.__leve = [];
    window.addEventListener('pointerup', () => w.__leve.push(w.__promi.horloge.maintenant()), true);
  });
  for (const d of dalles.slice(0, 6)) {
    const avant = (await page.evaluate(`${P_}.nav.journal().length`)) as number;
    await page.mouse.click(d.x, d.y);
    await page.waitForFunction(
      (n) => (window as unknown as { __promi: { nav: { journal(): unknown[] } } }).__promi.nav.journal().length > n,
      avant,
      { timeout: 5000 },
    );
    const j = (await page.evaluate(`${P_}.nav.journal()`)) as Array<{ vers: string; arg?: number; t: number }>;
    const leve = (await page.evaluate('window.__leve.at(-1)')) as number;
    expect(j.slice(avant), `la dalle ${String(d.pid)}`).toEqual([
      expect.objectContaining({ vers: 'fiche', arg: d.pid }),
    ]);
    expect(j.at(-1)!.t - leve, 'la fiche est demandée 260 ms après le lever du doigt').toBeGreaterThanOrEqual(259);
    await page.waitForTimeout(400);
  }
  // le double toucher : la vue glissée à la main revient au cadrage
  await page.mouse.move(195, 400);
  await page.mouse.down();
  await page.mouse.move(150, 360, { steps: 8 });
  await page.mouse.up();
  await page.waitForTimeout(600);
  expect(await page.evaluate(`${P_}.facade.vueALaMain()`)).toBe(true);
  // hors de toute dalle de parole (sur une dalle, la fiche serait demandée 260 ms après le premier toucher)
  const vide = (await page.evaluate(`(() => { for (let y = 200; y < 680; y += 9) for (let x = 40; x < 350; x += 9) {
    const h = Toile.hit(x, y); if (!h || (h.pid == null && h.kind !== 'nuee')) return [x, y]; } return [195, 400]; })()`)) as [
    number,
    number,
  ];
  await page.mouse.click(vide[0], vide[1]);
  await page.waitForTimeout(80);
  await page.mouse.click(vide[0], vide[1]);
  await page.waitForTimeout(600);
  expect(
    await page.evaluate(`${P_}.facade.vueALaMain()`),
    `le double toucher recadre (doigts posés vus par la Toile : ${String(await page.evaluate(() => document.getElementById('stage')!.dataset['doigts']))})`,
  ).toBe(false);
});

test('la barre : chaque entrée demande son écran sur toute sa zone ; le + ouvre les natures, une pilule sa page +, ailleurs referme', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, stockage());
  const zones = (await page.evaluate(() =>
    ['studioBtn', 'souffleBtn', 'indexBtn', 'filBtn'].map((id) => {
      const r = document.getElementById(id)!.getBoundingClientRect();
      return [id, r.left, r.top, r.width, r.height] as const;
    }),
  )) as Array<[string, number, number, number, number]>;
  const attendu: Record<string, string> = { studioBtn: 'studio', souffleBtn: 'aura', indexBtn: 'index', filBtn: 'fil' };
  for (const [id, x, y, w, h] of zones)
    for (const [fx, fy] of [
      [0.15, 0.15],
      [0.5, 0.5],
      [0.85, 0.85],
      [0.5, 0.95],
    ] as const) {
      await page.mouse.click(x + w * fx, y + h * fy);
      await page.waitForTimeout(60);
      const j = (await page.evaluate(`${P_}.nav.journal()`)) as Array<{ vers: string }>;
      expect(j.at(-1)?.vers, `${id} à (${String(fx)}, ${String(fy)})`).toBe(attendu[id]);
    }
  await ouvrirPlus(page);
  expect(await page.evaluate(() => document.getElementById('accChoix')!.classList.contains('ouvert'))).toBe(true);
  await page.mouse.click(195, 300); // ailleurs
  await page.waitForTimeout(100);
  expect(
    await page.evaluate(() => document.getElementById('accChoix')!.classList.contains('ouvert')),
    'un toucher ailleurs referme',
  ).toBe(false);
  for (const k of ['nuee', 'chiche', 'promi']) {
    await ouvrirPlus(page);
    const r = await page.evaluate((k) => {
      const b = document.querySelector(`#accChoix .acc-pil[data-k="${k}"]`)!.getBoundingClientRect();
      return [b.left + b.width / 2, b.top + b.height / 2];
    }, k);
    await page.mouse.click(r[0]!, r[1]!);
    await page.waitForTimeout(80);
    const j = (await page.evaluate(`${P_}.nav.journal()`)) as Array<{ vers: string; arg?: string }>;
    expect(j.at(-1)).toEqual(expect.objectContaining({ vers: 'pagePlus', arg: k }));
    expect(await page.evaluate(() => document.getElementById('accChoix')!.classList.contains('ouvert'))).toBe(false);
  }
});

test('le symbole « recadrer » naît quand la main bouge la vue, part après 4 s sans toucher, et recadre', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, stockage());
  const vu = (): Promise<boolean> =>
    page.evaluate(() => document.getElementById('accRecadre')!.classList.contains('vu'));
  expect(await vu(), 'absent au repos').toBe(false);
  await page.mouse.move(195, 420);
  await page.mouse.down();
  await page.mouse.move(140, 380, { steps: 10 });
  await page.mouse.up();
  await page.waitForTimeout(700);
  expect(
    await vu(),
    `paru quand la main a bougé la vue (${String(await page.evaluate(`${P_}.facade.vueALaMain()`))}, ${await page.evaluate(() => (window as unknown as { __promi: { accueil(): { etatRecadre(): { etat: string } } } }).__promi.accueil().etatRecadre().etat)})`,
  ).toBe(true);
  // la vue revient seule dans ses bornes (l'élastique du moteur) : les 4 s comptent depuis son DERNIER mouvement. Mesuré DANS la page, à
  // l'horloge de l'app (une machine lente rend chaque aller-retour du test plus long que la seconde) : le symbole est encore là quand la
  // vue est immobile depuis 3,5 s, et il part avant 4 s + 300 ms de flaques + 1 s de marge
  const attente = await page.evaluate(async () => {
    const a = (
      window as unknown as { __promi: { accueil(): { etatRecadre(): { etat: string; depuis: number } } } }
    ).__promi.accueil();
    let derniereLa = -1;
    const t0 = performance.now();
    const vues: string[] = [];
    for (;;) {
      const e = a.etatRecadre();
      const L = (
        window as unknown as { Toile_lecture(): { W: number; H: number; vue: { s: number; ox: number; oy: number } } }
      ).Toile_lecture();
      vues.push(`${L.vue.s.toFixed(4)}|${L.vue.ox.toFixed(2)}|${L.vue.oy.toFixed(2)}|${String(L.W)}x${String(L.H)}`);
      if (vues.length > 10) vues.shift();
      if (e.etat === 'la') derniereLa = e.depuis;
      if (e.etat === 'absent') return { derniereLa, absent: e.depuis };
      if (performance.now() - t0 > 30000)
        return { derniereLa, absent: -1, etat: e.etat, vues, remises: (e as unknown as { remises: unknown }).remises };
      await new Promise((f) => setTimeout(f, 50));
    }
  });
  expect(
    attente.derniereLa,
    `encore là 3,5 s après le dernier mouvement (${JSON.stringify(attente)})`,
  ).toBeGreaterThanOrEqual(3500);
  expect(attente.absent, `parti avant 5,3 s (${JSON.stringify(attente)})`).toBeGreaterThan(0);
  expect(attente.absent).toBeLessThanOrEqual(5300);
  await page.mouse.move(195, 420);
  await page.mouse.down();
  await page.mouse.move(250, 470, { steps: 10 });
  await page.mouse.up();
  await page.waitForTimeout(700);
  expect(await vu(), 'revenu au déplacement suivant').toBe(true);
  const r = await page.evaluate(() => {
    const b = document.getElementById('accRecadre')!.getBoundingClientRect();
    return [b.left + b.width / 2, b.top + b.height / 2, b.right, b.bottom];
  });
  // l'encre (22 pt) finit sur la marge (24 pt du bord) et 12 pt au-dessus de la barre
  expect(Math.round(r[2]! - 11)).toBe(390 - 24);
  await page.mouse.click(r[0]!, r[1]!);
  await page.waitForTimeout(700);
  expect(await page.evaluate(`${P_}.facade.vueALaMain()`), 'le symbole recadre').toBe(false);
  expect(await vu()).toBe(false);
});

test("la Toile vit au repos sous l'accueil (C-028) : un mouvement est prévu, il a lieu, rien de l'accueil ne couvre le centre", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, stockage());
  // le moteur ne bouge rien dans les 5 s qui suivent un changement de la Toile (la plantation au démarrage)
  await page.waitForTimeout(5600);
  const r = (await page.evaluate(`(() => { const c = document.getElementById('toileCv').getBoundingClientRect();
    const e = document.elementFromPoint(c.left + c.width / 2, c.top + c.height * 0.45);
    return { centre: e && e.id, prevu: Toile.vivant.attend() }; })()`)) as { centre: string; prevu: boolean };
  expect(r.centre, 'le centre de la Toile est libre (la condition de la vie au repos)').toBe('toileCv');
  expect(r.prevu, 'un mouvement de repos est prévu').toBe(true);
  const avant = (await page.evaluate('Toile.vivant.journal().length')) as number;
  await page.evaluate('Toile.vivant.force()');
  await page.waitForTimeout(300);
  expect(await page.evaluate('Toile.vivant.journal().length'), 'le mouvement a eu lieu').toBeGreaterThan(avant);
});

test('le bandeau « Garder ta Toile » : paru après le troisième Promi, « Plus tard » le retire et se note', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  const ls: Record<string, string> = {
    ...stockage(),
    promi_onb: '1',
    promi_compte: '',
    promi_rappel_n: '',
    promi_rappel_non: '',
    promi_rappel_fin: '',
    promi_rappel_vu: '',
  };
  await vraieApp(page, ls);
  const vu = (): Promise<boolean> =>
    page.evaluate(() => document.getElementById('accRappel')!.classList.contains('vu'));
  const paroles = (
    JSON.parse(ls['promi_state'] ?? '{"promises":[]}') as { promises: Array<{ draft?: boolean }> }
  ).promises.filter((p) => !p.draft).length;
  if (paroles < 3) test.skip(true, "l'état porte moins de trois paroles : le bandeau ne paraît pas (la règle)");
  expect(await vu(), 'paru après le troisième Promi').toBe(true);
  const plusTard = async (): Promise<void> => {
    const r = await page.evaluate(() => {
      const b = document.querySelector('#accRappel [data-r="non"]')!.getBoundingClientRect();
      return [b.left + b.width / 2, b.top + b.height / 2];
    });
    await page.mouse.click(r[0]!, r[1]!);
    await page.waitForTimeout(100);
  };
  await plusTard();
  expect(await vu()).toBe(false);
  // le reste de la règle (le retour plus loin, la fin au second refus) : tests/unitaires/accueil.test.ts
  const autres = (await page.evaluate(`${P_}.magasin.etat().autres`)) as Record<string, string>;
  expect(autres['promi_rappel_non']).toBe('1');
  expect(autres['promi_rappel_fin'] ?? '').toBe('');
});
