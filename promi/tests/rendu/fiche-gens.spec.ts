/**
 * LOT 3b-8 — LES PERSONNES CHOISIES DEPUIS PEAUFINER (le prototype : `_gensFiche`, la liste de lot-GENS dans la rangée ; C-122, C-269).
 *
 * Des deux côtés, la même fiche (le prototype dans la fenêtre du banc, la vraie app à 390 × 844, l'horloge pilotée) :
 *  · Peaufiner, puis la rangée À QUI (un Promi) ou AVEC (un Chiche) : la liste des personnes dépliée (« Moi » en tête, les choisies, les connues,
 *    « + ajouter quelqu'un ») — au pixel ;
 *  · une personne touchée : elle s'ajoute, écrite sur la parole — au pixel ;
 *  · « + ajouter quelqu'un », un prénom tapé, Retour : il s'ajoute (écrit des deux côtés) ;
 *  · Peaufiner refermé : la fiche, sa phrase avec les personnes — au pixel.
 * Sombre et clair. Tolérance : 2 niveaux, 0 pixel au-delà. EXCEPTIONS NOMMÉES : C1 (les coins, Peaufiner ouvert) ; V1, après un ajout, la valeur
 * de la rangée (le prototype la laisse à l'ancienne tant que Peaufiner n'est pas rebâti ; la vraie app la suit — elle est vérifiée en texte) ;
 * celles de la fiche (M1, M2, M3). PROTOCOLE : le prototype du banc garde des membres de Cercles de démonstration (`NUEEMEM` : « famille »,
 * « projet ») que l'état du banc n'a pas — ils sont retirés avant de juger (les connus viennent alors des mêmes paroles des deux côtés) ;
 * sa passe des plateaux (`_plateauPartout`) passée après chaque toucher.
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { PNG } from 'pngjs';
import {
  fichesPilotees,
  images,
  ecart,
  sonde,
  stockageFiches,
  zonesFiche,
  masquerFiche,
  P_,
  type Zone,
} from './aides.ts';

const RES = join(import.meta.dirname, 'resultats', 'fiche-gens');
const COINS: Zone[] = [
  [0, 0, 24, 24],
  [366, 0, 24, 24],
  [0, 820, 24, 24],
  [366, 820, 24, 24],
];

async function toucher(pg: Page, x: number, y: number): Promise<void> {
  const r = await pg.evaluate(() => {
    const b = document.getElementById('device')!.getBoundingClientRect();
    return { x: b.left, y: b.top, k: b.width / 390 };
  });
  await pg.mouse.click(r.x + x * r.k, r.y + y * r.k);
}
/** le centre de `sel` (en pt de l'écran 390), l'élément amené dans son rail s'il glisse */
async function centre(pg: Page, sel: string, gauche = false): Promise<[number, number]> {
  return (await pg.evaluate(
    ([sel, gauche]) => {
      const e = document.querySelector<HTMLElement>(sel as string)!;
      const gl = e.closest<HTMLElement>('.pc-glisse');
      if (gl) {
        const a = e.getBoundingClientRect();
        const b = gl.getBoundingClientRect();
        if (a.right > b.right) gl.scrollLeft += a.right - b.right;
      }
      const D = document.getElementById('device')!.getBoundingClientRect();
      const k = D.width / 390;
      const r = e.getBoundingClientRect();
      return [
        (r.left - D.left) / k + (gauche ? 30 : r.width / k / 2),
        (r.top - D.top) / k + Math.min(32, r.height / k / 2),
      ];
    },
    [sel, gauche] as const,
  )) as [number, number];
}
async function image(pg: Page): Promise<Buffer> {
  const clip = await pg.evaluate(() => {
    const r = document.getElementById('device')!.getBoundingClientRect();
    return { x: r.left, y: r.top, width: r.width, height: r.height };
  });
  return pg.screenshot({ clip });
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

/** la valeur de la rangée dépliée (en pt de l'écran 390) */
async function zoneValeur(A: Page): Promise<Zone[]> {
  return (await A.evaluate(() => {
    const v = document.querySelector('#dpdCorps .s2-reg.s2-ouv .s2-val');
    if (!v) return [];
    const D = document.getElementById('device')!.getBoundingClientRect();
    const k = D.width / 390;
    const b = v.getBoundingClientRect();
    return [[(b.left - D.left) / k - 2, (b.top - D.top) / k - 2, b.width / k + 4, b.height / k + 4]];
  })) as Zone[];
}
const pose = (P: Page): Promise<void> =>
  P.evaluate(() => {
    (window as unknown as { _plateauPartout?: () => void })._plateauPartout?.();
  });

const CAS: ReadonlyArray<[number, string, 'À QUI' | 'AVEC', string, string]> = [
  [148, 'Promi en cours, à Marion', 'À QUI', 'Lou', 'Zoé'],
  [162, 'Chiche lancé à Adrien', 'AVEC', 'Rachel', 'Zoé'],
];

for (const theme of ['sombre', 'clair'] as const)
  for (const [id, cas, rangee, touche, tape] of CAS)
    test(`les personnes choisies depuis Peaufiner, comme le prototype : ${cas}, ${rangee}, ${theme}`, async ({
      browser,
    }) => {
      const ls = { ...stockageFiches(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
      const { P, A, erreurs } = await fichesPilotees(browser, ls, id);
      try {
        // la sonde (sur « … Promi en cours, à Marion, À QUI, sombre ») : une personne touchée ne s'écrit pas sur la parole
        if (sonde('gens-fiche-sourd'))
          await A.evaluate(
            `(() => { const m = ${P_}.magasin; const f = m.peaufiner.bind(m); m.peaufiner = (id, c, t) => { if (c.qui || c.avec) return; f(id, c, t); }; })()`,
          );
        // la sonde (sur « … Chiche lancé à Adrien, AVEC, clair ») : les pastilles des personnes au dessin de la page + (162 de large)
        if (sonde('gens-fiche-page-plus'))
          await A.addStyleTag({
            content:
              '#detailPoster #dpdCorps .gn, #detailPoster #dpdCorps .gn-liste{grid-template-columns:repeat(2,minmax(0,162px))!important;gap:8px 12px!important}',
          });
        // (`NUEEMEM` est un `let` du prototype : il n'est pas sur `window`, on le nomme)
        await P.evaluate('for (const k of Object.keys(NUEEMEM)) delete NUEEMEM[k]');
        for (const pg of [P, A])
          await pg.addStyleTag({ content: '#device input,#device textarea{caret-color:transparent!important}' });
        mkdirSync(RES, { recursive: true });
        const juge = async (quoi: string, peauf: boolean, val = false): Promise<void> => {
          let ip: Buffer = Buffer.alloc(0);
          let ia: Buffer = Buffer.alloc(0);
          for (let k = 0; k < 20; k++) {
            await Promise.all([images(P, 40), images(A, 40)]);
            let p2: Buffer;
            let a2: Buffer;
            if (peauf) {
              const Z = val ? [...COINS, ...(await zoneValeur(A))] : COINS;
              p2 = masquer(await image(P), Z);
              a2 = masquer(await image(A), Z);
            } else {
              const Z = await zonesFiche(A, P);
              const n = await A.evaluate(() => document.querySelectorAll('#detailPoster.fiche canvas.kr-c').length);
              p2 = masquerFiche(await image(P), Z, n);
              a2 = masquerFiche(await image(A), Z, n);
            }
            const ok = k > 1 && p2.equals(ip) && a2.equals(ia);
            [ip, ia] = [p2, a2];
            if (ok) break;
          }
          writeFileSync(join(RES, `${theme}-${String(id)}-${quoi}-prototype.png`), ip);
          writeFileSync(join(RES, `${theme}-${String(id)}-${quoi}-app.png`), ia);
          const e = ecart(ip, ia);
          expect(
            { n: e.n, boite: e.boite },
            `${quoi} : pixels écartés de plus de 2 niveaux (bords lissés hors macOS : ${String(e.bords)})`,
          ).toEqual({ n: 0, boite: null });
        };
        const lus = async (): Promise<[string, string]> => {
          const champ = rangee === 'AVEC' ? 'avec' : 'who';
          const p = (await P.evaluate(`String(promises.find(q => q.id === ${String(id)}).${champ} || '')`)) as string;
          const a = (await A.evaluate(
            `(q => String((${JSON.stringify(champ)} === 'avec' ? (q.suite || {}).avec : q.who) || ''))(${P_}.magasin.etat().paroles.find(q => q.id === ${String(id)}))`,
          )) as string;
          return [p, a];
        };
        // Peaufiner, puis la rangée : la liste dépliée
        await Promise.all([toucher(P, 80, 802), toucher(A, 80, 802)]);
        await Promise.all([images(P, 60), images(A, 60)]);
        const rg = async (pg: Page): Promise<[number, number]> =>
          (await pg.evaluate((lab) => {
            const e = [...document.querySelectorAll('#dpdCorps .s2-reg')].find(
              (x) => (x.querySelector('.s2-lab')?.textContent ?? '').trim() === lab,
            )!;
            const D = document.getElementById('device')!.getBoundingClientRect();
            const k = D.width / 390;
            const r = e.getBoundingClientRect();
            return [(r.left - D.left) / k + 30, (r.top - D.top) / k + 30];
          }, rangee)) as [number, number];
        const [rx, ry] = await rg(A);
        await Promise.all([toucher(P, rx, ry), toucher(A, rx, ry)]);
        await Promise.all([images(P, 60), images(A, 60)]);
        await pose(P);
        expect(
          await A.evaluate(() => document.querySelectorAll('#dpdCorps .s2-ouv .gn .ph-o').length),
          'la liste dépliée',
        ).toBeGreaterThan(3);
        await juge('liste', true);
        // une personne touchée : elle s'ajoute
        const pastille = async (pg: Page): Promise<[number, number]> =>
          (await pg.evaluate((n) => {
            const e = [...document.querySelectorAll('#dpdCorps .s2-ouv .gn .ph-o')].find(
              (x) => (x.querySelector('.ppo-nom')?.textContent ?? '') === n,
            )!;
            const D = document.getElementById('device')!.getBoundingClientRect();
            const k = D.width / 390;
            const r = e.getBoundingClientRect();
            return [(r.left - D.left) / k + 50, (r.top - D.top) / k + r.height / k / 2];
          }, touche)) as [number, number];
        const pp = await pastille(P);
        const pa = await pastille(A);
        await Promise.all([toucher(P, pp[0], pp[1]), toucher(A, pa[0], pa[1])]);
        await Promise.all([images(P, 80), images(A, 80)]);
        await pose(P);
        const [p1, a1] = await lus();
        expect(p1, 'le prototype a pris la personne').toContain(touche);
        expect(a1, 'la personne écrite sur la parole, comme le prototype').toBe(p1);
        expect(
          await A.evaluate(() => document.querySelector('#dpdCorps .s2-reg.s2-ouv .s2-val')?.textContent ?? ''),
          'la valeur de la rangée suit le choix',
        ).toBe(a1);
        await juge('ajoute', true, true);
        // « + ajouter quelqu'un », un prénom tapé, Retour
        const zone = async (pg: Page): Promise<[number, number]> =>
          (await pg.evaluate(() => {
            const e = document.querySelector('#dpdCorps .s2-ouv .gn .ph-add')!;
            e.scrollIntoView({ block: 'nearest' });
            const D = document.getElementById('device')!.getBoundingClientRect();
            const k = D.width / 390;
            const r = e.getBoundingClientRect();
            return [(r.left - D.left) / k + r.width / k / 2, (r.top - D.top) / k + r.height / k / 2];
          })) as [number, number];
        const zp = await zone(P);
        const za = await zone(A);
        await Promise.all([toucher(P, zp[0], zp[1]), toucher(A, za[0], za[1])]);
        await Promise.all([images(P, 30), images(A, 30)]);
        for (const pg of [P, A]) {
          await pg.keyboard.type(tape);
          await images(pg, 20);
          await pg.keyboard.press('Enter');
        }
        await Promise.all([images(P, 80), images(A, 80)]);
        const [p2, a2] = await lus();
        expect(p2, 'le prototype a pris le prénom tapé').toContain(tape);
        expect(a2, 'le prénom tapé écrit sur la parole, comme le prototype').toBe(p2);
        // Peaufiner refermé par son X : la fiche, sa phrase avec les personnes
        for (const pg of [P, A]) await pg.evaluate(() => (document.activeElement as HTMLElement | null)?.blur());
        await Promise.all([images(P, 30), images(A, 30)]);
        const [xx, xy] = await centre(A, '#dpdCorps .s2-fermer');
        await Promise.all([toucher(P, xx, xy), toucher(A, xx, xy)]);
        await Promise.all([images(P, 80), images(A, 80)]);
        await pose(P);
        await juge('fiche', false);
        expect(erreurs).toEqual([]);
      } finally {
        await Promise.all([P.context().close(), A.context().close()]);
      }
    });

// LE « + » DES MEMBRES (C-254 ; le prototype : `ouvreGens` de lot-V181A-CERCLE) — touché des deux côtés : Peaufiner ouvert sur les personnes, leur
// rangée dépliée, le panneau glissé jusqu'à elle (420 ms) ; sur un Promi à soi, la rangée À QUI paraît pour l'occasion — au pixel, une fois posé
for (const theme of ['sombre', 'clair'] as const)
  for (const [id, cas] of [
    [144, 'Promi en cours, à soi'],
    [162, 'Chiche lancé à Adrien'],
  ] as const)
    test(`le + des membres ouvre Peaufiner sur les personnes, comme le prototype : ${cas}, ${theme}`, async ({
      browser,
    }) => {
      const ls = { ...stockageFiches(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
      const { P, A, erreurs } = await fichesPilotees(browser, ls, id);
      try {
        // la sonde (sur « le + des membres … : Promi en cours, à soi, sombre ») : le + ouvre Peaufiner sans y glisser
        if (sonde('plus-membres-sans-glisse'))
          await A.evaluate(() => {
            const c = document.getElementById('dpdCorps');
            if (c) Object.defineProperty(c, 'scrollTop', { set: () => undefined, get: () => 0 });
          });
        await P.evaluate('for (const k of Object.keys(NUEEMEM)) delete NUEEMEM[k]');
        mkdirSync(RES, { recursive: true });
        const centreDe = async (pg: Page, sel: string): Promise<[number, number]> =>
          (await pg.evaluate((sel) => {
            const e = document.querySelector(sel)!;
            const D = document.getElementById('device')!.getBoundingClientRect();
            const k = D.width / 390;
            const r = e.getBoundingClientRect();
            return [(r.left - D.left) / k + r.width / k / 2, (r.top - D.top) / k + r.height / k / 2];
          }, sel)) as [number, number];
        const cp = await centreDe(P, '#cerclePlusMembres');
        const ca = await centreDe(A, '#detailPoster .fi-plus-membres');
        await Promise.all([toucher(P, cp[0], cp[1]), toucher(A, ca[0], ca[1])]);
        await Promise.all([images(P, 90), images(A, 90)]);
        await pose(P);
        let ip: Buffer = Buffer.alloc(0);
        let ia: Buffer = Buffer.alloc(0);
        for (let k = 0; k < 20; k++) {
          await Promise.all([images(P, 40), images(A, 40)]);
          const p2 = masquer(await image(P), COINS);
          const a2 = masquer(await image(A), COINS);
          const ok = k > 1 && p2.equals(ip) && a2.equals(ia);
          [ip, ia] = [p2, a2];
          if (ok) break;
        }
        writeFileSync(join(RES, `${theme}-${String(id)}-plus-prototype.png`), ip);
        writeFileSync(join(RES, `${theme}-${String(id)}-plus-app.png`), ia);
        expect(
          await A.evaluate(() => document.querySelector('#dpdCorps .s2-reg.s2-ouv .s2-lab')?.textContent ?? ''),
          'la rangée des personnes, dépliée',
        ).toMatch(/^(À QUI|QUI OSE \?)$/);
        const e = ecart(ip, ia);
        expect(
          { n: e.n, boite: e.boite },
          `Peaufiner ouvert par le + : pixels écartés de plus de 2 niveaux (bords lissés hors macOS : ${String(e.bords)})`,
        ).toEqual({ n: 0, boite: null });
        expect(erreurs).toEqual([]);
      } finally {
        await Promise.all([P.context().close(), A.context().close()]);
      }
    });
