/**
 * LOT 5 — PEAUFINER D'UN CERCLE, AU DOIGT (redteam_peauf_rangees C-192, redteam_cercle_plus_membres C-242, redteam_nuee) — la vraie app seule
 * (le prototype : identité au pixel dans cercle-gestes.spec.ts) :
 *  · DISSOUDRE LE CERCLE : la feuille ; « Garder » ne fait rien ; « Dissoudre » : le Cercle part, ses paroles restent hors de lui, la fiche se
 *    ferme, « « Marseille » dissous » ; « Annuler » le rend, ses paroles y reviennent ;
 *  · MEMBRES : déplié, la croix d'une personne la retire, une personne connue s'ajoute ; la ligne « Avec … » de la fiche suit ;
 *  · le « + » des membres de la fiche ouvre Peaufiner sur MEMBRES déplié ;
 *  · DESCRIPTION : écrite, elle est gardée (le prototype la perdait au rechargement : schéma v3) ; aucun emoji (C-129).
 */
import { test, expect, type Page } from '@playwright/test';
import { vraieApp, sonde, stockageCercles, P_ } from './aides.ts';

type Etat = {
  cercles: Record<string, string>;
  membres: Record<string, string[]>;
  infosCercles: Record<string, { note?: string }>;
  paroles: Array<{ id: number; nuee?: string | null }>;
};
const etat = (pg: Page): Promise<Etat> => pg.evaluate(`${P_}.magasin.etat()`) as Promise<Etat>;

async function toucherEl(pg: Page, sel: string, mot = ''): Promise<void> {
  const c = await pg.evaluate(
    ([sel, mot]) => {
      const e = [...document.querySelectorAll<HTMLElement>(sel!)].find((x) =>
        (x.textContent ?? '').trim().startsWith(mot!),
      );
      if (!e) return null;
      e.scrollIntoView({ block: 'center' });
      const b = e.getBoundingClientRect();
      return [b.left + b.width / 2, b.top + b.height / 2];
    },
    [sel, mot],
  );
  if (!c) throw new Error(`introuvable : ${sel} « ${mot} »`);
  await pg.mouse.click(c[0]!, c[1]!);
  await pg.waitForTimeout(450);
}
async function ouvrirCercle(pg: Page): Promise<void> {
  await pg.evaluate(`${P_}.fiche().ouvrirCercle('n1')`);
  await pg.waitForFunction(() => {
    const f = document.getElementById('detailPoster');
    return (
      !!f && !f.hidden && !f.classList.contains('fi-bas') && f.getAnimations().every((a) => a.playState !== 'running')
    );
  });
  await pg.waitForTimeout(300);
}
async function ouvrirPeauf(pg: Page): Promise<void> {
  await toucherEl(pg, '#dpdTog');
  await pg.waitForFunction(() => !!document.querySelector('#dpdCorps #npMemb'));
  await pg.waitForTimeout(500);
}
const avec = (pg: Page): Promise<string> => pg.evaluate(() => document.getElementById('dptQui')?.textContent ?? '');

