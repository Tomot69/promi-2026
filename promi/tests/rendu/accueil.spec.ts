/**
 * LOT 1 — L'ACCUEIL ET LA TOILE VIVANTE.
 *
 * (1) IDENTITÉ AU PIXEL (la règle de la vraie app) : l'accueil de la vraie app à 390 × 844 contre celui du prototype (son appareil, dans la
 *     fenêtre du banc), même état importé des deux côtés, même WebKit, ×3, clair et sombre, menu du + fermé et ouvert. La Toile est masquée
 *     des deux côtés (elle est jugée au pixel par banc-rendu.spec et entrees.spec) et les animations gelées (le I qui clignote, l'anneau
 *     qui tourne : leur nom et leur durée sont jugés à part). Seuls les coins arrondis du téléphone que le prototype dessine sont exceptés.
 *     Tolérance : 2 niveaux sur 255 (l'anticrénelage du compositeur), 0 pixel au-delà.
 * (2) LES GESTES (SPEC-ECRANS §1) : toucher une dalle demande SA fiche, 260 ms plus tard ; le double toucher recadre ; le + ouvre les
 *     natures sur place, une pilule demande la page + de sa nature, un toucher ailleurs referme ; chaque entrée de la barre demande son
 *     écran sur toute sa zone (C-106) ; le symbole « recadrer » naît quand la main bouge la vue, part après 4 s (C-188) ; la Toile vit au
 *     repos sous l'accueil (C-028) ; « Plus tard » deux fois, le bandeau ne revient plus (C-200 ①).
 */
import { test, expect } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { ETAT, RESULTATS, stockage, GEL, prototype, vraieApp, ouvrirPlus, ecart, P_, sonde } from './aides.ts';

for (const theme of ['sombre', 'clair'] as const)
  for (const menu of [false, true])
    test(`identité au pixel : l'accueil${menu ? ', menu du + ouvert' : ''}, ${theme}`, async ({ browser }) => {
      const ls = { ...stockage(), promi_theme: theme === 'clair' ? 'light' : 'dark' };
      const P = await (
        await browser.newContext({ viewport: { width: 430, height: 932 }, deviceScaleFactor: 3 })
      ).newPage();
      const A = await (
        await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3 })
      ).newPage();
      const erreurs: string[] = [];
      A.on('pageerror', (e) => erreurs.push(String(e)));
      await Promise.all([prototype(P, ls), vraieApp(A, ls)]);
      for (const pg of [P, A]) await pg.addStyleTag({ content: GEL });
      await P.waitForTimeout(600);
      if (menu) await Promise.all([ouvrirPlus(P), ouvrirPlus(A)]);
      const dv = await P.evaluate(() => {
        const r = document.getElementById('device')!.getBoundingClientRect();
        return { x: r.left, y: r.top, width: r.width, height: r.height };
      });
      const ip = await P.screenshot({ clip: dv });
      const ia = await A.screenshot();
      mkdirSync(RESULTATS, { recursive: true });
      const nom = `${theme}${menu ? '-menu' : ''}`;
      writeFileSync(join(RESULTATS, `${nom}-prototype.png`), ip);
      writeFileSync(join(RESULTATS, `${nom}-app.png`), ia);
      const e = ecart(ip, ia);
      expect(erreurs).toEqual([]);
      expect(
        { n: e.n, boite: e.boite },
        `pixels écartés de plus de 2 niveaux (état : ${ETAT} ; bords lissés exceptés hors macOS : ${String(e.bords)})`,
      ).toEqual({ n: 0, boite: null });
    });

test("les animations de l'accueil : le I de PROMI clignote, l'anneau du + tourne", async ({ page }) => {
  await vraieApp(page, stockage());
  const r = await page.evaluate(() => {
    const i = getComputedStyle(document.querySelector('.acc-mm i')!);
    const b = getComputedStyle(document.getElementById('createBtn')!, '::before');
    return {
      i: [i.animationName, i.animationDuration, i.animationTimingFunction],
      anneau: [b.animationName, b.animationDuration, b.animationTimingFunction],
    };
  });
  expect(r.i).toEqual(['promiBlink', '1.15s', 'steps(1)']);
  expect(r.anneau).toEqual(['heroSpin', '100s', 'linear']);
});

