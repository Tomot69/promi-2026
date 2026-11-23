/**
 * LOT 3a-2 — TENIR : LES JUGES DU GESTE ET DE SA SUITE, en tests (l'horloge PILOTÉE : chaque instant se lit en images, jamais en temps réel).
 *  redteam_trait            → « le seuil de 60 pt » (C-107), décisions comparées au prototype geste par geste
 *  redteam_retour_trait     → « lâché avant le seuil, le trait revient » (C-264), image par image, la suite du prototype
 *  redteam_ruban            → « le ruban amande naît du trait » (C-148) : sa place, sa couleur pleine, son épaisseur qui grandit en 200 ms
 *  redteam_tenir, redteam_centre_validation → « le rideau descend à vitesse constante » (C-118, C-144, C-167) : le front, la phrase centrée, la remontée
 *  redteam_tenir_presse     → « un toucher pendant que le vert est posé le fait remonter, et il est avalé » (C-167)
 *  redteam_tenir_e3         → « Réduire les animations : la fiche passe tenue d'un coup » (E3)
 *  redteam_part, redteam_validation (ma part) → « ma part, sans être la dernière : la vague seule, pas de rideau » (C-115, C-156)
 *  redteam_tenu_trait, banc_apres_tenir (les données) → « ce que tenir écrit » : comparé au prototype (C-189, C-226)
 *  redteam_premier_toucher  → « le premier toucher prend le trait » (C-263), cinq fiches de suite
 *  redteam_fluide           → « le moment tenir est fluide » (C-102) : jugé au calme seulement (C-137)
 * Chaque test a sa sonde (tests/rendu/sondes/tenir-juges.json) : il doit y rougir.
 */
import { test, expect, type Browser, type Page } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { loadavg } from 'node:os';
import { join } from 'node:path';
import { AMORCE_MINUTEURS, PILOTE, T_FIGE } from './banc.ts';
import { GEL, appareil, images, prototype, sonde, stockageFiches, tracerPilote, vraieApp, P_ } from './aides.ts';

type EtatTenir = {
  geste: boolean;
  atteint: boolean;
  doigt: number | null;
  ruban: boolean;
  rideau: null | { t0: number; v: number; monte: boolean };
  instant: null | string;
  dernier: null | { avance: number; ok: boolean };
};
const tenirA = (A: Page): Promise<EtatTenir> => A.evaluate(`${P_}.fiche().tenir()`) as Promise<EtatTenir>;

/** la vraie app pilotée, la fiche `id` ouverte et montée (60 images) ; `avant` : un script posé avant l'app (une sonde) */
async function app(browser: Browser, id: number, ls = stockageFiches(), avant?: string): Promise<Page> {
  const A = await (await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 })).newPage();
  if (avant) await A.addInitScript({ content: avant });
  await vraieApp(A, ls, T_FIGE);
  // les transitions CSS gelées : en temps piloté, la fiche qui monte (0,4 s RÉELLES) ne serait pas encore sous le doigt
  await A.addStyleTag({ content: GEL });
  await ouvrirA(A, id);
  return A;
}
async function ouvrirA(A: Page, id: number): Promise<void> {
  await A.evaluate(`${P_}.fiche().ouvrir(${String(id)})`);
  await images(A, 60);
}
/** le prototype, la fiche ouverte en temps réel, puis PILOTÉ (banc_rendu) */
async function proto(browser: Browser, id: number, ls = stockageFiches()): Promise<Page> {
  const P = await (await browser.newContext({ viewport: { width: 430, height: 932 }, deviceScaleFactor: 2 })).newPage();
  await P.addInitScript((a) => new Function(a)(), AMORCE_MINUTEURS);
  await prototype(P, ls);
  await P.evaluate((id) => (window as unknown as { openDetail(i: number): void }).openDetail(id), id);
  await P.waitForTimeout(1600);
  await P.evaluate(`(${PILOTE})()`);
  return P;
}
const fermer = async (...L: Page[]): Promise<void> => {
  await Promise.all(L.map((p) => p.context().close()));
};
/** « Réduire les animations » posé en douce (la sonde des changements secs, comme au lot 2) */
const SEC = `(() => { const m = window.matchMedia.bind(window); window.matchMedia = (q) => /reduced-motion/.test(q) ? { matches: true, media: q, addEventListener() {}, removeEventListener() {}, addListener() {}, removeListener() {} } : m(q); })();`;

