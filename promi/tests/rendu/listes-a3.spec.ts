/**
 * LOT 4 — A3 (CLAUDE.md, porte de qualité : « toute mesure de mise en page à l'échelle 1 ET à l'échelle 0,79 ») pour l'Index, le Fil et la fiche
 * d'une personne. La vraie app s'adapte à l'écran (L0 §2) : à 390 de large, les cotes du prototype ; plus étroit (330 × 714, la fenêtre de Safari
 * à 0,79), les cartes et les bandeaux suivent la largeur. Le juge vérifie, à 390 et à 330 : aucun texte ne sort de l'écran, le X de l'encart est
 * atteignable au doigt, chaque titre de carte tient (ou s'arrête par « … ») sans toucher son état (C-151).
 */
import { test, expect, type Page } from '@playwright/test';
import { vraieApp, sonde, stockageFiches, P_ } from './aides.ts';

type Releve = { fautes: string[] };

async function relever(page: Page, feuille: string): Promise<Releve> {
  return (await page.evaluate((feuille) => {
    const sh = document.getElementById(feuille)!;
    // l'écran couvre l'appareil : son bord est celui de l'écran du téléphone
    const D = sh.getBoundingClientRect();
    const fautes: string[] = [];
    // C-151 : chaque titre de carte tient dans sa boîte (ou s'arrête par « … ») et le bas de ses lignes reste à 2 pt au moins au-dessus de l'état
    for (const c of sh.querySelectorAll<HTMLElement>('.s4-carte:not(.fil-b)')) {
      const ti = c.querySelector<HTMLElement>('.s4-ti')!;
      const et = c.querySelector<HTMLElement>('.s4-et');
      const kc = c.getBoundingClientRect().width / (c.offsetWidth || 1);
      const coupe = getComputedStyle(ti).webkitLineClamp !== 'none';
      if (!coupe && ti.scrollHeight > ti.clientHeight + 1) fautes.push(`titre coupé net : « ${ti.textContent ?? ''} »`);
      const r = document.createRange();
      r.selectNodeContents(ti);
      if (
        et &&
        (et.textContent ?? '').trim() &&
        r.getBoundingClientRect().bottom > et.getBoundingClientRect().top - 2 * kc + 0.5
      )
        fautes.push(`titre sur l'état : « ${ti.textContent ?? ''} »`);
    }
    // un texte visible hors de l'appareil
    const w = document.createTreeWalker(sh, NodeFilter.SHOW_TEXT);
    let t: Node | null;
    while ((t = w.nextNode())) {
      const el = t.parentElement!;
      if (!(t.nodeValue ?? '').trim() || el.closest('[hidden]') || getComputedStyle(el).visibility === 'hidden')
        continue;
      const r = document.createRange();
      r.selectNodeContents(t);
      let q = r.getBoundingClientRect();
      if (!q.width) continue;
      // un texte qui s'arrête par « … » est rogné par sa boîte : on lit la boîte qui rogne (le juge A3 de la page +)
      for (let x: Element | null = el; x && x !== sh; x = x.parentElement)
        if (getComputedStyle(x).overflowX !== 'visible') {
          const b = x.getBoundingClientRect();
          q = new DOMRect(
            Math.max(q.left, b.left),
            q.top,
            Math.min(q.right, b.right) - Math.max(q.left, b.left),
            q.height,
          );
          break;
        }
      if (q.left < D.left - 1 || q.right > D.right + 1)
        fautes.push(
          `sort de l'écran : « ${(t.nodeValue ?? '').trim().slice(0, 30)} » ${String(Math.round(q.left))} → ${String(Math.round(q.right))} (écran ${String(Math.round(D.left))} → ${String(Math.round(D.right))})`,
        );
    }
    // le X atteignable au doigt
    const x = sh.querySelector('.closeb')!.getBoundingClientRect();
    const sous = document.elementFromPoint(x.left + x.width / 2, x.top + x.height / 2);
    if (!sous?.closest('.closeb')) fautes.push(`le X n'est pas atteignable (${sous?.className ?? 'rien'})`);
    return { fautes };
  }, feuille)) as Releve;
}

const ECRANS: Array<{ nom: string; feuille: string; ouvrir: string }> = [
  { nom: "l'Index", feuille: 'indexSheet', ouvrir: `${P_}.index().ouvrir()` },
  { nom: 'le Fil', feuille: 'feedView', ouvrir: `${P_}.fil().ouvrir()` },
  { nom: 'la fiche de Marion', feuille: 'personSheet', ouvrir: `${P_}.personne().ouvrir('Marion')` },
];

for (const theme of ['sombre', 'clair'] as const)
  test(`A3, à 0,79 (330 × 714) : l'Index, le Fil, la fiche d'une personne — rien hors de l'écran, aucun titre coupé ni collé à son état : ${theme}`, async ({
    page,
  }) => {
    const ls = { ...stockageFiches(), promi_prenom: 'Tom', promi_theme: theme === 'clair' ? 'light' : 'dark' };
    const fautes: string[] = [];
    for (const E of ECRANS) {
      const r: Releve[] = [];
      for (const [w, h] of [
        [390, 844],
        [330, 714],
      ] as const) {
        await page.setViewportSize({ width: w, height: h });
        await vraieApp(page, ls);
        // la sonde (sur « … sombre ») : le titre d'une carte ajusté sans tenir compte de l'échelle (il garde sa taille de départ)
        if (sonde('a3-titres') && w === 330)
          await page.addStyleTag({ content: '#indexSheet .s4-ti{font-size:24px!important}' });
        await page.evaluate(E.ouvrir);
        await page.waitForTimeout(900);
        r.push(await relever(page, E.feuille));
      }
      for (const f of [...r[0]!.fautes, ...r[1]!.fautes]) fautes.push(`${E.nom} : ${f}`);
    }
    expect(fautes).toEqual([]);
  });