test('toucher une dalle demande SA fiche, 260 ms plus tard ; le double toucher recadre', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, stockage());
  // les dalles des paroles, à l'écran, hors du plateau et de la barre
  const dalles = (await page.evaluate(`(() => {
    const L = Toile_lecture(); const out = [];
    for (const g of L.graines) { if (g.kind === 'gray' || g.pid == null) continue;
      const x = g.x * L.vue.s + L.vue.ox, y = g.y * L.vue.s + L.vue.oy;
      if (x < 10 || x > 380 || y < 120 || y > 690) continue;
      const h = Toile.hit(x, y); if (h && h.pid === g.pid) out.push({ pid: g.pid, x, y }); }
    return out; })()`)) as Array<{ pid: number; x: number; y: number }>;
  expect(dalles.length, 'au moins une dalle de parole touchable').toBeGreaterThan(0);
  // l'heure du lever du doigt, à l'horloge de l'app (celle de la navigation) : la demande vient 260 ms après, jamais avant
  await page.evaluate(() => {
    const w = window as unknown as { __leve: number[]; __promi: { horloge: { maintenant(): number } } };
    w.__leve = [];
    window.addEventListener('pointerup', () => w.__leve.push(w.__promi.horloge.maintenant()), true);
  });
  for (const d of dalles.slice(0, 6)) {
    const avant = (await page.evaluate(`${P_}.nav.journal().length`)) as number;
    await page.mouse.click(d.x, d.y);
    await page.waitForFunction(
      (n) => (window as unknown as { __promi: { nav: { journal(): unknown[] } } }).__promi.nav.journal().length > n,
      avant,
      { timeout: 5000 },
    );
    const j = (await page.evaluate(`${P_}.nav.journal()`)) as Array<{ vers: string; arg?: number; t: number }>;
    const leve = (await page.evaluate('window.__leve.at(-1)')) as number;
    expect(j.slice(avant), `la dalle ${String(d.pid)}`).toEqual([
      expect.objectContaining({ vers: 'fiche', arg: d.pid }),
    ]);
    expect(j.at(-1)!.t - leve, 'la fiche est demandée 260 ms après le lever du doigt').toBeGreaterThanOrEqual(259);
    await page.waitForTimeout(400);
  }
  // le double toucher : la vue glissée à la main revient au cadrage
  await page.mouse.move(195, 400);
  await page.mouse.down();
  await page.mouse.move(150, 360, { steps: 8 });
  await page.mouse.up();
  await page.waitForTimeout(600);
  expect(await page.evaluate(`${P_}.facade.vueALaMain()`)).toBe(true);
  // la vue immobile (sur la CI, une image toutes les 0,7 s : son retour élastique y dure des dizaines de secondes), puis un point sans
  // aucune dalle de parole à 30 pt à la ronde (sur une dalle, ou à 22 pt d'une petite — C-239 —, la fiche serait demandée 260 ms après
  // le premier toucher, et le second toucher ne serait plus un double)
  await page.evaluate(async () => {
    const lit = (): string => {
      const v = (window as unknown as { Toile_vueLue(): { s: number; ox: number; oy: number } }).Toile_vueLue();
      return `${v.s.toFixed(4)}|${v.ox.toFixed(2)}|${v.oy.toFixed(2)}`;
    };
    let avant = lit();
    let depuis = performance.now();
    const t0 = performance.now();
    while (performance.now() - depuis < 1500 && performance.now() - t0 < 120000) {
      await new Promise((f) => setTimeout(f, 100));
      const s = lit();
      if (s !== avant) {
        avant = s;
        depuis = performance.now();
      }
    }
  });
  const vide = (await page.evaluate(`(() => {
    const libre = (x, y) => { for (let r = 0; r <= 30; r += 6) for (let a = 0; a < 16; a++) {
      const h = Toile.hit(x + r * Math.cos(a * Math.PI / 8), y + r * Math.sin(a * Math.PI / 8));
      if (h && (h.pid != null || h.kind === 'nuee')) return false; } return true; };
    for (let y = 200; y < 680; y += 9) for (let x = 40; x < 350; x += 9) if (libre(x, y)) return [x, y];
    return null; })()`)) as [number, number] | null;
  expect(vide, 'un point sans dalle à 30 pt à la ronde').not.toBeNull();
  await page.mouse.click(vide![0], vide![1]);
  await page.waitForTimeout(80);
  await page.mouse.click(vide![0], vide![1]);
  await page.waitForTimeout(600);
  expect(
    await page.evaluate(`${P_}.facade.vueALaMain()`),
    `le double toucher recadre (doigts posés vus par la Toile : ${String(await page.evaluate(() => document.getElementById('stage')!.dataset['doigts']))})`,
  ).toBe(false);
});

