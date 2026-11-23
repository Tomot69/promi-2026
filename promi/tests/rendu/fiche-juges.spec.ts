/**
 * LOT 3a-1 — LES JUGES DE LA FICHE AU REPOS, hors de l'identité au pixel (fiche.spec.ts) : ce que la comparaison masque ou ne voit pas.
 *  · les anneaux des Noyaux (M2 de fiche.spec : leur grain est masqué) — chaque angle porte la couleur du prototype (tenu `#00341A`, en cours
 *    `#291547`, le jour de 3 pt, l'anneau vide de la nature), lus au milieu de la bande ;
 *  · « + x personnes » se déroule au toucher : la phrase entière, le titre descend de la ligne gagnée (C-069) ;
 *  · une date passée s'écrit comme une date (C-160, D5) : `?jour=+N` avance aujourd'hui ;
 *  · la fiche monte du bas à l'ouverture et y redescend au X, jamais d'un coup (C-271 ; le prototype : `.poster`) ;
 *  · toucher une dalle de la Toile ouvre SA fiche (le vrai chemin).
 */
import { test, expect, type Page } from '@playwright/test';
import { prototype, vraieApp, sonde, P_, stockageFiches } from './aides.ts';

type FicheApp = { __promi: { fiche(): { ouvrir(i: number): void; fermer(): void; etat(): { id: number | null } } } };

async function app(page: Page, url = ''): Promise<void> {
  if (url) {
    await page.goto('http://127.0.0.1:5180/?banc=1' + url);
    await page.waitForFunction(() => !!(window as unknown as { __promi?: unknown }).__promi);
    await page.evaluate(async (ls) => {
      const p = (
        window as unknown as { __promi: { magasin: { importer(x: unknown): void }; demarrer(): Promise<void> } }
      ).__promi;
      p.magasin.importer({ ls });
      await p.demarrer();
    }, stockageFiches());
    await page.waitForTimeout(1500);
  } else await vraieApp(page, stockageFiches());
}

async function ouvrir(page: Page, id: number): Promise<void> {
  await page.evaluate((id) => {
    (window as unknown as FicheApp).__promi.fiche().ouvrir(id);
  }, id);
  await page.waitForTimeout(900);
}

/** la couleur de chaque anneau tous les 6°, au milieu de sa bande (en pt depuis le centre du canevas) */
const ANGLES = `(sel) => [...document.querySelectorAll(sel)].map((cv) => {
  const g = cv.getContext('2d'); const W = cv.width; const D = parseFloat(cv.style.width) || cv.getBoundingClientRect().width;
  const EP = D > 70 ? 12 : 9; const R = ((D - EP) / 2 / D) * W; const out = [];
  for (let a = 0; a < 360; a += 6) {
    const t = (a - 90) * Math.PI / 180; const d = g.getImageData(Math.round(W / 2 + R * Math.cos(t)), Math.round(W / 2 + R * Math.sin(t)), 1, 1).data;
    out.push([d[0], d[1], d[2], d[3]]);
  }
  return out; })`;