/** le doigt posé en (x, y) de l'appareil, levé après `n` images (rien ne bouge) */
async function pose(pg: Page, x: number, y: number, n: number): Promise<void> {
  const d = await appareil(pg);
  const k = d.width / 390;
  await pg.mouse.move(d.x + x * k, d.y + y * k);
  await pg.mouse.down();
  await images(pg, n);
  await pg.mouse.up();
}
/** un geste rapide, sans attendre l'ouverture : `pas` mouvements, une image chacun */
async function vif(pg: Page, x0: number, x1: number, pas: number): Promise<void> {
  const d = await appareil(pg);
  const k = d.width / 390;
  await pg.mouse.move(d.x + x0 * k, d.y + 303 * k);
  await pg.mouse.down();
  for (let i = 1; i <= pas; i++) {
    await pg.mouse.move(d.x + (x0 + ((x1 - x0) * i) / pas) * k, d.y + 303 * k);
    await images(pg, 1);
  }
  await pg.mouse.up();
}

test('le seuil de 60 pt : les décisions de la vraie app sont celles du prototype, geste par geste (C-107)', async ({
  browser,
}) => {
  // la sonde (tenir-seuil) : la zone mesurée deux fois trop étroite — chaque avancée compte double, 30 pt passent
  const avant = sonde('tenir-seuil')
    ? `(() => { const g = Element.prototype.getBoundingClientRect; Element.prototype.getBoundingClientRect = function () { const r = g.call(this); return this.id === 'tenirZone' ? new DOMRect(r.left, r.top, r.width / 2, r.height) : r; }; })();`
    : undefined;
  const [A, P] = await Promise.all([app(browser, 144, stockageFiches(), avant), proto(browser, 144)]);
  try {
    const lit = async (): Promise<[boolean | null, boolean | null]> => [
      (await tenirA(A)).dernier?.ok ?? null,
      ((await P.evaluate('window._traitDernier')) as { ok: boolean } | null)?.ok ?? null,
    ];
    const D: Record<string, [boolean | null, boolean | null]> = {};
    // 30 pt, lentement : refusé
    for (const pg of [A, P]) await tracerPilote(pg, 150, 180, 20);
    D['30 pt'] = await lit();
    // le doigt posé 800 ms sans bouger : refusé
    for (const pg of [A, P]) await pose(pg, 150, 303, 48);
    D['posé'] = await lit();
    // un départ au-delà de la première moitié (x 260) : la zone ne s'ouvre pas
    const ouvert = async (pg: Page): Promise<boolean> => {
      const d = await appareil(pg);
      const k = d.width / 390;
      await pg.mouse.move(d.x + 260 * k, d.y + 303 * k);
      await pg.mouse.down();
      const o = await pg.evaluate(() => !!document.querySelector('#tenirZone.ouvert'));
      await pg.mouse.up();
      return o;
    };
    D['départ à 260'] = [await ouvert(A), await ouvert(P)] as [boolean, boolean];
    // 70 pt après l'ouverture : tenu
    for (const pg of [A, P]) await tracerPilote(pg, 150, 220, 30);
    D['70 pt'] = await lit();
    expect(D).toEqual({
      '30 pt': [false, false],
      posé: [false, false],
      'départ à 260': [false, false],
      '70 pt': [true, true],
    });
    // un geste lâché dans les 340 premières ms (l'ouverture de la zone) ne compte pas, quelle que soit sa longueur : 210 pt en 200 ms (la vraie
    // app, pilotée ; le prototype fait de même en temps réel — écrit à Tom, QUESTIONS)
    const B = await app(browser, 148);
    try {
      await vif(B, 150, 360, 12);
      expect((await tenirA(B)).dernier).toEqual({ avance: 0, ok: false });
    } finally {
      await fermer(B);
    }
  } finally {
    await fermer(A, P);
  }
});

