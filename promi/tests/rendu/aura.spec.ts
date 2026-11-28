/**
 * LOT 6 — L'AURA, COMME LE PROTOTYPE (SPEC-ECRANS §10 ; lot-AURA-PELOTE, ses cotes B figées en v126, C-005).
 *
 * Des deux côtés, l'état des fiches (25 paroles, 5 tenues), l'horloge pilotée, « Réduire les animations » (la respiration immobile à mi-cycle, la
 * dérive arrêtée : la Pelote ne bouge plus d'une image à l'autre) ; l'Aura ouverte par sa porte, la Pelote figée à la même vue des deux côtés, les
 * tirages de couleur du PROTOTYPE (le poil, le corps, le bouton : tirés au hasard à chaque ouverture) posés dans l'app :
 *  · ce qu'elle dit — la phrase, les Noyaux (leurs noms, leurs arcs), la légende, les chiffres, « Ce que tu as tenu » — identique ;
 *  · la colonne : ses cotes (en dur : la composition B) ;
 *  · au repos, au pixel, deux thèmes — la Pelote comprise (le même moteur, les mêmes entrées). Tolérance : 2 niveaux, 0 pixel au-delà.
 * EXCEPTIONS NOMMÉES : M1, la matière de chaque dalle — celles de « Ce que tu as tenu » (leur boîte entière, `.au-bx`) et celles que portent
 * les îles de la Pelote (la Pelote est jugée au pixel SANS ses îles, des deux côtés ; les îles, par leur nombre, celles qui sont peintes et la
 * direction de la dernière) ; G, le visage d'un Noyau (`.au-vis` :
 * son grain est un bruit tiré au hasard par le prototype à chaque chargement, celui de l'app d'une graine fixe).
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { deuxPilotes, images, sonde, stockageFiches, P_ } from './aides.ts';
import { juger as jugerL, type Liste } from './listes.ts';

const RES = join(import.meta.dirname, 'resultats', 'aura');
const L: Liste = { liste: '#auCadre', menu: '#aucunMenu', res: RES, autres: '#auraScreen .au-bx, #auraScreen .au-vis' };

/** la composition B (v126) : les cotes de la colonne pour une phrase de deux lignes, en dur */
const COTES_B = { bt: 435.469, mot: 515.599, nx: 582.778, lg: 709.064, cpt: 752.028, mo: 800.528 };
/** la vue posée des deux côtés */
const VUE = [2.9, 0.32] as const;

async function ouvrir(P: Page, A: Page): Promise<void> {
  for (const pg of [P, A]) await pg.emulateMedia({ reducedMotion: 'reduce' });
  await P.evaluate(() => (document.getElementById('souffleBtn') as HTMLElement).click());
  await A.evaluate(`${P_}.nav.ouvrir('aura')`);
  for (let k = 0; k < 4; k++) await Promise.all([images(P, 30), images(A, 30)]);
  // les tirages du prototype (le poil tiré, l'ordre du corps, l'ordre du bouton), posés dans l'app ; puis la même vue, figée, sans roulis
  const t = await P.evaluate(() => {
    const a = (
      window as unknown as {
        _aura: {
          sol(): { idx: number };
          corps(): { ordre: number[]; idx: number };
          bouton(): { ordre: number[] };
          fige(b: boolean): void;
          vue(l: number, t: number): void;
        };
      }
    )._aura;
    return { solTire: a.sol().idx, corpsOrdre: a.corps().ordre, corpsIdx: a.corps().idx, texteOrdre: a.bouton().ordre };
  });
  await A.evaluate(`${P_}.aura().pelote().poserTirages(${JSON.stringify({ ...t, solEvite: -1 })})`);
  await P.evaluate(([l, tt]) => {
    const a = (window as unknown as { _aura: { fige(b: boolean): void; vue(l: number, t: number): void } })._aura;
    a.fige(true);
    a.vue(l!, tt!);
    const r = document.querySelector<HTMLElement>('#auraScreen .au-rot');
    if (r) r.style.transform = 'rotate(0deg)';
  }, VUE);
  await A.evaluate(
    `(()=>{const p=${P_}.aura().pelote();p.fige(true);p.poserVue(${String(VUE[0])},${String(VUE[1])});document.querySelector('#auraScreen .au-rot').style.transform='rotate(0deg)';p.peindre();})()`,
  );
  for (let k = 0; k < 4; k++) await Promise.all([images(P, 30), images(A, 30)]);
}