// C-101 (v142) et L1 (Tom, 20 nov. 2026) : « un appui de 0,8 s sur une dalle la détache ; elle suit le doigt ; au lâcher elle reste où on l'a
// posée, sa place est gardée ». Le moteur le fait (repris) ; l'app doit (1) laisser l'appui long au moteur — dans Safari d'iOS, une page qui
// permet la sélection de texte la lance vers 0,7 s (loupe, « Copier ») et la dalle ne bouge plus : c'était la régression du prototype —, et
// (2) garder la place que le moteur note. Valeurs décidées, en dur : 800 ms ; « sous le doigt » = 50 pt au plus du lâcher.
test("déplacer une dalle (C-101) : la page laisse l'appui long au moteur, la dalle suit le doigt, aucune fiche, sa place est gardée", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, stockage());
  // la sonde : la version fautive du prototype (la Toile permet la sélection de texte d'iOS)
  if (sonde('deplace-selection'))
    await page.addStyleTag({
      content: 'html,body,#stage,#toileCv{-webkit-user-select:text!important;user-select:text!important}',
    });
  // (1) la sélection de texte et le menu de l'appui long interdits sur la Toile ; le WebKit du Mac ne connaît pas -webkit-touch-callout
  // (il le jette au chargement) : il se lit dans le TEXTE des feuilles de la page
  const sel = (await page.evaluate(async () => {
    let txt = [...document.querySelectorAll('style')].map((s) => s.textContent).join('\n');
    for (const l of document.querySelectorAll<HTMLLinkElement>('link[rel=stylesheet]'))
      txt += await (await fetch(l.href)).text();
    txt = txt.replace(/\/\*[\s\S]*?\*\//g, '');
    const regles: string[] = [];
    for (const m of txt.matchAll(/([^{}]+)\{([^{}]*)\}/g))
      if (/-webkit-touch-callout\s*:\s*none/.test(m[2]!)) regles.push(m[1]!.trim());
    return ['stage', 'toileCv'].map((i) => {
      const e = document.getElementById(i)!;
      const s = getComputedStyle(e) as CSSStyleDeclaration & { webkitUserSelect?: string };
      const herite = (x: Element | null): boolean => {
        for (; x; x = x.parentElement)
          if (
            regles.some((r) =>
              r.split(',').some((q) => {
                try {
                  return x!.matches(q.trim());
                } catch {
                  return false;
                }
              }),
            )
          )
            return true;
        return false;
      };
      return [i, s.webkitUserSelect || s.userSelect, herite(e) ? 'none' : 'absent'];
    });
  })) as Array<[string, string, string]>;
  expect(sel, "la Toile interdit la sélection de texte et le menu de l'appui long").toEqual([
    ['stage', 'none', 'none'],
    ['toileCv', 'none', 'none'],
  ]);
  expect(await page.evaluate('window.Toile_tireRegle && Toile_tireRegle.MS'), 'la règle : 800 ms').toBe(800);
  // une dalle de parole, loin des bords
  const lire = `(() => { const L = Toile_lecture(); const out = [];
    for (const g of L.graines) { if (g.kind === 'gray' || g.pid == null) continue;
      const x = g.x * L.vue.s + L.vue.ox, y = g.y * L.vue.s + L.vue.oy; out.push({ pid: g.pid, x, y, tx: g.x, ty: g.y }); }
    return out; })()`;
  type D = { pid: number; x: number; y: number; tx: number; ty: number };
  const dalles = ((await page.evaluate(lire)) as D[]).filter((d) => d.x > 60 && d.x < 330 && d.y > 180 && d.y < 600);
  const a = dalles[0];
  expect(a, 'une dalle de parole loin des bords').toBeTruthy();
  const d0 = a!;
  const vers = (dx: number, dy: number): [number, number] => {
    const n = Math.hypot(195 - d0.x, 420 - d0.y) || 1;
    return n >= 60
      ? [d0.x + ((195 - d0.x) / n) * 110 + dx, d0.y + ((420 - d0.y) / n) * 110 + dy]
      : [d0.x + 90 + dx, d0.y + 90 + dy];
  };
  await page.evaluate(() => {
    const w = window as unknown as { __tire: number; Toile_tire(): unknown };
    w.__tire = 0;
    setInterval(() => {
      if (w.Toile_tire()) w.__tire++;
    }, 30);
  });
  const journal0 = (await page.evaluate(`${P_}.nav.journal().length`)) as number;
  // un glissé SANS attendre ne détache rien
  await page.mouse.move(d0.x, d0.y);
  await page.mouse.down();
  await page.waitForTimeout(150);
  await page.mouse.move(d0.x + 40, d0.y + 50, { steps: 8 });
  await page.mouse.up();
  await page.waitForTimeout(900);
  expect(await page.evaluate('window.__tire'), 'un glissé sans attendre 0,8 s ne détache aucune dalle').toBe(0);
  // la vue a pu glisser : on relit la dalle, puis l'appui de 0,95 s et le glissé
  const d1 = ((await page.evaluate(lire)) as D[]).find((d) => d.pid === d0.pid)!;
  Object.assign(d0, d1);
  const [x1, y1] = vers(0, 0);
  await page.mouse.move(d0.x, d0.y);
  await page.mouse.down();
  await page.waitForTimeout(950);
  await page.mouse.move(x1, y1, { steps: 14 });
  const prise = (await page.evaluate('window.__tire')) as number;
  await page.mouse.up();
  expect(prise, 'la dalle est attrapée pendant le geste').toBeGreaterThan(0);
  // elle finit sous le doigt (la Toile se repose : sur la CI une image toutes les 0,7 s)
  await page.waitForFunction(
    ([pid, x, y]) => {
      const L = (
        window as unknown as { Toile_lecture(): { graines: D[]; vue: { s: number; ox: number; oy: number } } }
      ).Toile_lecture();
      const g = L.graines.find((q) => q.pid === pid);
      return !!g && Math.hypot(g.x * L.vue.s + L.vue.ox - x!, g.y * L.vue.s + L.vue.oy - y!) <= 50;
    },
    [d0.pid, x1, y1],
    { timeout: 60000 },
  );
  await page.waitForTimeout(1200);
  const d2 = ((await page.evaluate(lire)) as D[]).find((d) => d.pid === d0.pid)!;
  expect(Math.hypot(d2.x - d0.x, d2.y - d0.y), 'à plus de 60 pt de son départ').toBeGreaterThanOrEqual(60);
  expect(((await page.evaluate(`${P_}.nav.journal()`)) as unknown[]).slice(journal0), 'aucune fiche demandée').toEqual(
    [],
  );
  // sa place est gardée par le magasin (le moteur la note : [x/W, y/H, famille])
  const place = (await page.evaluate(
    `(() => { const p = ${P_}.magasin.etat().paroles.find((q) => q.id === ${String(d0.pid)}); const L = Toile_lecture(); return p && p.place ? [p.place[0] * L.W, p.place[1] * L.H] : null; })()`,
  )) as [number, number] | null;
  expect(place, 'la place notée par le moteur est dans le magasin').not.toBeNull();
  expect(
    Math.hypot(place![0] - d2.tx, place![1] - d2.ty),
    'la place gardée est celle où la dalle a été posée (≤ 30 pt de Toile)',
  ).toBeLessThanOrEqual(30);
});