test('lâché avant le seuil, le trait revient à la pointe : image par image, la suite du prototype (C-264, 300 ms)', async ({
  browser,
}) => {
  const [A, P] = await Promise.all([app(browser, 144), proto(browser, 144)]);
  try {
    // la sonde (tenir-retour-sec) : l'horloge de la vraie app file trois fois plus vite dès le lever — le trait revient en un éclair
    const R: Record<string, { app: number[]; proto: number[] }> = {};
    for (const [x0, x1] of [
      [180, 205],
      [180, 224],
      [200, 250],
    ] as const) {
      for (const pg of [A, P]) {
        const d = await appareil(pg);
        const k = d.width / 390;
        await pg.mouse.move(d.x + x0 * k, d.y + 303 * k);
        await pg.mouse.down();
        await pg.waitForFunction(() => !!document.querySelector('#tenirZone.ouvert'));
        await pg.waitForTimeout(400);
        await images(pg, 25);
        for (let i = 1; i <= 10; i++) {
          await pg.mouse.move(d.x + (x0 + ((x1 - x0) * i) / 10) * k, d.y + 303 * k);
          await images(pg, 1);
        }
      }
      if (sonde('tenir-retour-sec'))
        await A.evaluate(
          `(() => { const H = ${P_}.horloge, m = H.maintenant.bind(H), t0 = m(); H.maintenant = () => t0 + (m() - t0) * 3; })()`,
        );
      const suite = async (pg: Page, lire: string): Promise<number[]> => {
        await pg.mouse.up();
        const L: number[] = [];
        for (let i = 0; i < 22; i++) {
          L.push(Math.round((((await pg.evaluate(lire)) as number | null) ?? 195) * 10) / 10);
          await images(pg, 1);
        }
        return L;
      };
      R[`${String(x0)} → ${String(x1)}`] = {
        app: await suite(A, `${P_}.fiche().tenir().doigt`),
        proto: await suite(P, 'window._ficheDoigt'),
      };
    }
    for (const [k, v] of Object.entries(R))
      expect(
        v.app.map((x, i) => Math.abs(x - v.proto[i]!) <= 0.5),
        `${k} : ${JSON.stringify(v)}`,
      ).not.toContain(false);
  } finally {
    await fermer(A, P);
  }
});

/** l'épaisseur peinte du ruban, au milieu (x 195), en pt — lue sur son canevas */
const epaisseurRuban = (A: Page): Promise<number> =>
  A.evaluate(() => {
    const cv = document.getElementById('tenirRuban') as HTMLCanvasElement | null;
    if (!cv) return -1;
    const k = cv.width / 390;
    const x = Math.round(195 * k);
    const d = cv.getContext('2d')!.getImageData(x, 0, 1, cv.height).data;
    let n = 0;
    for (let i = 0; i < cv.height; i++) if (d[i * 4 + 3]! > 128) n++;
    return n / k;
  });

