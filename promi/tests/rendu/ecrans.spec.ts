/**
 * L0 §2 (Tom, 20 nov. 2026) — L'APP S'ADAPTE À CHAQUE ÉCRAN. 390 × 844 reste la référence (identique au pixel au prototype :
 * banc-rendu.spec, entrees.spec) ; aux autres tailles la largeur est fluide, les cotes et les marges sont celles du prototype, ancrées aux
 * bords et aux zones sûres, et la Toile remplit TOUT l'écran — aucune bande vide.
 *
 * Quatre écrans : iPhone SE (375 × 667), iPhone 16e (390 × 844), iPhone 16 Pro Max (440 × 956), Android (412 × 915). Sur chacun, avec
 * l'état embarqué (celui de Tom) : le canevas du moteur couvre l'écran, le moteur s'y mesure, son bord est peint (pas une bande du fond
 * de page), toutes les dalles des paroles sont là et dans l'écran. Une capture de chaque écran porté est gardée (resultats/ecrans/).
 */
import { test, expect } from '@playwright/test';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';

const ECRANS = [
  { nom: 'iphone-se', viewport: { width: 375, height: 667 }, densite: 2 },
  { nom: 'iphone-16e', viewport: { width: 390, height: 844 }, densite: 3 },
  { nom: 'iphone-16-pro-max', viewport: { width: 440, height: 956 }, densite: 3 },
  { nom: 'android', viewport: { width: 412, height: 915 }, densite: 2.625 },
];
const CAPTURES = join(import.meta.dirname, 'resultats', 'ecrans');

for (const e of ECRANS)
  test(`l'accueil s'adapte, la Toile remplit l'écran : ${e.nom} ${e.viewport.width} × ${e.viewport.height}`, async ({
    browser,
  }) => {
    const ctx = await browser.newContext({ viewport: e.viewport, deviceScaleFactor: e.densite });
    const page = await ctx.newPage();
    const erreurs: string[] = [];
    page.on('pageerror', (x) => erreurs.push(String(x)));
    await page.goto('http://127.0.0.1:5180/');
    await page.waitForFunction(() => {
      const w = window as unknown as { Toile_graines?: () => unknown[] };
      return !!w.Toile_graines && w.Toile_graines().length > 0;
    });
    await page.waitForTimeout(2500);
    const lu = (await page.evaluate(`(() => {
      const cv = document.getElementById('toileCv');
      const r = cv.getBoundingClientRect();
      const L = Toile_lecture();
      // le bord du canevas : chaque pixel des quatre bords est peint (opaque) — une bande vide serait transparente ou hors du canevas
      const g = cv.getContext('2d');
      const bord = [];
      const cw = cv.width, ch = cv.height;
      for (const [x, y, w, h] of [[0, 0, cw, 2], [0, ch - 2, cw, 2], [0, 0, 2, ch], [cw - 2, 0, 2, ch]]) {
        const d = g.getImageData(x, y, w, h).data;
        let transparents = 0;
        for (let i = 3; i < d.length; i += 4) if (d[i] < 250) transparents++;
        bord.push(transparents);
      }
      const dalles = L.graines.filter((s) => s.kind !== 'gray' && s.pid != null).map((s) => ({
        pid: s.pid, x: s.x * L.vue.s + L.vue.ox, y: s.y * L.vue.s + L.vue.oy }));
      return { rect: [r.left, r.top, r.width, r.height], cv: [cw, ch], W: L.W, H: L.H, bord, dalles,
        paroles: promises.filter((p) => !p.draft).map((p) => p.id) };
    })()`)) as {
      rect: [number, number, number, number];
      cv: [number, number];
      W: number;
      H: number;
      bord: number[];
      dalles: Array<{ pid: number; x: number; y: number }>;
      paroles: number[];
    };
    mkdirSync(CAPTURES, { recursive: true });
    await page.screenshot({ path: join(CAPTURES, `${e.nom}.png`) });
    expect(erreurs).toEqual([]);
    expect(lu.rect, 'le canevas couvre tout l’écran').toEqual([0, 0, e.viewport.width, e.viewport.height]);
    expect([lu.W, lu.H], 'le moteur se mesure sur l’écran entier').toEqual([e.viewport.width, e.viewport.height]);
    expect(lu.bord, 'aucun pixel non peint sur les quatre bords (aucune bande vide)').toEqual([0, 0, 0, 0]);
    expect(lu.paroles.length).toBeGreaterThan(0);
    for (const id of lu.paroles) {
      const d = lu.dalles.find((x) => x.pid === id);
      expect(d, `la dalle de la parole ${String(id)}`).toBeTruthy();
      expect(d!.x >= 0 && d!.x <= lu.W && d!.y >= 0 && d!.y <= lu.H, `la dalle ${String(id)} est dans l'écran`).toBe(
        true,
      );
    }
    // L'ACCUEIL S'ADAPTE (lot 1) : le plateau ancré en haut (40 pt sans zone sûre), la barre en bas (34 pt), tous deux aux marges de
    // 24 pt sur toute la largeur ; le + au centre de la barre ; les entrées à leur distance du bord le plus proche (46 et 100 pt) ;
    // aucun recouvrement entre le plateau et la barre ; à ½ pt près (une densité de 2,625 arrondit la place au pixel de l'appareil, 0,38 pt)
    const acc =
      (await page.evaluate(`(() => { const r = (id) => { const b = document.getElementById(id).getBoundingClientRect();
      return [b.left, b.top, b.right, b.bottom].map((v) => Math.round(v * 10) / 10); };
      return { plat: r('accPlat'), barre: r('accBarre'), plus: r('createBtn'), studio: r('studioBtn'), fil: r('filBtn') }; })()`)) as Record<
        string,
        [number, number, number, number]
      >;
    const W = e.viewport.width;
    const H = e.viewport.height;
    expect(acc['plat'], 'le plateau').toEqual([24, 40, W - 24, 100]);
    expect(acc['barre'], 'la barre').toEqual([24, H - 134, W - 24, H - 34]);
    expect((acc['plus']![0] + acc['plus']![2]) / 2, 'le + au centre').toBeCloseTo(W / 2, 0);
    expect((acc['studio']![0] + acc['studio']![2]) / 2, 'STUDIO à 70 pt du bord gauche').toBeCloseTo(70, 0);
    expect((acc['fil']![0] + acc['fil']![2]) / 2, 'FIL à 70 pt du bord droit').toBeCloseTo(W - 70, 0);
    expect(acc['plat']![3] < acc['barre']![1], 'le plateau au-dessus de la barre').toBe(true);
    await ctx.close();
  });