test('la barre : chaque entrée demande son écran sur toute sa zone ; le + ouvre les natures, une pilule sa page +, ailleurs referme', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, stockage());
  const zones = (await page.evaluate(() =>
    ['studioBtn', 'souffleBtn', 'indexBtn', 'filBtn'].map((id) => {
      const r = document.getElementById(id)!.getBoundingClientRect();
      return [id, r.left, r.top, r.width, r.height] as const;
    }),
  )) as Array<[string, number, number, number, number]>;
  const attendu: Record<string, string> = { studioBtn: 'studio', souffleBtn: 'aura', indexBtn: 'index', filBtn: 'fil' };
  for (const [id, x, y, w, h] of zones)
    for (const [fx, fy] of [
      [0.15, 0.15],
      [0.5, 0.5],
      [0.85, 0.85],
      [0.5, 0.95],
    ] as const) {
      await page.mouse.click(x + w * fx, y + h * fy);
      await page.waitForTimeout(60);
      const j = (await page.evaluate(`${P_}.nav.journal()`)) as Array<{ vers: string }>;
      expect(j.at(-1)?.vers, `${id} à (${String(fx)}, ${String(fy)})`).toBe(attendu[id]);
    }
  await ouvrirPlus(page);
  expect(await page.evaluate(() => document.getElementById('accChoix')!.classList.contains('ouvert'))).toBe(true);
  await page.mouse.click(195, 300); // ailleurs
  await page.waitForTimeout(100);
  expect(
    await page.evaluate(() => document.getElementById('accChoix')!.classList.contains('ouvert')),
    'un toucher ailleurs referme',
  ).toBe(false);
  for (const k of ['nuee', 'chiche', 'promi']) {
    await ouvrirPlus(page);
    const r = await page.evaluate((k) => {
      const b = document.querySelector(`#accChoix .acc-pil[data-k="${k}"]`)!.getBoundingClientRect();
      return [b.left + b.width / 2, b.top + b.height / 2];
    }, k);
    await page.mouse.click(r[0]!, r[1]!);
    await page.waitForTimeout(80);
    const j = (await page.evaluate(`${P_}.nav.journal()`)) as Array<{ vers: string; arg?: string }>;
    expect(j.at(-1)).toEqual(expect.objectContaining({ vers: 'pagePlus', arg: k }));
    expect(await page.evaluate(() => document.getElementById('accChoix')!.classList.contains('ouvert'))).toBe(false);
  }
});