test('le ruban amande naît du trait au seuil : sa place, sa couleur pleine, son épaisseur qui grandit en 200 ms (C-148)', async ({
  browser,
}) => {
  // la sonde (tenir-ruban-sec) : « Réduire les animations » posé en douce — le ruban paraît d'un coup
  const A = await app(browser, 144, stockageFiches(), sonde('tenir-ruban-sec') ? SEC : undefined);
  try {
    const d = await appareil(A);
    await A.mouse.move(d.x + 150, d.y + 303);
    await A.mouse.down();
    await A.waitForFunction(() => !!document.querySelector('#tenirZone.ouvert'));
    await images(A, 25);
    // jusqu'au seuil (60 pt), puis on lit chaque image
    let x = 150;
    while (!(await tenirA(A)).atteint && x < 240) {
      x += 5;
      await A.mouse.move(d.x + x, d.y + 303);
      await images(A, 1);
    }
    const E: number[] = [await epaisseurRuban(A)];
    for (let i = 0; i < 14; i++) {
      await images(A, 1);
      E.push(await epaisseurRuban(A));
    }
    // sa place et sa couleur, une fois né (le milieu de sa bande, sur l'axe du trait à x 195)
    const place = await A.evaluate(() => {
      const cv = document.getElementById('tenirRuban') as HTMLCanvasElement | null;
      if (!cv) return null;
      const k = cv.width / 390;
      const d = cv.getContext('2d')!.getImageData(Math.round(195 * k), 0, 1, cv.height).data;
      let a = -1;
      let b = -1;
      for (let i = 0; i < cv.height; i++)
        if (d[i * 4 + 3]! > 128) {
          if (a < 0) a = i;
          b = i;
        }
      const m = Math.round((a + b) / 2) * 4;
      return { top: cv.style.top, h: cv.style.height, couleur: [d[m], d[m + 1], d[m + 2], d[m + 3]] };
    });
    await A.mouse.up();
    // la place (base 286, amplitude 36 : y0 = ⌊286 − 36 − 49⌋, h = ⌈72 + 106⌉), au-dessus de tout le corps de la fiche
    expect(place?.top).toBe('201px');
    expect(place?.h).toBe('178px');
    // la couleur : l'amande pleine, sans transparence (A2)
    expect(place?.couleur).toEqual([143, 224, 143, 255]);
    // l'épaisseur au milieu : 94 pt au bout (± les bords qui ondulent), partie de presque rien, sans jamais reculer, en 200 ms (12 images)
    expect(E[0], JSON.stringify(E)).toBeLessThan(40);
    expect(E[12]!, JSON.stringify(E)).toBeGreaterThan(88);
    expect(
      E.every((v, i) => i === 0 || v >= E[i - 1]! - 0.5),
      JSON.stringify(E),
    ).toBe(true);
  } finally {
    await fermer(A);
  }
});

/** le front du rideau à x 195 (le dernier pixel amande de la colonne, en pt) et l'encre de la phrase (sa boîte), lus sur #tenirMaree */
const lireRideau = (A: Page): Promise<null | { front: number; encre: number[] | null }> =>
  A.evaluate(() => {
    const cv = document.getElementById('tenirMaree') as HTMLCanvasElement | null;
    if (!cv) return null;
    const k = cv.width / 390;
    const g = cv.getContext('2d')!;
    const col = g.getImageData(Math.round(60 * k), 0, 1, cv.height).data;
    let front = -1;
    for (let i = 0; i < cv.height; i++) if (col[i * 4 + 3]! > 128) front = i / k;
    const y0 = Math.round(380 * k);
    const h = Math.round(60 * k);
    const z = g.getImageData(0, y0, cv.width, h).data;
    let x0 = 1e9;
    let x1 = -1;
    for (let j = 0; j < h; j++)
      for (let i = 0; i < cv.width; i++) {
        const q = (j * cv.width + i) * 4;
        if (z[q + 3]! > 200 && z[q]! < 80 && z[q + 1]! < 80) {
          x0 = Math.min(x0, i);
          x1 = Math.max(x1, i);
        }
      }
    return { front, encre: x1 > 0 ? [x0 / k, x1 / k] : null };
  });

