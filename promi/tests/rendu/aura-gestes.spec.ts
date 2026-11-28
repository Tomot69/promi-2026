/**
 * LOT 6 — LES GESTES DE LA PELOTE, COMME LE PROTOTYPE (lot-AURA-PELOTE : `gestesBoule`, `lacher` ; les acquis de la sphère).
 *
 * Des deux côtés, l'Aura ouverte, « Réduire les animations » (la dérive arrêtée : seule la main fait tourner), et LES MÊMES ÉVÉNEMENTS (au même
 * point de l'appareil, en pt) :
 *  A · un glissé sur la Pelote : la vue tourne EXACTEMENT de la même quantité (la vue suit la main : 0,011 rad par px sur une boule de 142,
 *      rapporté à 116 pt) — à 1e-4 rad près ; la trace sous le doigt : autant de segments, de la même largeur (le contact du pouce, sans
 *      capteur), les mêmes bouts dans l'objet ;
 *  B · lâché en mouvement : un élan dans le sens du geste, des deux côtés (sa grandeur dépend de l'heure de chaque événement : jugée en signe) ;
 *  C · un appui immobile : la forme du contact, un segment de plus, de la même largeur ;
 *  D · le double toucher relisse : plus aucune trace.
 */
import { test, expect, type Page } from '@playwright/test';
import { deuxPilotes, images, sonde, stockageFiches, P_ } from './aides.ts';

type Vue = { lac: number; tan: number; vlac: number; vtan: number };
type Tr = { a: number[]; b: number[]; L: number; w: number; f: number };

const vue = async (pg: Page, app: boolean): Promise<Vue> =>
  (await pg.evaluate(
    app
      ? `(()=>{const v=${P_}.aura().pelote().vue;return {lac:v.lac,tan:v.tan,vlac:v.vlac,vtan:v.vtan};})()`
      : '(()=>{const e=window._aura.etat();return {lac:e.lac,tan:e.tan,vlac:e.vlac,vtan:e.vtan};})()',
  )) as Vue;
const traces = async (pg: Page, app: boolean): Promise<Tr[]> =>
  (await pg.evaluate(app ? `${P_}.aura().pelote().traces()` : 'window._aura.tracesGeo()')) as Tr[];

/** le point (en pt de l'appareil) en coordonnées de la page */
async function ecran(pg: Page, x: number, y: number): Promise<[number, number]> {
  const r = await pg.evaluate(() => {
    const b = document.getElementById('device')!.getBoundingClientRect();
    return { x: b.left, y: b.top, k: b.width / 390 };
  });
  return [r.x + x * r.k, r.y + y * r.k];
}
/** un glissé de (x0, y0) de (dx, dy) en n pas, le doigt levé ou non */
async function glisser(
  pg: Page,
  x0: number,
  y0: number,
  dx: number,
  dy: number,
  n: number,
  lever: boolean,
): Promise<void> {
  const [a, b] = await ecran(pg, x0, y0);
  const [c, d] = await ecran(pg, x0 + dx, y0 + dy);
  await pg.mouse.move(a, b);
  await pg.mouse.down();
  for (let i = 1; i <= n; i++) await pg.mouse.move(a + ((c - a) * i) / n, b + ((d - b) * i) / n);
  if (lever) await pg.mouse.up();
}

async function ouvrir(P: Page, A: Page): Promise<void> {
  for (const pg of [P, A]) await pg.emulateMedia({ reducedMotion: 'reduce' });
  await P.evaluate(() => (document.getElementById('souffleBtn') as HTMLElement).click());
  await A.evaluate(`${P_}.nav.ouvrir('aura')`);
  for (let k = 0; k < 6; k++) await Promise.all([images(P, 30), images(A, 30)]);
  // la même vue de départ, sans roulis
  await P.evaluate(() => {
    (window as unknown as { _aura: { vue(l: number, t: number): void } })._aura.vue(2.9, 0.32);
    const r = document.querySelector<HTMLElement>('#auraScreen .au-rot');
    if (r) r.style.transform = 'rotate(0deg)';
  });
  await A.evaluate(
    `(()=>{${P_}.aura().pelote().poserVue(2.9,0.32);document.querySelector('#auraScreen .au-rot').style.transform='rotate(0deg)';})()`,
  );
  await Promise.all([images(P, 4), images(A, 4)]);
}

