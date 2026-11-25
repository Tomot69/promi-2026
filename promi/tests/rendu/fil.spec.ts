/**
 * LOT 4 — LE FIL, COMME LE PROTOTYPE (SPEC-ECRANS §9 ; `buildFeed`, `_s4Fil` de lot-S4, C-301, C-147, C-191, C-245).
 *
 * Des deux côtés, l'état des fiches (25 paroles, 29 événements) : le prototype dans la fenêtre du banc, la vraie app à 390 × 844, l'horloge
 * pilotée ; le Fil ouvert (le prototype par son bouton de la barre), puis posé :
 *  · l'écran au repos — l'encart et son compte, la recherche, le ⇅, les premiers bandeaux — au pixel ;
 *  · défilé au bout — les derniers bandeaux — au pixel ;
 *  · l'ordre des bandeaux, leurs mots (l'événement, le titre, l'état et l'heure).
 * Sombre et clair. Tolérance : 2 niveaux, 0 pixel au-delà. EXCEPTION NOMMÉE : M1, la matière de chaque dalle (listes.ts) — ici sa boîte seule,
 * sans marge : la dalle d'un bandeau est rendue pour y tenir, et le trait vertical reste jugé.
 */
import { test, expect, type Page } from '@playwright/test';
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { deuxPilotes, vraieApp, sonde, stockageFiches, P_ } from './aides.ts';
import { juger as jugerL, poser, toucherDeux, type Liste } from './listes.ts';

const RES = join(import.meta.dirname, 'resultats', 'fil');
const L: Liste = { liste: '#feedList', menu: '#fdMenu', res: RES, marge: 0 };
const juger = (P: Page, A: Page, nom: string): Promise<void> => jugerL(P, A, L, nom);

/** les bandeaux : l'événement, le titre, l'état */
async function bandeaux(pg: Page): Promise<string[]> {
  return pg.evaluate(() =>
    [...document.querySelectorAll('#feedList .s4-carte')].map((c) =>
      [
        c.getAttribute('data-pid'),
        c.querySelector('.s4-ev')?.textContent,
        c.querySelector('.s4-ti')?.textContent,
        c.querySelector('.s4-et')?.textContent,
      ].join(' | '),
    ),
  );
}

/** le Fil ouvert des deux côtés, posé */
async function ouvrirFil(P: Page, A: Page): Promise<void> {
  await P.evaluate(() => (document.getElementById('filBtn') as HTMLElement).click());
  await A.evaluate(`${P_}.fil().ouvrir()`);
  await poser(P, A, 8);
}