/** les îles, des deux côtés : leur nombre, celles qui sont peintes, la direction de la dernière (le tour qui la présente) */
async function iles(P: Page, A: Page): Promise<void> {
  const p = await P.evaluate(() => {
    const c = (window as unknown as { _auraComp: { iles: unknown[]; ilesPeintes: number; derniere: number[] | null } })
      ._auraComp;
    return { n: c.iles.length, peintes: c.ilesPeintes, derniere: c.derniere };
  });
  const a = (await A.evaluate(`${P_}.aura().pelote().iles()`)) as typeof p;
  expect(a.n).toBe(p.n);
  expect(a.peintes).toBe(p.peintes);
  expect(a.derniere?.map((v) => +v.toFixed(5))).toEqual(p.derniere?.map((v) => +v.toFixed(5)));
}

/** la Pelote sans ses îles des deux côtés (leur matière respire : M1), repeinte à la même vue */
async function sansIles(P: Page, A: Page): Promise<void> {
  await P.evaluate(() => {
    const a = (window as unknown as { _aura: { sansIles(b: boolean): void; pelote(): unknown } })._aura;
    a.sansIles(true);
    a.pelote();
  });
  await A.evaluate(`(()=>{const p=${P_}.aura().pelote();p.sansIles(true);p.peindre();})()`);
  for (let k = 0; k < 4; k++) await Promise.all([images(P, 30), images(A, 30)]);
}

/** ce que l'Aura dit */
const compo = (pg: Page): Promise<string> =>
  pg.evaluate(() =>
    JSON.stringify([
      document.querySelector('#auraScreen .au-mot')?.textContent,
      [...document.querySelectorAll('#auraScreen .au-n')].map((n) =>
        [
          n.getAttribute('data-qui'),
          n.querySelector('.au-lb')?.textContent,
          [...n.querySelectorAll('path.au-arc')]
            .map((a) => a.getAttribute('stroke') + ':' + a.getAttribute('d'))
            .join(';'),
        ].join('|'),
      ),
      [...document.querySelectorAll('#auraScreen .au-lg span')].map((s) => s.textContent),
      [...document.querySelectorAll('#auraScreen .au-cpt span')].map((s) => s.textContent),
      [...document.querySelectorAll('#auraScreen .au-gr canvas')].map((c) => c.getAttribute('data-pid')),
    ]),
  );

for (const theme of ['sombre', 'clair'] as const)
  test(`l'Aura au repos, comme le prototype : ${theme}`, async ({ browser }) => {
    test.setTimeout(180000);
    const ls = { ...stockageFiches(), promi_prenom: 'Tom', promi_theme: theme === 'clair' ? 'light' : 'dark' };
    const { P, A, erreurs } = await deuxPilotes(browser, ls);
    try {
      mkdirSync(RES, { recursive: true });
      await ouvrir(P, A);
      // la sonde (sur « l'Aura au repos, comme le prototype : sombre ») : la colonne descend d'un point
      if (sonde('aura-colonne') && theme === 'sombre')
        await A.addStyleTag({ content: '#auraScreen .au-nx{margin-top:1px}' });
      expect(await compo(A)).toBe(await compo(P));
      const col = (await A.evaluate(`${P_}.aura().colonne()`)) as Record<string, number>;
      for (const [k, v] of Object.entries(COTES_B)) expect(col[k], `la cote ${k}`).toBeCloseTo(v, 1);
      await iles(P, A);
      await sansIles(P, A);
      await jugerL(P, A, L, theme);
      expect(erreurs).toEqual([]);
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  });
