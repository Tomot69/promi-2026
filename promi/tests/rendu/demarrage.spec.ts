/**
 * L0 §0 c — L'APP DÉMARRE AVEC LES DONNÉES IMPORTÉES. Au premier lancement (stockage vide), l'app importe l'état embarqué
 * (src/donnees/etat-embarque.json) et le donne au moteur : toutes ses paroles, son monde, sa palette. Échoue si la construction n'embarque
 * rien, si l'import n'a pas lieu, ou si une parole manque. (Le défaut que Tom a vu le 20 nov. : une Toile sans ses paroles.)
 */
import { test, expect } from '@playwright/test';
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const EMBARQUE = join(import.meta.dirname, '..', '..', 'src', 'donnees', 'etat-embarque.json');

test("au premier lancement, l'app montre les paroles de l'état embarqué, toutes", async ({ page }) => {
  expect(existsSync(EMBARQUE), 'aucun état embarqué dans la construction (npm run embarquer)').toBe(true);
  const x = JSON.parse(readFileSync(EMBARQUE, 'utf8')) as { ls?: Record<string, string> } & Record<string, string>;
  const ls = x.ls ?? x;
  const st = JSON.parse(ls['promi_state']!) as { promises: Array<{ id: number; title: string; draft?: boolean }> };
  const studio = ls['promi_studio'] ? (JSON.parse(ls['promi_studio']) as { m: string; p: string }) : null;
  expect(st.promises.length, "l'état embarqué porte au moins une parole").toBeGreaterThan(0);
  const erreurs: string[] = [];
  page.on('pageerror', (e) => erreurs.push(String(e)));
  await page.goto('http://127.0.0.1:5180/');
  await page.waitForFunction(() => {
    const w = window as unknown as { Toile_graines?: () => unknown[] };
    return !!w.Toile_graines && w.Toile_graines().length > 0;
  });
  const lu = (await page.evaluate(`({
    paroles: promises.map(p=>[p.id,p.title]),
    dalles: Toile_graines().filter(g=>g[3]!=='gray').map(g=>g[0]),
    monde: Toile.getTheme(), palette: Toile.getPalette() })`)) as {
    paroles: Array<[number, string]>;
    dalles: number[];
    monde: string;
    palette: string;
  };
  expect(erreurs).toEqual([]);
  expect(lu.paroles).toEqual(st.promises.map((p) => [p.id, p.title]));
  for (const p of st.promises.filter((q) => !q.draft)) expect(lu.dalles, `la dalle de « ${p.title} »`).toContain(p.id);
  if (studio) expect([lu.monde, lu.palette]).toEqual([studio.m, studio.p]);
});

/**
 * LE GLISSÉ DÉPLACE LA VUE, COMME DANS LE PROTOTYPE (Tom, 20 nov. 2026 : le glissé qui changeait de monde ne servait qu'à la preuve de
 * L0, il est retiré ; le monde se change au Studio, lot 7). Le doigt est posé et levé SUR LE CANEVAS DU MOTEUR (qui arrête la propagation
 * de `pointerdown`) : le monde ne change pas, la vue appartient à la main.
 */
test('le glissé horizontal déplace la vue et ne change jamais de monde', async ({ page }) => {
  await page.goto('http://127.0.0.1:5180/');
  await page.waitForFunction(() => !!(window as unknown as { Toile?: unknown }).Toile);
  const glisser = (dx: number, dy: number): Promise<string> =>
    page.evaluate(
      async ([dx, dy]) => {
        const cv = document.getElementById('toileCv')!;
        const o = {
          pointerId: 7,
          pointerType: 'touch',
          isPrimary: true,
          bubbles: true,
          cancelable: true,
          composed: true,
        };
        cv.dispatchEvent(new PointerEvent('pointerdown', { ...o, clientX: 200, clientY: 400 }));
        for (let k = 1; k <= 6; k++)
          cv.dispatchEvent(
            new PointerEvent('pointermove', { ...o, clientX: 200 + (dx * k) / 6, clientY: 400 + (dy * k) / 6 }),
          );
        cv.dispatchEvent(new PointerEvent('pointerup', { ...o, clientX: 200 + dx, clientY: 400 + dy }));
        await new Promise((r) => requestAnimationFrame(r));
        return (window as unknown as { Toile: { getTheme(): string } }).Toile.getTheme();
      },
      [dx, dy] as const,
    );
  const m0 = (await page.evaluate('Toile.getTheme()')) as string;
  expect(await glisser(-150, 10)).toBe(m0);
  expect(await glisser(150, -10)).toBe(m0);
  expect(await page.evaluate('!!window._vueMain'), 'la vue appartient à la main').toBe(true);
});

/** L0 §0 a — une app qui garde l'état d'une construction précédente (l'iPhone de Tom, le 20 nov.) prend le nouvel export embarqué. */
test('une app déjà lancée prend le nouvel export embarqué', async ({ page }) => {
  const x = JSON.parse(readFileSync(EMBARQUE, 'utf8')) as { ls?: Record<string, string> } & Record<string, string>;
  const st = JSON.parse((x.ls ?? x)['promi_state']!) as { promises: Array<{ id: number; title: string }> };
  await page.addInitScript(() => {
    if (sessionStorage.getItem('__pose')) return;
    sessionStorage.setItem('__pose', '1');
    localStorage.setItem('promi.l0.embarque', '1:ancien');
    localStorage.setItem(
      'promi.etat.v1',
      JSON.stringify({
        schema: 1,
        paroles: [
          {
            id: 1,
            title: 'ancienne',
            who: 'moi',
            due: 0,
            intensity: 1,
            status: 'encours',
            from: 'moi',
            recur: null,
            remind: null,
            x: 0,
            y: 0,
            tx: 0,
            ty: 0,
          },
        ],
        effacees: [],
        cercles: {},
        membres: {},
        dallesCercles: {},
        placesCercles: {},
        personnes: [],
        fil: [],
        filReactions: {},
        partageMasque: {},
        reglages: { theme: 'clair', labels: true, tri: 'inspi', humeur: 'cobalt', notifOn: false },
        studio: { monde: 'encre', palette: 'signal', teinte: 0, acquis: {} },
        utilisateur: { prenom: null, graine: 1 },
        compteurs: { nid: 2, fid: 1 },
        autres: {},
      }),
    );
  });
  await page.goto('http://127.0.0.1:5180/');
  await page.waitForFunction(() => !!(window as unknown as { Toile_graines?: unknown }).Toile_graines);
  expect(await page.evaluate('promises.map(p=>[p.id,p.title])')).toEqual(st.promises.map((p) => [p.id, p.title]));
});