test('DISSOUDRE LE CERCLE : « Garder » ne fait rien ; « Dissoudre » : ses paroles restent hors de lui, la fiche se ferme ; « Annuler » le rend (C-192)', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, { ...stockageCercles(), promi_prenom: 'Tom' });
  // la sonde : « Dissoudre » emporte aussi les paroles du Cercle
  if (sonde('dissoudre-emporte'))
    await page.evaluate(`(() => { const m = ${P_}.magasin; const f = m.dissoudre.bind(m);
      m.dissoudre = (k) => { const ids = m.etat().paroles.filter((q) => q.nuee === k).map((q) => q.id); const r = f(k); for (const i of ids) m.effacer(i); return r; }; })()`);
  await ouvrirCercle(page);
  await ouvrirPeauf(page);
  await toucherEl(page, '#npDiss');
  expect(await page.locator('#v16Conf .v16-conf-t').textContent(), 'la feuille').toBe('Dissoudre « Marseille » ?');
  await toucherEl(page, '#v16Conf button', 'Garder');
  await page.waitForTimeout(500);
  expect((await etat(page)).cercles['n1'], '« Garder » : le Cercle est là').toBe('Marseille');
  await page.waitForFunction(() => !document.getElementById('v16Conf'), undefined, { timeout: 3000 });
  await toucherEl(page, '#npDiss');
  await toucherEl(page, '#v16Conf button', 'Dissoudre');
  await page.waitForTimeout(600);
  const e = await etat(page);
  expect(e.cercles['n1'], 'le Cercle est parti').toBeUndefined();
  expect(
    [144, 146, 147, 152, 169].map((id) => e.paroles.find((q) => q.id === id)?.nuee ?? null),
    'ses paroles restent, hors du Cercle',
  ).toEqual([null, null, null, null, null]);
  expect(
    await page.evaluate(() => document.getElementById('detailPoster')!.classList.contains('fi-bas')),
    'la fiche se ferme',
  ).toBe(true);
  expect(await page.locator('#v16Toast span').textContent(), 'le bandeau').toBe('« Marseille » dissous');
  await toucherEl(page, '#v16Toast button', 'Annuler');
  await page.waitForTimeout(500);
  const e2 = await etat(page);
  expect([e2.cercles['n1'], e2.membres['n1']], '« Annuler » : le Cercle revient').toEqual([
    'Marseille',
    ['Rachel', 'Marion'],
  ]);
  expect(
    [144, 146, 147, 152, 169].map((id) => e2.paroles.find((q) => q.id === id)?.nuee ?? null),
    'ses paroles y reviennent',
  ).toEqual(['n1', 'n1', 'n1', 'n1', 'n1']);
});

test('MEMBRES : déplié, la croix retire une personne, une personne connue s’ajoute ; « Avec … » suit ; le « + » des membres ouvre MEMBRES déplié (C-242)', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, { ...stockageCercles(), promi_prenom: 'Tom' });
  // la sonde : le « + » des membres n'ouvre rien sur un Cercle
  if (sonde('plus-membres-sourd'))
    await page.evaluate(() => {
      document.addEventListener(
        'pointerup',
        (ev) => {
          if ((ev.target as Element | null)?.closest('.fi-plus-membres')) ev.stopImmediatePropagation();
        },
        true,
      );
    });
  await ouvrirCercle(page);
  expect(await avec(page)).toBe('Avec Rachel, Marion, +1');
  await toucherEl(page, '.fi-plus-membres');
  await page.waitForTimeout(700);
  expect(
    await page.evaluate(() => !!document.querySelector('#dpdCorps #npMemb.np-ouv .ph-o')),
    'le « + » ouvre Peaufiner sur MEMBRES déplié',
  ).toBe(true);
  // la croix de Marion
  await toucherEl(page, '#npMemb .ph-o[data-v="Marion"] .ppo-x');
  await page.waitForTimeout(400);
  expect((await etat(page)).membres['n1'], 'Marion retirée').toEqual(['Rachel']);
  // une personne connue (Adrien, du jeu des fiches) s'ajoute
  await toucherEl(page, '#npMemb .ph-o[data-v="Adrien"]');
  await page.waitForTimeout(400);
  expect((await etat(page)).membres['n1'], 'Adrien ajouté').toEqual(['Rachel', 'Adrien']);
  expect(
    await page.evaluate(() => document.querySelector('#npMemb .np-val')?.textContent),
    'la valeur de MEMBRES',
  ).toBe('Rachel · Adrien');
  expect(await avec(page), 'la ligne de la fiche').toBe('Avec Rachel, Adrien, +1');
});

test('DESCRIPTION : écrite, gardée au rechargement (schéma v3), sans emoji (C-129)', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, { ...stockageCercles(), promi_prenom: 'Tom' });
  await ouvrirCercle(page);
  await ouvrirPeauf(page);
  await page.locator('#nqNote').fill('Le menu du 14 🎉 juillet');
  await page.locator('#nqNote').blur();
  await page.waitForTimeout(300);
  expect((await etat(page)).infosCercles['n1']?.note).toBe('Le menu du 14  juillet');
  await page.reload();
  await page.waitForFunction(() => !!(window as unknown as { __promi?: unknown }).__promi);
  await page.evaluate(`${P_}.demarrer()`);
  await page.waitForTimeout(1200);
  expect((await etat(page)).infosCercles['n1']?.note, 'relue').toBe('Le menu du 14  juillet');
  await ouvrirCercle(page);
  await ouvrirPeauf(page);
  expect(await page.locator('#nqNote').inputValue(), 'Peaufiner la montre').toBe('Le menu du 14  juillet');
});