for (const theme of ['sombre', 'clair'] as const)
  test(`le Fil au repos et défilé au bout, comme le prototype : ${theme}`, async ({ browser }) => {
    const ls = { ...stockageFiches(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
    const { P, A, erreurs } = await deuxPilotes(browser, ls);
    try {
      mkdirSync(RES, { recursive: true });
      // la sonde (sur « … sombre ») : le bandeau d'une parole tenue garde le corps de sa nature (au lieu de la terre de la fiche, C-147)
      if (sonde('fil-tenu-sans-terre'))
        await A.addStyleTag({ content: '#feedList .s4-carte[data-pid="164"]{background:#0E78F2!important}' });
      await ouvrirFil(P, A);
      expect(await bandeaux(A), 'les bandeaux, leurs mots').toEqual(await bandeaux(P));
      expect(await A.evaluate(() => document.getElementById('fdCount')?.textContent), 'le compte').toBe(
        await P.evaluate(() => document.getElementById('fdCount')?.textContent),
      );
      await juger(P, A, `${theme}-repos`);
      // au milieu : les bandeaux d'un événement venu de quelqu'un (« lire le roman », de Nico ; « envoyer la carte », de Marion) — leur visage
      for (const pg of [P, A])
        await pg.evaluate(() => {
          const l = document.getElementById('feedList')!;
          l.scrollTop = (l.querySelector('.s4-carte[data-pid="160"]') as HTMLElement).offsetTop - 10;
        });
      expect(
        await A.evaluate(() => document.querySelectorAll('#feedList .s4-vis').length),
        'des visages',
      ).toBeGreaterThan(0);
      await juger(P, A, `${theme}-milieu`);
      for (const pg of [P, A])
        await pg.evaluate(() => {
          const l = document.getElementById('feedList')!;
          l.scrollTop = l.scrollHeight;
        });
      await juger(P, A, `${theme}-bout`);
      expect(erreurs).toEqual([]);
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  });

for (const theme of ['sombre', 'clair'] as const)
  test(`le menu ⇅ du Fil, ses tris et ses filtres, comme le prototype : ${theme}`, async ({ browser }) => {
    const ls = { ...stockageFiches(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
    const { P, A, erreurs } = await deuxPilotes(browser, ls);
    try {
      mkdirSync(RES, { recursive: true });
      // la sonde (sur « … sombre ») : « Paroles tenues » ne filtre plus
      if (sonde('fil-filtre-sourd'))
        await A.evaluate(() => {
          document.addEventListener(
            'pointerup',
            (ev) => {
              if ((ev.target as Element | null)?.closest('[data-filt="tenues"]')) ev.stopImmediatePropagation();
            },
            true,
          );
        });
      await ouvrirFil(P, A);
      await toucherDeux(P, A, '#fdTriBtn');
      await juger(P, A, `${theme}-menu`);
      for (const sel of [
        '#fdMenu [data-tri="personne"]',
        '#fdMenu [data-tri="nuee"]',
        '#fdMenu [data-tri="recent"]',
        '#fdMenu [data-filt="tenues"]',
        '#fdMenu [data-filt="agir"]',
        '#fdMenu [data-filt="moi"]',
      ]) {
        if (!(await A.evaluate(() => document.getElementById('fdMenu')!.classList.contains('on'))))
          await toucherDeux(P, A, '#fdTriBtn');
        await toucherDeux(P, A, sel);
        expect(await bandeaux(A), `${sel} : les bandeaux`).toEqual(await bandeaux(P));
        await juger(P, A, `${theme}-${sel.replace(/[^a-z]/g, '')}`);
      }
      expect(erreurs).toEqual([]);
    } finally {
      await Promise.all([P.context().close(), A.context().close()]);
    }
  });

/** le texte de l'écran vide (ses deux lignes), ou rien */
const vide = (pg: Page): Promise<string> =>
  pg.evaluate(() => [...document.querySelectorAll('#feedList .e4v > *')].map((e) => e.textContent).join(' / '));

test('les écrans vides du Fil (E4, v178c) et leur seconde ligne, comme le prototype', async ({ browser }) => {
  const { P, A, erreurs } = await deuxPilotes(browser, stockageFiches());
  try {
    mkdirSync(RES, { recursive: true });
    // la sonde : la seconde ligne de la recherche vide ne mène plus à rien
    if (sonde('fil-vide-sourd')) await A.addStyleTag({ content: '#feedView .e4-l2{pointer-events:none!important}' });
    await ouvrirFil(P, A);
    const tout = await bandeaux(P);
    for (const pg of [P, A])
      await pg.evaluate(() => {
        const i = document.getElementById('fdSearch') as HTMLInputElement;
        i.value = 'zzz';
        i.dispatchEvent(new Event('input', { bubbles: true }));
      });
    await poser(P, A, 3);
    const mots = 'Rien pour «\u00a0zzz\u00a0». / Revenir à tout le Fil.';
    expect(await vide(A)).toBe(mots);
    expect(await vide(P)).toBe(mots);
    await juger(P, A, 'vide-recherche');
    await toucherDeux(P, A, '#feedList .e4-l2');
    expect(await bandeaux(A), 'la seconde ligne rend tout le Fil').toEqual(tout);
    expect(await bandeaux(P)).toEqual(tout);
    // « Demandes » : aucune → « Rien sous ce tri. »
    await toucherDeux(P, A, '#fdTriBtn');
    await toucherDeux(P, A, '#fdMenu [data-filt="demandes"]');
    expect(await vide(A)).toBe('Rien sous ce tri. / Revenir à tout le Fil.');
    expect(await vide(P)).toBe('Rien sous ce tri. / Revenir à tout le Fil.');
    await juger(P, A, 'vide-tri');
    await toucherDeux(P, A, '#feedList .e4-l2');
    expect(await bandeaux(A)).toEqual(tout);
    expect(erreurs).toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});

test("un bandeau du Fil ouvre sa fiche ; son X ramène le Fil tel qu'il était (C-250)", async ({ browser }) => {
  const { P, A, erreurs } = await deuxPilotes(browser, stockageFiches());
  try {
    mkdirSync(RES, { recursive: true });
    if (sonde('fil-retour-en-haut'))
      await A.evaluate(() => {
        document.querySelector('#detailPoster .closeb')!.addEventListener('pointerup', () => {
          document.getElementById('feedList')!.scrollTop = 0;
        });
      });
    await ouvrirFil(P, A);
    for (const pg of [P, A])
      await pg.evaluate(() => {
        document.getElementById('feedList')!.scrollTop = 700;
      });
    await poser(P, A, 2);
    // « nager jeudi » (161), à la même place des deux côtés
    await toucherDeux(P, A, '#feedList .s4-carte[data-pid="161"]');
    await poser(P, A, 4);
    const ouverte = async (pg: Page): Promise<string> =>
      pg.evaluate(() => {
        const f = document.getElementById('detailPoster')!;
        const vu = !f.hidden && getComputedStyle(f).display !== 'none' && f.getBoundingClientRect().top < 100;
        return vu ? (document.getElementById('dptTitre')?.textContent ?? '').trim() : '';
      });
    expect(await ouverte(A), 'la fiche du bandeau touché').toBe('nager jeudi');
    expect(await ouverte(P), 'le prototype aussi').toBe('nager jeudi');
    await toucherDeux(P, A, '#detailPoster .closeb');
    await poser(P, A, 4);
    expect(await ouverte(A), 'la fiche refermée').toBe('');
    expect(await A.evaluate(`${P_}.fil().ouvert()`), 'le Fil est là').toBe(true);
    expect(await A.evaluate(() => document.getElementById('feedList')!.scrollTop)).toBe(
      await P.evaluate(() => document.getElementById('feedList')!.scrollTop),
    );
    await juger(P, A, 'retour');
    expect(erreurs).toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});

test("le Fil glisse de la droite à l'ouverture et y repart au X, jamais d'un coup (C-271 ; le prototype : fil-cote, 0,34 s)", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, stockageFiches());
  if (sonde('fil-sec')) await page.addStyleTag({ content: '#feedView{transition:none!important}' });
  const releve = (
    geste: string,
  ): string => `(() => { ${geste}; const e = document.getElementById('feedView'); e.getBoundingClientRect();
    const t = e.getAnimations().find((a) => a.transitionProperty === 'transform'); if (!t) return null;
    const D = t.effect.getComputedTiming().duration; t.pause(); const v = [];
    for (const f of [0, 0.25, 0.5, 0.75, 1]) { t.currentTime = D * f; v.push(Math.round(e.getBoundingClientRect().left * 10) / 10); }
    t.finish(); return { D, v }; })()`;
  type Releve = { D: number; v: number[] } | null;
  const m = (await page.evaluate(releve(`${P_}.fil().ouvrir()`))) as Releve;
  expect(m, 'une transition de la place à l’ouverture').not.toBeNull();
  expect(m!.D, 'en 0,34 s (le prototype : fil-cote)').toBe(340);
  expect(m!.v[0], 'il part de la droite').toBeGreaterThan(380);
  expect(
    m!.v.slice(1, 4).every((x, i) => x > 1 && x < 389 && x < m!.v[i]!),
    `il glisse, image après image (${m!.v.join(' → ')})`,
  ).toBe(true);
  expect(m!.v[4], 'arrivé').toBeLessThan(1);
  expect(
    await page.evaluate(() => getComputedStyle(document.getElementById('accPlat')!).display),
    "l'accueil s'efface",
  ).toBe('none');
  await page.waitForTimeout(600);
  const d = (await page.evaluate(
    releve(`(() => { const x = document.querySelector('#feedView .closeb'); const r = x.getBoundingClientRect();
      const o = { bubbles: true, clientX: r.left + r.width / 2, clientY: r.top + r.height / 2, pointerId: 1, pointerType: 'touch', isPrimary: true };
      x.dispatchEvent(new PointerEvent('pointerdown', o)); x.dispatchEvent(new PointerEvent('pointerup', o)); x.dispatchEvent(new MouseEvent('click', o)); })()`),
  )) as Releve;
  expect(d, 'une transition de la place au X').not.toBeNull();
  expect(
    d!.v.slice(1, 4).every((x, i) => x > 1 && x < 389 && x > d!.v[i]!),
    `il repart, image après image (${d!.v.join(' → ')})`,
  ).toBe(true);
  await expect
    .poll(() => page.evaluate(() => document.getElementById('feedView')!.hidden), {
      message: 'caché à la fin',
      timeout: 5000,
    })
    .toBe(true);
});