test('le rideau descend à vitesse constante jusqu’à la barre, « Parole tenue ! » centrée, et remonte à 2 150 ms (C-118, C-144, C-167)', async ({
  browser,
}) => {
  const A = await app(browser, 144);
  try {
    await tracerPilote(A, 150, 360, 30);
    // la sonde (tenir-rideau-vite) : l'horloge file deux fois plus vite dès le lever — le rideau tombe en 350 ms
    if (sonde('tenir-rideau-vite'))
      await A.evaluate(
        `(() => { const H = ${P_}.horloge, m = H.maintenant.bind(H), t0 = m(); H.maintenant = () => t0 + (m() - t0) * 2; })()`,
      );
    const F: number[] = [];
    for (let i = 0; i < 44; i++) {
      F.push((await lireRideau(A))?.front ?? -1);
      await images(A, 1);
    }
    // descente : le front ne recule jamais ; à mi-course (21 images, 350 ms) il est à mi-chemin (± 30 pt) ; à 700 ms il atteint la barre (760)
    expect(
      F.every((v, i) => i === 0 || v >= F[i - 1]! - 0.5),
      JSON.stringify(F),
    ).toBe(true);
    // à vitesse constante : passé le premier quart (où le front perd la forme du ruban, C-156), chaque image le fait descendre du même pas
    // (± 1,5 pt de la médiane) ; il atteint la barre (760) à 700 ms (42 images), pas avant 36
    const P = F.slice(12, 40).map((v, i) => v - F[11 + i]!);
    const med = [...P].sort((a, b) => a - b)[P.length >> 1]!;
    expect(
      P.every((d) => Math.abs(d - med) <= 1.5),
      JSON.stringify(F),
    ).toBe(true);
    expect(F[36]!, JSON.stringify(F)).toBeLessThan(745);
    expect(F[43]!, JSON.stringify(F)).toBeGreaterThanOrEqual(759);
    // la phrase : à l'encre, centrée à 195 (± 1)
    const r = await lireRideau(A);
    expect(r?.encre, 'la phrase est peinte dans le rideau').not.toBeNull();
    expect(Math.abs((r!.encre![0]! + r!.encre![1]!) / 2 - 195)).toBeLessThanOrEqual(1);
    // posé jusqu'à 2 150 ms (129 images), puis il remonte et part (560 ms)
    await images(A, 128 - 44);
    expect((await tenirA(A)).rideau?.monte).toBe(false);
    await images(A, 3);
    expect((await tenirA(A)).rideau?.monte).toBe(true);
    expect((await tenirA(A)).instant).toBe('apres');
    await images(A, 36);
    expect((await tenirA(A)).rideau).toBeNull();
    expect(await A.evaluate(() => !!document.getElementById('tenirMaree'))).toBe(false);
  } finally {
    await fermer(A);
  }
});

test('un toucher pendant que le vert est posé le fait remonter tout de suite, et il est avalé : la fiche reste ouverte (C-167)', async ({
  browser,
}) => {
  const A = await app(browser, 144);
  try {
    // la sonde (tenir-presse-perce) : le toucher traverse jusqu'au X — la fiche se ferme
    if (sonde('tenir-presse-perce'))
      await A.evaluate(
        `window.addEventListener('pointerup', () => { if (${P_}.fiche().tenir().rideau) ${P_}.fiche().fermer(); }, true)`,
      );
    await tracerPilote(A, 150, 360, 30);
    // à 100 ms (6 images), un toucher ne presse rien (il n'est lu qu'à partir de 300 ms)
    await images(A, 6);
    await pose(A, 195, 600, 1);
    expect((await tenirA(A)).rideau?.monte).toBe(false);
    // à 1,3 s, un toucher sur le X : le vert remonte tout de suite, la fiche reste ouverte
    await images(A, 70);
    const x = await A.evaluate(() => {
      const r = document.querySelector('#detailPoster .closeb')!.getBoundingClientRect();
      return [r.left + r.width / 2, r.top + r.height / 2];
    });
    await pose(A, x[0]!, x[1]!, 1);
    await images(A, 2);
    const e = await tenirA(A);
    expect(e.rideau?.monte).toBe(true);
    expect(e.instant).toBe('apres');
    await images(A, 40);
    expect((await A.evaluate(`${P_}.fiche().etat()`)) as { id: number | null }).toMatchObject({ id: 144 });
    expect(await A.evaluate(() => !document.getElementById('detailPoster')!.classList.contains('fi-bas'))).toBe(true);
  } finally {
    await fermer(A);
  }
});

test('« Réduire les animations » : la fiche passe tenue d’un coup, ni rideau ni instant (E3)', async ({ browser }) => {
  const ctx = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    reducedMotion: 'reduce',
  });
  const A = await ctx.newPage();
  // la sonde (tenir-reduit-anime) : le réglage du téléphone n'est pas lu — le rideau joue quand même
  if (sonde('tenir-reduit-anime'))
    await A.addInitScript({
      content: `(() => { const m = window.matchMedia.bind(window); window.matchMedia = (q) => /reduced-motion/.test(q) ? { matches: false, media: q, addEventListener() {}, removeEventListener() {}, addListener() {}, removeListener() {} } : m(q); })();`,
    });
  try {
    await vraieApp(A, stockageFiches(), T_FIGE);
    await A.addStyleTag({ content: GEL });
    await ouvrirA(A, 144);
    await tracerPilote(A, 150, 360, 30);
    let rideau = false;
    for (let i = 0; i < 30; i++) {
      rideau ||= await A.evaluate(() => !!document.getElementById('tenirMaree'));
      await images(A, 1);
    }
    expect(rideau).toBe(false);
    expect(await A.evaluate(`${P_}.fiche().etat()`)).toMatchObject({ instant: null, base: 362, mode: 'complet' });
    expect(await A.evaluate(() => document.querySelector('#detailPoster .fi-trait')!.getAttribute('data-trait'))).toBe(
      '362,36,#0B4A2A,complet',
    );
  } finally {
    await ctx.close();
  }
});