test('le symbole « recadrer » naît quand la main bouge la vue, part après 4 s sans toucher, et recadre', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, stockage());
  const vu = (): Promise<boolean> =>
    page.evaluate(() => document.getElementById('accRecadre')!.classList.contains('vu'));
  expect(await vu(), 'absent au repos').toBe(false);
  await page.mouse.move(195, 420);
  await page.mouse.down();
  await page.mouse.move(140, 380, { steps: 10 });
  await page.mouse.up();
  await page.waitForTimeout(700);
  expect(
    await vu(),
    `paru quand la main a bougé la vue (${String(await page.evaluate(`${P_}.facade.vueALaMain()`))}, ${await page.evaluate(() => (window as unknown as { __promi: { accueil(): { etatRecadre(): { etat: string } } } }).__promi.accueil().etatRecadre().etat)})`,
  ).toBe(true);
  // la vue revient seule dans ses bornes (l'élastique du moteur) : les 4 s comptent depuis son DERNIER mouvement. Mesuré DANS la page, à
  // l'horloge de l'app (une machine lente rend chaque aller-retour du test plus long que la seconde ; sur la CI, sans carte graphique, la
  // Toile rend une image toutes les 0,7 s et la vue met plus de 30 s à revenir dans ses bornes — mesuré le 20 nov.) : le symbole est encore là quand la
  // vue est immobile depuis 3,5 s, et il part avant 4 s + 300 ms de flaques + 1 s de marge
  const attente = await page.evaluate(async () => {
    const a = (
      window as unknown as { __promi: { accueil(): { etatRecadre(): { etat: string; depuis: number } } } }
    ).__promi.accueil();
    let derniereLa = -1;
    const t0 = performance.now();
    const vues: string[] = [];
    for (;;) {
      const e = a.etatRecadre();
      const L = (
        window as unknown as { Toile_lecture(): { W: number; H: number; vue: { s: number; ox: number; oy: number } } }
      ).Toile_lecture();
      vues.push(`${L.vue.s.toFixed(4)}|${L.vue.ox.toFixed(2)}|${L.vue.oy.toFixed(2)}|${String(L.W)}x${String(L.H)}`);
      if (vues.length > 10) vues.shift();
      if (e.etat === 'la') derniereLa = e.depuis;
      if (e.etat === 'absent') return { derniereLa, absent: e.depuis };
      if (performance.now() - t0 > 120000)
        return { derniereLa, absent: -1, etat: e.etat, vues, remises: (e as unknown as { remises: unknown }).remises };
      await new Promise((f) => setTimeout(f, 50));
    }
  });
  expect(
    attente.derniereLa,
    `encore là 3,5 s après le dernier mouvement (${JSON.stringify(attente)})`,
  ).toBeGreaterThanOrEqual(3500);
  expect(attente.absent, `parti avant 5,3 s (${JSON.stringify(attente)})`).toBeGreaterThan(0);
  expect(attente.absent).toBeLessThanOrEqual(5300);
  await page.mouse.move(195, 420);
  await page.mouse.down();
  await page.mouse.move(250, 470, { steps: 10 });
  await page.mouse.up();
  await page.waitForTimeout(700);
  expect(await vu(), 'revenu au déplacement suivant').toBe(true);
  const r = await page.evaluate(() => {
    const b = document.getElementById('accRecadre')!.getBoundingClientRect();
    return [b.left + b.width / 2, b.top + b.height / 2, b.right, b.bottom];
  });
  // l'encre (22 pt) finit sur la marge (24 pt du bord) et 12 pt au-dessus de la barre
  expect(Math.round(r[2]! - 11)).toBe(390 - 24);
  await page.mouse.click(r[0]!, r[1]!);
  await page.waitForTimeout(700);
  expect(await page.evaluate(`${P_}.facade.vueALaMain()`), 'le symbole recadre').toBe(false);
  // il part en flaques (300 ms d'horloge ; sur la CI, une image toutes les 0,7 s : on l'attend jusqu'à 5 s)
  await page.waitForFunction(() => !document.getElementById('accRecadre')!.classList.contains('vu'), undefined, {
    timeout: 5000,
  });
});