test('les anneaux des Noyaux : à chaque angle la couleur du prototype — tenu, en cours, le jour, l’anneau vide (C-210, M2)', async ({
  browser,
}) => {
  const P = await (await browser.newContext({ viewport: { width: 430, height: 932 }, deviceScaleFactor: 3 })).newPage();
  const A = await (await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3 })).newPage();
  try {
    await Promise.all([prototype(P, stockageFiches()), app(A)]);
    // la sonde : les deux couleurs d'état échangées sur les anneaux de la vraie app
    if (sonde('fiche-anneau-faux'))
      await A.addInitScript(() => {
        const f = CanvasRenderingContext2D.prototype.stroke;
        CanvasRenderingContext2D.prototype.stroke = function (this: CanvasRenderingContext2D, ...a: unknown[]) {
          if (this.canvas.classList.contains('kr-c'))
            this.strokeStyle =
              this.strokeStyle === '#00341a'
                ? '#291547'
                : this.strokeStyle === '#291547'
                  ? '#00341a'
                  : this.strokeStyle;
          (f as (...x: unknown[]) => void).apply(this, a);
        };
      });
    if (sonde('fiche-anneau-faux')) await app(A, '&s=1');
    const pb: string[] = [];
    for (const id of [156, 167, 146]) {
      await P.evaluate(
        (id) => (window as unknown as { closeAll(): void; openDetail(i: number): void }).openDetail(id),
        id,
      );
      await ouvrir(A, id);
      // les anneaux du prototype POSÉS : deux relevés identiques à 600 ms (sur une machine lente, il les peint encore à 3 s)
      let cp = (await P.evaluate(`(${ANGLES})('#detailPoster canvas.kr-c')`)) as number[][][];
      for (let k = 0; k < 30; k++) {
        await P.waitForTimeout(600);
        const c2 = (await P.evaluate(`(${ANGLES})('#detailPoster canvas.kr-c')`)) as number[][][];
        const pose = k > 2 && JSON.stringify(c2) === JSON.stringify(cp);
        cp = c2;
        if (pose) break;
      }
      const ca = (await A.evaluate(`(${ANGLES})('#detailPoster.fiche canvas.kr-c')`)) as number[][][];
      if (cp.length !== ca.length)
        pb.push(`${String(id)} : ${String(ca.length)} anneaux, le prototype ${String(cp.length)}`);
      cp.forEach((anneau, i) =>
        anneau.forEach((c, j) => {
          const d = ca[i]?.[j];
          // le jour entre deux arcs : transparent des deux côtés (seul le grain, tiré au hasard dans le prototype, s'y lit)
          if (d && c[3]! < 32 && d[3]! < 32) return;
          if (!d || Math.max(...c.map((v, k) => Math.abs(v - d[k]!))) > 8)
            pb.push(
              `${String(id)}, anneau ${String(i)}, ${String(j * 6)}° : ${JSON.stringify(d)} au lieu de ${JSON.stringify(c)}`,
            );
        }),
      );
      await P.evaluate(() => (window as unknown as { closeAll(): void }).closeAll());
      await P.waitForTimeout(800);
    }
    expect(pb.slice(0, 12), 'les anneaux ont les couleurs du prototype à chaque angle').toEqual([]);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});