test('ma part, sans être la dernière : la vague seule sous le trait, pas de rideau, la parole reste en cours (C-115, C-156)', async ({
  browser,
}) => {
  // un Chiche reçu de Marion, avec Lou : ma part et celle de Lou
  const ls = stockageFiches();
  const st = JSON.parse(ls['promi_state']!) as { promises: Array<Record<string, unknown>> };
  const p157 = st.promises.find((p) => p['id'] === 157)!;
  p157['avec'] = 'Lou';
  ls['promi_state'] = JSON.stringify(st);
  const A = await app(browser, 157, ls);
  try {
    // la sonde (tenir-part-rideau) : la part prise pour la dernière — le rideau part
    if (sonde('tenir-part-rideau'))
      await A.evaluate(
        `(() => { const M = ${P_}.magasin, t = M.tenir.bind(M); M.tenir = (...a) => { t(...a); return 'tenue'; }; })()`,
      );
    const fil0 = (await A.evaluate(`${P_}.magasin.etat().fil.length`)) as number;
    await tracerPilote(A, 150, 360, 30);
    let rideau = false;
    let ruban = 0;
    for (let i = 0; i < 60; i++) {
      rideau ||= await A.evaluate(() => !!document.getElementById('tenirMaree'));
      if ((await tenirA(A)).ruban) ruban = i + 1;
      await images(A, 1);
    }
    const p = (await A.evaluate(`${P_}.magasin.etat().paroles.find((q) => q.id === 157)`)) as {
      status: string;
      parts?: Record<string, string>;
    };
    expect(rideau).toBe(false);
    // le ruban tient 520 ms puis se resserre en 320 ms : il part à ≈ 840 ms (50 à 52 images)
    expect(ruban).toBeGreaterThanOrEqual(49);
    expect(ruban).toBeLessThanOrEqual(53);
    expect(p.status).toBe('encours');
    expect(Object.keys(p.parts ?? {})).toEqual(['moi']);
    expect(await A.evaluate(() => document.getElementById('dptTrace')!.textContent)).toBe('à Lou de tracer sa part');
    expect(await A.evaluate(`${P_}.magasin.etat().fil.length`)).toBe(fil0);
  } finally {
    await fermer(A);
  }
});

test('ce que tenir écrit : la parole tenue, son trait, « vue tenue », la ligne du Fil — comme le prototype (C-189, C-226)', async ({
  browser,
}) => {
  const [A, P] = await Promise.all([app(browser, 144), proto(browser, 144)]);
  try {
    // la sonde (tenir-donnees) : le trait du geste n'est pas gardé
    if (sonde('tenir-donnees'))
      await A.evaluate(
        `(() => { const M = ${P_}.magasin, t = M.tenir.bind(M); M.tenir = (id, tr, m) => t(id, [], m); })()`,
      );
    for (const pg of [A, P]) await tracerPilote(pg, 150, 360, 30);
    await images(A, 5);
    await images(P, 5);
    const a = (await A.evaluate(`(() => { const e = ${P_}.magasin.etat(); const p = e.paroles.find((q) => q.id === 144);
      return { status: p.status, trace: (p.suite && p.suite.trace || []).length, vu: Object.keys(p.vuTenue || {}), fil: [e.fil[0].type, e.fil[0].text, e.fil[0].pid, e.fil[0].t, e.fil[0].unread] }; })()`)) as Record<
      string,
      unknown
    >;
    const q = (await P.evaluate(`(() => { const p = promises.find((x) => x.id === 144);
      return { status: p.status, trace: (p.trace || []).length, vu: Object.keys(p.vuTenue || {}), fil: [FEED[0].type, FEED[0].text, FEED[0].pid, FEED[0].t, FEED[0].unread] }; })()`)) as Record<
      string,
      unknown
    >;
    expect(a['trace'], 'le trait est gardé').toBeGreaterThan(5);
    expect(q['trace']).toBeGreaterThan(5);
    expect({ ...a, trace: a['trace'] ? 'gardé' : 'perdu' }).toEqual({ ...q, trace: q['trace'] ? 'gardé' : 'perdu' });
    // une parole ne se tient que par le trait (C-189) : la vraie app n'écrit « tenu » qu'en un endroit, l'action `tenir` du magasin, appelée par
    // le geste de la fiche
    const src = (f: string): string => readFileSync(join(import.meta.dirname, '..', '..', 'src', f), 'utf8');
    expect(src('etat/magasin.ts').match(/status: 'tenu'/g)?.length).toBe(1);
    expect(src('ecrans/fiche/fiche.ts')).toContain('magasin.tenir(');
  } finally {
    await fermer(A, P);
  }
});

