/**
 * LOT 4 — L'INDEX, COMME LE PROTOTYPE (SPEC-ECRANS §8 ; lot-S4, lot-V210-ENCART C-301, C-147, C-151).
 *
 * Des deux côtés, l'état des fiches (25 paroles) : le prototype dans la fenêtre du banc, la vraie app à 390 × 844, l'horloge pilotée ; l'Index
 * ouvert (le prototype par son bouton de la barre), puis posé :
 *  · l'écran au repos — l'encart, la recherche, le ⇅, les trois premières rangées de cartes — au pixel ;
 *  · la grille défilée au bout — les dernières cartes — au pixel ;
 *  · l'ordre des cartes (« Récents » : la dernière action, sinon la plus récemment plantée), leurs mots, la taille de chaque titre (C-151).
 * Sombre et clair. Tolérance : 2 niveaux, 0 pixel au-delà. EXCEPTION NOMMÉE : M1, la matière de chaque dalle (sa boîte déclarée `data-matiere`,
 * 8 pt autour) — elle respire (§8 bis) ; la boîte, la place, le champ autour d'elle restent jugés.
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { deuxPilotes, vraieApp, images, sonde, stockageFiches, P_, PAROLE_CERCLE } from './aides.ts';
import { juger as jugerL, toucher, toucherDeux, type Liste } from './listes.ts';

const RES = join(import.meta.dirname, 'resultats', 'index');
const L: Liste = { liste: '#indexList', menu: '#ixMenu', res: RES };
const juger = (P: Page, A: Page, nom: string): Promise<void> => jugerL(P, A, L, nom);

/** les cartes : la parole, le titre, sa taille, le sur-titre, l'état */
async function cartes(pg: Page): Promise<string[]> {
  return pg.evaluate(() =>
    [...document.querySelectorAll('#indexList .s4-carte')].map((c) =>
      [
        c.getAttribute('data-pid'),
        c.querySelector('.s4-eb')?.textContent,
        c.querySelector('.s4-ti')?.textContent,
        getComputedStyle(c.querySelector('.s4-ti')!).fontSize,
        c.querySelector('.s4-et')?.textContent,
      ].join(' | '),
    ),
  );
}

/** l'état des fiches, plus un Cercle de deux paroles (« Marseille ») et un gardé de côté (la fin de la liste) */
function stockageCercle(): Record<string, string> {
  const ls = stockageFiches(true);
  const st = JSON.parse(ls['promi_state']!) as { promises: Array<Record<string, unknown>>; nid: number };
  st.promises.push(
    {
      ...PAROLE_CERCLE,
      id: 171,
      title: 'acheter le pain',
      cle: 'acheter le pain',
      derAct: 1795483000000,
      place: [0.3, 0.42, 0],
    },
    {
      id: 170,
      title: 'ranger la cave',
      who: 'moi',
      due: null,
      intensity: 2,
      status: 'encours',
      from: 'moi',
      recur: null,
      remind: null,
      draft: true,
      files: [],
    },
  );
  st.nid = 172;
  ls['promi_state'] = JSON.stringify(st);
  return ls;
}

/** l'Index ouvert des deux côtés, posé */
async function ouvrirIndex(P: Page, A: Page): Promise<void> {
  await P.evaluate(() => (document.getElementById('indexBtn') as HTMLElement).click());
  await A.evaluate(`${P_}.index().ouvrir()`);
  // par tranches : les passes du prototype (`_s4TitresAjuste`) partent d'un observateur et de minuteurs — une seule tranche de 180 images ne
  // leur rend jamais la main (l'observateur ne tourne qu'entre deux tâches)
  for (let k = 0; k < 6; k++) await Promise.all([images(P, 30), images(A, 30)]);
}