test('« + x personnes » se déroule au toucher : la phrase entière, le titre descend de la ligne gagnée (C-069)', async ({
  browser,
}) => {
  const P = await (await browser.newContext({ viewport: { width: 430, height: 932 }, deviceScaleFactor: 3 })).newPage();
  const A = await (await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3 })).newPage();
  try {
    await Promise.all([prototype(P, stockageFiches()), app(A)]);
    await P.evaluate(() => (window as unknown as { openDetail(i: number): void }).openDetail(163));
    await P.waitForTimeout(3000);
    await ouvrir(A, 163);
    expect(await A.locator('#detailPoster.fiche .fi-phrase').textContent()).toBe(
      'Je promets à Rachel, Marion +\u00a03\u00a0personnes de',
    );
    // la sonde : le toucher sur « + x personnes » avalé avant d'arriver à la fiche
    if (sonde('fiche-deplie-mort'))
      await A.evaluate(() => {
        document.querySelector('#detailPoster.fiche .fi-plus')!.addEventListener('pointerdown', (e) => {
          e.stopPropagation();
        });
      });
    // le prototype : son propre chemin d'un clic sans doigt (`deroule` sur un clic de détail 0 — lot-V136-PHRASE) ; la vraie app : au doigt
    // (sur une machine chargée, une passe tardive du prototype peut recomposer sa phrase après le clic : on attend la liste entière — Adrien,
    // le dernier nom — et on ne reclique que si elle n'est pas venue ; un clic de plus la replierait)
    for (let k = 0; k < 5; k++) {
      await P.evaluate(() => {
        (document.querySelector('#dptQui .dpt-plus') as HTMLElement | null)?.click();
      });
      const ok = await P.waitForFunction(
        () => /Adrien/.test(document.getElementById('dptQui')?.textContent ?? ''),
        null,
        {
          timeout: 4000,
        },
      )
        .then(() => true)
        .catch(() => false);
      if (ok) break;
    }
    const b = await A.locator('#detailPoster.fiche .fi-plus').boundingBox();
    await A.mouse.click(b!.x + b!.width / 2, b!.y + b!.height / 2);
    await P.waitForTimeout(1500);
    await A.waitForTimeout(400);
    // la phrase et la place du titre, comme le prototype déplié (en pt de l'appareil)
    const lit = (
      sel: string,
    ): string => `(() => { const D = (document.getElementById('device') ?? document.getElementById('detailPoster')).getBoundingClientRect();
      const q = document.querySelector('${sel}'); const t = q.nextElementSibling && q.parentElement.querySelector('#dptTitre, .fi-titre');
      return [q.textContent.replace(/\\s+/g, ' ').trim(), Math.round((t.getBoundingClientRect().top - D.top) * 10) / 10]; })()`;
    const p = (await P.evaluate(lit('#dptQui'))) as [string, number];
    const a = (await A.evaluate(lit('#detailPoster.fiche .fi-phrase'))) as [string, number];
    expect(a[0], 'la liste entière').toBe('Je promets à Rachel, Marion, Nico, Lou et Adrien de');
    expect(a[0], 'la phrase du prototype dépliée').toBe(p[0]);
    expect(
      Math.abs(a[1] - p[1]),
      `le titre à la place du prototype déplié (${String(a[1])} contre ${String(p[1])})`,
    ).toBeLessThan(0.5);
  } finally {
    await Promise.all([P.context().close(), A.context().close()]);
  }
});

test('une date passée s’écrit comme une date : « EN COURS · 2 MARS » avec ?jour=+120, rien sans (C-160, D5)', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  // la sonde : `?jour` ignoré (le décalage ne passe pas)
  await app(page, sonde('fiche-jour-ignore') ? '&jourx=+120' : '&jour=+120');
  await ouvrir(page, 161);
  expect(await page.locator('#detailPoster.fiche .fi-etat').textContent()).toBe('EN COURS · 2 MARS');
  await app(page, '&x=1');
  await ouvrir(page, 161);
  expect(await page.locator('#detailPoster.fiche .fi-etat').textContent()).toBe('EN COURS');
});

test('la fiche monte du bas à l’ouverture et y redescend au X, jamais d’un coup (C-271 ; le prototype : .poster, 0,4 s)', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await app(page);
  // la sonde : la transition retirée (la fiche paraît et part d'un coup)
  if (sonde('fiche-seche')) await page.addStyleTag({ content: '#detailPoster.fiche{transition:none!important}' });
  // le relevé : toutes les 25 ms (réelles), la place calculée de la fiche — la transition s'échantillonne à chaque lecture du style, quelle que
  // soit la cadence des images (sur une machine lente, deux images seulement pendant 0,4 s)
  const releve = `(async () => { const v = []; const t0 = performance.now();
    await new Promise((ok) => { const f = () => { const e = document.getElementById('detailPoster'); const r = e.getBoundingClientRect();
      v.push([performance.now() - t0, e.hidden ? -1 : r.top, +getComputedStyle(e).opacity]); if (performance.now() - t0 < 700) setTimeout(f, 25); else ok(); }; setTimeout(f, 0); });
    return v; })()`;
  const montee = page.evaluate(releve) as Promise<number[][]>;
  await page.evaluate(() => {
    (window as unknown as FicheApp).__promi.fiche().ouvrir(144);
  });
  const m = await montee;
  const vus = m.filter((x) => x[1]! >= 0);
  expect(vus.length, 'des images pendant la montée').toBeGreaterThan(2);
  expect(
    vus.some((x) => x[1]! > 40 && x[1]! < 800),
    'une image à mi-chemin (elle monte, elle ne paraît pas d’un coup)',
  ).toBe(true);
  expect(vus.at(-1)![1], 'arrivée en haut').toBeLessThan(1);
  const descente = page.evaluate(releve) as Promise<number[][]>;
  const x = await page.locator('#detailPoster.fiche .closeb').boundingBox();
  await page.mouse.click(x!.x + x!.width / 2, x!.y + x!.height / 2);
  const d = await descente;
  expect(
    d.some((v) => v[1]! > 40 && v[1]! < 800),
    'une image à mi-chemin de la descente',
  ).toBe(true);
  expect(d.at(-1)![1], 'cachée à la fin').toBe(-1);
});