test("la Toile vit au repos sous l'accueil (C-028) : un mouvement est prévu, il a lieu, rien de l'accueil ne couvre le centre", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await vraieApp(page, stockage());
  // le moteur ne bouge rien dans les 5 s qui suivent un changement de la Toile (la plantation au démarrage)
  await page.waitForTimeout(5600);
  const r = (await page.evaluate(`(() => { const c = document.getElementById('toileCv').getBoundingClientRect();
    const e = document.elementFromPoint(c.left + c.width / 2, c.top + c.height * 0.45);
    return { centre: e && e.id, prevu: Toile.vivant.attend() }; })()`)) as { centre: string; prevu: boolean };
  expect(r.centre, 'le centre de la Toile est libre (la condition de la vie au repos)').toBe('toileCv');
  expect(r.prevu, 'un mouvement de repos est prévu').toBe(true);
  const avant = (await page.evaluate('Toile.vivant.journal().length')) as number;
  await page.evaluate('Toile.vivant.force()');
  await page.waitForTimeout(300);
  expect(await page.evaluate('Toile.vivant.journal().length'), 'le mouvement a eu lieu').toBeGreaterThan(avant);
});

test('le bandeau « Garder ta Toile » : paru après le troisième Promi, « Plus tard » le retire et se note', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  const ls: Record<string, string> = {
    ...stockage(),
    promi_onb: '1',
    promi_compte: '',
    promi_rappel_n: '',
    promi_rappel_non: '',
    promi_rappel_fin: '',
    promi_rappel_vu: '',
  };
  await vraieApp(page, ls);
  const vu = (): Promise<boolean> =>
    page.evaluate(() => document.getElementById('accRappel')!.classList.contains('vu'));
  const paroles = (
    JSON.parse(ls['promi_state'] ?? '{"promises":[]}') as { promises: Array<{ draft?: boolean }> }
  ).promises.filter((p) => !p.draft).length;
  if (paroles < 3) test.skip(true, "l'état porte moins de trois paroles : le bandeau ne paraît pas (la règle)");
  expect(await vu(), 'paru après le troisième Promi').toBe(true);
  const plusTard = async (): Promise<void> => {
    const r = await page.evaluate(() => {
      const b = document.querySelector('#accRappel [data-r="non"]')!.getBoundingClientRect();
      return [b.left + b.width / 2, b.top + b.height / 2];
    });
    await page.mouse.click(r[0]!, r[1]!);
    await page.waitForTimeout(100);
  };
  await plusTard();
  expect(await vu()).toBe(false);
  // le reste de la règle (le retour plus loin, la fin au second refus) : tests/unitaires/accueil.test.ts
  const autres = (await page.evaluate(`${P_}.magasin.etat().autres`)) as Record<string, string>;
  expect(autres['promi_rappel_non']).toBe('1');
  expect(autres['promi_rappel_fin'] ?? '').toBe('');
});