for (const theme of ['sombre', 'clair'] as const)
  test(`l'Index avec un Cercle de deux paroles et un gardé de côté, comme le prototype : ${theme}`, async ({
    browser,
  }) => {
    const ls = { ...stockageCercle(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
    const { P, A, erreurs } = await deuxPilotes(browser, ls);
    try {
      mkdirSync(RES, { recursive: true });
      // la sonde (sur « … sombre ») : le gardé de côté perd son pointillé
      if (sonde('garde-sans-pointille'))
        await A.addStyleTag({ content: '#indexSheet .s4-carte{outline:none!important}' });
      await ouvrirIndex(P, A);
      const c = await cartes(A);
      expect(c, 'les cartes, leurs mots, la taille de chaque titre').toEqual(await cartes(P));
      expect(c[0], 'le Cercle en tête (sa dernière action)').toMatch(/^ \| avec \+2 \| Marseille \|/);
      expect(c.at(-1), 'le gardé de côté ferme la liste').toMatch(/gardé de côté \| ranger la cave/);
      await juger(P, A, `${theme}-cercle-repos`);
      for (const pg of [P, A])
        await pg.evaluate(() => {
          const l = document.getElementById('indexList')!;
          l.scrollTop = l.scrollHeight;
        });
      await juger(P, A, `${theme}-cercle-bout`);
      expect(erreurs).toEqual([]);
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  });

for (const theme of ['sombre', 'clair'] as const)
  test(`l'Index au repos et défilé au bout, comme le prototype : ${theme}`, async ({ browser }) => {
    const ls = { ...stockageFiches(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
    const { P, A, erreurs } = await deuxPilotes(browser, ls);
    try {
      mkdirSync(RES, { recursive: true });
      // la sonde (sur « … sombre ») : la vraie app range les cartes par ordre de plantation, la plus ancienne d'abord
      if (sonde('ordre-plantation'))
        await A.evaluate(`(() => { for (const p of ${P_}.magasin.etat().paroles) p.derAct = 1000 - p.id; })()`);
      // la sonde (sur « … clair ») : les cartes prennent la crème en clair (l'ancien corps clair, avant C-147)
      if (sonde('carte-creme-clair'))
        await A.addStyleTag({ content: '.device.light #indexSheet .s4-carte{background:#F7F0DE!important}' });
      await P.evaluate(() => (document.getElementById('indexBtn') as HTMLElement).click());
      await A.evaluate(`${P_}.index().ouvrir()`);
      // par tranches : les passes du prototype (`_s4TitresAjuste`) partent d'un observateur et de minuteurs — une seule tranche de 180 images ne
      // leur rend jamais la main (l'observateur ne tourne qu'entre deux tâches)
      for (let k = 0; k < 6; k++) await Promise.all([images(P, 30), images(A, 30)]);
      expect(await cartes(A), 'les cartes, leurs mots, la taille de chaque titre').toEqual(await cartes(P));
      await juger(P, A, `${theme}-repos`);
      for (const pg of [P, A])
        await pg.evaluate(() => {
          const l = document.getElementById('indexList')!;
          l.scrollTop = l.scrollHeight;
        });
      await juger(P, A, `${theme}-bout`);
      expect(erreurs).toEqual([]);
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  });

for (const theme of ['sombre', 'clair'] as const)
  test(`le menu ⇅ de l'Index, ses tris et ses filtres, comme le prototype : ${theme}`, async ({ browser }) => {
    const ls = { ...stockageCercle(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
    const { P, A, erreurs } = await deuxPilotes(browser, ls);
    try {
      mkdirSync(RES, { recursive: true });
      // la sonde (sur « … sombre ») : « Par personne » range comme « Récents »
      if (sonde('tri-personne-sourd'))
        await A.evaluate(() => {
          document.addEventListener(
            'pointerup',
            (ev) => {
              if ((ev.target as Element | null)?.closest('[data-tri="personne"]')) ev.stopImmediatePropagation();
            },
            true,
          );
        });
      await ouvrirIndex(P, A);
      await toucherDeux(P, A, '#ixTriBtn');
      expect(
        await A.evaluate(() => document.getElementById('ixMenu')!.classList.contains('on')),
        'le menu est ouvert',
      ).toBe(true);
      await juger(P, A, `${theme}-menu`);
      // un toucher dans le panneau, hors d'un choix (son groupe « TRIER ») : il reste ouvert (Q578)
      await toucherDeux(P, A, '#ixMenu .ix-mg');
      expect(
        await A.evaluate(() => document.getElementById('ixMenu')!.classList.contains('on')),
        'Q578 : il reste',
      ).toBe(true);
      for (const sel of [
        '#ixMenu [data-tri="personne"]',
        '#ixMenu [data-tri="nuee"]',
        '#ixMenu [data-filt="suspens"]',
        '#ixMenu [data-filt="brouillons"]',
        '#ixMenu [data-filt="nuees"]',
      ]) {
        if (!(await A.evaluate(() => document.getElementById('ixMenu')!.classList.contains('on'))))
          await toucherDeux(P, A, '#ixTriBtn');
        await toucherDeux(P, A, sel);
        expect(await cartes(A), `${sel} : les cartes`).toEqual(await cartes(P));
        await juger(P, A, `${theme}-${sel.replace(/[^a-z]/g, '')}`);
      }
      // ailleurs que le panneau : il se referme
      await toucherDeux(P, A, '#ixTriBtn');
      await Promise.all([toucher(P, 195, 800), toucher(A, 195, 800)]);
      await Promise.all([images(P, 30), images(A, 30)]);
      expect(await A.evaluate(() => document.getElementById('ixMenu')!.classList.contains('on')), 'refermé').toBe(
        false,
      );
      expect(erreurs).toEqual([]);
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  });

/** une recherche écrite des deux côtés (le champ sans le focus : son texte d'exemple, qui se retrace au focus, n'est pas jugé ici) */
async function chercher(P: Page, A: Page, v: string): Promise<void> {
  for (const pg of [P, A])
    await pg.evaluate((v) => {
      const i = document.getElementById('ixSearch') as HTMLInputElement;
      i.value = v;
      i.dispatchEvent(new Event('input', { bubbles: true }));
    }, v);
  for (let k = 0; k < 3; k++) await Promise.all([images(P, 30), images(A, 30)]);
}
/** le texte de l'écran vide (ses deux lignes), ou rien */
const vide = (pg: Page): Promise<string> =>
  pg.evaluate(() => [...document.querySelectorAll('#indexList .e4v > *')].map((e) => e.textContent).join(' / '));

for (const theme of ['sombre', 'clair'] as const)
  test(`les écrans vides de l'Index (E4, v178c) et leur seconde ligne, comme le prototype : ${theme}`, async ({
    browser,
  }) => {
    const ls = { ...stockageFiches(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
    const { P, A, erreurs } = await deuxPilotes(browser, ls);
    try {
      mkdirSync(RES, { recursive: true });
      // la sonde (sur « … sombre ») : la seconde ligne de la recherche vide ne mène plus à rien
      if (sonde('vide-ligne-sourde'))
        await A.addStyleTag({ content: '#indexSheet .e4-l2{pointer-events:none!important}' });
      await ouvrirIndex(P, A);
      const cas: Array<[string, () => Promise<void>, string]> = [
        ['recherche', () => chercher(P, A, 'zzz'), 'Rien pour «\u00a0zzz\u00a0». / Revenir à tout l’Index.'],
        [
          'gardes',
          async () => {
            await toucherDeux(P, A, '#ixTriBtn');
            await toucherDeux(P, A, '#ixMenu [data-filt="brouillons"]');
          },
          'Rien de gardé de côté. / Revenir à toutes les paroles.',
        ],
        [
          'demandes',
          async () => {
            await toucherDeux(P, A, '#ixTriBtn');
            await toucherDeux(P, A, '#ixMenu [data-filt="demandes"]');
          },
          'Rien sous ce tri. / Revenir à toutes les paroles.',
        ],
      ];
      const tout = await cartes(P);
      for (const [nom, faire, mots] of cas) {
        await faire();
        expect(await vide(A), `${nom} : les deux lignes`).toBe(mots);
        expect(await vide(P), `${nom} : celles du prototype`).toBe(mots);
        await juger(P, A, `${theme}-vide-${nom}`);
        // la seconde ligne : retour à toute la liste
        await toucherDeux(P, A, '#indexList .e4-l2');
        expect(await cartes(A), `${nom} : la seconde ligne rend toute la liste`).toEqual(tout);
        expect(await cartes(P), `${nom} : le prototype aussi`).toEqual(tout);
      }
      expect(erreurs).toEqual([]);
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  });

test("l'Index sans aucune parole : « Pas encore de parole. », la seconde ligne ouvre la page + d'un Promi", async ({
  browser,
}) => {
  const ls = stockageFiches();
  const st = JSON.parse(ls['promi_state']!) as { promises: unknown[] };
  st.promises = [];
  ls['promi_state'] = JSON.stringify(st);
  const { P, A, erreurs } = await deuxPilotes(browser, ls);
  try {
    await ouvrirIndex(P, A);
    const mots = 'Pas encore de parole. / La première se plante en une phrase.';
    expect(await vide(A)).toBe(mots);
    expect(await vide(P)).toBe(mots);
    await juger(P, A, 'vide-aucune');
    const n0 = (await A.evaluate(`${P_}.nav.journal().length`)) as number;
    await toucherDeux(P, A, '#indexList .e4-l2');
    for (let k = 0; k < 6; k++) await Promise.all([images(P, 30), images(A, 30)]);
    expect(
      ((await A.evaluate(`${P_}.nav.journal()`)) as Array<{ vers: string; arg?: string }>)
        .slice(n0)
        .map((d) => [d.vers, d.arg]),
    ).toEqual([['pagePlus', 'promi']]);
    expect(await A.evaluate(`${P_}.index().ouvert()`), "l'Index s'est refermé").toBe(false);
    expect(
      await P.evaluate(() => document.getElementById('createSheet')!.classList.contains('show')),
      'le prototype : la page + ouverte',
    ).toBe(true);
    expect(erreurs).toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});

for (const theme of ['sombre', 'clair'] as const)
  test(`une carte de l'Index ouvre sa fiche ; son X ramène l'Index tel qu'il était (C-193, C-250) : ${theme}`, async ({
    browser,
  }) => {
    const ls = { ...stockageFiches(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
    const { P, A, erreurs } = await deuxPilotes(browser, ls);
    try {
      mkdirSync(RES, { recursive: true });
      // la sonde (sur « … sombre ») : la fiche, refermée, ramène l'Index en haut
      if (sonde('retour-en-haut'))
        await A.evaluate(() => {
          document.querySelector('#detailPoster .closeb')!.addEventListener('pointerup', () => {
            document.getElementById('indexList')!.scrollTop = 0;
          });
        });
      await ouvrirIndex(P, A);
      for (const pg of [P, A])
        await pg.evaluate(() => {
          document.getElementById('indexList')!.scrollTop = 640;
        });
      for (let k = 0; k < 2; k++) await Promise.all([images(P, 30), images(A, 30)]);
      // la carte « nager jeudi » (161, la troisième rangée), à la même place des deux côtés
      await toucherDeux(P, A, '#indexList .s4-carte[data-pid="161"]');
      for (let k = 0; k < 4; k++) await Promise.all([images(P, 30), images(A, 30)]);
      const ouverte = async (pg: Page): Promise<string> =>
        pg.evaluate(() => {
          const f = document.getElementById('detailPoster')!;
          const vu = !f.hidden && getComputedStyle(f).display !== 'none' && f.getBoundingClientRect().top < 100;
          return vu ? (document.getElementById('dptTitre')?.textContent ?? '').trim() : '';
        });
      expect(await ouverte(A), 'la fiche de la carte touchée').toBe('nager jeudi');
      expect(await ouverte(P), 'le prototype aussi').toBe('nager jeudi');
      // le X de la fiche
      await toucherDeux(P, A, '#detailPoster .closeb');
      for (let k = 0; k < 4; k++) await Promise.all([images(P, 30), images(A, 30)]);
      expect(await ouverte(A), 'la fiche refermée').toBe('');
      expect(await A.evaluate(`${P_}.index().ouvert()`), "l'Index est là").toBe(true);
      expect(await A.evaluate(() => document.getElementById('indexList')!.scrollTop), 'au même défilement').toBe(
        await P.evaluate(() => document.getElementById('indexList')!.scrollTop),
      );
      await juger(P, A, `${theme}-retour`);
      expect(erreurs).toEqual([]);
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  });

test("l'Index monte du bas à l'ouverture et y redescend au X, jamais d'un coup (C-271 ; le prototype : .sheet, 0,4 s)", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, stockageFiches());
  // la sonde : la transition retirée (l'Index paraît et part d'un coup)
  if (sonde('index-sec')) await page.addStyleTag({ content: '#indexSheet{transition:none!important}' });
  // la transition de l'Index (`getAnimations`), lue dans la tâche qui l'ouvre (ou qui touche son X), arrêtée à 0, ¼, ½, ¾ et à la fin
  const releve = (
    geste: string,
  ): string => `(() => { ${geste}; const e = document.getElementById('indexSheet'); e.getBoundingClientRect();
    const t = e.getAnimations().find((a) => a.transitionProperty === 'transform'); if (!t) return null;
    const D = t.effect.getComputedTiming().duration; t.pause(); const v = [];
    for (const f of [0, 0.25, 0.5, 0.75, 1]) { t.currentTime = D * f; v.push(Math.round(e.getBoundingClientRect().top * 10) / 10); }
    t.finish(); return { D, v }; })()`;
  type Releve = { D: number; v: number[] } | null;
  const m = (await page.evaluate(releve(`${P_}.index().ouvrir()`))) as Releve;
  expect(m, 'une transition de la place à l’ouverture').not.toBeNull();
  expect(m!.D, 'en 0,4 s (le prototype : .sheet)').toBe(400);
  expect(m!.v[0], 'il part d’en bas').toBeGreaterThan(800);
  expect(
    m!.v.slice(1, 4).every((y, i) => y > 1 && y < 843 && y < m!.v[i]!),
    `il monte, image après image (${m!.v.join(' → ')})`,
  ).toBe(true);
  expect(m!.v[4], 'arrivé en haut').toBeLessThan(1);
  await page.waitForTimeout(600);
  const d = (await page.evaluate(
    releve(`(() => { const x = document.querySelector('#indexSheet .closeb'); const r = x.getBoundingClientRect();
      const o = { bubbles: true, clientX: r.left + r.width / 2, clientY: r.top + r.height / 2, pointerId: 1, pointerType: 'touch', isPrimary: true };
      x.dispatchEvent(new PointerEvent('pointerdown', o)); x.dispatchEvent(new PointerEvent('pointerup', o)); x.dispatchEvent(new MouseEvent('click', o)); })()`),
  )) as Releve;
  expect(d, 'une transition de la place au X').not.toBeNull();
  expect(d!.D).toBe(400);
  expect(
    d!.v.slice(1, 4).every((y, i) => y > 1 && y < 843 && y > d!.v[i]!),
    `il redescend, image après image (${d!.v.join(' → ')})`,
  ).toBe(true);
  await expect
    .poll(() => page.evaluate(() => document.getElementById('indexSheet')!.hidden), {
      message: 'caché à la fin',
      timeout: 5000,
    })
    .toBe(true);
});