test('toucher une dalle de la Toile ouvre SA fiche (le vrai chemin), le X la referme', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await app(page);
  // une dalle de parole sous un point de l'accueil (la façade la donne : `toucher`) — on cherche sur une grille
  const cible = (await page.evaluate(`(() => { for (let y = 160; y < 680; y += 12) for (let x = 30; x < 360; x += 12) {
      const t = ${P_}.facade.toucher(x, y); if (t && t.pid != null) return [x, y, t.pid]; } return null; })()`)) as
    [number, number, number] | null;
  expect(cible, 'une dalle de parole sur l’accueil').not.toBeNull();
  await page.mouse.click(cible![0], cible![1]);
  await page.waitForTimeout(900);
  expect(await page.evaluate(() => (window as unknown as FicheApp).__promi.fiche().etat().id)).toBe(cible![2]);
  const x = await page.locator('#detailPoster.fiche .closeb').boundingBox();
  await page.mouse.click(x!.x + x!.width / 2, x!.y + x!.height / 2);
  await page.waitForTimeout(700);
  expect(await page.evaluate(() => document.getElementById('detailPoster')!.hidden)).toBe(true);
});

test('la fiche à l’échelle 0,79 (330 × 714) : chaque cote en pt est celle de 390 × 844, trois ouvertures de quatre fiches, la même (C-207, A3)', async ({
  browser,
}) => {
  // les cotes de mise en page (`offsetTop` dans la fiche, en pt) : elles ne dépendent pas de la réduction de l'appareil à l'écran
  const COTES = `(() => ['dptTrace', 'dAura', 'dptQui', 'dptTitre', 'dptQuand', 'cm5Ligne'].map((id) => { const e = document.getElementById(id);
      if (!e || e.hidden) return id + ':—'; return id + ':' + e.offsetTop.toFixed(1) + '+' + getComputedStyle(e).translate; }).join(' '))()`;
  const lire = async (vue: { width: number; height: number }): Promise<string[]> => {
    const pg = await (await browser.newContext({ viewport: vue, deviceScaleFactor: 3 })).newPage();
    try {
      await app(pg);
      // la sonde : à l'échelle réduite, la ligne d'état posée 4 pt plus haut (la faute de C-207 : une cote d'écran divisée par la mise en page)
      if (sonde('fiche-echelle') && vue.width < 390)
        await pg.addStyleTag({ content: '#detailPoster #dptQuand{translate:0 -4px!important}' });
      const out: string[] = [];
      for (const id of [148, 146, 167, 156]) {
        for (let n = 0; n < 3; n++) {
          await ouvrir(pg, id);
          out.push(String(id) + ' ' + ((await pg.evaluate(COTES)) as string));
          await pg.evaluate(() => {
            (window as unknown as FicheApp).__promi.fiche().fermer();
          });
          await pg.waitForTimeout(500);
        }
      }
      return out;
    } finally {
      await pg.context().close();
    }
  };
  const [a, b] = await Promise.all([lire({ width: 390, height: 844 }), lire({ width: 330, height: 714 })]);
  for (let i = 0; i < a.length; i += 3)
    expect(new Set(a.slice(i, i + 3)).size, `trois ouvertures, la même : ${a[i]!}`).toBe(1);
  expect(b, 'à 0,79, les mêmes cotes en pt').toEqual(a);
});