test('les gestes de la Pelote : la prise, la trace sous le doigt, l’élan, l’appui, le double toucher (comme le prototype)', async ({
  browser,
}) => {
  test.setTimeout(180000);
  const { P, A, erreurs } = await deuxPilotes(browser, { ...stockageFiches(), promi_prenom: 'Tom' });
  try {
    await ouvrir(P, A);
    // la sonde : la Pelote sourde au doigt
    if (sonde('aura-sourde'))
      await A.evaluate(() =>
        document
          .querySelector('#auraScreen .au-prise')!
          .addEventListener('pointerdown', (e) => e.stopImmediatePropagation(), true),
      );
    // A · un glissé de 60 pt à droite et 20 pt vers le haut, en 12 pas, le doigt gardé posé (pas d'élan)
    const v0 = [await vue(P, false), await vue(A, true)];
    for (const pg of [P, A]) await glisser(pg, 170, 240, 60, -20, 12, false);
    await Promise.all([images(P, 6), images(A, 6)]);
    const v1 = [await vue(P, false), await vue(A, true)];
    const dP = [v1[0]!.lac - v0[0]!.lac, v1[0]!.tan - v0[0]!.tan];
    const dA = [v1[1]!.lac - v0[1]!.lac, v1[1]!.tan - v0[1]!.tan];
    expect(dP[0], 'le prototype tourne sous la main').toBeGreaterThan(0.1);
    expect(dA[0], 'la vue suit la main (lac)').toBeCloseTo(dP[0]!, 4);
    expect(dA[1], 'la vue suit la main (tan)').toBeCloseTo(dP[1]!, 4);
    const tP = await traces(P, false);
    const tA = await traces(A, true);
    expect(tA.length, 'autant de segments de trace sous le doigt').toBe(tP.length);
    expect(tP.length).toBeGreaterThan(0);
    tA.forEach((t, i) => {
      expect(t.w, `segment ${String(i)} : sa largeur`).toBeCloseTo(tP[i]!.w, 5);
      for (let k = 0; k < 3; k++) {
        expect(t.a[k], `segment ${String(i)} : son départ`).toBeCloseTo(tP[i]!.a[k]!, 4);
        expect(t.b[k], `segment ${String(i)} : son arrivée`).toBeCloseTo(tP[i]!.b[k]!, 4);
      }
    });
    // B · le doigt continue et lâche en mouvement : un élan dans le sens du geste
    for (const pg of [P, A]) {
      const [c, d] = await ecran(pg, 260, 210);
      await pg.mouse.move(c, d, { steps: 4 });
      await pg.mouse.up();
    }
    const v2 = [await vue(P, false), await vue(A, true)];
    expect(v2[0]!.vlac, 'le prototype lance').toBeGreaterThan(0);
    expect(v2[1]!.vlac, 'l’élan, dans le sens du geste').toBeGreaterThan(0);
    // l'élan s'éteint
    for (let k = 0; k < 8; k++) await Promise.all([images(P, 30), images(A, 30)]);
    // C · un appui immobile : la forme du contact
    const n0 = [(await traces(P, false)).length, (await traces(A, true)).length];
    for (const pg of [P, A]) {
      const [c, d] = await ecran(pg, 195, 260);
      await pg.mouse.move(c, d);
      await pg.mouse.down();
    }
    await Promise.all([images(P, 20), images(A, 20)]);
    for (const pg of [P, A]) await pg.mouse.up();
    await Promise.all([images(P, 4), images(A, 4)]);
    const tP2 = await traces(P, false);
    const tA2 = await traces(A, true);
    expect(tP2.length - n0[0]!, 'le prototype : un appui, un segment').toBe(1);
    expect(tA2.length - n0[1]!, 'un appui immobile laisse la forme du contact').toBe(1);
    expect(tA2.at(-1)!.w, 'sa largeur : le petit rayon du contact').toBeCloseTo(tP2.at(-1)!.w, 5);
    // D · le double toucher relisse — une seconde PILOTÉE d'abord : sous l'horloge pilotée, l'heure des événements n'avance qu'avec les images, et
    // l'appui de C tomberait à moins de 350 ms du premier toucher (un double toucher compté trop tôt)
    for (let k = 0; k < 2; k++) await Promise.all([images(P, 30), images(A, 30)]);
    for (const pg of [P, A]) {
      const [c, d] = await ecran(pg, 195, 260);
      await pg.mouse.click(c, d);
      await pg.mouse.click(c, d);
    }
    await Promise.all([images(P, 4), images(A, 4)]);
    expect((await traces(P, false)).length, 'le prototype relisse').toBe(0);
    expect((await traces(A, true)).length, 'le double toucher relisse').toBe(0);
    expect(erreurs).toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});