test('le premier toucher prend le trait : cinq fiches de suite, chacune tenue du premier geste (C-263)', async ({
  browser,
}) => {
  const A = await app(browser, 144);
  try {
    // la sonde (tenir-premier-perdu) : la zone ne prend pas le doigt
    if (sonde('tenir-premier-perdu'))
      await A.addStyleTag({ content: '#detailPoster #tenirZone{pointer-events:none!important}' });
    const ok: Record<string, string> = {};
    for (const id of [144, 148, 147, 162, 160]) {
      await A.evaluate(`${P_}.fiche().fermer()`);
      await images(A, 30);
      await ouvrirA(A, id);
      await tracerPilote(A, 150, 360, 30).catch(() => undefined);
      await images(A, 4);
      ok[String(id)] = (await A.evaluate(
        `${P_}.magasin.etat().paroles.find((q) => q.id === ${String(id)}).status`,
      )) as string;
    }
    expect(ok).toEqual({ '144': 'tenu', '148': 'tenu', '147': 'tenu', '162': 'tenu', '160': 'tenu' });
  } finally {
    await fermer(A);
  }
});

test('le moment « tenir » est fluide : le travail de chaque image du rideau tient dans une image (C-102, v124 ; jugé au calme, C-137)', async ({
  browser,
}) => {
  // C-137 : une cadence ne se juge qu'au calme (la charge du Mac sous 4) — au-delà, « non jugé », écrit dans le rapport du test
  // (la sonde, elle, se joue toujours : 40 ms par image rougissent à toute charge)
  test.skip(
    !sonde('tenir-lourd') && loadavg()[0]! >= 4,
    `non jugé : la charge est à ${loadavg()[0]!.toFixed(1)} (C-137, au calme seulement)`,
  );
  const A = await app(browser, 144);
  try {
    // la sonde (tenir-lourd) : 40 ms de calcul ajoutées à chaque image (le travail de tout le document dans l'image, le défaut de v124)
    if (sonde('tenir-lourd'))
      await A.evaluate(
        `(() => { const H = ${P_}.horloge, im = H.image.bind(H); H.image = (cb) => im((t) => { const f = Date.now() + 40; while (Date.now() < f); cb(t); }); })()`,
      );
    await tracerPilote(A, 150, 360, 30);
    // le travail d'une image de l'horloge, en temps réel (`Date.now` : l'horloge pilotée ne compte pas le temps de calcul), sur tout le moment
    const T = (await A.evaluate(
      `(() => { const L = []; for (let i = 0; i < 170; i++) { const t = Date.now(); ${P_}.horloge.images(1); L.push(Date.now() - t); } return L; })()`,
    )) as number[];
    const tri = [...T].sort((a, b) => a - b);
    expect(tri[Math.floor(tri.length * 0.95)]!, JSON.stringify(T)).toBeLessThanOrEqual(16);
    expect(tri[tri.length - 1]!, JSON.stringify(T)).toBeLessThanOrEqual(33);
  } finally {
    await fermer(A);
  }
});
